# -*- coding: utf-8 -*-
"""Add the Blood Covenant and ten Sephirah offerings.

The divine-covenant generator that runs later owns the Old/New Covenant
rewards.  This module deliberately stops at the completed tree so legacy
"ten sources = New Covenant" text cannot leak back into a future build.
"""

import io
import json
import os
import sys

import rpg_ui_style as ui


DP = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "../rpg")
FUNC = os.path.join(DP, "data/rpg/function")
ADV = os.path.join(DP, "data/rpg/advancement")
LOOT = os.path.join(DP, "data/rpg/loot_table")

SEPHIROTH = [
    (1, "kether", "王冠", "minecraft:white_dye", "#FFF8E0", 0.00, -3.60),
    (2, "chokmah", "智慧", "minecraft:light_gray_dye", "#A0A3AD", 1.45, -2.55),
    (3, "binah", "理解", "minecraft:black_dye", "#202028", -1.45, -2.55),
    (4, "chesed", "慈悲", "minecraft:blue_dye", "#1F85D1", 1.45, -0.86),
    (5, "geburah", "严厉", "minecraft:red_dye", "#C7262E", -1.45, -0.86),
    (6, "tiphareth", "美丽", "minecraft:yellow_dye", "#F4C73B", 0.00, 0.00),
    (7, "netzach", "胜利", "minecraft:green_dye", "#40AD48", 1.45, 1.28),
    (8, "hod", "光辉", "minecraft:orange_dye", "#EB6129", -1.45, 1.28),
    (9, "yesod", "基础", "minecraft:purple_dye", "#8538AD", 0.00, 2.43),
    (10, "malkuth", "王国", "minecraft:brown_dye", "#7A4630", 0.00, 3.86),
]

# Particle colours keep the dye/reference palette; text uses brighter UI-safe
# values so Binah, Yesod and Malkuth remain legible on Minecraft's dark tooltip.
SEPHIRAH_UI_COLOURS = {
    "kether": "#FFF2A8", "chokmah": "#C9CDD6", "binah": "#AAB4C3",
    "chesed": "#62B8F0", "geburah": "#FF5A62", "tiphareth": "#FFD85A",
    "netzach": "#70DB70", "hod": "#FF8A4A", "yesod": "#D596F2",
    "malkuth": "#C58A62",
}


def fpath(rel):
    return os.path.join(FUNC, rel.replace("/", os.sep))


def read(rel):
    with io.open(fpath(rel), encoding="utf-8") as handle:
        return handle.read()


def write(rel, content):
    target = fpath(rel)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with io.open(target, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(content.rstrip("\n") + "\n")


def write_json(rel, value):
    target = os.path.join(ADV, rel.replace("/", os.sep))
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with io.open(target, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def write_loot_json(rel, value):
    target = os.path.join(LOOT, rel.replace("/", os.sep))
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with io.open(target, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def raw(parts):
    return json.dumps([""] + parts, ensure_ascii=False, separators=(",", ":"))


def txt(value, color="white", bold=False):
    return ui.comp(value, color, bold)


def item_name(prefix, name, prefix_color, name_color):
    return ui.item_name(prefix, name, prefix_color, name_color)


def lore(lines):
    return ui.lore([[txt(line, color)] for line, color in lines])


USE = 'food={nutrition:0,saturation:0f,can_always_eat:1b},consumable={consume_seconds:100180f,animation:"block",sound:"minecraft:block.enchantment_table.use",has_consume_particles:false,on_consume_effects:[]}'


def contract_item(target):
    name = item_name("[秘仪]", "卡巴拉血契", ui.RITUAL, ui.WHITE)
    item_lore = ui.lore([
        [txt("以花之纹章为钥，展开卡巴拉生命之树", ui.GRAY)],
        [txt("长按右键依照朝向铺开法阵", ui.GRAY)],
        [ui.label("秘仪", "🔱"), txt("[生命之树]", ui.RITUAL, True)],
        [txt("　将十枚源质嵌入各自对应的圆心", ui.GRAY)],
        [txt("　十源质归位后，", ui.GRAY), txt("『旧约』", ui.HOLY_DARK, True),
         txt("显于人间", ui.GRAY)],
        [txt("　血契不会在展开法阵时消耗", ui.DARK_GRAY)],
    ])
    return 'give %s minecraft:flower_banner_pattern[custom_name=%s,lore=%s,enchantment_glint_override=true,max_stack_size=1,custom_data={rpg_kabbalah_use:1b,rpg_kabbalah_contract:1b},%s] 1' % (target, name, item_lore, USE)


def sephirah_item(target, row):
    n, key, chinese, item, color, _, _ = row
    ui_color = SEPHIRAH_UI_COLOURS[key]
    name = item_name("[源质]", "%02d · %s" % (n, chinese), ui.RITUAL, ui.WHITE)
    item_lore = ui.lore([
        [txt("卡巴拉生命之树的第 %d 源质" % n, ui.GRAY)],
        [txt("长按右键嵌入 ", ui.GRAY), txt("[%s]" % chinese, ui_color, True),
         txt(" 圆心", ui.GRAY)],
        [txt("错误位置或已归位时不会消耗", ui.DARK_GRAY)],
    ])
    return 'give %s %s[custom_name=%s,lore=%s,enchantment_glint_override=true,custom_data={rpg_kabbalah_use:1b,rpg_sephirah:%db},%s] 1' % (target, item, name, item_lore, n, USE)


def patch_objectives_runtime():
    rel = "command/soreboard.mcfunction"
    src = "\n".join(line for line in read(rel).splitlines() if not any(name in line for name in ("rpg_lt_fill", "rpg_lt_usecd", "rpg_lt_covenant", "rpg_lt_bless"))).rstrip()
    for objective in ("rpg_lt_fill", "rpg_lt_usecd", "rpg_lt_covenant", "rpg_lt_bless"):
        src += "\nscoreboard objectives add %s dummy" % objective
    write(rel, src)

    rel = "exorcism.mcfunction"
    lines = [line for line in read(rel).splitlines() if "卡巴拉血契输入冷却" not in line and "rpg_lt_usecd" not in line and "function rpg:ritual/life_tree/covenant_tick" not in line and "新约常驻祝福" not in line]
    lines += [
        "",
        "# 卡巴拉血契输入冷却；仅处理实际使用过仪式物品的玩家。",
        "execute as @a[scores={rpg_lt_usecd=1..}] run scoreboard players remove @s rpg_lt_usecd 1",
    ]
    write(rel, "\n".join(lines))


def patch_tree_files():
    rel = "ritual/life_tree/place.mcfunction"
    src = read(rel)
    needle = "scoreboard players set #life_tree rpg_lt_tick 0"
    if "scoreboard players set @e[type=minecraft:marker,tag=rpg.ritual.life_tree,distance=..2,limit=1,sort=nearest] rpg_lt_fill 0" not in src:
        src = src.replace(needle, "scoreboard players set @e[type=minecraft:marker,tag=rpg.ritual.life_tree,distance=..2,limit=1,sort=nearest] rpg_lt_fill 0\n" + needle)
    write(rel, src)

    rel = "ritual/life_tree/draw.mcfunction"
    src = "\n".join(line for line in read(rel).splitlines() if "FILLED " not in line and "rpg.lt." not in line)
    lines = [src.rstrip(), "", "# 已归位源质获得额外辉光，染料本体由 item_display 平放在圆心。"]
    for _, key, _, _, _, x, z in SEPHIROTH:
        lines.append("# FILLED %s" % key)
        lines.append("execute if entity @s[tag=rpg.lt.%s] run particle end_rod ^%.3f ^0.105 ^%.3f 0.18 0.02 0.18 0.01 3" % (key, x, z))
        lines.append("execute if entity @s[tag=rpg.lt.%s] run particle enchant ^%.3f ^0.085 ^%.3f 0.30 0.02 0.30 0.02 4" % (key, x, z))
    write(rel, "\n".join(lines))

    rel = "ritual/life_tree/clear.mcfunction"
    src = read(rel)
    cleanup = "execute as @e[type=minecraft:marker,tag=rpg.ritual.life_tree,distance=..12] at @s run kill @e[type=minecraft:item_display,tag=rpg.ritual.life_tree.prop,distance=..8]"
    if cleanup not in src:
        src = src.replace("kill @e[type=minecraft:marker", cleanup + "\nkill @e[type=minecraft:marker")
    write(rel, src)

    rel = "ritual/life_tree/clear_all.mcfunction"
    write(rel, """kill @e[type=minecraft:item_display,tag=rpg.ritual.life_tree.prop]
kill @e[type=minecraft:marker,tag=rpg.ritual.life_tree]
""")


def build_advancement_and_input():
    write_json("ritual/life_tree/use.json", {
        "criteria": {"use": {
            "trigger": "minecraft:using_item",
            "conditions": {"item": {"predicates": {"minecraft:custom_data": "{rpg_kabbalah_use:1b}"}}},
        }},
        "rewards": {"function": "rpg:ritual/life_tree/input"},
    })

    lines = [
        "advancement revoke @s only rpg:ritual/life_tree/use",
        "scoreboard players add @s rpg_lt_usecd 0",
        "execute if score @s rpg_lt_usecd matches 1.. run return 0",
        "scoreboard players set @s rpg_lt_usecd 8",
        "execute if items entity @s weapon.mainhand minecraft:flower_banner_pattern[minecraft:custom_data~{rpg_kabbalah_contract:1b}] run return run function rpg:ritual/life_tree/place",
        "tag @s add rpg.kabbalah.user",
    ]
    for n, key, _, item, _, x, z in SEPHIROTH:
        lines.append(
            "execute if items entity @s weapon.mainhand %s[minecraft:custom_data~{rpg_sephirah:%db}] at @s as @e[type=minecraft:marker,tag=rpg.ritual.life_tree,tag=!rpg.lt.complete,distance=..12,sort=nearest,limit=1] at @s positioned ^%.3f ^0.06 ^%.3f if entity @a[tag=rpg.kabbalah.user,distance=..0.68,limit=1] run return run function rpg:ritual/life_tree/offer/%d"
            % (item, n, x, z, n))
    lines += [
        "tellraw @s " + raw([txt("[秘仪] ", ui.RITUAL, True), txt("源质未响应；请站入名称对应的圆心。", ui.GRAY)]),
        "tag @s remove rpg.kabbalah.user",
    ]
    write("ritual/life_tree/input.mcfunction", "\n".join(lines))


def build_offers():
    display = '{Tags:["rpg.ritual.life_tree.prop","rpg.ritual.life_tree.prop.%s"],item:{id:"%s",count:1,components:{"minecraft:enchantment_glint_override":1b}},item_display:"ground",view_range:0.65f,shadow_radius:0.15f,shadow_strength:0.38f,brightness:{block:15,sky:12},transformation:{translation:[0f,0.035f,0f],scale:[0.72f,0.72f,0.72f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}'
    for n, key, chinese, item, color, _, _ in SEPHIROTH:
        ui_color = SEPHIRAH_UI_COLOURS[key]
        msg_ok = raw([txt("[源质·%02d] " % n, ui.RITUAL, True),
                      txt(chinese, ui_color, True), txt("归位。", ui.GRAY),
                      txt("　完成度 ", ui.GRAY),
                      {"score": {"name": "@s", "objective": "rpg_lt_fill"},
                       "color": ui_color, "bold": True, "italic": False},
                      txt("/10", ui.DARK_GRAY)])
        msg_dup = raw([txt("[源质·%02d] " % n, ui.RITUAL, True),
                       txt(chinese, ui_color, True), txt("已经归位。", ui.GRAY)])
        body = [
            "execute if entity @s[tag=rpg.lt.%s] run tellraw @a[tag=rpg.kabbalah.user,distance=..1,limit=1] %s" % (key, msg_dup),
            "execute if entity @s[tag=rpg.lt.%s] run tag @a[tag=rpg.kabbalah.user,distance=..1] remove rpg.kabbalah.user" % key,
            "execute if entity @s[tag=rpg.lt.%s] run return 0" % key,
            "tag @s add rpg.lt.%s" % key,
            "scoreboard players add @s rpg_lt_fill 1",
            "clear @a[tag=rpg.kabbalah.user,distance=..1,sort=nearest,limit=1] %s[minecraft:custom_data~{rpg_sephirah:%db}] 1" % (item, n),
            "summon minecraft:item_display ~ ~0.04 ~ " + (display % (key, item)),
            "particle dust{color:[%s],scale:1.25} ~ ~0.10 ~ 0.40 0.03 0.40 0.02 22" % ",".join("%.3f" % (int(color[i:i+2], 16) / 255.0) for i in (1, 3, 5)),
            "particle end_rod ~ ~0.12 ~ 0.28 0.05 0.28 0.02 12",
            "playsound minecraft:block.amethyst_block.resonate ambient @a[distance=..16] ~ ~ ~ 0.65 %.2f" % (0.78 + n * 0.035),
            "tellraw @a[tag=rpg.kabbalah.user,distance=..1,limit=1] " + msg_ok,
            "execute if score @s rpg_lt_fill matches 10.. at @s run function rpg:ritual/life_tree/complete",
            "tag @a[tag=rpg.kabbalah.user,distance=..1] remove rpg.kabbalah.user",
        ]
        write("ritual/life_tree/offer/%d.mcfunction" % n, "\n".join(body))


def patch_give_catalog():
    all_lines = ["# 卡巴拉血契与十源质。"]
    all_lines.append(contract_item("@s"))
    all_lines.extend(sephirah_item("@s", row) for row in SEPHIROTH)
    write("ritual/life_tree/give/all.mcfunction", "\n".join(all_lines))

    rel = "command/give/extra.mcfunction"
    marker_a = "# == KABBALAH LIFE TREE ITEMS =="
    marker_b = "# == END KABBALAH LIFE TREE ITEMS =="
    src = read(rel)
    if marker_a in src and marker_b in src:
        before, rest = src.split(marker_a, 1)
        _, after = rest.split(marker_b, 1)
        src = before.rstrip() + "\n" + after.lstrip("\n")
    catalog = [marker_a, contract_item("@a")]
    catalog.extend(sephirah_item("@a", row) for row in SEPHIROTH)
    catalog.append(marker_b)
    write(rel, src.rstrip() + "\n\n" + "\n".join(catalog))


def main():
    patch_objectives_runtime()
    patch_tree_files()
    build_advancement_and_input()
    build_offers()
    patch_give_catalog()
    print("kabbalah covenant: blood pact + 10 dye Sephiroth (rewards owned by divine generator)")


if __name__ == "__main__":
    main()
