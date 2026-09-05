<div align="center">
  <h1>微信表情包收藏</h1>
  <p>给聊天和 AI Agent 准备的一份本地表情包素材库。<br>原图、动图、描述与校验清单一起保存，换台电脑也能继续用。</p>
  <p><strong>2638 张原图 · 1850 张 GIF · 全部附带描述 · 下载后可离线使用</strong></p>
  <p>
    <a href="#开始使用">开始使用</a> ·
    <a href="#交给-agent-使用">Agent 接入</a> ·
    <a href="#搜索表情包">搜索表情包</a> ·
    <a href="./AGENTS.md">AGENTS.md</a>
  </p>
</div>

## 这是什么？

这是一个可下载、可检索、可迁移的微信表情包收藏。图片保存在 `emoticons/`，根目录的 `manifest.json` 记录每张图的相对路径、格式、大小、内容哈希和简短描述。

你可以自己挑图，也可以让有本地文件访问和图片预览能力的 AI Agent 根据聊天场景选图。比如回复“收到”、一起解决问题时击个拳，或在工作间隙来一张咖啡续命。下载完成后，选图和预览只需要本地文件，不需要登录微信或访问原来的图片下载地址。

| 收到，明白了 | 一起搞定 | 咖啡续命 |
| :---: | :---: | :---: |
| <img src="./emoticons/6d9f83cc47182ebba6c3b17285074f11.png" alt="绿色 get 对话框" width="160"> | <img src="./emoticons/43c2fbb00d5ae0255d835efa92dabe1f.png" alt="两只小手击拳" width="160"> | <img src="./emoticons/c0523659d5bf0ffd3f3fe26d1da44c43.png" alt="白猫捧咖啡，文字：咖啡续命" width="160"> |

## 开始使用

### 下载到本地

需要 Git。在希望存放素材的目录中执行：

```bash
git clone --depth 1 https://github.com/9Ashwin/sticker-ext.git
cd sticker-ext
```

当前快照的图片内容约 **1.00 GiB**，完整克隆还需要 Git 数据的额外空间。`--depth 1` 只获取最新历史，仍会下载全部图片。也可以在仓库页面选择 **Code → Download ZIP**，解压后按同样的目录结构使用；ZIP 副本不能用 `git pull` 更新。

打开 `emoticons/` 就能浏览图片；需要按内容查找时，使用下方的[搜索示例](#搜索表情包)。Python 3 只用于文档中的搜索和校验示例，手动浏览图片不需要安装它。

### 导入支持清单的工具

将包含 `manifest.json` 的**仓库根目录**作为表情包目录，交给支持本清单格式的工具导入。若工具要求特定的素材目录，应把整个仓库放到该目录下，再按工具说明导入。

导入程序应校验文件路径、格式、大小、MD5 和 SHA-256，再按内容去重。兼容的重复导入应复用已有图片；具体的描述覆盖策略由导入工具决定。

## 交给 Agent 使用

### 让 Agent 安装

可以把下面这段话发给拥有文件和终端工具的 Agent：

```text
请安装并使用 https://github.com/9Ashwin/sticker-ext 的表情包素材。
先阅读仓库根目录的 AGENTS.md，按其中的安装流程下载到本地并校验清单。
记录素材库的绝对路径，根据当前聊天语境搜索描述、预览候选，再展示合适的原图。
工作中可以经常配一张应景的表情包，每次一张，避免连续重复；不要为选图耽误任务。
```

[AGENTS.md](./AGENTS.md) 包含安装、更新、检索、展示、收藏和描述维护的完整指引。安装完成后，让 Agent 搜索“收到”并展示一张，是一个简单的使用检查。

### 在其他项目里使用

仓库内的 `AGENTS.md` 不会自动让所有其他项目加载这份素材。可以让 Agent 在需要时读取它，也可以在已有的项目指引中追加以下内容，将占位路径替换为安装后的真实绝对路径：

```text
本地表情包素材库：/absolute/path/sticker-ext
使用前读取 /absolute/path/sticker-ext/AGENTS.md。
从根目录 manifest.json 搜索描述，预览确认后展示对应原图。
工作交流中经常用一张应景表情，避免近期重复，不延误实际任务。
```

保留原有项目指引，追加这段引用即可。安装、引用指引和支持图片展示是三个不同条件；实际能否在对话里显示图片，取决于 Agent 客户端的能力。

## 功能概览

| 能力 | 用法 |
| --- | --- |
| 本地原图 | 下载后直接读取文件，不依赖账号或临时下载链接 |
| 保留动图 | 使用原始 GIF；支持动画的客户端可以直接播放 |
| 描述检索 | 根据人物、动物、文字、情绪或场景筛选 `caption` |
| 内容去重 | 用 MD5 作为文件名，配合 SHA-256 检查内容是否相同 |
| 跨设备迁移 | 克隆或复制整个目录，图片与描述一起迁移 |
| Agent 使用 | 按 `AGENTS.md` 搜索、预览并展示图片，无需运行专门的服务 |

当前快照包含 **1850 张 GIF、476 张 PNG、297 张 JPG 和 15 张 WebP**，共 **2638 张**。数量与描述以 [manifest.json](./manifest.json) 为准。

所有条目都有 Luna 生成的 `caption`，尽量包含可见主体、动作或表情、文字和适用语气。遇到画面模糊、小字或动画内容时，描述仍可能存在不确定性。Agent 应先看候选图片，再决定是否使用；没有搜索结果也不代表库里一定没有合适的图。

## 搜索表情包

在仓库根目录运行以下示例，将 `收到` 换成 `咖啡`、`击拳`、`猫` 等关键词。示例最多输出 10 条结果，包含可直接打开的绝对路径：

```bash
python3 - 收到 10 <<'PY'
import json
import sys
from pathlib import Path

root = Path.cwd().resolve()
keyword = sys.argv[1].casefold()
limit = int(sys.argv[2])
manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
matches = [item for item in manifest["items"]
           if keyword in item.get("caption", "").casefold()]
print(f"找到 {len(matches)} 条，显示前 {limit} 条")
for item in matches[:limit]:
    print(json.dumps({"path": str(root / item["filename"]),
                      "format": item["format"], "size": item["size"],
                      "caption": item.get("caption", "")}, ensure_ascii=False))
PY
```

优先预览少量候选，再挑一张符合语境的图。如果客户端支持本地 Markdown 图片，可以使用 `![收到](/实际绝对路径/sticker-ext/emoticons/文件名.png)`；如果支持附件上传，则交给对应的图片工具。客户端仅能输出文字时，应说明无法直接展示。

## 目录与清单格式

```text
sticker-ext/
├── README.md
├── AGENTS.md
├── manifest.json
├── packs.json
├── packs/
│   └── curated.json
└── emoticons/
    ├── <md5>.gif
    ├── <md5>.png
    ├── <md5>.jpg
    └── <md5>.webp
```

`manifest.json` 始终放在根目录，图片保存在 `emoticons/`。下面是从当前清单取出的一条真实记录：

```json
{
  "schema_version": 1,
  "collection": "all_local",
  "items": [
    {
      "md5": "6d9f83cc47182ebba6c3b17285074f11",
      "sha256": "4e5c587fdc28c09dc67608e346e15de43aacbd004d0530c1a93233c987e7e8c7",
      "filename": "emoticons/6d9f83cc47182ebba6c3b17285074f11.png",
      "format": "png",
      "size": 12639,
      "caption": "绿色对话框写 get，闪亮星星，明白了收到"
    }
  ]
}
```

| 字段 | 含义 |
| --- | --- |
| `schema_version` | 清单版本，当前为 `1` |
| `collection` | 集合标识，当前为 `all_local` |
| `items` | 图片条目数组 |
| `md5` | 原始文件内容的 MD5，小写十六进制，用于命名和去重 |
| `sha256` | 原始文件内容的 SHA-256，用于完整性校验 |
| `filename` | 相对仓库根目录的路径，使用 `/` 分隔 |
| `format` | `gif`、`png`、`jpg` 或 `webp` |
| `size` | 原始文件的字节数 |
| `caption` | 可搜索的简短描述；格式上可省略，当前所有条目均已填写 |

分包入口为 [packs.json](./packs.json)，其中 `all` 使用根目录清单，`curated` 使用精选候选清单；两者共享原图。包目录记录名称、描述、数量、总字节数及清单原始字节的 SHA-256 修订。完整约束与维护命令见[素材包格式](./docs/pack-format.md)。精选候选的画面与描述复核尚待完成。

## 更新与校验

Git 安装可以在仓库根目录检查并拉取更新：

```bash
git status --short
git pull --ff-only
```

如果有自己的图片或描述修改，先保存这些改动，再拉取更新；不要用强制重置覆盖本地收藏。ZIP 安装需要重新下载并解压到另一个目录，确认后再迁移自己的改动。

<details>
<summary><strong>检查全部图片的路径、大小和内容哈希（Python 3）</strong></summary>

在仓库根目录运行。此检查会读取约 1 GiB 图片，适合首次下载、更新后或维护清单时执行，无需每次选图都重跑。

```bash
python3 - <<'PY'
import hashlib
import json
import re
from pathlib import Path

root = Path.cwd().resolve()
manifest_path = root / "manifest.json"
assert not manifest_path.is_symlink(), "manifest.json must be a regular file"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
assert manifest["schema_version"] == 1, "unsupported schema_version"
assert isinstance(manifest["items"], list), "items must be an array"
media_dir = root / "emoticons"
assert media_dir.is_dir() and not media_dir.is_symlink(), "invalid emoticons directory"
seen = set()
for item in manifest["items"]:
    digest, fmt = item["md5"], item["format"]
    assert re.fullmatch(r"[0-9a-f]{32}", digest), "invalid md5"
    assert re.fullmatch(r"[0-9a-f]{64}", item["sha256"]), "invalid sha256"
    assert digest not in seen, f"duplicate: {digest}"
    assert fmt in {"gif", "png", "jpg", "webp"}, f"unsupported format: {fmt}"
    expected = f"emoticons/{digest}.{fmt}"
    assert item["filename"] == expected, f"invalid path: {item['filename']}"
    file = root / expected
    assert file.is_file() and not file.is_symlink(), f"missing or unsafe: {expected}"
    data = file.read_bytes()
    assert len(data) == item["size"], f"size mismatch: {expected}"
    assert hashlib.md5(data).hexdigest() == digest, f"md5 mismatch: {expected}"
    assert hashlib.sha256(data).hexdigest() == item["sha256"], f"sha256 mismatch: {expected}"
    seen.add(digest)
print(f"校验通过：{len(seen)} 张图片")
PY
```

这个检查验证清单与文件是否一致；画面、动画和描述是否准确，需要另行预览确认。

</details>

## 收藏与完善描述

新增图片时，保存完整原图，计算 MD5 和 SHA-256，按 `emoticons/<md5>.<format>` 放入目录，并在清单中增加对应条目。同一份图片只保留一条记录。修改描述只需要更新 `caption`，原图内容和哈希保持不变。

描述建议写成“主体 + 动作或表情 + 可见文字 + 适用语气”，例如：“白猫双手抱咖啡杯，困倦脸；文字：咖啡续命”。看不清的内容不要猜；只看到静态预览时，不要补写未观察到的动作。

欢迎通过 Pull Request 补充准确描述、修复清单问题，或添加具有相应分享权限的素材。维护步骤与检查要求见 [AGENTS.md](./AGENTS.md#维护收藏与描述)。

## 常见问题

**下载后还需要微信吗？** 不需要。图片是仓库中的普通文件，浏览和使用不依赖账号登录。

**会自动同步到微信收藏吗？** 不会。这里只提供素材与清单，聊天软件中的收藏或发送需要对应客户端操作。

**为什么动图只显示一帧？** 有些预览工具只显示静态帧。保留并使用原始 GIF 文件，在支持动画的客户端里查看。

**为什么关键词没搜到？** 当前示例是描述子串匹配，不是语义搜索。可以换同义词或按“猫”“人物”“文字”等更宽泛的标签缩小范围，然后预览候选。

**克隆完成就能让所有 Agent 自动发图吗？** 还需要让 Agent 读取使用指引，并确认当前客户端有本地文件访问和图片展示能力。

## 版权

图片的原始版权归相应作者或权利人所有。本仓库整理收集的素材，不授予未获授权的再发布、商业使用或二次分发权利。权利人可通过 [Issue](https://github.com/9Ashwin/sticker-ext/issues) 提供对应文件路径，联系更正或移除。
