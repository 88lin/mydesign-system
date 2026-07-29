# Brand DNA — 品牌基因

> ⚠️ **使用前请确认配置：** 本设计系统内置 **10 套配色**，默认启用 **茶玫 `rose`**。
> 换配色只需要改一个属性：`<html data-palette="wine">`，模板里现有的 CSS 一行都不用动。
> 想看实际观感和实测对比度，打开 `palettes.html`——那一页会当场把 10 套 × 18 条门槛算给你看。
> 头像、气质关键词请替换成你自己的。

---

## 🎨 配色系统（10 套可切换）

整套系统是**偏女性化**的：低彩度雾面色、带一点血色的暖白纸、藏着配色色相的李子墨／咖啡墨，
强调色落在香槟金、蜜杏、腮红粉、淡丁香这些接近金属质感的浅色带上。**不是高饱和的粉。**

| 配色 | 主色 60% | 强调 30% | 点缀 10% | 气质 | 英文名 |
|---|---|---|---|---|---|
| **茶玫** `rose` **（默认）** | `#A15C63` | `#EED0A3` | `#458270` | 柔雾玫瑰 × 香槟金 | Rose Tea |
| **胭脂** `wine` | `#812A51` | `#F4C5AF` | `#377395` | 波尔多酒红 × 蜜杏 | Bordeaux Rouge |
| **樱** `sakura` | `#B25588` | `#EDDD7E` | `#54824F` | 樱粉 × 柠黄 | Sakura |
| **藕荷** `wisteria` | `#815C93` | `#A6E4E3` | `#BA5E54` | 紫藤丁香 × 薄荷 | Wisteria |
| **雾霞** `bluebell` | `#5C6A9F` | `#D5DFB1` | `#B6556A` | 雾霭蓝紫 × 芹绿 | Misty Bluebell |
| **青瓷** `celadon` | `#2E807F` | `#F9BAC4` | `#A25F32` | 青瓷湖水 × 腮红粉 | Celadon & Blush |
| **艾绿** `sage` | `#587255` | `#EDD080` | `#A25483` | 草木灰绿 × 蜜黄 | Sage & Honey |
| **奶咖** `latte` | `#7D5D45` | `#BBE5C4` | `#287A83` | 燕麦焦糖 × 抹茶奶绿 | Latte |
| **烟灰玫** `greige` | `#7C6B75` | `#DDD2F1` | `#4B5D8E` | 烟灰藕粉 × 淡丁香 | Smoked Greige |
| **雪青** `heather` | `#635B7B` | `#F9D0C7` | `#8E5C9D` | 灰丁香 × 藕粉 | Heather |

三色比例原则不变：主色 60% · 强调色 30% · 点缀色 10%（点缀色永远是点缀，不做主色）。

### 两层结构：色彩层 7 套 + 中性层 3 套

这不是「10 套随便选」，是两个类别：

- **色彩层（7 套）**——茶玫、胭脂、樱、藕荷、雾霞、青瓷、艾绿。带气质，主色有明确色相，适合页面本身就是主角的场合。
- **中性层（3 套）**——奶咖、烟灰玫、雪青。彩度压到极低（主色 C ≤ 0.055），
  存在感刻意做弱，适合摄影图文、作品集、长文——不想让配色抢走内容的场合。

10 套配色的 `ink / ink-light / ink-faint / cream / cream-dark / dark-panel` **明度台阶是对齐的**，
所以换配色只换气质、不换视觉节奏——同一个页面换到任何一套，字重和层级感觉都一样。派生色
（`-deep / -soft / accent-ink`）在 OKLCH 里按感知明度推导，不是 HSL 机械变暗，所以不会脏、不会偏色。

### 三层令牌结构

色值的唯一事实来源是 `assets/palettes.css`（4 个模板内联同一份副本，因为模板必须单文件可离线打开）。

```css
/* 第 1 层 · 配色定义：10 套 × 16 个色值 */
:root, [data-palette="rose"] { --p-primary: #A15C63; --p-accent: #EED0A3; /* … */ }
[data-palette="wine"]      { --p-primary: #812A51; --p-accent: #F4C5AF; /* … */ }

/* 第 2 层 · 语义令牌：页面只认这一层 */
:root {
  --brand-primary: var(--p-primary);
  --brand-primary-deep: var(--p-primary-deep);
  /* … */
  /* 已弃用的兼容别名。仓库内部一处都不再使用，只为仓库外的旧页面保留： */
  --blue: var(--brand-primary);  --yellow: var(--brand-accent);  --red: var(--brand-pop);
}

/* 第 3 层 · 全局细节：::selection、:focus-visible、prefers-reduced-motion */
```

CSS 自定义属性在**使用处**按元素解析，所以 `<html data-palette="wine">` 让 `--p-primary`
命中胭脂的值，`--brand-primary` 自动跟着变，整棵树继承。**换配色 = 改一个属性值。**

> ⚠️ **不要再写 `--blue` / `--yellow` / `--red`。** 它们仍然能解析，但在茶玫里
> `var(--blue)` 渲染出来是 `#A15C63`（灰玫红），在胭脂里是
> `#812A51`（波尔多红）。变量名说的是蓝色，渲染出来不是蓝色，会误导任何读它的人或 agent。
> 一律写 `--brand-primary` / `--brand-accent` / `--brand-pop`。

### 成文的用色规则（这些是对比度实测得出的，不是口味）

- **正文小字和链接用 `--brand-primary-deep`；`--brand-primary` 只用于大标题和装饰。**
  主色最浅的一套（樱）`--brand-primary` on 暖底只有 4.33 : 1 —— 够大字（≥3.0），
  不够小字（需 4.5）。10 套的区间是 4.33–8.27。
- **实心强调色块上的文字用 `--ink`；`--brand-accent-ink` 只用在 `--brand-accent-soft` 浅底上。**
  饱和的强调色上放同色系深字永远过不了 AA，这是色彩物理决定的，不是调不出来。
- **点缀色当小字用 `--brand-pop-deep`。**`--brand-pop` on 底色是 4.11–6.09，只够大字。
- **实心色块上的白色小字需要 `-deep` 底。** 白字 on 主色 / 主色深 / 点缀 / 深色面板实测：

  | 配色 | `#fff` on primary | on primary-deep | on pop | on dark-panel |
  |---|---|---|---|---|
  | 茶玫 `rose` | 4.97 | 7.74 | 4.49 | 18.13 |
  | 胭脂 `wine` | 8.81 | 13.29 | 5.19 | 18.13 |
  | 樱 `sakura` | 4.62 | 7.19 | 4.48 | 18.13 |
  | 藕荷 `wisteria` | 5.40 | 8.47 | 4.36 | 18.04 |
  | 雾霞 `bluebell` | 5.23 | 8.26 | 4.67 | 18.02 |
  | 青瓷 `celadon` | 4.66 | 7.39 | 4.98 | 18.04 |
  | 艾绿 `sage` | 5.31 | 8.33 | 5.08 | 18.01 |
  | 奶咖 `latte` | 5.96 | 9.31 | 5.00 | 18.10 |
  | 烟灰玫 `greige` | 4.98 | 7.80 | 6.45 | 18.02 |
  | 雪青 `heather` | 6.34 | 9.89 | 5.04 | 18.11 |

  大字门槛 3.0 处处满足；小字门槛 4.5 只有 primary-deep 和 dark-panel 处处满足
  （白字 on primary 最低 4.62）。
- **半透明色块写 `rgba(var(--brand-primary-rgb), .08)`，不要写死 `rgba(161, 92, 99, .08)`** ——
  否则换配色时它不跟着变。`palettes.css` 为 ink / primary / accent / pop 发布了 `--*-rgb` 三元组。
- **辅助小字落在 `--cream-dark` 色带或更深的纸感底板上时，`--ink-faint` 是按色带解出来的**
  （门槛 4.5，实测 4.65–4.69）。
  落在 `#F5F0E8`、`#EFE8D8` 这类**刻意不跟随配色**的纸色上时改用 `--ink-light`。
- **文档片段直接写 `var(--token)`，不要写 `var(--token, #hex)`。** 兜底值会把一个已经退役的
  色值永久钉在文档里；`assets/palettes.css` 一定会被加载，兜底只会骗人。
  唯一例外是公众号（见 `references/scene-wechat.md`）：那个编辑器会剥掉 `:root`，
  自定义属性根本不存在，所以只能写死 hex——那份文档里的 hex 是从同一份 spec 生成的。

### 刻意不跟随配色的颜色

不是漏了，是故意的：**语法高亮色**（约定俗成，像 macOS 红绿灯点一样属于「共识色」）、
**macOS 窗口红绿灯点** `#ff5f56/#ffbd2e/#27c93f`、**纸感底板**（`#F5F0E8` 打字机纸、`#FFFEF8` 笔记纸、
`#EFE8D8` 金句纸）。这些换了会失去所指。语法高亮按容器分亮/暗两套，亮底整体压暗过 AA，色相彩度不变。

### 全部 10 套配色的完整色值

#### 色彩层

**茶玫 — Rose Tea**　`<html data-palette="rose">`　气质：柔雾玫瑰 × 香槟金　适合：日常首选 · 教程 · 图文卡片　**（默认）**

| 令牌 | 色值 | 对比度实测 |
|---|---|---|
| `--p-primary` | `#A15C63` | 4.66 : 1 on 底色（大字门槛 3.0） |
| `--p-primary-deep` | `#7E4047` | 7.27 : 1 on 底色（小字门槛 4.5） |
| `--p-primary-soft` | `#FEE6E7` |  |
| `--p-accent` | `#EED0A3` |  |
| `--p-accent-soft` | `#FFEED5` |  |
| `--p-accent-ink` | `#85601D` | 5.00 : 1 on 浅强调底 |
| `--p-pop` | `#458270` | 4.21 : 1 on 底色（大字门槛 3.0） |
| `--p-pop-deep` | `#296352` | 6.57 : 1 on 底色（小字门槛 4.5） |
| `--p-cream` | `#FEF6F5` |  |
| `--p-cream-dark` | `#F8ECEA` |  |
| `--p-card` | `#FFFEFE` |  |
| `--p-ink` | `#24181E` | 16.10 : 1 on 底色 |
| `--p-ink-light` | `#50474B` | 7.75 : 1 on 色带 |
| `--p-ink-faint` | `#71686C` | 4.66 : 1 on 色带 |
| `--p-dark-panel` | `#1D1318` | 17.02 : 1 浅字 on 面板 |
| `--p-dark-panel-2` | `#33292E` |  |

**胭脂 — Bordeaux Rouge**　`<html data-palette="wine">`　气质：波尔多酒红 × 蜜杏　适合：长文 · 观点 · 深度复盘

| 令牌 | 色值 | 对比度实测 |
|---|---|---|
| `--p-primary` | `#812A51` | 8.27 : 1 on 底色（大字门槛 3.0） |
| `--p-primary-deep` | `#5D0E35` | 12.48 : 1 on 底色（小字门槛 4.5） |
| `--p-primary-soft` | `#FCE6ED` |  |
| `--p-accent` | `#F4C5AF` |  |
| `--p-accent-soft` | `#FFECE3` |  |
| `--p-accent-ink` | `#955637` | 5.01 : 1 on 浅强调底 |
| `--p-pop` | `#377395` | 4.87 : 1 on 底色（大字门槛 3.0） |
| `--p-pop-deep` | `#1A5473` | 7.70 : 1 on 底色（小字门槛 4.5） |
| `--p-cream` | `#FEF6F5` |  |
| `--p-cream-dark` | `#F8ECEA` |  |
| `--p-card` | `#FFFEFE` |  |
| `--p-ink` | `#25181E` | 16.05 : 1 on 底色 |
| `--p-ink-light` | `#51464B` | 7.81 : 1 on 色带 |
| `--p-ink-faint` | `#72676C` | 4.69 : 1 on 色带 |
| `--p-dark-panel` | `#1D1318` | 17.02 : 1 浅字 on 面板 |
| `--p-dark-panel-2` | `#34292E` |  |

**樱 — Sakura**　`<html data-palette="sakura">`　气质：樱粉 × 柠黄　适合：活动页 · 节日 · 高饱和场合

| 令牌 | 色值 | 对比度实测 |
|---|---|---|
| `--p-primary` | `#B25588` | 4.33 : 1 on 底色（大字门槛 3.0） |
| `--p-primary-deep` | `#8D3969` | 6.75 : 1 on 底色（小字门槛 4.5） |
| `--p-primary-soft` | `#FBE6F0` |  |
| `--p-accent` | `#EDDD7E` |  |
| `--p-accent-soft` | `#F7F2D2` |  |
| `--p-accent-ink` | `#73671D` | 5.04 : 1 on 浅强调底 |
| `--p-pop` | `#54824F` | 4.21 : 1 on 底色（大字门槛 3.0） |
| `--p-pop-deep` | `#386334` | 6.57 : 1 on 底色（小字门槛 4.5） |
| `--p-cream` | `#FEF6F5` |  |
| `--p-cream-dark` | `#F8ECEA` |  |
| `--p-card` | `#FFFEFE` |  |
| `--p-ink` | `#25181F` | 16.04 : 1 on 底色 |
| `--p-ink-light` | `#52464C` | 7.77 : 1 on 色带 |
| `--p-ink-faint` | `#73676D` | 4.67 : 1 on 色带 |
| `--p-dark-panel` | `#1D1318` | 17.02 : 1 浅字 on 面板 |
| `--p-dark-panel-2` | `#34292F` |  |

**藕荷 — Wisteria**　`<html data-palette="wisteria">`　气质：紫藤丁香 × 薄荷　适合：个人主页 · 分享会 · 手帐感

| 令牌 | 色值 | 对比度实测 |
|---|---|---|
| `--p-primary` | `#815C93` | 5.09 : 1 on 底色（大字门槛 3.0） |
| `--p-primary-deep` | `#614071` | 7.98 : 1 on 底色（小字门槛 4.5） |
| `--p-primary-soft` | `#F3E8F9` |  |
| `--p-accent` | `#A6E4E3` |  |
| `--p-accent-soft` | `#D1FAFA` |  |
| `--p-accent-ink` | `#217273` | 5.05 : 1 on 浅强调底 |
| `--p-pop` | `#BA5E54` | 4.11 : 1 on 底色（大字门槛 3.0） |
| `--p-pop-deep` | `#954239` | 6.35 : 1 on 底色（小字门槛 4.5） |
| `--p-cream` | `#FEF7F1` |  |
| `--p-cream-dark` | `#F9EDE4` |  |
| `--p-card` | `#FFFEFE` |  |
| `--p-ink` | `#1E1A25` | 16.09 : 1 on 底色 |
| `--p-ink-light` | `#4C4851` | 7.76 : 1 on 色带 |
| `--p-ink-faint` | `#6D6972` | 4.67 : 1 on 色带 |
| `--p-dark-panel` | `#18151D` | 17.00 : 1 浅字 on 面板 |
| `--p-dark-panel-2` | `#2E2B34` |  |

**雾霞 — Misty Bluebell**　`<html data-palette="bluebell">`　气质：雾霭蓝紫 × 芹绿　适合：科普 · 教程 · 需要冷静可信的场合

| 令牌 | 色值 | 对比度实测 |
|---|---|---|
| `--p-primary` | `#5C6A9F` | 4.93 : 1 on 底色（大字门槛 3.0） |
| `--p-primary-deep` | `#404C7C` | 7.79 : 1 on 底色（小字门槛 4.5） |
| `--p-primary-soft` | `#E6ECFF` |  |
| `--p-accent` | `#D5DFB1` |  |
| `--p-accent-soft` | `#EDF5D5` |  |
| `--p-accent-ink` | `#616D26` | 5.00 : 1 on 浅强调底 |
| `--p-pop` | `#B6556A` | 4.41 : 1 on 底色（大字门槛 3.0） |
| `--p-pop-deep` | `#91384E` | 6.88 : 1 on 底色（小字门槛 4.5） |
| `--p-cream` | `#FCF8EF` |  |
| `--p-cream-dark` | `#F6EEE0` |  |
| `--p-card` | `#FFFEFD` |  |
| `--p-ink` | `#1A1C26` | 16.00 : 1 on 底色 |
| `--p-ink-light` | `#484953` | 7.74 : 1 on 色带 |
| `--p-ink-faint` | `#696A74` | 4.66 : 1 on 色带 |
| `--p-dark-panel` | `#15161E` | 17.00 : 1 浅字 on 面板 |
| `--p-dark-panel-2` | `#2B2C36` |  |

**青瓷 — Celadon & Blush**　`<html data-palette="celadon">`　气质：青瓷湖水 × 腮红粉　适合：作品集 · 生活方式 · 清冷感

| 令牌 | 色值 | 对比度实测 |
|---|---|---|
| `--p-primary` | `#2E807F` | 4.39 : 1 on 底色（大字门槛 3.0） |
| `--p-primary-deep` | `#195F5F` | 6.97 : 1 on 底色（小字门槛 4.5） |
| `--p-primary-soft` | `#DAF3F2` |  |
| `--p-accent` | `#F9BAC4` |  |
| `--p-accent-soft` | `#FFEBED` |  |
| `--p-accent-ink` | `#97515F` | 5.02 : 1 on 浅强调底 |
| `--p-pop` | `#A25F32` | 4.70 : 1 on 底色（大字门槛 3.0） |
| `--p-pop-deep` | `#7F4216` | 7.36 : 1 on 底色（小字门槛 4.5） |
| `--p-cream` | `#FCF8EF` |  |
| `--p-cream-dark` | `#F5EFE0` |  |
| `--p-card` | `#FFFEFD` |  |
| `--p-ink` | `#131E1E` | 16.08 : 1 on 底色 |
| `--p-ink-light` | `#434B4B` | 7.80 : 1 on 色带 |
| `--p-ink-faint` | `#646C6C` | 4.69 : 1 on 色带 |
| `--p-dark-panel` | `#0F1818` | 17.02 : 1 浅字 on 面板 |
| `--p-dark-panel-2` | `#252F2E` |  |

**艾绿 — Sage & Honey**　`<html data-palette="sage">`　气质：草木灰绿 × 蜜黄　适合：读书笔记 · 植物 · 慢生活

| 令牌 | 色值 | 对比度实测 |
|---|---|---|
| `--p-primary` | `#587255` | 5.02 : 1 on 底色（大字门槛 3.0） |
| `--p-primary-deep` | `#3C543A` | 7.87 : 1 on 底色（小字门槛 4.5） |
| `--p-primary-soft` | `#E3F2E2` |  |
| `--p-accent` | `#EDD080` |  |
| `--p-accent-soft` | `#FBF0D1` |  |
| `--p-accent-ink` | `#7C641C` | 5.00 : 1 on 浅强调底 |
| `--p-pop` | `#A25483` | 4.80 : 1 on 底色（大字门槛 3.0） |
| `--p-pop-deep` | `#7F3863` | 7.50 : 1 on 底色（小字门槛 4.5） |
| `--p-cream` | `#FDF8EF` |  |
| `--p-cream-dark` | `#F7EEE1` |  |
| `--p-card` | `#FFFEFE` |  |
| `--p-ink` | `#181E19` | 16.03 : 1 on 底色 |
| `--p-ink-light` | `#464B47` | 7.75 : 1 on 色带 |
| `--p-ink-faint` | `#676C68` | 4.66 : 1 on 色带 |
| `--p-dark-panel` | `#121813` | 17.03 : 1 浅字 on 面板 |
| `--p-dark-panel-2` | `#292E29` |  |

#### 中性层

**奶咖 — Latte**　`<html data-palette="latte">`　气质：燕麦焦糖 × 抹茶奶绿　适合：作品集 · 简历 · 极简排版

| 令牌 | 色值 | 对比度实测 |
|---|---|---|
| `--p-primary` | `#7D5D45` | 5.61 : 1 on 底色（大字门槛 3.0） |
| `--p-primary-deep` | `#5D412B` | 8.76 : 1 on 底色（小字门槛 4.5） |
| `--p-primary-soft` | `#FBE9DC` |  |
| `--p-accent` | `#BBE5C4` |  |
| `--p-accent-soft` | `#DDF9E3` |  |
| `--p-accent-ink` | `#357449` | 5.00 : 1 on 浅强调底 |
| `--p-pop` | `#287A83` | 4.71 : 1 on 底色（大字门槛 3.0） |
| `--p-pop-deep` | `#175A61` | 7.40 : 1 on 底色（小字门槛 4.5） |
| `--p-cream` | `#FEF7F0` |  |
| `--p-cream-dark` | `#F9EDE2` |  |
| `--p-card` | `#FFFEFE` |  |
| `--p-ink` | `#211B17` | 16.03 : 1 on 底色 |
| `--p-ink-light` | `#4D4845` | 7.83 : 1 on 色带 |
| `--p-ink-faint` | `#6E6A66` | 4.66 : 1 on 色带 |
| `--p-dark-panel` | `#1A1512` | 17.05 : 1 浅字 on 面板 |
| `--p-dark-panel-2` | `#302C27` |  |

**烟灰玫 — Smoked Greige**　`<html data-palette="greige">`　气质：烟灰藕粉 × 淡丁香　适合：摄影图文 · 不想抢图的场合

| 令牌 | 色值 | 对比度实测 |
|---|---|---|
| `--p-primary` | `#7C6B75` | 4.70 : 1 on 底色（大字门槛 3.0） |
| `--p-primary-deep` | `#5D4E57` | 7.36 : 1 on 底色（小字门槛 4.5） |
| `--p-primary-soft` | `#FAE6F2` |  |
| `--p-accent` | `#DDD2F1` |  |
| `--p-accent-soft` | `#F3EDFF` |  |
| `--p-accent-ink` | `#735B97` | 5.00 : 1 on 浅强调底 |
| `--p-pop` | `#4B5D8E` | 6.09 : 1 on 底色（大字门槛 3.0） |
| `--p-pop-deep` | `#30406C` | 9.55 : 1 on 底色（小字门槛 4.5） |
| `--p-cream` | `#FEF7F4` |  |
| `--p-cream-dark` | `#F8ECE8` |  |
| `--p-card` | `#FFFEFE` |  |
| `--p-ink` | `#211A1E` | 16.10 : 1 on 底色 |
| `--p-ink-light` | `#4E484C` | 7.71 : 1 on 色带 |
| `--p-ink-faint` | `#6E696C` | 4.65 : 1 on 色带 |
| `--p-dark-panel` | `#1A1519` | 17.01 : 1 浅字 on 面板 |
| `--p-dark-panel-2` | `#302B2E` |  |

**雪青 — Heather**　`<html data-palette="heather">`　气质：灰丁香 × 藕粉　适合：长文 · 安静克制的个人主页

| 令牌 | 色值 | 对比度实测 |
|---|---|---|
| `--p-primary` | `#635B7B` | 5.97 : 1 on 底色（大字门槛 3.0） |
| `--p-primary-deep` | `#463F5B` | 9.32 : 1 on 底色（小字门槛 4.5） |
| `--p-primary-soft` | `#EEEAFD` |  |
| `--p-accent` | `#F9D0C7` |  |
| `--p-accent-soft` | `#FFECE7` |  |
| `--p-accent-ink` | `#995346` | 5.00 : 1 on 浅强调底 |
| `--p-pop` | `#8E5C9D` | 4.75 : 1 on 底色（大字门槛 3.0） |
| `--p-pop-deep` | `#6D407B` | 7.41 : 1 on 底色（小字门槛 4.5） |
| `--p-cream` | `#FEF7F1` |  |
| `--p-cream-dark` | `#F9EDE3` |  |
| `--p-card` | `#FFFEFE` |  |
| `--p-ink` | `#1D1B22` | 16.06 : 1 on 底色 |
| `--p-ink-light` | `#4A494E` | 7.75 : 1 on 色带 |
| `--p-ink-faint` | `#6B6A70` | 4.65 : 1 on 色带 |
| `--p-dark-panel` | `#17151B` | 17.07 : 1 浅字 on 面板 |
| `--p-dark-panel-2` | `#2D2C32` |  |

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
| 配色 | 蓝紫渐变、cyan、neon、纯黑白、AI常用的冷灰蓝调、任何多色渐变背景（占位色块用纯色 `var(--brand-accent-soft)` 或 `var(--brand-accent)`，荧光笔高亮的 `var(--highlighter)` 保留）；**写死任何品牌色的 hex 或 RGB 三元组**——一律走令牌，否则换配色时它不跟着走 |
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
