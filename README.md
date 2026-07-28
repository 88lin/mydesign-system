# Personal Design Skill

一套给 AI 看的个人品牌设计系统。

把审美写成操作手册，AI 每次帮你做页面时必须翻这本手册，不能自由发挥。**限制 AI 的自由度 = 保证输出质量。**

> ⚠️ **使用前请先完成 `brand-dna.md` 的配置：** 默认品牌色可直接使用，如需替换成你自己的请同步修改模板变量；并放入你自己的头像。

---

## Demo

用这套系统生成的真实页面（[总入口](https://88lin.github.io/mydesign-system/)）：

### 📖 教程型 - Design Skill 拆解

把审美写成操作手册——从纠正AI到做出自己的Design Skill的完整过程。

🔗 [在线预览](https://88lin.github.io/mydesign-system/demo-readme-tutorial.html)

---

### 🎪 活动页 / Landing

视觉冲击、深浅面板交替、强节奏感的活动邀请页。

🔗 [在线预览](https://88lin.github.io/mydesign-system/demo-landing.html)

---

### 📱 App 型 / 功能型

功能优先、交互感、信息密度高的应用型页面。

🔗 [在线预览](https://88lin.github.io/mydesign-system/demo-app.html)

---

### 📕 小红书图文卡片

3:4 比例、字大、手机可读、一键导出 PNG 的图文卡片。

🔗 [在线预览](https://88lin.github.io/mydesign-system/demo-cards.html)

---

### 📱 公众号排版

杂志编号风：全内联样式 + section 标签，复制粘贴进微信公众号编辑器即可。

🔗 [在线预览](https://88lin.github.io/mydesign-system/assets/demo-wechat.html)

---

### 📜 布局 Playground

16种经过验证的布局模式一览。

🔗 [在线预览](https://88lin.github.io/mydesign-system/demo-layouts.html)

---

### 🧩 组件库全览

52个经过验证的可复用组件。

🔗 [组件库预览](https://88lin.github.io/mydesign-system/components-preview.html)

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
├── brand-dna.md                ← 品牌基因:颜色/字体/气质/禁忌(部分内容由脚本生成)
├── tokens.json                 ← 设计令牌唯一来源:颜色/字号/间距/字体加载
├── index.html                  ← 作品集首页(Demo 总入口)
├── CHANGELOG.md                ← 版本变更记录
├── scripts/                    ← 工具链
│   ├── build_tokens.py             tokens.json → 各文件(带 --check)
│   ├── lint_design.py              规范检查器(8 类规则,带 --json/--report)
│   └── split_components.py         组件库分片(带 --check)
├── assets/                     ← 模板骨架(起点)
│   ├── template-tutorial.html      教程页模板
│   ├── template-landing.html       活动页模板
│   ├── template-app.html           App型模板
│   ├── template-cards.html         小红书卡片模板
│   ├── html2canvas.min.js          卡片导出依赖
│   ├── avatar-placeholder.svg      占位头像(可替换为你自己的 avatar.jpg)
│   └── avatar.jpg                  ← 你的头像(需自行放入,仓库未附带)
└── references/                 ← 规则和零件(知识库)
    ├── layouts.md                  16种布局模式(附完整代码)
    ├── components/                 组件库(52组件,按功能拆成9个分片)
    │   ├── 00-index.md                 ← 入口:场景索引+组件清单,先读这个
    │   ├── 01-卡片与网格.md
    │   ├── 02-引用与金句.md
    │   └── ...                         其余7个分片
    ├── components.md               指针,指向 components/00-index.md
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
| 5 | 先读 components/00-index.md 定位编号,再加载对应分片选组件 | 禁止用 HTML 默认样式;别整库读入 |
| 6 | 对照 checklist 自检 | P0 不过就打回 |
| 7 | 交付 HTML 文件 | 浏览器打开就能看 |

---

## 品牌基因速览

### 三色（默认配色，可在brand-dna.md中替换为你自己的）

| 角色 | Token | 色值 | 比例 | 说明 |
|------|-------|------|------|------|
| 主色 | `--brand` | `#A63D6F` 莓果玫红 | 60% | 大面积底色、品牌色条、按钮 |
| 强调色 | `--accent` | `#B59AD4` 藤萝紫 | 30% | 高亮块、装饰、chip 底色 |
| 点缀色 | `--pop` | `#E84A5F` 珊瑚红 | 10% | 只用来点睛，不要成片 |

> ⚠️ 这三支是**视觉识别色，不是文字色**。`--accent` 在暖底上对比度只有 2.40，正文/小字请用配套的 `--brand-deep` / `--accent-deep` / `--pop-deep` 或 `--ink` 系列。完整对比度矩阵见 `brand-dna.md`。

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

蓝紫渐变当主色 · 通用 glassmorphism · neon · bounce/elastic 动效 · Inter/Roboto 等 AI 默认字体 · 所有 section 居中 · HTML 默认样式 · 纯黑纯白 · 灰色竖线式引用 · 看起来像 AI 生成的通用模板

> 禁忌都有例外边界（比如固定导航条的 `backdrop-filter`、代码高亮里的紫色是被点名放行的）。完整的三列禁忌表（禁什么 / 为什么 / 例外）在 `brand-dna.md`。

---

## 质量检查

**P0(必须全过)**

品牌三色比例 · 无禁忌元素 · 无 HTML 默认样式 · 暖底背景 · 衬线+无衬线混搭 · 正文对比度 ≥ 4.5:1 · 键盘焦点环可见 · `prefers-reduced-motion` 且减弱后内容仍可见 · 响应式（卡片场景除外）· 每 section 布局不同 · clamp() fluid sizing · 截图发社交媒体不会被说"又是 AI 做的"

**P1(应过)**

至少一个视觉惊喜 section · 字号对比极端 · Scroll Reveal 动效 · 大装饰数字/英文 · 无纯黑纯白

**P2(加分)**

图片溢出容器 · 深色面板打破节奏 · 装饰元素克制 · 直接写 token 而非 hex

其中大部分可以机器检查：

```bash
python scripts/build_tokens.py --check      # token 是否与 tokens.json 同步
python scripts/split_components.py --check  # 组件分片是否与源同步
python scripts/lint_design.py               # 8 类规则，P0 必须为 0
```

判定规则、每条对应的 linter 规则号、以及 `--ds-contrast-ok` 逃生舱的用法见 `references/checklist.md`。

---

## 怎么用

1. Fork 或克隆本仓库
2. 放入你的头像 `assets/avatar.jpg`
3. （可选）换成你自己的品牌色：**只改 `tokens.json`**，然后跑 `python scripts/build_tokens.py`。脚本会把所有 HTML 的 `:root` 变量块、`brand-dna.md` 的对比度矩阵一起重写，并按 `color_migration` 表把文档里遗留的旧色值一并迁移。不要手工去每个文件里搜索替换 —— 那是这套系统改造前的做法，容易漏。
   - 公众号模板（`template-wechat.html`）必须全内联、不能有 CSS 变量，脚本对它只做色值替换，不注入 `:root`。
   - 改完跑 `python scripts/lint_design.py`，配色对比度不过会直接报 P0。
4. 把 `assets/template-cards.html` 中的作者名替换成你自己的
5. 把仓库链接发给你的 AI Agent，跟它说：

> 帮我读这个设计系统，以后做页面按这个规范来。

核心不是这些文件本身，是**你的审美判断力**。文件只是把你的判断写成了 AI 能执行的规则。

---

## Credits

- 方法论灵感来源于 [归藏](https://github.com/guizang) 的 PPT Skill——“限制AI的自由度 = 保证输出质量”这个核心思路参考了他的设计
