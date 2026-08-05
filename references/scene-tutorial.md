# Scene: 介绍型 / 教程型 / 科普型页面

> 基于 GitHub入门 V5 提炼的设计语言。适用于所有单页HTML科普、教程、功能介绍、概念解释类页面。

---

## 🎨 色板

| 用途 | 变量名 | 色值 | 说明 |
|------|--------|------|------|
| 强调色 | `--highlight` | `var(--highlight)` | 强调、装饰圆圈、连接线、badges |
| 强调柔光 | `--highlight-soft` | `var(--highlight-soft)` | 背景块、气泡底色 |
| 品牌展示色 | `--brand` | `var(--brand)` | 大标题、装饰字、section 编号 |
| 品牌文字色 | `--brand-text` | `var(--brand-text)` | 小字号英文标题、链接、标签 |
| 品牌承载色 | `--brand-surface` | `var(--brand-surface)` | 按钮、带字色块，前景用 `--on-brand` |
| 点缀展示色 | `--pop` | `var(--pop)` | 图形、下划线、装饰 |
| 点缀文字色 | `--pop-text` | `var(--pop-text)` | 小字号标签、强调文字 |
| 奶白底 | `--cream` | `var(--cream)` | 页面主背景 |
| 深奶底 | `--cream-dark` | `var(--cream-dark)` | section 间交替背景 |
| 墨色 | `--ink` | `var(--ink)` | 正文主色（非纯黑） |
| 浅墨 | `--ink-light` | `var(--ink-light)` | 次要正文 |
| 淡墨 | `--ink-faint` | `var(--ink-faint)` | 辅助文字、标签 |

### 色彩原则
- 页面不用纯黑/纯白：背景和文字始终来自当前主题 token，卡片使用 `--card-bg`
- 三种主题色可以跨色相组合；关键是角色和用量稳定，不要求每套都保持蓝/黄/红
- 小字号彩色文字和带字色块必须使用可读语义角色，不能直接拿展示色硬撑

---

## 🔤 字体

| 用途 | 字体 | 备注 |
|------|------|------|
| 英文标题/装饰 | `Fraunces` (Google Fonts) | italic用于副标题、accent文字 |
| 中文标题首选 | `Huiwen Mincho`（汇文明朝体） | 优先使用系统已安装字体；仓库未捆绑字体文件，不要引用不存在的 ttf |
| 中文标题备选 | `Noto Serif SC` (Google Fonts) | 默认 fallback；无汇文明朝体时自动使用 |
| 正文/UI | `Noto Sans SC` + 系统栈 `-apple-system, 'PingFang SC', 'Helvetica Neue', sans-serif` | 无衬线保证可读性 |
| 手写装饰 | `Caveat` (Google Fonts) | 轻松标注、注释性文字 |

### 字号层次（全部用 `clamp()` 做fluid sizing）
- **Hero大标题**: `clamp(2.8rem, 7vw, 5.5rem)` — 极大，有冲击力
- **Section标题**: `clamp(1.6rem, 4vw, 2.6rem)` — 大但不压人
- **卡片标题**: `1.15rem ~ 1.4rem` — 清晰可辨
- **正文**: `16px` (body base)
- **辅助文字**: `0.78rem ~ 0.85rem` — 小但可读
- **大装饰数字**: `clamp(3rem, 8vw, 7rem)` — 超大、低透明度做背景装饰

### 字体原则
- 标题用衬线，正文用无衬线——混搭产生节奏
- 字号对比要极端——大的要很大，小的要真的小
- `letter-spacing`: 英文大写标签加 `0.1em~0.2em` 间距

---

## 📐 布局

### 核心原则
- **左对齐为主**，不要居中病
- **不对称**——grid用 `1fr 1.1fr` 或 `0.45fr 1fr` 这种不等分
- **每个section布局形式不同**——避免单调重复
- **充足留白**——`clamp()` 控制padding，大屏更透气
- **max-width: 1300px** + `margin: 0 auto` 约束内容宽度

### 可选的布局模式（按需组合，每页至少3种）
1. **Hero分栏**: 左文字 + 右大图，grid两栏
2. **Sticky侧栏**: 左边大装饰字sticky，右边内容滚动
3. **时间线交错**: 中轴线+左右交替内容块（适合并列要点）
4. **全宽深色面板**: 突出某个重要内容，打破节奏
5. **Step引导**: 圆形编号+虚线连接+每步说明
6. **卡片网格**: 2~3列等宽卡片（注意：不要出现落单的孤儿卡片）
7. **产品出血型Hero**: 左侧40%紧凑文字（大标题+描述+缩略图），右侧60%大图溢出右边界。图片用 `margin-right: -5vw; border-radius: 24px 0 0 24px`，grid: `grid-template-columns: 0.4fr 0.6fr`
8. **条纹Editorial**: 条纹分割带（repeating-linear-gradient）做section分隔。内部左图右文，图片可加低饱和度滤镜。标题用Fraunces大号italic，正文小号无衬线
9. **横向滚动时间线**: flex横排 + scroll-snap + 固定宽度卡片，适合经历展示、项目历程
10. **全宽品牌色面板**: 背景使用 `--brand-surface` / `--highlight`，前景分别使用 `--on-brand` / `--on-highlight`。一页最多1~2个，用于打破奶白底的节奏
11. **对称双栏（Pain展示）**: `grid-template-columns: 1fr 1fr`，min-height: 100vh。左侧大字标题，右侧列表/解释。适合问题/痛点、before/after对比

### 间距系统
- Section之间: `clamp(80px, 12vh, 160px)`
- 内容块之间: `clamp(40px, 6vw, 100px)`
- 卡片内padding: `clamp(28px, 3vw, 44px)`
- 元素间gap: `clamp(24px, 3vw, 48px)`

---

## 🎭 装饰元素

### 可用的装饰手法
- **虚线圆圈**: `border: 2.5px dashed var(--highlight); border-radius: 50%`，半透明，大尺寸做背景
- **渐变光晕**: `radial-gradient(ellipse, rgba(var(--highlight-rgb), .18), transparent)` 做柔和背景
- **分割线**: `linear-gradient(90deg, transparent, var(--highlight), transparent)` 1px渐隐线
- **高亮标记**: `background: linear-gradient(180deg, transparent 50%, rgba(var(--highlight-rgb), .35) 50%)` 文字底部高亮
- **大透明数字**: 超大字号 + `opacity: 0.12~0.2` 做section装饰
- **SVG简笔画**: 用描边风格的简化示意图，不要写实截图
- **底部色条**: `border-bottom: 4px solid var(--highlight)`（或 `--brand` / `--pop`） 给卡片加标识（禁止使用 border-left 竖线引用块）

### 条纹肌理分割（替代渐隐线做section divider）
```css
.stripe-divider {
  height: 24px;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 3px,
    rgba(var(--pop-rgb), .08) 3px,
    rgba(var(--pop-rgb), .08) 4px
  );
}
```

### 关键词高亮底色块（比底部50%下划线更有冲击力）
```css
.keyword-highlight {
  background: rgba(var(--highlight-rgb), .25);
  padding: 0.1em 0.4em;
  border-radius: 6px;
  display: inline;
  box-decoration-break: clone;
}
```

### 浮动信息pill（在图片/hero区上浮动小标签）
```css
.float-pill {
  position: absolute;
  background: var(--cream);
  padding: 0.5em 1em;
  border-radius: 100px;
  font-size: 0.8rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  display: flex;
  align-items: center;
  gap: 0.5em;
}
```

### 双层装饰框
```css
.decorative-frame {
  position: relative;
  padding: 16px;
  border: 2.5px dashed var(--highlight);
  border-radius: 12px;
}
.decorative-frame::before {
  content: '';
  position: absolute;
  inset: -6px;
  border: 1.5px solid rgba(var(--brand-rgb), .2);
  border-radius: 16px;
}
```

### 全大写字间距标签
```css
.label-caps {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  font-weight: 500;
  color: var(--ink-light);
}
```

### 装饰原则
- 每种装饰最多同时用2-3种，不要堆砌
- 装饰是为了引导视线和制造节奏，不是为了好看
- ✅ 用材质感制造温度（条纹、肌理、多层框）
- ✅ 用出血/溢出制造惊喜（图片超出容器边界）
- ✅ 用极端字号对比制造节奏（超大装饰字 vs 超小标签）
- ✅ 用精准的色彩点缀（高亮底色块只用在1-2个关键词上）

---

## ✨ 动效

### Scroll Reveal
```css
.reveal {
  opacity: 0;
  transform: translateY(32px);
  transition: opacity 0.7s cubic-bezier(0.16, 1, 0.3, 1),
              transform 0.7s cubic-bezier(0.16, 1, 0.3, 1);
}
.reveal.visible { opacity: 1; transform: none; }
```
- 用 `IntersectionObserver`，threshold 0.12
- `unobserve` after triggering（只触发一次）
- 用 `.reveal-d1` ~ `.reveal-d5` 做 stagger（0.1s递增）
- 尊重 `prefers-reduced-motion`
- 选中文本高亮由 `palettes.css` 全局提供：`var(--highlight)` + `var(--on-highlight)`

### 动效原则
- **只用 opacity + transform**，不要animate layout属性
- **只用 expo ease-out** `cubic-bezier(0.16, 1, 0.3, 1)`——自然减速
- **不要 bounce/elastic/弹跳**——过时
- **入场一次就好**——不要滚回去再重新播放

### 明确禁止
- ❌ 不要用 `transform: rotate()` 让元素歪着放——这是廉价的假活泼
- ❌ 不要故意错位/偏移来制造"手工感"
- ❌ 不要蓝底面板上放红色文字

---

## 📱 响应式

### 断点
- **900px**: 两栏→单栏，图片缩小，sticky变static
- **600px**: 字号微缩(15px)，图片进一步缩小

### 原则
- 移动端不是"缩小版桌面"——重新排列而不是挤压
- 时间线/交错布局在移动端自动变成单列堆叠
- 不要在移动端隐藏内容

---

## 📝 内容语气

- 中文为主，英文点缀做装饰/标签
- 口语化、轻松、像跟朋友解释
- 用emoji但克制（每个标题一个就够）
- 类比优先（"就像百度网盘""相当于时光机"）
- 不堆术语，说人话

---

## 🧩 可发散方向

- **合作色**: 内容跟某品牌相关时增加局部 `--partner-accent`，不要改写全局主题；所有带字组合重新验对比度
- **布局组合**: 十一种布局模式自由组合
- **装饰密度**: 轻松内容多装饰，严肃内容减少装饰只保留字体层次
- **IP出现方式**: 不同姿势（叉腰、放大镜、坐椅子等）
- **深色section**: 可用一个 section 使用 `--dark-panel` + `--on-dark`，制造节奏对比
- **交互**: 如果内容适合，可加hover状态、tab切换、accordion——但不要为交互而交互

---

## 🎯 设计哲学："为什么好看"的底层逻辑

- **精致的不对称** + **物理材质感** + **极端字号对比**
- 不是"歪/rotate/错位"——是布局结构本身就有张力
- 图片应该"活在空间里"而不是"被框住"——至少一处溢出容器
- 色彩克制但精准——高亮只用在最关键的1-2处
