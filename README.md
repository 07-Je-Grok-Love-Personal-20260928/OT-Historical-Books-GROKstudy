# 📜 旧约历史书深读 · OT-Historical-Books-20261114-v3-GROKstudy

> **主题**：旧约历史书（约书亚记 → 以斯帖记）· 欧陆改革宗正统视角 · 圣经神学 × 圣约神学
> **版本**：v3.0（20261114-v3） · **GROKstudy**

## 🔗 在线访问（v3）

| 平台 | 链接 |
|---|---|
| GitHub Pages | https://07-je-grok-love-personal-20260928.github.io/OT-Historical-Books-GROKstudy/ |
| Surge | https://ot-historical-books-20261114-v3-grokstudy.surge.sh |
| Netlify | https://ot-historical-books-20261114-v3-grokstudy.netlify.app |
| 源码仓库 | https://github.com/07-Je-Grok-Love-Personal-20260928/OT-Historical-Books-GROKstudy |
| Release v3.0 | https://github.com/07-Je-Grok-Love-Personal-20260928/OT-Historical-Books-GROKstudy/releases/tag/v3.0-20261114 |

先前版本仍可访问（未覆盖）：

- v2：[Surge](https://ot-historical-books-20261114-v2-grokstudy.surge.sh) · [Netlify](https://ot-historical-books-20261114-v2-grokstudy.netlify.app) · [Release v2.0](https://github.com/07-Je-Grok-Love-Personal-20260928/OT-Historical-Books-GROKstudy/releases/tag/v2.0-20261114)
- v1：[Surge](https://ot-historical-books-20261023-v1-grokstudy.surge.sh) · [Netlify](https://ot-historical-books-20261023-v1-grokstudy.netlify.app) · [Release v1.0](https://github.com/07-Je-Grok-Love-Personal-20260928/OT-Historical-Books-GROKstudy/releases/tag/v1.0-20261023)

## 📚 内容（17 页）

| 页面 | 内容 |
|---|---|
| 🏠 首页 | 使用说明、标记图例、十二卷一览、一千年六幕短片、总口诀、故事线 |
| 📖 整本圣经 | 圣经神学与圣约神学：创造—堕落—救赎—成全 |
| ⏳ 史地总览 | 定年方法、总年表、时间轴（轻量，无实时地图） |
| ⛰️ 地理 | 五带动画与剖面、五带地图、陆桥与两条大道、犹大心脏、气候与巴力 |
| 🌍 帝国列国 | 被掳归回短片、帝国地图、七大势力、宗主更迭 |
| 🎭 文化考古 | 文化圈地图、宗主条约六段、当灭之物、亲属土地、十三件外证 |
| ⚔️ 约书亚记 | 征服四幕短片、征服与分地地图 |
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

**目录**：每页三级目录（1 / 1.1 / 1.1.1），每一级可折叠，状态记在 localStorage；打开后可用右侧手柄左右拖动加宽或收窄（有最小/最大宽度，宽度也会被记住；支持触控与方向键）。手机上目录是可加宽的抽屉。长标题默认单行省略并带 tooltip，加宽后自动换行。滚动时高亮当前节并自动展开其上级。

每幅地图提供三种视图：**🎨 概念示意图（完全离线）**、**🗺️ Natural Earth 真实地形图（离线）**、**📡 实时多源瓦片**（需点击后加载，避免滚动卡顿）。瓦片源包括 OpenStreetMap、OSM 德国/法国、HOT、CyclOSM、CARTO Voyager/浅色/深色、Esri 卫星/地形/街道/自然地貌/晕渲/浅灰/国家地理、OpenTopoMap；无需密钥；失败或超时自动切换；全部失败则保留离线矢量底图。Leaflet 自托管。

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
python3 ../tools/qa.py http://127.0.0.1:8769
```

纯静态 HTML/CSS/JS；Leaflet、GeoJSON、地形 SVG 全部自托管，无阻塞 CDN。

## 📝 更新说明

### v3.0 · 20261114-v3
- **三级目录**：编号 1 / 1.1 / 1.1.1；可折叠并记住状态；可左右拖动加宽（宽度记忆，触控与键盘）；手机为可加宽抽屉；长标题省略或加宽后换行；滚动高亮并自动展开上级。各页标题层级按导读 / 文本 / 地理 / 神学 / 应用重组。
- **滚动性能**：史地拆成四页；实时地图改为点击后加载，滚动中不再初始化 Leaflet；离屏暂停 SVG 动画；更广的 `content-visibility`；去掉静态地形图里无法暂停的动画。4 秒滚动测试（1440×900，`scroll-behavior:auto`）各测量页均 ≥55 fps。
- **地图与可视化**：新增「迦南五条纵带」地图（共 11 幅）与五带动画、宗主条约流程图；再增加若干无密钥瓦片源。
- **笔记标记**：新增「总纲」金条左边线，图例同步更新。
- **QA**：17 页 × 7 宽度共 119 项通过；目录展开/拖动、标签、测验、地图图层与瓦片阻断均反复测试。

### v2.0 · 20261114-v2
- 地图升级为「概念图 + 离线地形图 + 多源实时瓦片」共 10 幅；征服/分裂/被掳/总弧短片；标记系统；滚动性能优化。

### v1.0 · 20261023-v1
- 首次发布：14 页，7 幅真实地图，时间线、故事线、信条与信经、口诀与测验。

## 🗂️ 版本历史

| 版本 | 日期（台北时间） | 说明 |
|---|---|---|
| v3.0 | 2026-11-14 | 三级可拖宽目录、史地分页、点击加载实时地图、更多瓦片与五带图。tag `v3.0-20261114` |
| v2.0 | 2026-11-14 | 地图三视图与多源瓦片、短片动画、标记系统、滚动性能优化。tag `v2.0-20261114` |
| v1.0 | 2026-10-23 | 首次发布。tag `v1.0-20261023` |
