# -*- coding: utf-8 -*-
"""小支线、彩蛋与称号（策划书第六步，用户 2026-11-23/24）。

    python add_quests.py ../rpg

支线（不全程配音；字幕用 Boss 血条、句子短；开头有配乐）：
  1 铁匠的遗嘱   走完新手、原质 ≥ 1 自动接：冶炼一件装备 → 打倒一名精英 → 在魂火边换一次材料 → 自选一张史诗图纸
  2 守墓人       第一次打倒亡灵首领时接：再打倒 3 名亡灵首领 → 墓土 ×3
  3 圣卫的遗言   第一次打倒圣卫时接：打倒 3 名圣卫 → 圣殿铜 ×3、源质「慈悲」
     （策划书原是「迷途的圣卫」护送，要先把圣卫做成友方；先用这一条代替，见交付说明）
  4 玛门的账本   第一次打死寻宝兔时接：打死 3 只寻宝兔 → 玛门罪印碎片 ×4（商人做好后也能从神秘商人接）
  5 星辰拾荒者   第一次完成坠星时接：完成 3 次坠星 → 「无垠星空」传说图纸
  6 空缺者的名字 遇到「空缺者显现」时接：完成一次驱魔裁决 → 源质「理解」、一枚武器核心、阅历 +30
彩蛋（不提示）：大团长、所罗门的门户、所罗门的账簿、白昼流星、摇摆者（被商人记恨在商人那一步）。
称号：名字前的图标（队伍前缀，字体 rpg:world_titles，聊天、头顶、Tab 都显示），在「旅程」页切换。
"""
import io
import json
import os
import sys

import add_world_art as WA
import rpg_ui_style as ui
from display_mob import hook_tag

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data", "rpg", "function")
P = "rpg:quest"
COUNT = 0
TAG_Q = ui.HOLY_DARK

# id: (名, 英文, [(步骤文字, 钩子, 目标)], 奖励命令, 完成字幕)
QUESTS = {
    1: ("铁匠的遗嘱", "The Smith's Will",
        [("在魂火里冶炼一件装备", "smelt", 1), ("打倒一名精英", "elite", 1), ("在魂火边换一次材料", "conv", 1)],
        ["function %s/q1_pick" % P], "老铁匠留下的图纸，现在归你了。"),
    2: ("守墓人", "The Gravekeeper", [("打倒 3 名亡灵首领", "undead_champ", 3)],
        ["loot give @s loot rpg:world/sp/soil"] * 3, "墓地安静下来了。"),
    3: ("圣卫的遗言", "Last Words of the Guard", [("打倒 3 名圣卫", "guard", 3)],
        ["loot give @s loot rpg:world/sp/bronze"] * 3 + ["function rpg:world/kab/line_6"], "他们守着的，原来是这个。"),
    4: ("玛门的账本", "Mammon's Ledger", [("打死 3 只寻宝兔", "rabbit", 3)],
        ["loot give @s loot rpg:world/sin_shard_7"] * 4, "账平了。玛门记住了你的名字。"),
    5: ("星辰拾荒者", "Starscavenger", [("完成 3 次坠星", "star", 3)],
        ["loot give @s loot rpg:world/bp/starry"], "三颗星的残片拼成了一张图纸。"),
    6: ("空缺者的名字", "Name of the Vacant", [("完成一次驱魔裁决", "verdict", 1)],
        ["function rpg:world/kab/line_5", "scoreboard players add @s rpg_ex_xp 30",
         "function %s/q6_core" % P], "叫得出名字，才算理解。"),
    7: ("失乐园", "Paradise Lost", [("过比逊河庭", "court", 1), ("向生命树献一次", "tree", 1), ("打倒基路伯", "cherub", 1)],
        ["loot give @s loot rpg:world/bp_legend_any"], "门还在那里，只是没有人再守着它。"),
}
EPICS = None  # 由 add_world_items.WEAPONS 里的史诗图纸决定
TITLES = {  # key: (名, 来历)
    "gate": ("所罗门的门户", "左手雅斤，右手波阿斯，在高处站了十秒"),
    "ledger": ("所罗门的账簿", "七柱三十五名罪仆都亲手打败过"),
    "waverer": ("摇摆者", "同一天里堕入魔力又回到圣力"),
    "grandmaster": ("大团长的朋友", "让雅克的残影向一只叫「大团长」的狗行礼"),
    "meteor": ("白昼流星", "王冠阶的正午，对着太阳举起无垠星空"),
    "merchant": ("被商人记恨", "用金锄敲了商人三下"),
    "summit": ("登顶者", "打完了失乐园四座河庭的二十层"),
    "sever": ("断影者", "在深渊里斩断了自己的影子"),
    "mirror": ("照见者", "在深渊里接纳了自己的影子"),
}


def fn(name, lines):
    global COUNT
    path = os.path.join(FUNC, "quest", name + ".mcfunction")
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


def subtitle(k, line):
    """字幕：Boss 血条（粉色贴图透明）只剩名字；一句话，配支线名。"""
    name, en, _s, _r, _d = QUESTS[k]
    return ["bossbar set rpg:quest_sub name " + J(["", seg("〔支线%s%s〕 " % (ui.TAG_JOIN, name), TAG_Q, True), seg(line, ui.BROADCAST_NAME)]),
            "bossbar set rpg:quest_sub players @s",
            "scoreboard players set @s rpg_q_st 80",
            "tellraw @s " + J(["", seg("〔支线%s%s〕" % (ui.TAG_JOIN, name), TAG_Q, True), seg(" " + ui.fraktur(en), ui.BROADCAST_GLOSS),
                                seg("  " + line, ui.BROADCAST_BODY)])]


# ============================================================================ 支线
def quests():
    objs = ["rpg_q_st", "rpg_q_mt", "rpg_q_fd", "rpg_q_eg", "rpg_q_em", "rpg_title"] + \
           ["rpg_q%d" % k for k in QUESTS] + ["rpg_qc%d" % k for k in QUESTS]
    hook_tag(DP, "load", P + "/load", False)
    fn("load", ["scoreboard objectives add %s dummy" % o for o in objs] + [
        "scoreboard objectives add rpg_q_do trigger",
        "bossbar add rpg:quest_sub \"\"", "bossbar set rpg:quest_sub color pink"] + titles_load())
    hook_tag(DP, "tick", P + "/tick", True)
    fn("tick", [
        "execute as @a[scores={rpg_q_do=1..}] at @s run function %s/press" % P,
        "scoreboard players remove @a[scores={rpg_q_st=1..}] rpg_q_st 1",
        "execute as @a[scores={rpg_q_st=0}] run function %s/sub_off" % P,
        "scoreboard players remove @a[scores={rpg_q_mt=1..}] rpg_q_mt 1",
        "execute as @a[scores={rpg_q_mt=0}] run function %s/music_off" % P,
        "scoreboard players add #t rpg_q_st 1",
        "execute if score #t rpg_q_st matches 20.. run function %s/sec" % P,
    ])
    fn("sub_off", ["scoreboard players reset @s rpg_q_st", "bossbar set rpg:quest_sub players @a[scores={rpg_q_st=1..}]"])
    fn("music_off", ["scoreboard players reset @s rpg_q_mt", "stopsound @s record rpg:bgm.onboard_flow"])
    fn("sec", ["scoreboard players set #t rpg_q_st 0",
               "scoreboard players enable @a rpg_q_do",
               "execute as @a[scores={rpg_ob=100,rpg_sef=1..}] unless score @s rpg_q1 matches 1.. run function %s/start_1" % P,
               "function %s/egg/sec" % P])
    hooks = {}
    for k, (name, en, steps, reward, done) in QUESTS.items():
        fn("start_%d" % k, ["# 接下支线：%s" % name,
                            "execute if score @s rpg_q%d matches 1.. run return 0" % k,
                            "scoreboard players set @s rpg_q%d 1" % k, "scoreboard players set @s rpg_qc%d 0" % k,
                            "execute at @s run playsound rpg:bgm.onboard_flow record @s ~ ~ ~ 0.6 1",
                            "scoreboard players set @s rpg_q_mt 300"] + subtitle(k, steps[0][0]))
        for i, (text, hook, goal) in enumerate(steps, 1):
            hooks.setdefault(hook, []).append((k, i, goal))
            nxt = (["scoreboard players set @s rpg_q%d %d" % (k, i + 1), "scoreboard players set @s rpg_qc%d 0" % k] +
                   subtitle(k, steps[i][0])) if i < len(steps) else [
                "scoreboard players set @s rpg_q%d 99" % k] + reward + subtitle(k, done) + [
                "playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.7 1"]
            fn("step_%d_%d" % (k, i), ["scoreboard players add @s rpg_qc%d 1" % k,
                                        "execute if score @s rpg_qc%d matches %d.. run function %s/adv_%d_%d" % (k, goal, P, k, i)])
            fn("adv_%d_%d" % (k, i), nxt)
    for hook, lst in hooks.items():
        fn("hook/%s" % hook, ["execute if score @s rpg_q%d matches %d run function %s/step_%d_%d" % (k, i, P, k, i) for k, i, g in lst])
    # 铁匠的遗嘱：自选一张史诗图纸
    import add_world_items as WI
    epics = [w for w in WI.WEAPONS if w[2] == "epic"]
    from forge_ops import dialog, tt, T_HOLY, T_BODY  # 与锻造对话框同一个样式
    body = [tt("老铁匠留下的几张图纸，挑一张。", T_BODY)]
    d = dialog("铁匠的遗嘱", body, [(w[1], ui.tier_colour("epic"), 20 + i) for i, w in enumerate(epics)], exit_label="以后再挑")
    d = d.replace("/trigger rpg_fg_do set", "/trigger rpg_q_do set").replace('"[锻造]"', '"[支线]"')
    fn("q1_pick", ["tag @s add rpg.q1.pick", d])
    press = ["scoreboard players operation #do rpg_q_st = @s rpg_q_do", "scoreboard players set @s rpg_q_do 0",
             "scoreboard players enable @s rpg_q_do",
             "execute if score #do rpg_q_st matches 1 run return run function %s/titles" % P]
    for i, w in enumerate(epics):
        press.append("execute if score #do rpg_q_st matches %d if entity @s[tag=rpg.q1.pick] run loot give @s loot rpg:world/bp/%s" % (20 + i, w[0]))
    for i, t in enumerate(TITLES):
        press.append("execute if score #do rpg_q_st matches %d run function %s/title/wear_%s" % (40 + i, P, t))
    press.append("execute if score #do rpg_q_st matches 20..%d run tag @s remove rpg.q1.pick" % (19 + len(epics)))
    press.append("execute if score #do rpg_q_st matches 49 run function %s/title/off" % P)
    fn("press", press)
    fn("q6_core", ["execute store result score #r rpg_q_st run random value 1..7"] +
       ["execute if score #r rpg_q_st matches %d run function rpg:inquest/give/core%d" % (n, n) for n in range(1, 8)])
    # 钩子接到各系统
    patch("forge/smelt/make.mcfunction", "%s/hook/smelt" % P,
          "execute as @a if score @s rpg_fg_id = #me rpg_fg run function %s/hook/smelt\n" % P)
    for g in ("undead", "arthropod", "explosive", "arcane", "nether", "end", "water"):
        for suf in ("", "_champion"):
            patch("elite/kill/%s%s.mcfunction" % (g, suf), "%s/hook/elite" % P, "function %s/hook/elite\n" % P)
    patch("elite/kill/undead_champion.mcfunction", "%s/start_2" % P,
          "function %s/start_2\nfunction %s/hook/undead_champ\n" % (P, P))
    for r in (61, 62, 63, 64):
        patch("forge/conv/r%d.mcfunction" % r, "%s/hook/conv" % P, "function %s/hook/conv\n" % P, where="loot give @s loot")
    for g in ("hg", "tg", "rg"):
        patch("world/kill_guard_%s.mcfunction" % g, "%s/start_3" % P, "function %s/start_3\nfunction %s/hook/guard\n" % (P, P))
    patch("events/e4/kill.mcfunction", "%s/start_4" % P, "function %s/start_4\nfunction %s/hook/rabbit\n" % (P, P))
    patch("events/e2/reward.mcfunction", "%s/start_5" % P, "function %s/start_5\nfunction %s/hook/star\n" % (P, P))
    patch("events/e5/start.mcfunction", "%s/start_6" % P,
          "execute as @a[distance=..64,scores={rpg_ob=100}] run function %s/start_6\n" % P)
    patch("sephira/rite/verdict.mcfunction", "%s/hook/verdict" % P, "function %s/hook/verdict\n" % P)
    # 旅程页：支线进度（插在「今日悬赏」之前）
    jl = []
    for k, (name, en, steps, reward, done) in QUESTS.items():
        for i, (text, hook, goal) in enumerate(steps, 1):
            jl.append("execute if score @s rpg_q%d matches %d run data modify storage rpg:panel ui.body append value %s"
                      % (k, i, J({"text": "", "extra": [seg(name, ui.BROADCAST_NAME, True), seg("　" + text + "\n", ui.BROADCAST_BODY)]})))
        jl.append("execute if score @s rpg_q%d matches 99 run data modify storage rpg:panel ui.body append value %s"
                  % (k, J({"text": "", "extra": [seg(name, ui.MUTED), seg("　已完成\n", ui.READY)]})))
    head = "data modify storage rpg:panel ui.body append value " + J({"text": "", "extra": [seg("支线\n", ui.BROADCAST_BODY, True)]})
    s = read("events/jr/body.mcfunction")
    if "rpg_q1 matches" not in s:
        lines = s.split("\n")
        at = next(i for i, l in enumerate(lines) if "今日悬赏" in l)
        lines[at:at] = [head] + jl + ["data modify storage rpg:panel ui.body append value " + J({"text": "\n"})]
        at2 = next(i for i, l in enumerate(lines) if "返回面板" in l)
        lines.insert(at2, "data modify storage rpg:panel ui.actions append value " + J(
            {"label": seg("称号", ui.BROADCAST_HOLY, True), "tooltip": seg("名字前的小图标", ui.BROADCAST_BODY),
             "action": {"type": "minecraft:run_command", "command": "/trigger rpg_q_do set 1"}}))
        write("events/jr/body.mcfunction", "\n".join(lines))


# ============================================================================ 称号
def titles_load():
    out = []
    for k, (name, how) in TITLES.items():
        out += ["team add rpg_t_%s" % k,
                "team modify rpg_t_%s prefix %s" % (k, J(["", {"text": WA.TITLE_CHARS[k], "font": "rpg:world_titles", "color": "white"},
                                                         {"text": " ", "color": "white"}]))]
    return out


def titles():
    for k, (name, how) in TITLES.items():
        fn("title/get_%s" % k, [
            "execute if entity @s[tag=rpg.t.%s] run return 0" % k,
            "tag @s add rpg.t.%s" % k,
            "playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1.4",
            "tellraw @s " + J(["", seg("[称号]", ui.HOLY, True), seg("　", ui.GRAY),
                               {"text": WA.TITLE_CHARS[k], "font": "rpg:world_titles", "color": "white"},
                               seg(" " + name, ui.WHITE, True), seg("　" + how + "。在「旅程」页的称号里戴上它。", ui.GRAY)])])
        fn("title/wear_%s" % k, [
            "execute unless entity @s[tag=rpg.t.%s] run return run tellraw @s %s" % (k, J(["", seg("[称号]", ui.HOLY, True), seg("　还没得到这个称号。", ui.GRAY)])),
            "team join rpg_t_%s @s" % k, "playsound minecraft:item.armor.equip_gold player @s ~ ~ ~ 1 1.2"])
    fn("title/off", ["team leave @s"])
    from forge_ops import dialog, tt, T_BODY, T_MUTED, NL
    body = [tt("称号显示在名字前（聊天、头顶、Tab 列表）。一次只戴一个。", T_BODY), NL, NL]
    for k, (name, how) in TITLES.items():
        body += [{"text": WA.TITLE_CHARS[k], "font": "rpg:world_titles", "color": "white"}, tt(" " + name, T_BODY, True),
                 tt("　" + how, T_MUTED), NL]
    acts = [(name, ui.HOLY, 40 + i) for i, (k, (name, how)) in enumerate(TITLES.items())] + [("不戴", ui.MUTED, 49)]
    d = dialog("称号", body, acts, exit_label="合上").replace("/trigger rpg_fg_do set", "/trigger rpg_q_do set")
    d = d.replace('"[锻造]"', '"[称号]"')
    fn("titles", [d])


# ============================================================================ 彩蛋
def eggs():
    sec = ["# 每秒：满足条件的人计时加一，条件断了就清零",
           "tag @a remove rpg.q.gate", "tag @a remove rpg.q.sun",
           "execute as @a[y=150,dy=400] if items entity @s weapon.mainhand *[minecraft:custom_data~{jachin_tag:1b}] if items entity @s weapon.offhand *[minecraft:custom_data~{boaz_tag:1b}] at @s run function %s/egg/gate_tick" % P,
           "execute as @a[scores={rpg_sef=10},x_rotation=-90..-60] if items entity @s weapon.mainhand *[minecraft:custom_data~{saber_tag:1b}] at @s run function %s/egg/meteor_tick" % P,
           "scoreboard players set @a[tag=!rpg.q.gate,scores={rpg_q_eg=1..}] rpg_q_eg 0",
           "scoreboard players set @a[tag=!rpg.q.sun,scores={rpg_q_em=1..}] rpg_q_em 0"]
    fn("egg/sec", sec)
    # 所罗门的门户：主手雅斤、副手波阿斯，在 y ≥ 150 站 10 秒
    fn("egg/gate_tick", ["tag @s add rpg.q.gate", "scoreboard players add @s rpg_q_eg 1",
                         "particle minecraft:end_rod ~1.2 ~ ~ 0 3 0 0 12", "particle minecraft:end_rod ~-1.2 ~ ~ 0 3 0 0 12",
                         "execute if score @s rpg_q_eg matches 10 run function %s/title/get_gate" % P])
    # 白昼流星：王冠阶、正午前后，主手无垠星空，仰头 3 秒
    fn("egg/meteor_tick", ["execute store result score #d rpg_q_st run time query daytime",
                           "execute unless score #d rpg_q_st matches 5000..7000 run return 0",
                           "tag @s add rpg.q.sun", "scoreboard players add @s rpg_q_em 1",
                           "execute if score @s rpg_q_em matches 3 run function %s/egg/meteor_go" % P])
    fn("egg/meteor_go", ["particle minecraft:end_rod ~ ~30 ~ 16 2 16 0.3 300 force",
                         "particle minecraft:firework ~ ~25 ~ 12 4 12 0.1 120 force",
                         "playsound minecraft:entity.firework_rocket.twinkle_far master @a[distance=..64] ~ ~ ~ 1 1",
                         "function %s/title/get_meteor" % P])
    # 大团长：召出雅克残影时 16 格内有只叫「大团长」的狼
    patch("jacques_ally/summon.mcfunction", "%s/egg/grandmaster" % P,
          "execute if entity @e[type=minecraft:wolf,name=\"大团长\",distance=..16] run function %s/egg/grandmaster\n" % P)
    fn("egg/grandmaster", ["execute at @e[type=minecraft:wolf,name=\"大团长\",distance=..16,limit=1] run particle minecraft:end_rod ~ ~1.2 ~ 0.3 0.6 0.3 0.02 20",
                           "tellraw @s " + J(["", seg("（残影朝那只狗低头行了一礼。）", ui.MUTED)]),
                           "function %s/title/get_grandmaster" % P])
    # 所罗门的账簿：七柱三十五名罪仆都亲手打败过（一个进度 35 条）
    crit = {}
    for lord in range(1, 8):
        for role in range(1, 6):
            crit["l%dr%d" % (lord, role)] = {"trigger": "minecraft:player_killed_entity", "conditions": {"entity": [
                {"condition": "minecraft:entity_properties", "entity": "this",
                 "predicate": {"nbt": "{Tags:[\"rpg.demon.minion.lord%d\",\"rpg.demon.minion.role%d\"]}" % (lord, role)}}]}}
    wj(os.path.join(DP, "data", "rpg", "advancement", "quest", "ledger.json"),
       {"criteria": crit, "rewards": {"function": "%s/title/get_ledger" % P}})
    # 摇摆者：同一天里堕入魔力又回到圣力
    patch("sephira/force/fall.mcfunction", "rpg_q_fd", "execute store result score @s rpg_q_fd run time query day\n")
    patch("sephira/force/rise.mcfunction", "%s/egg/waverer" % P, "function %s/egg/waverer\n" % P)
    fn("egg/waverer", ["execute store result score #d rpg_q_st run time query day",
                       "execute if score #d rpg_q_st = @s rpg_q_fd run function %s/title/get_waverer" % P])


def main():
    import shutil
    shutil.rmtree(os.path.join(FUNC, "quest"), ignore_errors=True)
    quests()
    titles()
    eggs()
    print("quests: %d functions, %d side quests, %d titles" % (COUNT, len(QUESTS), len(TITLES)))


if __name__ == "__main__":
    main()
