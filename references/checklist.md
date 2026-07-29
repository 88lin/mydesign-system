# 质量检查清单

> 做完设计后逐条对照。P0必须全过，否则打回修改。

---

## P0（必须全过）

任何一条不过就要改：

- [ ] 品牌三色使用正确（主色60/强调30/点缀10比例）
- [ ] 没有使用禁忌清单里的任何元素（蓝紫渐变/glassmorphism/bounce动画/neon/居中病）
- [ ] 背景使用品牌暖底（`var(--cream)` / `var(--cream-dark)`，每套配色各自的暖白），非纯黑纯白
- [ ] 字体用了推荐字体池里的（Fraunces/Noto Serif SC/Caveat等）
- [ ] 标题衬线+正文无衬线混搭
- [ ] 有响应式（至少900px断点）
- [ ] 截图发Twitter不会被说"又是AI做的"
- [ ] 每个section布局形式不同
- [ ] clamp()做fluid sizing
- [ ] 没有使用任何HTML默认样式（默认blockquote、默认border-left引用、无样式ul/ol、默认table）——所有组件必须从components.md选用

---

## P1（应过）

尽量满足，提升品质：

- [ ] 至少一个section有视觉惊喜（出血/3D/全宽色块/装饰突破）
- [ ] 字号对比足够极端（大的>3rem，小的<0.85rem）
- [ ] 有Scroll Reveal动效 + stagger延迟
- [ ] 使用了大装饰数字或大透明英文做背景
- [ ] 有品牌色条（border-left）或高亮标记
- [ ] ::selection用强调色高亮

---

## P2（加分）

锦上添花：

- [ ] 图片溢出容器边界
- [ ] 有全宽深色面板打破节奏
- [ ] 装饰元素（虚线圆/渐变光晕/条纹肌理）使用克制
- [ ] prefers-reduced-motion尊重

---

## 🎨 配色与可达性（新增）

**P0 · 必须过**

- [ ] `<html>` 上有 `data-palette`，且页面引了 `assets/palettes.css`（或内联了配色 block）
- [ ] 没有写死的品牌十六进制色 —— 一律走 `var(--brand-*)`；半透明写 `rgba(var(--brand-primary-rgb), α)`
- [ ] **正文小字和链接用 `--brand-primary-deep`，不用 `--brand-primary`**（后者只够大字 3:1）
- [ ] 实心色块上的白色小字，底色是 `-deep` 那一档
- [ ] 实心强调色块上的文字是 `--ink`，不是 `--brand-accent-ink`
- [ ] 辅助小字落在 `--cream-dark` 或更深的纸感底板上时用 `--ink-light`
- [ ] 换到 10 套配色里的任意一套，页面都不出现看不清的文字（`data-palette` 逐个试：rose / wine / sakura / wisteria / bluebell / celadon / sage / latte / greige / heather）

**P1 · 应该过**

- [ ] 没有 `outline: none`；键盘 Tab 一圈能看清焦点在哪（`:focus-visible` 已全局提供）
- [ ] 图片上的白色标签，遮罩在**字形所在的高度**足够暗（不是只在盒底暗）
- [ ] 纯装饰的色块（光标、滑块、轮播点）可以保持亮色 —— 上面没有文字就不受对比度约束
