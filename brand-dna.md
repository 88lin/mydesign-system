# Brand DNA — 品牌基因

> ⚠️ **使用前请确认配置：** 配色已备好 10 套（A~J），选一套写进 `data-palette` 即可，不用自己调色。头像和气质关键词请替换成你自己的。

---

## 🎨 配色系统 — 10 套可选

配色不写死在页面里，全部集中在 **`assets/palettes.css`**。
换配色只改一个地方 —— `<html>` 上的 `data-palette`：

```html
<html lang="zh-CN" data-palette="C">   <!-- A ~ J，不写默认 A -->
```

想直接看效果、挑一套：打开 **`palettes-preview.html`**，点色卡实时切换整页。

### 10 套配色

| # | 名字 | 主色 | 强调色 | 点缀色 | 气质 |
|---|------|------|--------|--------|------|
| **A** | 经典 Classic | `#2B7FD8` | `#F4D758` | `#E84A5F` | 原版蓝黄红，识别度和亲和力最平衡（默认） |
| **B** | 黛蓝 Ink Blue | `#33548A` | `#F6C9D3` | `#C0395C` | 冷静克制，粉色只做柔光不做主角 |
| **C** | 莓紫 Mulberry | `#7A3560` | `#F7CDA9` | `#2F6B63` | 低饱和紫红，复古杂志感 |
| **D** | 鼠尾草 Sage | `#41684F` | `#F4D793` | `#B44761` | 温柔植物调，最耐看 |
| **E** | 赤茶 Terracotta | `#A8452F` | `#EFCE9A` | `#2F6B5B` | 陶土暖调，手作质感 |
| **F** | 豆沙 Red Bean | `#96545C` | `#EFD3A8` | `#7D5D91` | 最柔和的一套，气质安静 |
| **G** | 藕荷 Orchid | `#8A2F84` | `#F7DEA4` | `#BF4436` | 梦幻兰紫配奶油黄，甜而不腻；朱砂点缀拉出精神 |
| **H** | 孔雀蓝 Peacock | `#15697C` | `#F5CDB4` | `#B24935` | 通透的宝石蓝绿，清冷里带一点暖粉 |
| **I** | 紫藤 Wisteria | `#71519B` | `#F6DC8E` | `#B54070` | 梦幻但压得住，不甜腻 |
| **J** | 珊瑚 Coral | `#C33D46` | `#FBD97C` | `#2C7967` | 明亮外向，活力感最强 |

### 语义 token（写代码只用这些，永不写死色值）

| Token | 角色 | 用途 |
|-------|------|------|
| `--brand` | 主色 **60%** | 大标题、图形、装饰线；保留主题原色 |
| `--brand-text` | 品牌文字 | 小字号标题、链接、标签（正文级 AA） |
| `--brand-surface` / `--on-brand` | 品牌承载色 / 前景 | 主按钮、带字色块 |
| `--brand-deep` | 主色深阶 | hover、强调层级 |
| `--brand-tint` | 主色浅阶 | 柔和装饰、旧组件兼容，不承载正文 |
| `--brand-border` | 品牌描边 | 控件边界、焦点环（非文本 3:1） |
| `--brand-on-dark` | 深底品牌色 | 深色面板上的品牌提示文字 |
| `--brand-primary-*` / `--brand-accent-*` / `--brand-pop-*` | 新模板兼容别名 | 分别对应主色、强调色、点缀色，便于跨模板复用 |
| `--highlight` / `--on-highlight` | 强调色 **30%** / 前景 | 荧光笔高亮、badge、连接线 |
| `--highlight-soft` | 强调柔光 | 占位色块、浅底提示 |
| `--pop` | 点缀色 **10%** | 图形、装饰、下划线；保留主题原色 |
| `--pop-text` | 点缀文字 | 小字号标签、强调链接（正文级 AA） |
| `--pop-surface` / `--on-pop` | 点缀承载色 / 前景 | CTA、带字色块 |
| `--pop-deep` / `--pop-soft` | 点缀深阶 / 柔光 | hover、浅色提示背景 |
| `--cream` / `--cream-dark` | 背景 | 主背景 / 次级背景（section 交替） |
| `--ink` / `--ink-light` / `--ink-faint` | 文字 | 正文 / 次要 / 辅助 |
| `--dark-panel` | 深色面板底 | 打破节奏的全宽面板 |
| `--on-dark` / `--on-dark-dim` | 深底文字 | 深色面板上的正文 / 次要文字 |
| `--border` / `--hairline` / `--card-bg` | 结构 | 描边 / 细线 / 卡片底 |
| `--border-strong` / `--focus-ring` | 交互反馈 | 强描边 / 键盘焦点环 |
| `--highlighter` | 高亮 | `linear-gradient` 荧光笔效果，跟随当前强调色 |
| `--success` / `--warning` / `--danger-strong` / `--info` | 状态文字 | 成功 / 警告 / 危险 / 信息，独立于主题点缀色 |
| `--success-soft` / `--warning-soft` / `--danger-soft` / `--info-soft` | 状态柔光 | 对应状态的浅色背景 |

三色比例原则：**主色 60% · 强调色 30% · 点缀色 10%**，点缀色永远是点缀，不做主色。

> 💡 老色名 `--blue` / `--yellow` / `--red` 仍可用（已在 `palettes.css` 里映射到语义 token），
> 但**新代码请用语义名** —— 换配色后 `--blue` 可能根本不是蓝的。

### 全部通过对比度校验

运行下面的命令会按当前 CSS 实时检查全部主题，而不是依赖文档中的静态数字：

```bash
node scripts/validate-palettes.mjs
```

检查覆盖正文和按钮前景 4.5:1、控件边界 3:1、深色面板、状态色、
RGB 通道同步以及必需 token 完整性。原始 `--brand` / `--pop` 是展示色，
只要求满足大字或装饰用途；普通正文必须使用 `*-text`，带字色块必须使用 `*-surface`。

改色值前先想清楚：**任何手改都可能打破这个保证。**

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
| 中文标题首选 | `Huiwen Mincho`（汇文明朝体） | 优先使用系统已安装字体；仓库未捆绑字体文件，不要引用不存在的 ttf |
| 中文标题备选 | `Noto Serif SC` (900) | 默认可用的衬线体 fallback |
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

**第一原则：不写死主题色值，用 token。** 核心色、语义角色和状态色已覆盖绝大多数需求。

当 token 不够用时：

- 页面背景永远偏暖：`var(--cream)` / `var(--cream-dark)`；卡片使用 `var(--card-bg)`，不要直接写 `#fff`
- 文字永远非纯黑：`var(--ink)` / `--ink-light` / `--ink-faint`，绝不用纯黑 `#000`
- 深色面板：`var(--dark-panel)` + `var(--on-dark)` 承载文字
  （每套配色的深色面板都是**与主色同源的暖调深色**，不是冷灰蓝）
  仅适用于 HTML 全屏页面，3:4 卡片场景禁止深色底
- 需要半透明时使用同步通道：`rgba(var(--brand-rgb), .12)`、
  `rgba(var(--highlight-rgb), .18)`、`rgba(var(--pop-rgb), .12)` 或
  `rgba(var(--ink-rgb), .08)`；这套写法同时兼容当前 html2canvas
- 共享组件不要用 `color-mix()`：当前卡片导出链路无法可靠解析
- 终端语法色、macOS 三色圆点等“被模拟界面自身的标准颜色”可以在隔离组件内写死，
  但不能拿来充当页面的品牌色或状态色
- 公众号模板需要复制进第三方编辑器，是静态内联色例外；修改时要同步搜索替换整份模板
- 渐变只能组合当前主题 token，并用于局部层次或装饰，不能发明新的主题外颜色

**新增颜色前先自问：能不能用现有 token 表达？** 90% 的情况可以。

---

## 🚫 通用禁忌清单

| 类型 | 禁止 |
|------|------|
| 配色 | 蓝紫渐变、cyan、neon、纯黑白、AI常用的冷灰蓝调、任何多色渐变背景（占位色块用纯色 `var(--highlight-soft)` 或 `var(--highlight)`，荧光笔高亮的 `linear-gradient(transparent 60%, var(--highlight) 60%)` 保留） |
| 写死色值 | 品牌色、状态色、页面中性色必须用 token；只允许隔离的终端/系统控件模拟和公众号内联模板保留必要硬编码 |
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

- **选中文本高亮**: `palettes.css` 里已全局设好 `::selection`，不用重复写
- **链接悬停**: 用 `var(--highlight)` 底色块或下划线，不用变色

---

*This is the foundation. Every scene file builds on top of this.*
