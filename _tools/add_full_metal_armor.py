# -*- coding: utf-8 -*-
"""都灵裹尸布与圣荆棘冠换成 Minecraft Dungeons 全金属盔甲（Full Metal Armor）的 3D 模型。

两件神圣护甲本是皮革底材（`leather_chestplate` / `leather_helmet`），带染色和
盔甲纹饰，物品来自原包的发放命令（command/give/weapon、box）。这里只改这两件
的外观，不碰全包的纹饰体系。

模型在 `full_metal_armor_ref/full_metal_armor.bbmodel`（Blockbench，用原作贴图；
原贴图本身就是方块网格：头盔 10x8x8 在 0,0，胸甲 10x13x6 在 0,20，黑色内衬
10x11x6 在 0,41，护肩 6x7x8 在 36,0，护肩翻转 180 度让金边朝下、空心的口朝上）。

* 圣荆棘冠：物品模型就是头盔。物品带 `equippable`（槽位 head）但不指定
  `asset_id`，原版就不画盔甲层，而是把物品模型戴在头上（同南瓜、头颅），
  头盔随头转动、低头抬头。
* 都灵裹尸布：胸甲槽不会画物品模型，所以穿戴外观是一个展示实体：每个穿着它
  的玩家一个，每刻传送到玩家脚下、朝向玩家（偏航）。潜行时下沉一点；隐身、
  游泳、鞘翅滑翔时不显示。它不跟手臂摆动。物品本身同样带不含 `asset_id` 的
  `equippable`，不画皮革层。
* 两件的物品栏图标就是各自的 3D 模型。
* 去掉 `trim` 与 `dyed_color`（没有逻辑读它们）；属性、附魔、custom_data 不动。
  穿戴音换成原作的板甲声（内联声音，服务端不认识材质包里的声音 id）。

素材见 full_metal_armor_ref/SOURCES.md。
"""

import io
import json
import os
import re
import shutil
import sys

import display_mob as dm

RP = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
DP = sys.argv[2] if len(sys.argv) > 2 else "../rpg"

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "full_metal_armor_ref")
NS = "rpg"
KEY = "full_metal"

ITEMS = {
    # 物品名 -> (底材, 槽位, 物品模型, 穿戴音)
    "圣荆棘冠": ("leather_helmet", "head", "full_metal_helmet", "equip_light"),
    "都灵裹尸布": ("leather_chestplate", "chest", "full_metal_chestplate", "equip_heavy"),
}
CHEST_BONES = ["tunic", "breastplate", "right_pauldron", "left_pauldron"]
SOUNDS = {
    "equip_light": ("全金属盔甲：戴上", "Full metal armor equipped",
                    ["Sfx_item_plateArmorDropLight-%03d_soundWave.ogg" % i for i in range(1, 7)]),
    "equip_heavy": ("全金属盔甲：穿上", "Full metal armor equipped",
                    ["Sfx_item_plateArmorDropHeavy-%03d_soundWave.ogg" % i for i in range(1, 8)]),
}
HELMET_SCALE = 1.84     # 1.6 undoes the head layer's 0.625; x1.15 clears the hat layer
SNEAK_DROP = 0.2        # blocks


class Rig:
    """What display_mob needs to read the .bbmodel and place a model."""
    key = KEY
    bbmodel = os.path.join(REF, "full_metal_armor.bbmodel")
    glow = set()
    seat = 0.0
    model_scale = 1.0
    tex = "%s:item/%s/atlas" % (NS, KEY)


def wj(path, doc):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def wf(path, lines):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")


# ---------------------------------------------------------------------------
# 模型
# ---------------------------------------------------------------------------

# a half turn about one axis: the two other axes flip, and so do the faces
# on them; every face's texture turns 180 in its plane
HALF_TURN = {
    "x": ((1, 2), {"up": "down", "down": "up", "north": "south", "south": "north"}),
    "y": ((0, 2), {"east": "west", "west": "east", "north": "south", "south": "north"}),
    "z": ((0, 1), {"east": "west", "west": "east", "up": "down", "down": "up"}),
}


def half_turn(c, axis, pivot):
    """Bake a 180-degree bone rotation into cube c (Java elements only rotate
    by up to 45 degrees)."""
    flip, faces = HALF_TURN[axis]
    f, t = list(c["from"]), list(c["to"])
    for i in flip:
        f[i], t[i] = 2 * pivot[i] - c["to"][i], 2 * pivot[i] - c["from"][i]
    new = {}
    for face, data in c["faces"].items():
        d = dict(data)
        d["rotation"] = (data.get("rotation", 0) + 180) % 360
        new[faces.get(face, face)] = d
    return dict(c, **{"from": f, "to": t, "faces": new})


def cubes_of(bones, name):
    """(cube, remaining one-axis rotation or None) for bone `name`."""
    b = bones[name]
    rot = [(a, v) for a, v in zip("xyz", b["rotation"]) if v]
    if rot and abs(rot[0][1]) == 180:
        return [half_turn(c, rot[0][0], b["pivot"]) for c in b["cubes"]], None
    return b["cubes"], (rot[0] if rot else None)


def elements(bones, names, K, res):
    """Java model elements for the cubes of bones `names`, in rig space minus K.
    A bone's own rest rotation (one axis) goes on each of its elements."""
    su, sv = 16.0 / res["width"], 16.0 / res["height"]
    out = []
    for name in names:
        b = bones[name]
        cubes, rot = cubes_of(bones, name)
        for c in cubes:
            f = [c["from"][i] - K[i] for i in range(3)]
            t = [c["to"][i] - K[i] for i in range(3)]
            for v in f + t:
                if not -16 <= v <= 32:
                    raise SystemExit("%s: %s element out of -16..32 (%s)" % (KEY, name, v))
            el = {"from": [round(v, 4) for v in f], "to": [round(v, 4) for v in t], "faces": {}}
            if rot:
                axis, ang = rot
                el["rotation"] = {"origin": [round(b["pivot"][i] - K[i], 4) for i in range(3)],
                                  "axis": axis, "angle": ang}
            for face, data in c["faces"].items():
                if data.get("texture") is None:
                    continue
                u0, v0, u1, v1 = data["uv"]
                el["faces"][face] = {"uv": [round(u0 * su, 4), round(v0 * sv, 4),
                                            round(u1 * su, 4), round(v1 * sv, 4)], "texture": "#0"}
                if data.get("rotation"):
                    el["faces"][face]["rotation"] = data["rotation"]
            out.append(el)
    return out


def bounds(bones, names):
    lo, hi = [1e9] * 3, [-1e9] * 3
    for name in names:
        for c in cubes_of(bones, name)[0]:
            lo = [min(lo[i], c["from"][i]) for i in range(3)]
            hi = [max(hi[i], c["to"][i]) for i in range(3)]
    return lo, hi


def write_models():
    bones, png, res = dm.load_bbmodel(Rig)
    assets = os.path.join(RP, "assets", NS)
    tex = os.path.join(assets, "textures", "item", KEY, "atlas.png")
    os.makedirs(os.path.dirname(tex), exist_ok=True)
    with open(tex, "wb") as fh:
        fh.write(png)
    textures = {"0": Rig.tex, "particle": Rig.tex}

    # helmet: its centre on the model centre, which the head layer puts on
    # the head's centre
    lo, hi = bounds(bones, ["helmet"])
    K = [(lo[i] + hi[i]) / 2 - 8 for i in range(3)]
    s = HELMET_SCALE
    helmet = {"textures": textures, "elements": elements(bones, ["helmet"], K, res), "display": {
        "head": {"scale": [s, s, s]},
        "gui": {"rotation": [30, 225, 0], "scale": [1.05, 1.05, 1.05]},
        "ground": {"translation": [0, 3, 0], "scale": [0.5, 0.5, 0.5]},
        "fixed": {"rotation": [0, 180, 0], "scale": [1.0, 1.0, 1.0]},
        "thirdperson_righthand": {"rotation": [75, 45, 0], "translation": [0, 2.5, 0], "scale": [0.45, 0.45, 0.45]},
        "firstperson_righthand": {"rotation": [0, 45, 0], "scale": [0.5, 0.5, 0.5]},
    }}

    # chestplate: one model, worn through a display (mode "none") and also
    # drawn as the item
    lo, hi = bounds(bones, CHEST_BONES)
    Kc = [(lo[i] + hi[i]) / 2 - 8 for i in range(3)]
    chest = {"textures": textures, "elements": elements(bones, CHEST_BONES, Kc, res), "display": {
        "gui": {"rotation": [20, 205, 0], "scale": [0.72, 0.72, 0.72]},
        "ground": {"translation": [0, 3, 0], "scale": [0.4, 0.4, 0.4]},
        "fixed": {"rotation": [0, 180, 0], "scale": [0.75, 0.75, 0.75]},
        "thirdperson_righthand": {"rotation": [75, 45, 0], "translation": [0, 2.5, 0], "scale": [0.35, 0.35, 0.35]},
        "firstperson_righthand": {"rotation": [0, 45, 0], "scale": [0.4, 0.4, 0.4]},
    }}
    for name, model in (("full_metal_helmet", helmet), ("full_metal_chestplate", chest)):
        wj(os.path.join(assets, "models", "item", name + ".json"), model)
        wj(os.path.join(assets, "items", name + ".json"),
           {"model": {"type": "minecraft:model", "model": "%s:item/%s" % (NS, name)}})

    # worn chest: the display sits at the player's feet facing the player's yaw
    T = dm.display_matrix(Rig, bones, None, Kc, W=dm.ident())
    return dm.snbt_components(Rig, dm.components(T, 1.0))


def write_sounds():
    assets = os.path.join(RP, "assets", NS)
    out = os.path.join(assets, "sounds", KEY)
    os.makedirs(out, exist_ok=True)
    path = os.path.join(assets, "sounds.json")
    doc = {}
    if os.path.isfile(path):
        with io.open(path, encoding="utf-8") as fh:
            doc = json.load(fh)
    prefix = KEY + "."
    doc = {k: v for k, v in doc.items() if not k.startswith(prefix)}
    lang = {"zh_cn": {}, "en_us": {}}
    for event, (zh, en, files) in SOUNDS.items():
        entries = []
        for src in files:
            name = os.path.splitext(src)[0].lower().replace("-", "_")
            shutil.copyfile(os.path.join(REF, "sounds", src), os.path.join(out, name + ".ogg"))
            entries.append("%s:%s/%s" % (NS, KEY, name))
        key = "subtitles.%s.%s.%s" % (NS, KEY, event)
        doc[prefix + event] = {"subtitle": key, "sounds": entries}
        lang["zh_cn"][key], lang["en_us"][key] = zh, en
    wj(path, dict(sorted(doc.items())))
    for code, keys in lang.items():
        lp = os.path.join(assets, "lang", code + ".json")
        ldoc = {}
        if os.path.isfile(lp):
            with io.open(lp, encoding="utf-8") as fh:
                ldoc = json.load(fh)
        ldoc.update(keys)
        wj(lp, ldoc)


# ---------------------------------------------------------------------------
# 数据包
# ---------------------------------------------------------------------------

def patch_give(path):
    """In every item of the two, in either syntax:
    `give @a leather_helmet[trim=...,dyed_color=N,custom_name=...]` or
    `{id:"minecraft:leather_helmet",count:1,components:{"minecraft:trim":...}}`."""
    with io.open(path, encoding="utf-8") as fh:
        text = fh.read()
    count = 0
    for name, (base, slot, model, sound) in ITEMS.items():
        # no asset_id: no armour layer is drawn.  The sound event lives only
        # in the resource pack, so it goes inline (a bare id fails to parse)
        equippable = '{slot:"%s",equip_sound:{sound_id:"%s:%s.%s"}}' % (slot, NS, KEY, sound)
        pat = re.compile(r'(%s)(\[|",count:1,components:\{)(.{0,300}?)("text":"%s")' % (base, name), re.S)

        def fix(m):
            nonlocal count
            head, opener, mid, tail = m.groups()
            count += 1
            if KEY in mid:                   # already done
                return m.group(0)
            if opener == "[":
                mid = re.sub(r'trim=\{[^}]*\},', "", mid)
                mid = re.sub(r'dyed_color=\d+,', "", mid)
                mid = 'equippable=%s,item_model="%s:%s",' % (equippable, NS, model) + mid
            else:
                mid = re.sub(r'"minecraft:trim":\{[^}]*\},', "", mid)
                mid = re.sub(r'"minecraft:dyed_color":\d+,', "", mid)
                mid = '"minecraft:equippable":%s,"minecraft:item_model":"%s:%s",' % (
                    equippable, NS, model) + mid
            return head + opener + mid + tail
        text = pat.sub(fix, text)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    return count


def write_runtime(transformation):
    fn = os.path.join(DP, "data", NS, "function", KEY)
    pred = os.path.join(DP, "data", NS, "predicate", KEY)
    wj(os.path.join(pred, "wearing.json"), {
        "condition": "minecraft:entity_properties", "entity": "this",
        "predicate": {"equipment": {"chest": {
            "items": "minecraft:leather_chestplate",
            "components": {"minecraft:item_model": "%s:full_metal_chestplate" % NS}}}}})
    wj(os.path.join(pred, "hidden.json"), {"condition": "minecraft:any_of", "terms": [
        {"condition": "minecraft:entity_properties", "entity": "this",
         "predicate": {"effects": {"minecraft:invisibility": {}}}},
        {"condition": "minecraft:entity_properties", "entity": "this",
         "predicate": {"flags": {"is_swimming": True}}},
        {"condition": "minecraft:entity_properties", "entity": "this",
         "predicate": {"flags": {"is_flying": True}}},
    ]})
    wj(os.path.join(pred, "sneaking.json"), {
        "condition": "minecraft:entity_properties", "entity": "this",
        "predicate": {"flags": {"is_sneaking": True}}})

    part = "type=minecraft:item_display,tag=rpg.fm.part"
    wf(os.path.join(fn, "load.mcfunction"), [
        "# 都灵裹尸布的穿戴外观（add_full_metal_armor.py）",
        "scoreboard objectives add rpg_fm_id dummy",
    ])
    wf(os.path.join(fn, "tick.mcfunction"), [
        "# 都灵裹尸布（全金属盔甲胸甲）的穿戴外观：每个穿着它的玩家一个展示实体，",
        "# 每刻跟到玩家脚下。没人穿、也没有残留时直接返回。",
        "execute unless entity @a[predicate=%s:%s/wearing,limit=1] unless entity @e[%s,limit=1] run return 0"
        % (NS, KEY, part),
        "tag @e[%s] remove rpg.fm.seen" % part,
        "execute as @a[predicate=%s:%s/wearing,predicate=!%s:%s/hidden,gamemode=!spectator] at @s "
        "run function %s:%s/follow" % (NS, KEY, NS, KEY, NS, KEY),
        "# 脱下、隐身、下线、离得太远：没被认领的一律清掉",
        "kill @e[%s,tag=!rpg.fm.seen]" % part,
    ])
    wf(os.path.join(fn, "follow.mcfunction"), [
        "# as 穿戴者，at 其脚下。",
        "execute unless score @s rpg_fm_id matches 1.. store result score @s rpg_fm_id "
        "run scoreboard players add #next rpg_fm_id 1",
        "scoreboard players operation #id rpg_fm_id = @s rpg_fm_id",
        "execute as @e[%s,distance=..6] if score @s rpg_fm_id = #id rpg_fm_id run tag @s add rpg.fm.mine" % part,
        "execute unless entity @e[%s,tag=rpg.fm.mine,limit=1] run function %s:%s/summon" % (part, NS, KEY),
        "execute if predicate %s:%s/sneaking rotated ~ 0 positioned ~ ~-%s ~ as @e[%s,tag=rpg.fm.mine] "
        "run tp @s ~ ~ ~ ~ ~" % (NS, KEY, SNEAK_DROP, part),
        "execute unless predicate %s:%s/sneaking rotated ~ 0 as @e[%s,tag=rpg.fm.mine] run tp @s ~ ~ ~ ~ ~"
        % (NS, KEY, part),
        "tag @e[%s,tag=rpg.fm.mine] add rpg.fm.seen" % part,
        "tag @e[%s,tag=rpg.fm.mine] remove rpg.fm.mine" % part,
    ])
    wf(os.path.join(fn, "summon.mcfunction"), [
        'summon minecraft:item_display ~ ~ ~ {Tags:["rpg.fm.part","rpg.fm.new"],'
        'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"%s:full_metal_chestplate"}},'
        'item_display:"none",teleport_duration:1,view_range:1f,transformation:%s}' % (NS, transformation),
        "scoreboard players operation @e[%s,tag=rpg.fm.new] rpg_fm_id = #id rpg_fm_id" % part,
        "tag @e[%s,tag=rpg.fm.new] add rpg.fm.mine" % part,
        "tag @e[%s,tag=rpg.fm.new] remove rpg.fm.new" % part,
    ])
    dm.hook_tag(DP, "tick", "%s:%s/tick" % (NS, KEY), True)
    dm.hook_tag(DP, "load", "%s:%s/load" % (NS, KEY), False)


def main():
    transformation = write_models()
    write_sounds()
    give = os.path.join(DP, "data", NS, "function", "command", "give")
    if os.path.isdir(give):
        n = sum(patch_give(os.path.join(give, f)) for f in ("weapon.mcfunction", "box.mcfunction"))
        if n != 4:
            raise SystemExit("full_metal_armor: expected 4 items (2 in weapon, 2 in box), patched %d" % n)
        write_runtime(transformation)
        print("full_metal_armor: %d items" % n)


if __name__ == "__main__":
    main()
