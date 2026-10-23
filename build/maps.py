# -*- coding: utf-8 -*-
"""旧约历史书地图：Natural Earth 公有领域底图（/workspace/ne），构建时预投影为静态 SVG（docs/assets/maps/*.svg），无 CDN。
地点坐标为通行考古/历史地理认定（多处为“约”）；古代海岸线（如波斯湾）与今日不同；路线为示意方向。"""
import os, html as H, re
import rmap
from rmap import PAL, ink
def M(k, n, en, lon, lat, y, t, c='blue', hl=False, ylab=False):
    return dict(k=k, n=n, en=en, ll=(lon, lat), y=y, t=t, c=c, hl=hl, ylab=ylab)
SPECS = {}
def S(**k): SPECS[k["id"]] = k; return k
# 1 征服迦南
S(id="conquest", title="约书亚征服迦南：过约旦河 → 中部 → 南方 → 北方", bbox=(34.15, 36.35, 30.95, 33.35), fine=True, fs=17,
  markers=[M("shi","什亭","Abel-shittim",35.66,31.84,"书2–3","摩押平原营地；探子由此出发去耶利哥。","gray"),
    M("gil","吉甲","Gilgal",35.50,31.85,"书4–5","过约旦河后第一营：立十二块石头、行割礼、守逾越节。","gold",True),
    M("jer","耶利哥","Jericho",35.44,31.87,"书6","绕城七日，城墙倒塌；喇合因信得救。","red",True),
    M("ai","艾城","Ai (et-Tell?)",35.26,31.92,"书7–8","因亚干取当灭之物而败；悔改后再战得胜。","orange"),
    M("ebal","以巴路山 · 示剑","Mt Ebal / Shechem",35.27,32.23,"书8:30–35; 24","筑坛、宣读祝福与咒诅；约书亚晚年在示剑立约。","purple",True),
    M("gib","基遍","Gibeon",35.18,31.85,"书9–10","基遍人用计立约；日头停留之战。","blue"),
    M("ajl","亚雅仑谷","Aijalon",35.02,31.84,"书10:12","“月亮啊，你要止在亚雅仑谷。”","blue"),
    M("lac","拉吉","Lachish",34.85,31.56,"书10:31–32","南方联军之一；第二日被攻取。","orange"),
    M("heb","希伯仑","Hebron",35.10,31.53,"书14; 15","迦勒八十五岁求得的山地。","green"),
    M("shl","示罗","Shiloh",35.29,32.06,"书18","会幕设立之地；在此拈阄分地。","gold"),
    M("haz","夏琐","Hazor",35.57,33.02,"书11","北方联盟之首，被火焚烧（考古见大火层，年代有争议）。","red")],
  routes=[("shi","gil","gold",.0),("gil","jer","red",.25),("jer","ai","orange",-.15),("gil","gib","blue",.2),("gib","lac","blue",.15),("gil","haz","red",-.18)],
  water=[("大海（地中海）",34.45,32.55),("盐海",35.62,31.35)], rcap="箭头为征服战役先后的示意方向（中部→南方→北方），不代表精确行军路线")
# 2 十二支派
S(id="tribes", title="十二支派分地（书13–21）与六座逃城", bbox=(34.15, 36.35, 30.95, 33.35), fine=True, fs=15,
  markers=[M("shl","示罗（会幕）","Shiloh",35.29,32.06,"书18:1","会众聚集，支起会幕，七支派在此拈阄。","gold",True),
    M("ked","基低斯","Kedesh",35.53,33.11,"逃城","拿弗他利山地的逃城（书20:7）。","red"),
    M("she","示剑","Shechem",35.28,32.21,"逃城","以法莲山地的逃城。","red"),
    M("heb","希伯仑","Hebron",35.10,31.53,"逃城","犹大山地的逃城（基列亚巴）。","red"),
    M("bez","比悉","Bezer",35.86,31.62,"逃城 · 约","约旦河东、旷野平原，属流便。","red"),
    M("ram","基列的拉末","Ramoth-gilead",35.85,32.52,"逃城 · 约","属迦得。","red"),
    M("gol","哥兰","Golan",35.83,32.86,"逃城 · 约","巴珊的逃城，属玛拿西。","red")],
  regions=[("流便",35.78,31.62,.16,.2,"teal"),("迦得",35.72,32.15,.17,.25,"teal"),("玛拿西（东半）",35.95,32.72,.25,.22,"teal"),
    ("犹大",34.98,31.42,.32,.22,"gold"),("西缅",34.72,31.17,.2,.12,"orange"),("便雅悯",35.30,31.84,.13,.07,"pink"),
    ("但（原分地）",34.88,31.92,.13,.1,"purple"),("以法莲",35.18,32.10,.2,.09,"green"),("玛拿西（西半）",35.12,32.40,.25,.14,"green"),
    ("以萨迦",35.45,32.62,.13,.09,"blue"),("西布伦",35.25,32.76,.11,.07,"blue"),("亚设",35.18,33.02,.12,.2,"purple"),("拿弗他利",35.50,32.98,.1,.22,"orange")],
  water=[("大海",34.45,32.6)], rcap="支派范围为示意椭圆（按书13–19的大致方位），边界不精确；逃城见书20")
# 3 士师与路得
S(id="judges", title="士师时代与路得记：拯救者、迁移与回归", bbox=(34.15, 36.35, 30.95, 33.35), fine=True, fs=16,
  markers=[M("tab","他泊山","Mt Tabor",35.39,32.69,"士4–5","底波拉与巴拉克在此集结，基顺河大败西西拉。","purple",True),
    M("har","哈律泉","Spring of Harod",35.36,32.55,"士7","基甸三百人在此被拣选。","green",True),
    M("miz","基列的米斯巴","Mizpah of Gilead",35.75,32.30,"士11","耶弗他被立为首领；轻率许愿。","orange"),
    M("jer","棕树城（耶利哥）","Jericho",35.44,31.87,"士3:13","摩押王伊矶伦占据此地；以笏刺杀伊矶伦。","blue"),
    M("zor","琐拉","Zorah",34.98,31.77,"士13","参孙出生之地（但支派）。","red"),
    M("tim","亭拿","Timnah",34.91,31.78,"士14","参孙娶非利士女子。","red"),
    M("gaz","迦萨","Gaza",34.46,31.50,"士16","参孙拆毁大衮庙，与非利士人同死。","red",True),
    M("dan","但（拉亿）","Dan / Laish",35.65,33.25,"士18","但人北迁，立米迦的雕像——私设敬拜。","gray"),
    M("gib","基比亚","Gibeah",35.23,31.82,"士19–21","利未人的妾受辱，内战几乎灭绝便雅悯。","gray"),
    M("bet","伯利恒","Bethlehem",35.20,31.70,"得1–4","以利米勒一家离开饥荒；路得随拿俄米归回，嫁波阿斯。","gold",True),
    M("moa","摩押地","Moab",35.75,31.35,"得1","以利米勒寄居之地；路得的故乡。","pink")],
  routes=[("bet","moa","gray",.15),("moa","bet","gold",.15),("zor","dan","purple",-.2)],
  water=[("大海",34.45,32.6),("盐海",35.55,31.45)], rcap="灰色：以利米勒去摩押；金色：拿俄米与路得归回伯利恒；紫色：但人北迁")
# 4 撒母耳记
S(id="samuel", title="撒母耳记：约柜的旅程、扫罗与大卫", bbox=(34.25, 36.0, 31.05, 32.85), fine=True, fs=16,
  markers=[M("shl","示罗","Shiloh",35.29,32.06,"撒上1–4","撒母耳在此长大；以利家衰败。","gold"),
    M("aph","亚弗 · 以便以谢","Aphek / Ebenezer",34.93,32.10,"撒上4","以色列战败，约柜被掳。","gray"),
    M("ash","亚实突","Ashdod",34.65,31.80,"撒上5","大衮倒在约柜前。","red"),
    M("bsh","伯示麦","Beth-shemesh",34.98,31.75,"撒上6","母牛直行把约柜送回。","orange"),
    M("kj","基列耶琳","Kiriath-jearim",35.10,31.81,"撒上7; 撒下6","约柜停放约二十年，后由大卫迎往耶路撒冷。","orange"),
    M("ram","拉玛","Ramah",35.23,31.85,"撒上7–8","撒母耳的家；百姓求立王。","gold"),
    M("gib","基比亚","Gibeah of Saul",35.23,31.82,"撒上10–15","扫罗的王城。","purple"),
    M("mic","密抹","Michmash",35.28,31.87,"撒上14","约拿单攀崖突袭非利士营。","purple"),
    M("ela","以拉谷","Valley of Elah",34.97,31.68,"撒上17","大卫击杀歌利亚。","green",True),
    M("gat","迦特","Gath",34.85,31.70,"撒上21; 27","歌利亚的城；大卫两度投奔亚吉。","red"),
    M("zik","洗革拉","Ziklag",34.80,31.40,"撒上27–30","亚吉赐给大卫的城。","green"),
    M("eng","隐基底","En-gedi",35.39,31.46,"撒上24","大卫在洞中割下扫罗衣襟。","green"),
    M("glb","基利波山","Mt Gilboa",35.41,32.45,"撒上31","扫罗与约拿单阵亡。","purple",True),
    M("heb","希伯仑","Hebron",35.10,31.53,"撒下2–5","大卫作犹大王七年半。","green"),
    M("jeru","耶路撒冷","Jerusalem",35.23,31.78,"撒下5–7","大卫攻取锡安保障，迎约柜，得大卫之约。","gold",True),
    M("mah","玛哈念","Mahanaim",35.67,32.18,"撒下17","押沙龙叛乱时大卫退到此地。","blue")],
  routes=[("aph","ash","gray",.15),("ash","bsh","orange",.2),("bsh","kj","orange",-.3),("kj","jeru","gold",-.3),("heb","jeru","green",.2)],
  water=[("大海",34.45,32.5),("盐海",35.52,31.35)], rcap="约柜旅程（灰→橙→金）：亚弗→亚实突（另经迦特、以革伦）→伯示麦→基列耶琳→耶路撒冷；绿色：大卫从希伯仑到耶路撒冷")
# 5 分裂王国
S(id="divided", title="分裂王国：北国以色列与南国犹大（主前931–586）", bbox=(33.9, 37.0, 30.7, 34.0), fine=True, fs=16,
  markers=[M("jeru","耶路撒冷","Jerusalem",35.23,31.78,"南国首都","大卫王朝、圣殿所在；主前586年被巴比伦焚毁。","gold",True),
    M("she","示剑","Shechem",35.28,32.21,"王上12","罗波安在此拒绝民意，十个支派分裂。","gray"),
    M("bet","伯特利","Bethel",35.22,31.93,"王上12:29","耶罗波安所立金牛犊之一（南端）。","red",True),
    M("dan","但","Dan",35.65,33.25,"王上12:29","另一只金牛犊（北端）。","red",True),
    M("tir","得撒","Tirzah",35.35,32.29,"王上14–16","北国早期王城。","purple"),
    M("sam","撒玛利亚","Samaria",35.19,32.28,"王上16:24","暗利所建北国首都；主前722年陷落于亚述。","purple",True),
    M("car","迦密山","Mt Carmel",35.08,32.67,"王上18","以利亚与巴力先知对决：“耶和华是神！”","orange",True),
    M("jez","耶斯列","Jezreel",35.33,32.56,"王上21; 王下9","拿伯的葡萄园；耶户除灭亚哈家。","purple"),
    M("meg","米吉多","Megiddo",35.18,32.59,"王下23:29","约西亚战死于法老尼哥之手（主前609）。","gray"),
    M("lac","拉吉","Lachish",34.85,31.56,"王下18:14","西拿基立围攻（主前701），亚述宫墙浮雕所刻。","red"),
    M("dam","大马士革","Damascus",36.29,33.51,"亚兰","亚兰首都；以利沙、乃缦、哈薛的故事。","blue"),
    M("tyr","推罗","Tyre",35.20,33.27,"腓尼基","希兰为所罗门供应香柏木；耶洗别出自西顿人。","teal"),
    M("zar","撒勒法","Zarephath",35.30,33.45,"王上17","以利亚与寡妇的面和油。","orange"),
    M("rg","基列的拉末","Ramoth-gilead",35.85,32.52,"王上22","亚哈战死；耶户在此受膏。","blue")],
  regions=[("北国以色列（十支派）",35.45,32.55,.55,.45,"purple"),("南国犹大",35.05,31.5,.42,.3,"gold")],
  water=[("大海",34.3,32.8),("盐海",35.55,31.4)], rcap="两国范围为示意椭圆，边界随时代变动")
# 6 帝国与被掳归回
S(id="empires", title="古近东帝国：被掳与归回的路线（主前722–445）", bbox=(28.5, 56.0, 23.5, 39.5), fs=19,
  markers=[M("jeru","耶路撒冷","Jerusalem",35.23,31.78,"586 / 538","南国被掳与归回的中心。","gold",True),
    M("sam","撒玛利亚","Samaria",35.19,32.28,"722","北国陷落，居民被掳往亚述，外族被迁入。","purple"),
    M("nin","尼尼微","Nineveh",43.15,36.36,"612 亡","亚述首都；主前612年被巴比伦与米底攻陷。","red",True),
    M("goz","歌散（哈博河）","Gozan",40.04,36.83,"王下17:6","北国被掳者被安置之地之一。","red"),
    M("car","迦基米施","Carchemish",38.01,36.83,"605","尼布甲尼撒击败埃及，称霸西亚。","gray"),
    M("rib","利比拉","Riblah",36.55,34.45,"586","西底家在此被剜眼；巴比伦王的前线大营。","gray"),
    M("bab","巴比伦","Babylon",44.42,32.54,"605–539","南国被掳之地；主前539年被波斯古列攻取。","orange",True),
    M("nip","尼普尔（迦巴鲁河）","Nippur",45.23,32.13,"结1","以西结与被掳者住在迦巴鲁河边（附近）。","orange"),
    M("sus","书珊","Susa",48.26,32.19,"斯; 尼1","波斯王宫；以斯帖与尼希米的舞台。","green",True),
    M("ecb","亚马他（埃克巴他拿）","Ecbatana",48.52,34.80,"拉6:2","在此宫中找到古列的诏书。","green"),
    M("per","波斯波利斯","Persepolis",52.89,29.93,"大流士起","波斯礼仪首都。","green"),
    M("mem","孟斐斯","Memphis",31.25,29.85,"埃及","下埃及首都；约西亚之死与埃及势力（法老尼哥）。","blue"),
    M("dam","大马士革","Damascus",36.29,33.51,"732","亚述攻陷亚兰。","blue")],
  routes=[("sam","goz","red",-.12),("jeru","bab","orange",.34),("bab","jeru","gold",-.12),("sus","jeru","green",.18)],
  regions=[("亚述",43.0,36.0,2.2,1.4,"red"),("巴比伦尼亚",45.2,31.6,2.0,1.4,"orange"),("米底",49.5,35.6,2.6,1.6,"teal"),("波斯（帕尔斯）",53.0,29.8,2.4,1.6,"green"),("埃及",31.0,27.5,2.2,2.6,"blue")],
  water=[("大海（地中海）",31.5,33.6),("波斯湾",51.2,27.4),("红海",36.0,24.8)],
  rcap="红：北国被掳往亚述（722）；橙：南国被掳往巴比伦（605、597、586，沿肥沃月湾北绕）；金：所罗巴伯（538）与以斯拉（458）归回；绿：尼希米从书珊回耶路撒冷（445）。古代波斯湾海岸线比今日更靠西北")
# 7 波斯帝国（以斯帖）
S(id="persia", title="以斯帖记的世界：“从印度直到古实”的波斯帝国（斯1:1）", bbox=(22.0, 74.0, 12.0, 44.5), fs=21,
  markers=[M("sus","书珊城堡","Susa",48.26,32.19,"斯1–10","亚哈随鲁（薛西一世）的冬宫；普珥节的起源。","green",True),
    M("per","波斯波利斯","Persepolis",52.89,29.93,"礼仪首都","大流士与薛西建造的宫殿群。","green"),
    M("ecb","埃克巴他拿","Ecbatana",48.52,34.80,"夏宫","米底旧都。","teal"),
    M("bab","巴比伦","Babylon",44.42,32.54,"省会","许多犹太人仍留在此地。","orange"),
    M("sar","撒狄","Sardis",28.04,38.49,"西端","吕底亚省会；薛西远征希腊的集结地（主前480）。","purple"),
    M("jeru","耶路撒冷","Jerusalem",35.23,31.78,"河西省","重建后的圣殿（主前516）所在。","gold",True),
    M("mem","孟斐斯","Memphis",31.25,29.85,"埃及省","波斯治下的埃及。","blue")],
  regions=[("印度（印度河流域）",69.5,27.0,3.2,4.0,"pink"),("古实（努比亚）",32.5,18.5,3.0,3.5,"orange")],
  water=[("地中海",19.0,35.0),("波斯湾",51.5,26.8),("阿拉伯海",63.0,20.0)],
  rcap="斯1:1 一百二十七省；粉色与橙色示意帝国的东西（南）两端")
def build(outdir, ver):
    os.makedirs(outdir, exist_ok=True); out = {}
    for k, sp in SPECS.items():
        W = 1000 if sp["bbox"][1]-sp["bbox"][0] < 10 else 1200
        svg, w, h, hs = rmap.real_svg(sp, W)
        # 动态：路线虚线流动（SVG 内 CSS；尊重减少动态）
        svg = svg.replace('</defs>', '</defs><style>path[marker-end]{animation:fl 1.6s linear infinite}@keyframes fl{to{stroke-dashoffset:-26}}@media (prefers-reduced-motion:reduce){path[marker-end]{animation:none}}</style>', 1)
        open(os.path.join(outdir, k + ".svg"), "w").write(svg)
        out[k] = (sp, w, h, hs)
    return out
def html(k, built, ver):
    sp, w, h, hs = built[k]
    t = H.escape(sp["title"])
    hsb = "".join(f'<button class="hs" style="left:{x:.2f}%;top:{y:.2f}%" data-i="{i}" aria-label="{i+1} {H.escape(m["n"])}"></button>' for i, (m, (x, y)) in enumerate(hs))
    li = "".join(f'<li data-i="{i}" tabindex="0" style="--c:{PAL[m.get("c","blue")]};--t:{ink(PAL[m.get("c","blue")])}"><b>{i+1}</b><span><strong>{H.escape(m["n"])}</strong> <i>{H.escape(m["en"])}</i> · <em>{H.escape(m["y"])}</em>：{H.escape(m["t"])}</span></li>' for i, m in enumerate(sp["markers"]))
    return (f'<figure class="gmap" id="map-{k}"><div class="gm-bar"><span>🗺️ {t}</span><span class="gm-z"><button data-z="-1" aria-label="缩小">－</button><button data-z="0" aria-label="复位">⟲</button><button data-z="1" aria-label="放大">＋</button></span></div>'
            f'<div class="gm-view"><div class="gm-in" style="aspect-ratio:{w}/{h}"><img src="assets/maps/{k}.svg?v={ver}" width="{w}" height="{h}" loading="lazy" decoding="async" alt="{t}">{hsb}</div></div>'
            f'<figcaption>真实地形底图：Natural Earth（公有领域），本站绘制；地点为通行历史地理认定（部分为“约”）。{H.escape(sp.get("rcap",""))}。点编号或下方列表可高亮地点。</figcaption><ol class="gm-leg">{li}</ol></figure>')
