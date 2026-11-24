# -*- coding: utf-8 -*-
"""图鉴「XV 世界循环」一章：世界掉落、精英、罪器与图纸锻造、商人、事件、悬赏、支线、称号、卡巴拉来路。

表格里的名字和数字尽量直接读各生成器里的表（add_elites.AFFIX、add_events.EVENTS、add_quests.QUESTS……），
改了数据包重跑 emit_guide.py 就跟着变。
"""
import add_elites
import add_events
import add_forge_world
import add_quests
import add_world_items as WI
import world_loot_spec as W
from guide_tutorial import _part, _steps, _table

CLIP = {"undead": "亡灵", "arthropod": "节肢", "explosive": "爆裂", "arcane": "咒术", "nether": "下界", "end": "末地", "water": "水域"}


def _drops():
    rows = []
    for g, (name, mobs, raw, soul, blank, _cur) in W.GROUPS.items():
        prod = []
        for ds in mobs.values():
            for d in ds:
                if d[1] not in prod:
                    prod.append(d[1])
        raws = "、".join("%s %g%%" % (W.RAW[i][0], c * 100) for i, c, _a, _b in raw)
        rows.append((name, "、".join(W.MOB_NAME[m] for m in mobs), "、".join(prod) or "—", raws,
                     "残魂 %g%% · 器胚 %g%%" % (soul * 100, blank * 100), WI.SPECIAL[WI.GROUP_SP[g]][0]))
    return _table(["组", "怪物", "[遗物]", "[锻造] 原料", "养成材料", "首领的特殊材料"], rows)


def _weapons():
    rows = []
    for wid, name, tier, sp, _t in WI.WEAPONS:
        c = WI.COST[tier]
        rows.append((WI.TIER_TAG[tier], name, "%s ×%d、%s ×%d、器胚、残魂 ×%d" % (WI.SPECIAL[sp][0], c["sp"], c["main"][2], c["main"][1], c["souls"]),
                     "原质 %d 阶" % c["sef"]))
    return _table(["品级", "武器", "材料（另需这把武器的图纸）", "门槛"], rows)


def cards():
    import icons
    items = [("精英徽记", "elite_badge", "悬赏与商人的通用代币。精英掉 1 枚，首领掉 3 枚。"),
             ("图纸", "blueprint_legend", "写着一把史诗或传说武器的锻法。副手拿图纸、主手拿器胚，对灵魂营火右键。"),
             ("图纸碎片", "blueprint_fragment", "10 片换一张自选图纸。神秘商人用 6 枚徽记换一片。"),
             ("罪印碎片", "sin_shard", "同柱罪仆 30% 掉落。锻造那一柱的罪器要 8 片。")]
    src = {"star": "末地首领、事件「坠星」", "wind": "咒术首领", "tear": "水域首领、远古守卫者 50%", "core": "下界首领",
           "stone": "节肢与爆裂首领、地下的首领", "bronze": "圣卫 20%、支线「圣卫的遗言」", "soil": "亡灵首领"}
    items += [(v[0], v[1], "%s。%s。来路：%s，或神秘商人。" % (v[2][0], v[2][1], src[k])) for k, v in WI.SPECIAL.items()]
    out = []
    for name, model, text in items:
        out.append('<article class="card r-none" data-rarity="none" data-name="%s"><header class="card-h">%s<div class="card-id">'
                   '<h3>%s</h3><p class="base">世界材料</p></div></header><p class="flavour">%s</p></article>'
                   % (name, icons.img("minecraft:paper", alt=name, item_model="rpg:world/" + model), name, text))
    return "\n".join(out)


def section():
    p = []
    a = p.append
    a('''<section class="plate" id="s17">
<div class="plate-h"><span class="num">XV</span><h2>世界循环</h2><span class="sub">掉落 · 精英 · 锻造 · 商人 · 事件 · 支线</span></div>
<p class="tut-lead">野外的怪物掉原料和货币，精英掉徽记和图纸，魂火把它们锻成武器，商人和悬赏把多余的换成你缺的。
这一章写清楚每样东西<strong>从哪来、到哪去</strong>。原版合成表已经停用：装备只从魂火、掉落与奖励来。灵魂营火由地图放在固定的地方。</p>
<div class="note"><b>旅程：</b>玩家面板里的「旅程」页写着当前事件、今天的悬赏、支线进度、称号和配方书。</div>''')
    a(_part("w-drops", "怪物掉落", "玩家击杀才掉", _drops()))
    a(_part("w-elite", "精英与首领", "", _steps([
        ("什么会变成精英", "<p>野外怪物有 3% 的机会成为精英，原质越高机会越大（最高 8%），夜里再多一半。名字写在头顶：词缀小图标 + 花体英文名。"
                          "原质 6 阶起，五个精英里有一个是<b>首领</b>：两条词缀，有自己的血条，名字在血条下方。</p>", ""),
        ("掉什么", "<p>精英徽记 ×1（首领 ×3）、成堆的原料与残魂，另有机会掉器胚、养成材料、符文、符石；精英 1% 掉史诗图纸，首领再加一档，并掉本组的特殊材料。首领额外 +15 阅历。</p>", ""),
    ]) + _table(["词缀", "效果"], [(n, d) for _k, n, _c, d in add_elites.AFFIX])))
    a(_part("w-sin", "罪器锻造", "原质 %d 阶 · 锻成魔化 +%d" % (add_forge_world.SEF, add_forge_world.TAINT), _steps([
        ("备料", "<p>这一柱的<b>武器核心</b>（驱魔裁决选「消灭」）＋ 同柱罪仆掉的<b>罪印碎片 ×%d</b>（每名罪仆 30%%；七罪之仆锻自己那一柱只要 %d 片）＋ 下界合金锭（边缘者不用）＋ 器胚 ＋ 残魂 ×%d。</p>"
         % (add_forge_world.SHARDS, add_forge_world.SHARDS_OWN, add_forge_world.SOULS), ""),
        ("开炉", "<p>主手拿器胚对灵魂营火右键，在第一页点「罪器锻造」，选柱，开炉。</p>", ""),
    ])))
    a(_part("w-bp", "图纸锻造", "史诗与传说武器", _steps([
        ("拿到图纸", "<p>精英与首领掉落、Boss 首次击败、支线，或在奢侈品商人那里自选。<b>图纸碎片 ×10</b> 在锻造页换一张自选图纸，神秘商人用 6 枚徽记换一片。</p>", ""),
        ("锻造", "<p>主手拿器胚、<b>副手拿图纸</b>，对灵魂营火右键，点「按图纸锻造」。</p>", ""),
    ]) + _weapons()))
    a(_part("w-conv", "材料转换", "灵魂营火 · 锻造页「材料转换」", _table(["投入", "得到"], [
        ("、".join("%s ×%d" % (n, c) for _i, c, n in costs), out) for _k, _n, costs, _t, out in add_forge_world.CONV])))
    a(_part("w-mer", "商人", "原版交易界面", _table(["商人", "卖", "收", "在哪"], [
        ("铁匠", "铸造之石、洗炼钻、镀金箔、器胚", "铁锭、金锭和所有 [遗物]，换货币", "固定摆放"),
        ("神秘商人", "图纸碎片、特殊材料两种、罪印碎片、未立约契约书一柱（每天换一次货）", "精英徽记、货币", "固定摆放"),
        ("奢侈品商人", "自选史诗与传说图纸、全部符文与符石", "大量精英徽记与货币", "固定摆放"),
        ("迷途商人", "和神秘商人一样，但限量", "精英徽记、货币", "随机事件：白天，停 5 分钟"),
    ]) + '<p>七罪之仆买自己那一柱的契约书，成交后退一半。固定商人由管理员站在要放的位置执行 <code>/function rpg:merchant/place/smith</code>（<code>mystery</code>、<code>luxury</code>），'
         '<code>/function rpg:merchant/remove</code> 移走身边 4 格内的一位。</p>'))
    ev_body = {1: "夜里，原质 3 阶起：精英三倍、残魂更多；打倒 3 名首领得源质「基础」", 2: "原质 4 阶起：坠落处有三名精英守着星辰残片，守卫有 10% 的机会给源质「光辉」",
               3: "原质 5 阶起：一队罪仆路过", 4: "背钱袋的兔子，30 秒内打死它", 5: "附近的空缺者全部显形一分钟"}
    a(_part("w-ev", "随机事件", "约每 10 分钟一次", _table(["事件", "内容"],
            [(v[0], ev_body.get(k, "")) for k, v in add_events.EVENTS.items()] + [("迷途商人", "白天，附近来一位商人，停 5 分钟")])))
    a(_part("w-bt", "悬赏", "每天三条", '<p>从「%s」里每天抽三条。每条给货币 ×3、精英徽记和阅历 10；三条全做完再给一块铸造之石。累计 21 条得源质「王国」。</p>'
            % "、".join(b[0] for b in add_events.BOUNTIES.values())))
    how = {1: "踏上原质第 1 阶后自动接", 2: "第一次打倒亡灵首领后", 3: "第一次打倒圣卫后", 4: "第一次打死寻宝兔，或和神秘商人、迷途商人搭话", 5: "第一次完成坠星后", 6: "遇到事件「空缺者显现」", 7: "第一次进失乐园"}
    a(_part("w-q", "支线", "字幕在屏幕上方", _table(["支线", "怎么接", "要做什么"], [
        (q[0], how.get(k, ""), "；".join(s[0] for s in q[2])) for k, q in add_quests.QUESTS.items()])))
    a(_part("w-t", "称号与彩蛋", "戴上后图标显示在名字前面", _table(["称号", "怎么得到"], list(add_quests.TITLES.values()))))
    a(_part("w-kab", "卡巴拉物品的来路", "", _table(["物品", "来路"], [
        ("卡巴拉血契", "首次击败路西法"), ("王冠", "首次击败米迦勒"), ("智慧", "首次击败篡夺者"), ("理解", "支线「空缺者的名字」"), ("慈悲", "支线「圣卫的遗言」"),
        ("严厉", "首次击败扫罗"), ("美丽", "首次击败雅克"), ("胜利", "累计打倒 100 名精英"), ("光辉", "事件「坠星」的守卫，10%"),
        ("基础", "事件「罪潮之夜」里打倒 3 名首领"), ("王国", "野外怪物 0.1% 掉落，或累计 21 条悬赏"), ("真·十字架", "首次击败教皇"),
    ]) + '<p>Boss 给的几件，之后每次击败还有 20% 再给一件。七罪之仆在原质第 3 阶会在背包里得到自己领主的未立约契约书。</p>'))
    import guide_paradise
    a(guide_paradise.alchemy())
    a("</section>")
    return "\n".join(p)
