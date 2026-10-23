# 📜 旧约历史书深读 · OT-Historical-Books-20261023-v1-GROKstudy

> **主题**：旧约历史书（约书亚记 → 以斯帖记）· 欧陆改革宗正统视角 · 圣经神学 × 圣约神学
> **版本**：v1.0（20261023-v1） · **GROKstudy**

## 🔗 在线访问

| 平台 | 链接 |
|---|---|
| GitHub Pages | https://07-je-grok-love-personal-20260928.github.io/OT-Historical-Books-GROKstudy/ |
| Surge | https://ot-historical-books-20261023-v1-grokstudy.surge.sh |
| Netlify | https://ot-historical-books-20261023-v1-grokstudy.netlify.app |
| Release v1.0 | https://github.com/07-Je-Grok-Love-Personal-20260928/OT-Historical-Books-GROKstudy/releases/tag/v1.0-20261023 |
| 源码仓库 | https://github.com/07-Je-Grok-Love-Personal-20260928/OT-Historical-Books-GROKstudy |

## 📚 内容（14 页）

| 页面 | 内容 |
|---|---|
| 🏠 首页 | 使用说明、十二卷一览、总口诀、千年故事线 |
| 📖 整本圣经 | 圣经神学与圣约神学：创造—堕落—救赎—成全；历史书在救恩历史中的位置 |
| 🗺️ 史地文化 | 年代学（王上6:1、早期出埃及说、Thiele）、地形剖面、列国、古近东文化、考古 |
| ⚔️ 约书亚记 | 征服与分地地图、时间线、立约、指向基督 |
| 🌾 士师 · 路得 | 循环图、士师总表、地图；路得记的救赎主 |
| 👑 撒母耳记 | 撒母耳—扫罗—大卫；大卫之约；扫罗与大卫对比 |
| 🏛️ 列王纪 | 南北两国君王彩色总表、年代图、分裂王国地图 |
| 📜 历代志 | 与撒母耳记—列王纪对照、圣殿与大卫王朝 |
| 🧱 拉 · 尼 · 斯 | 波斯时期年代图、波斯帝国地图、圣殿 · 律法 · 城墙 · 护理 |
| 📚 信条对照 | 十一个主题 × 三项联合信条（逐字引用） |
| ✨ 三大信经 | 使徒、尼西亚、亚他那修信经全文背诵版（遮盖/逐行揭开/字号） |
| ⚖️ 信经对比 | 十二维度对比表、韦恩图、异端对照、时间线、“和子”、为什么需要三个 |
| 🧠 速记自测 | 口诀、16 张翻卡、32 题测验、30 天计划 |
| 🔖 来源 | 来源、核对方法、版本记录 |

每卷书统一结构：一眼看懂 · 为什么写 · 写了什么 · 时间线 · 地图 · 历史文化背景 · 圣约神学 · 指向基督 · 难点 · 信条对照 · 多角度 · 应用 · 测验 · CCI《圣经故事》延伸阅读。

## ✅ 引文核对

- 三项联合信条与三大信经的所有引文都**一字不差**取自 [ccifellowship.org](https://ccifellowship.org)（只省略脚注编号）。
- 构建时：每段引文 `assert` 必须是原文子串（`build/lib.py: cq()`），否则构建失败。
- 发布后：`tools/verify_quotes.py` 解析成品 HTML，逐条比对信条引文、信经片段、信经全文（逐字相等）与和合本经文。
- 在线复核：`tools/verify_live.py` 重新抓取 ccifellowship.org 页面，确认引文逐字出现。
- 威斯敏斯特标准只作转述，不作逐字引用。

## 🛠️ 构建

```bash
cd build && python3 build.py          # 生成 docs/
python3 ../tools/verify_quotes.py     # 引文核对
python3 ../tools/qa.py                # 390/768/1440 响应式与溢出检查
```

纯静态 HTML/CSS/JS，无外部 CDN；地图为 Natural Earth 数据自绘 SVG。

## 📝 更新说明

### v1.0 · 20261023-v1（发布：2026-10-24 00:11:33 (Asia/Taipei, UTC+8)）
- 首次发布：14 页，7 幅真实地图，时间线、故事线、流程图、思维导图、动画。
- 三项联合信条对照与三大信经背诵版、深度对比。
- 口诀、翻卡、测验；目录可收起；玻璃拟态、100% 宽度响应式。
- 390 / 768 / 1440 宽度均无横向溢出（`tools/qa.py`）。

## 🗂️ 版本历史

| 版本 | 日期（台北时间） | 说明 |
|---|---|---|
| v1.0 | 2026-10-23（Release 时间戳：2026-10-24 00:11:33 (Asia/Taipei, UTC+8)） | 首次发布；tag `v1.0-20261023` |
