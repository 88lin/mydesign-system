# 第三方依赖

| 文件 | 项目 | 版本 | 协议 | 来源 |
|------|------|------|------|------|
| `html2canvas.min.js` | html2canvas | 1.4.1 | MIT | https://github.com/niklasvh/html2canvas |

## 为什么内联而不是走 CDN

卡片模板（`template-cards.html` / `demo-cards.html`）的核心功能是**双击打开就能导出 PNG**，
交付物经常是离线传给对方的单个 HTML 文件。走 CDN 意味着断网就导不出图，所以这里选择把
198 KB 的 min.js 一起带上。

## 升级方式

1. 从上游 release 下载 `dist/html2canvas.min.js`
2. 覆盖 `assets/html2canvas.min.js`
3. 更新本文件的版本号
4. 打开 `demo-cards.html`，点一次导出确认 PNG 正常

## MIT 协议要求

html2canvas 以 MIT 协议分发，要求保留版权声明。`html2canvas.min.js` 文件头部的
`/*! ... */` 注释块即为其版权声明，**压缩或再打包时不要删掉**。
