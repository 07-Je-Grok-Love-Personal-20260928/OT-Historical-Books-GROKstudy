# 📜 旧约历史书深读 · OT-Historical-Books-20261114-v2-GROKstudy

> **主题**：旧约历史书（约书亚记 → 以斯帖记）· 欧陆改革宗正统视角 · 圣经神学 × 圣约神学
> **版本**：v2.0（20261114-v2） · **GROKstudy**

## 🔗 在线访问（v2）

| 平台 | 链接 |
|---|---|
| GitHub Pages | https://07-je-grok-love-personal-20260928.github.io/OT-Historical-Books-GROKstudy/ |
| Surge | https://ot-historical-books-20261114-v2-grokstudy.surge.sh |
| Netlify | https://ot-historical-books-20261114-v2-grokstudy.netlify.app |
| 源码仓库 | https://github.com/07-Je-Grok-Love-Personal-20260928/OT-Historical-Books-GROKstudy |
| Release v2.0 | https://github.com/07-Je-Grok-Love-Personal-20260928/OT-Historical-Books-GROKstudy/releases/tag/v2.0-20261114 |

v1 站点仍可访问（未覆盖）：[Surge v1](https://ot-historical-books-20261023-v1-grokstudy.surge.sh) · [Netlify v1](https://ot-historical-books-20261023-v1-grokstudy.netlify.app) · [Release v1.0](https://github.com/07-Je-Grok-Love-Personal-20260928/OT-Historical-Books-GROKstudy/releases/tag/v1.0-20261023)

## 📚 内容（14 页）

| 页面 | 内容 |
|---|---|
| 🏠 首页 | 使用说明、标记图例、十二卷一览、一千年六幕短片、总口诀、故事线 |
| 📖 整本圣经 | 圣经神学与圣约神学：创造—堕落—救赎—成全 |
| 🗺️ 史地文化 | 年代学、地形剖面、陆桥与两条大道、犹大心脏、帝国与被掳短片、文化圈、列国、考古 |
| ⚔️ 约书亚记 | 征服四幕短片、征服与分地地图（概念图 + 离线地形 + 实时瓦片） |
| 🌾 士师 · 路得 | 循环图、士师总表、地图 |
| 👑 撒母耳记 | 约柜旅程、扫罗与大卫、犹大心脏放大图 |
| 🏛️ 列王纪 | 分裂四幕短片、南北君王总表、分裂王国地图 |
| 📜 历代志 | 与撒母耳记—列王纪对照、圣殿与大卫王朝 |
| 🧱 拉 · 尼 · 斯 | 被掳归回短片、波斯帝国地图 |
| 📚 信条对照 | 十一主题 × 三项联合信条（逐字） |
| ✨ 三大信经 | 使徒、尼西亚、亚他那修信经全文背诵版 |
| ⚖️ 信经对比 | 十二维度、韦恩图、异端、为何需要三份信经 |
| 🧠 速记自测 | 口诀、16 张翻卡、32 题、30 天计划 |
| 🔖 来源 | 来源、核对方法、版本记录 |

每幅地图提供三种视图：**🎨 概念示意图（完全离线）**、**🗺️ Natural Earth 真实地形图（离线）**、**📡 实时多源瓦片**（OpenStreetMap、CARTO 浅色/深色/Voyager、Esri 卫星/地形/街道/自然地貌、OSM HOT、OpenTopoMap；无需密钥；失败或超时自动切换；全部失败则保留离线矢量底图与地点标记）。Leaflet 库自托管，进入视口后才初始化。

## ✅ 引文核对

- 三项联合信条与三大信经的所有引文都**一字不差**取自 [ccifellowship.org](https://ccifellowship.org)（只省略脚注编号）。
- 构建时：每段引文 `assert` 必须是原文子串，否则构建失败。
- 发布后：`tools/verify_quotes.py` 解析成品 HTML（信条引文、信经片段、信经全文、和合本经文）。
- 在线复核：`tools/verify_live.py` 重新抓取 ccifellowship.org。
- 威斯敏斯特标准只作转述，不作逐字引用。

## 🛠️ 构建

```bash
cd build && python3 build.py
python3 ../tools/verify_quotes.py
python3 ../tools/qa.py http://127.0.0.1:8767
```

纯静态 HTML/CSS/JS；Leaflet 与地图库、GeoJSON、地形 SVG 全部自托管，无阻塞 CDN。

## 📝 更新说明

### v2.0 · 20261114-v2
- **地图**：由 7 幅增至 10 幅（新增陆桥与两条大道、犹大山地心脏、古近东文化圈）。每幅地图配概念示意图 + 离线地形图 + 多源实时瓦片（图层切换、自动故障切换、懒加载、瓦片阻断时离线底图可用）。
- **动画**：征服迦南、王国分裂、被掳归回、千年六幕（进—乱—王—分—亡—回）原创 SVG/CSS 短片。
- **性能**：去掉滚动元素上的 `backdrop-filter` 与重阴影；`content-visibility`；GPU 友好的 transform/opacity 动画；尊重 `prefers-reduced-motion`；View Transitions 与页面预取；自托管全部资源。4 秒滚动测试：列王纪页从 22.3 fps（50 个长帧）提升到 60 fps（1 个长帧）；首页 39→60 fps。
- **笔记标记**：重点（金底）、难点（红波浪）、基督（粉实线）、圣约（青虚线）、记忆钩（紫点线）、年代/地名/人物；顶栏可打开图例。
- **QA**：360 / 390 / 430 / 768 / 1024 / 1440 / 1920 共 98 项无横向溢出；目录、标签、测验、翻卡、背诵、地图图层切换均反复点击通过；瓦片请求被阻断时正确回退到离线底图。

### v1.0 · 20261023-v1
- 首次发布：14 页，7 幅真实地图，时间线、故事线、信条与信经、口诀与测验。

## 🗂️ 版本历史

| 版本 | 日期（台北时间） | 说明 |
|---|---|---|
| v2.0 | 2026-11-14 | 地图三视图与多源瓦片、短片动画、标记系统、滚动性能优化。tag `v2.0-20261114` |
| v1.0 | 2026-10-23 | 首次发布。tag `v1.0-20261023` |
