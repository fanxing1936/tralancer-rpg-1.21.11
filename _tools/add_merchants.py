# -*- coding: utf-8 -*-
"""商人（策划书「商人」一节；用户 2026-11-24：模型用地下城的商人村民，步骤放在最终测试前）。

    python add_merchants.py ../rpg

* 铁匠、神秘商人、奢侈品商人：管理员站在要放的地方执行 rpg:merchant/place/<名> 放下（和固定的灵魂营火一样由地图决定位置）。
  迷途商人：第 6 种随机事件（白天），在玩家附近出现 5 分钟，货和神秘商人一样。
* 载体是不会走的村民（原版交易界面，冒险模式可用），名牌是花体英文；外观是 Codex 按 docs/MERCHANT-MODELS-PROMPT.md
  做的地下城商人村民（add_merchant_models.py 生成的 rpg:merchant_<名>/dress），交付前先用原版村民的样子。
* 交易里的物品与掉落表同一格式（[货币]、[锻造]、图纸……），从各自的掉落表里读组件，保证格式一致。
* 接线：神秘商人那里接「玛门的账本」；用金锄敲商人三下 → 彩蛋「被商人记恨」。
"""
import io
import json
import os
import re
import sys

import rpg_ui_style as ui

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data", "rpg", "function")
LOOT = os.path.join(DP, "data", "rpg", "loot_table")
P = "rpg:merchant"
COUNT = 0
HERE = os.path.dirname(os.path.abspath(__file__))

MERCHANTS = {  # 名: (英文, 村民职业, 花体名)
    "smith": ("Blacksmith", "weaponsmith"),
    "mystery": ("Mystery Merchant", "cleric"),
    "luxury": ("Luxury Merchant", "librarian"),
    "travel": ("Travelling Merchant", "cartographer"),
}


def fn(name, lines):
    global COUNT
    path = os.path.join(FUNC, "merchant", name + ".mcfunction")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    COUNT += 1


def wj(path, doc):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def J(o):
    return json.dumps(o, ensure_ascii=False, separators=(",", ":"))


def seg(text, colour, bold=False):
    return {"text": text, "color": colour, "bold": bold, "italic": False}


def read(rel):
    return io.open(os.path.join(FUNC, rel), encoding="utf-8").read()


def write(rel, s):
    io.open(os.path.join(FUNC, rel), "w", encoding="utf-8", newline="\n").write(s)


def patch(rel, guard, text, where="end"):
    s = read(rel)
    if guard in s:
        return
    if where == "end":
        s = s.rstrip("\n") + "\n" + text
    else:
        assert where in s, (rel, where)
        s = s.replace(where, text + where, 1)
    write(rel, s)


# ============================================================================ 物品：从掉落表读组件 → SNBT
def snbt(v):
    if isinstance(v, dict):
        return "{" + ",".join("%s:%s" % (json.dumps(k), snbt(x)) for k, x in v.items()) + "}"
    if isinstance(v, list):
        return "[" + ",".join(snbt(x) for x in v) + "]"
    if isinstance(v, bool):
        return "1b" if v else "0b"
    if isinstance(v, (int, float)):
        return str(v)
    return json.dumps(v, ensure_ascii=False)


def entry_of(table):
    """loot 表（rpg:...）第一个物品条目 → (id, 组件 SNBT)；loot_table 引用会跟进去。"""
    ns, path = table.split(":", 1)
    doc = json.load(io.open(os.path.join(DP, "data", ns, "loot_table", path + ".json"), encoding="utf-8"))
    e = doc["pools"][0]["entries"][-1]
    if e.get("type", "").endswith("loot_table"):
        return entry_of(e["value"])
    return item_of(e)


def item_of(e):
    comps, data = {}, None
    for f in e.get("functions", []):
        k = f.get("function", "").replace("minecraft:", "")
        if k == "set_components":
            comps.update(f["components"])
        elif k == "set_name":
            comps["minecraft:custom_name"] = f["name"]
        elif k == "set_lore":
            comps["minecraft:lore"] = f["lore"]
        elif k == "set_custom_data":
            data = f["tag"]
    body = ",".join("%s:%s" % (json.dumps(k), snbt(v)) for k, v in comps.items())
    if data:
        body += (",%s:%s" % (json.dumps("minecraft:custom_data"), data)) if body else "%s:%s" % (json.dumps("minecraft:custom_data"), data)
    return e["name"], "{" + body + "}"


def sell(table, count=1):
    iid, comps = entry_of(table)
    return "{id:\"%s\",count:%d,components:%s}" % (iid, count, comps)


def currency_item(count=1):
    tpl = json.load(io.open(os.path.join(HERE, "world_loot_currency.json"), encoding="utf-8"))
    iid, comps = item_of(tpl["entries"][1])
    return "{id:\"%s\",count:%d,components:%s}" % (iid, count, comps)


def cost_currency(n):
    return "{id:\"minecraft:raw_gold\",count:%d,components:{\"minecraft:custom_data\":{currency_tag:1b}}}" % n


def cost_badge(n):
    """徽记只有一个来源，价钱格里写全组件（图标、名字和掉落的一样）；货币来源多、旧存档也有，只认 custom_data。"""
    iid, comps = entry_of("rpg:elite/badge")
    return "{id:\"%s\",count:%d,components:%s}" % (iid, n, comps)


def cost_plain(item, n):
    return "{id:\"minecraft:%s\",count:%d}" % (item, n)


def offer(buy, out, buy_b=None, uses=999):
    b = (",buyB:%s" % buy_b) if buy_b else ""
    return "{buy:%s%s,sell:%s,maxUses:%d,rewardExp:0b,xp:0,priceMultiplier:0f,specialPrice:0,demand:0}" % (buy, b, out, uses)


# ============================================================================ 货单
BUY = [  # 铁匠收的 [货币] 类原版产物：(物品, 几个换 1 枚货币)，常见的要得多
    ("rotten_flesh", 32), ("bone", 32), ("arrow", 32), ("string", 24), ("spider_eye", 12), ("gunpowder", 16),
    ("redstone", 24), ("glowstone_dust", 24), ("breeze_rod", 8), ("blaze_powder", 16), ("ghast_tear", 4),
    ("magma_cream", 12), ("ender_pearl", 8), ("shulker_shell", 4), ("phantom_membrane", 8),
    ("prismarine_shard", 24), ("prismarine_crystals", 16)]
BOOK_BADGE, BOOK_CURRENCY = 20, 30  # 未立约契约书的价钱
SP_KEEP = 2                         # 神秘 / 迷途商人每次带几种特殊材料


def check_buy():
    """铁匠必须收齐 world_loot_spec 里每种 [货币] 产物。"""
    import world_loot_spec as W
    drops = set(d[0] for _n, mobs, *_r in W.GROUPS.values() for ds in mobs.values() for d in ds)
    missing = drops - set(i for i, _n in BUY)
    if missing:
        raise SystemExit("merchants: 铁匠没收 %s" % sorted(missing))


def offers(kind, pillar=None):
    import add_world_items as WI
    if kind == "smith":
        return [offer(cost_currency(10), sell("rpg:forge/item/forge_stone")),
                offer(cost_currency(12), sell("rpg:forge/item/wash_gem")),
                offer(cost_currency(8), sell("rpg:forge/item/gild_leaf")),
                offer(cost_currency(6), sell("rpg:forge/item/blank")),
                offer(cost_plain("iron_ingot", 24), currency_item(2)),
                offer(cost_plain("gold_ingot", 8), currency_item(3))] + [
                offer(cost_plain(item, n), currency_item(1)) for item, n in BUY]
    if kind in ("mystery", "travel"):
        out = [offer(cost_badge(6), sell("rpg:world/bp_fragment"), uses=8)]
        for k in WI.SPECIAL:
            out.append(offer(cost_badge(15), sell("rpg:world/sp/" + k), uses=1))
        out.append(offer(cost_currency(10), sell("rpg:world/sin_shard_%d" % pillar), uses=4))
        out.append(offer(cost_badge(BOOK_BADGE), pact_book(pillar), buy_b=cost_currency(BOOK_CURRENCY), uses=1))
        return out
    if kind == "luxury":
        out = []
        for w in WI.WEAPONS:
            if w[2] == "epic":
                out.append(offer(cost_badge(40), sell("rpg:world/bp/" + w[0]), buy_b=cost_currency(20)))
        for w in WI.WEAPONS:
            if w[2] == "legend":
                out.append(offer(cost_badge(64), sell("rpg:world/bp/" + w[0]), buy_b=cost_currency(40)))
        for name in sorted(os.listdir(os.path.join(LOOT, "forge", "item"))):
            stem = name[:-5]
            if stem.startswith("rune_"):
                out.append(offer(cost_badge(20), sell("rpg:forge/item/" + stem), buy_b=cost_currency(10)))
            elif stem.startswith("stone_"):
                out.append(offer(cost_badge(25), sell("rpg:forge/item/" + stem), buy_b=cost_currency(10)))
        return out
    raise KeyError(kind)


def pact_book(n):
    """未立约契约书：读驱魔「契约」结局的 give 行（同一件）。"""
    line = read("inquest/give/pact%d.mcfunction" % n).strip().splitlines()[-1]
    head, rest = line.split(" ", 2)[2].split("[", 1)
    comps = rest.rsplit("]", 1)[0]
    iid = head if ":" in head else "minecraft:" + head
    return "{id:\"%s\",count:1,components:{%s}}" % (iid, split_components(comps))


def split_components(s):
    out, depth, cur, parts = [], 0, "", []
    instr = False
    for ch in s:
        if ch == '"' and (not cur or cur[-1] != "\\"):
            instr = not instr
        if not instr:
            if ch in "[{":
                depth += 1
            elif ch in "]}":
                depth -= 1
        if ch == "," and depth == 0 and not instr:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    parts.append(cur)
    for p in parts:
        k, v = p.split("=", 1)
        out.append("%s:%s" % (json.dumps(k if ":" in k else "minecraft:" + k), v))
    return ",".join(out)


# ============================================================================ 放置
def place():
    import add_world_items as WI
    for k, (en, prof) in MERCHANTS.items():
        # 载体隐身，原版不给隐身实体画名牌 → 名牌是骑在身上的文字展示；CustomName 只当交易界面标题
        # （用原版标题的深灰；level 6 让标题后面不带「大师」）
        name = J(["", seg(ui.fraktur(en), "#404040")])
        plate = ("summon minecraft:text_display ~ ~ ~ {Tags:[\"rpg.mer.plate\",\"rpg.mer.pnew\"],billboard:\"center\",text:%s,"
                 "transformation:{translation:[0f,0.62f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f]}}"
                 % J(["", seg(ui.fraktur(en), ui.WHITE)]))
        variants = [None] if k in ("smith", "luxury") else [p["n"] for p in ui.PILLARS]
        for v in variants:
            rec = offers(k, v)
            if k != "travel":  # 常驻商人不会补货，所有玩家共用一份货 → 不限次数；只有迷途商人限量
                rec = [re.sub(r"maxUses:\d+", "maxUses:999", r) for r in rec]
            nbt = ("{Tags:[\"rpg.mer\",\"rpg.mer.%s\",\"rpg.vac.seen\",\"rpg.mer.new\"],NoAI:1b,Silent:0b,PersistenceRequired:1b,"
                   "Invulnerable:1b,CanPickUpLoot:0b,CustomNameVisible:0b,CustomName:%s,VillagerData:{type:\"minecraft:plains\","
                   "profession:\"minecraft:%s\",level:6},Offers:{Recipes:[%s]},"
                   "active_effects:[{id:\"resistance\",duration:-1,amplifier:4,show_particles:0b},{id:\"regeneration\",duration:-1,amplifier:2,show_particles:0b}]}"
                   % (k, name, prof, ",".join(rec)))
            stem = "spawn_%s" % k + ("" if v is None else "_%d" % v)
            # 外观：add_merchant_models.py 的 tick 会给带 rpg.mer.<名> 的村民自动换上地下城商人模型
            lines = ["summon minecraft:villager ~ ~ ~ %s" % nbt, plate,
                     "ride @e[type=minecraft:text_display,tag=rpg.mer.pnew,limit=1] mount @e[type=minecraft:villager,tag=rpg.mer.new,limit=1]",
                     "tag @e[type=minecraft:text_display,tag=rpg.mer.pnew] remove rpg.mer.pnew",
                     "rotate @e[type=minecraft:villager,tag=rpg.mer.new,limit=1] ~ 0"]
            if v is not None:  # 特殊材料随机留两种：七种排在第 1..7 条（第 0 条是图纸碎片）
                for left in range(len(WI.SPECIAL), SP_KEEP, -1):
                    lines += ["execute store result storage rpg:merchant cut.i int 1 run random value 1..%d" % left,
                              "execute as @e[type=minecraft:villager,tag=rpg.mer.new,limit=1] run function %s/cut with storage rpg:merchant cut" % P]
            fn(stem, lines + ["tag @e[type=minecraft:villager,tag=rpg.mer.new] remove rpg.mer.new"])
        if variants[0] is None:
            fn("place/%s" % k, ["# 管理员：在脚下放一位%s（as/at 管理员）" % en, "function %s/spawn_%s" % (P, k),
                                "playsound minecraft:entity.villager.celebrate neutral @a[distance=..16] ~ ~ ~ 1 1"])
        else:
            fn("place/%s" % k, ["# 管理员：在脚下放一位%s（货里的契约书随机一柱）" % en,
                                "execute store result score #pp rpg_ev run random value 1..7"] +
               ["execute if score #pp rpg_ev matches %d run function %s/spawn_%s_%d" % (n, P, k, n) for n in variants] +
               ["playsound minecraft:entity.villager.celebrate neutral @a[distance=..16] ~ ~ ~ 1 1"])
    fn("remove", ["# 管理员：移走 4 格内最近的商人（连同模型部件）",
                  "execute as @e[tag=rpg.mer,distance=..4,limit=1,sort=nearest] run function %s/gone" % P])
    fn("cut", ["$data remove entity @s Offers.Recipes[$(i)]"])
    # 固定的神秘商人每个游戏日换一次货（原位重放一位）
    fn("restock", ["tag @s add rpg.mer.old",
                   "execute rotated as @s run function %s/place/mystery" % P,
                   "scoreboard players operation @e[type=minecraft:villager,tag=rpg.mer.mystery,tag=!rpg.mer.old,distance=..0.1] rpg_mer_day = #day rpg_ev",
                   "particle minecraft:poof ~ ~1 ~ 0.3 0.6 0.3 0.05 20",
                   "function %s/gone" % P])
    fn("stamp", ["execute unless score @s rpg_mer_day matches 0.. run return run scoreboard players operation @s rpg_mer_day = #day rpg_ev",
                 "execute unless score @s rpg_mer_day = #day rpg_ev at @s run function %s/restock" % P])
    patch("events/sec.mcfunction", "rpg:merchant/stamp",
          "execute as @e[type=minecraft:villager,tag=rpg.mer.mystery] run function rpg:merchant/stamp\n")
    patch("events/load.mcfunction", "rpg_mer_day", "scoreboard objectives add rpg_mer_day dummy\n")
    fn("gone", ["execute on passengers run kill @s", "tp @s ~ -400 ~", "kill @s"])


# ============================================================================ 迷途商人事件、支线、彩蛋
def wire():
    # 第 6 种事件：迷途商人（白天）
    s = read("events/roll.mcfunction")
    if "random value 1..6" not in s:
        write("events/roll.mcfunction", s.replace("random value 1..5", "random value 1..6"))
    patch("events/try.mcfunction", "#k rpg_ev 6",
          "execute if score #r rpg_ev matches 6 if score #day rpg_ev matches 0..11000 run scoreboard players set #k rpg_ev 6\n",
          where="execute if score #k rpg_ev matches 1 run return run")
    patch("events/try.mcfunction", "rpg:merchant/ev/start",
          "execute if score #k rpg_ev matches 6 run return run function rpg:merchant/ev/start\n")
    patch("events/run.mcfunction", "rpg:merchant/ev/sec",
          "execute if score #ev rpg_ev matches 6 run function rpg:merchant/ev/sec\n",
          where="execute if score #ev rpg_ev matches 1.. if score #left")
    patch("events/end.mcfunction", "rpg:merchant/ev/stop",
          "execute if score #ev rpg_ev matches 6 run function rpg:merchant/ev/stop\n",
          where="scoreboard players set #ev rpg_ev 0")
    col = ui.HOLY_LIGHT
    bc = "tellraw @a %s" % J(["", seg("〖事件%s迷途商人〗" % ui.TAG_JOIN, col, True), seg(" " + ui.fraktur("Travelling Merchant"), ui.BROADCAST_GLOSS),
                              seg("  一位迷途商人在附近歇脚，只待 5 分钟。", ui.BROADCAST_BODY), seg("　坐标 ", ui.BROADCAST_BODY),
                              {"nbt": "cur.x", "storage": "rpg:events", "color": ui.BROADCAST_NAME, "bold": False, "italic": False}, seg(", ", ui.BROADCAST_BODY),
                              {"nbt": "cur.z", "storage": "rpg:events", "color": ui.BROADCAST_NAME, "bold": False, "italic": False}])
    fn("ev/start", ["function rpg:events/place_near",
                    "scoreboard players set #ev rpg_ev 6",
                    "scoreboard players operation #end rpg_ev = #now rpg_ev",
                    "scoreboard players add #end rpg_ev 6000",
                    "data modify storage rpg:events cur.n set value \"迷途商人\"",
                    "execute store result storage rpg:events cur.x int 1 run data get entity @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] Pos[0]",
                    "execute store result storage rpg:events cur.z int 1 run data get entity @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] Pos[2]",
                    "execute at @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] run function %s/place/travel" % P,
                    "execute at @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] run tag @e[type=minecraft:villager,tag=rpg.mer.travel,distance=..1,limit=1,sort=nearest] add rpg.mer.temp", bc])
    fn("ev/sec", ["execute unless entity @e[tag=rpg.mer.temp] run function rpg:events/end"])
    fn("ev/stop", ["execute as @e[tag=rpg.mer.temp] at @s run particle minecraft:poof ~ ~1 ~ 0.3 0.6 0.3 0.05 20",
                   "execute as @e[tag=rpg.mer.temp] run function %s/gone" % P])
    fn("admin/travel", ["function rpg:events/end", "execute store result score #now rpg_ev run time query gametime",
                        "function %s/ev/start" % P])
    # 每种商人一条搭话、一条成交进度：站在一起的商人互不串台
    def cond(tag):
        return [{"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"nbt": "{Tags:[\"%s\"]}" % tag}}]

    adv = os.path.join(DP, "data", "rpg", "advancement", "merchant")
    for k in MERCHANTS:
        near = "execute as @e[type=minecraft:villager,tag=rpg.mer.%s,distance=..8,limit=1,sort=nearest] run function rpg:merchant_%s/anim/" % (k, k)
        wj(os.path.join(adv, "talk_%s.json" % k), {
            "criteria": {"talk": {"trigger": "minecraft:player_interacted_with_entity", "conditions": {"entity": cond("rpg.mer." + k)}}},
            "rewards": {"function": "%s/talk_%s" % (P, k)}})
        lines = ["advancement revoke @s only rpg:merchant/talk_%s" % k,
                 "execute if items entity @s weapon.mainhand minecraft:golden_hoe run return run function %s/hoe" % P, near + "examine"]
        if k in ("mystery", "travel"):
            lines.append("function rpg:quest/start_4")
        fn("talk_%s" % k, lines)
        wj(os.path.join(adv, "trade_%s.json" % k), {
            "criteria": {"trade": {"trigger": "minecraft:villager_trade", "conditions": {"villager": cond("rpg.mer." + k)}}},
            "rewards": {"function": "%s/trade_%s" % (P, k)}})
        fn("trade_%s" % k, ["advancement revoke @s only rpg:merchant/trade_%s" % k, near + "bow"])
    # 七罪之仆买本柱契约书半价：原版交易没有每人一价，成交后退一半
    for p in ui.PILLARS:
        n = p["n"]
        wj(os.path.join(adv, "pact_%d.json" % n), {
            "criteria": {"trade": {"trigger": "minecraft:villager_trade", "conditions": {
                "villager": cond("rpg.mer"),
                "item": {"predicates": {"minecraft:custom_data": "{pact_tag:1b,pact:%d}" % n}}}}},
            "rewards": {"function": "%s/pact_%d" % (P, n)}})
        fn("pact_%d" % n, ["advancement revoke @s only rpg:merchant/pact_%d" % n,
                           "execute if score @s rpg_ident matches 4 if score @s rpg_ident_sin matches %d run function %s/refund" % (n, P)])
    fn("refund", ["loot give @s loot rpg:merchant/refund_badge", "loot give @s loot rpg:merchant/refund_currency",
                  "tellraw @s %s" % J(["", seg("[契约]", "#D596F2", True),
                                       seg("　你本就归在那根柱下，商人退了你一半。", ui.BROADCAST_BODY)])])
    badge = json.load(io.open(os.path.join(LOOT, "elite", "badge.json"), encoding="utf-8"))
    badge["pools"][0]["rolls"] = BOOK_BADGE // 2
    wj(os.path.join(LOOT, "merchant", "refund_badge.json"), badge)
    cur = json.load(io.open(os.path.join(HERE, "world_loot_currency.json"), encoding="utf-8"))["entries"][1]
    fns = [f for f in cur["functions"] if f["function"].replace("minecraft:", "") != "set_count"]
    wj(os.path.join(LOOT, "merchant", "refund_currency.json"), {"type": "minecraft:generic", "pools": [
        {"rolls": 1, "entries": [{"type": "minecraft:item", "name": cur["name"],
                                  "functions": fns + [{"function": "minecraft:set_count", "count": BOOK_CURRENCY // 2}]}]}]})
    # 彩蛋：拿金锄对商人右键（「敲」）三下（商人无敌，挨打不触发进度，所以算右键）
    patch("events/load.mcfunction",
          "rpg_mer_hoe", "scoreboard objectives add rpg_mer_hoe dummy\n")
    fn("hoe", ["scoreboard players add @s rpg_mer_hoe 1",
               "playsound minecraft:entity.villager.no neutral @a[distance=..16] ~ ~ ~ 1 1",
               "execute if score @s rpg_mer_hoe matches 3.. run function %s/hoe_done" % P])
    fn("hoe_done", ["scoreboard players set @s rpg_mer_hoe 0",
                    "loot give @s loot rpg:world/currency",
                    "execute as @e[tag=rpg.mer,distance=..6,limit=1,sort=nearest] at @s run particle minecraft:angry_villager ~ ~2 ~ 0.3 0.2 0.3 0 6",
                    "execute if entity @e[tag=rpg.mer.temp,distance=..6] run function rpg:events/end",
                    "function rpg:quest/title/get_merchant"])


def main():
    import shutil
    shutil.rmtree(os.path.join(FUNC, "merchant"), ignore_errors=True)
    shutil.rmtree(os.path.join(DP, "data", "rpg", "advancement", "merchant"), ignore_errors=True)
    check_buy()
    place()
    wire()
    print("merchants: %d functions, %d merchants" % (COUNT, len(MERCHANTS)))


if __name__ == "__main__":
    main()
