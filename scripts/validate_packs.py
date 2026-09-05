"""Validate local v1 manifests, catalog revisions, and shared original files."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

MAX_JSON = 8 * 1024 * 1024
MAX_IMAGE = 32 * 1024 * 1024


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def read_file(root, name, maximum):
    path = root
    for part in Path(name).parts:
        path = path / part
        require(not path.is_symlink(), f"symlink: {name}")
    require(path.is_file(), f"missing file: {name}")
    with path.open("rb") as source:
        data = source.read(maximum + 1)
    require(len(data) <= maximum, f"file too large: {name}")
    return data


def decode(data):
    def reject_constant(value):
        raise ValueError(f"invalid JSON constant: {value}")
    result = json.loads(data.decode("utf-8"), object_pairs_hook=unique_object,
                        parse_constant=reject_constant)
    require(isinstance(result, dict), "JSON root must be an object")
    require(type(result.get("schema_version")) is int and result["schema_version"] == 1,
            "unsupported schema_version")
    return result


def hex_digest(value, length):
    return isinstance(value, str) and re.fullmatch(f"[0-9a-f]{{{length}}}", value)


def manifest(data):
    value = decode(data)
    require(isinstance(value.get("collection"), str), "collection must be a string")
    value["collection"].encode("utf-8")
    items = value.get("items")
    require(isinstance(items, list) and len(items) <= 20000, "invalid items")
    seen = {}
    for item in items:
        require(isinstance(item, dict), "item must be an object")
        digest, fmt = item.get("md5"), item.get("format")
        require(hex_digest(digest, 32), "invalid md5")
        require(hex_digest(item.get("sha256"), 64), "invalid sha256")
        require(digest not in seen, f"duplicate md5: {digest}")
        require(fmt in ("gif", "png", "jpg", "webp"), "invalid format")
        require(item.get("filename") == f"emoticons/{digest}.{fmt}", "invalid filename")
        require(type(item.get("size")) is int and 0 < item["size"] <= MAX_IMAGE,
                "invalid image size")
        caption = item.get("caption", "")
        require(isinstance(caption, str) and len(caption.encode("utf-8")) <= 4096,
                "invalid caption")
        seen[digest] = item
    require(list(seen) == sorted(seen), "items must be sorted by md5")
    return seen


def validate(root, refresh=False):
    root = Path(root).absolute()
    catalog = decode(read_file(root, "packs.json", MAX_JSON))
    packs = catalog.get("packs")
    require(isinstance(packs, list), "packs must be an array")
    manifests, seen = {}, set()
    for pack in packs:
        require(isinstance(pack, dict), "pack must be an object")
        pack_id = pack.get("id")
        require(isinstance(pack_id, str) and re.fullmatch(r"[a-z][a-z0-9_-]{0,63}", pack_id),
                "invalid pack id")
        require(pack_id not in seen, "duplicate pack id")
        seen.add(pack_id)
        for key in ("name", "description"):
            require(isinstance(pack.get(key), str) and bool(pack[key].strip()), f"missing {key}")
            pack[key].encode("utf-8")
        expected = "manifest.json" if pack_id == "all" else f"packs/{pack_id}.json"
        require(pack.get("manifest") == expected, "invalid manifest path")
        data = read_file(root, expected, MAX_JSON)
        revision = hashlib.sha256(data).hexdigest()
        if not refresh:
            require(hex_digest(pack.get("manifest_sha256"), 64) and
                    pack["manifest_sha256"] == revision, f"revision mismatch: {pack_id}")
        items = manifest(data)
        summary = {"manifest_sha256": revision, "count": len(items),
                   "size": sum(item["size"] for item in items.values())}
        if refresh:
            pack.update(summary)
        else:
            for key in ("count", "size"):
                require(type(pack.get(key)) is int and pack[key] == summary[key],
                        f"{key} mismatch: {pack_id}")
        manifests[pack_id] = items
    require("all" in manifests and "curated" in manifests, "all and curated packs required")
    originals = manifests["all"]
    for pack_id, items in manifests.items():
        for digest, item in items.items():
            require(digest in originals, f"not a full-manifest subset: {pack_id}/{digest}")
            require(all(item[key] == originals[digest][key]
                        for key in ("sha256", "filename", "format", "size")),
                    f"conflicting original: {pack_id}/{digest}")
    media = root / "emoticons"
    require(media.is_dir() and not media.is_symlink(), "invalid emoticons directory")
    expected_files = {item["filename"] for item in originals.values()}
    actual_files = {str(path.relative_to(root)).replace("\\", "/") for path in media.rglob("*")}
    require(actual_files == expected_files, "missing or unregistered original files")
    for digest, item in originals.items():
        data = read_file(root, item["filename"], item["size"])
        require(len(data) == item["size"], f"size mismatch: {digest}")
        require(hashlib.md5(data).hexdigest() == digest, f"md5 mismatch: {digest}")
        require(hashlib.sha256(data).hexdigest() == item["sha256"], f"sha256 mismatch: {digest}")
    if refresh:
        (root / "packs.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n",
                                         encoding="utf-8")
    return [(pack["id"], pack["count"], pack["size"]) for pack in packs]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--refresh", action="store_true",
                        help="recompute catalog revision/count/size after validating all originals")
    args = parser.parse_args()
    try:
        for pack_id, count, size in validate(args.root, args.refresh):
            print(f"OK {pack_id}: {count} images, {size} bytes")
    except (ValueError, OSError) as error:
        print(f"Validation failed: {error}", file=sys.stderr)
        sys.exit(1)
