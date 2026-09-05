"""Regression tests for pack publication integrity."""

import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from validate_packs import decode, manifest, validate


class PackTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        (self.root / "packs").mkdir()
        (self.root / "emoticons").mkdir()
        self.image = b"GIF89a test original"
        digest = hashlib.md5(self.image).hexdigest()
        self.item = dict(md5=digest, sha256=hashlib.sha256(self.image).hexdigest(),
                         filename=f"emoticons/{digest}.gif", format="gif", size=len(self.image))
        (self.root / self.item["filename"]).write_bytes(self.image)
        self.value = dict(schema_version=1, collection="legacy_collection", items=[self.item])
        self.write("manifest.json", self.value)
        self.write("packs/curated.json", self.value)
        self.catalog = dict(schema_version=1, packs=[
            dict(id="all", name="All", description="Full collection", manifest="manifest.json"),
            dict(id="curated", name="Curated", description="Subset", manifest="packs/curated.json")])
        self.write("packs.json", self.catalog)
        validate(self.root, refresh=True)
        self.catalog = json.loads((self.root / "packs.json").read_text())

    def write(self, name, value):
        (self.root / name).write_text(json.dumps(value), encoding="utf-8")

    def test_valid_and_legacy_manifest(self):
        self.assertEqual(validate(self.root), [("all", 1, len(self.image)), ("curated", 1, len(self.image))])
        (self.root / "packs.json").unlink()
        self.assertEqual(manifest((self.root / "manifest.json").read_bytes()), {self.item["md5"]: self.item})

    def test_raw_bytes_revision_before_parse(self):
        path = self.root / "packs/curated.json"
        path.write_bytes(path.read_bytes() + b" ")
        with self.assertRaisesRegex(ValueError, "revision mismatch"):
            validate(self.root)
        validate(self.root, refresh=True)
        validate(self.root)
        path.write_bytes(b"not json")
        with self.assertRaisesRegex(ValueError, "revision mismatch"):
            validate(self.root)

    def test_catalog_contract(self):
        for key, bad in [("manifest", "../manifest.json"), ("id", "../all"),
                         ("count", 2), ("size", True), ("manifest_sha256", "0" * 64),
                         ("name", ""), ("description", None)]:
            with self.subTest(key=key):
                catalog = copy.deepcopy(self.catalog)
                catalog["packs"][0][key] = bad
                self.write("packs.json", catalog)
                with self.assertRaises(ValueError):
                    validate(self.root)
        self.catalog["packs"].append(self.catalog["packs"][0])
        self.write("packs.json", self.catalog)
        with self.assertRaisesRegex(ValueError, "duplicate pack"):
            validate(self.root)

    def test_manifest_contract(self):
        for key, bad in [("filename", "../image.gif"), ("md5", "A" * 32),
                         ("sha256", "x"), ("format", "svg"), ("size", 0),
                         ("size", True), ("size", 32 * 1024 * 1024 + 1),
                         ("caption", "中" * 1366), ("caption", "\ud800")]:
            with self.subTest(key=key, bad=repr(bad)[:30]):
                value = copy.deepcopy(self.value)
                value["items"][0][key] = bad
                with self.assertRaises(ValueError):
                    manifest(json.dumps(value).encode())
        self.value["items"].append(self.item)
        with self.assertRaisesRegex(ValueError, "duplicate md5"):
            manifest(json.dumps(self.value).encode())

    def test_json_contract(self):
        for data in [b'{"schema_version":1,"schema_version":1}', b'\xff',
                     b'{"schema_version":true}', b'{"schema_version":2}',
                     b'{"schema_version":1,"extra":NaN}']:
            with self.subTest(data=data), self.assertRaises(ValueError):
                decode(data)

    def test_subset_and_conflict(self):
        for key, bad in [("md5", "0" * 32), ("sha256", "0" * 64)]:
            value = copy.deepcopy(self.value)
            value["items"][0][key] = bad
            value["items"][0]["filename"] = f'emoticons/{value["items"][0]["md5"]}.gif'
            self.write("packs/curated.json", value)
            before = (self.root / "packs.json").read_bytes()
            with self.assertRaisesRegex(ValueError, "subset|conflicting original"):
                validate(self.root, refresh=True)
            self.assertEqual(before, (self.root / "packs.json").read_bytes())

    def test_original_integrity(self):
        path = self.root / self.item["filename"]
        for data in [self.image[:-1], b"x" * len(self.image), self.image + b"x"]:
            path.write_bytes(data)
            with self.assertRaises(ValueError):
                validate(self.root)
        path.unlink()
        with self.assertRaises(ValueError):
            validate(self.root)
        path.write_bytes(self.image)
        (self.root / "emoticons/extra.gif").write_bytes(self.image)
        with self.assertRaisesRegex(ValueError, "unregistered"):
            validate(self.root)

    def test_symlink_rejected(self):
        path = self.root / self.item["filename"]
        path.unlink()
        path.symlink_to(self.root / "manifest.json")
        with self.assertRaisesRegex(ValueError, "symlink"):
            validate(self.root)


if __name__ == "__main__":
    unittest.main()
