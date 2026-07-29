# Scene: 公众号排版（杂志编号风）

> 适用于将 OB 文档排版为公众号文章。产出可直接复制粘贴进微信公众号编辑器的 HTML。

---

## 触发场景

用户说"做公众号排版"、"公众号HTML"、"帮我排版到公众号"、"做分发"、"一鱼多吃"等。

---

## ⚠️ 微信编辑器限制（最重要）

微信公众号编辑器有严格的标签限制：

1. **只能用 `<section>` 标签** — `<div>` 的内联样式会被吃掉，格式丢失
2. **全内联样式** — 不能用 `<style>` 标签、CSS class、外部样式表
3. **不能用** `<figure>`、`<figcaption>`、`<article>`、`<main>` 等语义标签
4. **img 标签极简** — 只有 `src` + `style`，不加多余属性
5. **base64 版必须** — 微信编辑器粘贴时需要图片内嵌，否则无法抓取

---

## 📐 整体规格

| 属性 | 值 |
|------|-----|
| 最大宽度 | 677px |
| 底色 | `#FEF6F5`（奶白） |
| 正文字号 | 18px |
| 行高 | line-height: 2 |
| 正文色 | `#24181E`（墨色） |
| 字体栈 | `-apple-system, 'PingFang SC', 'Helvetica Neue', sans-serif` |
| 标签 | 全部用 `<section>`，禁止 `<div>` |

---

## 🏗️ 页面结构

```
body (background:#f5f5f5)
└── section (max-width:677px; margin:0 auto; background:#FEF6F5; padding:44px 26px 40px)
    ├── 点缀色 kicker
    ├── 大标题（如有）
    ├── 引言金句
    ├── 三色装饰条
    ├── 引言区块（方案C：浅强调色渐变底）
    ├── 章节 ×N（三件套头 + 内容 + 图片）
    ├── 三色分隔条（章节间）
    ├── ...
    ├── 结尾金句
    └── 签名档
```

---

## 🎨 组件样式

### 点缀色 kicker（顶部标签）
```html
<section style="text-align:center; margin-bottom:14px;">
  <span style="font-size:13px; font-weight:bold; letter-spacing:5px; color:#296352;">标签文字</span>
</section>
```

### 大标题（可选，用于长文叙事）
```html
<section style="text-align:center; margin-bottom:40px; padding:50px 0 40px;">
  <p style="margin:0 0 12px; font-family:Georgia,'Songti SC',serif; font-size:32px; font-weight:900; color:#24181E; line-height:1.5;">主标题</p>
  <p style="margin:0 0 24px; font-size:17px; color:#50474B; line-height:1.8;">副标题</p>
</section>
```

### 引言金句（居中衬线）
```html
<section style="text-align:center; margin-bottom:10px;">
  <p style="margin:0; font-family:Georgia,'Songti SC',serif; font-size:21px; font-weight:900; line-height:1.9;">金句文字<br>第二行<span style="color:#7E4047;">主色关键词</span>。</p>
</section>
```

### 三色装饰条
```html
<section style="text-align:center; margin-bottom:36px;">
  <span style="display:inline-block; width:36px; height:4px; background:#A15C63; border-radius:2px;"></span>
  <span style="display:inline-block; width:18px; height:4px; background:#EED0A3; border-radius:2px; margin-left:5px;"></span>
  <span style="display:inline-block; width:8px; height:4px; background:#458270; border-radius:2px; margin-left:5px;"></span>
</section>
```

### 引言区块（方案C：浅强调色渐变底）
```html
<section style="margin-bottom:28px; padding:24px 22px; background:#FFEED5; border-radius:16px;">
  <p style="margin:0 0 14px; font-size:16px; line-height:2; color:#24181E;">引言正文</p>
  <p style="margin:0; font-size:16px; line-height:2; color:#24181E;">第二段</p>
</section>
```

### 章节头三件套

教程/步骤类用四件套（含 STEP 标签），叙事类用三件套（装饰词 + 标题 + 强调色短条）：

**叙事类（推荐）：**
```html
<section style="margin-bottom:52px;">
  <!-- 大淡色英文装饰词 -->
  <section style="margin-bottom:6px;">
    <span style="font-family:Georgia,'Songti SC',serif; font-style:italic; font-size:68px; font-weight:bold; color:rgba(161,92,99,0.14); line-height:1;">EnglishWord</span>
  </section>
  <!-- 衬线标题 -->
  <section style="margin-bottom:10px;">
    <span style="font-family:Georgia,'Songti SC',serif; font-size:27px; font-weight:900;">中文章节标题</span>
  </section>
  <!-- 强调色短条 -->
  <section style="margin-bottom:22px;">
    <span style="display:inline-block; width:56px; height:6px; background:#EED0A3; border-radius:3px;"></span>
  </section>
  <!-- 正文内容 -->
  <p style="margin:0 0 18px; font-size:18px; line-height:2; color:#24181E;">段落文字</p>
</section>
```

**教程/步骤类（四件套）：**
```html
<section style="margin-bottom:52px;">
  <section style="margin-bottom:6px;">
    <span style="font-family:Georgia,'Songti SC',serif; font-style:italic; font-size:68px; font-weight:bold; color:rgba(161,92,99,0.14); line-height:1;">01</span>
  </section>
  <section style="margin-bottom:4px;">
    <span style="font-size:13px; font-weight:bold; letter-spacing:4px; color:#7E4047;">STEP 1</span>
  </section>
  <section style="margin-bottom:10px;">
    <span style="font-family:Georgia,'Songti SC',serif; font-size:27px; font-weight:900;">标题</span>
  </section>
  <section style="margin-bottom:22px;">
    <span style="display:inline-block; width:56px; height:6px; background:#EED0A3; border-radius:3px;"></span>
  </section>
  <!-- 内容 -->
</section>
```

### 图片
```html
<img src="图片路径或base64" style="width:100%; border-radius:14px; margin-bottom:20px;">
```

### 图片占位（模板中使用）
```html
<section style="width:100%; height:200px; border-radius:14px; margin-bottom:20px; background:#FFEED5; display:flex; align-items:center; justify-content:center; position:relative; overflow:hidden;">
  <span style="font-family:Georgia,serif; font-size:120px; font-weight:bold; color:rgba(238,208,163,0.3); position:absolute; top:50%; left:50%; transform:translate(-50%,-50%);">IMG</span>
  <span style="font-size:13px; color:#71686C; position:relative; z-index:1;">配图位置</span>
</section>
```

### 图注（可选）
```html
<section style="text-align:center; margin-bottom:20px;">
  <span style="font-size:13px; color:#71686C;">△ 图片说明文字</span>
</section>
```

### 荧光笔高亮（加粗文字）
```html
<span style="background:linear-gradient(transparent 60%, #EED0A3 60%); font-weight:bold; padding:0 2px;">高亮文字</span>
```
每节 1-3 处，不贪多。对应源文档中 `**加粗**` 的文字。

### 三色分隔条（章节之间）
```html
<section style="text-align:center; margin-bottom:56px;">
  <span style="display:inline-block; width:36px; height:4px; background:#A15C63; border-radius:2px;"></span>
  <span style="display:inline-block; width:18px; height:4px; background:#EED0A3; border-radius:2px; margin-left:5px;"></span>
  <span style="display:inline-block; width:8px; height:4px; background:#458270; border-radius:2px; margin-left:5px;"></span>
</section>
```

### 结尾金句
```html
<section style="text-align:center; margin:48px 0 36px;">
  <span style="font-family:Georgia,'Songti SC',serif; font-style:italic; font-size:56px; color:rgba(161,92,99,0.18); line-height:1;">"</span>
  <p style="margin:8px 0 6px; font-family:Georgia,'Songti SC',serif; font-size:21px; font-weight:900; line-height:1.8;">核心金句文字</p>
  <p style="margin:0 0 16px; font-size:14px; color:#71686C;">副句 / 补充</p>
  <section style="text-align:center;">
    <span style="display:inline-block; width:36px; height:4px; background:#A15C63; border-radius:2px;"></span>
    <span style="display:inline-block; width:18px; height:4px; background:#EED0A3; border-radius:2px; margin-left:5px;"></span>
    <span style="display:inline-block; width:8px; height:4px; background:#458270; border-radius:2px; margin-left:5px;"></span>
  </section>
</section>
```

### 签名档

```html
<section style="text-align:center; padding:20px 0 0;">
  <p style="margin:0 0 4px; font-size:15px; font-weight:bold; color:#24181E;">脆皮</p>
  <p style="margin:0; font-size:13px; color:#71686C; line-height:1.8;">▪️在AI时代认真生活的女生｜INTJ<br>▪️跟Agent搭档的第1年</p>
</section>
```

---

## 📝 排版原则

### 内容处理
- **文字 100% 使用原文**，不改写、不精简、不添加
- `**加粗**` → 荧光笔高亮 span
- `![[filename]]` → 对应图片的 img 标签
- `## 标题` → 章节头三件套
- `### 小标题` → 加粗 18px 段落
- `---` → 三色分隔条
- `> 引用` → 引言区块（方案C 浅强调色渐变底）
- 普通段落 → `<p>` 标签

### 叙事长文的章节装饰词
为每个 `## 标题` 匹配一个英文装饰词（Georgia italic 68px 淡色），例如：
- 剧本 → Script
- 米兰 → Milan
- 最后 → Finale

装饰词要短（1-2个英文单词），跟章节主题相关。

---

## 🖼️ 图片处理（base64 版）

必须产出 base64 版（文件名加 `-base64` 后缀），用 Python PIL：

```python
from PIL import Image
import base64, io

def img_to_base64(path, max_width=1080, quality=72):
    img = Image.open(path)
    if img.width > max_width:
        ratio = max_width / img.width
        img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)
    buffer = io.BytesIO()
    img.convert('RGB').save(buffer, format='JPEG', quality=quality)
    return base64.b64encode(buffer.getvalue()).decode()
```

- 宽度缩到 1080px
- JPEG quality=72（控制体积）
- PNG 也转 JPEG
- 目标整体文件 < 5MB

---

## ✅ Checklist

- [ ] 全部用 `<section>` 标签，0 个 `<div>`
- [ ] 全内联样式，无 `<style>` 标签
- [ ] 底色 `#FEF6F5`，max-width 677px
- [ ] 正文 18px，line-height:2
- [ ] 章节头三件套完整（装饰词 + 标题 + 强调色短条）
- [ ] 加粗文字 → 荧光笔高亮
- [ ] 图片 width:100%; border-radius:14px
- [ ] 三色分隔条在章节之间
- [ ] 有结尾金句 + 签名档
- [ ] base64 版已生成，图片内嵌可粘贴
- [ ] 文字 100% 原文未改写

---

## 📎 参考定稿

- 本仓库 `assets/demo-wechat.html`（完整 Demo，含所有组件示例）
- 本仓库 `assets/template-wechat.html`（可直接修改的模板骨架）

---

## 🎨 10 套配色的十六进制对照表

微信编辑器会剥掉 `:root` 和 CSS 变量，所以公众号模板只能用内联的字面色值。
上面所有片段用的是默认 **茶玫 `rose`**。
换配色的做法是**机械搜索替换**：把茶玫那一列的色值换成目标配色同一行的色值。
`palettes.html` 支持一键复制某一套配色的全部色值，可以直接对照。

**色彩层（7 套）**

| 令牌 | 茶玫<br>`rose` | 胭脂<br>`wine` | 樱<br>`sakura` | 藕荷<br>`wisteria` | 雾霞<br>`bluebell` | 青瓷<br>`celadon` | 艾绿<br>`sage` |
|---|---|---|---|---|---|---|---|
| `--p-primary` | `#A15C63` | `#812A51` | `#B25588` | `#815C93` | `#5C6A9F` | `#2E807F` | `#587255` |
| `--p-primary-deep` | `#7E4047` | `#5D0E35` | `#8D3969` | `#614071` | `#404C7C` | `#195F5F` | `#3C543A` |
| `--p-primary-soft` | `#FEE6E7` | `#FCE6ED` | `#FBE6F0` | `#F3E8F9` | `#E6ECFF` | `#DAF3F2` | `#E3F2E2` |
| `--p-accent` | `#EED0A3` | `#F4C5AF` | `#EDDD7E` | `#A6E4E3` | `#D5DFB1` | `#F9BAC4` | `#EDD080` |
| `--p-accent-soft` | `#FFEED5` | `#FFECE3` | `#F7F2D2` | `#D1FAFA` | `#EDF5D5` | `#FFEBED` | `#FBF0D1` |
| `--p-accent-ink` | `#85601D` | `#955637` | `#73671D` | `#217273` | `#616D26` | `#97515F` | `#7C641C` |
| `--p-pop` | `#458270` | `#377395` | `#54824F` | `#BA5E54` | `#B6556A` | `#A25F32` | `#A25483` |
| `--p-pop-deep` | `#296352` | `#1A5473` | `#386334` | `#954239` | `#91384E` | `#7F4216` | `#7F3863` |
| `--p-cream` | `#FEF6F5` | `#FEF6F5` | `#FEF6F5` | `#FEF7F1` | `#FCF8EF` | `#FCF8EF` | `#FDF8EF` |
| `--p-cream-dark` | `#F8ECEA` | `#F8ECEA` | `#F8ECEA` | `#F9EDE4` | `#F6EEE0` | `#F5EFE0` | `#F7EEE1` |
| `--p-card` | `#FFFEFE` | `#FFFEFE` | `#FFFEFE` | `#FFFEFE` | `#FFFEFD` | `#FFFEFD` | `#FFFEFE` |
| `--p-ink` | `#24181E` | `#25181E` | `#25181F` | `#1E1A25` | `#1A1C26` | `#131E1E` | `#181E19` |
| `--p-ink-light` | `#50474B` | `#51464B` | `#52464C` | `#4C4851` | `#484953` | `#434B4B` | `#464B47` |
| `--p-ink-faint` | `#71686C` | `#72676C` | `#73676D` | `#6D6972` | `#696A74` | `#646C6C` | `#676C68` |
| `--p-dark-panel` | `#1D1318` | `#1D1318` | `#1D1318` | `#18151D` | `#15161E` | `#0F1818` | `#121813` |
| `--p-dark-panel-2` | `#33292E` | `#34292E` | `#34292F` | `#2E2B34` | `#2B2C36` | `#252F2E` | `#292E29` |

**中性层（3 套）**

| 令牌 | 奶咖<br>`latte` | 烟灰玫<br>`greige` | 雪青<br>`heather` |
|---|---|---|---|
| `--p-primary` | `#7D5D45` | `#7C6B75` | `#635B7B` |
| `--p-primary-deep` | `#5D412B` | `#5D4E57` | `#463F5B` |
| `--p-primary-soft` | `#FBE9DC` | `#FAE6F2` | `#EEEAFD` |
| `--p-accent` | `#BBE5C4` | `#DDD2F1` | `#F9D0C7` |
| `--p-accent-soft` | `#DDF9E3` | `#F3EDFF` | `#FFECE7` |
| `--p-accent-ink` | `#357449` | `#735B97` | `#995346` |
| `--p-pop` | `#287A83` | `#4B5D8E` | `#8E5C9D` |
| `--p-pop-deep` | `#175A61` | `#30406C` | `#6D407B` |
| `--p-cream` | `#FEF7F0` | `#FEF7F4` | `#FEF7F1` |
| `--p-cream-dark` | `#F9EDE2` | `#F8ECE8` | `#F9EDE3` |
| `--p-card` | `#FFFEFE` | `#FFFEFE` | `#FFFEFE` |
| `--p-ink` | `#211B17` | `#211A1E` | `#1D1B22` |
| `--p-ink-light` | `#4D4845` | `#4E484C` | `#4A494E` |
| `--p-ink-faint` | `#6E6A66` | `#6E696C` | `#6B6A70` |
| `--p-dark-panel` | `#1A1512` | `#1A1519` | `#17151B` |
| `--p-dark-panel-2` | `#302C27` | `#302B2E` | `#2D2C32` |

> 这张表由 `palette_spec.py` 生成，和 `assets/palettes.css`、`assets/template-wechat.html`
> 出自同一份数据，不会各自漂移。

> 换色顺序建议：先换 `--p-ink` / `--p-cream` / `--p-cream-dark`（纸面与文字），
> 再换 `--p-primary` 系，最后换 `--p-accent` / `--p-pop`。
> 这样中途预览不会出现文字和底色撞色的中间态。

### 这些色值在公众号纸面上的实测对比度

微信文章的纸面就是 `--p-cream`，所以正文那几个令牌是按纸面解出来的，不是照搬网页的门槛：

| 文字 | 落在 | 门槛 | 10 套区间 |
|---|---|---|---|
| 正文 / 大标题　`--p-ink` | `--p-cream` | ≥ 12.0 | 16.00–16.10　✅ |
| 副标题　`--p-ink-light` | `--p-cream` | ≥ 7.0 | 8.41–8.49　✅ |
| 签名 · 图注小字　`--p-ink-faint` | `--p-cream` | ≥ 4.5 | 5.05–5.09　✅ |
| 关键词 · STEP 标签　`--p-primary-deep` | `--p-cream` | ≥ 4.5 | 6.75–12.48　✅ |
| kicker 标签　`--p-pop-deep` | `--p-cream` | ≥ 4.5 | 6.35–9.55　✅ |
| 浅强调底引言块上的字　`--p-accent-ink` | `--p-accent-soft` | ≥ 4.5 | 5.00–5.05　✅ |
| 荧光笔高亮上的字　`--p-ink` | `--p-accent` | ≥ 7.0 | 10.43–12.40　✅ |

> 荧光笔那一行是关键：实心强调色上放深色强调字永远过不了 AA，
> 所以高亮文字用 `--p-ink`，不是 `--p-accent-ink`。`--p-accent-ink` 只用在 `--p-accent-soft` 浅底上。
