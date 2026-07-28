# 质量检查清单

> 做完设计后逐条对照。P0必须全过，否则打回修改。
>
> 这份清单是**可执行**的：`python scripts/lint_design.py` 会自动核对其中大部分条目。
> 检查器报 P0 就等于这份清单没过。人工只需要盯住机器查不了的几条（气质、布局多样性、视觉惊喜）。

---

## 适用范围（重要）

不同场景的规则**不一样**，尤其是响应式。照单全收会做出错的东西。

| 场景 | 典型文件 | 响应式 | 深色面板 | CSS 变量 |
|---|---|---|---|---|
| **page** 全屏 HTML 页 | `demo-landing.html`、`demo-app.html`、`demo-readme-tutorial.html`、`assets/template-*.html`（app/landing/tutorial）| 必须有 900px 断点 + `clamp()` | 允许 | 允许 |
| **card** 3:4 图文卡片 | `demo-cards.html`、`assets/template-cards.html` | **禁止** `vw`/`vh`/`clamp()`/断点 | **禁止** | 允许 |
| **gallery** 组件库/布局库 | `components-preview.html`、`demo-layouts.html` | 必须有 900px 断点 | 允许 | 允许 |
| **wechat** 公众号 | `assets/template-wechat.html`、`assets/demo-wechat.html` | 不适用（平台容器决定）| 允许 | **禁止**（微信会剥掉 `<style>`，必须全内联字面值）|

检查器会按文件名自动判断场景；也可以在 HTML 顶部显式声明：`<!-- ds-scope: card -->`。

**为什么卡片场景反着来**：卡片是固定 `1080×1440px` 的导出画布，用 `transform: scale()` 预览、`html2canvas` 导出 PNG。
`vw` 会让**导出的图片**随浏览器窗口尺寸变化——同一份卡片在不同人的机器上导出结果不同。所以卡片场景一律固定 px。

---

## P0（必须全过）

任何一条不过就要改。右列是对应的检查器规则，`—` 表示只能人工判断。

### 配色

| 检查项 | 规则 |
|---|---|
| 没有使用已废弃的旧色值（`#A63D6F` / `#B59AD4` 等）| R1 |
| 没有多色渐变背景（≥3 色，或 2 个不同色的软过渡）| R1 |
| 背景使用品牌暖底（`--cream` / `--cream-dark` / `--card-bg`），非纯黑纯白 | R1 |
| 品牌三色比例大致 60/30/10，点缀色没有当主色用 | — |
| 没有使用禁忌清单里的任何元素（蓝紫渐变/neon/居中病/bounce）| 部分 R1 |
| **文字对比度全部达标**：正文 ≥4.5:1，大字（≥24px 或 ≥19px 粗体）≥3.0:1 | R5 |
| **半透明色块上的文字按合成后底色算**，不是按页面底色算 | R5 |
| 紫色/红色文字用了对应的 `-ink` / `-deep` 变体，不是直接用 `--accent` / `--pop` | R1 + R5 |

> 对比度是这份清单里最容易被"看着还行"糊过去的一条。所有数值以 `brand-dna.md` 的用法矩阵为准，那张表由 `tokens.json` 自动生成，不会漂移。

### 字体

| 检查项 | 规则 |
|---|---|
| 没有 Inter/Roboto/Arial/Helvetica Neue/Poppins 等 overused 字体 | R2 |
| 字体走 `var(--font-*)` token，不手写字体栈（wechat 场景除外）| R2 |
| 标题衬线 + 正文无衬线混搭 | — |
| Web 字体只引一个 URL（`font_loading.canonical_url`）| R2 |

### 结构与默认样式

| 检查项 | 规则 |
|---|---|
| 没有使用任何 HTML 默认样式（默认 blockquote、无样式 ul/ol、默认 table）| R3 |
| 没有裸 `border-left` 竖线引用块（Notion/飞书那种）| R3 |
| 每个 section 布局形式不同（page/gallery 场景）| R6 |
| 组件全部来自 `references/components/`，没有现场发明 | — |

> R3 认「祖先选择器统一接管」：`.cblock ul { ... }` 让里面所有 `<ul>` 都算已样式化，不必每个都挂 class。

### 响应式与无障碍

| 检查项 | 规则 | 适用场景 |
|---|---|---|
| 有 900px 断点，且是**重新排列**不是缩小 | R4 | page / gallery |
| `clamp()` 做 fluid sizing，没有写死 ≥2rem 的字号 | R4 | page / gallery |
| **不用** `vw`/`vh`/`clamp()`，尺寸锁 1080×1440（3:4 ±0.01）| R8 | card |
| **尊重 `prefers-reduced-motion`** — 见下方说明 | R5 | 全部 |
| 键盘焦点可见（`:focus-visible` 有环，没有裸 `outline: none`）| R5 | 全部 |

### 气质（人工）

| 检查项 |
|---|
| 截图发 Twitter 不会被说"又是AI做的" |
| 一眼能认出是你的品牌 |
| 没有哪个部分让你觉得"见过很多次了" |

---

## 关于 `prefers-reduced-motion`（从 P2 提升到 P0）

这一条原来在 P2「加分项」，**提到 P0**，原因是它不是审美偏好而是无障碍底线：前庭功能障碍者看到大幅位移/缩放动画会产生眩晕和恶心，`prefers-reduced-motion` 是他们唯一的表达渠道。本设计系统大量使用 Scroll Reveal + stagger，正是最需要降级的动效类型。

必须写成这样：

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
  .reveal, [class*="reveal"] { opacity: 1 !important; transform: none !important; }
}
```

**最后一行是重点**，也是最容易漏的地方：Scroll Reveal 的初始状态通常是 `opacity: 0` + `transform: translateY(30px)`，靠 JS 加 class 触发动画。如果只把动画时长压到 0，元素会**停在初始状态永久不可见**——降级反而把内容弄没了。必须显式把 `opacity` 和 `transform` 恢复。

---

## P1（应过）

尽量满足，提升品质：

- [ ] 至少一个 section 有视觉惊喜（出血/3D/全宽色块/装饰突破）
- [ ] 字号对比足够极端（大的 >3rem，小的 <0.85rem）
- [ ] 有 Scroll Reveal 动效 + stagger 延迟（配合上面的 reduced-motion 降级）
- [ ] 使用了大装饰数字或大透明英文做背景
- [ ] 有**品牌色条或高亮标记** — 注意这里指 ≥4px 品牌色实心条 + 至少一项其他设计，不是裸 `border-left` 灰线。区分标准见 `brand-dna.md` 的「品牌色条 vs Notion 竖线」
- [ ] `::selection` 用强调色高亮（`background: var(--accent); color: var(--ink)`）
- [ ] 文档里声明的组件数/布局数与实际一致（R7 会核对）

---

## P2（加分）

锦上添花：

- [ ] 图片溢出容器边界
- [ ] 有全宽深色面板打破节奏（仅 page/gallery 场景）
- [ ] 装饰元素（虚线圆/渐变光晕/条纹肌理）使用克制
- [ ] 色值全部走 `var(--token)`，没有裸写十六进制（R1 会提示；wechat 场景豁免）

---

## 逃生舱：`--ds-contrast-ok`

极少数情况下，文字并不压在自身元素的背景上——例如白字压在**同级**蒙版元素 `.ov { background: rgba(0,0,0,.85) }` 之上。静态分析看不出这层关系，会误报。

这时在该 CSS 规则里加一条自定义属性说明原因，检查器就会跳过：

```css
.mag-hero .mt {
  color: #fff;
  --ds-contrast-ok: "白字压在同级 .ov 的 rgba(0,0,0,.85) 蒙版上，非本元素背景";
}
```

写成 CSS 自定义属性而不是注释，是因为构建流程会剥掉注释。

**这是逃生舱，不是消音器。** 滥用它等于关掉无障碍检查。用之前先确认：真的是分析器看不见的层叠关系，而不是"这个对比度我觉得够了"。理由必须写清楚，以后别人（包括 AI）读到才知道能不能删。

---

## 怎么跑检查器

```bash
python scripts/build_tokens.py --check   # tokens.json 与全仓库是否同步
python scripts/lint_design.py            # 输出 P0/P1/P2 清单
python scripts/lint_design.py --json out.json --report out.md
python scripts/lint_design.py demo-app.html   # 只查单个文件
```

CI 里两条都会跑，P0 不为 0 直接失败。
