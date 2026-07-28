# CHANGELOG

版本号跟随 `tokens.json` 的 `meta.version` 与 `SKILL.md` 的 `version` 字段。

## [2.2.0] — 2026-07-28

这一版把「规范写在文档里、靠人记住」改成「规范收在 token 里、由脚本执行、由检查器验证」。

### 设计令牌单一来源

- 新增 `tokens.json` v2.2.0：23 个颜色 token、7 个半透明层、字体栈、流式字号、间距、字体加载白名单、29+8 条旧值迁移表
- 新增 `scripts/build_tokens.py`：把 token 注入 12 个 HTML 的 `:root`（内联，保证双击可开）、生成 `brand-dna.md` 的对比度矩阵与 wash 上限表、迁移文档里的遗留色值。`--check` 用于 CI
- 配色从蓝/黄/红换成莓果玫红 `#A63D6F` / 藤萝紫 `#B59AD4` / 珊瑚红 `#E84A5F`，并按 WCAG 推导 `-ink` / `-deep` 两级文字色阶

### 规范检查器

- 新增 `scripts/lint_design.py`：8 类规则（R1 配色 / R2 字体 / R3 默认样式 / R4 流式响应 / R5 无障碍 / R6 布局多样性 / R7 文档一致性 / R8 导出确定性）
- 按页面类型分别启用规则：`page` / `card` / `gallery` / `wechat`
- 对比度计算会解析 `rgba()` / `#rrggbbaa` / `var()` 并按 CSS 层叠合成实际前后景
- 提供 `--ds-contrast-ok` 逃生舱、`--json` / `--report` / `--baseline` 输出

### 无障碍（这一版真正修掉的 bug）

- `prefers-reduced-motion` 从 P2 加分项提升为 **P0**，并新增校验：Scroll Reveal 的 `opacity:0` 必须在减弱动效时同时恢复 `opacity:1` 与 `transform:none`，否则内容永久不可见
- 修复 `.app-input:focus{outline:none}` 抹掉键盘焦点环的问题（10% alpha 的替代阴影对比度只有 1.1:1，等于没有）
- 统一 9 个不同的 Google Fonts 请求 URL 为 1 个，消除字重合成（synthetic bolding）
- 补齐纯黑/纯白检查的属性范围：`-webkit-text-stroke`、`filter: drop-shadow()`、`border-*` 里藏的 `#000` 现在也会被查出来

### 组件库分片

- `references/components.md`（127 KB / 52 组件）拆成 `references/components/` 下 9 个功能分片 + 13 KB 机器可读索引；原文件保留为指针
- 新增 `scripts/split_components.py`（`--check` 可验证同步）；52 个组件逐字节一致，索引 61 条链接零死链
- AI 取一个组件的上下文成本从 124.5 KB 降到约 26 KB（索引 + 单个分片）
- `SKILL.md` Step 5 改为「先读索引 → 只打开命中的 1~2 个分片 → 复制代码」

### 规范文档

- `brand-dna.md` 重写：新增完整对比度矩阵（自动生成）、三列禁忌表（禁什么 / 为什么 / 例外边界）、深色面板取色警告
- `references/checklist.md` 重写：开篇适用范围表，每条 P0 映射到 linter 规则号
- 消解四处自相矛盾的表述：border-left 引用（禁的是灰竖线，品牌色条放行）、glassmorphism（固定导航条是点名例外）、紫色（禁的是蓝紫渐变当主色，代码高亮放行）、汇文明朝体（降级为可选升级，仓库未附带字体文件）

### 工程化

- 新增 `index.html`：作品集首页 / Demo 总入口
- 新增 `.github/workflows/lint.yml`（三个检查器）与 `pages.yml`（自动部署 Pages）
- 新增 `assets/VENDOR.md`：html2canvas 版本、MIT 协议、升级步骤
- 修正 README 的 8 个失效 Demo 链接（原先指向另一个账号的 Pages，本仓库打不开）、
  旧配色表、旧的「手工搜索替换色值」指引
- `.gitignore` 补上 `__pycache__/`、`*.pyc`、`.venv/`

### 检查结果

| 快照 | P0 | P1 | P2 |
|------|----|----|----|
| 改造前基线 | 280 | 91 | 74 |
| 本版 | **0** | 67 | 52 |

剩余 P1/P2 绝大多数是 demo 页面里的纯白 `#fff` 与裸写 hex —— 属于「应改」不是「必改」，且集中在展示页而非模板，留待后续逐页处理。
