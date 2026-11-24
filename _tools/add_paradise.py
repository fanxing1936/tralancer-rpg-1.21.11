# -*- coding: utf-8 -*-
"""失乐园：维度、自由猎杀、四座河庭的试炼、宝库（策划书「失乐园」「试炼与宝库」，用户 2026-11-24）。

    python add_paradise.py ../rpg ../resourcepack

* 玩家面板「失乐园」页进出。伊甸之门（中心 32 格）安全，有灵魂营火、铁匠、枯死的生命树。
* 门外按离门多远分三区，怪物强化、精英更多、掉落更多；血月、游荡的基路伯。
* 四座河庭（比逊 / 基训 / 希底结 / 伯拉）各 5 层：试炼刷怪笼进冷却就升一层（作者原来的骨架），第 5 层守关。
* 宝库：钥匙只定义一份，锁从同一份读；开箱演出与 8 档天降沿用作者原来的 rpg:loot/loot，奖励换成体系内的。
* 黑石堡垒由 add_blackstone_fortress.py（Antigravity）生成，这里只给宝箱掉落与堡主。
"""
import io
import json
import math
import os
import re
import sys

import add_alchemy as AL
import add_eden_gate as EG
import add_elite_bar_art as BA
import paradise_world
import potion_spec as PS
import rpg_ui_style as ui
import world_loot_spec as W
from display_mob import hook_tag

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data", "rpg", "function")
LOOT = os.path.join(DP, "data", "rpg", "loot_table")
P = "rpg:pl"
O = "rpg_pl"
DIM = "rpg:paradise_lost"
INDIM = '{Dimension:"%s"}' % DIM      # @s[distance=..] 不分维度，判断自己在不在要看 Dimension
IN = "execute in %s positioned 0 83 0 " % DIM
FLOOR = 82
DECK = FLOOR + 1 + EG.DECK + 1        # 门内亭台上站人的高度
GATE_R = 36
BUILT = 9                             # 伊甸之门的版本：旧档读进来会自动换成新门
LAND = "execute in %s run tp @s 0.5 %d 17.5 180 0" % (DIM, DECK)
COUNT = 0
COL = "#E0483C"
HUNT = "type=#rpg:elite_pool"

COURTS = {  # 编号: (名, 拉丁, 中心 x, z, 灾厄?, 每层总数, 每人加, 同时, 每人加, 怪 [(id, 权重)], 生命, 攻击, 落物药水)
    1: ("比逊", "Pishon", 0, -120, False, 10, 2, 3, 1, [("zombie", 3), ("husk", 2), ("skeleton", 2), ("bogged", 1)], 30, 4, ["venom"]),
    2: ("基训", "Gihon", 120, 0, False, 15, 2, 4, 1, [("spider", 3), ("cave_spider", 2), ("creeper", 2), ("zombie", 1)], 36, 5, ["venom", "decay"]),
    3: ("希底结", "Hiddekel", 0, 120, True, 20, 3, 4, 2, [("vindicator", 2), ("pillager", 2), ("wither_skeleton", 2), ("blaze", 1)], 44, 7, ["venom", "decay", "fatigue"]),
    4: ("伯拉", "Euphrates", -120, 0, True, 30, 4, 5, 3, [("wither_skeleton", 3), ("stray", 2), ("enderman", 1), ("husk", 2)], 54, 9, ["venom", "decay", "fatigue", "harm"]),
}
CENTRE = {  # 河庭正中的大建筑: (结构, 旋转, 走近多少格开打, 刷怪半径, 落物偏移倍率, 守关者离中心, 祭坛层数)
    1: ("house_medium", "none", 7, 6, 0.8, 5, 1), 2: ("tower_large", "none", 5, 4, 0.6, 4, 1),
    3: ("house_large", "none", 8, 7, 1.0, 7, 2), 4: ("house_large", "clockwise_90", 8, 7, 1.0, 5, 2)}
SMALL = {  # 散在四周的小建筑
    1: ["house_small", "tower_small", "tower_small", "house_small"], 2: ["tower_medium", "house_small", "tower_small", "tower_small", "house_small"],
    3: ["tower_medium", "house_small", "tower_small", "tower_medium", "house_small", "tower_small"],
    4: ["tower_big", "house_small", "tower_medium", "tower_small", "house_small", "tower_big"]}
VAULT = (7, 17)                        # 宝库在大建筑南边的露天处（宝物从天上落，上面要空着）
ZONES = {1: ("泥沼", 0.5, 0.25, 2), 2: ("血泽", 1.0, 0.5, 3), 3: ("灰烬边境", 2.0, 1.0, 4)}  # 名, 生命加成, 伤害加成, 精英倍数
ZONE_R = (240, 560)
BOSSES = {"warden": "Gate Warden", "cherub": "Cherub", "castellan": "Castellan"}
TIER3 = ["wither_skeleton", "blaze", "enderman", "vindicator"]     # 泥沼里不留


def fn(name, lines):
    global COUNT
    path = os.path.join(FUNC, "pl", name + ".mcfunction")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    COUNT += 1


def wj(path, doc):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


J, read, write, patch, seg, snbt = AL.J, AL.read, AL.write, AL.patch, AL.seg, AL.snbt


def say(text, to="@s", colour=ui.BROADCAST_BODY):
    return "tellraw %s %s" % (to, J(["", seg("〖失乐园〗", COL, True), seg(" " + ui.fraktur("Paradise Lost"), ui.BROADCAST_GLOSS),
                                     seg("  " + text, colour)]))


def ev(name, en, text, to):
    return "tellraw %s %s" % (to, J(["", seg("〖失乐园%s%s〗" % (ui.TAG_JOIN, name), COL, True), seg(" " + ui.fraktur(en), ui.BROADCAST_GLOSS),
                                     seg("  " + text, ui.BROADCAST_BODY)]))


HERE_P = "@a[x=0,y=83,z=0,distance=0..]"     # 要在 IN 里用：本维度的玩家


# ============================================================================ 物品
def key_components(omen):
    tag, col = ui.TIERS["legend"]
    rule = ["", seg(ui.RULE_TEXT, ui.WHITE)]
    return {"minecraft:custom_name": ["", seg(tag, col, True), seg("灾厄试炼之匙" if omen else "试炼之匙", ui.WHITE)],
            "minecraft:lore": [rule, ["", seg("开辟神启的", ui.GRAY), seg("[钥匙]", col, True)],
                               ["", seg("唤出传奇的", ui.GRAY), seg("[宝具]", col, True)], rule]}


def key_id(omen):
    return "minecraft:ominous_trial_key" if omen else "minecraft:trial_key"


def loot_entry(iid, comps, n=1, weight=None, data=None):
    comps = dict(comps)
    d = comps.pop("minecraft:custom_data", None)
    e = {"type": "minecraft:item", "name": iid, "functions": [{"function": "minecraft:set_components", "components": comps}]}
    if d:
        e["functions"].append({"function": "minecraft:set_custom_data", "tag": re.sub(r'"(\w+)":', r"\1:", snbt(d))})
    if n != 1:
        e["functions"].append({"function": "minecraft:set_count", "count": n if isinstance(n, int) else {"type": "minecraft:uniform", "min": n[0], "max": n[1]}})
    if weight:
        e["weight"] = weight
    return e


def ref(table, weight=1):
    return {"type": "minecraft:loot_table", "value": table, "weight": weight}


def pool(entries, rolls=1, chance=None):
    p = {"rolls": rolls if isinstance(rolls, int) else {"type": "minecraft:uniform", "min": rolls[0], "max": rolls[1]}, "entries": entries}
    if chance is not None:
        p["conditions"] = [{"condition": "minecraft:random_chance", "chance": chance}]
    return p


def table(name, *pools):
    wj(os.path.join(LOOT, *(name + ".json").split("/")), {"type": "minecraft:generic", "pools": list(pools)})


RELICS = {  # 失乐园独有的遗物
    "fruit": ("禁果", "forbidden_fruit", ["咬过一口，还在流汁的果子", "献给生命树，或卖给神秘商人"]),
    "mud": ("血泥", "blood_mud", ["血泽里捧起来的泥", "献给生命树，或卖给神秘商人"]),
    "feather": ("断羽", "broken_feather", ["从天上掉下来、烧断了的羽毛", "献给生命树，或卖给神秘商人"]),
}


def loots():
    import add_world_loot as L
    for om in (False, True):
        table("trial/ominous_key" if om else "trial/key", pool([loot_entry(key_id(om), key_components(om))]))
    for k, (name, model, lines) in RELICS.items():
        rule = ["", seg(ui.RULE_TEXT, ui.WHITE)]
        table("paradise/" + k, pool([loot_entry("minecraft:paper", {
            "minecraft:custom_name": ["", seg(W.RELIC, ui.MUTED, True), seg(name, ui.WHITE)],
            "minecraft:lore": [rule] + [["", seg(l, ui.GRAY)] for l in lines] + [rule],
            "minecraft:item_model": "rpg:relic/" + model, "minecraft:max_stack_size": 64,
            "minecraft:custom_data": {"rpg_mat": "pl_" + k}})]))
    # 遗物随机
    ents = []
    for item in W.RELIC_USE:
        name, comps = L.relic_first(item)
        ents.append(loot_entry("minecraft:" + item, comps, (1, 3)))
    table("paradise/relic_any", pool(ents))
    table("paradise/z1", pool([ref("rpg:paradise/relic_any")], 1, 0.5))
    table("paradise/z2", pool([ref("rpg:paradise/relic_any")]), pool([ref("rpg:forge/item/soul")], 1, 0.15),
          pool([ref("rpg:potion/any_brave")], 1, 0.04), pool([ref("rpg:paradise/mud")], 1, 0.08))
    sps = [ref("rpg:world/sp/" + k) for k in ("star", "wind", "tear", "core", "stone", "bronze", "soil")]
    table("paradise/sp_any", pool(sps))
    table("paradise/z3", pool([ref("rpg:paradise/relic_any")], (1, 2)), pool([ref("rpg:forge/item/soul")], 1, 0.25),
          pool([ref("rpg:paradise/sp_any")], 1, 0.04), pool([ref("rpg:elite/badge")], 1, 0.06), pool([ref("rpg:paradise/feather")], 1, 0.05))
    table("paradise/champ", pool([ref("rpg:paradise/fruit")], 1, 0.15))
    # 河庭：刷怪笼吐的
    for k, c in COURTS.items():
        omen = c[4]
        table("paradise/court_%d" % k, pool([
            ref("rpg:world/currency", 20), ref("rpg:paradise/relic_any", 24), ref("rpg:forge/item/soul", 12), ref("rpg:forge/item/blank", 3),
            ref("rpg:forge/item/forge_stone", 6), ref("rpg:forge/item/wash_gem", 5), ref("rpg:forge/item/gild_leaf", 4), ref("rpg:forge/rune_any", 5),
            ref("rpg:forge/stone_any", 4 if omen else 1), ref("rpg:potion/any_brave", 10), ref("rpg:potion/any_epic", 5 if omen else 2),
            ref("rpg:world/bp_fragment", 4), ref("rpg:trial/ominous_key" if omen else "rpg:trial/key", 5 if omen else 8)], 2))
    table("paradise/fortress_chest", pool([ref("rpg:paradise/sp_any", 4), ref("rpg:potion/any_epic", 4), ref("rpg:forge/rune_any", 3),
                                           ref("rpg:trial/key", 3), ref("rpg:paradise/relic_any", 8), ref("rpg:world/currency", 6)], (3, 5)),
          pool([ref("rpg:world/bp_epic_any")], 1, 0.05))
    # 基路伯
    table("paradise/cherub", pool([ref("rpg:paradise/feather")]), pool([ref("rpg:world/bp_fragment")], 8))
    # 宝库八档（1 樱怒之日 由原来的 summon 给，不在表里）
    table("paradise/v_material", pool([ref("rpg:paradise/sp_any", 3), ref("rpg:forge/rune_any", 2), ref("rpg:forge/stone_any", 2)]))
    table("paradise/v_misc", pool([ref("rpg:potion/any_epic"), ref("rpg:forge/bundle")]))


# ============================================================================ 宝库与钥匙
def vault_nbt(omen):
    comps = ",".join("%s:%s" % (json.dumps(k), snbt(v)) for k, v in key_components(omen).items())
    return ('minecraft:vault[ominous=%s]{config:{loot_table:"rpg:loot/%s",key_item:{id:"%s",count:1,components:{%s}}}}'
            % ("true" if omen else "false", "loot_ominous" if omen else "loot", key_id(omen), comps))


def vaults():
    for name, v in (("loot", 2), ("loot_ominous", 1)):
        table("loot/" + name, pool([{"type": "minecraft:item", "name": "minecraft:nether_star",
                                     "functions": [{"function": "minecraft:set_custom_data", "tag": "{loot_trigger:%db}" % v}]}]))
    for f, omen in (("g0", True), ("g1", False)):
        rel = "loot/loot/%s.mcfunction" % f
        out = []
        for l in read(rel).rstrip("\n").split("\n"):
            m = re.match(r"(execute as \S+ at @s run setblock ~ ~-1 ~ )minecraft:vault", l)
            out.append(m.group(1) + vault_nbt(omen) if m else l)
        assert any(vault_nbt(omen) in l for l in out), rel
        write(rel, "\n".join(out) + "\n")
    # 概率（百分）：1 樱怒之日、2 传说图纸、3 史诗图纸、4 特殊材料/符文/符石、5 药水/养成包、6 传说药水
    star = 'summon minecraft:ominous_item_spawner ~ ~5 ~ {"item":{components:{"minecraft:custom_data":{loot:%db}},count:1,id:"minecraft:nether_star"},"spawn_item_after_ticks":80}'
    for f, odds in (("trigger", [(1, 1), (4, 2), (15, 3), (30, 4), (50, 5)]), ("trigger_ominous", [(1, 1), (6, 2), (20, 3), (40, 4), (30, 5), (3, 6)])):
        lines, at = ["# 开箱：落哪一档", "execute store result score #loot loot run random value 1..100"], 1
        for pct, k in odds:
            lines.append("execute if score #loot loot matches %d..%d run %s" % (at, at + pct - 1, star % k))
            at += pct
        assert at == 101
        write("loot/%s.mcfunction" % f, "\n".join(lines + ["scoreboard players reset * loot"]) + "\n")
    # 落地：1 原样；2..6 换成掉落表；7、8 不再出现
    tab = {2: "rpg:world/bp_legend_any", 3: "rpg:world/bp_epic_any", 4: "rpg:paradise/v_material", 5: "rpg:paradise/v_misc", 6: "rpg:potion/any_legend"}
    out = []
    for l in read("loot/loot.mcfunction").rstrip("\n").split("\n"):
        m = re.match(r"execute as @e\[type=minecraft:item,tag=rpg\.i\.loot(\d)\] at @s unless block ~ ~-1 ~ air run (summon|loot)", l)
        if m and int(m.group(1)) in tab:
            l = "execute as @e[type=minecraft:item,tag=rpg.i.loot%s] at @s unless block ~ ~-1 ~ air run loot spawn ~ ~ ~ loot %s" % (m.group(1), tab[int(m.group(1))])
        out.append(l)
    guard = "execute as @e[type=minecraft:item,tag=rpg.i.loot%d] run data merge entity @s {PickupDelay:20s}"
    if not any("PickupDelay" in l for l in out):      # 半空里的宝物别被人捡走
        out = [guard % k for k in range(1, 9)] + out
    write("loot/loot.mcfunction", "\n".join(out) + "\n")
    fn("place/vault", ["# 管理员：在脚下放一座试炼宝库；站在旧宝库上执行就是换锁", "setblock ~ ~ ~ " + vault_nbt(False)])
    fn("place/vault_ominous", ["# 管理员：在脚下放一座灾厄宝库", "setblock ~ ~ ~ " + vault_nbt(True)])
    # 最早的布置指令：原来两座宝库叠在一格
    s = read("command/setblock.mcfunction").split("\n")
    s = [l for l in s if not l.startswith("setblock ~ ~ ~ minecraft:vault")]
    write("command/setblock.mcfunction", "\n".join(["# 试炼刷怪笼在头顶，普通宝库在脚下，灾厄宝库在身前 3 格"] + s[:1] +
                                                   ["setblock ~ ~ ~ " + vault_nbt(False), "setblock ~ ~ ~3 " + vault_nbt(True)] + s[1:]))
    # 旧试炼表：钥匙改成同一份，直接掉成品武器的两条改成图纸
    for name in ("trial", "trial_ominous"):
        p = os.path.join(LOOT, "trial", name + ".json")
        doc = json.load(io.open(p, encoding="utf-8"))
        for pl in doc["pools"]:
            for i, e in enumerate(pl["entries"]):
                s = json.dumps(e)
                w = e.get("weight", 1)
                if e.get("name") == "minecraft:trial_key":
                    pl["entries"][i] = ref("rpg:trial/key", w)
                elif e.get("name") == "minecraft:ominous_trial_key":
                    pl["entries"][i] = ref("rpg:trial/ominous_key", w)
                elif "trial_tag" in s:
                    pl["entries"][i] = ref("rpg:world/bp_legend_any" if '"trial_tag": 1' in s else "rpg:world/bp_epic_any", w)
        wj(p, doc)
    hole = os.path.join(DP, "data", "rpg", "trial_spawner", "hole.json")
    if os.path.exists(hole):
        os.remove(hole)
    # 旧的层数试炼（地图里的命令方块还在调）：20 层封顶后从头、去掉表情、第 5 层的落物真的召首领
    t = read("task/trial/trigger.mcfunction")
    if "matches 21.." not in t:
        t = t.replace("scoreboard players add 层数 trial 1\n", "scoreboard players add 层数 trial 1\nexecute if score 层数 trial matches 21.. run scoreboard players set 层数 trial 1\n", 1)
        t = re.sub(r'(title @a\[distance=\.\.20\] title )\[.*?\]\s*$',
                   lambda m: m.group(1) + J(["", seg("试炼之室", COL, True), seg(" " + ui.fraktur("Trial"), ui.BROADCAST_GLOSS)]), t, flags=re.M)
        write("task/trial/trigger.mcfunction", t)
    s = read("task/trial/trial.mcfunction")
    if "rpg:pl/old_champ" not in s:
        s = s.replace("execute as @e[type=minecraft:item,tag=rpg.i.trial_summon1] at @s run kill",
                      "execute as @e[type=minecraft:item,tag=rpg.i.trial_summon1] at @s run function rpg:pl/old_champ\n"
                      "execute as @e[type=minecraft:item,tag=rpg.i.trial_summon1] at @s run kill", 1)
        write("task/trial/trial.mcfunction", s)
    fn("old_champ", ["function %s/court/champ" % P])


# ============================================================================ 门与河庭的建造
def disc(r, y, block, hollow=0):
    out = []
    for z in range(-r, r + 1):
        w = int((r * r - z * z) ** 0.5)
        if hollow and abs(z) < hollow:
            w2 = int((hollow * hollow - z * z) ** 0.5)
            out.append("fill ~%d ~%d ~%d ~%d ~%d ~%d %s" % (-w, y, z, -w2, y, z, block))
            out.append("fill ~%d ~%d ~%d ~%d ~%d ~%d %s" % (w2, y, z, w, y, z, block))
        else:
            out.append("fill ~%d ~%d ~%d ~%d ~%d ~%d %s" % (-w, y, z, w, y, z, block))
    return out


def altar(big):
    """刷怪笼的祭坛（at 中心 y=FLOOR）：一层台或两层台，四角立碑，地上嵌一圈。刷怪笼在台顶。"""
    out = []

    def tier(y, rad, cut):
        st = "minecraft:stone_brick_stairs"
        for k, f in ((-rad, "south"), (rad, "north")):
            out.append("fill ~%d ~%d ~%d ~%d ~%d ~%d %s[facing=%s]" % (-rad + cut, y, k, rad - cut, y, k, st, f))
        for k, f in ((-rad, "east"), (rad, "west")):
            out.append("fill ~%d ~%d ~%d ~%d ~%d ~%d %s[facing=%s]" % (k, y, -rad + 1, k, y, rad - 1, st, f))
        out.append("fill ~%d ~%d ~%d ~%d ~%d ~%d minecraft:stone_bricks" % (1 - rad, y, 1 - rad, rad - 1, y, rad - 1))
    rad = 4 if big else 2
    q = rad + 1
    out.append("fill ~%d ~ ~%d ~%d ~ ~%d minecraft:polished_deepslate" % (-q, -q, q, q))
    out.append("fill ~%d ~ ~%d ~%d ~ ~%d minecraft:smooth_stone" % (-rad, -rad, rad, rad))
    out.extend("setblock ~%d ~ ~%d minecraft:chiseled_stone_bricks" % (a * q, b * q) for a, b in ((1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)))
    tier(1, rad, 0)
    if big:
        tier(2, 2, 0)
        out.append("fill ~-3 ~1 ~-3 ~3 ~1 ~3 minecraft:polished_andesite replace minecraft:stone_bricks")
    top = 2 if big else 1
    out.append("fill ~-1 ~%d ~-1 ~1 ~%d ~1 minecraft:polished_diorite" % (top, top))
    out.append("setblock ~ ~%d ~ minecraft:chiseled_stone_bricks" % top)
    h = 5 if big else 3
    for a in (-rad, rad):
        for b in (-rad, rad):
            out.append("setblock ~%d ~1 ~%d minecraft:chiseled_stone_bricks" % (a, b))
            if big:
                out.append("setblock ~%d ~2 ~%d minecraft:polished_deepslate" % (a, b))
            out.append("fill ~%d ~%d ~%d ~%d ~%d ~%d minecraft:deepslate_brick_wall" % (a, 3 if big else 2, b, a, h, b))
            out.append("setblock ~%d ~%d ~%d minecraft:chiseled_stone_bricks" % (a, h + 1, b))
    return out


def template(key, rot):
    """把结构的中心对到原点：(x0, z0, 宽, 深, place template 的落点)。"""
    sx, _sy, sz = EG.SIZE[key]
    wx, wz = (sx, sz) if rot in ("none", "180") else (sz, sx)
    x0, z0 = -(wx // 2), -(wz // 2)
    return x0, z0, wx, wz, {"none": (x0, z0), "180": (x0 + wx - 1, z0 + wz - 1), "clockwise_90": (x0 + wx - 1, z0), "counterclockwise_90": (x0, z0 + wz - 1)}[rot]


def blob(x, z, seed, size):
    """平滑的块状噪声，0 到 1。"""
    def h(i, j):
        n = (i * 374761393 + j * 668265263 + seed * 1274126177) & 0xFFFFFFFF
        n = ((n ^ (n >> 13)) * 1274126177) & 0xFFFFFFFF
        return ((n ^ (n >> 16)) & 0xFFFF) / 65535.0
    fx, fz = x / float(size), z / float(size)
    i, j = int(fx // 1), int(fz // 1)
    u, v = fx - i, fz - j
    u, v = u * u * (3 - 2 * u), v * v * (3 - 2 * v)
    return (h(i, j) * (1 - u) + h(i + 1, j) * u) * (1 - v) + (h(i, j + 1) * (1 - u) + h(i + 1, j + 1) * u) * v


def ground(cells):
    """河庭的地面：和原始建筑同一套灰石，成片地过渡（亮石、中灰、深板岩、苔石），和墙面一个路子。"""
    pal = [("cobbled_deepslate", "cracked_deepslate_bricks", "deepslate_bricks", "cobbled_deepslate"), ("tuff", "cobblestone", "tuff", "mossy_cobblestone"),
           ("andesite", "stone", "gravel", "andesite"), ("smooth_stone", "stone", "andesite", "smooth_stone"), ("diorite", "polished_diorite", "smooth_stone", "calcite")]
    at = {}
    for x, z in cells:
        v = 0.65 * blob(x, z, 1, 7) + 0.35 * blob(x, z, 2, 3)
        band = pal[max(0, min(4, int((v - 0.28) / 0.44 * 5)))]
        at[(x, z)] = band[int(blob(x, z, 3, 1) * 3.999)]
    out = []
    for z in sorted({q[1] for q in at}):
        xs = sorted(q[0] for q in at if q[1] == z)
        k = 0
        while k < len(xs):
            e = k
            while e + 1 < len(xs) and xs[e + 1] == xs[e] + 1 and at[(xs[e + 1], z)] == at[(xs[k], z)]:
                e += 1
            out.append("fill ~%d ~ ~%d ~%d ~ ~%d minecraft:%s" % (xs[k], z, xs[e], z, at[(xs[k], z)]))
            k = e + 1
    return out


def dead_tree():
    """枯死的生命树：有根、扭一下的树干、八根往上翘的枝。{(x, y, z): 方块}，y=0 是亭台地面。"""
    out = {}
    for y in range(0, 5):
        for x in (-1, 0, 1):
            for z in (-1, 0, 1):
                if y < 2 or abs(x) + abs(z) < 2 or (x, z) == ((1, 1) if y == 2 else (-1, 1)):
                    out[(x, y, z)] = "stripped_dark_oak_wood"
    for x, z, h in ((2, 0, 2), (-2, 1, 1), (0, -2, 2), (1, 2, 1), (-1, -2, 1), (3, 0, 1), (0, -3, 1), (-2, 0, 2), (-3, 1, 1), (0, 2, 2)):
        for y in range(h):
            out[(x, y, z)] = "dark_oak_wood"
    for y in range(5, 14):
        out[(0, y, 0)] = "stripped_dark_oak_wood" if y < 10 else "dark_oak_wood"
        if y < 8:
            out[(0, y, 1 if y < 7 else -1)] = out[(1 if y < 6 else -1, y, 0)] = "stripped_dark_oak_wood"
    for dx, dz, y, n in ((1, 0, 6, 5), (-1, 0, 7, 5), (0, 1, 8, 5), (0, -1, 6, 5), (1, 1, 9, 3), (-1, 1, 10, 3), (1, -1, 11, 2), (-1, -1, 8, 3)):
        yy = y
        for k in range(1, n + 1):
            out[(dx * k, yy, dz * k)] = "dark_oak_wood"
            if k % 2 == 0 or k == n:
                yy += 1
                out[(dx * k, yy, dz * k)] = "dark_oak_wood"
        out[(dx * n, yy + 1, dz * n)] = "dark_oak_fence"
    out[(0, 14, 0)] = "dark_oak_fence"
    return out


def building():
    """positioned 在地面中心（y=FLOOR）。"""
    BB, CB, GB = "minecraft:polished_blackstone_bricks", "minecraft:cracked_polished_blackstone_bricks", "minecraft:gilded_blackstone"
    gate = ["# 伊甸之门（positioned 0 %d 0）" % FLOOR]
    for dy in range(1, 46):
        gate += disc(30, dy, "minecraft:air")
    for dy in range(-10, 0):
        gate += disc(29, dy, "minecraft:packed_mud")
    gate += ["execute as @e[tag=rpg.mer,distance=..60] run function rpg:merchant/gone", "kill @e[type=minecraft:interaction,tag=rpg.pl.tree,distance=..60]",
             "kill @e[type=minecraft:item,distance=..40]"]
    gate += disc(30, 0, BB) + disc(27, 0, CB, 26)
    # 中央的大门：四面对称的十字亭（add_eden_gate.py），亭台地面比广场高 5 格
    gate += ["place template rpg:paradise/eden_gate ~%d ~1 ~%d" % (-EG.CX, -EG.CZ)]
    t = DECK - FLOOR
    gate += ["fill ~-2 ~%d ~-2 ~2 ~%d ~2 %s" % (t - 1, t - 1, GB), "fill ~-1 ~%d ~-1 ~1 ~%d ~1 minecraft:muddy_mangrove_roots" % (t - 1, t - 1)]
    gate += ["setblock ~%d ~%d ~%d minecraft:%s" % (x, t + y, z, b) for (x, y, z), b in sorted(dead_tree().items())]
    gate += ["setblock ~%d ~%d ~%d minecraft:soul_campfire[lit=true]" % (x, t, z) for x, z in ((9, 3), (-9, -3))]
    for dx, dz in ((17, 17), (-17, 17), (17, -17), (-17, -17), (5, 28), (-5, 28), (5, -28), (-5, -28), (28, 5), (28, -5), (-28, 5), (-28, -5)):
        h = 6 if abs(dx) == 17 else 4
        gate += ["fill ~%d ~1 ~%d ~%d ~%d ~%d %s" % (dx, dz, dx, h, dz, BB), "setblock ~%d ~%d ~%d minecraft:soul_lantern" % (dx, h + 1, dz)]
    gate += ['summon minecraft:interaction ~ ~%d ~ {Tags:["rpg.pl.tree"],width:7.2f,height:5f,response:1b}' % t,
             "execute positioned ~3 ~%d ~11 rotated 90 0 run function rpg:merchant/place/smith" % t,
             "execute as @a[distance=..34,gamemode=!spectator] run " + LAND]
    fn("build/gate", gate)
    court = ["# 一座河庭的场地（positioned 中心 y=%d）" % FLOOR, "execute as @e[%s,distance=..60] run tp @s ~ -400 ~" % HUNT, "kill @e[type=minecraft:item,distance=..28]"]
    for dy in range(1, 33):
        court += disc(26, dy, "minecraft:air")
    for dy in range(-8, 0):
        court += disc(26, dy, "minecraft:" + ("andesite", "tuff", "cobblestone")[dy % 3])
    court += ground([(x, z) for z in range(-26, 27) for x in range(-26, 27) if x * x + z * z <= 676])
    court += disc(24, 0, "minecraft:water", 22) + disc(24, -1, "minecraft:tuff", 22)
    for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)):               # 过血池的四座小桥
        x, z = (20 * a, 25 * a), (20 * b, 25 * b)
        court += ["fill ~%d ~ ~%d ~%d ~ ~%d minecraft:polished_andesite" % (min(x) - abs(b), min(z) - abs(a), max(x) + abs(b), max(z) + abs(a))]
    for i in range(8):
        x, z = round(20 * math.cos(math.pi * i / 4 + 0.39)), round(20 * math.sin(math.pi * i / 4 + 0.39))
        court += ["fill ~%d ~1 ~%d ~%d ~%d ~%d minecraft:%s" % (x, z, x, 3 + i % 2, z, ("stone_bricks", "mossy_stone_bricks", "cracked_stone_bricks", "andesite")[i % 4]),
                  "setblock ~%d ~%d ~%d minecraft:soul_lantern" % (x, 4 + i % 2, z)]
    fn("build/court", court)
    # 原始建筑（add_eden_gate.py）：大的一座放正中，试炼就在里面打；小的散在四周，贴着地形
    used = set()
    for k, c in COURTS.items():
        out = ["# %s河庭的建筑（positioned 中心 y=%d）" % (c[0], FLOOR)]
        key, rot = CENTRE[k][:2]
        x0, z0, wx, wz, at = template(key, rot)
        out += ["place template rpg:paradise/%s ~%d ~ ~%d %s" % (key, at[0], at[1], rot)]
        gx, gz = (c[2] < 0) - (c[2] > 0), (c[3] < 0) - (c[3] > 0)      # 朝伊甸之门的方向：开门洞
        if gx:
            e = x0 + wx - 1 if gx > 0 else x0
            lo, hi = sorted((e, e - 5 * gx))
            out += ["fill ~%d ~1 ~-1 ~%d ~4 ~1 minecraft:air" % (lo, hi), "fill ~%d ~ ~-1 ~%d ~ ~1 minecraft:polished_andesite" % (min(lo, 20 * gx), max(hi, 20 * gx))]
        else:
            e = z0 + wz - 1 if gz > 0 else z0
            lo, hi = sorted((e, e - 5 * gz))
            out += ["fill ~-1 ~1 ~%d ~1 ~4 ~%d minecraft:air" % (lo, hi), "fill ~-1 ~ ~%d ~1 ~ ~%d minecraft:polished_andesite" % (min(lo, 20 * gz), max(hi, 20 * gz))]
        out += altar(CENTRE[k][6] == 2)
        # 室内照明只用光明方块（用户：不放灵魂灯）
        long_x, long_z = (9, 4) if wx > wz + 4 else (4, 9) if wz > wx + 4 else (4, 4)
        out += ["execute if block ~%d ~4 ~%d minecraft:air run setblock ~%d ~4 ~%d minecraft:light[level=13]" % (a, b, a, b)
                for a in (-long_x, 0, long_x) for b in (-long_z, 0, long_z)]
        ga, n = math.atan2(gz, gx), len(SMALL[k])
        for m, key in enumerate(SMALL[k]):
            a, d = ga + math.radians(45 + 270.0 * m / (n - 1)), 36 + (m * 5 + k * 3) % 7
            rot = ("none", "clockwise_90", "180", "counterclockwise_90")[(m + k) % 4]
            used.add((key, rot))
            out += ["execute unless score #sites %s matches 1 positioned ~%d ~ ~%d positioned over motion_blocking_no_leaves run function %s/build/site/%s_%s" % (O, round(d * math.cos(a)), round(d * math.sin(a)), P, key, rot)]
        fn("build/court_%d" % k, out)
    for key, rot in sorted(used):
        x0, z0, wx, wz, at = template(key, rot)
        a, b = (x0 - 1, z0 - 1), (x0 + wx, z0 + wz)
        fn("build/site/%s_%s" % (key, rot), [
            "# 散在四周的小建筑（at 地表）：清出空间，垫实脚下，铺同一套灰石地面",
            "fill ~%d ~ ~%d ~%d ~28 ~%d minecraft:air" % (a[0], a[1], b[0], b[1])] + [
            "fill ~%d ~%d ~%d ~%d ~%d ~%d minecraft:%s" % (a[0], dy, a[1], b[0], dy, b[1], ("andesite", "tuff", "cobblestone")[dy % 3]) for dy in range(-9, -1)] +
            [q.replace(" ~ ~", " ~-1 ~") for q in ground([(x, z) for z in range(a[1], b[1] + 1) for x in range(a[0], b[0] + 1)])] +
            ["place template rpg:paradise/%s ~%d ~-1 ~%d %s" % (key, at[0], at[1], rot),
             "execute if block ~ ~2 ~ minecraft:air run setblock ~ ~2 ~ minecraft:light[level=13]"])
    lines = ["# 失乐园打开：放好伊甸之门与四座河庭。旧档（#built 2 到 8）读进来时重放一遍", "scoreboard players set #built %s %d" % (O, BUILT),
             IN + "positioned 0 %d 0 run function %s/build/gate" % (FLOOR, P)]
    for k, c in COURTS.items():
        lines += ["scoreboard players set #c%d %s 0" % (k, O), IN + "positioned %d %d %d run function %s/build/court" % (c[2], FLOOR, c[3], P),
                  IN + "positioned %d %d %d run function %s/build/court_%d" % (c[2], FLOOR, c[3], P, k),
                  IN + "run kill @e[type=minecraft:marker,tag=rpg.pl.court%d]" % k,
                  IN + "run setblock %d %d %d %s" % (c[2] + VAULT[0], FLOOR + 1, c[3] + VAULT[1], vault_nbt(c[4])),
                  IN + 'run summon minecraft:marker %d %d %d {Tags:["rpg.pl.court","rpg.pl.court%d"]}' % (c[2], FLOOR + 1, c[3], k)]
    lines += ["scoreboard players set #sites %s 1" % O, IN + "run forceload remove all", "execute as @a[tag=rpg.pl.wait] run function %s/go" % P]
    fn("build/all", lines)


# ============================================================================ 进出
def travel():
    fn("enter", [
        "# 玩家面板「进入」",
        "execute if data entity @s %s run return run %s" % (INDIM, say("你已经在失乐园里了。")),
        "execute if entity @s[tag=rpg.pr] run return run " + say("序章还没结束。"),
        "execute store result storage rpg:paradise t.id int 1 run scoreboard players get @s rpg_fg_id",
        "function %s/save with storage rpg:paradise t" % P,
        "tag @s add rpg.pl.wait",
        "execute if score #built %s matches %d run return run function %s/go" % (O, BUILT, P),
        "execute unless score #built %s matches 1 run function %s/prepare" % (O, P),
        say("门正在打开……")])
    fn("save", ["$data modify storage rpg:paradise r.p$(id).dim set from entity @s Dimension",
                "$execute store result storage rpg:paradise r.p$(id).x double 0.01 run data get entity @s Pos[0] 100",
                "$execute store result storage rpg:paradise r.p$(id).y double 0.01 run data get entity @s Pos[1] 100",
                "$execute store result storage rpg:paradise r.p$(id).z double 0.01 run data get entity @s Pos[2] 100",
                "$execute store result storage rpg:paradise r.p$(id).yaw float 0.01 run data get entity @s Rotation[0] 100"])
    fn("prepare", ["scoreboard players set #built %s 1" % O,
                   IN + "run forceload add -32 -32 40 40"] +
       [IN + "run forceload add %d %d %d %d" % (c[2] - 56, c[3] - 56, c[2] + 56, c[3] + 56) for c in COURTS.values()] +
       ["schedule function %s/build/all 100t" % P])
    fn("go", ["# 落到门内（as 玩家）", "tag @s remove rpg.pl.wait", "tag @s add rpg.pl.in",
              "scoreboard players add @s rpg_pl_best 0", "scoreboard players set @s rpg_pl_dc 0",
              LAND,
              "effect give @s minecraft:slow_falling 5 0 true",
              "playsound minecraft:block.end_portal.spawn player @s ~ ~ ~ 0.5 0.6",
              "title @s times 10 50 20",
              "title @s title " + J(["", seg("失乐园", COL, True)]), "title @s subtitle " + J(["", seg(ui.fraktur("Paradise Lost"), ui.BROADCAST_GLOSS)]),
              "function rpg:quest/start_7"])
    fn("leave", [
        "execute unless data entity @s %s run return run %s" % (INDIM, say("你不在失乐园里。")),
        "execute in %s if entity @s[x=0,y=83,z=0,distance=..%d] run return run function %s/back" % (DIM, GATE_R, P),
        "scoreboard players set @s rpg_pl_lv 5",
        "execute store result score @s rpg_pl_px run data get entity @s Pos[0] 4",
        "execute store result score @s rpg_pl_pz run data get entity @s Pos[2] 4",
        say("站着别动，5 秒后离开。")])
    fn("leave_sec", ["execute store result score #x %s run data get entity @s Pos[0] 4" % O, "execute store result score #z %s run data get entity @s Pos[2] 4" % O,
                     "execute unless score #x %s = @s rpg_pl_px run return run function %s/leave_stop" % (O, P),
                     "execute unless score #z %s = @s rpg_pl_pz run return run function %s/leave_stop" % (O, P),
                     "scoreboard players remove @s rpg_pl_lv 1",
                     "particle minecraft:crimson_spore ~ ~1 ~ 0.5 1 0.5 0 40",
                     "execute if score @s rpg_pl_lv matches 0 run function %s/back" % P])
    fn("leave_stop", ["scoreboard players set @s rpg_pl_lv 0", say("你动了，离开取消。")])
    fn("back", ["tag @s remove rpg.pl.in", "scoreboard players set @s rpg_pl_lv 0",
                "execute store result storage rpg:paradise t.id int 1 run scoreboard players get @s rpg_fg_id",
                "function %s/back_m with storage rpg:paradise t" % P,
                "stopsound @s record rpg:bgm.prologue_waves",
                "playsound minecraft:block.portal.travel player @s ~ ~ ~ 0.2 1.4"])
    fn("back_m", ["$execute unless data storage rpg:paradise r.p$(id) in minecraft:overworld run return run tp @s 0 120 0",
                  "$function %s/back_at with storage rpg:paradise r.p$(id)" % P, "$data remove storage rpg:paradise r.p$(id)"])
    fn("back_at", ["$execute in $(dim) run tp @s $(x) $(y) $(z) $(yaw) 0"])
    fn("revive", ["# 死在失乐园里：复活后回到门内", "scoreboard players set @s rpg_pl_dc 0",
                  LAND, "effect give @s minecraft:weakness 30 1",
                  say("你在门里醒来。")])


# ============================================================================ 面板页
def panel():
    T = lambda text, col=ui.BROADCAST_BODY, bold=False: {"text": text, "color": col, "bold": bold, "italic": False}
    fn("page", ["# 失乐园页（as 玩家）", "scoreboard players add @s rpg_pl_best 0", "scoreboard players add @s rpg_pl_kill 0", "scoreboard players add #moon %s 0" % O,
                "execute store result storage rpg:paradise v.best int 1 run scoreboard players get @s rpg_pl_best",
                "execute store result storage rpg:paradise v.kill int 1 run scoreboard players get @s rpg_pl_kill",
                "execute store result storage rpg:paradise v.moon int 1 run scoreboard players get #moon %s" % O,
                "function %s/page_m with storage rpg:paradise v" % P])
    def ap(comp, macro=False, cond=""):
        l = "%sdata modify storage rpg:panel ui.body append value %s" % (("execute %s run " % cond) if cond else "", J({"text": "", "extra": comp}))
        return ("$" if macro else "") + l
    def act(label, v, tip):
        return "data modify storage rpg:panel ui.actions append value " + J({"label": T(label, ui.BROADCAST_HOLY, True), "tooltip": T(tip, ui.BROADCAST_BODY),
                                                                             "action": {"type": "minecraft:run_command", "command": "/trigger rpg_panel set %d" % v}})
    lines = ["data modify storage rpg:panel ui set value {title:{text:\"\"},body:[],actions:[]}",
             "data modify storage rpg:panel ui.title set value " + J(["", T("失乐园", COL, True), T(" " + ui.fraktur("Paradise Lost"), ui.BROADCAST_GLOSS)]),
             ap([T("泥与血的地方。伊甸之门里安全，门外越远，怪越强、掉得越多。\n\n")]),
             ap([T("最高层数　", ui.BROADCAST_BODY, True), T("$(best)", ui.BROADCAST_NAME), T(" / 20\n")], True),
             ap([T("猎杀　", ui.BROADCAST_BODY, True), T("$(kill)", ui.BROADCAST_NAME), T(" 只\n")], True),
             ap([T("血月　", ui.BROADCAST_BODY, True), T("正在天上，还剩 "), T("$(moon)", ui.BROADCAST_NAME), T(" 秒\n\n")], True, "if score #moon %s matches 1.." % O),
             ap([T("血月　", ui.BROADCAST_BODY, True), T("没有\n\n", ui.MUTED)], False, "if score #moon %s matches ..0" % O)]
    for k, c in COURTS.items():
        lo, hi = (k - 1) * 5 + 1, k * 5
        need = (k - 1) * 5
        lines += [ap([T("%s河庭　" % c[0], ui.BROADCAST_NAME, True), T("第 %d 到 %d 层　" % (lo, hi)), T("已过\n", ui.READY)], False, "if score @s rpg_pl_best matches %d.." % hi),
                  ap([T("%s河庭　" % c[0], ui.BROADCAST_NAME, True), T("第 %d 到 %d 层　" % (lo, hi)), T("可以进\n", ui.BROADCAST_HOLY)], False, "if score @s rpg_pl_best matches %d..%d" % (need, hi - 1)),
                  ap([T("%s河庭　" % c[0], ui.MUTED, True), T("第 %d 到 %d 层　先过前一座\n" % (lo, hi), ui.MUTED)], False, "if score @s rpg_pl_best matches ..%d" % (need - 1)) if need else ""]
    lines = [l for l in lines if l]
    lines += ["execute unless data entity @s %s run %s" % (INDIM, act("进入", 13, "落在伊甸之门，回来时回到现在的位置")),
              "execute if data entity @s %s run %s" % (INDIM, act("离开", 14, "门内立刻离开，门外要站着不动 5 秒")),
              act("返回面板", 8, "回到玩家面板"),
              "function rpg:panel/ui/show with storage rpg:panel ui"]
    fn("page_m", lines)
    button = "data modify storage rpg:panel ui.actions append value " + J({
        "label": T("失乐园", COL, True), "tooltip": T("进入失乐园：四座河庭的试炼与自由猎杀", ui.BROADCAST_BODY),
        "action": {"type": "minecraft:run_command", "command": "/trigger rpg_panel set 12"}})
    s = read("panel/pages/panel_open.mcfunction")
    if "rpg_panel set 12" not in s:
        i = s.index("data modify storage rpg:panel ui.actions append value {\"label\":{\"text\":\"HUD 开关\"")
        write("panel/pages/panel_open.mcfunction", s[:i] + button + "\n" + s[i:])
    patch("panel/tick.mcfunction", "rpg:pl/page",
          "execute if score @s rpg_panel matches 12 run function rpg:pl/page\n"
          "execute if score @s rpg_panel matches 13 run function rpg:pl/enter\n"
          "execute if score @s rpg_panel matches 14 run function rpg:pl/leave\n",
          where="execute if score @s rpg_panel matches 1.. run scoreboard players set @s rpg_panel 0")


# ============================================================================ 自由猎杀
def hunt():
    objs = [O, "rpg_pl_best", "rpg_pl_kill", "rpg_pl_lv", "rpg_pl_px", "rpg_pl_pz", "rpg_pl_er", "rpg_pl_tree"]
    hook_tag(DP, "load", P + "/load", False)
    hook_tag(DP, "tick", P + "/tick", True)
    fn("load", ["scoreboard objectives add %s dummy" % o for o in objs] + ["scoreboard objectives add rpg_pl_dc deathCount",
                "scoreboard players add #built %s 0" % O, "scoreboard players set #2 %s 2" % O, "scoreboard players set #100 %s 100" % O] +
       ["scoreboard players add #c%d %s 0" % (k, O) for k in COURTS] +
       ["scoreboard players set #%d rpg_el %d" % (n, n) for n in (2, 4)] +
       ["execute if score #built %s matches 2..8 run function %s/prepare" % (O, P)])
    fn("tick", ["scoreboard players add #t %s 1" % O,
                "execute if score #t %s matches 20.. run function %s/sec" % (O, P),
                "execute as @e[type=minecraft:interaction,tag=rpg.pl.tree] if data entity @s interaction on target run function %s/tree/use" % P,
                "execute as @e[type=minecraft:interaction,tag=rpg.pl.tree] run data remove entity @s interaction"])
    fn("sec", ["scoreboard players set #t %s 0" % O,
               "# 死在里面的人在主世界复活：要先接回来，这时维度里可能一个人都没有",
               "execute as @a[tag=rpg.pl.in,scores={rpg_pl_dc=1..}] unless data entity @s %s run function %s/revive" % (INDIM, P),
               "# 用别的办法离开了维度的人",
               "execute as @a[tag=rpg.pl.in,scores={rpg_pl_dc=0}] unless data entity @s %s run tag @s remove rpg.pl.in" % INDIM,
               IN + "unless entity @a[distance=0..] run return 0",
               "execute as @a[tag=rpg.pl.in,scores={rpg_pl_lv=1..}] at @s run function %s/leave_sec" % P,
               "# 门里不留怪",
               IN + "as @e[%s,distance=..%d] unless entity @s[tag=rpg.pl.g] run tp @s ~ -200 ~" % (HUNT, GATE_R + 2),
               "# 新刷出来的怪按离门多远强化",
               IN + "as @e[%s,tag=!rpg.pl.s,distance=%d..] at @s run function %s/mob/see" % (HUNT, GATE_R, P),
               "# 侵蚀：门外每分钟",
               IN + "as @a[distance=%d..,gamemode=!spectator,gamemode=!creative] run function %s/erode" % (GATE_R, P),
               "function %s/moon" % P, "function %s/cherub/sec" % P] +
       ["execute if score #c%d %s matches 1.. run function %s/court/%d/sec" % (k, O, P, k) for k in COURTS] +
       ["execute if score #built %s matches %d in %s positioned %d %d %d if score #c%d %s matches 0 if entity @a[distance=..%d,gamemode=!spectator] run function %s/court/%d/try"
        % (O, BUILT, DIM, c[2], FLOOR + 1, c[3], k, O, CENTRE[k][2], P, k) for k, c in COURTS.items()])
    see = ["# 第一次见到这只怪（as/at 它）：本包召唤的（有名字或 NoAI）不动", "tag @s add rpg.pl.s",
           "execute if data entity @s CustomName run return 0",
           "execute if entity @e[type=minecraft:marker,tag=rpg.pl.court,distance=..22] run return 0"]
    see += [IN + "if entity @s[distance=..%d] run return run function %s/mob/z1" % (ZONE_R[0], P),
            IN + "if entity @s[distance=..%d] run return run function %s/mob/z2" % (ZONE_R[1], P),
            "function %s/mob/z3" % P]
    fn("mob/see", see)
    for z, (name, hp, dmg, mul) in ZONES.items():
        pre = ["execute if entity @s[type=minecraft:%s] run return run tp @s ~ -200 ~" % m for m in TIER3] if z == 1 else []
        fn("mob/z%d" % z, ["# " + name] + pre + [
            "tag @s add rpg.pl.z%d" % z,
            "attribute @s minecraft:max_health modifier add rpg:pl %s add_multiplied_base" % hp,
            "attribute @s minecraft:attack_damage modifier add rpg:pl %s add_multiplied_base" % dmg,
            "attribute @s minecraft:movement_speed modifier add rpg:pl 0.08 add_multiplied_base",
            "data modify entity @s Health set value 1024f"])
        wj(os.path.join(DP, "data", "rpg", "advancement", "paradise", "kill_z%d.json" % z), {
            "criteria": {"kill": {"trigger": "minecraft:player_killed_entity", "conditions": {"entity": [
                {"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"nbt": "{Tags:[\"rpg.pl.z%d\"]}" % z}}]}}},
            "rewards": {"function": "%s/mob/kill_z%d" % (P, z)}})
        fn("mob/kill_z%d" % z, ["advancement revoke @s only rpg:paradise/kill_z%d" % z, "scoreboard players add @s rpg_pl_kill 1",
                                "loot give @s loot rpg:paradise/z%d" % z,
                                "execute if score #moon %s matches 1.. run loot give @s loot rpg:paradise/z%d" % (O, z),
                                "function rpg:events/bt/paradise"])
    # 精英：标签不算「本包召唤」，机率按区
    s = read("elite/roll.mcfunction")
    if "rpg.pl.s" not in s:
        s = s.replace("execute if score #nt rpg_el matches 1.. run return 0",
                      "execute if entity @s[tag=rpg.pl.s] run scoreboard players remove #nt rpg_el 1\n"
                      + "".join("execute if entity @s[tag=rpg.pl.z%d] run scoreboard players remove #nt rpg_el 1\n" % z for z in ZONES)
                      + "execute if score #nt rpg_el matches 1.. run return 0", 1)
        add = "".join("execute if entity @s[tag=rpg.pl.z%d] run scoreboard players operation #p rpg_el *= #%d rpg_el\n" % (z, v[3]) for z, v in ZONES.items())
        add += "execute if entity @s[tag=rpg.pl.s] if score #moon %s matches 1.. run scoreboard players operation #p rpg_el *= #2 rpg_el\n" % O
        add += "execute if entity @s[tag=rpg.pl.s] if score #p rpg_el matches 251.. run scoreboard players set #p rpg_el 250\n"
        add += "execute if entity @s[tag=rpg.pl.z2] if score #sef rpg_el matches ..5 run scoreboard players set #sef rpg_el 6\n"
        add += "execute if entity @s[tag=rpg.pl.z3] if score #sef rpg_el matches ..5 run scoreboard players set #sef rpg_el 6\n"
        s = s.replace("execute store result score #r rpg_el run random value 1..1000", add + "execute store result score #r rpg_el run random value 1..1000", 1)
        write("elite/roll.mcfunction", s)
    for g in W.GROUPS:
        patch("elite/kill/%s_champion.mcfunction" % g, "rpg:paradise/champ",
              "execute if entity @s[tag=rpg.pl.in] run loot give @s loot rpg:paradise/champ\n"
              "execute if entity @s[tag=rpg.pl.in] run function rpg:events/bt/paradise_champ\n")
    fn("erode", ["scoreboard players add @s rpg_pl_er 1", "execute unless score @s rpg_pl_er matches 60.. run return 0",
                 "scoreboard players set @s rpg_pl_er 0",
                 "execute if score @s rpg_force matches 1 if score @s rpg_vital matches 1.. run scoreboard players remove @s rpg_vital 1",
                 "execute unless score @s rpg_force matches 1 if score @s rpg_taint matches ..89 run scoreboard players add @s rpg_taint 1"])
    # 血月：20 分钟一次，3 分钟
    fn("moon", ["execute if score #moon %s matches 1.. run return run function %s/moon_on" % (O, P),
                "scoreboard players add #mw %s 1" % O,
                "execute if score #mw %s matches 1200.. run function %s/moon_start" % (O, P)])
    fn("moon_start", ["scoreboard players set #mw %s 0" % O, "scoreboard players set #moon %s 180" % O,
                      IN + "run " + ev("血月", "Blood Moon", "天上开始落血。三分钟内怪更多，掉落翻倍。", "@a[distance=0..]"),
                      IN + "run playsound minecraft:ambient.crimson_forest.mood master @a[distance=0..] ~ ~ ~ 2 0.5"])
    fn("moon_on", ["scoreboard players remove #moon %s 1" % O,
                   IN + "as @a[distance=%d..,gamemode=!spectator] at @s run particle minecraft:falling_dust{block_state:{Name:\"minecraft:redstone_block\"}} ~ ~8 ~ 8 2 8 0 60" % GATE_R,
                   "scoreboard players operation #q %s = #moon %s" % (O, O), "scoreboard players set #15 %s 15" % O,
                   "scoreboard players operation #q %s %%= #15 %s" % (O, O),
                   "execute if score #q %s matches 0 " % O + "in %s positioned 0 83 0 as @a[distance=%d..,gamemode=!spectator,gamemode=!creative] at @s run function %s/moon_wave" % (DIM, GATE_R + 8, P),
                   "execute if score #moon %s matches 0 in %s positioned 0 83 0 run " % (O, DIM) + ev("血月", "Blood Moon", "血停了。", "@a[distance=0..]")])
    wave = ["# 血月：身边多刷三只"]
    for i, m in enumerate(("zombie", "skeleton", "spider")):
        wave += ["summon minecraft:%s ~ ~ ~ {Tags:[\"rpg.pl.new\"]}" % m, "spreadplayers ~ ~ 2 18 under 200 false @e[type=minecraft:%s,tag=rpg.pl.new,limit=1]" % m,
                 "tag @e[tag=rpg.pl.new] remove rpg.pl.new"]
    fn("moon_wave", wave)
    # 生命树
    fn("tree/use", ["# 右键生命树（as 玩家）：每天献一次",
                    "execute store result score #d %s run time query day" % O,
                    "execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_mat:\"pl_fruit\"}] run return run function %s/tree/fruit" % P,
                    "execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_mat:\"pl_mud\"}] run return run function %s/tree/mud" % P,
                    "execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_mat:\"pl_feather\"}] run return run function %s/tree/feather" % P,
                    say("枯死的生命树。手里拿着禁果、血泥或断羽再来，每天一次。")])
    for k, attr, val, text in (("fruit", "attack_damage", "0.1 add_multiplied_base", "攻击 +10%，一小时"), ("mud", "max_health", "8 add_value", "生命 +8，一小时"),
                               ("feather", "movement_speed", "0.1 add_multiplied_base", "移速 +10%，一小时")):
        fn("tree/" + k, ["execute if score @s rpg_pl_tree = #d %s run return run %s" % (O, say("今天已经献过了。")),
                         "scoreboard players operation @s rpg_pl_tree = #d %s" % O,
                         'item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}',
                         "attribute @s minecraft:%s modifier remove rpg:pl_tree" % attr, "attribute @s minecraft:%s modifier add rpg:pl_tree %s" % (attr, val),
                         "scoreboard players set @s rpg_pl_tb 3600",
                         "execute at @s run particle minecraft:end_rod ~ ~1 ~ 0.5 1 0.5 0.02 60", "playsound minecraft:block.beacon.power_select player @s ~ ~ ~ 1 1.2",
                         say("生命树收下了%s：%s。" % (RELICS[k][0], text)), "function rpg:quest/hook/tree"])
    s = read("pl/load.mcfunction")
    write("pl/load.mcfunction", s + "scoreboard objectives add rpg_pl_tb dummy\n")
    s = read("pl/tick.mcfunction")
    write("pl/tick.mcfunction", s + "execute if score #t %s matches 10 run scoreboard players remove @a[scores={rpg_pl_tb=1..}] rpg_pl_tb 1\n" % O +
          "execute if score #t %s matches 11 as @a[scores={rpg_pl_tb=0}] run function %s/tree/off\n" % (O, P))
    fn("tree/off", ["scoreboard players reset @s rpg_pl_tb"] + ["attribute @s minecraft:%s modifier remove rpg:pl_tree" % a for a in ("attack_damage", "max_health", "movement_speed")])


# ============================================================================ 首领血条（守关者、基路伯、堡主）
def bossbar():
    for k, en in BOSSES.items():
        fn("bar/" + k, ["# %s 的位图血条（as/at 它）" % en,
                        "execute store result score #h rpg_el run data get entity @s Health 20",
                        "execute store result score #mh rpg_el run attribute @s minecraft:max_health get",
                        "scoreboard players operation #h rpg_el /= #mh rpg_el"] +
           ["execute if score #h rpg_el matches %d run data modify storage rpg:elite t.st set value \"%s\"" % (i, BA.char(i)) for i in range(21)] +
           ["data modify storage rpg:elite t.i1 set value \"%s\"" % BA.icon(0), "data modify storage rpg:elite t.i2 set value \"%s\"" % BA.icon(0),
            "data modify storage rpg:elite t.bb set value \"%s\"" % BA.back_char(k), "data modify storage rpg:elite t.bn set value \"%s\"" % BA.name_char(k),
            "data modify storage rpg:elite t.bo set value \"%s\"" % BA.on_char(k),
            "function rpg:elite/bar_set with storage rpg:elite t", "bossbar set rpg:elite_champion_bar players @a[distance=..32]"])
    patch("elite/sec.mcfunction", "rpg:pl/bar/all", "function rpg:pl/bar/all\n")
    fn("bar/all", ["execute as @e[tag=rpg.pl.b.%s] at @s if entity @a[distance=..32] run function %s/bar/%s" % (k, P, k) for k in BOSSES])


# ============================================================================ 河庭
def courts():
    champ = ["summon minecraft:husk ~ ~1 ~ {Tags:[\"rpg.pl.g\",\"rpg.pl.s\",\"rpg.pl.gn\"],PersistenceRequired:1b}",
             "scoreboard players set #sef rpg_el 8",
             "execute as @e[tag=rpg.pl.gn] at @s run function rpg:elite/make",
             "execute as @e[tag=rpg.pl.gn,tag=!rpg.el.boss] at @s run function rpg:elite/champion",
             "execute as @e[tag=rpg.pl.gn] at @s run function rpg:elite/stats",
             "execute as @e[tag=rpg.pl.gn] at @s run function rpg:elite/name_pick",
             "tag @e[tag=rpg.pl.gn] remove rpg.pl.gn"]
    fn("court/champ", champ)
    warden = ('summon minecraft:zombie_villager ~ ~1 ~ {Tags:["rpg.pl.g","rpg.pl.s","rpg.pl.b.warden"],PersistenceRequired:1b,CustomNameVisible:1b,CustomName:%s,'
              'VillagerData:{type:"minecraft:taiga",profession:"minecraft:armorer",level:5},Health:150f,'
              'active_effects:[{id:"wind_charged",duration:-1,amplifier:2,ambient:1b,show_particles:1b}],'
              'equipment:{mainhand:{id:"minecraft:iron_sword",count:1},offhand:{id:"minecraft:shield",count:1},feet:{id:"minecraft:netherite_boots",count:1},'
              'legs:{id:"minecraft:chainmail_leggings",count:1},chest:{id:"minecraft:chainmail_chestplate",count:1},head:{id:"minecraft:iron_helmet",count:1}},'
              'drop_chances:{mainhand:0f,offhand:0f,feet:0f,legs:0f,chest:0f,head:0f},'
              'attributes:[{id:"minecraft:attack_damage",base:7d},{id:"minecraft:max_health",base:150d},{id:"minecraft:scale",base:1.2d}]}'
              % J(["", seg(ui.fraktur(BOSSES["warden"]), ui.WHITE)]))
    fn("court/guard_1", ["function %s/court/champ" % P])
    fn("court/guard_2", [warden])
    fn("court/guard_3", ["function rpg:holy_guard/summon", "execute positioned ~4 ~ ~ run function rpg:holy_guard/summon",
                         "tag @e[tag=rpg.hg,distance=..10] add rpg.pl.g"])
    lords = [p["slug"] for p in ui.PILLARS]
    import add_demon_minions as DM
    g4 = ["# 随机一柱的五名罪仆", "execute store result score #l %s run random value 1..7" % O]
    for i, slug in enumerate(lords, 1):
        g4.append("execute if score #l %s matches %d run function rpg:minion/summon/%s/all" % (O, i, slug))
    g4.append("tag @e[tag=rpg.demon.minion,distance=..14] add rpg.pl.g")
    fn("court/guard_4", g4)
    for k, (name, en, x, z, omen, total, tadd, simul, sadd, mobs, hp, atk, pots) in COURTS.items():
        base = (k - 1) * 5
        UP = CENTRE[k][6]                     # 刷怪笼在祭坛顶上
        at = IN + "positioned %d %d %d " % (x, FLOOR + 1, z)
        d = "court/%d/" % k
        # 状态：0 空、1 打、2 歇、3 冷却
        fn(d + "try", ["# 有人走近（at 中心）：过了前一座的人在场才开",
                       "execute unless entity @a[distance=..12,gamemode=!spectator,scores={rpg_pl_best=%d..}] run return run title @a[distance=..12] actionbar %s" % (base, J(["", seg("先过前一座河庭", ui.BROADCAST_BODY)])) if base else
                       "execute unless entity @a[distance=..12,gamemode=!spectator] run return 0",
                       "scoreboard players set #l%d %s 1" % (k, O), "scoreboard players set #f%d %s 0" % (k, O),
                       "function %s/court/%d/layer" % (P, k)])
        pot = []
        pot_nbt = {}
        for key in pots:
            if key == "harm":
                pot_nbt[key] = '{id:"minecraft:lingering_potion",count:1,components:{"minecraft:potion_contents":{potion:"minecraft:strong_harming"}}}'
            else:
                use = PS.POTIONS[key]
                effs = ",".join('{id:"minecraft:%s",duration:%d,amplifier:%d}' % (e, dd, a) for e, dd, a in use[4])
                pot_nbt[key] = '{id:"minecraft:lingering_potion",count:1,components:{"minecraft:potion_contents":{custom_color:%d,custom_effects:[%s]}}}' % (use[3], effs)
        drops = [("wind", '{id:"minecraft:wind_charge",count:1}')] * 2 + list(pot_nbt.items())
        offs = [(3, 6, 3, 100), (-3, 7, 4, 120), (1, 5, -5, 50), (-4, 6, -3, 80), (6, 7, -5, 150), (-5, 5, 5, 110)]
        spawn_lines = []
        for i, (_n, it) in enumerate(drops):
            ox, oy, oz, t = offs[i % len(offs)]
            ox, oz, oy = round(ox * CENTRE[k][4]), round(oz * CENTRE[k][4]), min(oy, 6)
            spawn_lines.append("summon minecraft:ominous_item_spawner ~%d ~%d ~%d {item:%s,spawn_item_after_ticks:%dL}" % (ox, oy, oz, it, t))
        pots_list = ",".join("{data:{entity:%s},weight:%d}" % (mob_nbt(m, hp, atk), w) for m, w in mobs)
        first = mob_nbt(mobs[0][0], hp, atk)
        cfg = ("{spawn_potentials:[%s],loot_tables_to_eject:[{data:\"rpg:paradise/court_%d\",weight:1}],simultaneous_mobs:%df,simultaneous_mobs_added_per_player:%df,"
               "ticks_between_spawn:6,total_mobs:%df,total_mobs_added_per_player:%df,spawn_range:%d}" % (pots_list, k, simul, sadd, total, tadd, CENTRE[k][3]))
        key = "ominous_config" if omen else "normal_config"
        layer = ["# 开一层（at 中心）", "scoreboard players set #c%d %s 1" % (k, O), "scoreboard players set #r%d %s 0" % (k, O),
                 "scoreboard players operation #n %s = #l%d %s" % (O, k, O), "scoreboard players add #n %s %d" % (O, base),
                 "execute store result storage rpg:paradise c.n int 1 run scoreboard players get #n %s" % O,
                 "setblock ~ ~%d ~ minecraft:air" % UP,
                 "setblock ~ ~%d ~ minecraft:trial_spawner[ominous=%s]{%s:%s,spawn_data:{entity:%s},required_player_range:16,target_cooldown_length:36000}" % (UP, "true" if omen else "false", key, cfg, first),
                 "effect give @a[distance=..24] minecraft:instant_health 1 1 true",
                 "execute as @a[distance=..24,scores={rpg_force=1}] run scoreboard players add @s rpg_mana 20",
                 "execute as @a[distance=..24,scores={rpg_force=2..3}] run scoreboard players add @s rpg_mana 20",
                 "particle minecraft:trial_spawner_detection%s ~ ~2 ~ 1 1 1 0.2 200" % ("_ominous" if omen else ""),
                 "function %s/court/%d/title with storage rpg:paradise c" % (P, k)] + spawn_lines + [
                 "execute if score #l%d %s matches 5 positioned ~ ~ ~%d run function %s/court/guard_%d" % (k, O, CENTRE[k][5], P, k),
                 "execute if score #l%d %s matches 1 as @a[distance=..24] at @s run playsound rpg:bgm.prologue_waves record @s ~ ~ ~ 0.6 1" % (k, O)]
        fn(d + "layer", layer)
        fn(d + "title", ["title @a[distance=..24] times 5 40 10", "title @a[distance=..24] title " + J(["", seg("试炼之室", COL, True), seg(" " + ui.fraktur("Trial"), ui.BROADCAST_GLOSS)]),
                         "$title @a[distance=..24] subtitle " + J(["", seg("%s河庭　" % name, ui.BROADCAST_BODY), seg("第 $(n) 层", ui.BROADCAST_NAME, True)])])
        fn(d + "sec", ["# 每秒（1 打、2 歇、3 冷却）", at + "run function %s/court/%d/sec_at" % (P, k)])
        fn(d + "sec_at", [
            "execute if score #c%d %s matches 1..2 unless entity @a[distance=..32,gamemode=!spectator] run scoreboard players add #f%d %s 1" % (k, O, k, O),
            "execute if entity @a[distance=..32,gamemode=!spectator] run scoreboard players set #f%d %s 0" % (k, O),
            "execute if score #f%d %s matches 60.. run return run function %s/court/%d/fail" % (k, O, P, k),
            "execute if score #c%d %s matches 1 if block ~ ~%d ~ minecraft:trial_spawner[trial_spawner_state=cooldown] unless entity @e[tag=rpg.pl.g,distance=..28] run return run function %s/court/%d/clear" % (k, O, UP, P, k),
            "execute if score #c%d %s matches 2.. run scoreboard players add #r%d %s 1" % (k, O, k, O),
            "execute if score #c%d %s matches 2 if score #r%d %s matches 8.. run return run function %s/court/%d/next" % (k, O, k, O, P, k),
            "execute if score #c%d %s matches 3 if score #r%d %s matches 300.. run scoreboard players set #c%d %s 0" % (k, O, k, O, k, O)])
        fn(d + "clear", ["# 这一层过了（at 中心）", "scoreboard players set #c%d %s 2" % (k, O), "scoreboard players set #r%d %s 0" % (k, O),
                         "execute as @a[distance=..32,gamemode=!spectator] run scoreboard players add @s rpg_ex_xp 3",
                         "execute as @a[distance=..32,gamemode=!spectator] run function rpg:events/bt/trial",
                         "playsound minecraft:block.trial_spawner.about_to_spawn_item master @a[distance=..32] ~ ~ ~ 1 1.2",
                         "execute if score #l%d %s matches 5.. run function %s/court/%d/done" % (k, O, P, k)])
        fn(d + "next", ["scoreboard players add #l%d %s 1" % (k, O), "function %s/court/%d/layer" % (P, k)])
        summit = ["execute as @a[distance=..32,gamemode=!spectator] unless entity @s[tag=rpg.t.summit] run function %s/summit" % P] if k == 4 else []
        fn(d + "done", ["# 一座河庭打完（at 中心）", "scoreboard players set #c%d %s 3" % (k, O), "setblock ~ ~%d ~ minecraft:air" % UP,
                        "execute as @a[distance=..32,gamemode=!spectator] run loot give @s loot rpg:trial/%s" % ("ominous_key" if omen else "key"),
                        "execute as @a[distance=..32,gamemode=!spectator] run scoreboard players add @s rpg_ex_xp 12",
                        "execute as @a[distance=..32,gamemode=!spectator] if score @s rpg_pl_best matches ..%d run scoreboard players set @s rpg_pl_best %d" % (k * 5 - 1, k * 5)] + summit + [
                        "stopsound @a[distance=..48] record rpg:bgm.prologue_waves",
                        ev(name + "河庭", en, "五层都过了。宝库在南边，钥匙已经给你。", "@a[distance=..48]")] +
           (["execute as @a[distance=..32,gamemode=!spectator] run function rpg:quest/hook/court"] if k == 1 else []))
        fn(d + "fail", ["scoreboard players set #c%d %s 0" % (k, O), "scoreboard players set #f%d %s 0" % (k, O), "setblock ~ ~%d ~ minecraft:air" % UP,
                        "kill @e[%s,distance=..26]" % HUNT, "execute as @e[tag=rpg.pl.g,distance=..30] run tp @s ~ -200 ~", "stopsound @a[distance=..64] record rpg:bgm.prologue_waves"])
    fn("summit", ["scoreboard players add @s rpg_ex_xp 50", "function rpg:quest/title/get_summit", "loot give @s loot rpg:world/bp_epic_any",
                  ev("登顶", "Summit", "二十层都在你脚下。", "@a[distance=0..]")])


def mob_nbt(m, hp, atk):
    eq = {"zombie": 'equipment:{mainhand:{id:"minecraft:iron_sword",count:1},head:{id:"minecraft:iron_helmet",count:1}},',
          "husk": 'equipment:{mainhand:{id:"minecraft:iron_axe",count:1},chest:{id:"minecraft:iron_chestplate",count:1}},',
          "skeleton": 'equipment:{mainhand:{id:"minecraft:bow",count:1},head:{id:"minecraft:chainmail_helmet",count:1}},',
          "stray": 'equipment:{mainhand:{id:"minecraft:bow",count:1},head:{id:"minecraft:iron_helmet",count:1}},',
          "bogged": 'equipment:{mainhand:{id:"minecraft:bow",count:1}},',
          "wither_skeleton": 'equipment:{mainhand:{id:"minecraft:stone_sword",count:1}},',
          "vindicator": 'equipment:{mainhand:{id:"minecraft:iron_axe",count:1}},',
          "pillager": 'equipment:{mainhand:{id:"minecraft:crossbow",count:1}},'}.get(m, "")
    return ('{id:"minecraft:%s",%sdrop_chances:{mainhand:0f,offhand:0f,head:0f,chest:0f},Health:%df,attributes:[{id:"minecraft:max_health",base:%dd},{id:"minecraft:attack_damage",base:%dd}]}'
            % (m, eq, hp, hp, atk))


# ============================================================================ 基路伯与堡主
def wanderers():
    fn("cherub/sec", ["scoreboard players add #ch %s 1" % O,
                      "execute unless score #ch %s matches 2400.. run return 0" % O,
                      "execute if entity @e[tag=rpg.pl.b.cherub] run return run scoreboard players set #ch %s 0" % O,
                      IN + "unless entity @a[distance=%d..,gamemode=!spectator] run return 0" % ZONE_R[1],
                      "scoreboard players set #ch %s 0" % O,
                      IN + "as @r[distance=%d..,gamemode=!spectator] at @s run function %s/cherub/spawn" % (ZONE_R[1], P)])
    fn("cherub/spawn", ["# 在这名玩家附近落下（as/at 玩家）",
                        "summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.pl.cm\"]}", "spreadplayers ~ ~ 4 24 under 200 false @e[type=minecraft:marker,tag=rpg.pl.cm,limit=1]",
                        "execute at @e[type=minecraft:marker,tag=rpg.pl.cm,limit=1] run function rpg:royal_guard/summon",
                        "execute at @e[type=minecraft:marker,tag=rpg.pl.cm,limit=1] as @e[tag=rpg.rg,distance=..6,limit=1,sort=nearest] run function %s/cherub/make" % P,
                        "kill @e[type=minecraft:marker,tag=rpg.pl.cm]",
                        IN + "run " + ev("基路伯", "Cherub", "四面转动的火焰的剑，落在了灰烬边境。", "@a[distance=0..]")])
    fn("cherub/make", ["tag @s add rpg.pl.b.cherub", "tag @s add rpg.pl.g", "attribute @s minecraft:max_health base set 320", "attribute @s minecraft:attack_damage base set 12",
                       "data modify entity @s Health set value 320f", "data modify entity @s CustomNameVisible set value 1b",
                       "data modify entity @s CustomName set value " + J(["", seg(ui.fraktur(BOSSES["cherub"]), ui.WHITE)]),
                       "particle minecraft:flame ~ ~1 ~ 1 2 1 0.1 120", "playsound minecraft:item.trident.thunder master @a[distance=..48] ~ ~ ~ 1 0.8"])
    for k, lootn, extra in (("cherub", "rpg:paradise/cherub", ["function rpg:quest/hook/cherub", "scoreboard players add @s rpg_ex_xp 20"]),
                            ("castellan", "rpg:trial/ominous_key", ["loot give @s loot rpg:elite/badge"] * 5 + ["scoreboard players add @s rpg_ex_xp 15"])):
        wj(os.path.join(DP, "data", "rpg", "advancement", "paradise", k + ".json"), {
            "criteria": {"kill": {"trigger": "minecraft:player_killed_entity", "conditions": {"entity": [
                {"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"nbt": "{Tags:[\"rpg.pl.b.%s\"]}" % k}}]}}},
            "rewards": {"function": "%s/%s_dead" % (P, k)}})
        fn("%s_dead" % k, ["advancement revoke @s only rpg:paradise/" + k, "loot give @s loot " + lootn] + extra)
    # 堡垒的分布：换成同心环，离门 400 格左右才有第一圈，不会压到伊甸之门和河庭（Antigravity 交的是随机散布）
    sset = os.path.join(DP, "data", "rpg", "worldgen", "structure_set", "paradise", "fortress.json")
    if os.path.exists(sset):
        wj(sset, {"structures": [{"structure": "rpg:paradise/fortress", "weight": 1}],
                  "placement": {"type": "minecraft:concentric_rings", "distance": 7, "spread": 4, "count": 90,
                                "preferred_biomes": "rpg:paradise_lost", "salt": 1795411}})
    # 堡主：玩家走进黑石堡垒（结构由 add_blackstone_fortress.py 生成），每人每天召一次
    if os.path.exists(os.path.join(DP, "data", "rpg", "worldgen", "structure", "paradise", "fortress.json")):
        wj(os.path.join(DP, "data", "rpg", "predicate", "paradise", "in_fortress.json"), {
            "condition": "minecraft:location_check", "predicate": {"structures": "rpg:paradise/fortress", "position": {"y": {"min": 120}}}})      # 柱子底下的地面不算进堡垒
        s = read("pl/sec.mcfunction")
        write("pl/sec.mcfunction", s + "execute store result score #d %s run time query day\n" % O +
              "execute in %s as @a[x=0,y=83,z=0,distance=%d..,gamemode=!spectator] unless score @s rpg_pl_fort = #d %s at @s if predicate rpg:paradise/in_fortress run function %s/fortress/enter\n" % (DIM, GATE_R, O, P))
        s = read("pl/load.mcfunction")
        write("pl/load.mcfunction", s + "scoreboard objectives add rpg_pl_fort dummy\n")
        fn("fortress/enter", ["scoreboard players operation @s rpg_pl_fort = #d %s" % O,
                              "execute if entity @e[tag=rpg.pl.b.castellan,distance=..64] run return 0",
                              "# 堡垒悬在一百格高处：就落在玩家身前两格，别掉下去",
                              "execute rotated ~ 0 positioned ^ ^ ^2 run function %s/fortress/castellan" % P,
                              ev("堡主", "Castellan", "黑石堡垒的主人听见了脚步声。", "@a[distance=..64]")])
    fn("fortress/castellan", ["# 在执行位置落一名堡主",
        'summon minecraft:wither_skeleton ~ ~ ~ {Tags:["rpg.pl.g","rpg.pl.s","rpg.pl.b.castellan"],PersistenceRequired:1b,CustomNameVisible:1b,CustomName:%s,Health:220f,'
        'equipment:{mainhand:{id:"minecraft:netherite_sword",count:1},chest:{id:"minecraft:netherite_chestplate",count:1},head:{id:"minecraft:netherite_helmet",count:1}},'
        'drop_chances:{mainhand:0f,chest:0f,head:0f},attributes:[{id:"minecraft:max_health",base:220d},{id:"minecraft:attack_damage",base:11d},{id:"minecraft:scale",base:1.25d}]}'
        % J(["", seg(ui.fraktur(BOSSES["castellan"]), ui.WHITE)])])


# ============================================================================ 悬赏、支线、旅程（挂到别的生成器的产物上）
def hooks():
    for name, txt in (("trial", "通过试炼"), ("paradise", "失乐园"), ("paradise_champ", "失乐园首领")):
        p = os.path.join(FUNC, "events", "bt", name + ".mcfunction")
        assert os.path.exists(p), "add_events 里要有悬赏 %s" % name


def main():
    import shutil
    shutil.rmtree(os.path.join(FUNC, "pl"), ignore_errors=True)
    n = paradise_world.write(DP)
    loots()
    vaults()
    building()
    travel()
    panel()
    hunt()
    bossbar()
    courts()
    wanderers()
    hooks()
    print("paradise: %d functions, %d worldgen files, %d courts" % (COUNT, n, len(COURTS)))


if __name__ == "__main__":
    main()
