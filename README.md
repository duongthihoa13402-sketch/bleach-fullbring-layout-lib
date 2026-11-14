# Bleach Fullbring Arc (c425–c478) Manga Layout & Reference Library

本仓库包含《死神·完现术篇》（50 话 / 1,075 页 / 4,276 个分格）的全量版式语法、逐页人工核验 JSON 索引、以及全部章节原图与场景分类参考图，专供 **ChatGPT / Codex** 自动检索版式、配标签并调用参考图生成漫画页。

## 1. 核心入口文件（供 ChatGPT / Codex 直接读取）

| 文件 | 路径 / 链接 | 用途 |
|---|---|---|
| **Codex 排版规范提示词 (v3)** | [`CODEX-PROMPT.md`](https://cdn.jsdelivr.net/gh/duongthihoa13402-sketch/bleach-fullbring-layout-lib@main/CODEX-PROMPT.md) | 直接复制给 ChatGPT / Codex 的完整排版规则（18 种标准版式 L1–L18 + 15 种内容标签 T1–T15） |
| **1075 页全量验证报告与对应表** | [`VERIFIED-LAYOUT-GUIDE.md`](https://cdn.jsdelivr.net/gh/duongthihoa13402-sketch/bleach-fullbring-layout-lib@main/VERIFIED-LAYOUT-GUIDE.md) | 场景决策表、18 版式每格槽位标签配比、9 套高频连招公式 |
| **机器可读版式语法 JSON** | [`report/layout-grammar.json`](https://cdn.jsdelivr.net/gh/duongthihoa13402-sketch/bleach-fullbring-layout-lib@main/report/layout-grammar.json) | 10 类剧情场景规则 + L1–L18 槽位配方 + T1–T15 实测几何分布 |
| **1,012 页版式抽样索引库** | [`report/fullbring-layout-index.json`](https://cdn.jsdelivr.net/gh/duongthihoa13402-sketch/bleach-fullbring-layout-lib@main/report/fullbring-layout-index.json) | 配合 `pick_layout.py` 按格数 `N` 抽取真实页面坐标，内置每页 `cdn_url` 与 `tag_seq` |
| **1,075 页完整分格标注库** | [`report/fullbring-1075-annotations.json`](https://cdn.jsdelivr.net/gh/duongthihoa13402-sketch/bleach-fullbring-layout-lib@main/report/fullbring-1075-annotations.json) | 每页每格的百分比坐标、标签、一句话画面描述、气泡数、边框属性 |
| **单格素材与场景索引** | [`period-reference-index.json`](https://cdn.jsdelivr.net/gh/duongthihoa13402-sketch/bleach-fullbring-layout-lib@main/period-reference-index.json) / [`period-source-index.json`](https://cdn.jsdelivr.net/gh/duongthihoa13402-sketch/bleach-fullbring-layout-lib@main/period-source-index.json) | 对应 `scene-images/` 下的 228 张分类场景与人物参考图 |

## 2. 图片直接访问 URL 规则（支持 ChatGPT 联网读取）

所有图片均可通过 **jsDelivr CDN**（无防盗链，ChatGPT 可直接读取）或 **GitHub Raw** 访问：

- **章节原图（1,075 张）**：
  - CDN: `https://cdn.jsdelivr.net/gh/duongthihoa13402-sketch/bleach-fullbring-layout-lib@main/chapters/c425/p001.jpg`
  - Raw: `https://raw.githubusercontent.com/duongthihoa13402-sketch/bleach-fullbring-layout-lib/main/chapters/c425/p001.jpg`
- **场景分类参考图（228 张）**：
  - CDN: `https://cdn.jsdelivr.net/gh/duongthihoa13402-sketch/bleach-fullbring-layout-lib@main/scene-images/<subfolder>/<filename>.jpg`

## 3. 在 Codex 中调用版式抽样器

```bash
git clone https://github.com/duongthihoa13402-sketch/bleach-fullbring-layout-lib.git
cd bleach-fullbring-layout-lib
python pick_layout.py --n 5 --canvas 1800x1200 --seed 42
```
