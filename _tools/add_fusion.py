# -*- coding: utf-8 -*-
"""武器熔铸、拆解、淬炼星（《开局参与感》策划书「武器熔铸」一节）：营火工作台第六页签「熔铸」。

- 熔铸：主手拿要保留的主件，背包里两把同类的「祭品」（品质不低于主件低一档），花残魂（1 / 2 / 4 / 6），
  主件品质升一档（残次 → 普通 → 精良 → 完美）；已经完美的再熔，加一颗淬炼星（每颗基础伤害或护甲 +2%，最多 5 颗，品质名后显示 ★）。
  主件的等级、经验、源、符文、符石、镀金、名字都留下；两把祭品各自经验的一半加给主件，祭品身上的符文、符石、源熔掉（想留就先拆解）。
- 拆解：主手的装备拆掉，返还一半主材、1 枚残魂，身上的符文、符石、源原样退回。
- 同类：长剑跟长剑、战斧跟战斧……头盔跟头盔（按物品种类判断，档次可以不同）。
- 每次熔铸或拆解给 rpg_tl_fu 加一（城镇支线「铁匠的学徒」）。
- 升档熔铸：完美的主件 + 两把同类、同档、完美的祭品，再加下一档主材的一半（无档 → 勇者：钻石 ×2；勇者 → 史诗：下界合金锭 ×1、钻石 ×2），
  熔成上一档的同类装备，品质回到精良；等级、经验、源、符文、符石留下，淬炼星清零。
- 祭品只认魂火冶炼出来的装备（custom_data 带 rpg_forged）：罪器、图纸武器、首领掉的传说武器只能当主件。

python add_fusion.py ../rpg
"""
import io
import json
import os
import sys

import rpg_ui_style as ui
import forge_spec as S

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data", "rpg", "function")
F = "rpg:forge/fuse"
O = "rpg_fg"
WS = "@e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1]"
EQ = 'item.components."minecraft:custom_data".rpg_eq'
SOUL = 'minecraft:paper[minecraft:custom_data~{rpg_mat:"soul"}]'
COUNT = [0]
CLASSES = {  # 键: (名, 物品)
    "sword": ("长剑", ["iron_sword", "diamond_sword", "netherite_sword"]), "axe": ("战斧", ["iron_axe", "diamond_axe", "netherite_axe"]),
    "mace": ("重锤", ["mace"]), "bow": ("长弓", ["bow"]), "crossbow": ("劲弩", ["crossbow"]),
    "head": ("头盔", ["iron_helmet", "diamond_helmet", "netherite_helmet"]), "chest": ("胸甲", ["iron_chestplate", "diamond_chestplate", "netherite_chestplate"]),
    "legs": ("护腿", ["iron_leggings", "diamond_leggings", "netherite_leggings"]), "feet": ("战靴", ["iron_boots", "diamond_boots", "netherite_boots"]),
}
GRADES = [("残次", -10, -6), ("普通", -5, 5), ("精良", 6, 10), ("完美", 11, 15)]
COST = [1, 2, 4, 6]
RUNES = [r for r in "backstab bloodpact echo ember execute hunt lastbreath meteor poise recoil split stillwater swift".split()]
STONES = "banner blood frost gale rift shadow volley".split()
SOURCES = "faith hatred hope malice pride resolve".split()
GOLD = ui.BROADCAST_HOLY
BODY = ui.BROADCAST_BODY
NAME = ui.BROADCAST_NAME
C_FORGE = S.C_FORGE


def J(c):
    return json.dumps(c, ensure_ascii=False, separators=(",", ":"))


def T(text, colour=BODY, bold=False):
    return {"text": text, "color": colour, "bold": bold, "italic": False}


def fn(name, lines):
    path = os.path.join(FUNC, "forge", "fuse", name + ".mcfunction")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    COUNT[0] += 1


def read(rel):
    return io.open(os.path.join(FUNC, rel + ".mcfunction"), encoding="utf-8").read()


def write(rel, s):
    io.open(os.path.join(FUNC, rel + ".mcfunction"), "w", encoding="utf-8", newline="\n").write(s)


def say(text, colour=BODY):
    return "tellraw @s " + J(["", T("[熔铸] ", C_FORGE, True), T(text, colour)])


def grade_of(src, dst):
    return ["scoreboard players set %s %s 0" % (dst, O)] + [
        "execute if score %s %s matches %d.. run scoreboard players set %s %s %d" % (src, O, lo, dst, O, g) for g, (_n, lo, _hi) in enumerate(GRADES) if g]


TIERS = ["plain", "brave", "epic"]
UP_COST = {0: [("diamond", 2)], 1: [("netherite_ingot", 1), ("diamond", 2)]}


def tier_lines(slot_item, dst):
    """档次（0 无档 1 勇者 2 史诗）：剑斧护甲看底材；重锤看耐久附魔；弓弩取「力量/快速装填」与「耐久」两者的较小值（镀金只会抬一条）。"""
    return ["scoreboard players set %s %s 0" % (dst, O),
            "execute if items %s #rpg:fuse/t_brave run scoreboard players set %s %s 1" % (slot_item, dst, O),
            "execute if items %s #rpg:fuse/t_epic run scoreboard players set %s %s 2" % (slot_item, dst, O)]


def build():
    for k, (zh, items) in CLASSES.items():
        p = os.path.join(DP, "data", "rpg", "tags", "item", "fuse", k + ".json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        json.dump({"values": ["minecraft:" + i for i in items]}, io.open(p, "w", encoding="utf-8"), indent=1)
    # 主件是哪一类 → rpg:forge fu.cls
    cls = ["# 主手是哪一类（as 玩家）", 'data modify storage rpg:forge fu.cls set value ""']
    for k in CLASSES:
        cls.append('execute if items entity @s weapon.mainhand #rpg:fuse/%s[minecraft:custom_data~{rpg_eq:{}}] run data modify storage rpg:forge fu.cls set value "%s"' % (k, k))
    fn("cls", cls)
    # 扫背包：同类、带 rpg_eq、不是主手那一格、品质不低于主件低一档 → fu.c 列表（格号）
    scan = ["# 扫祭品（as 玩家；#g 主件档）", "data modify storage rpg:forge fu.c set value []",
            "execute store result score #sel %s run data get entity @s SelectedItemSlot" % O]
    for n in range(36):
        scan.append("$execute unless score #sel %s matches %d if items entity @s container.%d #rpg:fuse/$(cls)[minecraft:custom_data~{rpg_eq:{},rpg_forged:1b}] run function %s/cand {n:%d}" % (O, n, n, F, n))
    fn("scan", scan)
    fn("cand", ["$execute store result score #cq %s run data get entity @s Inventory[{Slot:$(n)b}].components.\"minecraft:custom_data\".rpg_eq.q" % O] +
       grade_of("#cq", "#cg") + ["scoreboard players operation #lo %s = #g %s" % (O, O), "scoreboard players remove #lo %s 1" % O,
                                 "execute if score #cg %s < #lo %s run return 0" % (O, O),
                                 "$data modify storage rpg:forge fu.c append value $(n)"])
    pre = ["# 主手的档与星（as 玩家）",
           "execute store result score #q %s run data get entity @s SelectedItem.components.\"minecraft:custom_data\".rpg_eq.q" % O,
           "execute store result score #st %s run data get entity @s SelectedItem.components.\"minecraft:custom_data\".rpg_eq.star" % O] + grade_of("#q", "#g") + [
           "function %s/cls" % F,
           "execute unless data storage rpg:forge fu{cls:\"\"} run function %s/scan with storage rpg:forge fu" % F,
           "execute store result score #nc %s run data get storage rpg:forge fu.c" % O,
           "execute store result score #ns %s run clear @s %s 0" % (O, SOUL),
           "scoreboard players set #need %s 0" % O] + [
           "execute if score #g %s matches %d run scoreboard players set #need %s %d" % (O, g, O, c) for g, c in enumerate(COST)]
    fn("pre", pre)
    # 页面
    view = ["# 工作台「熔铸」页（as/at 玩家）", "function %s/pre" % F,
            "execute store result storage rpg:forge fu.nc int 1 run scoreboard players get #nc %s" % O,
            "execute store result storage rpg:forge fu.ns int 1 run scoreboard players get #ns %s" % O,
            "execute store result storage rpg:forge fu.need int 1 run scoreboard players get #need %s" % O,
            "execute store result storage rpg:forge fu.st int 1 run scoreboard players get #st %s" % O,
            'data modify storage rpg:forge fu.now set value "主手没有可熔铸的装备"',
            'data modify storage rpg:forge fu.after set value "—"']
    for g, (n, _lo, _hi) in enumerate(GRADES):
        nxt = GRADES[g + 1][0] if g < 3 else "完美 + 1 颗淬炼星"
        view.append('execute unless data storage rpg:forge fu{cls:""} if score #g %s matches %d run data modify storage rpg:forge fu merge value {now:"%s",after:"%s"}' % (O, g, n, nxt))
    view.append('execute if score #g %s matches 3 if score #st %s matches 5.. run data modify storage rpg:forge fu.after set value "已经五颗星，不能再熔"' % (O, O))
    view.append("function %s/view_m with storage rpg:forge fu" % F)
    fn("open", view)
    import add_bench as BN
    body = [BN.bar(87),
            BN.card("rpg:town/tab_fuse", "熔铸", ["主手拿主件；背包里两把同类祭品（品质不低于主件低一档）", "主件　$(now)　→　$(after)", "身上可当祭品的　$(nc) 把　　残魂　$(ns) / $(need)"], C_FORGE),
            BN.card("rpg:town/tab_salvage", "拆解", ["拆掉主手的装备：返还一半主材、1 枚残魂", "符文、符石、源原样退回"], C_FORGE),
            {"type": "minecraft:plain_message", "width": 320, "contents": T("熔铸：主件的等级、源、符文、符石、镀金、名字都留下，两把祭品各自经验的一半加给主件；祭品身上的符文、符石、源会熔掉，想留就先拆。完美再熔加淬炼星（每颗 +2%，最多 5 颗）。升档熔铸：完美主件 + 两把同类同档的完美祭品 + 下一档主材的一半（钻石 ×2；勇者升史诗再加下界合金锭 ×1），熔成上一档，品质回到精良。罪器、图纸武器、传说武器只能当主件。", ui.MUTED)}]
    fn("view_m", ["$dialog show @s " + BN.dump(BN.dialog(BN.title("熔铸", "Fuse"), body, [("熔铸", GOLD, 261), ("升档熔铸", GOLD, 264), ("拆解", ui.WARN, 262), ("‹ 总台", NAME, 86)]))])
    # 熔铸
    do = ["# 熔铸（as/at 玩家）", "function %s/pre" % F,
          "execute if data storage rpg:forge fu{cls:\"\"} run return run " + say("主手要拿着魂火冶炼出来的装备", ui.WARN),
          "execute if score #g %s matches 3 if score #st %s matches 5.. run return run " % (O, O) + say("已经五颗淬炼星了", ui.WARN),
          "execute if score #nc %s matches ..1 run return run " % O + say("背包里同类的祭品不够两把（品质不低于主件低一档）", ui.WARN),
          "execute if score #ns %s < #need %s run return run " % (O, O) + say("残魂不够", ui.WARN),
          "scoreboard players set #xa %s 0" % O,
          "function %s/eat with storage rpg:forge fu" % F,
          "data remove storage rpg:forge fu.c[0]",
          "function %s/eat with storage rpg:forge fu" % F,
          "scoreboard players operation #k %s = #need %s" % (O, O),
          "function %s/pay" % F,
          "function rpg:forge/wb/new", "function rpg:forge/wb/load_main",
          "execute if score #g %s matches 0 store result entity %s %s.q int 1 run random value -5..5" % (O, WS, EQ),
          "execute if score #g %s matches 1 store result entity %s %s.q int 1 run random value 6..10" % (O, WS, EQ),
          "execute if score #g %s matches 2 store result entity %s %s.q int 1 run random value 11..15" % (O, WS, EQ),
          "execute if score #g %s matches 3 run scoreboard players add #st %s 1" % (O, O),
          "execute if score #g %s matches 3 store result entity %s %s.star int 1 run scoreboard players get #st %s" % (O, WS, EQ, O),
          "function rpg:forge/xp/add",
          "function rpg:forge/render",
          "function rpg:forge/wb/save_main", "function rpg:forge/wb/close",
          "scoreboard players add @s rpg_tl_fu 1",
          "particle minecraft:flame ~ ~1 ~ 0.3 0.4 0.3 0.06 30", "particle minecraft:lava ~ ~1 ~ 0.2 0.2 0.2 0 8",
          "summon minecraft:item_display ~ ~1.2 ~ {Tags:[\"rpg.fu.fx\"],billboard:\"center\",item:{id:\"minecraft:paper\",count:1,components:{\"minecraft:item_model\":\"rpg:town/fx_fuse_spark\"}},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.5f,1.5f,1.5f]}}",
          "schedule function %s/fx_clear 12t" % F,
          "playsound minecraft:block.anvil.use player @a[distance=..16] ~ ~ ~ 0.8 0.8",
          "playsound minecraft:block.trial_spawner.eject_item block @a[distance=..16] ~ ~ ~ 1 0.9",
          "execute if score #g %s matches ..2 run " % O + say("熔铸完成：品质升了一档", GOLD),
          "execute if score #g %s matches 3 run " % O + say("熔铸完成：加了一颗淬炼星", GOLD)]
    fn("do_fuse", do)
    fn("fx_clear", ["kill @e[type=minecraft:item_display,tag=rpg.fu.fx]"])
    fn("eat", ["# 吃掉一把祭品（宏：fu.c[0] 是格号）：经验的一半记进 #xa",
               "$execute store result score #cx %s run data get entity @s Inventory[{Slot:$(c0)b}].components.\"minecraft:custom_data\".rpg_eq.xp" % O,
               "scoreboard players operation #cx %s /= #2 %s" % (O, O), "scoreboard players operation #xa %s += #cx %s" % (O, O),
               "$item replace entity @s container.$(c0) with minecraft:air"])
    fn("pay", ["execute if score #k %s matches 1.. run clear @s %s 1" % (O, SOUL), "scoreboard players remove #k %s 1" % O,
               "execute if score #k %s matches 1.. run function %s/pay" % (O, F)])
    # 宏要 c0：把 c[0] 抄出来
    s = "\n".join(do)
    s = s.replace("function %s/eat with storage rpg:forge fu" % F, "data modify storage rpg:forge fu.c0 set from storage rpg:forge fu.c[0]\nfunction %s/eat with storage rpg:forge fu" % F)
    write("forge/fuse/do_fuse", s + "\n")
    # 拆解
    sal = ["# 拆解（as/at 玩家）",
           "execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{}}] run return run " + say("主手要拿着魂火冶炼出来的装备", ui.WARN),
           "data modify storage rpg:forge sv set from entity @s SelectedItem.components.\"minecraft:custom_data\".rpg_eq"]
    for r in RUNES:
        sal.append('execute if data storage rpg:forge sv{rune:"%s"} run loot give @s loot rpg:forge/item/rune_%s' % (r, r))
    for r in STONES:
        sal.append('execute if data storage rpg:forge sv{stone:"%s"} run loot give @s loot rpg:forge/item/stone_%s' % (r, r))
    for r in SOURCES:
        sal.append('execute if data storage rpg:forge sv{src:"%s"} run loot give @s loot rpg:forge/item/source_%s' % (r, r))
    sal += ["execute if items entity @s weapon.mainhand #minecraft:diamond_tool_materials run give @s minecraft:diamond 2",
            "execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{}}] unless items entity @s weapon.mainhand #rpg:fuse/rich run give @s minecraft:iron_ingot 3",
            "execute if items entity @s weapon.mainhand #rpg:fuse/rich run give @s minecraft:diamond 2",
            "loot give @s loot rpg:forge/item/soul",
            "item replace entity @s weapon.mainhand with minecraft:air",
            "scoreboard players add @s rpg_tl_fu 1",
            "particle minecraft:smoke ~ ~1 ~ 0.3 0.3 0.3 0.02 20", "playsound minecraft:block.grindstone.use player @a[distance=..16] ~ ~ ~ 1 0.9",
            say("拆解完成：材料与镶嵌的东西都退回来了", GOLD)]
    sal = [l for l in sal if "diamond_tool_materials" not in l]
    fn("do_salvage", sal)
    for t, pre in (("t_brave", "diamond"), ("t_epic", "netherite")):
        json.dump({"values": ["minecraft:" + i for k, (zh, items) in CLASSES.items() for i in items if i.startswith(pre)]},
                  io.open(os.path.join(DP, "data", "rpg", "tags", "item", "fuse", t + ".json"), "w", encoding="utf-8"), indent=1)
    rich = [i for k, (zh, items) in CLASSES.items() for i in items if i.startswith(("diamond", "netherite"))]
    json.dump({"values": ["minecraft:" + i for i in rich]}, io.open(os.path.join(DP, "data", "rpg", "tags", "item", "fuse", "rich.json"), "w", encoding="utf-8"), indent=1)
    fn("confirm_salvage", ["execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{}}] run return run " + say("主手要拿着魂火冶炼出来的装备", ui.WARN),
                           "$dialog show @s " + BN.dump(BN.dialog(BN.title("拆解", "Salvage"), [BN.bar(87), {"type": "minecraft:plain_message", "width": 300, "contents": T("真的要拆掉主手的装备吗？拆了就没有了。", ui.WARN)}],
                                                                  [("确认拆解", ui.WARN, 263), ("‹ 熔铸", NAME, 87)]))])
    p = os.path.join(FUNC, "forge", "fuse", "confirm_salvage.mcfunction")
    s = io.open(p, encoding="utf-8").read().replace("$dialog", "dialog")
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    up = ["# 升档熔铸（as/at 玩家）", "function %s/pre" % F,
          "execute if data storage rpg:forge fu{cls:\"\"} run return run " + say("主手要拿着魂火冶炼出来的装备", ui.WARN),
          "execute unless score #g %s matches 3 run return run " % O + say("升档要主件已经是完美品质", ui.WARN)]
    up += ["execute if items entity @s weapon.mainhand #rpg:fuse/%s run data modify storage rpg:forge fu.cls set value \"%s\"" % (k, k) for k in CLASSES]
    up += ["function %s/up_tier with storage rpg:forge fu" % F,
           "execute if score #tier %s matches 2.. run return run " % O + say("史诗已经是最高一档", ui.WARN),
           "data modify storage rpg:forge fu.c set value []",
           "execute store result score #sel %s run data get entity @s SelectedItemSlot" % O,
           "function %s/up_scan with storage rpg:forge fu" % F,
           "execute store result score #nc %s run data get storage rpg:forge fu.c" % O,
           "execute if score #nc %s matches ..1 run return run " % O + say("要两把同类、同档、完美品质的祭品", ui.WARN)]
    for t, cost in UP_COST.items():
        for item, n in cost:
            up.append("execute if score #tier %s matches %d store result score #m %s run clear @s minecraft:%s[!minecraft:custom_data] 0" % (O, t, O, item))
            up.append("execute if score #tier %s matches %d if score #m %s matches ..%d run return run " % (O, t, O, n - 1) + say("下一档的主材不够：%s ×%d" % (S.TIER_MAT_NAME[item], n), ui.WARN))
    for t, cost in UP_COST.items():
        for item, n in cost:
            up.append("execute if score #tier %s matches %d run clear @s minecraft:%s[!minecraft:custom_data] %d" % (O, t, item, n))
    up += ["scoreboard players set #xa %s 0" % O,
           "data modify storage rpg:forge fu.c0 set from storage rpg:forge fu.c[0]", "function %s/eat with storage rpg:forge fu" % F,
           "data remove storage rpg:forge fu.c[0]",
           "data modify storage rpg:forge fu.c0 set from storage rpg:forge fu.c[0]", "function %s/eat with storage rpg:forge fu" % F,
           "data modify storage rpg:forge old set from entity @s SelectedItem.components.\"minecraft:custom_data\".rpg_eq",
           "function rpg:forge/wb/new",
           "execute store result score #r %s run random value 0..7" % O,
           "execute store result storage rpg:forge nm.r int 1 run scoreboard players get #r %s" % O,
           "function rpg:forge/smelt/prefix with storage rpg:forge nm"]
    for t in (0, 1):
        for k in CLASSES:
            up.append('execute if score #tier %s matches %d if data storage rpg:forge fu{cls:"%s"} run function rpg:forge/smelt/m/%s_%s with storage rpg:forge nm' % (O, t, k, k, TIERS[t + 1]))
    up += ["execute store result score #mlv %s run data get storage rpg:forge old.lv" % O, "scoreboard players set #mgild %s 0" % O,
           "execute store result score #q0 %s run random value 6..10" % O,
           "execute as %s run function rpg:forge/init" % WS]
    for f in ("xp", "src", "stone", "runes"):
        up.append("execute if data storage rpg:forge old.%s run data modify entity %s %s.%s set from storage rpg:forge old.%s" % (f, WS, EQ, f, f))
    up += ["function rpg:forge/xp/add", "function rpg:forge/render",
           "item replace entity @s weapon.mainhand from entity %s contents" % WS, "function rpg:forge/wb/close",
           "scoreboard players add @s rpg_tl_fu 1",
           "particle minecraft:flame ~ ~1 ~ 0.4 0.5 0.4 0.08 50", "particle minecraft:end_rod ~ ~1.2 ~ 0.3 0.4 0.3 0.05 20",
           "playsound minecraft:block.anvil.use player @a[distance=..16] ~ ~ ~ 0.8 0.6",
           "playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.6 1.2",
           say("升档熔铸完成：装备上了一档，品质回到精良", GOLD)]
    fn("do_up", up)
    ut = ["$execute store result score #tier %s run function %s/tier_main" % (O, F)]
    fn("up_tier", ["scoreboard players set #tier %s 0" % O] + [l.replace("items %s" % "MAIN", "items entity @s weapon.mainhand") for l in tier_lines("MAIN", "#tier")] +
       ["execute if score #tier %s matches 0 run function %s/tier_ench {slot:\"SelectedItem\"}" % (O, F)])
    fn("tier_ench", ["# 重锤、弓弩：看附魔（宏 slot：SelectedItem 或 Inventory[{Slot:Nb}]）",
                     "scoreboard players set #e1 %s 0" % O, "scoreboard players set #e2 %s 0" % O,
                     '$execute store result score #e1 %s run data get entity @s $(slot).components."minecraft:enchantments"."minecraft:unbreaking"' % O,
                     '$execute store result score #e2 %s run data get entity @s $(slot).components."minecraft:enchantments"."minecraft:power"' % O,
                     '$execute if score #e2 %s matches 0 store result score #e2 %s run data get entity @s $(slot).components."minecraft:enchantments"."minecraft:quick_charge"' % (O, O),
                     "execute if items entity @s weapon.mainhand minecraft:mace run scoreboard players operation #e2 %s = #e1 %s" % (O, O),
                     "execute if items entity @s weapon.mainhand minecraft:mace run scoreboard players add #e2 %s 1" % O,
                     "execute if items entity @s weapon.mainhand minecraft:mace run scoreboard players add #e1 %s 1" % O,
                     "scoreboard players operation #e1 %s < #e2 %s" % (O, O),
                     "scoreboard players remove #e1 %s 1" % O,
                     "execute if score #e1 %s matches 1.. run scoreboard players operation #tier %s = #e1 %s" % (O, O, O),
                     "execute if score #tier %s matches 3.. run scoreboard players set #tier %s 2" % (O, O)])
    us = ["# 升档的祭品：同类、带 rpg_forged、完美、同档（#tier）"]
    for n in range(36):
        us.append("$execute unless score #sel %s matches %d if items entity @s container.%d #rpg:fuse/$(cls)[minecraft:custom_data~{rpg_eq:{},rpg_forged:1b}] run function %s/up_cand {n:%d}" % (O, n, n, F, n))
    fn("up_scan", us)
    fn("up_cand", ["$execute store result score #cq %s run data get entity @s Inventory[{Slot:$(n)b}].components.\"minecraft:custom_data\".rpg_eq.q" % O,
                   "execute if score #cq %s matches ..10 run return 0" % O,
                   "scoreboard players set #ct %s 0" % O,
                   "$execute if items entity @s container.$(n) #rpg:fuse/t_brave run scoreboard players set #ct %s 1" % O,
                   "$execute if items entity @s container.$(n) #rpg:fuse/t_epic run scoreboard players set #ct %s 2" % O,
                   "scoreboard players operation #keep %s = #tier %s" % (O, O),
                   "$execute if score #ct %s matches 0 run function %s/tier_ench_slot {n:$(n)}" % (O, F),
                   "execute unless score #ct %s = #keep %s run return 0" % (O, O),
                   "$data modify storage rpg:forge fu.c append value $(n)"])
    fn("tier_ench_slot", ["# 祭品是重锤或弓弩：同样看附魔（借 #tier 算，再还原）",
                          "scoreboard players set #tier %s 0" % O,
                          "$function %s/tier_ench_inv {n:$(n)}" % F,
                          "scoreboard players operation #ct %s = #tier %s" % (O, O), "scoreboard players operation #tier %s = #keep %s" % (O, O)])
    fn("tier_ench_inv", ["$function %s/tier_ench {slot:\"Inventory[{Slot:$(n)b}]\"}" % F])
    fn("do", ["execute if score #do %s matches 264 run return run function %s/do_up" % (O, F),
              "execute if score #do %s matches 261 run return run function %s/do_fuse" % (O, F),
              "execute if score #do %s matches 262 run return run function %s/confirm_salvage" % (O, F),
              "execute if score #do %s matches 263 run return run function %s/do_salvage" % (O, F)])
    s = read("forge/smelt/do")
    if F + "/do" not in s:
        a = "execute if score #do rpg_fg matches 200..259"
        s = s.replace(a, "execute if score #do rpg_fg matches 260..269 run return run function %s/do\n" % F + a, 1)
        write("forge/smelt/do", s)
    s = read("bench/do")
    if F + "/open" not in s:
        write("bench/do", s.rstrip("\n") + "\nexecute if score #do rpg_fg matches 87 run return run function %s/open\n" % F)
    # 淬炼星：渲染时每颗 +2%，品质名后加 ★
    s = read("forge/render")
    if "e.star" not in s:
        a = "execute store result score #q rpg_fg run data get storage rpg:forge e.q\n"
        assert a in s
        s = s.replace(a, a + "execute store result score #st rpg_fg run data get storage rpg:forge e.star\n", 1)
        b = "scoreboard players operation #f rpg_fg = #q rpg_fg\n"
        assert b in s
        s = s.replace(b, b + "scoreboard players operation #f rpg_fg += #st rpg_fg\nscoreboard players operation #f rpg_fg += #st rpg_fg\n", 1)
        c = 'execute if score #q rpg_fg matches 11..15 run data modify storage rpg:forge ui merge value {qn:"完美",qc:"#FFAA00"}\n'
        assert c in s
        stars = "".join('execute if score #st rpg_fg matches %d run data modify storage rpg:forge ui.qn set value "完美%s"\n' % (n, "★" * n) for n in range(1, 6))
        s = s.replace(c, c + stars, 1)
        write("forge/render", s)


def main():
    build()
    print("fusion: %d 个函数" % COUNT[0])


if __name__ == "__main__":
    main()
