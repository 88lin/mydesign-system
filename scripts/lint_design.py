#!/usr/bin/env python3
"""checklist.md 的可执行版本。

把 P0/P1/P2 从"人肉逐条看"变成"每次 push 自动跑"。纯标准库，无 npm/pip 依赖。

规则（按场景域生效，见 SCOPES）
  R1 色彩合规    tokens 区块外的旧品牌色 / 多色渐变背景 / 纯黑纯白      全域
  R2 字体合规    Inter/Roboto/Arial 等 overused 字体（等宽白名单例外）  全域
  R3 默认样式    裸 blockquote / 无样式 ul·ol / 裸 table / Notion 式引用 全域
  R4 流体与响应  hero·标题必须 clamp()、必须有 900px 断点               page
  R5 无障碍      lang / img alt / prefers-reduced-motion / focus / 对比度 page·card·gallery
  R6 布局重复    同一页 section 结构签名重复度 > 50%                    page
  R7 文档一致    组件·布局计数、README 链接指向真实存在的文件            仓库级
  R8 导出确定性  固定画布内禁止 vw/vh、画布尺寸必须锁定                  card

为什么要分域：3:4 图文卡片是固定 1080×1440 的导出画布，靠 transform: scale() 预览、
html2canvas 导出 PNG。在其中使用 clamp()/vw 会让导出结果随浏览器窗口宽度变化，
所以 card 域里固定像素才是正确写法；公众号模板会被微信编辑器剥掉 CSS 变量和媒体查询，
因此不检查断点与变量。

用法
  python scripts/lint_design.py                  # 全量
  python scripts/lint_design.py --json out.json  # 同时输出 JSON
  python scripts/lint_design.py --baseline b.json --json now.json   # 与基线对比
  python scripts/lint_design.py demo-app.html    # 只查指定文件
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOKENS_PATH = ROOT / "tokens.json"
CSS_START_MARK = "/* tokens:start"
CSS_END_MARK = "/* tokens:end */"

P0, P1, P2 = "P0", "P1", "P2"


def load_tokens() -> dict:
    """tokens.json 是唯一色彩/字体真源，linter 与 codemod 共用同一个入口。

    代码面板的具名例外调色板会被摊平进 color 表，这样 `var(--code-cmt)` 之类
    也能被对比度规则解析；浅底那套写的是 `var(--brand)` 形式，需要再解一层。
    """
    t = json.loads(TOKENS_PATH.read_text(encoding="utf-8"))
    code = t.get("code_color", {})
    flat: dict[str, dict] = {}
    for group in ("dark", "light"):
        for key, spec in code.get(group, {}).items():
            if key.startswith("_"):
                continue
            flat[key] = dict(spec)
    for key, spec in flat.items():  # 解开 var(--brand) 这种间接引用
        m = re.match(r"var\(\s*--([a-z0-9-]+)", str(spec["value"]))
        if m:
            ref = t["color"].get(t["legacy_aliases"].get(m.group(1), m.group(1)))
            spec["value"] = ref["value"] if ref else "#000000"
        t["color"].setdefault(key, spec)
    return t

# 场景域：文件名关键字 -> 域。也可在 HTML 里写 <!-- ds-scope: card --> 显式声明。
SCOPE_BY_KEYWORD = [
    ("wechat", "wechat"),
    ("cards", "card"),
    ("components-preview", "gallery"),
    ("layouts", "gallery"),
]
SCOPE_DEFAULT = "page"
SCOPE_RE = re.compile(r"<!--\s*ds-scope:\s*(page|card|wechat|gallery)\s*-->", re.I)
# base64 数据块会污染正则匹配，统一先抹掉
B64_RE = re.compile(r"(data:[a-z/+.-]+;base64,)[A-Za-z0-9+/=\s]+", re.I)


def scope_of(rel: str, text: str) -> str:
    m = SCOPE_RE.search(text)
    if m:
        return m.group(1).lower()
    name = rel.lower()
    for kw, scope in SCOPE_BY_KEYWORD:
        if kw in name:
            return scope
    return SCOPE_DEFAULT


def strip_b64(text: str) -> str:
    """把 base64 载荷替换成等长空白，保持行号与偏移不变。"""
    return B64_RE.sub(lambda m: m.group(1) + " " * (len(m.group(0)) - len(m.group(1))), text)


# ---------- 工具 ----------
def hex2rgb(h: str):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def relative_luminance(hex_color: str) -> float:
    chan = [c / 255 for c in hex2rgb(hex_color)]
    chan = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in chan]
    return 0.2126 * chan[0] + 0.7152 * chan[1] + 0.0722 * chan[2]


def contrast(a: str, b: str) -> float:
    la, lb = relative_luminance(a), relative_luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def line_of(text: str, idx: int) -> int:
    return text.count("\n", 0, idx) + 1


def strip_tokens_block(text: str) -> str:
    """把 tokens 区块替换成等长空白，保持行号不变。"""
    if CSS_START_MARK in text and CSS_END_MARK in text:
        s = text.index(CSS_START_MARK)
        e = text.index(CSS_END_MARK) + len(CSS_END_MARK)
        return text[:s] + re.sub(r"[^\n]", " ", text[s:e]) + text[e:]
    return text


class Findings:
    def __init__(self) -> None:
        self.items: list[dict] = []
        self.scopes: dict[str, str] = {}

    def add(self, rule: str, sev: str, file: str, line: int | None, msg: str, fix: str = "") -> None:
        self.items.append({"rule": rule, "severity": sev, "file": file, "line": line, "message": msg, "fix": fix})

    def count(self, sev: str) -> int:
        return sum(1 for i in self.items if i["severity"] == sev)


# ---------- R1 色彩 ----------
def rule_colors(text: str, rel: str, tokens: dict, f: Findings, scope: str = "page") -> None:
    body = strip_tokens_block(text)
    legacy = {k.lower(): v for k, v in tokens["color_migration"]["hex"].items()}
    for m in re.finditer(r"#[0-9a-fA-F]{6}\b", body):
        hx = m.group(0).lower()
        if hx in legacy:
            f.add("R1", P0, rel, line_of(body, m.start()),
                  f"tokens 区块外出现已弃用色值 {m.group(0)}",
                  f"改用 var() 引用 token（对应新值 {legacy[hx]}）")
    rgba_legacy = {tuple(int(x) for x in k.split(",")): v for k, v in tokens["color_migration"]["rgba"].items()}
    for m in re.finditer(r"rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})", body):
        triple = tuple(int(m.group(i)) for i in (1, 2, 3))
        if triple in rgba_legacy:
            f.add("R1", P0, rel, line_of(body, m.start()),
                  f"tokens 区块外出现已弃用 rgba 色值 rgba({','.join(map(str, triple))}…)",
                  f"改用 var(--accent-wash) 等半透明 token（对应新值 {rgba_legacy[triple]}）")
    # 多色渐变背景（禁忌）。两类合法例外：transparent->单色 高亮/遮罩；硬停色段条（并排色块而非渐变过渡）
    for start, frag in _gradient_frags(body):
        colors = re.findall(r"#[0-9a-fA-F]{3,6}|rgba?\([^)]*\)|var\(--[a-z0-9-]+[^)]*\)", frag)
        uniq = {c.lower() for c in colors}
        if "transparent" in frag and len(uniq) <= 1:
            continue
        if len(uniq) < 2 or is_hard_stop(frag, colors) or _single_hue(colors, tokens):
            continue
        f.add("R1", P0, rel, line_of(body, start),
              "多色渐变背景（禁忌清单：任何多色渐变背景）",
              "改成硬停色段（每色写起止两个位置，如 var(--brand) 0 60%）或改用纯色 token")
    # 纯黑/纯白不只出现在 color/background 上：描边、阴影、滤镜里一样是纯黑。
    # 只查不透明写法；rgba(0,0,0,.x) 半透明阴影是常规做法，不在禁忌范围内。
    for m in re.finditer(
        r"(?:^|[;{])\s*(-webkit-text-stroke(?:-color)?|text-stroke|color|background(?:-color)?|border(?:-[a-z]+)?|"
        r"outline(?:-color)?|box-shadow|text-shadow|filter|fill|stroke|caret-color|text-decoration-color)"
        r"\s*:\s*([^;{}]*)",
        body, re.I,
    ):
        prop, val = m.group(1), m.group(2)
        hit = re.search(r"(?<![0-9a-fA-F])(#000000|#000|#ffffff|#fff)(?![0-9a-fA-F])", val)
        if not hit:
            continue
        f.add("R1", P1, rel, line_of(body, m.start()),
              f"{prop} 使用纯黑/纯白 {hit.group(1)}（brand-dna：绝不用纯黑纯白）",
              "文字用 var(--ink)，底色用 var(--card-bg) / var(--cream)，"
              "描边/阴影用 var(--ink) 或 var(--alpha-shadow) 之类的暖调色")
    # 裸品牌色值（不算错，但可维护性差）。公众号必须全内联 hex，微信编辑器会剥掉 CSS 变量，故豁免。
    if scope == "wechat":
        return
    token_hex = {spec["value"].lower(): key for key, spec in tokens["color"].items()}
    for m in re.finditer(r"#[0-9a-fA-F]{6}\b", body):
        key = token_hex.get(m.group(0).lower())
        if key:
            f.add("R1", P2, rel, line_of(body, m.start()),
                  f"裸写 token 色值 {m.group(0)}", f"改用 var(--{key})")


def _gradient_frags(body: str):
    """按括号配对切出每个 gradient() 的内容。

    用 `[^;]{0,260}` 截取会串到同一行的下一个 gradient 里去——三个同色系
    色调洗写在一行时，第一个的片段会把后两个的颜色也吞进来，于是被误判成多色渐变。
    """
    for m in re.finditer(r"(?:repeating-)?(?:linear|radial|conic)-gradient\(", body):
        depth, i, n = 1, m.end(), len(body)
        while i < n and depth:
            ch = body[i]
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            elif ch == ";":
                break
            i += 1
        yield m.start(), body[m.end(): i - 1 if depth == 0 else i]


def _single_hue(colors: list[str], tokens: dict) -> bool:
    """同一个色相、只有透明度差别的渐变不算「多色」。

    例：linear-gradient(145deg, rgba(166,61,111,.08), rgba(166,61,111,.02))
    禁忌清单禁的是多**色**渐变；同色系深浅过渡是这套设计里合法的「色调洗」。
    """
    rgbs = set()
    for c in colors:
        if c.strip().lower() == "transparent":
            continue
        got = _resolve_translucent(c, tokens)
        if got:
            rgbs.add(got[0].upper())
            continue
        solid = _resolve_color(c, tokens)
        if not solid:
            return False
        rgbs.add(("#%02X%02X%02X" % hex2rgb(solid)).upper())
    return len(rgbs) <= 1


def is_hard_stop(frag: str, colors: list[str]) -> bool:
    """硬停色段：每个颜色后面跟两个位置值，或相邻颜色共用同一位置。

    例：linear-gradient(90deg, var(--brand) 0 60%, var(--accent) 60% 80%)
    这类写法渲染出来是并排色块，不产生渐变过渡，不属于「多色渐变背景」禁忌。
    """
    if len(colors) < 2:
        return False
    pattern = r"(?:#[0-9a-fA-F]{3,6}|rgba?\([^)]*\)|var\(--[a-z0-9-]+[^)]*\))\s+([0-9.]+%?)\s+([0-9.]+%?)"
    if len(re.findall(pattern, frag)) >= len(colors) - 1:
        return True
    stops = re.findall(r"(?:#[0-9a-fA-F]{3,6}|rgba?\([^)]*\)|var\(--[a-z0-9-]+[^)]*\))\s+([0-9.]+%)", frag)
    return len(stops) >= 2 and len(stops) != len(set(stops))


# ---------- R2 字体 ----------
def rule_fonts(text: str, rel: str, tokens: dict, f: Findings) -> None:
    forbidden = tokens["font_loading"]["forbidden_families"]
    whitelist = {w.lower() for w in tokens["font_loading"]["mono_whitelist"]}
    for fam in forbidden:
        if fam.lower() in whitelist:
            continue
        for m in re.finditer(rf"family={re.escape(fam)}\b", text, re.I):
            f.add("R2", P0, rel, line_of(text, m.start()),
                  f"Google Fonts 加载了禁忌字体 {fam}",
                  "使用 tokens.json 的 font_loading.canonical_url")
        for m in re.finditer(rf"font-family\s*:[^;{{}}]*\b{re.escape(fam)}\b", text, re.I):
            f.add("R2", P0, rel, line_of(text, m.start()),
                  f"font-family 使用了禁忌字体 {fam}",
                  "改用 var(--font-sans) / var(--font-serif) / var(--font-display)")
    _check_font_url(text, rel, tokens, f)


GF_URL_RE = re.compile(r"https://fonts\.googleapis\.com/css2\?[^\"'\s>]+")


def _gf_families(url: str) -> set[str]:
    out = set()
    for block in re.findall(r"family=([^&]+)", url):
        out.add(block.split(":", 1)[0].replace("+", " "))
    return out


def _check_font_url(text: str, rel: str, tokens: dict, f: Findings) -> None:
    """全仓库只应该有一个字体 URL。多套 URL 会让同一个组件在不同页面拿到不同字重，
    浏览器只能合成假粗体/假斜体，视觉就漂移了；每套 URL 也各自是一次阻塞渲染的请求。"""
    fl = tokens.get("font_loading", {})
    canonical = fl.get("canonical_url")
    if not canonical:
        return
    allowed = _gf_families(canonical) | {e for e in fl.get("declared_exceptions", {})}
    urls = GF_URL_RE.findall(text)
    for url in urls:
        fams = _gf_families(url)
        extra = fams - allowed
        for fam in sorted(extra):
            f.add("R2", P0, rel, line_of(text, text.index(url)),
                  f"加载了未登记的字体 {fam}",
                  f"要么改用字体池里的字体，要么在 tokens.json 的 "
                  f"font_loading.declared_exceptions 里登记 {fam} 并写明理由")
        # 已登记的例外字体：允许在 canonical 之外追加，但其余家族必须与 canonical 一致
        missing = _gf_families(canonical) - fams
        if missing:
            f.add("R2", P1, rel, line_of(text, text.index(url)),
                  "字体 URL 与 tokens.json 的 canonical_url 不一致，缺少 "
                  + "、".join(sorted(missing)),
                  "统一换成 font_loading.canonical_url（需要的例外字体用 & 追加在后面）")
        elif url != canonical and not (fams - _gf_families(canonical)):
            f.add("R2", P1, rel, line_of(text, text.index(url)),
                  "字体 URL 家族相同但字重参数与 canonical_url 不同，会各自请求不同字重子集",
                  "统一换成 font_loading.canonical_url")


# ---------- R3 默认样式 ----------
NOTION_QUOTE = re.compile(
    r"\.(?:[a-z0-9_-]*(?:quote|callout|tip|note|insight)[a-z0-9_-]*)\s*\{[^}]*border-left\s*:[^}]*padding-left\s*:[^}]*\}"
    r"|\.(?:[a-z0-9_-]*(?:quote|callout|tip|note|insight)[a-z0-9_-]*)\s*\{[^}]*padding-left\s*:[^}]*border-left\s*:[^}]*\}",
    re.I | re.S,
)


def _styled_by_ancestor(text: str, styles: str, tag: str, line: int) -> bool:
    """该行上的 <tag> 元素，是否被任何 CSS 规则命中（含祖先作用域选择器）。"""
    if not styles:
        return False
    dom = _dom_cache(text)
    targets = [p for p, at in zip(dom.paths, dom.at) if at[0] == line and p and p[-1][0] == tag]
    if not targets:
        return False
    rules = []
    for sel, _decl in _css_blocks(styles):
        for one in sel.split(","):
            parsed = _parse_selector(one.strip())
            if parsed and parsed[-1][0] == tag:
                rules.append(parsed)
    if not rules:
        return False
    return all(any(_matches(p, r) for r in rules) for p in targets)


def rule_default_styles(text: str, rel: str, f: Findings) -> None:
    styles = "".join(m.group(1) for m in re.finditer(r"<style[^>]*>(.*?)</style>", text, re.S))
    for tag, hint in (("blockquote", "从 components.md 选引用块组件"),
                      ("table", "从 components.md 的对比表组件里选"),
                      ("ul", "从 components.md 选列表组件"),
                      ("ol", "从 components.md 选列表组件")):
        for m in re.finditer(rf"<{tag}(\s[^>]*)?>", text, re.I):
            attrs = m.group(1) or ""
            if "class=" in attrs.lower() or "style=" in attrs.lower():
                continue
            line = line_of(text, m.start())
            # 没有 class 不等于会走默认样式：`.cblock ul{...}` 这类祖先作用域选择器
            # 一样管得到。只有 CSS 里确实没有任何规则命中它，才是真的裸元素。
            if _styled_by_ancestor(text, styles, tag, line):
                continue
            f.add("R3", P0, rel, line, f"裸 <{tag}> 无 class/style，会走浏览器默认样式", hint)
    for m in NOTION_QUOTE.finditer(text):
        f.add("R3", P0, rel, line_of(text, m.start()),
              "Notion/飞书式 border-left + padding-left 引用块（禁忌清单）",
              "改用 components.md 的引用块组件；品牌色条请用独立装饰元素而非引用块左竖线")


# ---------- R4 流体与响应式 ----------
def rule_fluid(text: str, rel: str, f: Findings) -> None:
    has_media = re.search(r"@media[^{]*max-width\s*:\s*(9\d\d|1[0-9]\d\d)px", text)
    if not has_media:
        f.add("R4", P0, rel, None, "缺少 900px 级响应式断点（checklist P0）",
              "加 @media (max-width: 900px) 把两栏改单栏")
    body = strip_tokens_block(text)
    for m in re.finditer(r"font-size\s*:\s*([0-9.]+)rem", body):
        if float(m.group(1)) >= 2.0:
            f.add("R4", P0, rel, line_of(body, m.start()),
                  f"大字号 {m.group(1)}rem 写成固定值，未用 clamp()（checklist P0）",
                  "改用 var(--fs-hero) / var(--fs-section-title) 或 clamp()")
    for m in re.finditer(r"font-size\s*:\s*(\d{2,3})px", body):
        if int(m.group(1)) >= 32:
            f.add("R4", P0, rel, line_of(body, m.start()),
                  f"大字号 {m.group(1)}px 写成固定值，未用 clamp()", "改用 clamp() 或 --fs-* token")


# ---------- R5 无障碍 ----------
def rule_a11y(text: str, rel: str, tokens: dict, f: Findings) -> None:
    if not re.search(r"<html[^>]*\blang=", text, re.I):
        f.add("R5", P0, rel, 1, "<html> 缺少 lang 属性", '写成 <html lang="zh-CN">')
    for m in re.finditer(r"<img(\s[^>]*)?>", text, re.I):
        if not re.search(r"\balt\s*=", m.group(1) or "", re.I):
            f.add("R5", P0, rel, line_of(text, m.start()), "<img> 缺少 alt", "补 alt；纯装饰图写 alt=\"\"")
    has_motion = re.search(r"(animation\s*:|transition\s*:|@keyframes)", text)
    if has_motion and "prefers-reduced-motion" not in text:
        f.add("R5", P0, rel, None, "有动效但未处理 prefers-reduced-motion",
              "加 @media (prefers-reduced-motion: reduce) { *,*::before,*::after{animation:none!important;transition:none!important} }")
    elif has_motion:
        _check_reduced_motion_reveal(text, rel, f)

    interactive = re.search(r"<(?:a|button|input|select|textarea|summary)\b|onclick=|tabindex=", text, re.I)
    if interactive:
        _check_focus_visible(text, rel, f)


# reveal 类动效的初始态：常见写法是 opacity:0 + transform:translateY(...)
REVEAL_SEL_RE = re.compile(r"[.#][\w-]*reveal[\w-]*|\[class\*=[\"']?reveal", re.I)


def _check_reduced_motion_reveal(text: str, rel: str, f: Findings) -> None:
    """只把动画时长压到 0 是不够的：Scroll Reveal 初始 opacity:0，
    降级后元素会永久停在不可见状态——降级反而把内容弄没了。"""
    reveal_hidden = False
    for sel, decl in _css_blocks(strip_tokens_block(text)):
        if not REVEAL_SEL_RE.search(sel):
            continue
        if re.search(r"opacity\s*:\s*0(?:\.0+)?\s*(?:;|$)", decl):
            reveal_hidden = True
            break
    if not reveal_hidden:
        return
    # 抓 @media (prefers-reduced-motion...) 的整段内容（含嵌套花括号）
    blocks = _at_rule_bodies(text, "prefers-reduced-motion")
    body = "\n".join(blocks)
    restores_opacity = re.search(r"opacity\s*:\s*1\b", body)
    restores_transform = re.search(r"transform\s*:\s*none\b", body)
    if not (restores_opacity and restores_transform):
        missing = []
        if not restores_opacity:
            missing.append("opacity: 1")
        if not restores_transform:
            missing.append("transform: none")
        f.add("R5", P0, rel, None,
              "reveal 元素初始 opacity:0，但 prefers-reduced-motion 降级里没有恢复 "
              + " / ".join(missing) + "，降级后内容会永久不可见",
              "在 @media (prefers-reduced-motion: reduce) 里加 "
              ".reveal, [class*=\"reveal\"] { opacity: 1 !important; transform: none !important; }")


def _at_rule_bodies(text: str, needle: str) -> list[str]:
    """按花括号配平提取 @media ... { ... } 的内容，正则做不到嵌套。"""
    out: list[str] = []
    for m in re.finditer(r"@media[^{]*" + re.escape(needle) + r"[^{]*\{", text):
        i = m.end() - 1
        depth = 0
        for j in range(i, len(text)):
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
                if depth == 0:
                    out.append(text[i + 1:j])
                    break
    return out


def _check_focus_visible(text: str, rel: str, f: Findings) -> None:
    """键盘焦点：必须有真正画出焦点环的 :focus-visible 规则。
    只写 :focus{outline:none} 或只写 :focus:not(:focus-visible){outline:none} 都不算。"""
    body = strip_tokens_block(text)
    draws = False
    hard_kills: list[str] = []
    soft_kills: list[str] = []
    for sel, decl in _css_blocks(body):
        if ":focus" not in sel:
            continue
        replaces = re.search(
            r"(?:box-shadow|border(?:-color|-bottom|-left|-right|-top)?)\s*:\s*"
            r"(?!none\b|0\b|unset\b|initial\b)[^;]+", decl)
        draws_outline = re.search(r"outline\s*:\s*(?!none\b|0\b|unset\b|initial\b)[^;]+", decl)
        kills_ring = re.search(r"outline\s*:\s*(?:none|0)\b", decl)
        if ":focus-visible" in sel and "not(:focus-visible)" not in sel and (draws_outline or replaces):
            draws = True
            continue
        if kills_ring and "not(:focus-visible)" not in sel:
            (soft_kills if replaces else hard_kills).append(sel.strip())
    if not draws:
        f.add("R5", P0, rel, None, "有可交互元素但没有可见的键盘焦点样式",
              "加 :focus-visible { outline: 2px solid var(--brand); outline-offset: 3px; } "
              "并用 :focus:not(:focus-visible){outline:none} 只对鼠标点击消环")
    for sel in hard_kills:
        f.add("R5", P0, rel, None,
              f"`{sel}` 用 outline:none 关掉了焦点环，且没有提供任何替代指示",
              "改成 :focus:not(:focus-visible){outline:none}，保留键盘用户的焦点环")
    for sel in soft_kills:
        f.add("R5", P1, rel, None,
              f"`{sel}` 自带替代焦点环，但 outline:none 的选择器权重高于全局 :focus-visible，"
              "键盘用户会同时丢掉全局焦点环",
              f"把消环拆出来写成 {sel.replace(':focus', ':focus:not(:focus-visible)', 1)}"
              " { outline: none }，:focus 里只留替代样式")


# ---------- R5b 对比度（解析所在规则块的真实背景，而不是一律假设暖底） ----------
CSS_BLOCK_RE = re.compile(r"([^{}]+)\{([^{}]*)\}")
LARGE_RE = re.compile(r"font-size\s*:\s*(?:clamp\(\s*)?([0-9.]+)(rem|px|em)")


def _scrim_color(value: str) -> str | None:
    """`linear-gradient(to top, rgba(0,0,0,.7), transparent)` 这类蒙版当成实色处理。

    文字压在图片上的深色蒙版是很常见的排版手法。取渐变里 alpha 最大的那一站
    做近似——不精确，但比"解析不出来就假设页面底色"靠谱得多。
    """
    if "gradient(" not in value:
        return None
    best, best_a = None, 0.0
    for r, g, b, a in re.findall(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([0-9.]+))?\s*\)", value):
        alpha = float(a) if a else 1.0
        if alpha >= best_a:
            best, best_a = f"#{int(r):02x}{int(g):02x}{int(b):02x}", alpha
    for h in re.findall(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b", value):
        if best_a < 1.0:
            best, best_a = f"#{h}", 1.0
    return best if best_a >= 0.5 else None


def _resolve_translucent(value: str, tokens: dict) -> tuple[str, float] | None:
    """把 `rgba()` / `#rrggbbaa` / `var(--<alpha token>)` 解成 (色值, alpha)。

    半透明色块压在别的底上，真实底色是混色后的结果。以前 linter 解析不出 rgba 背景
    就直接退回"页面底色"，于是 `.card-badge.red{background:rgba(232,74,95,.1);color:var(--pop-ink)}`
    这种"彩色小徽章"被算成压在卡片白底上（4.81 通过），实际混色底是 #FDEBE9，只有 4.25。
    """
    v = value.strip()
    m = re.match(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:[,/]\s*([0-9.]+%?))?\s*\)", v)
    if m:
        raw = m.group(4)
        if raw is None:
            alpha = 1.0
        elif raw.endswith("%"):
            alpha = float(raw[:-1]) / 100
        else:
            alpha = float(raw)
        return "#%02X%02X%02X" % tuple(int(m.group(i)) for i in (1, 2, 3)), max(0.0, min(1.0, alpha))
    m = re.match(r"#([0-9a-fA-F]{8})\b", v)
    if m:
        h = m.group(1)
        return f"#{h[:6]}", int(h[6:], 16) / 255
    m = re.match(r"var\(\s*--([a-z0-9-]+)", v)
    if m:
        spec = tokens.get("alpha", {}).get(m.group(1))
        if spec:
            raw = spec["value"] if isinstance(spec, dict) else spec
            return _resolve_translucent(raw, tokens)
    return None


def _composite(top: str, alpha: float, under: str) -> str:
    """把半透明前层叠在不透明底层上，算出实际可见色。"""
    return "#%02X%02X%02X" % tuple(
        round(alpha * t + (1 - alpha) * u) for t, u in zip(hex2rgb(top), hex2rgb(under))
    )


def _resolve_color(value: str, tokens: dict) -> str | None:
    value = value.strip()
    m = re.match(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b", value)
    if m:
        return m.group(0)
    m = re.match(r"var\(\s*--([a-z0-9-]+)", value)
    if m:
        key = m.group(1)
        alias = tokens["legacy_aliases"].get(key, key)
        spec = tokens["color"].get(alias)
        if spec:
            return spec["value"]
    return None


def _is_large(block_body: str) -> bool:
    m = LARGE_RE.search(block_body)
    if not m:
        return False
    val, unit = float(m.group(1)), m.group(2)
    px = val if unit == "px" else val * 16
    bold = re.search(r"font-weight\s*:\s*(?:bold|[7-9]00)", block_body) is not None
    return px >= 24 or (px >= 18.66 and bold)


def _norm_selector(sel: str) -> list[str]:
    """生成一个选择器的候选查找键：原样、去伪类伪元素、**末段**复合类逐级削减。

    注意：复合类削减只能作用在最后一个简单选择器上。早期版本直接对整个选择器
    `split(".")`，`.reveal-card .ro` 会被削成 `".reveal-card "`（带尾空格），
    于是 `.reveal-card .rs` 查表时撞上这个键，把兄弟元素的背景当成自己的，
    产出一堆假的对比度 P0。
    """
    sel = re.sub(r"\s+", " ", sel.strip())
    keys = [sel]
    bare = re.sub(r"::?[a-z-]+(\([^)]*\))?", "", sel).strip()
    bare = re.sub(r"\s+", " ", bare)
    if bare and bare != sel:
        keys.append(bare)
    for k in list(keys):
        parts = k.split()
        if not parts:
            continue
        segs = parts[-1].split(".")
        while len(segs) > 2:
            segs = segs[:-1]
            keys.append(" ".join(parts[:-1] + [".".join(segs)]))
    return [k for k in dict.fromkeys(keys) if k and k == k.strip()]


# 交互态与伪元素的背景不代表元素自身的底色：
#   .cool-btn-outline:hover{background:var(--ink)} 不是常态背景；
#   .dot-dim::before{background:var(--accent)} 只是一个 7px 装饰圆点。
# 把它们计入背景索引会造出大量假 P0。
PSEUDO_NOT_BG = re.compile(
    r"::|:(?:hover|focus|focus-visible|focus-within|active|target|checked|disabled|visited)\b",
    re.I,
)

VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input",
             "link", "meta", "param", "source", "track", "wbr"}


class _DomPaths(HTMLParser):
    """收集每个元素的祖先链（tag + class 集合）。

    纯 CSS 选择器链解析不到 `.kw`、`.str` 这类**裸类名**的背景——它们写在
    `.code-mac pre` 里面，选择器本身不含任何祖先信息。只看 CSS 就只能"按页面
    底色假设"，于是深色代码面板里的语法高亮全被误报。读一遍真实 DOM 就能定位
    到它们实际压在哪个容器上。
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, set[str]]] = []
        self.paths: list[list[tuple[str, set[str]]]] = []
        self.at: list[tuple[int, int]] = []  # 与 paths 一一对应的 (行, 列)

    def handle_starttag(self, tag, attrs):
        cls = set((dict(attrs).get("class") or "").split())
        self.stack.append((tag, cls))
        self.paths.append(list(self.stack))
        self.at.append(self.getpos())
        if tag in VOID_TAGS:
            self.stack.pop()

    def handle_startendtag(self, tag, attrs):
        cls = set((dict(attrs).get("class") or "").split())
        self.paths.append(list(self.stack) + [(tag, cls)])
        self.at.append(self.getpos())

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break


def _parse_compound(tok: str) -> tuple[str | None, frozenset[str]] | None:
    """`div.a.b` -> ('div', {'a','b'})。带 # / [] / * 的选择器不支持，返回 None。"""
    if any(c in tok for c in "#[]*"):
        return None
    tok = re.sub(r"::?[a-z-]+(\([^)]*\))?", "", tok)
    m = re.fullmatch(r"([a-zA-Z][\w-]*)?((?:\.[\w-]+)*)", tok or "")
    if not m:
        return None
    tag = m.group(1).lower() if m.group(1) else None
    classes = frozenset(re.findall(r"\.([\w-]+)", m.group(2) or ""))
    return (tag, classes) if (tag or classes) else None


def _parse_selector(sel: str) -> list[tuple[str | None, frozenset[str]]] | None:
    """只支持后代/子代组合（> 视作后代）；兄弟选择器不支持。"""
    if "+" in sel or "~" in sel:
        return None
    parts = []
    for tok in sel.replace(">", " ").split():
        c = _parse_compound(tok)
        if c is None:
            return None
        parts.append(c)
    return parts or None


def _match_compound(el: tuple[str, set[str]], part: tuple[str | None, frozenset[str]]) -> bool:
    tag, classes = el
    ptag, pclasses = part
    return (ptag is None or tag == ptag) and pclasses <= classes


def _matches(path: list[tuple[str, set[str]]], parts: list) -> bool:
    """parts 作为子序列匹配 path，且最后一段必须命中 path 末元素。"""
    if not _match_compound(path[-1], parts[-1]):
        return False
    i, j = len(parts) - 2, len(path) - 2
    while i >= 0 and j >= 0:
        if _match_compound(path[j], parts[i]):
            i -= 1
        j -= 1
    return i < 0


def _bg_rules(styles: str, tokens: dict) -> list[tuple[list, str, int, int]]:
    """收集可解析的 background 规则：(选择器段, 颜色, 出现次序, 特异度)。"""
    rules = []
    for order, (sel, decl) in enumerate(_css_blocks(styles)):
        m = re.search(r"background(?:-color)?\s*:\s*([^;]+)", decl)
        if not m:
            continue
        parts_val = m.group(1).split()
        color = _resolve_color(parts_val[0], tokens) if parts_val else None
        if not color:
            continue
        for one in sel.split(","):
            one = one.strip()
            if PSEUDO_NOT_BG.search(one):
                continue
            parsed = _parse_selector(one)
            if parsed:
                spec = sum(len(c) for _, c in parsed) * 10 + len(parsed)
                rules.append((parsed, color, order, spec))
    return rules


def _dom_bg_table(text: str, styles: str, tokens: dict) -> list[tuple[list, str]]:
    """给每个 DOM 元素算出生效背景（自身没有就沿祖先继承）。整份文件只算一次。"""
    key = (_txt_key(text), "table")
    if key in _DOM_CACHE:
        return _DOM_CACHE[key]
    rules = _bg_rules(styles, tokens)
    table: list[tuple[list, str]] = []
    for path in _dom_cache(text).paths:
        bg = None
        for k in range(len(path), 0, -1):  # 自身 -> 祖先
            sub = path[:k]
            best = None
            for parsed, color, order, spec in rules:
                if _matches(sub, parsed) and (best is None or (spec, order) > best[:2]):
                    best = (spec, order, color)
            if best:
                bg = best[2]
                break
        if bg:
            table.append((path, bg))
    _DOM_CACHE[key] = table
    return table


def _dom_any_match(text: str, parsed: list) -> bool:
    return any(_matches(path, parsed) for path in _dom_cache(text).paths)


def _fg_rules(styles: str) -> list[tuple[list, int, int]]:
    """收集所有声明了 `color:` 的规则，用于判断某条规则在哪些元素上真正生效。

    没有这一步会误判：`.fnc{color:var(--code-fn)}` 是深底面板用的，
    而 `.code-cl .fnc{...}` 在白底面板上覆盖了它——按 CSS 层叠，
    白底里的 .fnc 根本不是冷蓝色，不该拿白底去核对深底那条规则。
    """
    key = ("__fg", _txt_key(styles))
    if key in _FG_CACHE:
        return _FG_CACHE[key]
    out: list[tuple[list, int, int]] = []
    for order, (sel, decl) in enumerate(_css_blocks(styles)):
        if not re.search(r"(?<!-)color\s*:", decl):
            continue
        for one in sel.split(","):
            one = one.strip()
            if PSEUDO_NOT_BG.search(one):  # 交互态不覆盖静态态
                continue
            parsed = _parse_selector(one)
            if parsed:
                out.append((parsed, order, sum(len(c) for _, c in parsed) * 10 + len(parsed)))
    _FG_CACHE[key] = out
    return out


_FG_CACHE: dict[tuple, list] = {}


def dom_background(
    text: str, styles: str, sel: str, tokens: dict, own: tuple[int, int] | None = None
) -> tuple[str, str] | None:
    """用真实 DOM 判定该选择器的文字实际压在什么背景上（多数表决）。

    `own=(order, specificity)` 给出时，会跳过那些被更具体的 color 规则覆盖掉的元素。
    返回 ("bg", 色值) / ("nobg", "") / ("dead", "") / None（选择器不支持解析）。
    """
    first = sel.split(",")[0].strip()
    if not first:
        return None
    parsed = _parse_selector(first)
    if parsed is None:
        return None
    overrides = []
    if own is not None:
        overrides = [(p, o, s) for p, o, s in _fg_rules(styles) if (s, o) > (own[1], own[0])]

    def wins(path) -> bool:
        return not any(_matches(path, p) for p, _, _ in overrides)

    votes: Counter = Counter()
    for path, bg in _dom_bg_table(text, styles, tokens):
        if _matches(path, parsed) and wins(path):
            votes[bg] += 1
    if votes:
        return ("bg", votes.most_common(1)[0][0])
    hit = [p for p in _dom_cache(text).paths if _matches(p, parsed)]
    if hit:
        return ("nobg", "") if any(wins(p) for p in hit) else ("bg", "")
    return ("dead", "")          # 没有任何元素命中 -> 死代码


_DOM_CACHE: dict = {}


def _txt_key(text: str) -> tuple[int, int]:
    """按内容取缓存键。用 id() 会踩坑：字符串被回收后新对象可能拿到同一个地址，
    于是 rule_default_styles 传的原文和 rule_contrast 传的去 tokens 版会互相命中，
    整份文件的 DOM 都被换掉——表现为一堆"静态 HTML 里找不到元素"的假死代码告警。"""
    return (len(text), hash(text))


def _dom_cache(text: str) -> _DomPaths:
    key = _txt_key(text)
    if key not in _DOM_CACHE:
        p = _DomPaths()
        try:
            p.feed(text)
        except Exception:  # 容错：HTML 再脏也不该让 linter 崩
            pass
        _DOM_CACHE[key] = p
    return _DOM_CACHE[key]


def _css_blocks(styles: str) -> list[tuple[str, str]]:
    """解析 CSS 规则块。先去注释，否则注释会被当成选择器的一部分。"""
    clean = re.sub(r"/\*.*?\*/", " ", styles, flags=re.S)
    out = []
    for m in CSS_BLOCK_RE.finditer(clean):
        sel = m.group(1).strip().splitlines()[-1].strip() if m.group(1).strip() else ""
        if not sel or sel.startswith("@"):
            continue
        out.append((sel, m.group(2)))
    return out


def rule_contrast(text: str, rel: str, tokens: dict, f: Findings, scope: str = "page") -> None:
    """按 CSS 规则块解析真实的前景/背景配对；解析不到背景时降级为 P1 并注明是假设值。"""
    cream = tokens["color"]["cream"]["value"]
    body = strip_tokens_block(text)
    styles = "".join(m.group(1) for m in re.finditer(r"<style[^>]*>(.*?)</style>", body, re.S))
    blocks = _css_blocks(styles)

    bg_by_selector: dict[str, str] = {}
    for sel, decl in blocks:
        m = re.search(r"background(?:-color)?\s*:\s*([^;]+)", decl)
        if not m:
            continue
        first = m.group(1).split()[0] if m.group(1).split() else ""
        resolved = _resolve_color(first, tokens)
        if not resolved:
            continue
        for one in sel.split(","):
            one = one.strip()
            if PSEUDO_NOT_BG.search(one):  # 交互态/伪元素背景不入索引
                continue
            for key in _norm_selector(one):
                bg_by_selector.setdefault(key, resolved)

    # 卡片场景的"页面底色"是导出画布 .card，不是预览外壳 body
    if scope == "card":
        page_bg = bg_by_selector.get(".card") or bg_by_selector.get("body") or cream
    else:
        page_bg = bg_by_selector.get("body") or bg_by_selector.get("html") or cream

    for order, (sel, decl) in enumerate(blocks):
        # 前景既要认字面 hex，也要认 var(--token)：否则 `color: var(--accent)`
        # 这类「装饰色当正文用」的错误会完全逃过检查。
        cm = re.search(r"(?<!-)color\s*:\s*(#[0-9a-fA-F]{3,6}\b|var\(\s*--[a-z0-9-]+\s*[,)])", decl)
        if not cm:
            continue
        fg = _resolve_color(cm.group(1).rstrip(",)"), tokens)
        if not fg:
            continue
        if "--ds-contrast-ok" in decl:  # 人工确认过的例外（如压在图片蒙版上）
            continue
        bg, assumed = None, True
        own_layer = None  # 自身的半透明色块，最后再叠到解析出的底色上
        own = re.search(r"background(?:-color)?\s*:\s*([^;]+)", decl)
        if own:
            first = own.group(1).split()[0] if own.group(1).split() else ""
            bg = _resolve_color(first, tokens) or _scrim_color(own.group(1))
            assumed = bg is None
            if bg is None:
                layer = _resolve_translucent(first, tokens)
                if layer and layer[1] >= 0.995:
                    bg, assumed = layer[0], False
                elif layer and layer[1] > 0.0:
                    own_layer = layer
        if bg is None:
            first_sel = sel.split(",")[0].strip()
            # 自身（去伪类）-> 最近祖先 -> 更远祖先
            for key in _norm_selector(first_sel):
                if key in bg_by_selector:
                    bg, assumed = bg_by_selector[key], False
                    break
            if bg is None:
                parts = first_sel.split()
                for i in range(len(parts) - 1, 0, -1):
                    for key in _norm_selector(" ".join(parts[:i])):  # 只用祖先前缀，不用裸类名（会误撞无关的同名全局类）
                        if key in bg_by_selector:
                            bg, assumed = bg_by_selector[key], False
                            break
                    if bg is not None:
                        break
        if bg is None:  # CSS 选择器链走不通，再问一次真实 DOM
            first_sel = sel.split(",")[0].strip()
            parsed_own = _parse_selector(first_sel)
            own_key = None
            if parsed_own:
                own_key = (order, sum(len(c) for _, c in parsed_own) * 10 + len(parsed_own))
            got = dom_background(body, styles, sel, tokens, own=own_key)
            if got and got[0] == "bg" and not got[1]:
                continue  # 命中的元素全被更具体的 color 规则覆盖了，这条规则实际不生效
            if got and got[0] == "bg":
                bg, assumed = got[1], False
            elif got and got[0] == "dead":
                f.add("R5", P2, rel, None,
                      f"`{sel[:56]}` 在静态 HTML 里没有匹配到元素，无法核对对比度",
                      "若由 JS 动态生成，请人工确认；若是死代码，删掉以减少 AI 读取噪声")
                continue
        if bg is None:
            bg, assumed = page_bg, True
        if own_layer:  # 半透明色块叠在底色上，用混色后的真实底色核对
            bg = _composite(own_layer[0], own_layer[1], bg)

        ratio = contrast(fg, bg)
        need = 3.0 if _is_large(decl) else 4.5
        if ratio >= need:
            continue
        sev = P0 if not assumed else P1
        note = "" if not assumed else "（背景未解析出，按页面底色假设，请人工确认）"
        f.add("R5", sev, rel, None,
              f"`{sel[:56]}` 文字 {fg} 压在 {bg} 上对比度 {ratio:.2f}:1，需 ≥{need}{note}",
              "换 --ink / --ink-light / --ink-faint / --accent-ink / --pop-ink；深色面板上用 --cream / --accent")


# ---------- R6 布局重复 ----------
def rule_layout_variety(text: str, rel: str, f: Findings) -> None:
    sections = re.findall(r"<section\b([^>]*)>", text, re.I)
    if len(sections) < 4:
        return
    sigs = []
    for attrs in sections:
        cls = re.search(r'class\s*=\s*"([^"]*)"', attrs)
        sigs.append(" ".join(sorted((cls.group(1) if cls else "").split())))
    common, n = Counter(sigs).most_common(1)[0]
    ratio = n / len(sigs)
    if ratio > 0.5:
        f.add("R6", P1, rel, None,
              f"{len(sigs)} 个 section 中 {n} 个（{ratio:.0%}）结构签名相同：'{common or '(无 class)'}'",
              "从 layouts.md 换 3~5 种不同布局分配给各 section")


# ---------- R8 导出确定性（card 域） ----------
CANVAS_RE = re.compile(r"\.card\s*\{[^}]*?width\s*:\s*(\d+)px[^}]*?height\s*:\s*(\d+)px", re.S)


def rule_export_determinism(text: str, rel: str, f: Findings) -> None:
    """固定画布卡片：任何视口相关单位都会让导出 PNG 随窗口宽度变化。"""
    body = strip_tokens_block(text)
    for m in re.finditer(r"(?:font-size|width|height|padding|margin|gap|top|left|right|bottom)\s*:[^;{}]*?([0-9.]+)(vw|vh|vmin|vmax)\b", body):
        f.add("R8", P0, rel, line_of(body, m.start()),
              f"导出画布内使用视口单位 {m.group(1)}{m.group(2)}，会导致导出 PNG 随浏览器窗口变化",
              "卡片场景改用固定 px；缩放交给 .card 的 transform: scale()")
    for m in re.finditer(r"clamp\(", body):
        f.add("R8", P1, rel, line_of(body, m.start()),
              "导出画布内使用 clamp()，导出尺寸不确定",
              "卡片场景用固定 px（这是 card 域的正确写法，不是违规）")
    m = CANVAS_RE.search(body)
    if not m:
        f.add("R8", P0, rel, None, ".card 未锁定固定画布尺寸",
              "写死 width/height（如 1080px × 1440px 即 3:4）以保证导出比例")
    else:
        w, h = int(m.group(1)), int(m.group(2))
        ratio = w / h
        if abs(ratio - 0.75) > 0.01:
            f.add("R8", P1, rel, line_of(body, m.start()),
                  f"画布 {w}×{h} 比例 {ratio:.3f}，不是小红书 3:4（0.75）",
                  "改成 1080×1440 或其他 3:4 尺寸")


# ---------- R7 文档一致性 ----------
# 「选 3-5 种布局」是让 AI 挑几个，不是在声明库里只有 5 种；
# 「16 种经过验证的布局模式」才是清单声明。只有后者需要和实际数量对账。
_PICK_RE = re.compile(r"(?:[选挑取用留加]\s*|最多\s*|至少\s*|每\s*|共\s*\d+\s*个中\s*|\d+\s*[-~–—]\s*)$")


def _is_inventory_claim(txt: str, pos: int) -> bool:
    """判断数字是「库里一共有 N 个」还是「从库里挑 N 个」。"""
    return not _PICK_RE.search(txt[max(0, pos - 16):pos])


def rule_docs(f: Findings) -> None:
    comp_dir = ROOT / "references" / "components"
    comp_single = ROOT / "references" / "components.md"
    ids: set[int] = set()
    if comp_dir.exists():
        for p in sorted(comp_dir.glob("*.md")):
            for m in re.finditer(r"^##\s*(\d+)\.\s", p.read_text(encoding="utf-8"), re.M):
                ids.add(int(m.group(1)))
    elif comp_single.exists():
        for m in re.finditer(r"^##\s*(\d+)\.\s", comp_single.read_text(encoding="utf-8"), re.M):
            ids.add(int(m.group(1)))
    n_comp = len(ids)
    layouts = ROOT / "references" / "layouts.md"
    n_layout = len(re.findall(r"^##\s*\d+\.\s", layouts.read_text(encoding="utf-8"), re.M)) if layouts.exists() else 0

    for doc in ("README.md", "SKILL.md", "references/components.md",
                "references/components/00-index.md"):
        p = ROOT / doc
        if not p.exists():
            continue
        txt = p.read_text(encoding="utf-8")
        for m in re.finditer(r"(\d+)\s*个?\s*(?:经过验证的)?(?:可复用)?组件", txt):
            if _is_inventory_claim(txt, m.start()) and int(m.group(1)) != n_comp:
                f.add("R7", P1, doc, line_of(txt, m.start()),
                      f"声明「{m.group(1)} 个组件」，实际 {n_comp} 个", f"改成 {n_comp}")
        for m in re.finditer(r"(\d+)\s*种(?:经过验证的)?布局", txt):
            if _is_inventory_claim(txt, m.start()) and int(m.group(1)) != n_layout:
                f.add("R7", P1, doc, line_of(txt, m.start()),
                      f"声明「{m.group(1)} 种布局」，实际 {n_layout} 种", f"改成 {n_layout}")

    readme = ROOT / "README.md"
    if readme.exists():
        txt = readme.read_text(encoding="utf-8")
        for m in re.finditer(r"https://([a-z0-9-]+)\.github\.io/([a-z0-9._-]+)/([^)\s]+)", txt, re.I):
            user, repo, path = m.groups()
            if repo == ROOT.name:
                if not (ROOT / path).exists():
                    f.add("R7", P0, "README.md", line_of(txt, m.start()),
                          f"Pages 链接指向仓库中不存在的文件: {path}", "修正路径或补上文件")
            else:
                f.add("R7", P0, "README.md", line_of(txt, m.start()),
                      f"链接指向他人仓库 {user}/{repo}，对本仓库是坏链",
                      f"改成 https://{{你的用户名}}.github.io/{ROOT.name}/… 或移到 Credits 并标注来源")


# ---------- 主流程 ----------
HTML_TARGETS = sorted(
    [p for p in ROOT.glob("*.html")] + [p for p in (ROOT / "assets").glob("*.html")]
)


def render_report(f: Findings, files: list[str], baseline: dict | None) -> str:
    out = ["# Design System Lint Report", ""]
    out.append(f"检查文件 {len(files)} 个 · **P0 {f.count(P0)}** · P1 {f.count(P1)} · P2 {f.count(P2)}")
    out.append("")
    if f.scopes:
        by_scope: dict[str, list[str]] = {}
        for file, sc in f.scopes.items():
            by_scope.setdefault(sc, []).append(file)
        out += ["## 场景域", "", "| 域 | 生效规则 | 文件 |", "|---|---|---|"]
        rules = {"page": "R1-R7", "card": "R1·R2·R3·R5·R8", "wechat": "R1·R2·R3", "gallery": "R1-R6"}
        for sc in sorted(by_scope):
            out.append(f"| `{sc}` | {rules.get(sc, '-')} | {', '.join(sorted(by_scope[sc]))} |")
        out.append("")
    if baseline:
        b = Counter(i["rule"] for i in baseline.get("findings", []))
        c = Counter(i["rule"] for i in f.items)
        out += ["## 与基线对比", "", "| 规则 | 基线 | 当前 | 变化 |", "|---|---|---|---|"]
        for rule in sorted(set(b) | set(c)):
            delta = c[rule] - b[rule]
            out.append(f"| {rule} | {b[rule]} | {c[rule]} | {delta:+d} |")
        out.append("")
    by_rule: dict[str, list[dict]] = {}
    for i in f.items:
        by_rule.setdefault(i["rule"], []).append(i)
    for rule in sorted(by_rule):
        items = by_rule[rule]
        out.append(f"## {rule} — {len(items)} 条")
        out.append("")
        agg: dict[tuple[str, str, str], list[int | None]] = {}
        for i in items:
            agg.setdefault((i["file"], i["severity"], i["message"]), []).append(i["line"])
        for (file, sev, msg), lines in sorted(agg.items()):
            shown = [str(l) for l in lines[:6] if l is not None]
            loc = f":{','.join(shown)}" + ("…" if len(lines) > 6 else "") if shown else ""
            out.append(f"- **[{sev}]** `{file}{loc}` — {msg}")
        out.append("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*", help="限定检查的文件（默认全量 HTML）")
    ap.add_argument("--json", dest="json_out", help="输出 JSON 路径")
    ap.add_argument("--baseline", help="基线 JSON，用于对比")
    ap.add_argument("--report", help="输出 markdown 报告路径")
    args = ap.parse_args()

    tokens = load_tokens()
    targets = [(ROOT / x).resolve() for x in args.files] if args.files else HTML_TARGETS
    f = Findings()
    checked: list[str] = []

    scopes: dict[str, str] = {}
    for path in targets:
        if not path.exists():
            print(f"[WARN] 文件不存在，已跳过: {path}", file=sys.stderr)
            continue
        try:
            rel = str(path.relative_to(ROOT))
        except ValueError:
            # 允许检查仓库外的文件（临时验证、CI 缓存目录等），用文件名当标识
            rel = path.name
        raw = path.read_text(encoding="utf-8")
        text = strip_b64(raw)  # base64 载荷会污染所有正则
        scope = scope_of(rel, text)
        scopes[rel] = scope
        checked.append(rel)

        # 全域规则
        rule_colors(text, rel, tokens, f, scope)
        rule_fonts(text, rel, tokens, f)
        rule_default_styles(text, rel, f)
        # 分域规则
        if scope in ("page", "gallery"):
            rule_fluid(text, rel, f)
            rule_layout_variety(text, rel, f)
        if scope in ("page", "card", "gallery"):
            rule_a11y(text, rel, tokens, f)
            rule_contrast(text, rel, tokens, f, scope)
        if scope == "card":
            rule_export_determinism(text, rel, f)
    if not args.files:
        rule_docs(f)
    f.scopes = scopes

    baseline = json.loads(Path(args.baseline).read_text(encoding="utf-8")) if args.baseline else None
    report = render_report(f, checked, baseline)
    print(report)

    if args.json_out:
        Path(args.json_out).write_text(
            json.dumps({"summary": {"P0": f.count(P0), "P1": f.count(P1), "P2": f.count(P2),
                                    "files": checked, "scopes": f.scopes}, "findings": f.items},
                       ensure_ascii=False, indent=2), encoding="utf-8")
    if args.report:
        Path(args.report).write_text(report, encoding="utf-8")

    return 1 if f.count(P0) else 0


if __name__ == "__main__":
    sys.exit(main())
