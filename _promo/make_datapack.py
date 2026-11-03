# -*- coding: utf-8 -*-
"""生成宣传片拍摄用的小数据包 _promo/datapack/（命名空间 promo）。

只布景、不改玩法：召唤与技能一律调用 rpg/ 里现成的函数，
武器清单从 _tools/rpg_catalogue.py 读，不另抄一份物品组件。

    python _promo/make_datapack.py

运镜交给 ReplayMod 在回放里做，所以这里没有逐 tick 的镜头路径。
"""
import json
import re
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_tools"))
from rpg_catalogue import catalogue  # noqa: E402

OUT = os.path.join(ROOT, "_promo", "datapack")
FN = os.path.join(OUT, "data", "promo", "function")

WEAPON_SUFFIX = ("sword", "axe", "bow", "crossbow", "mace", "spear", "trident", "fishing_rod")
# 名字前缀里有几件写的是中文品质
# LTD（限定款）在 README 的五档里算传说，陈列也归进传说
TIER_ALIAS = {"传说": "legend", "史诗": "epic", "勇者": "brave", "恶魔": "DEVIL", "神圣": "HOLY",
              "LTD": "legend", "限定": "legend"}
# 五档品质的陈列顺序；glow 是陈列时的描边色
TIERS = [
    ("brave", "勇者", 0xBFC7D5),
    ("epic", "史诗", 0xB26BFF),
    ("legend", "传说", 0xF2B33D),
    ("DEVIL", "恶魔", 0x7A8F22),
    ("HOLY", "神圣", 0xFFF2B0),
]


def weapons():
    items = catalogue(os.path.join(ROOT, "rpg"))
    out = []
    for recs in items.values():
        r = recs[0]
        ident = r["id"].split(":")[-1]
        if ident.endswith(WEAPON_SUFFIX) and not ident.endswith("pickaxe"):
            m = re.search(r"\[(\w+)\]", r["full_name"])
            if not m:
                continue
            tier = TIER_ALIAS.get(m.group(1), m.group(1))
            if tier not in [t[0] for t in TIERS]:   # [锻造] 之类的类目前缀，不是档次
                continue
            out.append((tier, r["name"], r["item"]))
    order = [t[0] for t in TIERS]
    out.sort(key=lambda w: order.index(w[0]))
    return out


def write(rel, text):
    path = os.path.join(FN, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text.strip() + "\n")


def tellraw(text, color="#D9C9A3"):
    return "tellraw @s " + json.dumps({"text": text, "color": color}, ensure_ascii=False)


def armory(ws):
    """两排陈列，沿 +Z 铺开成一条长廊；品质越往里越高。"""
    lines = [
        "# 武器长廊：31 件武器两排相对，玩家站在廊口（执行位置）朝 +Z 看。",
        "function promo:armory/clear",
    ]
    for i, (tier, name, item) in enumerate(ws):
        side = -1 if i % 2 == 0 else 1
        z = 3 + (i // 2) * 1.6
        x = side * 2.2
        yaw = -90 if side < 0 else 90   # 面朝长廊中线
        glow = dict((t[0], t[2]) for t in TIERS)[tier]
        lines.append(
            "summon minecraft:item_display ~%.1f ~1.6 ~%.1f {Tags:[\"promo.disp\",\"promo.new\"],"
            "Rotation:[%df,0f],item_display:\"fixed\",Glowing:1b,glow_color_override:%d,"
            "brightness:{sky:15,block:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],"
            "scale:[1.3f,1.3f,1.3f],right_rotation:[0f,0f,0f,1f]}}" % (x, z, yaw, glow))
        lines.append("item replace entity @e[type=minecraft:item_display,tag=promo.new,limit=1] contents with %s" % item)
        lines.append("tag @e[tag=promo.new] remove promo.new")
    # 每档开头放一块品质牌
    seen = {}
    for i, (tier, _n, _it) in enumerate(ws):
        seen.setdefault(tier, i)
    for tier, label, color in TIERS:
        if tier not in seen:
            continue
        z = 3 + (seen[tier] // 2) * 1.6
        lines.append(
            "summon minecraft:text_display ~ ~2.9 ~%.1f {Tags:[\"promo.disp\"],billboard:\"center\","
            "background:0,shadow:1b,text:%s,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],"
            "scale:[1.6f,1.6f,1.6f],right_rotation:[0f,0f,0f,1f]}}"
            % (z, json.dumps({"text": label, "color": "#%06X" % color, "bold": True}, ensure_ascii=False)))
    lines.append(tellraw("[宣传片] 武器长廊已摆好：%d 件，沿 +Z 由勇者到神圣。" % len(ws)))
    write("armory/spawn.mcfunction", "\n".join(lines))
    write("armory/clear.mcfunction", "kill @e[tag=promo.disp]")


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(FN)
    with open(os.path.join(OUT, "pack.mcmeta"), "w", encoding="utf-8") as f:
        json.dump({"pack": {"description": "破碎大陆宣传片拍摄布景（promo）",
                            "min_format": [94, 1], "max_format": 94,
                            "pack_format": 94}}, f, ensure_ascii=False, indent=2)

    ws = weapons()
    assert len(ws) == 31, "武器数量变了：%d" % len(ws)
    armory(ws)

    write("setup.mcfunction", """
# 拍摄环境：黄昏定格、晴天、不刷怪；玩家生存模式 + 无敌，这样别西卜的招式会对准你。
gamerule advance_time false
gamerule advance_weather false
gamerule spawn_mobs false
gamerule spawn_phantoms false
gamerule show_death_messages false
time set 12600
weather clear
gamemode survival @s
function promo:god
""" + tellraw("[宣传片] 拍摄环境就绪：黄昏、晴天、不刷怪。"))

    write("god.mcfunction", """
# 录制期间不死不饿，粒子全隐藏，免得挡镜头。
effect give @s minecraft:resistance infinite 4 true
effect give @s minecraft:regeneration infinite 2 true
effect give @s minecraft:saturation infinite 0 true
effect give @s minecraft:fire_resistance infinite 0 true
""")

    write("time/dusk.mcfunction", "time set 12600")
    write("time/night.mcfunction", "time set 18000")
    write("time/noon.mcfunction", "time set 6000")

    # 别西卜：完整入口 = 拨 #boss + lord4（召唤 + 记名 + 给寿命），见 rpg:command/summon_devil。
    # 按 rpg_dm_lord=4 找他而不是按模型标签 —— 模型标签随建模调整会变，记名分数不变。
    bz = "@e[type=minecraft:vindicator,scores={rpg_dm_lord=4},limit=1,sort=nearest]"
    write("bz/summon.mcfunction", """
# 在你视线前方 10 格召唤别西卜。
scoreboard players set #boss rpg_fall 1
execute positioned ^ ^ ^10 run function rpg:taint/lord4
""" + tellraw("[宣传片] 别西卜已降临。用 promo:bz/cast1..5、promo:bz/ult 点名放招。", "#7A8F22"))
    for n in range(1, 6):
        write("bz/cast%d.mcfunction" % n,
              "execute as %s at @s run function rpg:taint/sk4_%d" % (bz, n))
    write("bz/ult.mcfunction", """
# 万蝇饕宴：先预警再爆发，和实战节奏一致。
execute as %s at @s run function rpg:taint/ult4_warn
schedule function promo:bz/ult_fire 40t
""" % bz)
    write("bz/ult_fire.mcfunction",
          "execute as %s at @s run function rpg:taint/ult4" % bz)

    write("guards.mcfunction", """
# 圣卫方阵：视线前方 8 格，三人一排。
execute positioned ^-2.5 ^ ^8 run function rpg:tower_guard/summon
execute positioned ^ ^ ^9 run function rpg:tower_guard/summon
execute positioned ^2.5 ^ ^8 run function rpg:tower_guard/summon
""" + tellraw("[宣传片] 圣卫方阵已列队。", "#E3B04B"))

    write("tree.mcfunction", """
# 生命之树粒子阵，沿你的朝向平铺在脚下。
function rpg:ritual/life_tree/place
""")

    write("clear.mcfunction", """
# 收场：撤掉陈列、领主、圣卫和生命之树，不碰别的实体。
function promo:armory/clear
execute as @e[type=minecraft:vindicator,scores={rpg_dm_lord=4}] on passengers run kill @s
kill @e[type=minecraft:vindicator,scores={rpg_dm_lord=4}]
execute as @e[type=minecraft:vindicator,tag=rpg.tg] on passengers run kill @s
kill @e[type=minecraft:vindicator,tag=rpg.tg]
function rpg:ritual/life_tree/clear_all
""" + tellraw("[宣传片] 场地已清空。"))

    write("help.mcfunction", "\n".join(tellraw(t) for t in [
        "[宣传片] 拍摄函数：",
        " promo:setup  环境就绪   promo:clear  清场",
        " promo:armory/spawn  武器长廊（朝 +Z）",
        " promo:guards  圣卫方阵   promo:bz/summon  别西卜",
        " promo:bz/cast1..5  别西卜五式   promo:bz/ult  万蝇饕宴",
        " promo:tree  生命之树   promo:time/dusk|night|noon",
    ]))
    os.makedirs(os.path.join(OUT, "data", "minecraft", "tags", "function"), exist_ok=True)
    with open(os.path.join(OUT, "data", "minecraft", "tags", "function", "load.json"), "w", encoding="utf-8") as f:
        json.dump({"values": ["promo:help"]}, f)
    print("wrote", OUT, "with", len(ws), "weapons")


if __name__ == "__main__":
    main()
