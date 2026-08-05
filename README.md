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

51个经过验证的可复用组件。

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
esther-design-system/
├── SKILL.md                    ← 7步工作流(大脑)
├── brand-dna.md                ← 品牌基因:颜色/字体/气质/禁忌(需配置)
├── palettes-preview.html       ← 配色选择器(点色卡实时预览10套)
├── assets/                     ← 模板骨架(起点)
│   ├── palettes.css                ← 10套配色 + 语义token(单一事实来源)
│   ├── template-tutorial.html      教程页模板
│   ├── template-landing.html       活动页模板
│   ├── template-app.html           App型模板
│   ├── template-cards.html         小红书卡片模板
│   ├── html2canvas.min.js          卡片导出依赖
│   ├── avatar-placeholder.svg      占位头像(可替换为你自己的 avatar.jpg)
│   └── avatar.jpg                  ← 你的头像(需自行放入,仓库未附带)
├── scripts/
│   └── validate-palettes.mjs       ← 校验主题 token、RGB 通道和对比度
└── references/                 ← 规则和零件(知识库)
    ├── layouts.md                  16种布局模式(附完整代码)
    ├── components.md               组件库(51组件,完整HTML+CSS)
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

### 配色 — 10 套可选，一个属性切换

```html
<html lang="zh-CN" data-palette="C">   <!-- A ~ J，不写默认 A -->
```

| # | 名字 | 主色 | # | 名字 | 主色 |
|---|------|------|---|------|------|
| **A** | 经典 Classic（默认） | `#2B7FD8` | **F** | 豆沙 Red Bean | `#96545C` |
| **B** | 黛蓝 Ink Blue | `#33548A` | **G** | 藕荷 Orchid | `#8A2F84` |
| **C** | 莓紫 Mulberry | `#7A3560` | **H** | 孔雀蓝 Peacock | `#15697C` |
| **D** | 鼠尾草 Sage | `#41684F` | **I** | 紫藤 Wisteria | `#71519B` |
| **E** | 赤茶 Terracotta | `#A8452F` | **J** | 珊瑚 Coral | `#C33D46` |

👉 **打开 `palettes-preview.html` 点色卡实时预览**，挑好再写进 `data-palette`。

每套都按主色 60% · 强调色 30% · 点缀色 10%组织，并通过自动化的
token 完整性、RGB 通道同步和对比度校验。校验项会随语义角色增加而变化，
以 `node scripts/validate-palettes.mjs` 的实时结果为准。

配色定义集中在 `assets/palettes.css`，组件只用语义 token
（`--brand` / `--highlight` / `--pop` / `--ink` …），所以换配色不用改任何组件代码。
其中 `--brand` / `--pop` 保留主题最有辨识度的展示色；小字号文字用
`--brand-text` / `--pop-text`，带字按钮和色块用 `--brand-surface` /
`--pop-surface`，既保留原色观感，也保证实际阅读场景的对比度。
跨模板复用时可使用 `--brand-primary-*` / `--brand-accent-*` / `--brand-pop-*` 别名；
`--focus-ring`、`--border-strong` 和 `--highlighter` 负责交互反馈与高亮，
`palettes.css` 还会统一处理 `prefers-reduced-motion`。

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
3. **挑配色**：打开 `palettes-preview.html` 点色卡预览，选好后把字母写进模板的 `<html data-palette="X">`。
   想用自己的品牌色，就改 `assets/palettes.css` 里某一套的色值 —— 只改这一个文件，全站生效。
   ⚠️ 手改色值可能打破对比度保证，改完运行 `node scripts/validate-palettes.mjs`。
   注意：公众号模板（`template-wechat.html`）因为要粘进公众号编辑器，全部是内联样式、不能用 CSS 变量，需要手动搜索替换色值
4. 把 `assets/template-cards.html` 中的作者名替换成你自己的
5. 把仓库链接发给你的 AI Agent，跟它说：

> 帮我读这个设计系统，以后做页面按这个规范来。

核心不是这些文件本身，是**你的审美判断力**。文件只是把你的判断写成了 AI 能执行的规则。

---

## Credits

- 方法论灵感来源于 [归藏](https://github.com/guizang) 的 PPT Skill——“限制AI的自由度 = 保证输出质量”这个核心思路参考了他的设计
