# -*- coding: utf-8 -*-
"""离线概念示意图 + 影视感短动画（纯 SVG/CSS，无版权素材、无网络）。"""
import math, html as HH
import rmap
from rmap import PAL, ink, Placer, tw
def _waves(W, H, n=5):
    o = ['<g class="waves" aria-hidden="true">']
    for i in range(n):
        y = 30 + i * (H - 60) / max(n-1,1)
        d = f"M0,{y:.0f}" + "".join(f" q{W/16:.0f},{8 if j%2==0 else -8} {W/8:.0f},0" for j in range(8))
        o.append(f'<path d="{d}" class="wave" style="--d:{i*.4}s"/>')
    o.append("</g>")
    return "".join(o)
# 各地图的讲解短句与场景装饰
DECOR = {
    "conquest": ("进迦南三步：中部（耶利哥、艾城）→ 南方（基遍、拉吉、希伯仑）→ 北方（夏琐）。", "⚔️"),
    "tribes": ("十二支派分地，六座逃城（河西三、河东三）均匀分布，会幕在示罗。", "🪧"),
    "judges": ("黑暗循环里仍有亮光：底波拉、基甸、路得——神不断兴起拯救者。", "🌀"),
    "samuel": ("约柜从示罗被掳，经非利士地回到耶路撒冷：神的同在不靠人的盒子。", "📜"),
    "divided": ("一分为二：北国十支派立金牛犊，南国留下大卫的灯与圣殿。", "👑"),
    "empires": ("722 北国被掳亚述，586 南国被掳巴比伦，538 起余民归回。", "🏺"),
    "persia": ("“从印度直到古实”的 127 省：书珊宫里，隐藏的神翻转了签。", "👸"),
    "landbridge": ("迦南是陆桥：西有沿海大道（Via Maris），东有君王大道。神把百姓放在列国眼前。", "🌉"),
    "heartland": ("犹大山地是心脏：圣殿在山顶的耶路撒冷，周围是伯利恒、基遍、拉吉、耶利哥。", "🏔️"),
    "culture": ("古近东文化圈：埃及、迦南、腓尼基、亚兰、亚述、巴比伦、波斯——历史书的真实舞台。", "🎭"),
}
def concept(spec, W=1040):
    """活泼的讲解型概念图：真实投影的海岸线剪影 + 动画路线 + 情景装饰。"""
    P, sx, sy, H, land, lakes, riv = rmap.base(spec["bbox"], W, spec.get("fine", False))
    mid = spec["id"]; title = spec["title"]
    fs = 19 if (spec["bbox"][1]-spec["bbox"][0]) > 15 else 21
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{HH.escape(title)}（概念示意图）" class="cmap-svg">',
         f'<defs><linearGradient id="sea-{mid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="var(--geo-sea,#1a3a5c)"/><stop offset="1" stop-color="var(--geo-sea2,#0e2438)"/></linearGradient>',
         f'<linearGradient id="ld-{mid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="var(--geo-land,#e8c98a)"/><stop offset="1" stop-color="var(--geo-land2,#c9a35e)"/></linearGradient>',
         f'<filter id="glow-{mid}"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>']
    cols = sorted({PAL[r[2]] for r in spec.get("routes", ())})
    for c in cols:
        o.append(f'<marker id="ac-{mid}{c[1:]}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="{c}"/></marker>')
    o.append("</defs>")
    o.append(f'<rect width="{W}" height="{H}" rx="18" fill="url(#sea-{mid})"/>')
    o.append(_waves(W, H, 4))
    if land:
        o.append(f'<path d="{land}" class="cland" fill="url(#ld-{mid})" stroke="var(--geo-coast,#8a6a3a)" stroke-width="1.6" stroke-linejoin="round" fill-rule="evenodd"/>')
    if lakes:
        o.append(f'<path d="{lakes}" fill="var(--geo-sea,#1a3a5c)" stroke="#7fb0d4" stroke-width=".8" opacity=".9"/>')
    if riv:
        o.append(f'<path d="{riv}" fill="none" stroke="#5eb0e6" stroke-width="2.2" stroke-linecap="round" opacity=".85"/>')
    # decorative vignette (map-specific), placed in a quiet corner
    o.append(_vignette(mid, W, H, P, spec))
    pl = Placer(W, H)
    for reg in spec.get("regions", ()):
        lab, lon, lat, rx, ry, c = reg; x, y = P(lon, lat)
        o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx*sx:.0f}" ry="{ry*sy:.0f}" fill="{PAL[c]}" fill-opacity=".20" stroke="{PAL[c]}" stroke-opacity=".75" stroke-width="2" stroke-dasharray="7 6"/>')
    for lab, pts, c in spec.get("lines", ()):
        d = "M" + " ".join(f"{P(*p)[0]:.0f},{P(*p)[1]:.0f}" for p in pts)
        o.append(f'<path d="{d}" class="cline" fill="none" stroke="{PAL[c]}" stroke-width="3" stroke-dasharray="10 7" opacity=".85"/>')
    mk = spec["markers"]; pos = rmap.spread(mk, P, 16, 13)
    for m in mk:
        x, y, r = pos[m["k"]]; pl.add((x-r-2, y-r-2, x+r+2, y+r+2))
    nrt = 0
    for a, b, c, *rest in spec.get("routes", ()):
        (x1, y1, r1), (x2, y2, r2) = pos[a], pos[b]
        L = math.hypot(x2-x1, y2-y1) or 1; ux, uy = (x2-x1)/L, (y2-y1)/L
        x1,y1,x2,y2 = x1+ux*(r1+3), y1+uy*(r1+3), x2-ux*(r2+5), y2-uy*(r2+5)
        bend = (rest[0] if rest else .18)*L; mx, my = (x1+x2)/2 + uy*bend, (y1+y2)/2 - ux*bend
        o.append(f'<path d="M{x1:.0f},{y1:.0f} Q{mx:.0f},{my:.0f} {x2:.0f},{y2:.0f}" class="croute" style="stroke:{PAL[c]};--i:{nrt}" marker-end="url(#ac-{mid}{PAL[c][1:]})"/>')
        nrt += 1
    T = []
    for i in sorted(range(len(mk)), key=lambda i: (not mk[i].get("hl"), i)):
        m = mk[i]; x, y, r = pos[m["k"]]
        lab = m["n"]
        res = pl.label(x, y, r, lab, fs)
        if not res: continue
        bx, by, an, far = res
        if far: T.append(f'<path d="M{x:.0f},{y:.0f}L{bx:.0f},{by-6:.0f}" class="cldr"/>')
        T.append(f'<text x="{bx:.0f}" y="{by:.0f}" text-anchor="{an}" class="cml{" hl" if m.get("hl") else ""}">{HH.escape(lab)}</text>')
    for lab, lon, lat, rx, ry, c in spec.get("regions", ()):
        x, y = P(lon, lat); res = pl.label(x, y - ry*sy*.15, 0, lab, fs-2)
        if res: T.append(f'<text x="{res[0]:.0f}" y="{res[1]:.0f}" text-anchor="{res[2]}" class="crg" fill="{PAL[c]}">{HH.escape(lab)}</text>')
    for lab, lon, lat in spec.get("water", ()):
        x, y = P(lon, lat); T.append(f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="middle" class="cwat">{HH.escape(lab)}</text>')
    for lab, pts, c in spec.get("lines", ()):
        x, y = P(*pts[len(pts)//2]); res = pl.label(x, y, 6, lab, fs-3)
        if res: T.append(f'<text x="{res[0]:.0f}" y="{res[1]:.0f}" text-anchor="{res[2]}" class="crg" fill="{PAL[c]}">{HH.escape(lab)}</text>')
    o += T
    for i, m in enumerate(mk):
        x, y, r = pos[m["k"]]; c = PAL[m.get("c","blue")]
        pulse = ' class="cpt hl"' if m.get("hl") else ' class="cpt"'
        o.append(f'<g{pulse} style="--d:{i*.08}s"><circle cx="{x:.0f}" cy="{y:.0f}" r="{r+5 if m.get("hl") else r}" style="fill:{c}" filter="url(#glow-{mid})"/>'
                 f'<text x="{x:.0f}" y="{y+5:.0f}" text-anchor="middle" class="cmn" fill="{ink(c)}">{i+1}</text></g>')
    cap, ic = DECOR.get(mid, (spec.get("rcap",""), "🗺️"))
    o.append(f'<g class="cbanner"><rect x="16" y="14" width="{min(W-32, tw(cap,16)+80):.0f}" height="44" rx="12" fill="rgba(10,16,32,.72)"/>'
             f'<text x="28" y="42" font-size="18" font-weight="800" fill="#ffe7a3">{ic} {HH.escape(title)}</text></g>')
    o.append("</svg>")
    return "".join(o)
def _vignette(mid, W, H, P, spec):
    """地图一角的情景小图（纯几何，不盖住要点）。"""
    # 放在右下或左上的空白装饰，用 CSS 动画
    x, y = W - 130, H - 120
    if mid == "conquest":
        return (f'<g class="vig jericho" transform="translate({x},{y})" aria-hidden="true">'
                f'<rect class="wall w1" x="0" y="20" width="16" height="50" rx="2" fill="#c9a35e"/>'
                f'<rect class="wall w2" x="20" y="10" width="16" height="60" rx="2" fill="#e8c98a"/>'
                f'<rect class="wall w3" x="40" y="18" width="16" height="52" rx="2" fill="#c9a35e"/>'
                f'<rect class="wall w4" x="60" y="8" width="16" height="62" rx="2" fill="#e8c98a"/>'
                f'<text x="38" y="90" text-anchor="middle" font-size="13" fill="#ffe7a3">耶利哥城墙</text></g>')
    if mid == "divided":
        return (f'<g class="vig splitc" transform="translate({x},{y})" aria-hidden="true">'
                f'<circle cx="30" cy="36" r="28" fill="#f2c14e"/><circle cx="86" cy="36" r="28" fill="#a98bff"/>'
                f'<path class="crack" d="M58,8 L50,36 L62,64" fill="none" stroke="#ff6b5b" stroke-width="4" stroke-linecap="round"/>'
                f'<text x="58" y="90" text-anchor="middle" font-size="13" fill="#ffe7a3">一国裂为二</text></g>')
    if mid in ("empires","persia"):
        return (f'<g class="vig caravan" transform="translate({x-20},{y})" aria-hidden="true">'
                f'<ellipse class="camel" cx="20" cy="50" rx="18" ry="10" fill="#d4a574"/>'
                f'<ellipse class="camel" cx="58" cy="48" rx="18" ry="10" fill="#c48a4a"/>'
                f'<path d="M4,50 Q80,20 120,50" class="croute" style="stroke:#f2c14e" fill="none"/>'
                f'<text x="60" y="90" text-anchor="middle" font-size="13" fill="#ffe7a3">被掳与归回之路</text></g>')
    if mid == "samuel":
        return (f'<g class="vig ark" transform="translate({x},{y})" aria-hidden="true">'
                f'<rect class="arkbox" x="18" y="24" width="70" height="36" rx="6" fill="#f2c14e" stroke="#8a6a00" stroke-width="2"/>'
                f'<rect x="30" y="14" width="8" height="16" fill="#e8c98a"/><rect x="68" y="14" width="8" height="16" fill="#e8c98a"/>'
                f'<text x="53" y="90" text-anchor="middle" font-size="13" fill="#ffe7a3">约柜的旅程</text></g>')
    if mid == "judges":
        return (f'<g class="vig cycle" transform="translate({x+10},{y-10})" aria-hidden="true">'
                f'<circle cx="48" cy="40" r="32" fill="none" stroke="#ff9f43" stroke-width="3" stroke-dasharray="8 6" class="spin"/>'
                f'<text x="48" y="36" text-anchor="middle" font-size="12" fill="#ffe7a3">犯罪</text>'
                f'<text x="48" y="52" text-anchor="middle" font-size="12" fill="#ff6b5b">呼求</text>'
                f'<text x="48" y="90" text-anchor="middle" font-size="13" fill="#ffe7a3">士师循环</text></g>')
    if mid == "tribes":
        return (f'<g class="vig" transform="translate({x},{y})" aria-hidden="true">'
                f'<circle cx="24" cy="28" r="12" fill="#ff6b5b"/><circle cx="52" cy="28" r="12" fill="#ff6b5b"/>'
                f'<circle cx="80" cy="28" r="12" fill="#ff6b5b"/><circle cx="24" cy="56" r="12" fill="#ff6b5b"/>'
                f'<circle cx="52" cy="56" r="12" fill="#ff6b5b"/><circle cx="80" cy="56" r="12" fill="#ff6b5b"/>'
                f'<text x="52" y="90" text-anchor="middle" font-size="13" fill="#ffe7a3">六座逃城</text></g>')
    if mid == "landbridge":
        return (f'<g class="vig" transform="translate({x-10},{y})" aria-hidden="true">'
                f'<rect x="0" y="30" width="110" height="18" rx="9" fill="#3ccf8e" opacity=".8"/>'
                f'<rect x="40" y="8" width="18" height="62" rx="9" fill="#f2c14e" opacity=".9"/>'
                f'<text x="55" y="90" text-anchor="middle" font-size="13" fill="#ffe7a3">陆桥 · 两条大道</text></g>')
    if mid == "heartland":
        return (f'<g class="vig temple" transform="translate({x},{y})" aria-hidden="true">'
                f'<path d="M20,60 L52,20 L84,60 Z" fill="#f2c14e"/><rect x="36" y="48" width="32" height="22" fill="#e8c98a"/>'
                f'<text x="52" y="90" text-anchor="middle" font-size="13" fill="#ffe7a3">圣殿在山顶</text></g>')
    if mid == "culture":
        return (f'<g class="vig" transform="translate({x},{y})" aria-hidden="true">'
                f'<circle cx="24" cy="36" r="14" fill="#5aa9ff"/><circle cx="52" cy="36" r="14" fill="#f2c14e"/>'
                f'<circle cx="80" cy="36" r="14" fill="#ff6b5b"/>'
                f'<text x="52" y="90" text-anchor="middle" font-size="13" fill="#ffe7a3">列国文化圈</text></g>')
    return ""
# ---------- 影视感短动画（分镜） ----------
def film(fid, title, scenes, hint=""):
    """scenes: [(emoji, title, body, color), ...] — CSS/JS 驱动的短片式分镜。"""
    dots = "".join(f'<button type="button" class="dot" data-i="{i}" aria-label="第{i+1}幕">{i+1}</button>' for i in range(len(scenes)))
    st = []
    for i, (em, t, b, c) in enumerate(scenes):
        st.append(f'<div class="st{" on" if i==0 else ""}" data-i="{i}" style="--c:{c}"><div class="film-art" aria-hidden="true">{_art(fid,i)}</div>'
                  f'<div class="film-copy"><span class="em">{em}</span><h4>{t}</h4><p>{b}</p></div></div>')
    return (f'<div class="film reveal" id="film-{fid}" data-n="{len(scenes)}" style="--n:{len(scenes)}">'
            f'<div class="sbar"><strong>🎬 {HH.escape(title)}</strong><div class="dots">{dots}</div>'
            f'<button type="button" class="ib" data-a="p" aria-label="上一幕">◀</button>'
            f'<button type="button" class="ib" data-a="n" aria-label="下一幕">▶</button>'
            f'<button type="button" class="ib" data-a="play">▶ 播放短片</button></div>'
            f'<div class="stage">{"".join(st)}</div>'
            f'<p class="film-hint">{hint or "本短片为教学示意，由本站原创 SVG/CSS 动画绘制，不含任何版权影像。"}</p></div>')
def _art(fid, i):
    """每幕一张原创小动画。"""
    arts = {
        ("conquest",0): '<svg viewBox="0 0 200 120"><rect width="200" height="120" rx="12" fill="#1a3a5c"/><path class="river" d="M120,0 C110,40 130,80 100,120" fill="none" stroke="#5eb0e6" stroke-width="14"/><g class="priests"><rect x="108" y="20" width="16" height="22" fill="#f2c14e"/><circle cx="116" cy="14" r="6" fill="#ffe7a3"/></g><text x="16" y="108" fill="#ffe7a3" font-size="13" font-weight="700">约旦河立起成垒</text></svg>',
        ("conquest",1): '<svg viewBox="0 0 200 120"><rect width="200" height="120" rx="12" fill="#3a2a16"/>'+ "".join(f'<rect class="wall w{k}" x="{20+k*28}" y="{18 if k%2 else 28}" width="22" height="{70 if k%2 else 60}" fill="#c9a35e" rx="2"/>' for k in range(5))+'<text x="16" y="108" fill="#ffe7a3" font-size="13" font-weight="700">耶利哥城墙倒塌</text></svg>',
        ("conquest",2): '<svg viewBox="0 0 200 120"><rect width="200" height="120" rx="12" fill="#1e2a20"/><circle class="sun" cx="150" cy="28" r="16" fill="#f2c14e"/><path d="M20,90 L180,90" stroke="#c9a35e" stroke-width="8"/><text x="16" y="70" fill="#ffe7a3" font-size="13" font-weight="700">日头停留 · 南方之战</text></svg>',
        ("conquest",3): '<svg viewBox="0 0 200 120"><rect width="200" height="120" rx="12" fill="#2a1520"/><g class="fire"><circle cx="100" cy="70" r="20" fill="#ff6b5b"/><circle cx="100" cy="58" r="12" fill="#f2c14e"/></g><text x="16" y="108" fill="#ffe7a3" font-size="13" font-weight="700">夏琐被焚 · 北方联盟败</text></svg>',
        ("split",0): '<svg viewBox="0 0 200 120"><rect width="200" height="120" rx="12" fill="#1a2030"/><circle cx="100" cy="52" r="28" fill="#f2c14e"/><text x="100" y="58" text-anchor="middle" font-size="16" font-weight="800" fill="#1b1406">统一王国</text><text x="16" y="108" fill="#ffe7a3" font-size="13">扫罗 · 大卫 · 所罗门</text></svg>',
        ("split",1): '<svg viewBox="0 0 200 120"><rect width="200" height="120" rx="12" fill="#1a2030"/><circle cx="100" cy="52" r="28" fill="#f2c14e"/><path class="crack" d="M100,20 L94,52 L106,84" fill="none" stroke="#ff6b5b" stroke-width="3"/><text x="16" y="108" fill="#ff6b5b" font-size="13" font-weight="700">示剑：罗波安拒听劝</text></svg>',
        ("split",2): '<svg viewBox="0 0 200 120"><rect width="200" height="120" rx="12" fill="#1a2030"/><circle class="sL" cx="58" cy="52" r="26" fill="#a98bff"/><circle class="sR" cx="142" cy="52" r="26" fill="#f2c14e"/><text x="58" y="58" text-anchor="middle" font-size="12" fill="#fff">以色列</text><text x="142" y="58" text-anchor="middle" font-size="12" fill="#1b1406">犹大</text><text x="16" y="108" fill="#ffe7a3" font-size="13">主前 931 · 一分为二</text></svg>',
        ("split",3): '<svg viewBox="0 0 200 120"><rect width="200" height="120" rx="12" fill="#2a1520"/><ellipse cx="50" cy="70" rx="16" ry="10" fill="#d4a020"/><ellipse cx="150" cy="70" rx="16" ry="10" fill="#d4a020"/><text x="50" y="44" text-anchor="middle" font-size="12" fill="#ff6b5b">但</text><text x="150" y="44" text-anchor="middle" font-size="12" fill="#ff6b5b">伯特利</text><text x="16" y="108" fill="#ff6b5b" font-size="13" font-weight="700">耶罗波安的金牛犊</text></svg>',
        ("exile",0): '<svg viewBox="0 0 200 120"><rect width="200" height="120" rx="12" fill="#3a1520"/><path class="arrow" d="M30,60 L170,40" stroke="#ff6b5b" stroke-width="5" fill="none" marker-end="none"/><text x="16" y="100" fill="#ff6b5b" font-size="13" font-weight="700">722 · 北国亡于亚述</text></svg>',
        ("exile",1): '<svg viewBox="0 0 200 120"><rect width="200" height="120" rx="12" fill="#2a1a10"/><path d="M40,80 L40,40 L80,20 L80,80 Z" fill="#c9a35e"/><path class="flame" d="M60,40 Q70,10 60,0 Q50,10 60,40" fill="#ff6b5b"/><text x="16" y="108" fill="#ff9f43" font-size="13" font-weight="700">586 · 圣殿被焚</text></svg>',
        ("exile",2): '<svg viewBox="0 0 200 120"><rect width="200" height="120" rx="12" fill="#14301a"/><path class="arrow" d="M170,70 L40,70" stroke="#f2c14e" stroke-width="5" fill="none"/><text x="16" y="100" fill="#f2c14e" font-size="13" font-weight="700">538 · 古列下诏归回</text></svg>',
        ("exile",3): '<svg viewBox="0 0 200 120"><rect width="200" height="120" rx="12" fill="#1a2030"/><rect x="40" y="50" width="120" height="24" fill="#2ed3c6"/><rect x="40" y="30" width="16" height="44" fill="#f2c14e"/><rect x="144" y="30" width="16" height="44" fill="#f2c14e"/><text x="16" y="108" fill="#2ed3c6" font-size="13" font-weight="700">445 · 城墙五十二日竣工</text></svg>',
        ("arc",0): '<svg viewBox="0 0 200 120"><rect width="200" height="120" rx="12" fill="#1a3a5c"/><path d="M20,90 L80,90 L80,50 L140,50" fill="none" stroke="#f2c14e" stroke-width="6"/><text x="16" y="108" fill="#ffe7a3" font-size="13">进 — 得地为业</text></svg>',
        ("arc",1): '<svg viewBox="0 0 200 120"><rect width="200" height="120" rx="12" fill="#2a1520"/><path class="spin" d="M100,20 A32,32 0 1 1 99.9,20" fill="none" stroke="#ff9f43" stroke-width="5"/><text x="16" y="108" fill="#ff9f43" font-size="13">乱 — 没有王</text></svg>',
        ("arc",2): '<svg viewBox="0 0 200 120"><rect width="200" height="120" rx="12" fill="#1a2030"/><circle cx="100" cy="52" r="28" fill="#f2c14e"/><text x="16" y="108" fill="#ffe7a3" font-size="13">王 — 大卫之约</text></svg>',
        ("arc",3): '<svg viewBox="0 0 200 120"><rect width="200" height="120" rx="12" fill="#1a2030"/><circle cx="60" cy="52" r="22" fill="#a98bff"/><circle cx="140" cy="52" r="22" fill="#f2c14e"/><text x="16" y="108" fill="#ffe7a3" font-size="13">分 — 北以色列 · 南犹大</text></svg>',
        ("arc",4): '<svg viewBox="0 0 200 120"><rect width="200" height="120" rx="12" fill="#3a1520"/><text x="100" y="58" text-anchor="middle" font-size="28" fill="#ff6b5b" font-weight="800">722 / 586</text><text x="16" y="108" fill="#ff6b5b" font-size="13">亡 — 被掳</text></svg>',
        ("arc",5): '<svg viewBox="0 0 200 120"><rect width="200" height="120" rx="12" fill="#14301a"/><text x="100" y="58" text-anchor="middle" font-size="22" fill="#3ccf8e" font-weight="800">上去吧！</text><text x="16" y="108" fill="#3ccf8e" font-size="13">回 — 余民归回，等候基督</text></svg>',
    }
    return arts.get((fid,i), '<svg viewBox="0 0 200 120"><rect width="200" height="120" rx="12" fill="#1a2030"/></svg>')
def film_conquest():
    return film("conquest", "征服迦南 · 四幕短片", [
        ("🌊", "第一幕 · 过河", "祭司抬约柜脚一入水，约旦河在亚当城立起成垒。神走在百姓前面。", "var(--blue)"),
        ("🧱", "第二幕 · 耶利哥", "绕城七日，第七日七次，城墙倒塌。喇合因信得救，一根朱红线记在家谱里。", "var(--red)"),
        ("☀️", "第三幕 · 南方", "基遍人立约；日头停留在基遍。迦勒八十五岁仍求希伯仑山地。", "var(--gold)"),
        ("🔥", "第四幕 · 北方", "夏琐为北方联盟之首，被火焚烧。地的应许实现，但赶出并不彻底——难处从此埋伏。", "var(--orange)"),
    ], "故事见约书亚记 1–12 章。路线为示意，不是精确行军轨迹。")
def film_split():
    return film("split", "王国分裂 · 四幕短片", [
        ("👑", "第一幕 · 统一的荣华", "扫罗、大卫、所罗门各约四十年。圣殿落成，列国来朝。裂痕已在所罗门晚年种下。", "var(--gold)"),
        ("🪓", "第二幕 · 示剑的决定", "罗波安拒绝长者的劝告：“我的小拇指头比我父亲的腰还粗。”十个支派离去（王上12）。", "var(--red)"),
        ("💔", "第三幕 · 一国变两国", "主前约 931 年：北国以色列（十支派）与南国犹大（大卫家）。同一位神，两条道路。", "var(--purple)"),
        ("🐮", "第四幕 · 金牛犊", "耶罗波安在但与伯特利立牛犊，以免百姓上耶路撒冷。这成为北国十九王的标签。", "var(--orange)"),
    ], "关键章：王上 11–12。分裂是管教，不是神废弃大卫之约。")
def film_exile():
    return film("exile", "被掳与归回 · 四幕短片", [
        ("⛓️", "第一幕 · 722", "撒玛利亚陷落，北国被亚述迁走。迁民政策打碎十支派的认同。", "var(--red)"),
        ("🔥", "第二幕 · 586", "耶路撒冷与圣殿被巴比伦焚毁。大卫的国好像断了，只留下被抬举的约雅斤。", "var(--orange)"),
        ("📜", "第三幕 · 538", "古列下诏：“上耶路撒冷去，建造耶和华的殿。”余民归回，第二圣殿于 516 年完工。", "var(--gold)"),
        ("🧱", "第四幕 · 445", "尼希米修城墙五十二日。律法被大声宣读。故事停在等候中——真大卫、真圣殿还未完全显明。", "var(--teal)"),
    ], "路线沿肥沃月湾北绕，不是直线穿过沙漠。")
def film_arc():
    return film("arc", "一千年六幕：进 · 乱 · 王 · 分 · 亡 · 回", [
        ("⚔️", "进", "约书亚领百姓过河、夺城、分地。神信守对亚伯拉罕“地”的应许。", "var(--gold)"),
        ("🌀", "乱", "没有王，各人任意而行。循环下坠，却总有拯救者被兴起。", "var(--orange)"),
        ("👑", "王", "百姓求王；神赐大卫之约——永远的家、国、位，指向基督。", "var(--purple)"),
        ("💔", "分", "一分为二。北国无一例义王；南国大卫的灯未灭。", "var(--red)"),
        ("🏚️", "亡", "722 与 586：背约的结局是被赶出应许之地。", "var(--red)"),
        ("🌅", "回", "余民归回，殿与墙重建，但安息仍不完全。历史书把我们带到真约书亚、真大卫面前。", "var(--green)"),
    ], "口诀：进—乱—王—分—亡—回。全部指向那位成全圣约的基督。")
