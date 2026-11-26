# -*- coding: utf-8 -*-
"""达阿特试炼：维度、场地、进出、快照、夺走物品的归还（docs/DAATH-DESIGN.md §3、§4.1、§4.2、§4.10）。"""
import math
import os

import add_daath_art as art
from add_sephira_tiers import TIERS as SEPH
from daath_lib import *  # noqa: F401,F403
from daath_lib import B, DIM, DP, FLOOR, GAP, LAMP_R, LIGHT_R, ME, O, POOL_R, R, SLOTS, UNIT, at, line, msg, snd, txt, ui, w, wf, wj

# 倒着的生命之树（俯视，水下 12 格）：王冠在北、王国在南的真树上下颠倒
TREE = {  # 源质: (x, z, 玻璃)
    "kether": (0, 18, "white"), "chokmah": (8, 11, "light_gray"), "binah": (-8, 11, "gray"),
    "chesed": (8, 3, "light_blue"), "geburah": (-8, 3, "red"), "tiphareth": (0, -5, "yellow"),
    "netzach": (8, -10, "lime"), "hod": (-8, -10, "orange"), "yesod": (0, -14, "purple"), "malkuth": (0, -20, "brown")}
PATHS = [("kether", "chokmah"), ("kether", "binah"), ("kether", "tiphareth"), ("chokmah", "binah"), ("chokmah", "chesed"), ("chokmah", "tiphareth"),
         ("binah", "geburah"), ("binah", "tiphareth"), ("chesed", "geburah"), ("chesed", "tiphareth"), ("chesed", "netzach"), ("geburah", "tiphareth"),
         ("geburah", "hod"), ("tiphareth", "netzach"), ("tiphareth", "yesod"), ("tiphareth", "hod"), ("netzach", "hod"), ("netzach", "yesod"),
         ("netzach", "malkuth"), ("hod", "yesod"), ("hod", "malkuth"), ("yesod", "malkuth")]
# 十盏灯：从北开始顺时针，颜色取源质
LAMPS = ["kether", "chokmah", "chesed", "netzach", "tiphareth", "malkuth", "yesod", "hod", "geburah", "binah"]
TREE_Y = FLOOR - 13


def lamp_xy(i, r=LAMP_R):
    a = 2 * math.pi * i / 10 - math.pi / 2
    return r * math.cos(a), r * math.sin(a)


def dimension():
    d = os.path.join(DP, "data", "rpg")
    wj(os.path.join(d, "dimension_type", "daath.json"), {
        "ambient_light": 0.05,
        "attributes": {
            "minecraft:gameplay/bed_rule": {"can_set_spawn": "never", "can_sleep": "never", "explodes": False},
            "minecraft:gameplay/respawn_anchor_works": False, "minecraft:gameplay/can_start_raid": False,
            "minecraft:visual/sky_color": "#59626f", "minecraft:visual/fog_color": "#4e5663",
            "minecraft:visual/fog_start_distance": 10.0, "minecraft:visual/fog_end_distance": 70.0,
            "minecraft:gameplay/monsters_burn": False},
        "coordinate_scale": 1.0, "has_ceiling": False, "has_fixed_time": True, "has_skylight": False, "height": 256,
        "infiniburn": "#minecraft:infiniburn_overworld", "logical_height": 256, "min_y": 0,
        "monster_spawn_block_light_limit": 0, "monster_spawn_light_level": 0, "skybox": "none"})
    wj(os.path.join(d, "dimension", "daath.json"), {"type": "rpg:daath", "generator": {"type": "minecraft:flat", "settings": {
        "biome": "rpg:daath", "features": False, "lakes": False, "layers": [{"block": "minecraft:air", "height": 1}], "structure_overrides": []}}})
    wj(os.path.join(d, "worldgen", "biome", "daath.json"), {
        "has_precipitation": False, "temperature": 0.5, "downfall": 0.0,
        "attributes": {"minecraft:visual/sky_color": "#59626f", "minecraft:visual/fog_color": "#4e5663",
                       "minecraft:visual/ambient_particles": [{"particle": {"type": "minecraft:white_ash"}, "probability": 0.004}],
                       "minecraft:audio/ambient_sounds": {"loop": "minecraft:ambient.underwater.loop"}},
        "effects": {"water_color": "#0b0c10", "grass_color": "#2a2e38", "foliage_color": "#2a2e38", "dry_foliage_color": "#2a2e38"},
        "spawners": {k: [] for k in ("monster", "creature", "ambient", "axolotls", "underground_water_creature", "water_creature",
                                     "water_ambient", "misc")},
        "spawn_costs": {}, "carvers": [], "features": []})
    wj(os.path.join(d, "damage_type", "daath.json"), {"message_id": "daath", "scaling": "never", "exhaustion": 0.0, "effects": "hurt"})
    for t in ("bypasses_armor", "bypasses_cooldown", "bypasses_enchantments"):
        p = os.path.join(DP, "data", "minecraft", "tags", "damage_type", t + ".json")
        import io
        import json
        doc = json.load(io.open(p, encoding="utf-8"))
        if "rpg:daath" not in doc["values"]:
            doc["values"].append("rpg:daath")
        wj(p, doc)
    wj(os.path.join(d, "tags", "item", "daath", "weapon.json"), {"values": [
        "#minecraft:swords", "#minecraft:axes", "#minecraft:spears", "#minecraft:hoes", "minecraft:mace", "minecraft:trident", "minecraft:bow",
        "minecraft:crossbow"]})


def arena():
    """一块场地（at 场地中心，水面上一格）：黑玻璃水面、倒树、十根灯柱。"""
    c = ["# 场地（positioned 场地中心）", "fill ~-22 ~-18 ~-22 ~22 ~-2 ~0 minecraft:air", "fill ~-22 ~-18 ~1 ~22 ~-2 ~22 minecraft:air"]
    for x in range(-R, R + 1):
        h = int(math.floor(math.sqrt(max(0, (R + 0.5) ** 2 - x * x))))
        c.append("fill ~%d ~-1 ~%d ~%d ~-1 ~%d minecraft:black_stained_glass" % (x, -h, x, h))
    # 水面底下是一只黑色的深桶：侧壁与桶底全黑，倒树在里面发光
    for x in range(-R - 2, R + 3):
        def half(rr):
            v = (rr + 0.5) ** 2 - x * x
            return int(math.floor(math.sqrt(v))) if v >= 0 else -1
        a, b = half(R + 1), half(R)
        if a >= 0:
            c.append("fill ~%d ~-19 ~%d ~%d ~-19 ~%d minecraft:black_concrete" % (x, -a, x, a))
            lo = b + 1 if b >= 0 else 0
            c += ["fill ~%d ~-18 ~%d ~%d ~-1 ~%d minecraft:black_concrete" % (x, lo, x, max(lo, a)), "fill ~%d ~-18 ~%d ~%d ~-1 ~%d minecraft:black_concrete" % (x, -max(lo, a), x, -lo)]
    for i, k in enumerate(LAMPS):
        x, z = lamp_xy(i)
        X, Z = int(round(x)), int(round(z))
        c += ["fill ~%d ~ ~%d ~%d ~2 ~%d minecraft:polished_blackstone_wall" % (X, Z, X, Z),
              "setblock ~%d ~3 ~%d minecraft:%s_stained_glass" % (X, Z, TREE[k][2]),
              "setblock ~%d ~4 ~%d minecraft:polished_blackstone_slab" % (X, Z)]
    c += ["# 很弱的底光：看得见水面", "setblock ~ ~9 ~ minecraft:light[level=14]"]
    for i in range(6):
        a = 2 * math.pi * i / 6
        c.append("setblock ~%d ~8 ~%d minecraft:light[level=13]" % (round(13 * math.cos(a)), round(13 * math.sin(a))))
    w("arena/build", c)
    # 机关：中心标记、十盏灯的交互体
    s = ["# 场次开始：中心标记与十盏灯（positioned 场地中心）", "kill @e[type=minecraft:interaction,tag=rpg.dt.lamp,distance=..60]",
         "kill @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60]",
         "summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.dt.c\"]}"]
    for i, k in enumerate(LAMPS):
        x, z = lamp_xy(i)
        X, Z = int(round(x)), int(round(z))
        s.append("summon minecraft:interaction ~%d ~ ~%d {Tags:[\"rpg.dt.lamp\",\"rpg.dt.l%d\"],width:1.5f,height:4.2f,response:1b}" % (X, Z, i))
    s.append("function %s/arena/tree" % B)
    w("arena/props", s)
    # 倒树：原质是法阵贴图，路径是贴图带（用户 2026-11-25）。Codex 的 daath_ref/tree/ 来了就用那套
    y = TREE_Y - FLOOR
    col = {k: int(c[1:], 16) for _n, k, _zh, _la, _he, c, _pl in SEPH}
    inner = {0: "hexagram", 1: "sigil", 2: "hexagon"}
    tr = ["# 倒着的生命之树（positioned 场地中心）", "kill @e[type=minecraft:item_display,tag=rpg.dt.tree,distance=..60]"]

    def plane(model, x, z, dy, size, color, tags="", yaw=0.0, sx=None):
        return ("summon minecraft:item_display ~%.3f ~%.3f ~%.3f {Tags:[\"rpg.dt.tree\"%s],item:{id:\"minecraft:paper\",count:1,components:{\"minecraft:item_model\":\"%s\",\"minecraft:custom_model_data\":{colors:[%d]}}},"
                "brightness:{sky:15,block:15},teleport_duration:3,view_range:3f,Rotation:[%.2ff,0f],transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[%gf,1f,%gf],right_rotation:[0f,0f,0f,1f]}}"
                % (x, y + dy, z, tags, model, color, yaw, sx or size, size))
    for a, b in PATHS:
        (x0, z0, _), (x1, z1, _) = TREE[a], TREE[b]
        L = math.hypot(x1 - x0, z1 - z0)
        ux, uz = (x1 - x0) / L, (z1 - z0) / L
        gap = 2.7                                  # 两头让开法阵
        ln = L - 2 * gap
        yaw = math.degrees(math.atan2(-ux, uz))
        # 用户 2026-11-25：路径换成扫罗突进那条预警线的贴图（usurper_fx/beam，0x8C96A2）
        tr.append("summon minecraft:item_display ~%.3f ~%.3f ~%.3f {Tags:[\"rpg.dt.tree\"],item:{id:\"minecraft:paper\",count:1,components:{\"minecraft:item_model\":\"rpg:usurper_fx/beam\",\"minecraft:custom_model_data\":{colors:[%d]}}},"
                  "brightness:{sky:15,block:15},view_range:3f,Rotation:[%.2ff,0f],transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.6f,0.02f,%gf],right_rotation:[0f,0f,0f,1f]}}"
                  % ((x0 + x1) / 2.0, y, (z0 + z1) / 2.0, 0x8C96A2, yaw, ln))
    for k, (x, z, _g) in TREE.items():
        c_, pl = col[k], next(p[6] for p in SEPH if p[1] == k)
        own = art.tree(k)
        if own:
            tr += [plane("rpg:usurper_fx/glow", x, z, 0.02, 6.4, c_), plane(own, x, z, 0.06, 5.6, 0xFFFFFF, ',\"rpg.dt.trs\"')]
        else:
            tr += [plane("rpg:usurper_fx/glow", x, z, 0.02, 6.2, c_), plane("rpg:usurper_fx/ring", x, z, 0.05, 5.8, c_),
                   plane("rpg:usurper_fx/" + inner[pl], x, z, 0.08, 4.6, c_, ',\"rpg.dt.trs\"'), plane("rpg:usurper_fx/hexagram", x, z, 0.11, 2.6, 0xFFFFFF, ',\"rpg.dt.trr\"')]
    # 第十一个：达阿特，只有一圈淡影，接纳以后才亮
    tr += [plane(art.tree("daath") or "rpg:daath_fx/seal_daath", 0, 3.5, 0.05, 4.6, 0xFFFFFF if art.tree("daath") else 0x6A7280, ',\"rpg.dt.trd\"')]
    w("arena/tree", tr)
    w("arena/tree_lit", ["# 达阿特亮了（positioned 场地中心）", "kill @e[type=minecraft:item_display,tag=rpg.dt.trd,distance=..40]",
                         plane("rpg:usurper_fx/glow", 0, 3.5, 0.03, 6.4, 0xFFF2A8), plane(art.tree("daath_lit") or "rpg:daath_fx/seal_daath_lit", 0, 3.5, 0.08, 5.4, 0xFFFFFF, ',\"rpg.dt.trs\"'),
                         plane("rpg:usurper_fx/ring", 0, 3.5, 0.06, 6.2, 0xFFF2A8)])


def travel():
    load = ["scoreboard objectives add %s dummy" % s for s in (
        O, "rpg_dt_sid", "rpg_dt_ph", "rpg_dt_pt", "rpg_dt_cd", "rpg_dt_n", "rpg_dt_cast", "rpg_dt_drk", "rpg_dt_win",
        "rpg_dt_life", "rpg_dt_kd", "rpg_dt_st", "rpg_dt_h", "rpg_dt_mx", "rpg_dt_sk", "rpg_dt_t", "rpg_dt_gap", "rpg_dt_cl", "rpg_dt_ht", "rpg_dt_ln",
        "rpg_dt_sh", "rpg_dt_pc", "rpg_dt_id", "rpg_dt_wc", "rpg_dt_far", "rpg_dt_still", "rpg_dt_mel", "rpg_dt_melt", "rpg_dt_same", "rpg_dt_slot",
        "rpg_dt_ek", "rpg_dt_et", "rpg_dt_eid", "rpg_dt_esm", "rpg_dt_ult", "rpg_dt_scd", "rpg_dt_gcd", "rpg_dt_lit", "rpg_dt_blade", "rpg_dt_sw", "rpg_dt_sa", "rpg_dt_sp",
        "rpg_dt_lt", "rpg_dt_i", "rpg_dt_bar", "rpg_dt_px", "rpg_dt_pz", "rpg_dt_shell", "rpg_dt_tries", "rpg_dt_e", "rpg_dt_q", "rpg_dt_bgm", "rpg_dt_die",
        "rpg_dt_pcd", "rpg_dt_got", "rpg_dt_dsp", "rpg_dt_orb", "rpg_dt_rd", "rpg_dt_say")]
    load += ["scoreboard objectives add rpg_dt_de minecraft.custom:minecraft.deaths",
             "scoreboard objectives add rpg_dt_dc deathCount",
             "scoreboard players set #100 %s 100" % O, "scoreboard players set #10 %s 10" % O, "scoreboard players set #12 %s 12" % O, "scoreboard players set #13 %s 13" % O, "scoreboard players set #8 %s 8" % O]
    for n in range(1, SLOTS + 1):
        load += ["bossbar add rpg:daath_%d \"影\"" % n, "bossbar set rpg:daath_%d color pink" % n, "bossbar set rpg:daath_%d style notched_20" % n]
    w("load", load)

    # ------------------------------------------------ 进场
    blocked = [("if entity @s[tag=rpg.pr]", "序章还没结束。"), ("if entity @s[tag=rpg.ob.hold]", "先走完开局。"),
               ("if entity @s[tag=rpg.pl.in]", "先离开失乐园。"), ("if score @s %s matches 1.." % O, "你已经在深渊里了。"),
               ("unless score @s rpg_sef matches 7..", "走到第 7 阶「慈悲」，深渊才会打开。"),
               ("if entity @e[type=minecraft:marker,tag=rpg.jqb.center,distance=..64]", "打完眼前这一场再说。")]
    for tag in ("rpg.slb.center", "rpg.mkb.center", "rpg.usb.center", "rpg.lub.center", "rpg.pf.center"):
        blocked.append(("if entity @e[type=minecraft:marker,tag=%s,distance=..64]" % tag, "打完眼前这一场再说。"))
    gate = ["execute %s run return run %s" % (c, msg([txt(m)])) for c, m in blocked]
    body = [txt("深渊在你脚下。", ui.BROADCAST_NAME, True), txt("\n\n那里只有一个人，穿你的盔甲，拿你背包里的每一把武器，会你的技能。\n\n", ui.BROADCAST_BODY),
            txt("只能一个人进去。\n失败不掉东西，不会真的死，两分钟后可以再来。\n它会夺走你手里的武器或身上的盔甲，打完一定归还。\n", ui.BROADCAST_BODY)]
    import json
    dlg = {"type": "minecraft:multi_action", "title": ui.row_value(ui.comp("达阿特 ", SIL, True), ui.comp(ui.fraktur("Daath"), ui.BROADCAST_GLOSS)),
           "body": {"type": "minecraft:plain_message", "width": 320, "contents": ui.row_value(*body)},
           "actions": [{"label": ui.comp("踏入深渊", SIL, True), "action": {"type": "minecraft:run_command", "command": "/trigger rpg_sef_do set 31"}},
                       {"label": ui.comp("还不是时候", ui.BROADCAST_BODY, True), "action": {"type": "minecraft:run_command", "command": "/trigger rpg_sef_do set 20"}}],
           "columns": 2, "can_close_with_escape": True, "pause": False, "after_action": "close"}
    w("ask", ["# 原质页「踏入深渊」（as/at 玩家）"] + gate + ["dialog show @s " + json.dumps(dlg, ensure_ascii=False, separators=(",", ":"))])
    w("go", ["# 确认（as/at 玩家）"] + gate + [
        "execute if score @s rpg_dt_cd matches 1.. run return run function %s/cd_say" % B,
        "scoreboard players set #slot %s 0" % O] +
      ["execute if score #slot %s matches 0 unless score #b%d %s matches 1 run scoreboard players set #slot %s %d" % (O, n, O, O, n) for n in range(1, SLOTS + 1)] + [
        "execute if score #slot %s matches 0 run return run %s" % (O, msg([txt("深渊里已经站满了人，稍后再来。")])),
        "function %s/begin" % B])
    w("cd_say", ["scoreboard players operation #s %s = @s rpg_dt_cd" % O, "scoreboard players set #k %s 20" % O, "scoreboard players operation #s %s /= #k %s" % (O, O),
                 msg([txt("刚从深渊里上来，再等 "), {"score": {"name": "#s", "objective": O}, "color": SIL}, txt(" 秒。")])])
    w("begin", ["# 占一块场地、记下来处、拍快照（as/at 玩家，#slot 场地号）",
                "scoreboard players operation @s %s = #slot %s" % (O, O), "scoreboard players add #sid %s 1" % O, "scoreboard players operation @s rpg_dt_sid = #sid %s" % O,
                "scoreboard players set @s rpg_dt_ph 1", "scoreboard players set @s rpg_dt_pt 0", "scoreboard players set @s rpg_dt_dc 0",
                "scoreboard players add @s rpg_dt_n 0", "scoreboard players set @s rpg_dt_cast 0", "scoreboard players set @s rpg_dt_drk 0",
                "execute store result storage rpg:daath t.id int 1 run scoreboard players get @s rpg_fg_id",
                "execute store result storage rpg:daath t.n int 1 run scoreboard players get @s %s" % O,
                "function %s/begin_m with storage rpg:daath t" % B,
                "function %s/snap/all" % B,
                "effect give @s minecraft:darkness 6 0 true", "effect give @s minecraft:slowness 4 3 true",
                "playsound minecraft:ambient.underwater.enter player @s ~ ~ ~ 1 0.5",
                "playsound minecraft:block.conduit.deactivate player @s ~ ~ ~ 1 0.5"])
    w("begin_m", ["$scoreboard players set #b$(n) %s 1" % O,
                  "$execute store result score #sid$(n) %s run scoreboard players get @s rpg_dt_sid" % O,
                  "$scoreboard players set #em$(n) %s 0" % O,
                  "$data modify storage rpg:daath r.p$(id).dim set from entity @s Dimension",
                  "$execute store result storage rpg:daath r.p$(id).x double 0.01 run data get entity @s Pos[0] 100",
                  "$execute store result storage rpg:daath r.p$(id).y double 0.01 run data get entity @s Pos[1] 100",
                  "$execute store result storage rpg:daath r.p$(id).z double 0.01 run data get entity @s Pos[2] 100",
                  "$execute store result storage rpg:daath r.p$(id).yaw float 0.01 run data get entity @s Rotation[0] 100",
                  "$execute if dimension rpg:daath run data modify storage rpg:daath r.p$(id) set value {dim:\"minecraft:overworld\",x:0.0d,y:120.0d,z:0.0d,yaw:0.0f}",
                  "$data modify storage rpg:daath s$(n) set value {arms:[]}",
                  "function %s/slot/load" % B])
    # 按自己的场地号分发（不用宏拼函数名：校验认不出）
    for nm in ("load", "open", "close", "pull", "loot"):
        w("slot/%s" % nm if nm != "open" else "slot/open_by", ["execute if score @s %s matches %d run return run function %s/slot/%s_%d" % (O, n, B, nm, n) for n in range(1, SLOTS + 1)])
    for n in range(1, SLOTS + 1):
        x = n * GAP
        w("slot/load_%d" % n, ["execute in %s run forceload add %d -32 %d 32" % (DIM, x - 32, x + 32)])
        w("slot/open_%d" % n, ["# 场地 %d 开场（as 玩家）" % n,
                               "execute in %s positioned %d.5 %d 0.5 run function %s/slot/open" % (DIM, x, FLOOR, B),
                               "execute in %s positioned %d.5 %d 0.5 run tp @s ~ ~ ~8 180 0" % (DIM, x, FLOOR)])
        w("slot/close_%d" % n, ["# 收场 %d：清实体、放开区块" % n,
                                "execute in %s positioned %d.5 %d 0.5 run function %s/slot/sweep" % (DIM, x, FLOOR, B),
                                "execute in %s run forceload remove %d -32 %d 32" % (DIM, x - 32, x + 32),
                                "bossbar set rpg:daath_%d players" % n, "bossbar set rpg:daath_%d visible false" % n,
                                "scoreboard players set #b%d %s 0" % (n, O), "data remove storage rpg:daath s%d" % n])
    w("slot/open", ["# positioned 场地中心，as 玩家", "function %s/slot/sweep" % B, "function %s/arena/build" % B, "function %s/arena/props" % B,
                    "scoreboard players operation @e[type=minecraft:marker,tag=rpg.dt.c,distance=..4] %s = @s %s" % (O, O),
                    "scoreboard players operation @e[type=minecraft:marker,tag=rpg.dt.c,distance=..4] rpg_dt_sid = @s rpg_dt_sid"])
    w("slot/sweep", ["execute as @e[%s,distance=..120] run function %s/unit/vanish" % (UNIT, B),
                     "execute as @e[type=minecraft:zombie,tag=rpg.dt.minion,distance=..120] run function %s/unit/vanish" % B,
                     "kill @e[tag=rpg.dt.fx,distance=..120]", "kill @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60]",
                     "kill @e[type=minecraft:marker,tag=rpg.dt.pool,distance=..60]", "kill @e[type=minecraft:interaction,tag=rpg.dt.lamp,distance=..60]",
                     "kill @e[type=minecraft:interaction,tag=rpg.dt.touch,distance=..60]", "kill @e[type=minecraft:item_display,tag=rpg.dt.tree,distance=..60]"])
    w("unit/vanish", ["execute on passengers run kill @s", "tp @s ~ -256 ~", "kill @s"])

    # ------------------------------------------------ 快照：背包里的所有武器
    slots = ["hotbar.%d" % i for i in range(9)] + ["inventory.%d" % i for i in range(27)] + ["weapon.offhand"]
    w("snap/all", ["# 把背包里的武器抄一份（as/at 玩家）", "summon minecraft:item_display ~ ~ ~ {Tags:[\"rpg.dt.tmp\"]}"] +
      ["execute if items entity @s %s #rpg:daath/weapon run function %s/snap/one {s:\"%s\"}" % (s, B, s) for s in slots] + [
          "kill @e[type=minecraft:item_display,tag=rpg.dt.tmp,distance=..4]"])
    tmp = "@e[type=minecraft:item_display,tag=rpg.dt.tmp,distance=..4,limit=1]"
    cls = ["scoreboard players set #c %s 1" % O]
    C = "execute if items entity %s contents " % tmp
    for pred, c in (("#minecraft:axes", 2), ("minecraft:mace", 3), ("#minecraft:spears", 4), ("minecraft:trident", 4), ("#minecraft:hoes", 7),
                    ("minecraft:bow", 8), ("minecraft:crossbow", 9),
                    ("*[minecraft:custom_data~{forge_tag:1b}]", 3), ("*[minecraft:custom_data~{michael_spine_tag:1b}]", 5),
                    ("*[minecraft:custom_data~{grave_bane_tag:1b}]", 5), ("*[minecraft:custom_data~{michael_rib_tag:1b}]", 6)):
        cls.append("%s%s run scoreboard players set #c %s %d" % (C, pred, O, c))
    w("snap/one", ["$item replace entity %s contents from entity @s $(s)" % tmp] + cls + [
        "data modify storage rpg:daath t.e set value {c:1}", "execute store result storage rpg:daath t.e.c int 1 run scoreboard players get #c %s" % O,
        "data modify storage rpg:daath t.e.item set from entity %s item" % tmp,
        "function %s/snap/push with storage rpg:daath t" % B])
    w("snap/push", ["$execute store result score #len %s run data get storage rpg:daath s$(n).arms" % O,
                    "execute if score #len %s matches 18.. run return 0" % O,
                    "$data modify storage rpg:daath s$(n).arms append from storage rpg:daath t.e"])

    # ------------------------------------------------ 每刻：挑战者
    w("tick", ["# 每刻入口（add_daath.py）",
               "execute as @a[scores={rpg_dt_cd=1..}] run scoreboard players remove @s rpg_dt_cd 1",
               "execute as @a[scores={%s=1..}] at @s run function %s/pl/tick" % (O, B),
               "execute in %s if entity @a[distance=0..] run function %s/dim" % (DIM, B)])
    w("dim", ["# 维度里有人才跑（in rpg:daath）",
              "execute as @e[type=minecraft:marker,tag=rpg.dt.c] at @s run function %s/arena/tick" % B,
              "execute as @e[%s,distance=0..] at @s rotated ~ 0 run function %s/unit/tick" % (UNIT, B),
              "execute as @e[tag=rpg.dt.fx,distance=0..] at @s run function %s/fx/tick" % B,
              "execute as @e[type=minecraft:item_display,tag=rpg.dt.shot,distance=0..] at @s run function %s/shot/tick" % B,
              "execute as @e[type=minecraft:zombie,tag=rpg.dt.minion,distance=0..] at @s run function %s/minion/tick" % B,
              "execute as @e[type=minecraft:item_display,tag=rpg.dt.pp,distance=0..] at @s unless entity @e[type=minecraft:zombie,tag=rpg.dt.minion,distance=..12] run kill @s"])
    w("pl/tick", ["# 挑战者每刻（as/at 玩家）",
                  "execute store result storage rpg:daath t.n int 1 run scoreboard players get @s %s" % O,
                  "function %s/pl/check with storage rpg:daath t" % B,
                  "execute unless score @s %s matches 1.. run return 0" % O,
                  "execute if score @s rpg_dt_dc matches 1.. run return run function %s/pl/died" % B,
                  "scoreboard players add @s rpg_dt_pt 1",
                  "execute if score @s rpg_dt_ph matches 1 run return run function %s/pl/sink" % B,
                  "execute if score @s rpg_dt_ph matches 2 run return run function %s/pl/arrive" % B,
                  "execute if score @s rpg_dt_ph matches 3 run return run function %s/pl/bound" % B,
                  "execute if score @s rpg_dt_ph matches 4 run return run function %s/pl/rise" % B,
                  "execute if score @s rpg_dt_ph matches 5 run return run function %s/pl/lost" % B])
    w("pl/check", ["# 场次对不上（掉线太久、服务器清过）：送回去", "$execute if score #b$(n) %s matches 1 if score #sid$(n) %s = @s rpg_dt_sid run return 0" % (O, O),
                   "function %s/pl/out" % B])
    w("pl/sink", ["particle %s ~ ~0.1 ~ 0.8 0.05 0.8 0 12" % DUST_D, "particle minecraft:squid_ink ~ ~0.2 ~ 0.5 0.1 0.5 0.02 4",
                  "execute if score @s rpg_dt_pt matches 20 run effect give @s minecraft:blindness 4 0 true",
                  "execute if score @s rpg_dt_pt matches 30 run playsound minecraft:ambient.underwater.loop.additions.rare player @s ~ ~ ~ 1 0.6",
                  "execute if score @s rpg_dt_pt matches 50.. run function %s/pl/down" % B])
    w("pl/down", ["scoreboard players set @s rpg_dt_ph 2", "scoreboard players set @s rpg_dt_pt 0",
                  "execute store result storage rpg:daath t.n int 1 run scoreboard players get @s %s" % O,
                  "function %s/pl/down_m with storage rpg:daath t" % B,
                  "tag @s add rpg.dt.in", "effect give @s minecraft:slow_falling 3 0 true",
                  "title @s times 10 50 20", "title @s subtitle " + ui.row(ui.comp("דעת", ui.BROADCAST_GLOSS)),
                  "title @s title " + ui.row(ui.comp("Daath", SIL, True)),
                  "playsound minecraft:block.end_portal.spawn player @s ~ ~ ~ 0.5 0.5"])
    w("pl/down_m", ["function %s/slot/open_by" % B])
    w("pl/arrive", ["effect clear @s minecraft:blindness",
                    "execute if score @s rpg_dt_pt matches 40 run function %s/unit/summon" % B,
                    "execute if score @s rpg_dt_pt matches 110.. run scoreboard players set @s rpg_dt_ph 3"])
    w("pl/bound", ["# 场地没有墙：走出去就从对面走回来",
                   "execute unless entity @e[type=minecraft:marker,tag=rpg.dt.c,distance=..120] run return run function %s/pl/strayed" % B,
                   "execute if entity @e[type=minecraft:marker,tag=rpg.dt.c,distance=..23.6] run return 0",
                   "execute at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..120,limit=1,sort=nearest] facing entity @s feet rotated ~ 0 positioned ^ ^ ^-22 run tp @s ~ ~0.1 ~",
                   "execute at @s run particle %s ~ ~0.3 ~ 0.6 0.2 0.6 0 16" % DUST, "execute at @s run playsound minecraft:block.glass.hit player @s ~ ~ ~ 0.6 0.6",
                   "execute unless entity @s[tag=rpg.dt.walk] as @e[%s,distance=..80,limit=1,sort=nearest] at @s run function %s/say_walk" % (UNIT, B),
                   "tag @s add rpg.dt.walk"])
    w("say_walk", ["tag @p[tag=rpg.dt.in] add rpg.dt.me"] + line("S02") + ["tag @a remove rpg.dt.me"])
    w("pl/strayed", ["# 被传送走了：拉回来", "execute store result storage rpg:daath t.n int 1 run scoreboard players get @s %s" % O,
                     "function %s/pl/pull_m with storage rpg:daath t" % B])
    w("pl/pull_m", ["function %s/slot/pull" % B])
    for n in range(1, SLOTS + 1):
        w("slot/pull_%d" % n, ["execute in %s run tp @s %d.5 %d 8.5 180 0" % (DIM, n * GAP, FLOOR)])
    w("pl/rise", ["# 赢了：上浮", "execute if score @s rpg_dt_pt matches 1 run effect give @s minecraft:levitation 4 1 true",
                  "particle minecraft:end_rod ~ ~0.6 ~ 0.6 0.8 0.6 0.02 4",
                  "execute if score @s rpg_dt_pt matches 50 run effect give @s minecraft:blindness 2 0 true",
                  "execute if score @s rpg_dt_pt matches 70.. run function %s/pl/won" % B])
    w("pl/won", ["scoreboard players add @s rpg_dt_win 1", "function %s/pl/out" % B,
                 "execute unless score @s rpg_daath matches 1 run function rpg:sephira/daath/pass",
                 "function %s/reward" % B])
    w("pl/lost", ["# 判负：它按住你的额头",
                  "execute if score @s rpg_dt_pt matches 1 run effect give @s minecraft:blindness 4 0 true",
                  "execute if score @s rpg_dt_pt matches 1 run effect give @s minecraft:resistance 6 4 true",
                  "execute if score @s rpg_dt_pt matches 1 run effect give @s minecraft:slowness 4 6 true",
                  "execute if score @s rpg_dt_pt matches 50.. run function %s/pl/lost_go" % B])
    tips = ["眼睛里显示的是它记住了什么。别总用同一招。", "打亮灯柱，它走进光里才会显形。", "地上先亮的线、圈、影子，都是它要打的地方。",
            "夺走的东西：灯下打中它四下，或者让它眩晕，就能拿回来。", "「同一把剑」亮到最亮的那一瞬间出手。"]
    w("pl/lost_go", ["scoreboard players add @s rpg_dt_n 1", "function %s/pl/out" % B, "scoreboard players set @s rpg_dt_cd 2400",
                     "effect give @s minecraft:regeneration 8 3 true",
                     msg([txt("你被送了回来。两分钟后可以再来。")])] +
      ["execute if score @s rpg_dt_n matches %d run %s" % (i + 1, msg([txt("提示：" + t, SIL)])) for i, t in enumerate(tips)] +
      ["execute if score @s rpg_dt_n matches %d.. run %s" % (len(tips) + 1, msg([txt("提示：打法越单一，它越强。", SIL)]))])
    w("pl/died", ["# 其他原因死了：等复活（躺着的时候给东西会丢），再把掉在场地里的东西送到脚下，判负",
                  "execute store result score #h %s run data get entity @s Health 10" % O,
                  "execute if score #h %s matches ..0 run return run function %s/pl/keep" % (O, B), "scoreboard players set @s rpg_dt_dc 0", "tag @s remove rpg.dt.kept",
                  "execute store result storage rpg:daath t.n int 1 run scoreboard players get @s %s" % O,
                  "function %s/pl/loot_m with storage rpg:daath t" % B,
                  "scoreboard players add @s rpg_dt_n 1", "tag @s add rpg.dt.dead", "function %s/pl/out" % B, "scoreboard players set @s rpg_dt_cd 2400"])
    w("pl/keep", ["# 还没复活：掉落物不许消失", "execute if entity @s[tag=rpg.dt.kept] run return 0", "tag @s add rpg.dt.kept",
                  "execute in %s as @e[type=minecraft:item,distance=0..] run data merge entity @s {Age:-32768s}" % DIM])
    w("pl/loot_m", ["tag @s add rpg.dt.mine", "function %s/slot/loot" % B, "tag @s remove rpg.dt.mine"])
    for n in range(1, SLOTS + 1):
        w("slot/loot_%d" % n, ["execute in %s positioned %d.5 %d 0.5 run tp @e[type=minecraft:item,distance=..90] @a[tag=rpg.dt.mine,limit=1]" % (DIM, n * GAP, FLOOR),
                               "execute in %s positioned %d.5 %d 0.5 run tp @e[type=minecraft:experience_orb,distance=..90] @a[tag=rpg.dt.mine,limit=1]" % (DIM, n * GAP, FLOOR)])
    w("pl/out", ["# 离开深渊（任何原因）：先还东西，再送回来处，收场（as 玩家）",
                 "function %s/steal/give_all" % B,
                 "execute store result storage rpg:daath t.id int 1 run scoreboard players get @s rpg_fg_id",
                 "execute store result storage rpg:daath t.n int 1 run scoreboard players get @s %s" % O,
                 "execute unless entity @s[tag=rpg.dt.dead] run function %s/pl/back_m with storage rpg:daath t" % B,
                 "function %s/pl/close_m with storage rpg:daath t" % B,
                 "tag @s remove rpg.dt.in", "tag @s remove rpg.dt.me", "tag @s remove rpg.dt.walk", "tag @s remove rpg.dt.dead",
                 "scoreboard players set @s %s 0" % O, "scoreboard players set @s rpg_dt_ph 0",
                 "effect clear @s minecraft:levitation", "effect clear @s minecraft:blindness", "effect clear @s minecraft:darkness",
                 "effect give @s minecraft:slow_falling 3 0 true", "stopsound @s record",
                 "playsound minecraft:ambient.underwater.exit player @s ~ ~ ~ 1 0.7"])
    w("pl/back_m", ["$execute unless data storage rpg:daath r.p$(id) in minecraft:overworld run return run tp @s 0 120 0",
                    "$function %s/pl/back_at with storage rpg:daath r.p$(id)" % B, "$data remove storage rpg:daath r.p$(id)"])
    w("pl/back_at", ["$execute in $(dim) run tp @s $(x) $(y) $(z) $(yaw) 0"])
    w("pl/close_m", ["$execute unless score #sid$(n) %s = @s rpg_dt_sid run return 0" % O, "function %s/slot/close" % B])

    # ------------------------------------------------ 场地每刻
    w("arena/tick", ["# 场地每刻（as/at 中心标记）",
                     "execute if entity @a[tag=rpg.dt.in,distance=..90] run scoreboard players set @s rpg_dt_e 0",
                     "execute unless entity @a[tag=rpg.dt.in,distance=..90] run scoreboard players add @s rpg_dt_e 1",
                     "execute if score @s rpg_dt_e matches 1200.. run return run function %s/arena/timeout" % B,
                     "# 保险：打着打着影子没了（被指令杀掉之类），还东西、送回去",
                     "execute if entity @a[tag=rpg.dt.in,distance=..90,scores={rpg_dt_ph=3}] unless entity @e[%s,distance=..120] run return run function %s/arena/gone" % (UNIT, B),
                     "execute as @e[type=minecraft:item_display,tag=rpg.dt.trs,distance=..40] at @s run rotate @s ~0.6 0", "execute as @e[type=minecraft:item_display,tag=rpg.dt.trr,distance=..40] at @s run rotate @s ~-1 0",
                     "execute as @e[type=minecraft:interaction,tag=rpg.dt.lamp,distance=..30] at @s run function %s/lamp/tick" % B,
                     "execute as @e[type=minecraft:marker,tag=rpg.dt.pool,distance=..30] at @s run function %s/lamp/pool" % B])
    w("arena/gone", ["execute as @a[tag=rpg.dt.in,distance=..90,scores={rpg_dt_ph=3}] run function %s/arena/gone_pl" % B])
    w("arena/gone_pl", [msg([txt("影子消失了，这一场不算。")]), "function %s/pl/out" % B])
    w("arena/timeout", ["# 挑战者离开太久", "execute store result storage rpg:daath t.n int 1 run scoreboard players get @s %s" % O, "function %s/arena/timeout_m with storage rpg:daath t" % B])
    w("arena/timeout_m", ["function %s/slot/close" % B])

    # ------------------------------------------------ 灯
    on = []
    for i, k in enumerate(LAMPS):
        x, z = lamp_xy(i)
        X, Z = int(round(x)), int(round(z))
        px, pz = lamp_xy(i, POOL_R)
        # 从灯到光圈圆心的偏移
        on.append("execute if entity @s[tag=rpg.dt.l%d] positioned ~%.2f ~ ~%.2f run function %s/lamp/lit_at" % (i, px - X, pz - Z, B))
    w("lamp/tick", ["# 每盏灯（as/at 灯）：rpg_dt_lt 亮着的剩余刻，rpg_dt_pcd 冷却",
                    "execute if score @s rpg_dt_lt matches 1.. run function %s/lamp/burn" % B,
                    "execute if score @s rpg_dt_pcd matches 1.. run scoreboard players remove @s rpg_dt_pcd 1",
                    "scoreboard players set #hit %s 0" % O,
                    "execute if data entity @s attack run scoreboard players set #hit %s 1" % O,
                    "execute if data entity @s interaction run scoreboard players set #hit %s 1" % O,
                    "execute if score #hit %s matches 0 run return 0" % O,
                    "data remove entity @s attack", "data remove entity @s interaction",
                    "execute if score @s rpg_dt_lt matches 1.. run return 0",
                    "execute if score @s rpg_dt_pcd matches 1.. run return run playsound minecraft:block.candle.fall block @a[distance=..16] ~ ~2 ~ 1 0.6",
                    "execute store result score #on %s if entity @e[type=minecraft:marker,tag=rpg.dt.pool,distance=..60]" % O,
                    "execute if score #on %s matches 2.. run return run playsound minecraft:block.candle.fall block @a[distance=..16] ~ ~2 ~ 1 0.6" % O,
                    "function %s/lamp/lit" % B])
    w("lamp/lit", ["scoreboard players set @s rpg_dt_lt 160", "scoreboard players set @s rpg_dt_pcd 560",
                   "playsound minecraft:block.beacon.activate block @a[distance=..40] ~ ~3 ~ 0.8 1.6", "playsound minecraft:item.firecharge.use block @a[distance=..40] ~ ~3 ~ 0.6 1.4",
                   "particle minecraft:end_rod ~ ~3.6 ~ 0.3 0.4 0.3 0.05 20", "setblock ~ ~5 ~ minecraft:light[level=15]"] + on)
    w("lamp/lit_at", ["# positioned 光圈圆心", "summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.dt.pool\"]}",
                      "scoreboard players set @e[type=minecraft:marker,tag=rpg.dt.pool,distance=..0.5] rpg_dt_lt 160",
                      "setblock ~ ~3 ~ minecraft:light[level=15]"] +
      fx.decal("glow", LIGHT_R * 2.2, LIGHTC, pos="~ ~0.04 ~", life=160, tags=("rpg.dt.poolfx",)) +
      fx.decal("ring", LIGHT_R * 2, WHITE, pos="~ ~0.07 ~", life=160, tags=("rpg.dt.poolfx",)) + light_pillar(LIGHTC))
    w("lamp/burn", ["scoreboard players remove @s rpg_dt_lt 1",
                    "execute if score @s rpg_dt_lt matches 0 run function %s/lamp/out" % B])
    w("lamp/out", ["# 灯灭（as/at 灯）", "scoreboard players set @s rpg_dt_lt 0", "setblock ~ ~5 ~ minecraft:air",
                   "playsound minecraft:block.candle.extinguish block @a[distance=..40] ~ ~3 ~ 1 0.6", "particle minecraft:smoke ~ ~3.8 ~ 0.2 0.3 0.2 0.02 12"])
    w("lamp/pool", ["# 光圈（as/at 圆心）", "scoreboard players remove @s rpg_dt_lt 1",
                    "execute if score @s rpg_dt_lt matches ..0 run return run function %s/lamp/pool_out" % B,
                    "particle minecraft:end_rod ~ ~1.4 ~ 2 1 2 0.005 1"])
    w("lamp/pool_out", ["setblock ~ ~3 ~ minecraft:air", "kill @e[tag=rpg.dt.poolfx,distance=..1]", "kill @s"])
    w("lamp/all_out", ["# 全灭（at 场地中心附近）",
                       "execute as @e[type=minecraft:interaction,tag=rpg.dt.lamp,distance=..60,scores={rpg_dt_lt=1..}] at @s run function %s/lamp/out" % B,
                       "execute as @e[type=minecraft:marker,tag=rpg.dt.pool,distance=..60] at @s run function %s/lamp/pool_out" % B])

    # ------------------------------------------------ 夺走的东西：存在存储 st.p<玩家号>.{w,a}
    w("steal/give_all", ["# 全部归还（as 玩家）", "execute store result storage rpg:daath t.id int 1 run scoreboard players get @s rpg_fg_id",
                         "function %s/steal/give_w with storage rpg:daath t" % B, "function %s/steal/give_a with storage rpg:daath t" % B, "function %s/steal/done with storage rpg:daath t" % B])
    w("steal/done", ["$execute if data storage rpg:daath st.p$(id).w run return 0", "$execute if data storage rpg:daath st.p$(id).a run return 0", "scoreboard players set @s rpg_dt_got 0"])
    for k in ("w", "a"):
        w("steal/give_%s" % k, ["$execute unless data storage rpg:daath st.p$(id).%s run return 0" % k,
                                "execute at @s run summon minecraft:item_display ~ ~ ~ {Tags:[\"rpg.dt.ret\"]}",
                                "# 区块还没载入（刚复活、刚换维度）就放不下展示实体：先留在存储里，每秒再试", "execute unless entity @e[type=minecraft:item_display,tag=rpg.dt.ret,limit=1] run return 0",
                                "$data modify entity @e[type=minecraft:item_display,tag=rpg.dt.ret,limit=1] item set from storage rpg:daath st.p$(id).%s.item" % k,
                                "$data modify storage rpg:daath t.slot set from storage rpg:daath st.p$(id).%s.slot" % k,
                                "$data remove storage rpg:daath st.p$(id).%s" % k,
                                "function %s/steal/put with storage rpg:daath t" % B,
                                "kill @e[type=minecraft:item_display,tag=rpg.dt.ret]"])
    w("steal/put", ["# 原来的格子空着就放回去，否则掉在脚下（不会被别人捡走）",
                    "$execute unless items entity @s $(slot) * run return run item replace entity @s $(slot) from entity @e[type=minecraft:item_display,tag=rpg.dt.ret,limit=1] contents",
                    "execute at @s run summon minecraft:item ~ ~0.3 ~ {Tags:[\"rpg.dt.drop\"],PickupDelay:0s,Item:{id:\"minecraft:paper\",count:1}}",
                    "execute at @s run data modify entity @e[type=minecraft:item,tag=rpg.dt.drop,limit=1,sort=nearest] Item set from entity @e[type=minecraft:item_display,tag=rpg.dt.ret,limit=1] item",
                    "execute at @s run data modify entity @e[type=minecraft:item,tag=rpg.dt.drop,limit=1,sort=nearest] Owner set from entity @s UUID",
                    "tag @e[type=minecraft:item,tag=rpg.dt.drop] remove rpg.dt.drop"])
    w("sec", ["# 每秒：不在试炼里却还有东西没还的人（服务器重启、异常）",
              "schedule function %s/sec 20t" % B,
              "execute as @a unless score @s %s matches 1.. if score @s rpg_dt_got matches 1.. run function %s/steal/late" % (O, B),
              "# 场次早没了人还留在深渊里：送回主世界", "execute in %s as @a[distance=0..] unless score @s %s matches 1.. run function %s/pl/stray_home" % (DIM, O, B)])
    w("pl/stray_home", ["effect give @s minecraft:slow_falling 12 0 true", "execute in minecraft:overworld run tp @s 0 120 0"])
    w("steal/late", ["function %s/steal/give_all" % B])
    w("reward", ["# 奖励（as 玩家，已回到原处）",
                 "execute unless score @s rpg_dt_win matches 2.. run loot give @s loot rpg:daath/shard",
                 "execute if score @s rpg_dt_win matches 2.. unless score @s rpg_dt_rd = #day rpg_sef run loot give @s loot rpg:forge/item/soul",
                 "execute if score @s rpg_dt_win matches 2.. unless score @s rpg_dt_rd = #day rpg_sef run loot give @s loot rpg:forge/item/soul",
                 "scoreboard players operation @s rpg_dt_rd = #day rpg_sef"])
    w("clear", ["# 管理员：清掉自己这一场并回到原处（as 玩家）", "execute if score @s %s matches 1.. run function %s/pl/out" % (O, B)])
    w("summon", ["# 管理员：立刻进场（as/at 玩家），不看阶位与冷却",
                 "execute if score @s %s matches 1.. run return run function %s/clear" % (O, B), "scoreboard players set #slot %s 0" % O] +
      ["execute if score #slot %s matches 0 unless score #b%d %s matches 1 run scoreboard players set #slot %s %d" % (O, n, O, O, n) for n in range(1, SLOTS + 1)] +
      ["execute if score #slot %s matches 1.. run function %s/begin" % (O, B)])
