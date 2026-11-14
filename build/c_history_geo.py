# -*- coding: utf-8 -*-
from lib import *
import lib
def profile():
    pts = [(0,0),(60,0),(80,-20),(230,-60),(260,-120),(330,-260),(380,-330),(440,-560),(500,-700),(560,-760),(610,-720),(660,-520),(700,-280),(730,40),(760,90),(840,90),(860,40),(900,-300),(950,-640),(1000,-820),(1080,-860),(1160,-880)]
    base = 300; k = .22
    d = "M" + " ".join(f"{x},{base - y*k:.0f}" for x, y in [(p[0], -p[1]) for p in pts])
    d2 = d + " L1160,420 L0,420 Z"
    zones = [(30,"地中海","#5aa9ff"),(150,"沿海平原","#3ccf8e"),(300,"示非拉（低丘）","#f2c14e"),(520,"中央山地（犹大山地）","#ff9f43"),(790,"约旦河谷 · 死海","#2ed3c6"),(1060,"外约旦高原（摩押）","#a98bff")]
    o = ['<svg viewBox="0 0 1160 430" role="img" aria-label="迦南东西向地形剖面示意">',
         '<defs><linearGradient id="pf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c9a46a"/><stop offset="1" stop-color="#6b4f2a"/></linearGradient></defs>',
         '<rect x="0" y="300" width="70" height="120" fill="#5aa9ff" opacity=".45"/>',
         f'<path d="{d2}" fill="url(#pf)" opacity=".9"/><path d="{d}" fill="none" stroke="#f2c14e" stroke-width="3"/>',
         '<line x1="0" y1="300" x2="1160" y2="300" stroke="#8c97b2" stroke-dasharray="6 6"/><text x="1150" y="294" text-anchor="end" font-size="13" class="tx">海平面 0 m</text>',
         '<rect x="740" y="318" width="110" height="10" fill="#2ed3c6" opacity=".8"/><text x="795" y="350" text-anchor="middle" font-size="14" font-weight="800">死海 约 −430 m（地表最低）</text>',
         '<circle cx="560" cy="133" r="7" fill="#ff6b5b"/><text x="560" y="118" text-anchor="middle" font-size="15" font-weight="800">耶路撒冷 约 750 m</text>',
         '<circle cx="1000" cy="120" r="7" fill="#a98bff"/><text x="1000" y="105" text-anchor="middle" font-size="15" font-weight="800">尼波山 约 800 m</text>']
    for x, t, c in zones:
        o.append(f'<text x="{x}" y="30" text-anchor="middle" font-size="15" font-weight="800" fill="{c}">{t}</text><line x1="{x}" y1="38" x2="{x}" y2="70" stroke="{c}" stroke-width="2"/>')
    o.append('<text x="580" y="415" text-anchor="middle" font-size="12" class="tx">西 ← 约 110 km（示意剖面，垂直比例夸大）→ 东</text></svg>')
    return '<div class="profile reveal"><div class="in">' + "".join(o) + '</div></div>'

def belts():
    # animated west-to-east five belts (schematic, not a map projection)
    cols = [("#5aa9ff","海","地中海"),("#3ccf8e","1 沿海平原","Via Maris · 非利士五城"),
            ("#f2c14e","2 示非拉","谷口战场 · 拉吉、以拉"),("#ff9f43","3 中央山地","耶路撒冷 · 示剑 · 示罗"),
            ("#2ed3c6","4 裂谷","耶利哥 · 盐海 −430m"),("#a98bff","5 外约旦","君王大道 · 摩押亚扪")]
    w, h = 1100, 280
    bw = 150
    o = [f'<div class="zones-film reveal inview"><svg viewBox="0 0 {w} {h}" role="img" aria-label="五条纵带从西到东的示意动画">']
    o.append('<text x="550" y="28" text-anchor="middle" font-size="16" font-weight="800" fill="currentColor">西 ← 五条纵带（示意，非精确宽度）→ 东</text>')
    for i,(c,t,s) in enumerate(cols):
        x = 40 + i*bw + (20 if i else 0)
        delay = i*0.12
        o.append(f'<g class="belt" style="animation-delay:{delay:.2f}s">')
        o.append(f'<rect x="{x}" y="50" width="130" height="190" rx="16" fill="{c}" fill-opacity=".28" stroke="{c}" stroke-width="2"/>')
        o.append(f'<text x="{x+65}" y="100" text-anchor="middle" font-size="15" font-weight="800" fill="{c}">{t}</text>')
        # wrap note
        o.append(f'<text x="{x+65}" y="145" text-anchor="middle" font-size="13" fill="currentColor">{s[:8]}</text>')
        o.append(f'<text x="{x+65}" y="168" text-anchor="middle" font-size="13" fill="currentColor">{s[8:]}</text>')
        o.append('</g>')
        if i < len(cols)-1:
            o.append(f'<text x="{x+140}" y="155" font-size="20" fill="#8c97b2">→</text>')
    o.append('</svg><p class="map-note">颜色与下一幅真实地图、剖面图一致，便于记忆：绿—橙—金—青—紫。</p></div>')
    return "".join(o)

def body():
    o = []
    o.append('''<section class="hero reveal"><div class="kick">GEOGRAPHY · LAND BRIDGE · FIVE BELTS</div>
<h1>⛰️ 地理：五条纵带与两条大道</h1>
<p class="lead"><b class="th">先记住剖面，再记住道路，然后放大心脏。</b>西低东裂、中间高耸：百姓住在「中央山地」，国际大道却从旁边擦过——神把见证的灯台放在列国能看见、却不在商路正中的地方。</p></section>''')
    o.append(hist_nav("history-geo"))
    o.append(H2("belts", "🗺️", "五条纵带：从海到高原", "var(--green)"))
    o.append(H3("belts-anim", "🎬", "从西到东的记忆动画"))
    o.append(belts())
    o.append(H3("belts-profile", "📐", "东西向地形剖面"))
    o.append(profile())
    o.append(H3("belts-table", "📋", "五带与历史书事件"))
    o.append(table(["地带", "特点", "历史书中的事件"], [
        ["🌊 沿海平原", "肥沃、平坦，国际大道（Via Maris）经过；非利士五城所在", "参孙、约柜在亚实突、非利士人的铁器优势（撒上13:19-22）"],
        ["⛰️ 示非拉（低丘）", "犹大山地与沿海之间的缓冲带，「兵家必争」", "以拉谷（大卫与歌利亚）、拉吉（亚述围城）、伯示麦"],
        ["🏔️ 中央山地", "以色列的「心脏」：耶路撒冷、伯利恒、希伯仑、伯特利、示罗、示剑、撒玛利亚", "大部分历史书的主舞台；易守难攻"],
        ["🏞️ 约旦河谷", "大裂谷：加利利海（约 −210m）到死海（约 −430m）", "过约旦河（书3）、耶利哥、以利亚升天（王下2）"],
        ["🐑 外约旦高原", "基列、摩押、亚扪、以东；「君王大道」（民20:17）南北贯通", "耶弗他、路得的故乡摩押、米沙碑"]]))
    o.append(H3("belts-map", "🗺️", "五带真实地图（概念图 + 离线地形 + 实时瓦片）"))
    o.append(lib.MAP("zones"))
    o.append(H2("roads", "🛤️", "陆桥与两条国际大道", "var(--orange)"))
    o.append(H3("roads-why", "❓", "为什么这块地决定历史"))
    o.append(BG('<p>西有大海，东有沙漠，南接埃及，北通两河流域。谁控制这条走廊，谁就控制古代世界的贸易与战争。沿海大道走平原，君王大道走外约旦；<b class="k">耶路撒冷偏在中央山地，不在两条干道上</b>。</p>'))
    o.append(H3("roads-map", "🗺️", "陆桥地图"))
    o.append(lib.MAP("landbridge"))
    o.append(H2("heart", "❤️", "犹大山地的心脏", "var(--gold)"))
    o.append(H3("heart-map", "🗺️", "圣殿、京城与四周关隘"))
    o.append(lib.MAP("heartland"))
    o.append(H2("climate", "🌧️", "气候与信仰", "var(--purple)"))
    o.append(H3("climate-rain", "☁️", "靠天上的雨水，不靠尼罗河"))
    o.append(BG('<p>迦南不像埃及靠尼罗河灌溉，而是「<b class="k">靠天上的雨水滋润</b>」（申11:10-12）。秋雨（十月）与春雨（三四月）决定一年收成，所以迦南人崇拜风暴与雨水之神<span class="pn">巴力</span>。以利亚宣告「这几年我若不祷告，必不降露、不下雨」（王上17:1），正是<b class="k">当面挑战巴力的「专业领域」</b>；迦密山上降下的不是雨而是火，然后才是大雨（王上18）。</p>'))
    o.append(H3("climate-mem", "🧠", "记忆钩"))
    o.append(mnem("海 — 平 — 丘 — 山 — 谷 — 原", "西向东：地中海 · 沿海平原 · 示非拉 · 中央山地 · 裂谷 · 外约旦高原"))
    return "".join(o)
