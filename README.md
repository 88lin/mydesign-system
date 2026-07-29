# Personal Design Skill

一套给 AI 看的个人品牌设计系统。

把审美写成操作手册，AI 每次帮你做页面时必须翻这本手册，不能自由发挥。**限制 AI 的自由度 = 保证输出质量。**

> ⚠️ **使用前请先完成 `brand-dna.md` 的配置：** 默认品牌色可直接使用，如需替换成你自己的请同步修改模板变量；并放入你自己的头像。

---

## Demo

用这套系统生成的真实页面：

### 📖 教程型 - 分享会页面

信息清晰、步骤明确、有节奏的单页科普/教程。

🔗 [在线预览](https://esthersjw.github.io/cola-ob-sharing/cola-ob-sharing.html)

---

### 📖 教程型 - Design Skill 拆解

把审美写成操作手册——从纠正AI到做出自己的Design Skill的完整过程。

🔗 [在线预览](https://esthersjw.github.io/esther-design-system/demo-readme-tutorial.html)

---

### 🎪 活动页 / Landing

视觉冲击、深浅面板交替、强节奏感的活动邀请页。

🔗 [在线预览](https://esthersjw.github.io/esther-design-system/demo-landing.html)

---

### 📱 App 型 / 功能型

功能优先、交互感、信息密度高的应用型页面。

🔗 [在线预览](https://esthersjw.github.io/esther-design-system/demo-app.html)

---

### 📕 小红书图文卡片

3:4 比例、字大、手机可读、一键导出 PNG 的图文卡片。

🔗 [在线预览](https://esthersjw.github.io/esther-design-system/demo-cards.html)

---

### 📱 公众号排版

杂志编号风：全内联样式 + section 标签，复制粘贴进微信公众号编辑器即可。

🔗 [在线预览](https://esthersjw.github.io/esther-design-system/assets/demo-wechat.html)

---

### 📜 布局 Playground

16种经过验证的布局模式一览。

🔗 [在线预览](https://esthersjw.github.io/esther-design-system/demo-layouts.html)

---

### 🧩 组件库全览

52个经过验证的可复用组件。

🔗 [组件库预览](https://esthersjw.github.io/esther-design-system/components-preview.html)

---

## 核心逻辑

```
SKILL.md(流程 - AI 按什么步骤干活)
    ↓
brand-dna.md + references/*(规范 - 能用什么不能用什么)
    ↓
assets/template-*.html(起点 - 从模板改,不从零写)
```

- AI 不能随便发明布局 → 只能从 16 种里选
- AI 不能随便用颜色 → 只能用你定义的品牌色 + 扩展规则
- AI 不能随便写样式 → 必须从组件库里选
- AI 做完要自检 → 对照 checklist 逐条过，P0 不过就打回

---

## 文件结构

```
mydesign-system/
├── SKILL.md                    ← 7步工作流(大脑)
├── brand-dna.md                ← 品牌基因:颜色/字体/气质/禁忌(需配置)
├── assets/                     ← 模板骨架(起点)
│   ├── template-tutorial.html      教程页模板
│   ├── template-landing.html       活动页模板
│   ├── template-app.html           App型模板
│   ├── template-cards.html         小红书卡片模板
│   ├── html2canvas.min.js          卡片导出依赖
│   ├── avatar-placeholder.svg      占位头像(可替换为你自己的 avatar.jpg)
│   └── avatar.jpg                  示例头像(已附带,请替换成你自己的)
└── references/                 ← 规则和零件(知识库)
    ├── layouts.md                  16种布局模式(附完整代码)
    ├── components.md               组件库(52组件,完整HTML+CSS)
    ├── checklist.md                质量检查清单(P0/P1/P2)
    ├── scene-tutorial.md           教程场景规范
    ├── scene-landing.md            活动页场景规范
    ├── scene-app.md                App型场景规范
    ├── scene-cards.md              小红书卡片场景规范
    └── scene-wechat.md             公众号排版场景规范
```

---

## 7 步工作流

AI 每次做设计必须按这个顺序走：

| # | 做什么 | 为什么 |
|---|--------|--------|
| 1 | 问 5 个问题(类型/受众/几屏/素材/约束)。类型含：教程/活动页/App/卡片/**公众号** | 不自作主张 |
| 2 | 读 brand-dna + 对应场景文件 | 先学规矩再动手 |
| 3 | 从 assets/ 复制对应模板 | 从半成品开始，不从零写 |
| 4 | 从 layouts.md 选 3-5 种布局 | 每个 section 不能一样 |
| 5 | 从 components.md 选组件 | 禁止用 HTML 默认样式 |
| 6 | 对照 checklist 自检 | P0 不过就打回 |
| 7 | 交付 HTML 文件 | 浏览器打开就能看 |

---

## 品牌基因速览

### 三色（默认配色，可在brand-dna.md中替换为你自己的）

| 颜色 | 色值 | 比例 |
|------|------|------|
| 主色 | `var(--brand-primary)` | 60% |
| 强调色 | `var(--brand-accent)` | 30% |
| 点缀色 | `var(--brand-pop)` | 10% |

> 具体色值随当前启用的配色变化（A 配色为 `#2B7FD8` / `#F4D758` / `#E84A5F`）。

### 字体

| 用途 | 字体 |
|------|------|
| 中文标题 | 汇文明朝体 / Noto Serif SC |
| 中文正文 | Noto Sans SC |
| 英文装饰 | Fraunces italic |
| 手写/注释 | Caveat |
| 代码/终端 | Fira Code |

### 气质关键词（请根据你的品牌调性修改）

可爱但有品质 · 手绘蜡笔感 · 有温度 · **不像 AI** · 一看就是你的

### 禁忌

蓝紫渐变 · glassmorphism · neon · bounce 动画 · Inter/Roboto · 所有 section 居中 · HTML 默认样式 · 看起来像 AI 生成的通用模板

---

## 质量检查

**P0(必须全过)**

品牌三色比例 · 无禁忌元素 · 无 HTML 默认样式 · 暖底背景 · 衬线+无衬线混搭 · 响应式 · 每 section 布局不同 · clamp() fluid sizing · 截图发社交媒体不会被说"又是 AI 做的"

**P1(应过)**

至少一个视觉惊喜 section · 字号对比极端 · Scroll Reveal 动效 · 大装饰数字/英文

**P2(加分)**

图片溢出容器 · 深色面板打破节奏 · 装饰元素克制 · prefers-reduced-motion

---

## 怎么用

1. Fork 或克隆本仓库
2. 放入你的头像 `assets/avatar.jpg`
3. （可选）打开 `brand-dna.md`，把默认品牌色替换成你自己的，并同步修改 `assets/template-*.html` 里 `:root` 的变量。注意：公众号模板（`template-wechat.html`）全部是内联样式，没有 CSS 变量，需要手动搜索替换色值。快捷方法：在所有模板文件中搜索 `#2B7FD8` 替换为你的主色，`#F4D758` 替换为你的强调色，`#E84A5F` 替换为你的点缀色
4. 把 `assets/template-cards.html` 中的作者名替换成你自己的
5. 把仓库链接发给你的 AI Agent，跟它说：

> 帮我读这个设计系统，以后做页面按这个规范来。

核心不是这些文件本身，是**你的审美判断力**。文件只是把你的判断写成了 AI 能执行的规则。

---

## 配色

内置 **5 套配色**，默认 A · 原色。换配色改一个属性即可，模板里现有的 CSS 一行都不用动：

```html
<html lang="zh-CN" data-palette="c">   <!-- a 原色 / b 松墨 / c 陶土 / d 梅子 / e 山墨 -->
```

| 配色 | 气质 | 适合 |
|---|---|---|
| **A · 原色** | 明亮、亲和、可信赖 | 日常首选 · 教程 · 科普 |
| **B · 松墨** | 文人、沉静、耐看 | 长文 · 读书笔记 · 复盘 |
| **C · 陶土** | 手作、温暖、土陶质感 | 作品集 · 生活方式 · 活动页 |
| **D · 梅子** | 柔和有格调、不甜 | 个人主页 · 分享会 · 图文卡片 |
| **E · 山墨** | 极简编辑感、印刷味最重 | 作品集 · 观点长文 · 高级感 |

打开 `palettes.html` 可以实时切换、看完整色板与 16 条对比度门槛的实测读数，
并一键复制当前配色的全部色值（喂给公众号编辑器的搜索替换）。色值的唯一事实来源是
`assets/palettes.css`；详细令牌结构和用色规则见 `brand-dna.md`。

> 公众号模板是纯内联样式（微信编辑器会剥掉 CSS 变量），用不了令牌。
> `references/scene-wechat.md` 里有 A–E × 全令牌的十六进制对照表，换色就是机械搜索替换。

---

## Credits

- 本仓库起源于 [esthersjw/esther-design-system](https://github.com/esthersjw/esther-design-system)，在其基础上加入了多配色令牌系统与一轮可达性修缮
- 上面各场景的「在线预览」链接目前指向**上游作者的 GitHub Pages**。在本仓库 Settings → Pages 里开启 Pages 后，把链接域名换成你自己的即可
- 方法论灵感来源于 [归藏](https://github.com/guizang) 的 PPT Skill——“限制AI的自由度 = 保证输出质量”这个核心思路参考了他的设计
