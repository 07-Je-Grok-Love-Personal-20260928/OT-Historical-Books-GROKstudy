#!/usr/bin/env python3
"""Playwright scroll/interaction timings + optional Lighthouse. Usage: perf.py URL_PREFIX out_json [pages...]"""
import json, sys, time, subprocess, os
from playwright.sync_api import sync_playwright
base = sys.argv[1].rstrip("/")
outp = sys.argv[2]
pages = sys.argv[3:] or ["index", "history", "kings", "compare"]
res = {}
JS_SETUP = """() => {
  window.__lt = [];
  try { new PerformanceObserver(l => l.getEntries().forEach(e => window.__lt.push(e.duration))).observe({type:'longtask', buffered:true}); } catch(e) {}
}"""
JS_SCROLL = """async () => {
  const t0 = performance.now();
  let frames = 0, last = t0, gaps = [];
  const step = () => { const n = performance.now(); gaps.push(n-last); last=n; frames++; };
  const id = requestAnimationFrame(function loop(){ step(); if (document.scrollingElement.scrollTop + innerHeight < document.scrollingElement.scrollHeight - 8) { document.scrollingElement.scrollBy(0, 90); requestAnimationFrame(loop);} else { window.__doneScroll=true; }});
  await new Promise(r => { const w = () => window.__doneScroll ? r() : setTimeout(w, 40); w(); });
  cancelAnimationFrame(id);
  const dur = performance.now()-t0;
  const fps = frames / (dur/1000);
  const longFrames = gaps.filter(g => g>32).length;
  const nav = performance.getEntriesByType('navigation')[0] || {};
  const paint = Object.fromEntries(performance.getEntriesByType('paint').map(p=>[p.name, Math.round(p.startTime)]));
  const lt = (window.__lt||[]).slice();
  return {dur:Math.round(dur), frames, fps:+fps.toFixed(1), longFrames, longTasks:lt.length, longTaskMs:Math.round(lt.reduce((a,b)=>a+b,0)),
    dcl:Math.round(nav.domContentLoadedEventEnd||0), load:Math.round(nav.loadEventEnd||0),
    ttfb:Math.round(nav.responseStart||0), transfer:Math.round(nav.transferSize||0), paints:paint,
    sw:document.documentElement.scrollWidth, vw:document.documentElement.clientWidth, h:document.documentElement.scrollHeight};
}"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox","--disable-dev-shm-usage"])
    for pg in pages:
        url = f"{base}/{pg}.html"
        page = b.new_page(viewport={"width":1440,"height":900})
        page.add_init_script("window.__lt=[]")
        t0=time.time(); page.goto(url, wait_until="networkidle", timeout=60000)
        page.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
        page.evaluate("""() => { try { new PerformanceObserver(l => l.getEntries().forEach(e => (window.__lt=window.__lt||[]).push(e.duration))).observe({type:'longtask', buffered:true}); } catch(e) {} }""")
        data = page.evaluate(JS_SCROLL)
        data["navMs"] = round((time.time()-t0)*1000)
        # click a few interactive bits if present
        data["clicks"] = page.evaluate("""() => {
          const r={toc:false,quiz:false,flip:false,story:false};
          const tb=document.getElementById('tocBtn'); if(tb){tb.click();tb.click();r.toc=true}
          const q=document.querySelector('.quiz .qq button.o'); if(q){q.click();r.quiz=true}
          const f=document.querySelector('.flip'); if(f){f.click();f.click();r.flip=true}
          const s=document.querySelector('.story [data-a=n]'); if(s){s.click();s.click();r.story=true}
          return r;
        }""")
        res[pg]=data; print(pg, data); page.close()
    b.close()
# lighthouse if available
lh = {}
lhbin = os.path.expanduser("~/.local/bin/lighthouse")
if os.path.exists(lhbin):
    for pg in pages[:3]:
        tmp=f"/tmp/lh-{pg}.json"
        cmd=[lhbin, f"{base}/{pg}.html", "--only-categories=performance", "--chrome-flags=--headless --no-sandbox --disable-gpu",
             "--quiet", "--output=json", f"--output-path={tmp}", "--throttling-method=provided"]
        try:
            subprocess.run(cmd, check=False, timeout=180)
            d=json.load(open(tmp))
            a=d["audits"]; cat=d["categories"]["performance"]["score"]
            def v(k, field="numericValue"):
                x=a.get(k,{})
                return x.get(field)
            lh[pg]=dict(score=cat, lcp=v("largest-contentful-paint"), tbt=v("total-blocking-time"),
                        cls=v("cumulative-layout-shift"), fcp=v("first-contentful-paint"),
                        si=v("speed-index"), tti=v("interactive"))
            print("LH", pg, lh[pg])
        except Exception as e:
            print("LH fail", pg, e)
res["_lighthouse"]=lh
json.dump(res, open(outp,"w"), indent=2)
print("wrote", outp)
