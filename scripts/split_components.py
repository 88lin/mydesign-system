#!/usr/bin/env python3
"""把 references/components.md（127 KB / 52 组件）拆成按功能分类的分片 + 机器可读索引。

动机
----
单文件 127 KB 对 AI 不友好：为了拿 1 个组件的代码，得把 52 个组件全读进上下文。
拆分后的读取顺序是「先读 00-index.md（约 7 KB）定位编号 → 只加载命中的分片」。

不改动任何组件代码，只做搬运 + 加锚点。可重复执行（幂等）：每次都从 git 里的
原始单文件重新生成；如果单文件已被替换成指针，则从现有分片重新聚合。

用法
----
    python scripts/split_components.py            # 执行拆分
    python scripts/split_components.py --check    # 只校验，不写文件（CI 用）
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "references" / "components.md"
OUT_DIR = ROOT / "references" / "components"

H2_RE = re.compile(r"^##\s+(\d+)\.\s*(.+?)\s*$", re.M)
VARIANT_RE = re.compile(r"(\d+)\s*种")
POINTER_MARK = "<!-- ds-components-split -->"

# ---------------------------------------------------------------- 分类定义
# 按「功能」而不是「场景」分类：一个组件可以出现在多个场景里，但只能存放在一个文件里。
# 场景 → 组件的多对多关系放在索引的场景表里。
CATEGORIES: list[tuple[str, str, str, list[int]]] = [
    # (文件名前缀, 分类名, 一句话说明, 组件编号)
    ("01", "卡片与网格", "内容分块的主力组件。先在这里找，找不到再考虑别的分类。",
     [1, 10, 15, 30, 31, 32, 34, 37]),
    ("02", "引用与金句", "所有引用块都必须从这里选——禁止 HTML 默认 blockquote。",
     [3, 6, 38, 39, 40, 50]),
    ("03", "标题与主视觉", "Section 分隔、首屏大标题、页尾签名。",
     [2, 8, 18, 24, 33, 43]),
    ("04", "导航与内容切换", "在有限空间里塞多屏内容：导航、Tab、手风琴、轮播、横向滑动。",
     [9, 14, 16, 26, 27, 28, 29, 36]),
    ("05", "流程 · 时间线 · 清单", "有先后顺序或需要勾选的内容。",
     [11, 17, 35, 41, 42]),
    ("06", "对比与数据表", "两方对比、参数表——替代默认 <table>。",
     [12, 19, 20]),
    ("07", "代码 · 终端 · 对话", "技术类内容的展示外壳。",
     [5, 7, 25]),
    ("08", "场景化卡片与版式", "强主题的成套版式，整体使用、不要拆零件。",
     [13, 21, 22, 23]),
    ("09", "动效与文字特效", "⚠️ 一个页面最多用 1–2 个，放在 Hero 或结尾。动效堆叠 = 廉价感。",
     [4, 44, 45, 46, 47, 48, 49, 51, 52]),
]

# 关键词：给 AI 做语义检索用，不是给人看的装饰
TAGS: dict[int, str] = {
    1: "卡片 变体 网格 通用容器", 2: "章节 标题 编号 分隔",
    3: "引用 金句 洞察 强调块", 4: "滚动 淡入 出场动画 容器",
    5: "代码 高亮 语法 macOS窗口", 6: "引用 大字 装饰引号",
    7: "对话 气泡 聊天 问答", 8: "标题 超大数字 提示",
    9: "导航栏 固定 毛玻璃 顶栏", 10: "三列 人物 卡片 变体",
    11: "流程 箭头 步骤 管线", 12: "对比 正误 DoDont 清单",
    13: "头像 集群 轨道标签 团队", 14: "筛选 标签 分类 Filter",
    15: "书卡 封面 推荐 出版物", 16: "弹窗 Modal 长文阅读",
    17: "日历 网格 情绪 打卡", 18: "按钮 CTA 行动号召",
    19: "对比表 杂志 编排", 20: "对比表 圆点 标识",
    21: "机票 航班 登机牌 旅行", 22: "住宿 酒店 房卡 旅行",
    23: "报纸 多栏 分栏 编排", 24: "全屏 大图 压字 首屏",
    25: "打字机 终端 命令行", 26: "横向滑动 滚动 卡片轨道",
    27: "Tab 切换 面板 选项卡", 28: "手风琴 折叠 展开 FAQ",
    29: "轮播 箭头 走马灯", 30: "堆叠 层叠 卡片组",
    31: "翻转 3D 正反面", 32: "悬停 揭示 遮罩 卡片",
    33: "暗底 大字 按钮揭示 Hero", 34: "编号 卡片 网格 步骤",
    35: "清单 勾选 交互 待办", 36: "缩略图 轨道 侧面板 图集",
    37: "悬停 翻转 卡片组", 38: "引号 居中 巨大 金句",
    39: "肖像 分割 引号 人物金句", 40: "极简 留白 引号",
    41: "时间线 横向 彩色标题 变体", 42: "步骤 圆形 环形 循环",
    43: "签名 Tagline 页尾 作者",
    44: "星光 闪烁 文字特效 Hero", 45: "变形 Morph 文字切换",
    46: "粒子 点击爆发 交互特效", 47: "打字 逐字 动画 Hero",
    48: "字重 动态 Kinetic 文字", 49: "像素 渐显 图片",
    50: "荧光笔 手绘标注 波浪线 画圈", 51: "漫画 波普 描边文字",
    52: "环形 旋转 文字 装饰",
}

# 场景索引：从原文件的 14 行表格继承，并补齐原表没覆盖到的 12 个组件
SCENES: list[tuple[str, list[int]]] = [
    ("Hero区 / 首屏大标题", [44, 47, 48, 45, 33, 24]),
    ("图片展示 / 头像", [49, 10, 13, 36]),
    ("正文重点标注", [50, 3, 6]),
    ("趣味 / 活动标题", [51, 2, 8]),
    ("装饰 / CTA", [52, 46, 18, 43]),
    ("卡片类", [1, 10, 34, 32, 15, 37]),
    ("引用 / 金句", [3, 6, 38, 40, 39]),
    ("代码 / 终端", [5, 7, 25]),
    ("导航 / 切换", [9, 14, 27, 28, 29]),
    ("步骤 / 流程", [11, 42, 34, 35]),
    ("对比 / 列表", [12, 19, 20]),
    ("动效 / 滑动", [4, 28, 31, 30, 26]),
    ("日历 / 时间", [17, 41]),
    ("旅行 / 生活", [21, 22]),
    ("长文 / 阅读", [16, 23, 5]),
]

PRINCIPLES = """> 🚨 组件选择原则：
> - **连贯性 > 多样性。** 一个页面的视觉语言应该统一，不是"组件展览会"。同类内容用同一种组件样式，不要每个 section 都换一种全新的视觉形式。
> - **内容决定形式。** 先看内容是什么（流程？对比？金句？代码？），然后查索引找对应组件。不要为了用某个组件而硬塞内容。
> - **动效组件克制使用。** 一个页面最多 1-2 个动效组件（#44-52），用在最重要的位置（Hero/结尾）。动效太多=廉价感。"""

BAN_QUOTE = """> 🚫 **引用块禁令（最高优先级）：**
> - **绝对禁止** 使用 HTML 默认 `<blockquote>` 样式（左侧灰色竖线+浅灰背景）
> - **绝对禁止** 左色条+白底卡片的引用样式（特别丑）
> - **绝对禁止** 任何未经设计的浏览器默认引用样式
> - 需要引用/金句时，**必须**从下方组件中选用：#3 Key Insight、#6 Pull Quote、#50 Text Highlighter、#38 巨大引号、#40 极简留白引号、#39 肖像分割引号
> - 如果只是一句话的重点标注，用 #50 Text Highlighter（荧光笔/波浪线/画圈）而不是引用块"""


# ---------------------------------------------------------------- 解析
def read_source() -> str:
    """拿到 52 个组件的全文。

    优先用工作区里的 components.md；如果它已经被换成指针（说明脚本跑过一次），
    就从现有分片重新聚合，保证幂等。再退一步从 git HEAD 取原始版本。
    """
    if SRC.exists():
        txt = SRC.read_text(encoding="utf-8")
        if POINTER_MARK not in txt and len(H2_RE.findall(txt)) > 40:
            return txt
    if OUT_DIR.exists():
        parts = []
        for p in sorted(OUT_DIR.glob("*.md")):
            if p.name == "00-index.md":
                continue
            txt = p.read_text(encoding="utf-8")
            # 必须砍掉分片自己的表头，否则它会被并进上一个分片最后那个组件的正文里，
            # 每跑一次就多吃 ~500 字节，脚本就不幂等了。
            first = H2_RE.search(txt)
            if first:
                parts.append(txt[first.start():])
        joined = "\n".join(parts)
        if len(H2_RE.findall(joined)) > 40:
            return joined
    out = subprocess.run(["git", "show", "HEAD:references/components.md"],
                         cwd=ROOT, capture_output=True, text=True)
    if out.returncode == 0 and len(H2_RE.findall(out.stdout)) > 40:
        return out.stdout
    sys.exit("[FAIL] 找不到含 52 个组件的 components.md 原文")


def parse(text: str) -> dict[int, dict]:
    marks = list(H2_RE.finditer(text))
    blocks: dict[int, dict] = {}
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        body = text[m.end():end]
        # 先摘掉本脚本加过的锚点行（重复执行时它会落在上一个组件的尾部），
        # 再去掉块尾的分隔线和空行——输出时统一补回去。顺序反了会漏。
        body = re.sub(r'(?m)^[ \t]*<a id="c\d+"></a>[ \t]*\n?', "", body)
        body = re.sub(r"\n+(?:---+[ \t]*\n+)*[ \t\n]*$", "\n", body)
        cid = int(m.group(1))
        title = m.group(2)
        vm = VARIANT_RE.search(title)
        blocks[cid] = {
            "id": cid,
            "title": title,
            "body": body.strip("\n"),
            "variants": int(vm.group(1)) if vm else 1,
        }
    return blocks


# ---------------------------------------------------------------- 渲染
def shard_name(prefix: str, label: str) -> str:
    slug = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", label).strip("-")
    return f"{prefix}-{slug}.md"


def render_shard(label: str, note: str, ids: list[int], blocks: dict[int, dict]) -> str:
    listed = "、".join(f"[#{i} {blocks[i]['title']}](#c{i})" for i in ids)
    out = [
        f"# 组件库 · {label}",
        "",
        f"> {note}",
        "",
        f"> 本文件是 `references/components.md` 的分片之一，索引见 "
        f"[`00-index.md`](00-index.md)。共 {len(ids)} 个组件：",
        f"> {listed}",
        "",
        "---",
        "",
    ]
    for cid in ids:
        b = blocks[cid]
        out += [f'<a id="c{cid}"></a>', f"## {cid}. {b['title']}", "", b["body"], "", "---", ""]
    return "\n".join(out).rstrip() + "\n"


def render_index(blocks: dict[int, dict], shard_of: dict[int, str],
                 sizes: dict[str, int]) -> str:
    total = len(blocks)
    L = [
        "# 组件库索引",
        "",
        f"> **{total} 个组件**，按功能拆成 {len(CATEGORIES)} 个分片文件。",
        "> 读取顺序：**先读本索引定位编号 → 只打开命中的分片文件 → 复制代码**。",
        f"> 不要一次性读入全部分片（合计约 {sum(sizes.values()) // 1024} KB）；"
        f"本索引约 {{index_kb}} KB 就够定位组件了。",
        "",
        "---",
        "",
        "## 🚨 选组件前必读",
        "",
        PRINCIPLES,
        "",
        BAN_QUOTE,
        "",
        "---",
        "",
        "## 📌 场景 → 组件",
        "",
        "先按场景缩小范围，再去下面的组件清单查分片文件。",
        "",
        "| 场景 | 推荐组件（编号） |",
        "|------|------|",
    ]
    for scene, ids in SCENES:
        cells = "、".join(f"#{i} {blocks[i]['title'].split('（')[0]}" for i in ids)
        L.append(f"| **{scene}** | {cells} |")

    L += ["", "---", "", "## 📂 分片文件", "",
          "| 文件 | 分类 | 组件编号 | 组件数 | 大小 |", "|------|------|------|------|------|"]
    for prefix, label, _note, ids in CATEGORIES:
        fn = shard_name(prefix, label)
        rng = ", ".join(f"#{i}" for i in ids)
        L.append(f"| [`{fn}`]({fn}) | {label} | {rng} | {len(ids)} | {sizes[fn] // 1024} KB |")

    L += ["", "---", "", "## 🔎 组件清单", "",
          "按编号排序。`变体` = 该组件自带几种风格；`关键词` 用于语义检索。", "",
          "| # | 组件 | 分类 | 变体 | 关键词 | 分片文件 |",
          "|---|------|------|------|------|------|"]
    cat_of = {i: label for _p, label, _n, ids in CATEGORIES for i in ids}
    for cid in sorted(blocks):
        b = blocks[cid]
        fn = shard_of[cid]
        L.append(f"| {cid} | [{b['title']}]({fn}#c{cid}) | {cat_of[cid]} | "
                 f"{b['variants']} | {TAGS.get(cid, '')} | `{fn}` |")

    L += ["", "---", "",
          "## 引用方式", "",
          "其他文档引用组件时写 `组件库 #编号`（例如 `组件库 #3`），"
          "编号在拆分前后保持不变；需要给出链接时用 "
          "`references/components/<分片文件>#c<编号>`。", ""]
    body = "\n".join(L)
    return body.replace("{index_kb}", str(max(1, len(body.encode()) // 1024)))


def render_pointer(sizes: dict[str, int], blocks: dict[int, dict]) -> str:
    rows = []
    for prefix, label, note, ids in CATEGORIES:
        fn = shard_name(prefix, label)
        rows.append(f"| [`components/{fn}`](components/{fn}) | {label} | "
                    f"{len(ids)} 个 | {note} |")
    return "\n".join([
        "# 组件库",
        "",
        POINTER_MARK,
        f"> ⚠️ 本文件已拆分。{len(blocks)} 个组件现在放在 [`components/`](components/) 目录下，"
        "按功能分成 9 个分片。",
        "> **入口是 [`components/00-index.md`](components/00-index.md)** —— "
        "先读索引定位编号，再只加载对应分片，不要整目录读进上下文。",
        "",
        "拆分原因：原单文件 127 KB，为了取 1 个组件的代码要把 52 个组件全部读入，"
        "既浪费上下文也容易让模型抄错组件。编号没有变，`组件库 #3` 依然是 #3。",
        "",
        "| 分片 | 分类 | 组件数 | 说明 |",
        "|------|------|------|------|",
        *rows,
        "",
    ]) + "\n"


# ---------------------------------------------------------------- 主流程
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只校验，不写文件")
    args = ap.parse_args()

    blocks = parse(read_source())
    ids_all = sorted(blocks)
    assigned = [i for _p, _l, _n, ids in CATEGORIES for i in ids]

    # 完整性校验：不允许漏、不允许重、不允许无主
    dup = {i for i in assigned if assigned.count(i) > 1}
    missing = set(ids_all) - set(assigned)
    ghost = set(assigned) - set(ids_all)
    if dup or missing or ghost:
        print(f"[FAIL] 分类表有问题 重复={sorted(dup)} 未分类={sorted(missing)} "
              f"不存在={sorted(ghost)}")
        return 1
    if ids_all != list(range(1, len(ids_all) + 1)):
        print(f"[FAIL] 组件编号不连续: {ids_all}")
        return 1

    shard_of: dict[int, str] = {}
    payload: dict[str, str] = {}
    for prefix, label, note, ids in CATEGORIES:
        fn = shard_name(prefix, label)
        payload[fn] = render_shard(label, note, ids, blocks)
        for i in ids:
            shard_of[i] = fn
    sizes = {fn: len(txt.encode("utf-8")) for fn, txt in payload.items()}
    payload["00-index.md"] = render_index(blocks, shard_of, sizes)

    # 内容守恒：拆分后每个组件的代码块数量必须和拆分前一致
    src_fences = sum(b["body"].count("```") for b in blocks.values())
    out_fences = sum(t.count("```") for fn, t in payload.items() if fn != "00-index.md")
    if src_fences != out_fences:
        print(f"[FAIL] 代码块数量不守恒: 拆分前 {src_fences} 拆分后 {out_fences}")
        return 1

    print(f"组件 {len(blocks)} 个 · 分片 {len(CATEGORIES)} 个 · "
          f"索引 {len(payload['00-index.md'].encode()) // 1024} KB · "
          f"代码块 ``` 计数 {src_fences} 守恒")
    for prefix, label, _n, ids in CATEGORIES:
        fn = shard_name(prefix, label)
        print(f"  {fn:34s} {len(ids):2d} 个  {sizes[fn] / 1024:6.1f} KB")

    if args.check:
        if not OUT_DIR.exists():
            print("[FAIL] references/components/ 不存在，需要先运行一次拆分")
            return 1
        bad = [fn for fn, txt in payload.items()
               if not (OUT_DIR / fn).exists()
               or (OUT_DIR / fn).read_text(encoding="utf-8") != txt]
        if bad:
            print(f"[FAIL] 分片与源文件不同步: {bad}")
            return 1
        print("[OK] 分片是最新的")
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for fn, txt in payload.items():
        (OUT_DIR / fn).write_text(txt, encoding="utf-8")
    SRC.write_text(render_pointer(sizes, blocks), encoding="utf-8")
    print(f"[OK] 已写入 {len(payload)} 个文件 → references/components/，"
          f"components.md 变为指针（{len(SRC.read_bytes())} 字节）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
