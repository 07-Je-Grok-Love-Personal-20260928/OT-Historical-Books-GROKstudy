# -*- coding: utf-8 -*-
import re, html as H
from lib import VER
PAGES = [("index", "🏠 首页"), ("bible", "📖 整本圣经"),
         ("history", "🗺️ 史地总览"), ("history-geo", "⛰️ 地理"), ("history-world", "🌍 帝国列国"), ("history-culture", "🎭 文化考古"),
         ("joshua", "⚔️ 约书亚记"), ("judges", "🌾 士师·路得"),
         ("samuel", "👑 撒母耳记"), ("kings", "🏛️ 列王纪"), ("chronicles", "📜 历代志"), ("return", "🧱 拉·尼·斯"),
         ("confessions", "📚 信条对照"), ("creeds", "✨ 三大信经"), ("compare", "⚖️ 信经对比"), ("memory", "🧠 速记自测"), ("sources", "🔖 来源")]
TITLE = "旧约历史书 · 欧陆改革宗深读"

def _plain(t):
    return re.sub(r"<[^>]+>", "", t)

def toc(body):
    hs = re.findall(r'<h([2-4]) id="([^"]+)"[^>]*>(.*?)</h\1>', body)
    tree = []
    for lv, id, t in hs:
        t = _plain(t); lv = int(lv)
        node = {"id": id, "t": t, "ch": []}
        if lv == 2 or not tree:
            tree.append(node)
        elif lv == 3:
            tree[-1]["ch"].append(node)
        else:
            if not tree[-1]["ch"]:
                tree[-1]["ch"].append({"id": tree[-1]["id"] + "-sec", "t": "本节", "ch": []})
            tree[-1]["ch"][-1]["ch"].append(node)
    def li(node, nums, level):
        num = ".".join(str(n) for n in nums)
        title = H.escape(node["t"])
        ch = node["ch"]
        has = " has" if ch else ""
        btn = ('<button class="tg" type="button" aria-label="展开或收起下级目录" aria-expanded="true">▼</button>' if ch else "")
        sub = ""
        if ch:
            inner = "".join(li(c, nums + [i + 1], level + 1) for i, c in enumerate(ch))
            sub = f'<ol class="toc-l{level+1}">{inner}</ol>'
        return (f'<li class="l{level}{has}" data-id="{H.escape(node["id"])}">'
                f'<div class="grp"><span class="num">{num}</span>'
                f'<a href="#{H.escape(node["id"])}" title="{title}">{title}</a>{btn}</div>{sub}</li>')
    return "".join(li(n, [i + 1], 1) for i, n in enumerate(tree))

def wrap_blk(body):
    parts = re.split(r'(?=<h2\b)', body, flags=re.I)
    out = []
    for i, ch in enumerate(parts):
        if not ch.strip(): continue
        out.append(f'<section class="blk" data-i="{i}">{ch}</section>')
    return "".join(out)

def page(slug, title, body, desc=""):
    nav = "".join(f'<a href="{s}.html"{" class=on" if s == slug else ""}>{t}</a>' for s, t in PAGES)
    i = [s for s, _ in PAGES].index(slug)
    pv = PAGES[i - 1] if i > 0 else None; nx = PAGES[i + 1] if i + 1 < len(PAGES) else None
    pager = '<nav class="pager">' + (f'<a href="{pv[0]}.html"><small>← 上一页</small>{pv[1]}</a>' if pv else "<span></span>") + (f'<a href="{nx[0]}.html"><small>下一页 →</small>{nx[1]}</a>' if nx else "") + "</nav>"
    body = wrap_blk(body)
    tc = toc(body)
    return f'''<!doctype html><html lang="zh-Hans" data-theme="night"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{H.escape(title)} · {TITLE}</title><meta name="description" content="{H.escape(desc or title)}"><meta name="theme-color" content="#0b1020">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E📜%3C/text%3E%3C/svg%3E">
<script>(function(h){{h.classList.add('js');try{{var t=localStorage.getItem('otb.theme');if(t)h.setAttribute('data-theme',t);if(localStorage.getItem('otb.toc')==='off')h.classList.add('toc-off');var w=+localStorage.getItem('otb.tocw');if(w>=200&&w<=720)h.style.setProperty('--tocw',w+'px')}}catch(e){{}}}})(document.documentElement)</script>
<link rel="stylesheet" href="assets/site.css?v={VER}"></head><body>
<div class="clouds" aria-hidden="true"><i style="--c:rgba(90,169,255,.55);--s:420px;--x:-8%;--y:-6%;--t:32s"></i><i style="--c:rgba(242,193,78,.4);--s:360px;--x:72%;--y:8%;--t:26s"></i><i style="--c:rgba(169,139,255,.45);--s:480px;--x:40%;--y:70%;--t:38s"></i></div>
<div class="prog" aria-hidden="true"></div>
<header class="top"><button class="ib" id="tocBtn" aria-label="显示/隐藏目录" type="button">☰ <small>目录</small></button><a class="brand" href="index.html">📜 <span>{TITLE}</span></a><nav class="nav" aria-label="页面">{nav}</nav>
<div class="legpop"><button class="ib" id="legBtn" aria-expanded="false" aria-label="笔记标记图例" type="button">🖍 <span class="lab">标记</span></button>
<div class="panel" role="note"><strong>笔记标记图例</strong>
<div class="legend" style="margin:8px 0 0;padding:0;border:0;background:none">
<span><b class="k">重点</b>＝金色底纹</span>
<span><b class="h">难点</b>＝红色波浪线</span>
<span><b class="xr">指向基督</b>＝粉色实线</span>
<span><b class="cv">圣约</b>＝青色虚线</span>
<span><b class="mm">记忆钩</b>＝紫色点线</span>
<span><b class="th">总纲</b>＝金条左边线</span>
<span><span class="d">年代</span></span>
<span><span class="pl">地名</span></span>
<span><span class="pn">人物</span></span>
<span><span class="vr">经文</span></span>
</div></div></div>
<button class="ib" id="thBtn" aria-label="切换深色/羊皮纸主题" type="button">🌓</button></header>
<div class="wrap"><aside class="toc" id="tocPanel" aria-label="本页目录">
<div class="toc-scroll">
<div class="toc-head"><h5>本页目录 · {H.escape(title)}</h5>
<input id="tocQ" type="search" placeholder="🔍 筛选目录…" aria-label="筛选目录">
<div class="tools"><button class="ib" type="button" id="tocAll">⇅ 全部展开/收起</button></div></div>
<ol class="toc-l1">{tc}</ol>
</div>
<div class="toc-resizer" id="tocResize" role="separator" aria-orientation="vertical" aria-label="拖动调整目录宽度" tabindex="0"></div>
</aside><div class="scrim" id="tocScrim"></div>
<main id="main">{body}{pager}</main></div>
<footer>📜 {TITLE} · 版本 {VER} · GROKstudy｜三大普世信经与三项联合信条引文逐字取自 <a href="https://ccifellowship.org" target="_blank" rel="noopener">ccifellowship.org</a>（脚注编号省略）；经文为和合本。其余讲解为本站学习概述。<a href="sources.html">来源与核对 →</a></footer>
<div class="fab"><button class="ib" id="toTop" aria-label="回到顶部" type="button">⬆</button></div>
<script src="assets/site.js?v={VER}" defer></script></body></html>'''
