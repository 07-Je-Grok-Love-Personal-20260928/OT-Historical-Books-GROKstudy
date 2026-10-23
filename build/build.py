# -*- coding: utf-8 -*-
import os, json, importlib, sys
sys.path.insert(0, os.path.dirname(__file__))
import lib, layout, maps
OUT = os.path.join(os.path.dirname(__file__), "..", "docs")
MAPS = maps.build(os.path.join(OUT, "assets", "maps"), lib.VER)
lib.MAPS = MAPS
lib.MAP = lambda k: maps.html(k, MAPS, lib.VER)
DESC = {"index": "旧约历史书（约书亚记—以斯帖记）欧陆改革宗深读：时间线、故事线、地图、圣约神学、三项联合信条与三大信经",}
TITLES = {"index": "首页", "bible": "从整本圣经看历史书", "history": "史地与古近东文化", "joshua": "约书亚记", "judges": "士师记 · 路得记", "samuel": "撒母耳记上下",
          "kings": "列王纪上下", "chronicles": "历代志上下", "return": "以斯拉记 · 尼希米记 · 以斯帖记", "confessions": "三项联合信条对照", "creeds": "三大普世信经 · 阅读背诵版",
          "compare": "三大信经深度对比", "memory": "速记与自测", "sources": "来源与核对"}
only = sys.argv[1:]
for slug, _ in layout.PAGES:
    if only and slug not in only: continue
    try: m = importlib.import_module("c_" + slug)
    except ModuleNotFoundError: print("skip", slug); continue
    html = layout.page(slug, TITLES[slug], m.body(), DESC.get(slug, TITLES[slug] + " · 旧约历史书 欧陆改革宗深读"))
    open(os.path.join(OUT, slug + ".html"), "w").write(html); print("wrote", slug, len(html))
os.makedirs(os.path.join(os.path.dirname(__file__), "data"), exist_ok=True)
if not only:
    json.dump(dict(confessions=lib.USED, bible=sorted(set(lib.VUSED))), open(os.path.join(os.path.dirname(__file__), "data", "quotes_used.json"), "w"), ensure_ascii=False, indent=1)
