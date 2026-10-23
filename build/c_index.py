# -*- coding: utf-8 -*-
from lib import *
import lib
BOOKS = [("约书亚记", "joshua.html#jos", "⚔️", "#ff6b5b", "1406–1375", "进入迦南，神信实赐地", "过河 · 夺城 · 分地 · 立约"),
         ("士师记", "judges.html#jdg", "🌀", "#ff9f43", "1375–1050", "没有王，各人任意而行", "犯罪→受罚→呼求→拯救→太平"),
         ("路得记", "judges.html#rut", "🌾", "#f2c14e", "约1150–1100", "黑暗时代的忠诚之爱", "空 → 拾 → 求 → 满"),
         ("撒母耳记上", "samuel.html#sam", "👑", "#a98bff", "1105–1010", "从撒母耳到扫罗，大卫受膏", "哈拿祷 · 以利倒 · 扫罗高"),
         ("撒母耳记下", "samuel.html#sam-cov", "📜", "#a98bff", "1010–970", "大卫作王与大卫之约", "大卫好 · 约坚牢 · 罪难逃"),
         ("列王纪上", "kings.html#kgs", "🏛️", "#2ed3c6", "970–853", "所罗门、分裂、以利亚", "荣 — 裂 — 火"),
         ("列王纪下", "kings.html#kgs-list", "🔥", "#2ed3c6", "853–561", "两国相继灭亡，大卫的灯", "亡 — 灯"),
         ("历代志上", "chronicles.html#chr", "🌳", "#5aa9ff", "亚当–970", "家谱与大卫预备建殿", "谱 · 卫"),
         ("历代志下", "chronicles.html#chr-vs", "📖", "#5aa9ff", "970–538", "圣殿与犹大诸王的复兴", "殿 · 王 · 上去"),
         ("以斯拉记", "return.html#ezr", "🧱", "#2ed3c6", "538–457", "重建圣殿与圣言之民", "诏 · 坛 · 基 · 阻 · 成"),
         ("尼希米记", "return.html#neh", "🏰", "#f2c14e", "445–432", "重建城墙与立约群体", "哭 · 修 · 读 · 约 · 改"),
         ("以斯帖记", "return.html#est", "👸", "#ff7eb6", "483–473", "隐藏的神，护理的手", "宴 · 谋 · 眠 · 翻 · 节")]
def body():
    o = []
    o.append('''<section class="hero reveal"><div class="kick">OLD TESTAMENT HISTORICAL BOOKS · CONTINENTAL REFORMED · GROKstudy 20261023-v1</div>
<h1>📜 旧约历史书深读<br><small style="font-size:.5em;opacity:.85">约书亚记 → 以斯帖记 · 欧陆改革宗正统视角</small></h1>
<p class="lead">十二卷书、一千年历史、一条主线：<b class="k">守约的神</b>把祂的百姓带进应许之地，赐他们君王与圣殿，又因他们背约而把他们赶出，最后带领余民归回——一切都在等候那位<b class="k">真约书亚、真大卫、真圣殿</b>：<b class="xr">耶稣基督</b>。</p>
<div class="chips"><span class="chip">📖 先整体后细节</span><span class="chip">🔗 圣约神学</span><span class="chip">🗺️ 7 幅真实地图</span><span class="chip">📜 三项联合信条逐字引用</span><span class="chip">✨ 三大信经背诵版</span><span class="chip">🧠 口诀 · 卡片 · 测验</span></div></section>''')
    o.append(H2("start", "🧭", "怎样使用本站", "var(--gold)"))
    o.append(flow([("① 整本圣经", "圣经神学与圣约神学的大框架", "var(--gold)"), ("② 史地文化", "年代、地理、列国、考古", "var(--green)"), ("③ 逐卷深读", "十二卷书：为什么写、写了什么、如何应用", "var(--red)")]))
    o.append(flow([("④ 信条对照", "三项联合信条与历史书的主题对照", "var(--teal)"), ("⑤ 三大信经", "背诵版与深度对比", "var(--purple)"), ("⑥ 速记自测", "口诀、翻卡、测验", "var(--blue)")]))
    o.append('<div class="legend"><span><b class="k">金色</b>＝重点</span><span><b class="h">红色波浪</b>＝难点</span><span><span class="d">蓝色</span>＝年代</span><span><span class="pl">绿色</span>＝地名</span><span><span class="pn">紫色</span>＝人物</span><span><b class="xr">粉色</b>＝指向基督</span></div>')
    o.append(H2("books", "📚", "十二卷历史书一览", "var(--red)"))
    o.append('<div class="grid" style="--min:250px">' + "".join(
        f'<a class="card bk reveal" href="{u}" style="--c:{c};text-decoration:none;color:inherit;position:relative"><span class="no">{i+1}</span><div class="ic">{e}</div><h4>{n}</h4><p><span class="d">主前 {d}</span></p><p>{t}</p><p style="opacity:.8;font-size:.9em">🧠 {m}</p></a>'
        for i, (n, u, e, c, d, t, m) in enumerate(BOOKS)) + '</div>')
    o.append(mnem("书士得 · 撒上下 · 王上下 · 代上下 · 拉尼斯", "十二卷历史书顺序（中文和合本）"))
    o.append(mnem("进 — 乱 — 王 — 分 — 亡 — 回", "约书亚记进迦南 · 士师记乱 · 撒母耳记立王 · 列王纪分裂与灭亡 · 以斯拉—以斯帖归回"))
    o.append(H2("arc", "🌈", "一千年的故事线", "var(--purple)"))
    o.append(era([("约书亚：征服", -1406, -1375, "#ff6b5b", "1406 过约旦河"), ("士师时代", -1375, -1050, "#ff9f43", "七轮循环"), ("统一王国", -1050, -931, "#a98bff", "扫罗 · 大卫 · 所罗门"),
                  ("北国以色列", -931, -722, "#ff7eb6", "722 撒玛利亚陷落"), ("南国犹大", -931, -586, "#3ccf8e", "586 圣殿被焚"), ("被掳巴比伦", -605, -538, "#8c97b2", "七十年"),
                  ("归回与重建", -538, -432, "#2ed3c6", "殿 · 律 · 墙 · 命")], -1450, -400, title="历史书总时间轴"))
    o.append(table(["阶段", "核心问题", "神的作为", "指向基督"], [
        ["进迦南（书）", "神的应许可信吗？", "为百姓争战、赐地", "真约书亚带我们进入安息（来4）"], ["士师（士、得）", "没有王会怎样？", "一再兴起拯救者；在伯利恒预备王的家族", "完全的拯救者，大卫的子孙"],
        ["立王（撒上下）", "怎样的王合神心意？", "拣选大卫，立永约", "大卫的子孙作王到永远（路1:32-33）"], ["分裂与灭亡（王上下）", "为什么被掳？", "照约审判，为大卫保留灯", "比所罗门更大的；带来新约"],
        ["回顾（代上下）", "我们还是神的百姓吗？", "从亚当起召聚子民；悔改得医治", "建造真殿的大卫之子"], ["归回（拉尼斯）", "应许会完全实现吗？", "激动外邦君王；隐藏地保守", "更荣耀的殿；第三天的反转"]]))
    o.append(H2("why", "💎", "为什么要读历史书？", "var(--teal)"))
    o.append(grid([card("它是真实的历史", "<p>救恩不是神话，而是神在时间与空间中的作为。历史书提供了从摩西到玛拉基的历史骨架。</p>", "📜", "var(--gold)"),
                   card("它是先知的书", "<p>希伯来圣经把约书亚记到列王纪称为“前先知书”：这是<b class='k'>先知式的历史解释</b>，用神的约来评价历史。</p>", "🗣️", "var(--blue)"),
                   card("它是为我们写的", "<p>“他们遭遇这些事都要作为鉴戒，并且写在经上，正是警戒我们这末世的人”（林前10:11）。</p>", "🪞", "var(--green)"),
                   card("它指向基督", "<p>“这经就是为我作见证的”（约5:39）。地、王、殿、归回——都是基督的影子。</p>", "✝️", "var(--pink)")], 240))
    o.append(KEY('<p><b>阅读原则（改革宗）：</b>① 唯独圣经（BC 7）——经文本身是最高权威；② 以经解经——历代志与列王纪互相参照；③ 救赎历史——每段历史在神的救恩计划中的位置；④ 基督中心——但不随意寓意化，先明白原意，再沿着圣约的线索走向基督。</p>'))
    o.append(cq("BC", 7, part="我们相信，圣经中包含了神全部的旨意；我们也相信它对人得救所必须信的一切真理作了充分的教导。"))
    return "".join(o)
