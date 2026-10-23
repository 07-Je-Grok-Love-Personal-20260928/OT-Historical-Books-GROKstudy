# -*- coding: utf-8 -*-
import json, re, html as H
from lib import *
import lib
CR = json.load(open(lib.CCI + "/creeds.json"))
def _intro(k): 
    t = CR[k].get("intro_text"); return t[0] if isinstance(t, list) else t
def cpq(k, part, note=""):
    """三大信经 CCI 介绍文字逐字引用"""
    t = _intro(k); assert part in t, (k, part)
    lib.USED.append(dict(key="CR-intro." + k, doc="CR", n=k, parts=[part], url=CR[k]["url"], label=CR[k]["title"] + " · 简介"))
    pre = "" if t.startswith(part) else "……"; post = "" if t.endswith(part) else "……"
    return (f'<blockquote class="cq reveal" data-k="CR-intro.{k}"><div class="cq-h">📜 {CR[k]["title"]} · CCI 简介 <span class="badge">CCI 逐字</span></div>'
            f'<div class="cq-t">{pre}{H.escape(part)}{post}</div><cite>出处：<a href="{CR[k]["url"]}" target="_blank" rel="noopener">{CR[k]["url"].replace("https://","")}</a>{note}</cite></blockquote>')
def lines(k, p):
    if k == "athanasian": return [x for x in re.split(r"(?<!\d)(?=\d+\) )", p) if x]
    return [x for x in re.split(r"(?<=[；。])(?=.)(?!阿们)", p) if x]
LAB = {"apostles": {0: "🅰️ 论圣父与我们的受造", 1: "🅱️ 论圣子与我们的得赎", 2: "🅲 论圣灵与我们的成圣"},
       "nicene": {0: "🅰️ 圣父", 1: "🅱️ 圣子：永恒的神性", 2: "🅱️ 圣子：道成肉身与救赎", 3: "🅲 圣灵", 4: "⛪ 教会 · 洗礼 · 盼望"},
       "athanasian": {0: "🚪 引言（1–2）", 1: "🔺 第一部分：三位一体（3–28）", 7: "✝️ 第二部分：道成肉身（29–41）", 12: "🔚 结语（42）"}}
def creed(k):
    t = CR[k]["text"]; ps = t.split("\n\n"); o = []; n = 0
    for i, p in enumerate(ps):
        if i in LAB[k]: o.append(f'<span class="art">{LAB[k][i]}</span>')
        ls = lines(k, p); assert "".join(ls) == p
        sp = []
        for l in ls:
            n += 1
            dn = f' data-n="{n}"' if k != "athanasian" else ""
            sp.append(f'<span class="ln"{dn}>{H.escape(l)}</span>')
        o.append(f'<div class="cp">{"".join(sp)}</div>')
    return (f'<div class="tools reveal"><button class="ib" data-recite="cr-{k}">🙈 背诵模式（遮盖）</button><button class="ib" data-big="cr-{k}" data-d="+">A＋</button><button class="ib" data-big="cr-{k}" data-d="-">A－</button>'
            f'<a class="ib" href="{CR[k]["url"]}" target="_blank" rel="noopener">🔗 CCI 原文</a></div><div class="creed" id="cr-{k}" data-creed="{k}">{"".join(o)}</div>')
def body():
    o = []
    o.append('''<section class="hero reveal"><div class="kick">THE THREE ECUMENICAL CREEDS · RECITATION EDITION</div><h1>✨ 三大普世信经 · 阅读背诵版</h1>
<p class="lead">《使徒信经》《尼西亚信经》《亚他那修信经》全文<b class="k">逐字</b>取自 ccifellowship.org《赞美诗集》信经部分，并由程序验证与原文完全一致。点击 <b>🙈 背诵模式</b> 遮盖全文，再逐行点击揭开自测；<b>A＋/A－</b> 调整字号。</p>
<div class="chips"><span class="chip">🅰️ 使徒信经 · 12 条</span><span class="chip">🅱️ 尼西亚信经 · 325/381</span><span class="chip">🅲 亚他那修信经 · 42 点</span></div></section>''')
    o.append(H2("cr-how", "🧠", "背诵方法", "var(--gold)"))
    o.append(story([("📖", "1 读", "先整段朗读 3 遍，注意分段标题（父—子—灵）"), ("🙈", "2 遮", "打开背诵模式，按行回忆，想不起来再点开"), ("🔗", "3 链", "用“三位一体骨架”串起：父造—子救—灵圣—教会—盼望"), ("⛪", "4 用", "在主日崇拜中与会众一同宣认；把条文与历史书故事挂钩")]))
    o.append(MEM('<p>三大信经都按<b class="k">三位一体</b>排列（海德堡第24问）：父（创造）→ 子（救赎）→ 灵（成圣）。背诵时先记这副骨架，再往里填细节。</p>'))
    o.append(cq("HC", 24))
    o.append(H2("cr-apostles", "🅰️", "使徒信经", "var(--gold)"))
    o.append(cpq("apostles", "这一信经被称为《使徒信经》，并不是因为它是使徒写的，而是因为它是对使徒教导所作的总结。"))
    o.append(creed("apostles"))
    o.append(mnem("父造 · 子降—难—死—活—升—坐—来 · 灵 · 会 · 赦 · 复 · 永", "使徒信经 12 条速记"))
    o.append(H2("cr-nicene", "🅱️", "尼西亚信经", "var(--blue)"))
    o.append(cpq("nicene", "《尼西亚信经》又称《尼西亚-君士坦丁堡信经》，它是早期基督教会的正统信仰告白，旨在驳斥某些异端，尤其是亚流主义。"))
    o.append(creed("nicene"))
    o.append(mnem("出于神且是神 · 出于光且是光 · 出于真神且是真神 · 受生却非被造 · 与父同质", "尼西亚核心五句——专门对付亚流“子是受造者”"))
    o.append(H2("cr-athanasian", "🅲", "亚他那修信经", "var(--purple)"))
    o.append(cpq("athanasian", "撇开信经的开头和结尾，《亚他那修信经》可以分为两个部分："))
    o.append(creed("athanasian"))
    o.append(mnem("位格不紊 · 本质不分 ‖ 神性不变 · 二性不混", "亚他那修信经两大支柱：前半防撒伯流/三神论，后半防基督论异端"))
    o.append(H2("cr-hist", "🔗", "信经条文 × 历史书", "var(--teal)"))
    o.append(table(["信经条文", "历史书中的伏笔", "说明"], [
        ["“创造天地的主”", "以利亚在迦密山（王上18）", "巴力号称掌管雨水，耶和华却是天地的创造主——三年不下雨就是宣告"],
        ["“神的独生子”", "撒下7:14 “我要作他的父，他要作我的子”", "大卫之约中的“子”最终应验在永恒的子（来1:5）"],
        ["“在本丢·彼拉多手下受难”", "历史书的“年代坐标”", "信仰扎根于真实历史：正如列王纪以列王年数纪年，福音也有确切的历史坐标"],
        ["“他的国没有穷尽”", "撒下7:16 “你的国必在我面前永远坚立”", "被掳时大卫王朝似乎断绝（王下25），信经宣告这国永存"],
        ["“他曾藉众先知说话”", "拿单、以利亚、以利沙、户勒大……", "历史书在希伯来正典中称为“前先知书”"],
        ["“圣而公之教会”", "以利亚时代的七千人（王上19:18）", "比利时信条第27条正是以此为例：教会有时人数稀少，却从未灭绝"],
        ["“身体复活 · 永生”", "约书亚、所罗门的“安息”不完全", "应许之地只是影子，指向新天新地（来4:8–9；11:16）"]]))
    return "".join(o)
