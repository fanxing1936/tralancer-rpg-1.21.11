# -*- coding: utf-8 -*-
"""图鉴「XVII 失乐园」一章，以及 XV 里的炼药、制器、遗物去处三节（数据读 add_paradise / potion_spec / world_loot_spec）。"""
import add_paradise as PL
import add_world_items as WI
import potion_spec as PS
import world_loot_spec as W
from guide_tutorial import _part, _steps, _table


def alchemy():
    rows = []
    for k, (name, tier, use, _c, _e, _f, line, _fl, rec, sp) in PS.POTIONS.items():
        tname, sef, souls, _st, cd = PS.TIER[tier]
        need = ["%s ×%d" % (PS.item_name(i), n) for i, n in rec]
        if souls:
            need.append("残魂 ×%d" % souls)
        if sp:
            need.append(WI.SPECIAL[sp][0] + " ×1")
        rows.append(("[%s]" % tname, "<span class=\"nm\">%s</span>" % name, PS.USE[use][1], line, "、".join(need), "%d 阶" % sef, "%d 秒" % cd))
    out = _part("w-alc", "炼药", "空瓶 · 灵魂营火", _steps([
        ("拿空瓶", "<p>铁匠 1 枚货币换 4 个，女巫 30% 掉 1 个；喝完饮用的药水会还一个。</p>", ""),
        ("炼", "<p>主手拿<b>空瓶</b>对灵魂营火右键，选药水，看清材料点「动手」。</p>", ""),
        ("别的来路", "<p>女巫 5% 勇者药水，首领 10% 史诗药水，悬赏全清送一瓶史诗药水，神秘商人每天带两种，失乐园里还有更多。同一档的药水共用冷却。</p>", ""),
    ]) + _table(["档", "药水", "用法", "效果", "配方（另需空瓶）", "原质", "冷却"], rows))
    rr = []
    for k, (name, _f, rec, sp, req) in PS.RITES.items():
        need = ["%s ×%d" % (PS.item_name(i), n) for i, n in rec] + ([WI.SPECIAL[sp][0] + " ×1"] if sp else [])
        rr.append(("<span class=\"nm\">%s</span>" % name, "空白圣具 ×1、" + "、".join(need), "原质 %d 阶" % req[1] if req[0] == "sef" else "裁决 %d 次" % req[1]))
    rr.append(("<span class=\"nm\">驱魔圣水</span>", "空瓶 ×1、恶魂之泪 ×1、海晶砂粒 ×4（在炼药页）", "原质 2 阶"))
    rr.append(("<span class=\"nm\">浓缩驱魔圣水</span>", "空瓶 ×1、驱魔圣水 ×2、圣殿铜 ×1（在炼药页）", "裁决 3 次"))
    out += _part("w-rite", "制器", "空白圣具 · 灵魂营火", "<p>主手拿<b>空白圣具</b>对灵魂营火右键。空白圣具来自圣卫（30%）、铁匠（8 枚货币）和悬赏（每条 10%）。</p>"
                 + _table(["器具", "配方", "要求"], rr))
    rel = [("<span class=\"nm\">%s</span>" % PS.item_name(i), u) for i, u in W.RELIC_USE.items()]
    out += _part("w-relic", "遗物的去处", "18 种", "<p>怪物掉的 <b>[遗物]</b> 还能当<a href=\"#s12\">契约祭品</a>与五职材料、上交悬赏；多余的卖给铁匠。</p>" + _table(["遗物", "用处"], rel))
    return out


def section():
    p = []
    a = p.append
    a('''<section class="plate" id="s19">
<div class="plate-h"><span class="num">XVII</span><h2>失乐园</h2><span class="sub">泥与血的维度 · 四座河庭 · 自由猎杀 · 宝库</span></div>
<p class="tut-lead">从玩家面板的「失乐园」页进出。落点是<strong>伊甸之门</strong>：一座四面敞开的金顶拱亭，四条石阶正对四座河庭。门里安全，有灵魂营火、铁匠，中庭是枯死的生命树。出了门就是猎场：怪物不燃烧、比主世界强，掉的也更多。</p>''')
    z = [("伊甸之门", "0 到 %d 格" % PL.GATE_R, "—", "—", "安全区")]
    far = [PL.GATE_R] + list(PL.ZONE_R)
    drop = {1: "多滚一次遗物", 2: "再加残魂、勇者药水、血泥", 3: "再加特殊材料、徽记、断羽"}
    for n, (name, hp, dmg, mul) in PL.ZONES.items():
        z.append((name, "%d 格起" % far[n - 1], "生命 +%d%%，伤害 +%d%%" % (hp * 100, dmg * 100), "%d 倍" % mul, drop[n]))
    a(_part("x-zone", "分区", "离门越远越强", _table(["区域", "离门", "怪物", "精英机率", "额外掉落"], z)
            + "<p>门外每分钟魔化 +1，圣力者改为生命力 −1。<b>血月</b>约 20 分钟一次，持续 3 分钟：怪更多，掉落翻倍。灰烬边境会出现持火剑的<b>基路伯</b>。"
              "死在里面会回到门内，虚弱 30 秒。门外离开要站着不动 5 秒。</p>"))
    rows = []
    for k, c in PL.COURTS.items():
        guard = {1: "一名首领", 2: "守关者", 3: "两名圣卫", 4: "随机一柱的五名罪仆"}[k]
        rows.append(("<span class=\"nm\">%s</span>" % c[0], "第 %d 到 %d 层" % ((k - 1) * 5 + 1, k * 5), "%d，每多一人 +%d" % (c[5], c[6]), "第 5 层：" + guard, "灾厄" if c[4] else "普通"))
    a(_part("x-court", "四座河庭", "离门 120 格，东南西北各一座", "<p>每座河庭正中是一座灰石大屋或高塔，小屋与小塔散在四周。大屋里有一座<b>祭坛</b>，刷怪笼在台顶，走近祭坛就开始。刷怪笼进冷却算过一层，歇 8 秒开下一层；五层打完发钥匙，大屋外面、河庭南边就是宝库。先过前一座才能进后一座。全员倒下或离开 60 秒，退回这一座的第一层。</p>"
            + _table(["河庭", "层数", "每层怪", "守关", "宝库"], rows)
            + "<p>每层阅历 3，守关层另加 12。第一次打完二十层得称号<b>登顶者</b>、阅历 50 和一张史诗图纸。</p>"))
    a(_part("x-vault", "宝库", "钥匙开启 · 宝物天降", _table(["普通 / 灾厄", "得到"], [
        ("1% / 1%", "樱怒之日（只在这里）"), ("4% / 6%", "随机传说图纸"), ("15% / 20%", "随机史诗图纸"),
        ("30% / 40%", "特殊材料、符文或符石"), ("50% / 30%", "史诗药水或养成材料包"), ("— / 3%", "传说药水")])
        + "<p>普通宝库一次落 1 件；灾厄宝库一次落 10 件，9 件按普通的表、1 件按灾厄的表。开完立刻重置，钥匙够就能再开。管理员站着执行 "
          "<code>/function rpg:pl/place/vault</code> 或 <code>vault_ominous</code> 可以另放，站在旧宝库上执行就是换锁。</p>"))
    a(_part("x-tree", "生命树与失乐园的遗物", "每天献一次", _table(["遗物", "来路", "献给生命树（一小时）", "卖给神秘商人"], [
        ("<span class=\"nm\">禁果</span>", "失乐园里的首领 15%", "攻击 +10%", "徽记 ×4"), ("<span class=\"nm\">血泥</span>", "血泽的怪 8%", "生命 +8", "徽记 ×1"),
        ("<span class=\"nm\">断羽</span>", "灰烬边境的怪 5%，基路伯必掉", "移速 +10%", "徽记 ×2")])))
    a(_part("x-fort", "黑石堡垒", "血泽与灰烬边境", "<p>原版地狱堡垒的布局换成黑石，离门约 300 格外才有。<b>桥面悬在离地约 100 格处</b>，柱子一直扎进泥里，掉下去就是深渊。走进堡垒会惊动<b>堡主</b>（每人每天一次），打倒给灾厄试炼之匙和徽记 ×5。里面是烈焰人与凋灵骷髅，宝箱给特殊材料、史诗药水、符文和钥匙，有 5% 出史诗图纸。</p>"))
    a("</section>")
    return "\n".join(p)
