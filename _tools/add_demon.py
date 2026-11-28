# -*- coding: utf-8 -*-
"""恶魔阵营（《开局参与感》策划书第四节）：无知者、边缘者做一场小召唤仪式，投入恶魔阵营，和教廷为敌。

- 七大罪之仆生来就在这边（rpg_ident 4 一进故乡就算）；神职者、圣子、圣灵、弥赛亚不能入伙。
- 找到门：女巫那场听完她讲，或替神父找回失踪的孩子（rpg.tl.camp），林中营地就向你敞开。
- 营地里有女巫（黑蜡烛 3 枚货币）、兜帽人（秘密委托）。
- 仪式：夜里，营地的祭坛（拿着黑蜡烛右键），备齐罪印碎片 ×3、黑蜡烛 ×1，再付一半的血。
  召来七十二柱的一位低阶罪仆，递出投诚契约；确认后魔化 +30，名字前多一枚紫色魔印（队伍 rpg_dm，同阵营不伤友军）。
- 入伙以后：圣水会烫伤你；在镇上的圣卫面前拿着罪器、罪印就会「暴露」，五分钟内上告示板的通缉令。
  粮仓那场多一个「悄悄放走」，女巫那场奖励翻倍（add_town_events）。

python add_demon.py ../rpg
"""
import io
import json
import os
import sys

import rpg_ui_style as ui
import town_text as TT
from display_mob import hook_tag

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data", "rpg", "function")
D = "rpg:town/demon"
O = "rpg_dm"
TW = "rpg_tw"
COUNT = [0]
CUR = 'minecraft:raw_gold[minecraft:custom_data~{currency_tag:1b}]'
SHARD = 'minecraft:paper[minecraft:custom_data~{rpg_mat:"sin_shard"}]'
CANDLE = 'minecraft:candle[minecraft:custom_data~{rpg_black_candle:1b}]'
PURPLE = "#A276BE"
BODY = ui.BROADCAST_BODY
NAME = ui.BROADCAST_NAME
SIN_HELD = ('*[minecraft:custom_data~{devil_tag:1b}]',)          # 罪器（rpg:inquest/give/pact_weapon*、罪遗武器）都带 devil_tag


def J(c):
    return json.dumps(c, ensure_ascii=False, separators=(",", ":"))


def T(text, colour=BODY, bold=False):
    return {"text": text, "color": colour, "bold": bold, "italic": False}


def fn(name, lines):
    path = os.path.join(FUNC, "town", "demon", name + ".mcfunction")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    COUNT[0] += 1


def wj(rel, doc):
    path = os.path.join(DP, "data", rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)


def tag_values(name, values):
    path = os.path.join(DP, "data", "rpg", "tags", "function", name + ".json")
    doc = json.load(io.open(path, encoding="utf-8")) if os.path.exists(path) else {"values": []}
    for v in values:
        if v not in doc["values"]:
            doc["values"].append(v)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=1)


def note(text, colour=BODY, who="@s"):
    return "tellraw %s %s" % (who, J(["", T("〖林中营地〗", PURPLE, True), T(ui.GAP + text, colour)]))


def dlg(title, gloss, body, actions, trig="rpg_dm_do", columns=2, esc=True, prefix="林中营地"):
    doc = {"type": "minecraft:multi_action", "title": ["", T(prefix + " · ", ui.BROADCAST_VOID, True), T(title, NAME, True), T(" " + ui.fraktur(gloss), ui.BROADCAST_GLOSS)],
           "body": [{"type": "minecraft:plain_message", "width": 300, "contents": ["", *body]}],
           "actions": [{"label": T(l, c, True), "action": {"type": "minecraft:run_command", "command": "/trigger %s set %d" % (trig, v)}} for l, c, v in actions],
           "columns": columns, "can_close_with_escape": esc, "pause": False, "after_action": "close"}
    if esc:
        doc["exit_action"] = {"label": T("离开", BODY)}
    return "dialog show @s " + J(ui.darken(doc))


def candle_item():
    return ('minecraft:candle[minecraft:custom_name=%s,minecraft:lore=[%s,%s,%s,%s],minecraft:custom_data={rpg_black_candle:1b},minecraft:item_model="rpg:town/black_candle"]'
            % (J(["", T("[恶魔]", PURPLE, True), T("黑蜡烛", "#FFFFFF")]), J(T("+------------------+", "#FFFFFF")),
               J(T("逆着画圈，点在林中祭坛上", "gray")), J(T("召来七十二柱里的一位低阶罪仆", "gray")), J(T("+------------------+", "#FFFFFF"))))


def build():
    fn("load", ["scoreboard objectives add %s dummy" % O, "scoreboard objectives add rpg_dm_do trigger", "scoreboard objectives add rpg_dm_rep dummy",
                "scoreboard objectives add rpg_dm_exp dummy",
                "team add rpg_dm", "team modify rpg_dm friendlyFire false", "team modify rpg_dm color dark_purple",
                "team modify rpg_dm prefix " + J(["", T("魔印 ", PURPLE, True)]),
                "schedule function %s/sec 20t" % D])
    hook_tag(DP, "load", D + "/load", False)
    fn("sec", ["schedule function %s/sec 20t" % D,
               "execute as @a[scores={rpg_dm_do=1..}] at @s run function %s/do" % D,
               "execute as @a[scores={rpg_ident=4},tag=!rpg.dm] run function %s/born" % D,
               "execute as @a[tag=rpg.dm] at @s run function %s/each" % D])
    fn("born", ["# 七大罪之仆：生来就在这边", "tag @s add rpg.dm", "team join rpg_dm @s"])
    fn("each", ["# 每秒（as/at 恶魔阵营的玩家）：圣水烫人；在圣卫面前拿罪器、罪印就暴露",
                "execute if entity @e[type=minecraft:area_effect_cloud,tag=rpg.holy_water,distance=..4] run damage @s 2 minecraft:magic",
                "execute if score @s rpg_dm_exp matches 1.. run scoreboard players remove @s rpg_dm_exp 1",
                "execute if score @s rpg_dm_exp matches 1 run " + note("圣卫不再追查你了。通缉令撤下了。", NAME),
                "execute if score @s rpg_dm_exp matches ..0 if entity @e[tag=rpg.tw.guard,distance=..12] run function %s/check_held" % D])
    held = ["execute if items entity @s weapon.mainhand %s run return run function %s/exposed" % (s, D) for s in SIN_HELD]
    fn("check_held", held)
    fn("exposed", ["scoreboard players set @s rpg_dm_exp 300",
                   "execute as @e[tag=rpg.tw.guard,distance=..16] at @s run particle minecraft:angry_villager ~ ~2.6 ~ 0.3 0.2 0.3 0 3",
                   "playsound minecraft:entity.vindicator.celebrate hostile @a[distance=..24] ~ ~ ~ 1 0.7",
                   "tellraw @a[distance=..64] " + J(["", T("〖圣卫〗", ui.BROADCAST_HOLY, True), T(ui.GAP + "罪器！拿下他——", BODY)]),
                   note("你在圣卫面前亮了罪器。五分钟内，你的名字挂在告示板的通缉令上。", ui.WARN)])
    fn("wanted_list", ["tellraw @s " + J(["", T("〖通缉令〗", ui.BROADCAST_HOLY, True), T(ui.GAP + "教廷悬赏捉拿以下暴露的恶魔信徒：", BODY)]),
                       "execute unless entity @a[scores={rpg_dm_exp=1..}] run tellraw @s " + J(["", T("　（眼下没有）", ui.MUTED)]),
                       "execute as @a[scores={rpg_dm_exp=1..}] run tellraw @a[tag=rpg.dm.reader] " + J(["", T("　", BODY), {"selector": "@s", "color": PURPLE}, T("　还剩 ", BODY), {"score": {"name": "@s", "objective": "rpg_dm_exp"}, "color": NAME}, T(" 秒", BODY)])])
    p = os.path.join(FUNC, "town", "demon", "wanted_list.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    io.open(p, "w", encoding="utf-8", newline="\n").write("tag @s add rpg.dm.reader\n" + s + "tag @s remove rpg.dm.reader\n")
    # 营地：女巫、兜帽人、祭坛（镇建好时放）
    fn("camp", ["# 林中营地（as 营地锚点，at 它）",
                'summon minecraft:villager ~2 ~ ~ {Tags:["rpg.tnpc","rpg.tnpc.witch","rpg.dm.camp","rpg.tl.new"],NoAI:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,CustomName:%s,VillagerData:{type:"minecraft:swamp",profession:"minecraft:none",level:1}}' % J(T("女巫", "#B48AD8", True)),
                'summon minecraft:villager ~-2 ~ ~1 {Tags:["rpg.tnpc","rpg.tnpc.hood","rpg.dm.camp","rpg.tl.new"],NoAI:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,CustomName:%s,VillagerData:{type:"minecraft:swamp",profession:"minecraft:none",level:1}}' % J(T("兜帽人", ui.RITUAL, True)),
                'summon minecraft:interaction ~ ~ ~-4 {Tags:["rpg.tnpc","rpg.tnpc.altar","rpg.tl.new"],width:1.6f,height:1.2f,response:1b}',
                'summon minecraft:text_display ~ ~1.6 ~-4 {Tags:["rpg.tnpc.plate"],billboard:"center",text:%s}' % J(["", T("林中祭坛", PURPLE, True), T("\n" + ui.fraktur("Altar"), ui.BROADCAST_GLOSS)]),
                "execute positioned ~-1 ~ ~-4 run function rpg:town/prop {n:\"candles_a\"}", "execute positioned ~1 ~ ~-4 run function rpg:town/prop {n:\"candles_b\"}",
                "execute positioned ~3 ~ ~2 run function rpg:town/prop {n:\"cauldron\"}",
                "scoreboard players operation @e[tag=rpg.tl.new,distance=..6] %s_id = #built %s" % (TW, TW),
                "execute as @e[type=minecraft:villager,tag=rpg.tl.new,distance=..6] store result entity @s Rotation[0] float 1 run random value -180..179",
                "execute as @e[type=minecraft:villager,tag=rpg.tl.new,distance=..6] at @s run function #rpg:town_dress",
                "tag @e[tag=rpg.tl.new,distance=..6] remove rpg.tl.new"])
    fn("camp_all", ["execute as @e[type=minecraft:marker,tag=rpg.tw.at.camp] if score @s %s_id = #built %s at @s run function %s/camp" % (TW, TW, D)])
    tag_values("camp_built", [D + "/camp_all"])
    q = os.path.join(DP, "data", "rpg", "tags", "function", "town_built.json")      # 旧版挂在 town_built 上
    if os.path.exists(q):
        doc = json.load(io.open(q, encoding="utf-8"))
        doc["values"] = [v for v in doc["values"] if v != D + "/camp_all"]
        with io.open(q, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(doc, fh, indent=1)
    # 右键路由：营地里的兜帽人（没有副本时）、祭坛
    p = os.path.join(FUNC, "town", "life", "whoami.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    if "rpg.tnpc.altar" not in s:
        s += "execute if entity @s[tag=rpg.tnpc.altar] run scoreboard players set #role rpg_tl 10\n"
        io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    p = os.path.join(FUNC, "town", "life", "talk.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    if "demon/hood_talk" not in s:
        s += ("execute if score #role rpg_tl matches 8 run return run function %s/hood_talk\n"
              "execute if score #role rpg_tl matches 10 run return run function %s/altar\n") % (D, D)
        io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    gate = "execute unless entity @s[tag=rpg.tl.camp] unless entity @s[tag=rpg.dm] run return run " + note("营地里的人看了你一眼，没有说话。（先在镇上听说过这里）", ui.MUTED)
    fn("witch_talk", [gate] + TT.say("WI11", "@s") + ["scoreboard players enable @s rpg_dm_do",
                      dlg("女巫", "The Witch", [T("「坐吧，火是暖的。」\n", NAME), T("黑蜡烛三枚货币一支。祭坛在营地后面。", BODY)],
                          [("买黑蜡烛（3 货币）", PURPLE, 1), ("祭坛的事", NAME, 2)])])
    fn("hood_talk", [gate] + TT.say("EW13", "@s") + ["execute if entity @s[tag=rpg.dm] run function %s/secret" % D])
    fn("secret", TT.say("EW14", "@s") + [
        note("秘密委托：今夜去任意一座镇，在教堂门口站五秒，吹灭他们的蜡烛。", PURPLE),
        "tag @s add rpg.dm.job"])
    fn("do", ["scoreboard players operation #do %s = @s rpg_dm_do" % O, "scoreboard players set @s rpg_dm_do 0", "scoreboard players enable @s rpg_dm_do",
              "execute if score #do %s matches 1 run return run function %s/buy" % (O, D),
              "execute if score #do %s matches 2 run return run function %s/altar_info" % (O, D),
              "execute if score #do %s matches 11 run return run function %s/sign" % (O, D),
              "execute if score #do %s matches 12 run return run function %s/refuse" % (O, D)])
    fn("buy", ["execute store result score #m %s run clear @s %s 0" % (O, CUR),
               "execute if score #m %s matches ..2 run return run " % O + note("三枚货币一支。", ui.WARN),
               "clear @s %s 3" % CUR, "give @s " + candle_item(), note("黑蜡烛到手。", PURPLE)])
    fn("altar_info", TT.say("WI12", "@s") + [note("备齐罪印碎片 ×3、黑蜡烛 ×1，夜里拿着黑蜡烛右键祭坛。仪式要付一半的血。", PURPLE)])
    fn("altar", ["# 右键祭坛（as/at 玩家）",
                 "execute if entity @s[tag=rpg.dm] run return run " + note("你已经是这边的人了。", PURPLE),
                 "execute if score @s rpg_ident matches 3.. unless score @s rpg_ident matches 4 run return run " + note("祭坛对你毫无反应。侍奉神的人不能入伙。", ui.MUTED),
                 "execute unless entity @s[tag=rpg.tl.camp] run return run " + note("你还不知道这座祭坛是做什么的。", ui.MUTED),
                 "execute store result score #tod %s run time query daytime" % O,
                 "execute unless score #tod %s matches 13000..23000 run return run " % O + note("仪式要在夜里做。", ui.WARN),
                 "execute unless items entity @s weapon.mainhand %s run return run " % CANDLE + note("拿着黑蜡烛右键祭坛。", ui.WARN),
                 "execute store result score #s %s run clear @s %s 0" % (O, SHARD),
                 "execute if score #s %s matches ..2 run return run " % O + note("还差罪印碎片（要 3 片，哪一柱的都行）。", ui.WARN),
                 "function %s/rite" % D])
    fn("rite", ["# 反向的仪式：逆着画的圈、黑烛、一半的血 → 罪仆现身，递出契约",
                "item modify entity @s weapon.mainhand {function:\"minecraft:set_count\",count:-1,add:true}",
                "clear @s %s 3" % SHARD,
                "execute store result score #h %s run data get entity @s Health" % O, "scoreboard players operation #h %s /= #2 rpg_tw" % O,
                "execute store result storage rpg:town dm.h int 1 run scoreboard players get #h %s" % O,
                "function %s/bleed with storage rpg:town dm" % D,
                "execute as @e[type=minecraft:interaction,tag=rpg.tnpc.altar,distance=..8,limit=1,sort=nearest] at @s run function %s/circle" % D]
       + TT.say("SV01", "@s") + TT.say("SV02", "@s") + TT.say("SV03", "@s") + TT.say("SV04", "@s") + [
                "scoreboard players enable @s rpg_dm_do",
                dlg("投诚契约", "Pact of Allegiance", [T("立约人投入七十二柱一方，与教廷为敌。\n\n", NAME), T("代价：魔化 +30；名字前多一枚魔印；圣水从此会烫伤你；在圣卫面前亮出罪器就会被通缉。\n", BODY),
                                                       T("回头的路是有的（堕落者凭新约回头），但代价很高。", ui.MUTED)],
                    [("签下", PURPLE, 11), ("不签", NAME, 12)], esc=False, prefix="契约")])
    fn("bleed", ["$damage @s $(h) minecraft:magic"])
    fn("circle", ["particle minecraft:dust{color:[0.45,0.2,0.55],scale:1.6} ~ ~0.1 ~ 1.6 0.05 1.6 0 80",
                  "particle minecraft:soul_fire_flame ~ ~0.3 ~ 1.2 0.1 1.2 0 30",
                  "summon minecraft:item_display ~ ~0.05 ~ {Tags:[\"rpg.dm.fx\"],item:{id:\"minecraft:paper\",count:1,components:{\"minecraft:item_model\":\"rpg:town/fx_rev_circle\"}},transformation:{translation:[0f,0f,0f],left_rotation:[-0.7071f,0f,0f,0.7071f],right_rotation:[0f,0f,0f,1f],scale:[4f,4f,4f]}}",
                  "playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..24] ~ ~ ~ 1 0.6",
                  "schedule function %s/fx_clear 200t" % D])
    fn("fx_clear", ["kill @e[type=minecraft:item_display,tag=rpg.dm.fx]"])
    fn("sign", ["execute if entity @s[tag=rpg.dm] run return 0"] + TT.say("SV05", "@s") + [
                "tag @s add rpg.dm", "team join rpg_dm @s", "scoreboard players add @s rpg_taint 30", "scoreboard players add @s rpg_dm_rep 10",
                "title @s times 10 60 20", "title @s title " + J(["", T("投诚", PURPLE, True)]),
                "title @s subtitle " + J(["", T("你的名字前多了一枚魔印", BODY)]),
                "playsound minecraft:entity.wither.spawn hostile @s ~ ~ ~ 0.5 1.4"])
    fn("refuse", TT.say("SV06", "@s"))
    # 秘密委托：夜里在任意一座镇的教堂门口站五秒
    fn("job_tick", ["execute store result score #tod %s run time query daytime" % O,
                    "execute unless score #tod %s matches 13000..23000 run return 0" % O,
                    "execute as @a[tag=rpg.dm.job] at @s if entity @e[type=minecraft:marker,tag=rpg.tw.at.church,distance=..4] run scoreboard players add @s %s 1" % O,
                    "execute as @a[tag=rpg.dm.job,scores={%s=5..}] at @s run function %s/job_done" % (O, D)])
    fn("job_done", ["tag @s remove rpg.dm.job", "scoreboard players set @s %s 0" % O, "scoreboard players add @s rpg_dm_rep 10",
                    "loot give @s loot rpg:world/sin_shard_6", "loot give @s loot rpg:world/currency",
                    "particle minecraft:smoke ~ ~1.5 ~ 0.4 0.3 0.4 0.01 20", note("教堂门口的蜡烛灭了。没有人看见你。", PURPLE)])
    p = os.path.join(FUNC, "town", "demon", "sec.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    io.open(p, "w", encoding="utf-8", newline="\n").write(s + "function %s/job_tick\n" % D)


def main():
    build()
    print("demon: %d 个函数" % COUNT[0])
    # 城镇台词节奏：城镇各模块（life、ev、demon）的函数都写完了，最后统一把连说的台词排成一句一句
    files, n = TT.pace(DP)
    hook_tag(DP, "load", "rpg:town/say/load", False)
    hook_tag(DP, "tick", "rpg:town/say/tick", False)
    print("town dialogue pacing: %d 个函数、%d 句排队" % (files, n))


if __name__ == "__main__":
    main()
