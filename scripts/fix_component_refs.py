#!/usr/bin/env python3
"""把散落在文档里的 `components.md #N` 引用改成拆分后的分片链接。

编号 → 分片文件的映射从 references/components/00-index.md 反查，不硬编码，
所以以后调整分类也不会产生死链。可重复执行。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IDX = ROOT / "references" / "components" / "00-index.md"

# `components.md` #43 / `components.md #6` / components.md #9 —— 三种写法都见过
REF_RE = re.compile(r"`?components\.md`?\s*#\s*(\d+)`?")


def shard_map() -> dict[int, str]:
    if not IDX.exists():
        sys.exit("[FAIL] 找不到 references/components/00-index.md，先跑 split_components.py")
    txt = IDX.read_text(encoding="utf-8")
    m: dict[int, str] = {}
    for cid, fn in re.findall(r"^\|\s*(\d+)\s*\|.*?\|\s*`(\d\d-[^`]+\.md)`\s*\|\s*$",
                              txt, re.M):
        m[int(cid)] = fn
    if len(m) < 40:
        sys.exit(f"[FAIL] 只从索引里解析出 {len(m)} 个组件映射，格式可能变了")
    return m


def main() -> int:
    smap = shard_map()
    total = 0

    # 场景文件：这些地方是「去看这个组件」的指路牌，值得带上可点的链接
    for p in sorted((ROOT / "references").glob("scene-*.md")):
        txt = orig = p.read_text(encoding="utf-8")

        def to_link(mm: re.Match) -> str:
            cid = int(mm.group(1))
            fn = smap.get(cid)
            if not fn:
                return mm.group(0)
            return f"[组件库 #{cid}](components/{fn}#c{cid})"

        txt = REF_RE.sub(to_link, txt)
        if txt != orig:
            n = len(REF_RE.findall(orig))
            p.write_text(txt, encoding="utf-8")
            print(f"  {p.relative_to(ROOT)}: {n} 处")
            total += n

    # brand-dna.md：禁忌表里的提及，加链接反而吵，只把文件名换成「组件库」
    bd = ROOT / "brand-dna.md"
    if bd.exists():
        txt = orig = bd.read_text(encoding="utf-8")
        txt = REF_RE.sub(lambda mm: f"组件库 #{mm.group(1)}", txt)
        txt = txt.replace("从 components.md 选", "从组件库选")
        txt = txt.replace("必须从components.md选用", "必须从组件库选用")
        txt = txt.replace("从 components.md 的对比表", "从组件库的对比表")
        if txt != orig:
            bd.write_text(txt, encoding="utf-8")
            print(f"  brand-dna.md: 已改为「组件库 #N」写法")
            total += 1

    left = []
    for p in list(ROOT.glob("*.md")) + list((ROOT / "references").glob("*.md")):
        if p.name == "components.md":
            continue  # 它自己就是指针，正文里必然提到自己
        t = p.read_text(encoding="utf-8")
        for mm in re.finditer(r"components\.md", t):
            ctx = t[max(0, mm.start() - 40):mm.end() + 20].replace("\n", " ")
            left.append(f"{p.relative_to(ROOT)}: …{ctx}…")
    print(f"\n处理 {total} 处引用")
    if left:
        print(f"仍提到 components.md 的 {len(left)} 处（需人工确认是否有意）:")
        for s in left:
            print("  " + s)
    else:
        print("已无遗留的 components.md 引用")
    return 0


if __name__ == "__main__":
    sys.exit(main())
