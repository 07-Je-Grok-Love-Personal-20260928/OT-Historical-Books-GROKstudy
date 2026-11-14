(function(){
var d=document,h=d.documentElement,LS=window.localStorage;
function g(k){try{return LS.getItem(k)}catch(e){return null}}function s(k,v){try{LS.setItem(k,v)}catch(e){}}
var wide=function(){return window.matchMedia('(min-width:1100px)').matches};
// ----- 3-level TOC: toggle, fold memory, resize, filter -----
var tb=d.getElementById('tocBtn');
if(tb)tb.addEventListener('click',function(){if(wide()){h.classList.toggle('toc-off');s('otb.toc',h.classList.contains('toc-off')?'off':'on')}else h.classList.toggle('toc-open')});
var sc=d.querySelector('.scrim');if(sc)sc.addEventListener('click',function(){h.classList.remove('toc-open')});
d.querySelectorAll('.toc a').forEach(function(a){a.addEventListener('click',function(){if(!wide())h.classList.remove('toc-open')})});
var foldKey='otb.tocfold.'+(location.pathname.split('/').pop()||'index.html');
function readFold(){try{return JSON.parse(g(foldKey)||'{}')}catch(e){return {}}}
function saveFold(){var o={};d.querySelectorAll('.toc li.has').forEach(function(li){o[li.getAttribute('data-id')||'']=li.classList.contains('closed')});s(foldKey,JSON.stringify(o))}
(function restoreFold(){
  var o=readFold();
  d.querySelectorAll('.toc li.has').forEach(function(li){
    var id=li.getAttribute('data-id');
    if(o[id]){li.classList.add('closed');var b=li.querySelector(':scope > .grp .tg');if(b)b.setAttribute('aria-expanded','false')}
  });
})();
d.querySelectorAll('.toc .tg').forEach(function(b){b.addEventListener('click',function(){var li=b.closest('li');li.classList.toggle('closed');b.setAttribute('aria-expanded',!li.classList.contains('closed'));saveFold()})});
var ex=d.getElementById('tocAll');if(ex)ex.addEventListener('click',function(){var c=d.querySelectorAll('.toc li.has.closed').length;var close=!c;d.querySelectorAll('.toc li.has').forEach(function(li){li.classList.toggle('closed',close);var b=li.querySelector(':scope > .grp .tg');if(b)b.setAttribute('aria-expanded',!close)});saveFold()});
var ti=d.getElementById('tocQ');if(ti)ti.addEventListener('input',function(){var q=ti.value.trim();d.querySelectorAll('.toc li').forEach(function(li){var show=!q||(li.textContent||'').indexOf(q)>=0;li.style.display=show?'':'none';if(q&&show){li.classList.remove('closed');var b=li.querySelector(':scope > .grp .tg');if(b)b.setAttribute('aria-expanded','true')}})});
function clampToc(w){
  var min=220, max=Math.min(640, Math.floor(innerWidth*(wide()?0.7:0.92)));
  return Math.max(min, Math.min(max, Math.round(w)));
}
function applyTocW(w){w=clampToc(w);h.style.setProperty('--tocw',w+'px');var r=d.getElementById('tocResize');if(r){r.setAttribute('aria-valuenow',w);r.setAttribute('aria-valuemin',220);r.setAttribute('aria-valuemax',640)}return w}
applyTocW(parseInt(getComputedStyle(h).getPropertyValue('--tocw'),10)||320);
(function tocResize(){
  var handle=d.getElementById('tocResize'), panel=d.getElementById('tocPanel');
  if(!handle||!panel)return;
  var dragging=false, startX=0, startW=0;
  function widthNow(){return panel.getBoundingClientRect().width}
  function down(ev){
    if(ev.pointerType==='mouse'&&ev.button!==0)return;
    ev.preventDefault();
    dragging=true; startX=ev.clientX; startW=widthNow();
    h.classList.add('toc-drag');
    try{handle.setPointerCapture(ev.pointerId)}catch(e){}
  }
  function move(ev){if(!dragging)return;ev.preventDefault();applyTocW(startW+(ev.clientX-startX))}
  function up(ev){
    if(!dragging)return;dragging=false;h.classList.remove('toc-drag');
    s('otb.tocw', String(clampToc(widthNow())));
    try{handle.releasePointerCapture(ev.pointerId)}catch(e){}
  }
  handle.addEventListener('pointerdown',down);
  handle.addEventListener('pointermove',move);
  handle.addEventListener('pointerup',up);
  handle.addEventListener('pointercancel',up);
  handle.addEventListener('keydown',function(e){
    var w=widthNow();
    if(e.key==='ArrowLeft'){e.preventDefault();s('otb.tocw',String(applyTocW(w-24)))}
    if(e.key==='ArrowRight'){e.preventDefault();s('otb.tocw',String(applyTocW(w+24)))}
    if(e.key==='Home'){e.preventDefault();s('otb.tocw',String(applyTocW(220)))}
    if(e.key==='End'){e.preventDefault();s('otb.tocw',String(applyTocW(640)))}
  });
})();
// theme
var th=d.getElementById('thBtn');if(th)th.addEventListener('click',function(){var n=h.getAttribute('data-theme')==='paper'?'night':'paper';h.setAttribute('data-theme',n);s('otb.theme',n)});
// progress
var pr=d.querySelector('.prog'),tick=false;
function onS(){if(tick)return;tick=true;requestAnimationFrame(function(){var m=h.scrollHeight-h.clientHeight;pr.style.transform='scaleX('+(m>0?h.scrollTop/m:0)+')';tick=false})}
if(pr){window.addEventListener('scroll',onS,{passive:true});onS()}
// scrollspy
var links={};d.querySelectorAll('.toc a[href^="#"]').forEach(function(a){links[a.getAttribute('href').slice(1)]=a});
function openAncestors(a){
  var li=a.closest('li');
  while(li){
    if(li.classList.contains('has')&&li.classList.contains('closed')){
      li.classList.remove('closed');
      var b=li.querySelector(':scope > .grp .tg');if(b)b.setAttribute('aria-expanded','true');
    }
    var ol=li.parentElement;li=ol?ol.closest('li'):null;
  }
}
if('IntersectionObserver' in window){
 var cur=null,io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){var a=links[e.target.id];if(a&&a!==cur){if(cur)cur.classList.remove('on');a.classList.add('on');cur=a;openAncestors(a);if(a.scrollIntoViewIfNeeded)a.scrollIntoViewIfNeeded(false);else a.scrollIntoView({block:'nearest'})}}})},{rootMargin:'-70px 0px -70% 0px'});
 d.querySelectorAll('main h2[id],main h3[id],main h4[id]').forEach(function(x){io.observe(x)});
 if(!window.matchMedia('(prefers-reduced-motion:reduce)').matches){
  var ro=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');ro.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
  d.querySelectorAll('.reveal').forEach(function(x){ro.observe(x)});
 } else d.querySelectorAll('.reveal').forEach(function(x){x.classList.add('in')});
} else d.querySelectorAll('.reveal').forEach(function(x){x.classList.add('in')});
// story stepper
d.querySelectorAll('.story').forEach(function(st){var ss=st.querySelectorAll('.st'),ds=st.querySelectorAll('.dot'),i=0,tm=null;
 function go(n){i=(n+ss.length)%ss.length;ss.forEach(function(x,j){x.classList.toggle('on',j===i)});ds.forEach(function(x,j){x.classList.toggle('on',j===i)})}
 ds.forEach(function(b,j){b.addEventListener('click',function(){stop();go(j)})});
 var pv=st.querySelector('[data-a=p]'),nx=st.querySelector('[data-a=n]'),pl=st.querySelector('[data-a=play]');
 function stop(){if(tm){clearInterval(tm);tm=null;if(pl)pl.textContent='▶ 自动播放'}}
 if(pv)pv.addEventListener('click',function(){stop();go(i-1)});if(nx)nx.addEventListener('click',function(){stop();go(i+1)});
 if(pl)pl.addEventListener('click',function(){if(tm){stop();return}pl.textContent='⏸ 暂停';tm=setInterval(function(){go(i+1)},4200)});go(0)});
// maps
d.querySelectorAll('.gmap').forEach(function(m){var inn=m.querySelector('.gm-in'),z=1,hs=m.querySelectorAll('.hs'),li=m.querySelectorAll('.gm-leg li');
 m.querySelectorAll('.gm-z button').forEach(function(b){b.addEventListener('click',function(){var k=+b.getAttribute('data-z');z=k===0?1:Math.max(1,Math.min(3,z+k*.5));inn.style.width=(z*100)+'%'})});
 function on(i,scroll){hs.forEach(function(x,j){x.classList.toggle('on',j==i)});li.forEach(function(x,j){x.classList.toggle('on',j==i)});
  if(scroll==='map'&&hs[i]){var v=m.querySelector('.gm-view'),r=hs[i];v.scrollTo({left:r.offsetLeft-v.clientWidth/2,top:r.offsetTop-v.clientHeight/2,behavior:'smooth'})}
  if(scroll==='leg'&&li[i]&&li[i].scrollIntoView){var p=li[i].parentElement;if(p.scrollHeight>p.clientHeight)p.scrollTop=li[i].offsetTop-p.offsetTop-40}}
 hs.forEach(function(b){b.addEventListener('click',function(){on(b.getAttribute('data-i'),'leg')})});
 li.forEach(function(x){function f(){on(x.getAttribute('data-i'),'map')}x.addEventListener('click',f);x.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();f()}})})});
// flip cards
d.querySelectorAll('.flip').forEach(function(f){f.setAttribute('tabindex','0');function t(){f.classList.toggle('on')}f.addEventListener('click',t);f.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();t()}})});
var fa=d.getElementById('flipAll');if(fa)fa.addEventListener('click',function(){var fs=d.querySelectorAll('.flip'),any=d.querySelectorAll('.flip.on').length;fs.forEach(function(f){f.classList.toggle('on',!any)})});
// quiz
d.querySelectorAll('.quiz').forEach(function(q){var tot=q.querySelectorAll('.qq').length,ok=0,sc=q.querySelector('.score');
 q.querySelectorAll('.qq').forEach(function(x){x.querySelectorAll('button.o').forEach(function(b){b.addEventListener('click',function(){if(x.classList.contains('done'))return;x.classList.add('done');
  if(b.hasAttribute('data-ok')){b.classList.add('ok');ok++}else{b.classList.add('no');var r=x.querySelector('[data-ok]');if(r)r.classList.add('ok')}
  if(sc)sc.textContent='得分 '+ok+' / '+tot})})});
 var rs=q.querySelector('[data-a=reset]');if(rs)rs.addEventListener('click',function(){ok=0;q.querySelectorAll('.qq').forEach(function(x){x.classList.remove('done');x.querySelectorAll('.o').forEach(function(b){b.classList.remove('ok','no')})});if(sc)sc.textContent='得分 0 / '+tot})});
// recite mode
d.querySelectorAll('[data-recite]').forEach(function(b){var c=d.getElementById(b.getAttribute('data-recite'));b.addEventListener('click',function(){c.classList.toggle('recite');c.querySelectorAll('.ln').forEach(function(l){l.classList.remove('show')});b.textContent=c.classList.contains('recite')?'👁️ 显示全文':'🙈 背诵模式（遮盖）'})});
d.querySelectorAll('.creed').forEach(function(c){c.addEventListener('click',function(e){var l=e.target.closest('.ln');if(l&&c.classList.contains('recite'))l.classList.toggle('show')})});
d.querySelectorAll('[data-big]').forEach(function(b){var c=d.getElementById(b.getAttribute('data-big'));b.addEventListener('click',function(){var f=parseFloat(getComputedStyle(c).fontSize);c.style.fontSize=(f*(b.getAttribute('data-d')==='+'?1.1:0.9))+'px'})});
var top=d.getElementById('toTop');if(top)top.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'})});
})();

/* ===== v2.0: smooth nav, films, maps, prefetch, view-transitions ===== */
(function(){
var d=document,h=d.documentElement,LS=window.localStorage;
function g(k){try{return LS.getItem(k)}catch(e){return null}}function s(k,v){try{LS.setItem(k,v)}catch(e){}}
var RM=window.matchMedia('(prefers-reduced-motion:reduce)').matches;
/* accurate in-page nav with content-visibility sections */
function topOff(){return (parseInt(getComputedStyle(h).getPropertyValue('--top'))||58)+12}
function settle(t){
  d.querySelectorAll('.blk').forEach(function(c){
    if(c===t||c.contains(t)||(c.compareDocumentPosition(t)&Node.DOCUMENT_POSITION_FOLLOWING)) c.style.contentVisibility='visible';
  });
  t.getBoundingClientRect();
  setTimeout(function(){d.querySelectorAll('.blk').forEach(function(c){c.style.contentVisibility='';});},600);
}
function goTo(t,smooth){
  settle(t);
  var y=function(){return t.getBoundingClientRect().top+(h.scrollTop||scrollY)-topOff();};
  var user=false;['wheel','touchstart','keydown','pointerdown'].forEach(function(ev){addEventListener(ev,function(){user=true},{once:true,passive:true})});
  var fix=function(){if(user)return;var df=t.getBoundingClientRect().top-topOff();if(Math.abs(df)>4)scrollTo({top:y(),behavior:'instant'})};
  if(smooth&&!RM){scrollTo({top:y(),behavior:'smooth'});addEventListener('scrollend',fix,{once:true});[800,1400].forEach(function(ms){setTimeout(fix,ms)})}
  else{scrollTo({top:y(),behavior:'instant'});requestAnimationFrame(fix)}
}
d.addEventListener('click',function(e){
  var a=e.target.closest('a[href^="#"]');if(!a||e.defaultPrevented||e.button!==0||e.metaKey||e.ctrlKey)return;
  var id=decodeURIComponent(a.getAttribute('href').slice(1));var t=id&&d.getElementById(id);if(!t)return;
  e.preventDefault();history.pushState(null,'','#'+id);goTo(t,true);
});
if(location.hash.length>1){var t0=d.getElementById(decodeURIComponent(location.hash.slice(1)));if(t0){if('scrollRestoration' in history)history.scrollRestoration='manual';requestAnimationFrame(function(){goTo(t0,false)})}}
/* legend popover */
var lp=d.getElementById('legBtn'),panel=d.querySelector('.legpop .panel');
if(lp){lp.addEventListener('click',function(e){e.stopPropagation();lp.parentElement.classList.toggle('open');lp.setAttribute('aria-expanded',lp.parentElement.classList.contains('open'))});
d.addEventListener('click',function(){if(lp.parentElement.classList.contains('open'))lp.parentElement.classList.remove('open')});
if(panel)panel.addEventListener('click',function(e){e.stopPropagation()})}
/* films share story-like controls */
d.querySelectorAll('.film').forEach(function(st){
  var ss=st.querySelectorAll('.st'),ds=st.querySelectorAll('.dot'),i=0,tm=null;
  function go(n){i=(n+ss.length)%ss.length;ss.forEach(function(x,j){x.classList.toggle('on',j===i)});ds.forEach(function(x,j){x.classList.toggle('on',j===i)})}
  ds.forEach(function(b,j){b.addEventListener('click',function(){stop();go(j)})});
  var pv=st.querySelector('[data-a=p]'),nx=st.querySelector('[data-a=n]'),pl=st.querySelector('[data-a=play]');
  function stop(){if(tm){clearInterval(tm);tm=null;if(pl)pl.textContent='▶ 播放短片'}}
  if(pv)pv.addEventListener('click',function(){stop();go(i-1)});
  if(nx)nx.addEventListener('click',function(){stop();go(i+1)});
  if(pl)pl.addEventListener('click',function(){if(tm){stop();return}pl.textContent='⏸ 暂停';tm=setInterval(function(){go(i+1)},RM?2800:2200)});
  go(0);
});
/* prefetch next/prev */
d.querySelectorAll('.pager a[href], .nav a[href]').forEach(function(a){
  var href=a.getAttribute('href');if(!href||href.indexOf('http')===0)return;
  var l=d.createElement('link');l.rel='prefetch';l.href=href;d.head.appendChild(l);
});
/* ---------- maps ---------- */
var TILES=[
 {id:'osm',n:'OpenStreetMap',u:'https://tile.openstreetmap.org/{z}/{x}/{y}.png',o:{maxZoom:19,attribution:'© <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>'}},
 {id:'voyager',n:'CARTO Voyager',u:'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',o:{maxZoom:20,subdomains:'abcd',attribution:'© OSM · © <a href="https://carto.com/attributions" target="_blank" rel="noopener">CARTO</a>'}},
 {id:'positron',n:'CARTO 浅色',u:'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',o:{maxZoom:20,subdomains:'abcd',attribution:'© OSM · © CARTO'}},
 {id:'darkmatter',n:'CARTO 深色',u:'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',o:{maxZoom:20,subdomains:'abcd',attribution:'© OSM · © CARTO'}},
 {id:'esri-img',n:'Esri 卫星影像',u:'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',o:{maxZoom:19,attribution:'Tiles © Esri — Source: Esri, Maxar, Earthstar Geographics'}},
 {id:'esri-topo',n:'Esri 地形',u:'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',o:{maxZoom:19,attribution:'Tiles © Esri'}},
 {id:'esri-street',n:'Esri 街道',u:'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',o:{maxZoom:19,attribution:'Tiles © Esri'}},
 {id:'esri-phys',n:'Esri 自然地貌',u:'https://server.arcgisonline.com/ArcGIS/rest/services/World_Physical_Map/MapServer/tile/{z}/{y}/{x}',o:{maxZoom:8,attribution:'Tiles © Esri'}},
 {id:'hot',n:'OSM France · HOT',u:'https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',o:{maxZoom:19,subdomains:'abc',attribution:'© OSM · HOT · OSM France'}},
 {id:'topo',n:'OpenTopoMap',u:'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',o:{maxZoom:17,subdomains:'abc',attribution:'© OSM, SRTM, OpenTopoMap (CC-BY-SA)'}},
 {id:'osmde',n:'OSM 德国',u:'https://tile.openstreetmap.de/{z}/{x}/{y}.png',o:{maxZoom:19,attribution:'© <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>'}},
 {id:'osmfr',n:'OSM 法国',u:'https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png',o:{maxZoom:20,subdomains:'abc',attribution:'© OSM · OSM France'}},
 {id:'cyclosm',n:'CyclOSM',u:'https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png',o:{maxZoom:20,subdomains:'abc',attribution:'© OSM · CyclOSM'}},
 {id:'esri-relief',n:'Esri 晕渲地形',u:'https://server.arcgisonline.com/ArcGIS/rest/services/World_Shaded_Relief/MapServer/tile/{z}/{y}/{x}',o:{maxZoom:13,attribution:'Tiles © Esri'}},
 {id:'esri-gray',n:'Esri 浅灰底图',u:'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}',o:{maxZoom:16,attribution:'Tiles © Esri'}},
 {id:'esri-natgeo',n:'Esri 国家地理',u:'https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}',o:{maxZoom:16,attribution:'Tiles © Esri'}}
];
window.__tileLog=[];
var leafletP=null;
function loadLeaflet(){
  if(leafletP)return leafletP;
  leafletP=new Promise(function(res,rej){
    if(window.L)return res(window.L);
    var c=d.createElement('link');c.rel='stylesheet';c.href='assets/vendor/leaflet/leaflet.css';d.head.appendChild(c);
    var s=d.createElement('script');s.src='assets/vendor/leaflet/leaflet.js';s.onload=function(){res(window.L)};s.onerror=rej;d.head.appendChild(s);
  });
  return leafletP;
}
var geoP={};
function getGeo(b){return geoP[b]||(geoP[b]=fetch('assets/geo/'+b+'.json').then(function(r){if(!r.ok)throw new Error(r.status);return r.json()}))}
function curve(a,b,bend){var n=24,mx=(a[0]+b[0])/2,my=(a[1]+b[1])/2,dx=b[0]-a[0],dy=b[1]-a[1],cx=mx-dy*bend,cy=my+dx*bend,pts=[];for(var i=0;i<=n;i++){var t=i/n,u=1-t;pts.push([u*u*a[0]+2*u*t*cx+t*t*b[0],u*u*a[1]+2*u*t*cy+t*t*b[1]])}return pts}
function liveMap(box,data,onPick){
  var el=box.querySelector('.lmap');el.textContent='🗺️ 地图加载中…';
  return loadLeaflet().then(function(L){
    el.textContent='';
    var coarse=matchMedia('(pointer:coarse)').matches;
    var map=L.map(el,{zoomSnap:.5,scrollWheelZoom:false,dragging:!coarse,tap:false,worldCopyJump:true});
    map.createPane('basePane').style.zIndex=150;
    var rend=L.canvas({pane:'basePane',padding:.3});
    map.attributionControl.setPrefix('<a href="https://leafletjs.com" target="_blank" rel="noopener">Leaflet</a>');
    map.attributionControl.addAttribution('离线底图 <a href="https://www.naturalearthdata.com/" target="_blank" rel="noopener">Natural Earth</a>（公有领域）');
    var st={map:map,base:null,layer:null,idx:-1,ok:0,err:0,timer:0};
    function probe(v){return getComputedStyle(h).getPropertyValue(v).trim()}
    function baseStyle(f){var k=f&&f.properties&&f.properties.k;var land=probe('--geo-land')||'#e4c88a',coast=probe('--geo-coast')||'#8a6a3a',riv=probe('--geo-river')||'#5eb0e6',sea=probe('--geo-sea')||'#16344f';
      return k==='river'?{color:riv,weight:1.4,opacity:.85,fill:false}:k==='lake'?{color:riv,weight:.6,fillColor:sea,fillOpacity:1}:{color:coast,weight:1,fillColor:land,fillOpacity:1}}
    el.style.background=probe('--geo-sea')||'#16344f';
    getGeo(data.base||'ane').then(function(gj){st.base=L.geoJSON(gj,{renderer:rend,pane:'basePane',interactive:false,style:baseStyle}).addTo(map)}).catch(function(e){console.warn('geo base',e)});
    var P=new Map(data.places.map(function(p){return [p.k,p]}));
    var mk=data.places.map(function(p,i){
      return L.marker([p.lat,p.lng],{title:p.n,riseOnHover:true,icon:L.divIcon({className:'',html:'<div class="lpin" style="--c:'+p.c+'">'+p.i+'</div>',iconSize:[28,28],iconAnchor:[14,14]})})
        .bindTooltip(p.n,{className:'ltip',direction:'right',offset:[12,0]})
        .bindPopup('<b>'+p.i+' '+p.n+'</b>'+(p.en?' <i>'+p.en+'</i>':'')+'<br><span class="d">'+p.w+'</span><p style="margin:.4em 0 0">'+p.d+'</p>',{maxWidth:280})
        .on('click',function(){onPick(i,true)}).addTo(map);
    });
    var rl=null;
    function drawRoutes(){
      if(rl)map.removeLayer(rl);
      rl=L.layerGroup((data.routes||[]).map(function(r){
        var a=P.get(r.a),b=P.get(r.b);if(!a||!b)return null;
        var col={'gold':'#f2c14e','red':'#ff6b5b','orange':'#ff9f43','blue':'#5aa9ff','green':'#3ccf8e','purple':'#a98bff','teal':'#2ed3c6','pink':'#ff7eb6','gray':'#8c97b2'}[r.k]||'#f2c14e';
        return L.polyline(curve([a.lat,a.lng],[b.lat,b.lng],r.bend||.16),{color:col,weight:3,opacity:.85});
      }).filter(Boolean)).addTo(map);
    }
    drawRoutes();
    var bds=L.latLngBounds(data.places.map(function(p){return [p.lat,p.lng]}));
    map.fitBounds(bds,{padding:[32,32],maxZoom:data.base==='levant'?11:7});
    var Ctl=L.Control.extend({onAdd:function(){var div=L.DomUtil.create('div','mctl');div.innerHTML='<span class="mst wait">⏳ 准备瓦片…</span><select aria-label="在线瓦片来源"><option value="auto">自动（失败时切换）</option>'+TILES.map(function(t){return '<option value="'+t.id+'">'+t.n+'</option>'}).join('')+'<option value="none">仅离线底图</option></select>';L.DomEvent.disableClickPropagation(div);L.DomEvent.disableScrollPropagation(div);return div}});
    var ctl=new Ctl({position:'topright'}).addTo(map),cd=ctl.getContainer(),stEl=cd.querySelector('.mst'),sel=cd.querySelector('select');
    function status(c,t){stEl.className='mst '+c;stEl.textContent=t;box.dataset.tiles=c+':'+(st.idx>=0?TILES[st.idx].id:'none')}
    var T=function(){return window.__tileTimeout||6000};
    function clear(){clearTimeout(st.timer);if(st.layer){var ly=st.layer;st.layer=null;map.removeLayer(ly);ly.off('tileload tileerror')}}
    function use(i){
      clear();var mode=sel.value;
      if(i<0||i>=TILES.length){st.idx=-1;status('off',mode==='none'?'🧭 仅离线底图（已手动选择）':'🧭 离线底图（在线瓦片均不可用）');window.__tileLog.push([data.id,'offline']);return}
      st.idx=i;st.ok=0;st.err=0;var t=TILES[i];status('wait','⏳ 正在连接 '+t.n+'…');
      var ly=L.tileLayer(t.u,Object.assign({updateWhenIdle:true,keepBuffer:1,referrerPolicy:'strict-origin-when-cross-origin',crossOrigin:true},t.o));
      st.layer=ly;
      ly.on('tileload',function(){if(st.layer!==ly)return;st.ok++;if(st.ok===1){clearTimeout(st.timer);status('on','✅ 在线瓦片：'+t.n);window.__tileLog.push([data.id,t.id,'ok'])}});
      ly.on('tileerror',function(){if(st.layer!==ly)return;st.err++;if((st.ok===0&&st.err>=3)||st.err-st.ok>=8)fail('error')});
      st.timer=setTimeout(function(){if(st.layer===ly&&st.ok===0)fail('timeout')},T());
      ly.addTo(map);
    }
    function fail(why){var t=TILES[st.idx];window.__tileLog.push([data.id,t&&t.id,why]);if(sel.value==='auto')use(st.idx+1);else{clear();st.idx=-1;status('off','❌ '+(t?t.n:'')+' 不可用，已保留离线底图')}}
    function apply(){var v=sel.value;v==='auto'?use(0):v==='none'?use(-1):use(TILES.findIndex(function(t){return t.id===v}))}
    sel.value=g('otb.tiles')||'auto';if(![].some.call(sel.options,function(o){return o.value===sel.value}))sel.value='auto';
    sel.addEventListener('change',function(){s('otb.tiles',sel.value);apply()});apply();
    if(coarse){var hint=L.DomUtil.create('div','lhint',el);hint.textContent='👆 点按地图以启用拖动；双指缩放';map.once('click',function(){map.dragging.enable();hint.remove()})}
    map.on('focus click',function(){map.scrollWheelZoom.enable()});map.on('blur',function(){map.scrollWheelZoom.disable()});
    st.focus=function(i,pan){var m=mk[i];if(!m)return;if(pan)map.panTo(m.getLatLng(),{animate:!RM});m.openPopup()};
    return st;
  }).catch(function(e){console.warn(e);el.innerHTML='<p style="padding:20px">交互地图组件加载失败；请改用「🎨 概念示意图」或「🗺️ 真实地形图」（均离线可用）。</p>';return null});
}
function initMapbox(box){
  var raw=box.querySelector('.mdata');if(!raw)return;
  var data;try{data=JSON.parse(raw.textContent)}catch(e){return}
  var tabs=box.querySelectorAll('.mtabs [data-v]'),views={c:box.querySelector('.mv-c'),g:box.querySelector('.mv-g'),l:box.querySelector('.mv-l')};
  var info=box.querySelector('.minfo'),lis=box.querySelectorAll('.gm-leg li'),pins=box.querySelectorAll('.hs'),play=box.querySelector('.mplay');
  var live=box.__live||null,liveP=null,cur=box.__cur||-1,timer=0;
  function show(i,fromMap){
    var p=data.places[i];if(!p)return;cur=i;box.__cur=i;
    pins.forEach(function(x,j){x.classList.toggle('on',j===i)});
    lis.forEach(function(x,j){x.classList.toggle('on',j===i)});
    if(info){info.style.setProperty('--c',p.c);info.innerHTML='<div><b>'+p.i+' '+p.n+'</b> '+(p.en?'<i>'+p.en+'</i>':'')+' · <span class="d">'+p.w+'</span> · <span class="mut">'+(i+1)+' / '+data.places.length+'</span></div><div>'+p.d+'</div>'}
    if(live&&!fromMap&&views.l.classList.contains('on'))live.focus(i,true);
    if(fromMap!== 'skipg'){
      var hs=pins[i],v=box.querySelector('.gm-view');
      if(hs&&v&&views.g.classList.contains('on'))v.scrollTo({left:hs.offsetLeft-v.clientWidth/2,top:hs.offsetTop-v.clientHeight/2,behavior:RM?'auto':'smooth'});
    }
  }
  function view(v){
    tabs.forEach(function(t){var on=t.getAttribute('data-v')===v;t.classList.toggle('on',on);t.setAttribute('aria-selected',on)});
    Object.keys(views).forEach(function(k){if(views[k])views[k].classList.toggle('on',k===v)});
    if(v==='l'){
      if(box.__live&&box.__live.map){live=box.__live;setTimeout(function(){live.map.invalidateSize()},80);return}
      if(!box.__armLive)armLive(box,data,show);
      /* do not auto-start Leaflet during scroll or tab peek — user clicks the button */
    }
  }
  tabs.forEach(function(t){t.addEventListener('click',function(){view(t.getAttribute('data-v'))})});
  pins.forEach(function(p){p.addEventListener('click',function(){stop();show(+p.getAttribute('data-i'),'skipg')})});
  lis.forEach(function(li){li.addEventListener('click',function(){stop();show(+li.getAttribute('data-i'))});li.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();stop();show(+li.getAttribute('data-i'))}})});
  var gm=box.querySelector('.gmap-inner')||box;
  var inn=box.querySelector('.gm-in'),z=1;
  box.querySelectorAll('.gm-z button').forEach(function(b){b.addEventListener('click',function(){if(!inn)return;var k=+b.getAttribute('data-z');z=k===0?1:Math.max(1,Math.min(3,z+k*.5));inn.style.width=(z*100)+'%'})});
  function stop(){clearTimeout(timer);timer=0;if(play){play.classList.remove('on');play.textContent='▶ 按地点播放'}}
  if(play)play.addEventListener('click',function(){
    if(timer){stop();return}play.classList.add('on');play.textContent='⏸ 暂停';
    var k=0,step=function(){show(k);k++;timer=k<data.places.length?setTimeout(step,RM?2600:2000):0;if(!timer)setTimeout(stop,1600)};step();
  });
  var cmap=box.querySelector('.cmap');
  if(cmap&&'IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){cmap.classList.toggle('play',e.isIntersecting);if(e.isIntersecting)cmap.classList.add('seen')})},{rootMargin:'0px 0px -10% 0px'});io.observe(cmap)}
}
function armLive(box, data, show){
  var el=box.querySelector('.lmap');if(!el||el.dataset.armed)return;
  el.dataset.armed='1';el.dataset.idle='1';
  el.innerHTML='<div class="map-arm"><button type="button" class="ib" data-arm>📡 加载实时地图（多源瓦片，失败自动切换）</button><p>概念示意图与离线地形图已可离线使用。实时瓦片只在点击后加载，以免滚动时卡顿。</p></div>';
  var btn=el.querySelector('[data-arm]');
  function start(){
    el.removeAttribute('data-idle');el.textContent='🗺️ 地图加载中…';
    liveMap(box,data,function(i){show(i,true)}).then(function(s){box.__live=s||null;if(box.__live&&box.__cur>=0)box.__live.focus(box.__cur,false)});
  }
  if(btn)btn.addEventListener('click',start);
  box.__armLive=start;
}
/* cheap wiring now; Leaflet only after explicit click. Do not init during scroll. */
d.querySelectorAll('.mapbox').forEach(function(box){
  var raw=box.querySelector('.mdata');
  function wire(){
    if(box.dataset.ready)return;box.dataset.ready='1';
    initMapbox(box);
  }
  /* bind tabs immediately so first click works; initMapbox itself does not load Leaflet until live tab + arm */
  wire();
});
if('IntersectionObserver' in window){
  var playIO=new IntersectionObserver(function(es){es.forEach(function(e){e.target.classList.toggle('inview',e.isIntersecting);if(e.target.classList.contains('cmap'))e.target.classList.toggle('play',e.isIntersecting)})},{rootMargin:'0px',threshold:0.08});
  d.querySelectorAll('.film,.era,.mind,.cmap,.zones-film').forEach(function(x){playIO.observe(x)});
}
})();
