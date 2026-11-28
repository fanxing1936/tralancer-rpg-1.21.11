# -*- coding: utf-8 -*-
"""营火工作台（方案书「原质二十二路径与面板重构」·工作台，2026-11-26 用户「全部照默认」）。

空手右键灵魂营火 → 工作台总页：五张卡片（冶炼 / 养成 / 锻造 / 转换 / 炼药与制器），每张写清
要拿什么、身上有多少，点卡片下的按钮进那一项。原来的「拿着材料对准营火右键」照旧能用。

- 冶炼、炼药、制器原本要主手拿着器胚 / 空瓶 / 空白圣具：从总页进时，若主手空着就从背包取一件放到主手
  （这几样都是同一张掉落表出来的同一件东西，清一件、补一件，不会丢数据）。
- 各子页（冶炼选型、主材、罪器、转换、图纸、炼药、制器）顶上加一条工作台页签，任何一页一下到任何一页。
- 按钮仍走 rpg_fg_do（80..86 是本文件的），经 rpg:forge/smelt/do 路由。

排在 add_panel_v2 之后。
"""

import io
import json
import os
import re
import sys

import rpg_ui_style as ui

DP = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "../rpg")
FUNC = os.path.join(DP, "data/rpg/function")
GOLD, GLOSS, BODY, NAME, MUTED = ui.BROADCAST_HOLY, ui.BROADCAST_GLOSS, ui.BROADCAST_BODY, ui.BROADCAST_NAME, ui.MUTED
import forge_spec as FS
from add_alchemy import C_ALC

C_FORGE = FS.C_FORGE
B = "rpg:bench"
MAT = lambda k: '*[minecraft:custom_data~{rpg_mat:"%s"}]' % k
TABS = [(80, "冶炼", "Smelt"), (81, "养成", "Temper"), (82, "锻造", "Forge"), (83, "转换", "Convert"), (84, "炼药与制器", "Alchemy"), (87, "熔铸", "Fuse")]   # 87：add_fusion.py
COUNT = [0]


def txt(s, c=BODY, b=False):
    return {"text": s, "color": c, "bold": b, "italic": False}


def dump(v):
    return json.dumps(ui.darken(v), ensure_ascii=False, separators=(",", ":"))


def raw(v):
    return json.dumps(v, ensure_ascii=False, separators=(",", ":"))


def path_of(rel):
    return os.path.join(FUNC, rel.replace("/", os.sep) + ".mcfunction")


def read(rel):
    return io.open(path_of(rel), encoding="utf-8").read()


def write(rel, lines):
    p = path_of(rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if isinstance(lines, list):
        lines = "\n".join(lines).rstrip("\n") + "\n"
    with io.open(p, "w", encoding="utf-8", newline="\n") as h:
        h.write(lines)
    COUNT[0] += 1


def jw(rel, doc):
    p = os.path.join(DP, "data", rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as h:
        json.dump(doc, h, ensure_ascii=False, indent=2)


def bar(active):
    parts = [""]
    import add_panel_v2 as PV
    icons = {80: "tab_smelt", 81: "tab_grow", 82: "tab_forge", 83: "tab_convert", 84: "tab_brew"}
    for i, (v, name, gloss) in enumerate([(86, "工作台", "Workbench")] + TABS):
        if i:
            parts.append(txt("  ·  ", GLOSS))
        on = v == active
        ic = PV.icon(icons[v]) if v in icons else None
        if ic:
            parts += [dict(ic, click_event={"action": "run_command", "command": "/trigger rpg_fg_do set %d" % v}), txt(" ", MUTED)]
        parts.append({"text": ("" if ic else "◆ " if on else "") + name, "color": GOLD if on else MUTED, "bold": on, "italic": False,
                      "click_event": {"action": "run_command", "command": "/trigger rpg_fg_do set %d" % v},
                      "hover_event": {"action": "show_text", "value": txt(ui.fraktur(gloss), GLOSS)}})
    return {"type": "minecraft:plain_message", "width": 360, "contents": ui.darken(parts)}


def card(model, head, lines, colour=NAME):
    return {"type": "minecraft:item", "item": {"id": "minecraft:paper", "count": 1, "components": {"minecraft:item_model": model}},
            "description": {"contents": ["", txt(head + "\n", colour, True)] + [txt(l + ("\n" if i < len(lines) - 1 else ""), BODY) for i, l in enumerate(lines)],
                            "width": 270},
            "show_decorations": False, "show_tooltip": False, "width": 16, "height": 16}


def dialog(title, body, actions, columns=3):
    return {"type": "minecraft:multi_action", "title": title, "body": body,
            "actions": [{"label": txt(l, c, True), "action": {"type": "minecraft:run_command", "command": "/trigger rpg_fg_do set %d" % v}} for l, c, v in actions],
            "columns": columns, "exit_action": {"label": txt("离开", BODY)},
            "can_close_with_escape": True, "pause": False, "after_action": "close"}


def title(name, gloss):
    return ["", txt("工作台 · ", GOLD, True), txt(name, NAME, True), txt(" " + ui.fraktur(gloss), GLOSS)]


COUNTS = [("nb", MAT("blank")), ("ns", 'minecraft:paper[minecraft:custom_data~{rpg_mat:"soul"}]'), ("nf", MAT("forge_stone")),
          ("nw", MAT("wash_gem")), ("ng", MAT("gild_leaf")), ("nk", MAT("sin_shard")), ("np", MAT("bp_frag")), ("nv", MAT("vial")), ("nt", MAT("blank_rite"))]


def build():
    # 入口：空手右键灵魂营火。原版空手点营火什么也不「消耗」，任何方块进度都不响；
    # 所以空手、准星对着灵魂营火时，在火上放一个交互实体（看别处或手里拿东西就收走），右键它开工作台。
    # 手里拿着东西不放实体：材料右键、原版烤食物都照旧。
    write("bench/tick", ["# 每 4 刻：空手看着灵魂营火的玩家（rpg:bench/tick 挂在 tick 标签）",
                         "scoreboard players add #t rpg_bn 1",
                         "execute if score #t rpg_bn matches 4.. run function %s/scan" % B,
                         "execute as @e[type=minecraft:interaction,tag=rpg.bench] run function %s/age" % B])
    write("bench/scan", ["scoreboard players set #t rpg_bn 0",
                         "execute as @a[gamemode=!spectator] unless items entity @s weapon.mainhand * at @s anchored eyes positioned ^ ^ ^ run function %s/look" % B])
    write("bench/look", ["scoreboard players set #i rpg_bn 20", "function %s/ray" % B])
    write("bench/ray", ["execute if block ~ ~ ~ minecraft:soul_campfire align xyz positioned ~0.5 ~ ~0.5 run return run function %s/mark" % B,
                        "execute unless block ~ ~ ~ #minecraft:replaceable run return 0",
                        "scoreboard players remove #i rpg_bn 1",
                        "execute if score #i rpg_bn matches 1.. positioned ^ ^ ^0.25 run function %s/ray" % B])
    write("bench/mark", ["execute unless entity @e[type=minecraft:interaction,tag=rpg.bench,distance=..0.2] run summon minecraft:interaction ~ ~ ~ {Tags:[\"rpg.bench\"],width:1.02f,height:0.5f,response:1b}",
                         "scoreboard players set @e[type=minecraft:interaction,tag=rpg.bench,distance=..0.2] rpg_bn 6"])
    write("bench/age", ["scoreboard players remove @s rpg_bn 1", "execute if score @s rpg_bn matches ..0 run kill @s"])
    write("bench/load", ["scoreboard objectives add rpg_bn dummy", "kill @e[type=minecraft:interaction,tag=rpg.bench]"])
    for kind, entry in (("load", B + "/load"), ("tick", B + "/tick")):
        tp = os.path.join(DP, "data/minecraft/tags/function/%s.json" % kind)
        doc = json.load(io.open(tp, encoding="utf-8"))
        if entry not in doc["values"]:
            doc["values"].append(entry)
        jw("minecraft/tags/function/%s.json" % kind, doc)
    jw("rpg/advancement/bench/use.json", {"criteria": {"u": {"trigger": "minecraft:player_interacted_with_entity", "conditions": {
        "entity": [{"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"type": "minecraft:interaction", "nbt": "{Tags:[\"rpg.bench\"]}"}}]}}},
        "rewards": {"function": B + "/use"}})
    write("bench/use", ["# 右键了营火上的交互实体（as 玩家）：空手开工作台；万一手里刚换上东西，交给原来的材料右键",
                        "advancement revoke @s only rpg:bench/use",
                        "execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_fm:1b}] run return run function rpg:forge/use",
                        "execute if items entity @s weapon.mainhand * run return 0",
                        "execute if entity @s[tag=rpg.fg.ui] run return 0",
                        "tag @s add rpg.fg.ui", "scoreboard players set @s rpg_fg_lk 6",
                        "function %s/home" % B])
    # 总页
    cnt = ["execute store result storage rpg:bench d.%s int 1 run clear @s %s 0" % (k, sel) for k, sel in COUNTS]
    write("bench/home", ["# 工作台总页（as/at 玩家）",
                         "scoreboard players set #i rpg_fg 30", "scoreboard players set #found rpg_fg 0",
                         "execute anchored eyes positioned ^ ^ ^ run function rpg:forge/smelt/ray",
                         "execute if score #found rpg_fg matches 0 run return run tellraw @s " + raw(["", txt("[工作台] ", C_FORGE, True), txt("对准灵魂营火右键", ui.WARN)]),
                         "scoreboard players enable @s rpg_fg_do", "scoreboard players set @s rpg_fg_op 10", "scoreboard players set @s rpg_fg_arg -1",
                         "playsound minecraft:block.campfire.crackle player @s ~ ~ ~ 1 0.8"] + cnt + ["function %s/home_m with storage rpg:bench d" % B])
    body = [bar(86),
            card("rpg:forge/blank", "冶炼", ["器胚 + 主材 + 残魂 → 一件新装备", "身上　器胚 $(nb)　残魂 $(ns)"], C_FORGE),
            card("rpg:forge/forge_stone", "养成", ["副手拿装备，主手拿锻石、洗炼钻、鎏金叶、源、符文或符石，对准营火右键", "身上　锻石 $(nf)　洗炼钻 $(nw)　鎏金叶 $(ng)"], C_FORGE),
            card("rpg:world/sin_shard", "锻造", ["罪印碎片锻造一柱的罪器；副手拿图纸锻造图纸武器", "身上　罪印碎片 $(nk)"], C_FORGE),
            card("rpg:world/blueprint_fragment", "转换", ["材料互换；10 片图纸碎片合一张自选图纸", "身上　图纸碎片 $(np)"], C_FORGE),
            card("rpg:relic/empty_vial", "炼药与制器", ["空瓶加遗物炼药；空白圣具加遗物做驱魔器具", "身上　空瓶 $(nv)　空白圣具 $(nt)"], C_ALC),
            card("rpg:town/tab_fuse", "熔铸与拆解", ["两把同类祭品熔进主件，品质升一档；完美再熔加淬炼星", "不要的装备拆掉，退回一半主材和镶嵌"], C_FORGE)]
    acts = [(name, GOLD if v != 84 else C_ALC, v) for v, name, _g in TABS[:4]] + [("炼药", C_ALC, 84), ("制器", C_ALC, 85), ("熔铸", GOLD, 87)]
    write("bench/home_m", ["$dialog show @s " + dump(dialog(title("总台", "Workbench"), body, acts))])

    # 路由
    do = ["# 工作台按钮 80..86（rpg:forge/smelt/do 转来）",
          "execute if score #do rpg_fg matches 86 run return run function %s/home" % B,
          "execute if score #do rpg_fg matches 80 run return run function %s/smelt" % B,
          "execute if score #do rpg_fg matches 81 run return run function %s/grow" % B,
          "execute if score #do rpg_fg matches 82 run return run function %s/forge" % B,
          "execute if score #do rpg_fg matches 83 run return run function %s/conv" % B,
          "execute if score #do rpg_fg matches 84 run return run function %s/potion" % B,
          "execute if score #do rpg_fg matches 85 run return run function %s/rite" % B]
    write("bench/do", do)
    s = read("forge/smelt/do")
    if B + "/do" not in s:
        a = "execute if score #do rpg_fg matches 50..59"
        i = s.index(a)
        s = s[:i] + "execute if score #do rpg_fg matches 80..89 run return run function %s/do\n" % B + s[i:]
        write("forge/smelt/do", s)

    # 冶炼、炼药、制器：主手空着就从背包取一件
    for name, key, table, then, what in (("smelt", "blank", "rpg:forge/item/blank", "rpg:forge/smelt/open", "器胚"),
                                         ("potion", "vial", "rpg:potion/vial", "rpg:alc/open_potion", "空瓶"),
                                         ("rite", "blank_rite", "rpg:potion/blank_rite", "rpg:alc/open_rite", "空白圣具")):
        write("bench/" + name, [
            "execute if items entity @s weapon.mainhand %s run return run function %s" % (MAT(key), then),
            "execute if items entity @s weapon.mainhand * run return run tellraw @s " + raw(["", txt("[工作台] ", C_FORGE, True), txt("先空出主手，或主手拿着%s" % what, ui.WARN)]),
            "execute store result score #c rpg_fg run clear @s %s 0" % MAT(key),
            "execute if score #c rpg_fg matches 0 run return run tellraw @s " + raw(["", txt("[工作台] ", C_FORGE, True), txt("身上没有%s" % what, ui.WARN)]),
            "clear @s %s 1" % MAT(key),
            "loot replace entity @s weapon.mainhand loot %s" % table,
            "function " + then])
    # 养成：说明 + 身上的材料
    cnt = ["execute store result storage rpg:bench d.%s int 1 run clear @s %s 0" % (k, sel) for k, sel in COUNTS if k in ("nf", "nw", "ng")]
    write("bench/grow", cnt + ["function %s/grow_m with storage rpg:bench d" % B])
    body = [bar(81),
            card("rpg:forge/forge_stone", "锻石", ["装备经验 +1 级的进度；Lv.10 封顶", "身上 $(nf)"], C_FORGE),
            card("rpg:forge/wash_gem", "洗炼钻", ["重洗一条属性（先看洗前与洗后再确认）；也用来给路径翻面", "身上 $(nw)"], C_FORGE),
            card("rpg:forge/gild_leaf", "鎏金叶", ["把一条属性锁住，以后洗炼不动它", "身上 $(ng)"], C_FORGE),
            card("rpg:forge/source_faith", "源 · 符文 · 符石", ["源定装备的气质；符文给近战词缀；符石给 F 键技能"], C_FORGE),
            {"type": "minecraft:plain_message", "width": 320, "contents": txt("做法：副手拿要养成的装备，主手拿材料，对准营火右键。每一步都会先给你看改前与改后。", MUTED)}]
    write("bench/grow_m", ["$dialog show @s " + dump(dialog(title("养成", "Temper"), body, [("‹ 总台", NAME, 86)], 1))])
    # 锻造、转换：卡片 + 进原来的流程
    write("bench/forge", ["execute store result storage rpg:bench d.nk int 1 run clear @s %s 0" % MAT("sin_shard"),
                          "execute store result score #a rpg_fg run clear @s *[minecraft:item_model=\"rpg:world/blueprint_epic\"] 0",
                          "execute store result score #b rpg_fg run clear @s *[minecraft:item_model=\"rpg:world/blueprint_legend\"] 0",
                          "execute store result storage rpg:bench d.nbp int 1 run scoreboard players operation #a rpg_fg += #b rpg_fg",
                          "function %s/forge_m with storage rpg:bench d" % B])
    body = [bar(82),
            card("rpg:world/sin_shard", "罪器锻造", ["一柱的罪印碎片集够，锻那一柱的罪器", "身上　罪印碎片 $(nk)"], C_FORGE),
            card("rpg:world/blueprint_epic", "图纸锻造", ["副手拿图纸、主手拿器胚，按图纸做出武器", "身上　图纸 $(nbp)"], C_FORGE)]
    write("bench/forge_m", ["$dialog show @s " + dump(dialog(title("锻造", "Forge"), body, [("罪器锻造", GOLD, 50), ("图纸锻造", GOLD, 70), ("‹ 总台", NAME, 86)]))])
    write("bench/conv", ["execute store result storage rpg:bench d.np int 1 run clear @s %s 0" % MAT("bp_frag"),
                         "function %s/conv_m with storage rpg:bench d" % B])
    body = [bar(83),
            card("rpg:forge/soul", "材料转换", ["多余的材料按比例换成要的"], C_FORGE),
            card("rpg:world/blueprint_fragment", "碎片合图纸", ["10 片合一张自选图纸", "身上　图纸碎片 $(np)"], C_FORGE)]
    write("bench/conv_m", ["$dialog show @s " + dump(dialog(title("转换", "Convert"), body, [("材料转换", GOLD, 60), ("碎片合图纸", GOLD, 65), ("‹ 总台", NAME, 86)]))])

    # 子页顶上加工作台页签
    inject = {"forge/smelt/open": 80, "forge/smelt/tiers": 80, "forge/smelt/confirm": 80, "forge/sin/open": 82, "forge/bp/open": 82,
              "forge/conv/open": 83, "forge/conv/show": 83, "forge/bp/frag_open": 83, "alc/open_potion": 84, "alc/open_rite": 84}
    n = 0
    for rel, tab in inject.items():
        if not os.path.exists(path_of(rel)):
            continue
        s = read(rel)
        if "rpg_fg_do set 86" in s:
            n += 1
            continue
        out = []
        for line in s.split("\n"):
            m = re.match(r'^(\$?)(.*?)dialog show @s (\{.*\})$', line)
            if not m:
                out.append(line)
                continue
            line = inject_bar(line, raw(bar(tab)))
            out.append(line)
            n += 1
        write(rel, "\n".join(out))
    assert n >= 6, n


def inject_bar(line, bar_json):
    k = line.index('"body":') + len('"body":')
    if line[k] == "[":
        return line[:k + 1] + bar_json + "," + line[k + 1:]
    e = match_brace(line, k)
    return line[:k] + "[" + bar_json + "," + line[k:e + 1] + "]" + line[e + 1:]


def match_brace(s, i):
    assert s[i] == "{", s[i:i + 20]
    depth, q, esc = 0, False, False
    for k in range(i, len(s)):
        c = s[k]
        if q:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                q = False
            continue
        if c == '"':
            q = True
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return k
    raise ValueError("unbalanced")


def main():
    build()
    print("bench: %d functions" % COUNT[0])


if __name__ == "__main__":
    main()
