# Brand DNA — 品牌基因

> ⚠️ **使用前请确认配置：** 本设计系统内置 **5 套配色（A–E）**，默认启用 **A · 原色**。
> 换配色只需要改一个属性：`<html data-palette="c">`，模板里现有的 CSS 一行都不用动。
> 想看实际观感和实测对比度，打开 `palettes.html`。头像、气质关键词请替换成你自己的。

---

## 🎨 配色系统（5 套可切换）

**当前启用：A · 原色**（改 `<html>` 上的 `data-palette` 即可切换）

| 配色 | 主色 60% | 强调 30% | 点缀 10% | 气质 | 英文名 |
|---|---|---|---|---|---|
| **A · 原色** **（当前启用）** | `#2B7FD8` | `#F4D758` | `#E84A5F` | 明亮、亲和、可信赖 | Cobalt & Butter |
| **B · 松墨** | `#35774B` | `#EEBC5D` | `#D15A42` | 文人、沉静、耐看 | Ink Pine |
| **C · 陶土** | `#B35630` | `#ECD06E` | `#348979` | 手作、温暖、土陶质感 | Terracotta |
| **D · 梅子** | `#87486D` | `#FCCC69` | `#5F8041` | 柔和有格调、不甜 | Mulberry & Honey |
| **E · 山墨** | `#3C352E` | `#E5CCA6` | `#C8482F` | 极简编辑感、印刷味最重 | Sumi & Vermilion |

三色比例原则不变：主色 60% · 强调色 30% · 点缀色 10%（点缀色永远是点缀，不做主色）。

五套配色的 `ink / ink-light / ink-faint / cream / cream-dark / dark-panel` **明度台阶是对齐的**，
所以换配色只换气质、不换视觉节奏——同一个页面换到任何一套，字重和层级感觉都一样。派生色
（`-deep / -soft / accent-ink`）在 OKLCH 里按感知明度推导，不是 HSL 机械变暗，所以不会脏、不会偏色。

### 三层令牌结构

色值的唯一事实来源是 `assets/palettes.css`（4 个模板内联同一份副本，因为模板必须单文件可离线打开）。

```css
/* 第 1 层 · 配色定义：5 套 × 16 个色值 */
:root, [data-palette="a"] { --p-primary: #2B7FD8; --p-accent: #F4D758; /* … */ }
[data-palette="b"]        { --p-primary: #35774B; --p-accent: #EEBC5D; /* … */ }

/* 第 2 层 · 语义令牌：页面只认这一层 */
:root {
  --brand-primary: var(--p-primary);
  --brand-primary-deep: var(--p-primary-deep);
  /* … */
  /* 兼容别名：老代码继续用 --blue/--yellow/--red，零改动 */
  --blue: var(--brand-primary);  --yellow: var(--brand-accent);  --red: var(--brand-pop);
}

/* 第 3 层 · 全局细节：::selection、:focus-visible、prefers-reduced-motion */
```

CSS 自定义属性在**使用处**按元素解析，所以 `<html data-palette="c">` 让 `--p-primary` 命中 C 的值，
`--brand-primary` 和 `--blue` 自动跟着变，整棵树继承。**换配色 = 改一个属性值。**

### 成文的用色规则（这些是对比度实测得出的，不是口味）

- **正文小字和链接用 `--brand-primary-deep`；`--brand-primary` 只用于大标题和装饰。**
  A 配色的 `#2B7FD8` on 暖底只有 3.99 : 1 —— 够大字（≥3.0），不够小字（需 4.5）。
- **实心强调色块上的文字用 `--ink`；`--brand-accent-ink` 只用在 `--brand-accent-soft` 浅底上。**
  饱和的中黄上放深黄字永远过不了 AA，这是色彩物理决定的，不是调不出来。
- **点缀色当小字用 `--brand-pop-deep`。**
- **实心色块上的白色小字需要 `-deep` 底。** 白字 on 主色 / 主色深 / 点缀 / 深色面板实测：

  | 配色 | `#fff` on primary | on primary-deep | on pop | on dark-panel |
  |---|---|---|---|---|
| A · 原色 | 4.09 | 6.74 | 3.77 | 17.73 |
| B · 松墨 | 5.40 | 8.48 | 4.00 | 17.54 |
| C · 陶土 | 4.89 | 7.65 | 4.20 | 17.43 |
| D · 梅子 | 6.61 | 10.29 | 4.52 | 17.50 |
| E · 山墨 | 12.06 | 17.00 | 4.75 | 17.53 |

  大字门槛 3.0 处处满足；小字门槛 4.5 只有 primary-deep 和 dark-panel 处处满足。
- **半透明色块写 `rgba(var(--brand-primary-rgb), .08)`，不要写死 `rgba(43,127,216,.08)`** ——
  否则换配色时它不跟着变。`palettes.css` 为 ink / primary / accent / pop 发布了 `--*-rgb` 三元组。
- **辅助小字落在 `--cream-dark` 色带或更深的纸感底板上时，改用 `--ink-light`。**
  `--ink-faint` 在 `#F5F0E8`、`#EFE8D8` 这类纸色上实测只有 4.11–4.66，不达标。
- **文档片段写 `var(--token, #hex)` 形式** —— 微信等会剥掉 `:root` 的编辑器里仍能降级到 A 配色。

### 刻意不跟随配色的颜色

不是漏了，是故意的：**语法高亮色**（约定俗成，像 macOS 红绿灯点一样属于「共识色」）、
**macOS 窗口红绿灯点** `#ff5f56/#ffbd2e/#27c93f`、**纸感底板**（`#F5F0E8` 打字机纸、`#FFFEF8` 笔记纸、
`#EFE8D8` 金句纸）。这些换了会失去所指。语法高亮按容器分亮/暗两套，亮底整体压暗过 AA，色相彩度不变。

### 全部 5 套配色的完整色值

**A · 原色 — Cobalt & Butter**　`<html data-palette="a">`　适合：日常首选 · 教程 · 科普

| 令牌 | 色值 | 对比度实测 |
|---|---|---|
| `--p-primary` | `#2B7FD8` | 3.99 : 1 on 底色 |
| `--p-primary-deep` | `#1E5BA8` | 6.57 : 1 on 底色 |
| `--p-primary-soft` | `#E2EEFE` |  |
| `--p-accent` | `#F4D758` |  |
| `--p-accent-soft` | `#FFF3CD` |  |
| `--p-accent-ink` | `#78671B` | 5.05 : 1 on 浅强调底 |
| `--p-pop` | `#E84A5F` | 3.67 : 1 on 底色 |
| `--p-pop-deep` | `#BF2A44` | 5.64 : 1 on 底色 |
| `--p-cream` | `#FEFCF6` |  |
| `--p-cream-dark` | `#FAF6EB` |  |
| `--p-card` | `#FFFEFC` |  |
| `--p-ink` | `#1A1A2E` | 16.63 : 1 on 底色 |
| `--p-ink-light` | `#4A4A5A` | 8.04 : 1 on 色带 |
| `--p-ink-faint` | `#6D6E7E` | 4.65 : 1 on 色带 |
| `--p-dark-panel` | `#151821` | 17.28 : 1 浅字 on 面板 |
| `--p-dark-panel-2` | `#292B3C` |  |

**B · 松墨 — Ink Pine**　`<html data-palette="b">`　适合：长文 · 读书笔记 · 复盘

| 令牌 | 色值 | 对比度实测 |
|---|---|---|
| `--p-primary` | `#35774B` | 5.26 : 1 on 底色 |
| `--p-primary-deep` | `#175830` | 8.27 : 1 on 底色 |
| `--p-primary-soft` | `#DFF3E3` |  |
| `--p-accent` | `#EEBC5D` |  |
| `--p-accent-soft` | `#FEEED4` |  |
| `--p-accent-ink` | `#846015` | 5.02 : 1 on 浅强调底 |
| `--p-pop` | `#D15A42` | 3.90 : 1 on 底色 |
| `--p-pop-deep` | `#AA3C27` | 6.05 : 1 on 底色 |
| `--p-cream` | `#FEFCF6` |  |
| `--p-cream-dark` | `#F7F1E3` |  |
| `--p-card` | `#FFFEFC` |  |
| `--p-ink` | `#19211C` | 16.05 : 1 on 底色 |
| `--p-ink-light` | `#454E48` | 7.65 : 1 on 色带 |
| `--p-ink-faint` | `#646E68` | 4.69 : 1 on 色带 |
| `--p-dark-panel` | `#0F1C15` | 17.10 : 1 浅字 on 面板 |
| `--p-dark-panel-2` | `#223028` |  |

**C · 陶土 — Terracotta**　`<html data-palette="c">`　适合：作品集 · 生活方式 · 活动页

| 令牌 | 色值 | 对比度实测 |
|---|---|---|
| `--p-primary` | `#B35630` | 4.78 : 1 on 底色 |
| `--p-primary-deep` | `#8E3912` | 7.47 : 1 on 底色 |
| `--p-primary-soft` | `#FEE8DF` |  |
| `--p-accent` | `#ECD06E` |  |
| `--p-accent-soft` | `#FDF1C5` |  |
| `--p-accent-ink` | `#7A6514` | 5.02 : 1 on 浅强调底 |
| `--p-pop` | `#348979` | 4.10 : 1 on 底色 |
| `--p-pop-deep` | `#16695A` | 6.40 : 1 on 底色 |
| `--p-cream` | `#FFFCF5` |  |
| `--p-cream-dark` | `#F9F1E0` |  |
| `--p-card` | `#FFFEFC` |  |
| `--p-ink` | `#271D18` | 16.07 : 1 on 底色 |
| `--p-ink-light` | `#564942` | 7.70 : 1 on 色带 |
| `--p-ink-faint` | `#786961` | 4.68 : 1 on 色带 |
| `--p-dark-panel` | `#241710` | 17.01 : 1 浅字 on 面板 |
| `--p-dark-panel-2` | `#382921` |  |

**D · 梅子 — Mulberry & Honey**　`<html data-palette="d">`　适合：个人主页 · 分享会 · 图文卡片

| 令牌 | 色值 | 对比度实测 |
|---|---|---|
| `--p-primary` | `#87486D` | 6.45 : 1 on 底色 |
| `--p-primary-deep` | `#652D4F` | 10.04 : 1 on 底色 |
| `--p-primary-soft` | `#F9E7F0` |  |
| `--p-accent` | `#FCCC69` |  |
| `--p-accent-soft` | `#FEEFD2` |  |
| `--p-accent-ink` | `#826114` | 5.04 : 1 on 浅强调底 |
| `--p-pop` | `#5F8041` | 4.41 : 1 on 底色 |
| `--p-pop-deep` | `#426126` | 6.91 : 1 on 底色 |
| `--p-cream` | `#FFFCF6` |  |
| `--p-cream-dark` | `#F8F1E3` |  |
| `--p-card` | `#FFFEFC` |  |
| `--p-ink` | `#271C23` | 16.06 : 1 on 底色 |
| `--p-ink-light` | `#53494F` | 7.68 : 1 on 色带 |
| `--p-ink-faint` | `#756971` | 4.65 : 1 on 色带 |
| `--p-dark-panel` | `#24151D` | 17.09 : 1 浅字 on 面板 |
| `--p-dark-panel-2` | `#37272F` |  |

**E · 山墨 — Sumi & Vermilion**　`<html data-palette="e">`　适合：作品集 · 观点长文 · 高级感

| 令牌 | 色值 | 对比度实测 |
|---|---|---|
| `--p-primary` | `#3C352E` | 11.76 : 1 on 底色 |
| `--p-primary-deep` | `#221B15` | 16.57 : 1 on 底色 |
| `--p-primary-soft` | `#F9EADB` |  |
| `--p-accent` | `#E5CCA6` |  |
| `--p-accent-soft` | `#FEEED7` |  |
| `--p-accent-ink` | `#81612E` | 5.00 : 1 on 浅强调底 |
| `--p-pop` | `#C8482F` | 4.63 : 1 on 底色 |
| `--p-pop-deep` | `#A12911` | 7.21 : 1 on 底色 |
| `--p-cream` | `#FEFCF6` |  |
| `--p-cream-dark` | `#F8F1E2` |  |
| `--p-card` | `#FFFEFC` |  |
| `--p-ink` | `#221F1A` | 16.00 : 1 on 底色 |
| `--p-ink-light` | `#504B46` | 7.66 : 1 on 色带 |
| `--p-ink-faint` | `#716B65` | 4.68 : 1 on 色带 |
| `--p-dark-panel` | `#1F1812` | 17.09 : 1 浅字 on 面板 |
| `--p-dark-panel-2` | `#322B24` |  |

---

## 👤 头像/IP形象

请将你的头像文件放入 `assets/avatar.jpg`（建议正方形，至少 400×400px）。

如果你有完整IP形象（全身/半身），放入 `assets/character.png`。

### 使用规则
- 需要头像时优先用 `assets/avatar.jpg`
- 是否在页面中使用IP形象由你决定，不强制

---

## 🔤 字体基因

### 核心原则
- **标题用衬线，正文用无衬线** — 混搭产生节奏
- **中英文搭配** — 英文做装饰/标签，中文承载内容
- **字号对比极端** — 大的要很大，小的要真的小

### 推荐字体池

| 场景 | 推荐 | 备注 |
|------|------|------|
| 英文装饰/标题 | `Fraunces` (italic) | 有品质的衬线体 |
| 英文手写/轻松 | `Caveat` | 手绘感、标注、注释 |
| 英文等宽/终端 | `Fira Code` | 技术/终端场景专用 |
| 中文标题首选 | `Huiwen Mincho`（汇文明朝体） | 需本地ttf文件 |
| 中文标题备选 | `Noto Serif SC` (900) | 无本地字体时的衬线体fallback |
| 中文正文 | `Noto Sans SC` + 系统栈 | 跨平台无衬线 |

### 字号系统（fluid sizing）
- Hero大标题: `clamp(2.8rem, 7vw, 5.5rem)`
- Section标题: `clamp(1.6rem, 4vw, 2.6rem)`
- 卡片标题: `1.15rem ~ 1.4rem`
- 正文: `16px`
- 辅助文字: `0.78rem ~ 0.85rem`
- 大装饰数字: `clamp(3rem, 8vw, 7rem)` + `opacity: 0.12~0.2`

---

## ✨ 气质关键词

设计出来的东西应该让人觉得：

- **可爱但有品质** — 不是幼儿风也不是奢侈风
- **手绘蜡笔感** — 有温度、有人味
- **不像AI** — 这是最高优先级的约束
- **有设计师眼光** — 细节讲究、间距精确、色彩克制
- **温暖但不幼稚** — 有内容有深度
- **个人品牌感** — 一看就知道是"你的"

> 💡 请根据你自己的品牌调性修改上面的关键词。

---

## 🎨 配色扩展原则

当 16 个令牌不够用时：

- 背景永远偏暖：用 `--cream`（主背景）、`--cream-dark`（深奶）
- 文字永远非纯黑：用 `--ink`（墨色）
- 次要文字：`--ink-light`、`--ink-faint`
- 绝不用纯黑 `#000` 或纯白 `#fff` 作大面积底色
- 暗色场景底色：`--dark-panel`、`--dark-panel-2`（仅适用于 HTML 全屏页面，3:4 卡片场景禁止深色底）
- 终端绿：`#4ade80`（仅终端风格场景使用）
- 径向渐变制造层次，不用纯平色

---

## 🚫 通用禁忌清单

| 类型 | 禁止 |
|------|------|
| 配色 | 蓝紫渐变、cyan、neon、纯黑白、AI常用的冷灰蓝调、任何多色渐变背景（占位色块用纯色 `#FFF8E1` 或 `#F4D758`，荧光笔高亮的 `linear-gradient(transparent 60%, #F4D758 60%)` 保留） |
| 深色版面 | 仅3:4图文卡片场景禁止黑色/深色版面；HTML全屏页面可用深色面板 |
| 字体 | Inter/Roboto/Arial等overused字体（除非明确是终端风格辅助字体）、monospace充当"技术感" |
| 布局 | 所有section居中、千篇一律卡片网格、cards嵌套cards |
| 动效 | bounce/elastic、animate width/height、无限循环动画 |
| 装饰 | glassmorphism、圆角矩形+阴影千篇一律、渐变文字、AI光效、border-left 竖线引用块（类似 Notion/飞书的左侧竖条引用样式） |
| 整体 | 看起来像AI生成的通用模板、generic Landing Page模板感 |
| 边框 | 强调色装饰边框细于40px（统一40px，不得更细） |
| 排版 | 行间距/字间距必须肉眼检查，不允许出现过松或过紧的异常节奏 |
| 图片 | AI生成的stock photo风、过度滤镜、无意义装饰图 |
| 默认样式 | HTML默认blockquote、默认border-left引用块、无样式ul/ol列表、默认table——所有组件必须从components.md选用，绝不允许浏览器默认渲染 |

### 自检问题
做完设计后问自己：
1. 这个页面截图发到社交媒体，会不会被人评论"又是AI做的"？
2. 能不能一眼认出这是你的品牌？
3. 有没有哪个部分让你觉得"见过很多次了"？

---

## 📐 通用间距原则

- Section之间: `clamp(80px, 12vh, 160px)`
- 内容块之间: `clamp(40px, 6vw, 100px)`
- 卡片内padding: `clamp(28px, 3vw, 44px)`
- 元素间gap: `clamp(24px, 3vw, 48px)`
- 全部用 `clamp()` 做fluid sizing
- `max-width: 1300px` + `margin: 0 auto` 约束内容宽度

---

## 📱 响应式通用规则

- 断点: 900px（两栏→单栏）、600px（字号微缩）
- 移动端是"重新排列"不是"缩小"
- 尊重 `prefers-reduced-motion`
- 移动端不隐藏内容——adapt不amputate

---

## 🔍 细节规范

- **选中文本高亮**: 已由 `assets/palettes.css` 全局提供 —— `::selection { background: var(--brand-accent); color: var(--ink); }`，各页面不必再写。
- **键盘焦点环**: `:focus-visible { outline: 2px solid var(--focus-ring); outline-offset: 3px }`。同样已全局提供。**不要写 `outline: none`** —— 键盘用户会彻底失去位置感。
- **降低动效偏好**: `@media (prefers-reduced-motion: reduce)` 已全局提供。
- **链接悬停**: 用强调色底色块或下划线，不用变色

---

*This is the foundation. Every scene file builds on top of this.*
