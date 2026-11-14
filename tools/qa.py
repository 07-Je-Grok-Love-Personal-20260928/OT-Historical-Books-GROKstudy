#!/usr/bin/env python3
"""v2 QA: 360/390/430/768/1024/1440/1920 overflow, interactions, tile-blocked fallback."""
import os, sys, json, re
from playwright.sync_api import sync_playwright
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = os.path.join(R, "docs")
BASE = sys.argv[1] if len(sys.argv)>1 else "file://"+D
PAGES = [f[:-5] for f in sorted(os.listdir(D)) if f.endswith(".html")]
WS = [360, 390, 430, 768, 1024, 1440, 1920]
JS = """()=>{const vw=document.documentElement.clientWidth;const o=[];
document.querySelectorAll('body *').forEach(e=>{if(e.closest('.tw,.scrollx,svg,.toc,.nav,nav,pre,.mapwrap,.gm-view,.lmap,.leaflet-container,.era,.profile,.mind,.hscroll,.clouds,.cmap,.film-art'))return;const r=e.getBoundingClientRect();
if(r.width&&(r.right>vw+2||r.left<-2)){const cs=getComputedStyle(e);if(cs.position!=='fixed'&&cs.visibility!=='hidden'&&cs.display!=='none')o.push(e.tagName+'.'+(e.className||'').toString().slice(0,40)+' '+Math.round(r.left)+'-'+Math.round(r.right))}});
const ids=new Set([...document.querySelectorAll('[id]')].map(e=>e.id));
const miss=[...document.querySelectorAll('a[href^="#"]')].map(a=>a.getAttribute('href').slice(1)).filter(h=>h&&!ids.has(h));
return {sw:document.documentElement.scrollWidth,vw,over:o.slice(0,8),miss:[...new Set(miss)]}}"""
out={}; bad=0
def url(pg):
    return f"{BASE}/{pg}.html" if not BASE.startswith("file://") else f"{BASE}/{pg}.html"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox","--disable-dev-shm-usage"])
    for pg_ in PAGES:
        for w in WS:
            page=b.new_page(viewport={"width":w,"height":800}); errs=[]
            page.on("pageerror", lambda e: errs.append(str(e)))
            page.goto(url(pg_), wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(200)
            page.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
            # interactions (repeat twice)
            for _ in range(2):
                page.evaluate("""() => {
                  const tb=document.getElementById('tocBtn'); if(tb){tb.click(); tb.click();}
                  const ta=document.getElementById('tocAll'); if(ta){ta.click(); ta.click();}
                  const lg=document.getElementById('legBtn'); if(lg){lg.click(); lg.click();}
                  const th=document.getElementById('thBtn'); if(th){th.click(); th.click();}
                  document.querySelectorAll('details.more').forEach(d=>{d.open=true;d.open=false;d.open=true});
                  document.querySelectorAll('.toc .tg').forEach((b,i)=>{if(i<3)b.click()});
                  const fl=document.querySelector('.film [data-a=n], .story [data-a=n]'); if(fl){fl.click();fl.click();}
                  const q=document.querySelector('.quiz .qq button.o'); if(q)q.click();
                  const f=document.querySelector('.flip'); if(f){f.click();f.click();}
                  const rec=document.querySelector('[data-recite]'); if(rec){rec.click();rec.click();}
                }""")
            page.wait_for_timeout(150)
            r=page.evaluate(JS); r["errs"]=errs
            fail = r["sw"]>r["vw"]+2 or r["over"] or errs or r["miss"]
            bad += bool(fail); out[f"{pg_}@{w}"]=r
            print(("❌" if fail else "✅"), pg_, w, "" if not fail else r)
            page.close()
    # interaction + tile block on history (has multiple maps)
    page=b.new_page(viewport={"width":1440,"height":900})
    page.route(re.compile(r"tile\.openstreetmap|basemaps\.cartocdn|arcgisonline|opentopomap|tile-cyclosm|openstreetmap\.fr"), lambda route: route.abort())
    page.goto(url("history"), wait_until="domcontentloaded")
    page.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
    # open first live map tab
    page.wait_for_timeout(400)
    tabs=page.locator('.mapbox .mtabs [data-v="l"]')
    info={"maps": tabs.count(), "tiles": None, "offline_ok": False, "switcher": False, "err": []}
    page.on("pageerror", lambda e: info["err"].append(str(e)))
    if tabs.count():
        page.locator('.mapbox').first.scroll_into_view_if_needed()
        page.wait_for_timeout(400)
        tabs.first.click()
        try:
            page.wait_for_selector('.mapbox .mctl select', timeout=8000)
        except Exception as e:
            info['wait_err']=str(e)
        page.wait_for_timeout(2500)
        box=page.locator('.mapbox').first
        info["tiles"]=box.get_attribute("data-tiles")
        # layer switcher select should exist
        sel=page.locator('.mapbox .mctl select').first
        info["switcher"]=sel.count()>0
        if sel.count():
            # switch to none then auto
            sel.select_option("none"); page.wait_for_timeout(400)
            info["tiles_none"]=box.get_attribute("data-tiles")
            sel.select_option("auto"); page.wait_for_timeout(2000)
            info["tiles_auto"]=box.get_attribute("data-tiles")
        st=page.locator('.mapbox .mst').first
        info["status"]=st.inner_text() if st.count() else ""
        # concept tab still works
        page.locator('.mapbox .mtabs [data-v="c"]').first.click()
        info["concept"]=page.locator('.mapbox .mv-c.on').count()>0
        info["offline_ok"]= (info.get("tiles") or "").startswith("off") or (info.get("tiles_auto") or "").startswith("off") or "离线" in (info.get("status") or "")
    print("TILE-BLOCK", info)
    out["_tile_block"]=info
    if not info["offline_ok"] or info["err"]:
        bad += 1
    page.screenshot(path=os.path.join(R,"_shots","map_tiles_blocked_1440.png"), full_page=False)
    page.close()
    b.close()
json.dump(out, open(os.path.join(R,"build","data","qa_report.json"),"w"), ensure_ascii=False, indent=1)
print("FAILS", bad)
sys.exit(1 if bad else 0)
