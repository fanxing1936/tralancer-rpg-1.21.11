# -*- coding: utf-8 -*-
"""新手开局（用户 2026-11-23）。

新人第一次进世界：
  黑屏 · 欢迎来到破碎大陆（希伯来原文）+ 写昵称
  → 要不要先看序章（自由选择；进的话只带他一个人，有人在玩就黑屏排队或跳过；
    之后任何人都能在玩家面板点「序章」进入，用户 2026-11-23）
  → 随机全名 / 家族 / 国家（可以换）
  → 抽身份（onboard_spec.IDENTITIES / ODDS；圣子、圣灵、弥赛亚全世界各一人）
  → 锻造教学：选一种武器，魂火冶炼出一身装备（四件护甲 + 一把武器），免费洗炼、镀金各一次，
    免费镶一枚符文或符石；最后告诉玩家以后冶炼要找灵魂营火
  → 回到出生的位置，正式开始。

黑屏：玩家切旁观、升到原地上空 y=316、失明（失明的雾把天空和远处全压成黑色）。所有界面都是对话框，
不能按 Esc 关；万一界面没了，聊天栏有一行「点这里重新打开」。
昵称用对话框的文字输入框 + /function 宏传回来：要有执行命令的权限（单人存档开作弊、或服务器 OP）。
没权限时可以点「用游戏名」继续。

所有人都要走（用户 2026-11-23「所有人只要在新版本进入游戏都需要过一遍新手教程」）：rpg_ob_v 没到 1 的人
进流程；已经在新手开局里抽过身份的人算走完。老玩家身上的护甲、副手、主手先收进 storage，
结束时还回去，教学装备格子不空就掉在脚边。游戏模式结束时还原。

管理员：
  /function rpg:onboard/admin/new      把自己当新人，从序章开始走一遍（会放回唯一身份）
  /function rpg:onboard/admin/skip     结束自己的流程（不发装备）
  /function rpg:onboard/admin/free_unique   把圣子、圣灵、弥赛亚放回池子
身份记分板：rpg_ident（1 无知者 2 边缘者 3 神职者 4 七大罪之仆 5 圣子 6 圣灵 7 弥赛亚）、
rpg_ident_sin（七大罪之仆的领主，ui.PILLARS 的 n）、rpg_messiah（圣子/圣灵/弥赛亚为 1）。
"""
import io
import json
import os
import sys

import rpg_ui_style as ui
import onboard_spec as S
import forge_spec as FS
from forge_common import WS, EQ
from forge_ops import grade_lines
from display_mob import hook_tag

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
RP = sys.argv[2] if len(sys.argv) > 2 else None      # 资源包：旁白的语言文件与配音
FUNC = os.path.join(DP, "data", "rpg", "function")
OUT = os.path.join(FUNC, "onboard")
P = "rpg:onboard"
O = "rpg_ob"            # 阶段
DO = "rpg_ob_do"        # 对话框按钮（trigger）
COUNT = 0

C_TITLE = "#E8D9B0"
C_BODY = ui.BROADCAST_BODY
C_NAME = ui.BROADCAST_NAME
C_GOLD = "#FFD85A"
C_MUTED = ui.MUTED
C_WARN = ui.BROADCAST_WARN
HOLD_Y = 316

# 阶段
ST_PRO, ST_NAME, ST_CARD, ST_DRAW, ST_IDENT = 1, 2, 3, 4, 5
ST_ASK = 16             # 起好名字后：要不要先看序章（用户 2026-11-23「序章放到欢迎页后面，自由选择进入」）
ST_WEAPON, ST_MADE, ST_WASH, ST_WASH_PICK, ST_GILD, ST_GILD_DONE = 6, 7, 8, 9, 10, 11
ST_INLAY, ST_RUNE, ST_STONE, ST_END = 12, 13, 14, 15
ST_INTRO = 17           # 黑屏里的世界观旁白，起名之前（用户 2026-11-23）
ST_DONE = 100

# 新手护甲（用户 2026-11-23）：四件各不相同，都带纹饰。(底材, 纹饰图案, 纹饰材料)
STARTER = {
    "head": ("iron_helmet", "ward", "quartz"),              # 铁头盔 · 监守 · 石英
    "chest": ("chainmail_chestplate", "ward", "iron"),      # 锁链胸甲 · 监守 · 铁
    "legs": ("leather_leggings", "flow", "copper"),         # 皮革护腿 · 涤流 · 铜
    "feet": ("iron_boots", "rib", "netherite"),             # 铁靴 · 肋骨 · 下界合金（黑）
}
# 新手装备按物品规范（ART-STYLE §2）：[启程] 前缀加粗暗金、本名白色；Lore 分隔线 + 题记 + 灰色正文，
# 下面接锻造的属性块（属性块自己以分隔线收尾）
STARTER_PREFIX = ("[启程]", ui.HOLY_DARK)
STARTER_LORE = [[{"text": ui.RULE_TEXT, "color": ui.WHITE, "bold": False, "italic": False}],
                [{"text": "[魂火初炼]", "color": ui.HOLY_DARK, "bold": True, "italic": False}],
                [{"text": "破碎大陆为初来者炼成的第一身装备", "color": ui.GRAY, "bold": False, "italic": False}]]

# 配乐（唱片机音量，同 Boss 战与序章）：旁白一首，之后的流程一首。曲子登记在 add_boss_bgm.py
MUSIC = {1: "onboard_intro", 2: "onboard_flow"}
# 按钮音效：对话框每次按下都响一声（用户 2026-11-23「点按钮的时候需要有音效反馈」）
CLICK = "playsound minecraft:block.note_block.chime master @s ~ ~ ~ 0.55 1.2"

WEAPONS = [t for t in FS.SMELT_TYPES if t[2] != "armor"]          # 长剑 战斧 重锤 长弓 劲弩
ARMOR = [t for t in FS.SMELT_TYPES if t[2] == "armor"]
TIER = FS.TIERS[0][0]                                              # 教学用无档（铁）


def fn(name, lines):
    global COUNT
    path = os.path.join(OUT, name + ".mcfunction")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    COUNT += 1


def J(o):
    return json.dumps(o, ensure_ascii=False, separators=(",", ":"))


def t(text, colour=C_BODY, bold=False, italic=False):
    return {"text": text, "color": colour, "bold": bold, "italic": italic}


NL = t("\n")


def trig(v):
    return {"type": "minecraft:run_command", "command": "/trigger %s set %d" % (DO, v)}


def dialog(title, body, actions, inputs=None, columns=None):
    """黑屏里的对话框：不能 Esc 关，没有退出按钮。actions: [(文字, 颜色, trigger 值或 action 字典)]。"""
    doc = {
        "type": "minecraft:multi_action",
        "title": ["", t(title, C_TITLE, True)],
        "body": {"type": "minecraft:plain_message", "width": 320, "contents": [""] + body},
        "actions": [{"label": t(lab, col, True), "action": (trig(v) if isinstance(v, int) else v)} for lab, col, v in actions],
        "columns": columns or (1 if len(actions) == 1 else 2),
        "can_close_with_escape": False,
        "pause": False,
        "after_action": "close",
    }
    if inputs:
        doc["inputs"] = inputs
    return "dialog show @s " + J(doc)


def say(text, colour=C_BODY):
    return "tellraw @s " + J(["", t("[破碎大陆] ", C_GOLD, True), t(text, colour)])


def pid_macro(lines):
    """以玩家号为宏参数的函数：先把 rpg_fg_id 放进 rpg:onboard tmp.id。"""
    return ["execute store result storage rpg:onboard tmp.id int 1 run scoreboard players get @s rpg_fg_id"] + lines


# ---------------------------------------------------------------------------- 加载、每刻、判新人
def core():
    fn("load", [
        "scoreboard objectives add %s dummy" % O,
        "scoreboard objectives add %s trigger" % DO,
        "scoreboard objectives add rpg_ob_t dummy",
        "scoreboard objectives add rpg_pro_go trigger",
        "scoreboard objectives add rpg_ob_w dummy",
        "scoreboard objectives add rpg_ob_lv minecraft.custom:minecraft.leave_game",
        "scoreboard objectives add rpg_ident dummy",
        "scoreboard objectives add rpg_ident_sin dummy",
        "scoreboard objectives add rpg_messiah dummy",
        "scoreboard objectives add rpg_ob_v dummy",
        "scoreboard objectives add rpg_ob_gm dummy",
        "scoreboard objectives add rpg_ob_it dummy",     # 旁白计时（刻）
        "scoreboard objectives add rpg_ob_mt dummy",     # 配乐剩余（刻），到 0 重放
        "scoreboard objectives add rpg_ob_mi dummy",     # 正在放哪一首（MUSIC 的键，0 = 不放）
        "# 装上这个模块的那一刻：已经有锻造玩家号的人都是老玩家",
        "execute unless score #inst %s matches 1 run scoreboard players operation #cut %s = #pid rpg_fg" % (O, O),
        "execute unless score #inst %s matches 1 unless score #cut %s matches 0.. run scoreboard players set #cut %s 0" % (O, O, O),
        "scoreboard players set #inst %s 1" % O,
        "scoreboard players set #twenty %s 20" % O,
        "data modify storage rpg:onboard names.given set value %s" % J(S.GIVEN),
        "data modify storage rpg:onboard names.house set value %s" % J(S.HOUSES),
        "data modify storage rpg:onboard names.nation set value %s" % J(S.NATIONS),
        "data modify storage rpg:onboard names.mid set value %s" % J(["·" + c for c in S.MIDDLE_LETTERS]),
    ])
    fn("tick", [
        "scoreboard players enable @a rpg_pro_go",
        "execute as @a[scores={rpg_pro_go=1..}] run function %s/pro/req" % P,
        "execute as @a[tag=!rpg.ob,tag=!rpg.pr] unless score @s rpg_ob_v matches 1.. run function %s/check" % P,
        "execute as @a[tag=rpg.ob,tag=!rpg.pr] at @s run function %s/player" % P,
    ])
    fn("check", [
        "# 新版本里第一次见到这名玩家（as 玩家）。用户 2026-11-23：所有人都要走一遍新手开局，老玩家也不例外。",
        "# 已经在新手开局里抽过身份的人（这一版之前测试过的）算走完了，不再重来。",
        "execute unless score @s rpg_fg_id matches 1.. run return 0",
        "execute if score @s rpg_ident matches 1.. run scoreboard players set @s %s %d" % (O, ST_DONE),
        "execute if score @s rpg_ident matches 1.. run return run scoreboard players set @s rpg_ob_v 1",
        "function %s/begin" % P,
    ])
    fn("begin", pid_macro([
        "# 新人：记下出生的位置，进黑屏，先听世界观旁白，再到欢迎页起名",
        "tag @s add rpg.ob",
        "scoreboard players set @s %s %d" % (O, ST_INTRO),
        "scoreboard players set @s rpg_ob_lv 0",
        "function %s/save_pos with storage rpg:onboard tmp" % P,
        "# 原来的游戏模式：结束时还原（不是一律生存）",
        "scoreboard players set @s rpg_ob_gm 0",
        "execute if entity @s[gamemode=creative] run scoreboard players set @s rpg_ob_gm 1",
        "execute if entity @s[gamemode=adventure] run scoreboard players set @s rpg_ob_gm 2",
        "# 老玩家身上的护甲、副手、主手先收起来，教学用的格子要空着；结束时原样还回去",
        "function %s/stash/put with storage rpg:onboard tmp" % P,
        "function %s/hold/enter" % P,
        "tag @s add rpg.ob.wait",
        "scoreboard players set @s rpg_ob_t 0",
    ]))
    fn("save_pos", [
        "$data modify storage rpg:onboard p$(id).dim set from entity @s Dimension",
        "$data modify storage rpg:onboard p$(id).x set from entity @s Pos[0]",
        "$data modify storage rpg:onboard p$(id).y set from entity @s Pos[1]",
        "$data modify storage rpg:onboard p$(id).z set from entity @s Pos[2]",
    ])
    fn("player", [
        "# 流程中的玩家每刻（as/at 玩家；序章里的人不走这里）",
        "execute if score @s rpg_ob_lv matches 1.. run function %s/relog" % P,
        "scoreboard players add @s rpg_ob_t 1",
        "scoreboard players enable @s %s" % DO,
        "execute if score @s %s matches 1.. run function %s/press" % (DO, P),
        "execute if score @s %s matches %d unless entity @s[tag=rpg.ob.pro] if score @s rpg_ob_t matches 100.. run function %s/pro/try" % (O, ST_PRO, P),
        "execute as @s[tag=rpg.ob.queued] unless score @s %s matches %d run tag @s remove rpg.ob.queued" % (O, ST_PRO),
        "# 序章在准备阶段就取消了（没把人接进去）：跳过序章",
        "execute if entity @s[tag=rpg.ob.pro] if score @s rpg_ob_t matches 100.. unless score #state rpg_pr matches 1.. run function %s/pro/after" % P,
        "execute if entity @s[tag=rpg.ob.wait] if score @s rpg_ob_t matches 60.. run function %s/show" % P,
        "execute if entity @s[tag=rpg.ob.intro] run function %s/intro/tick" % P,
        "execute if score @s rpg_ob_mi matches 1.. run function %s/music/tick" % P,
        "scoreboard players operation #m %s = @s rpg_ob_t" % O,
        "scoreboard players operation #m %s %%= #twenty %s" % (O, O),
        "execute if score #m %s matches 0 run function %s/hold/keep" % (O, P),
    ])
    fn("relog", [
        "# 中途退出又回来：回到黑屏，重新弹出当前这一步",
        "scoreboard players set @s rpg_ob_lv 0",
        "# 旁白听到一半退出：回来从头放（配乐也要重新起）",
        "execute if entity @s[tag=rpg.ob.intro] run function %s/intro/stop" % P,
        "scoreboard players set @s rpg_ob_mt 0",
        "execute if score @s %s matches %d run tag @s remove rpg.ob.queued" % (O, ST_PRO),
        "execute if score @s %s matches %d run return run scoreboard players set @s rpg_ob_t 0" % (O, ST_PRO),
        "function %s/hold/enter" % P,
        "tag @s add rpg.ob.wait",
        "scoreboard players set @s rpg_ob_t 0",
    ])


# ---------------------------------------------------------------------------- 黑屏
def hold():
    fn("hold/tp", ["$execute in $(dim) run tp @s $(x) %d $(z) 0 90" % HOLD_Y])
    fn("hold/tp_go", ["$function %s/hold/tp with storage rpg:onboard p$(id)" % P])
    fn("hold/enter", pid_macro([
        "# 进黑屏：旁观、失明、升到原地上空（周围什么都没有，失明的雾把画面压成全黑）",
        "tag @s add rpg.ob.hold",
        "gamemode spectator @s",
        "effect clear @s",
        "effect give @s minecraft:blindness infinite 0 true",
        "function %s/hold/tp_go with storage rpg:onboard tmp" % P,
        "stopsound @s music",
        "title @s clear",
        "tellraw @s %s" % J(["", t("[破碎大陆] ", C_GOLD, True), t("界面不见了？", C_BODY),
                             {"text": "[点这里重新打开]", "color": C_GOLD, "underlined": True, "bold": False, "italic": False,
                              "click_event": {"action": "run_command", "command": "/trigger %s set 99" % DO}}]),
    ]))
    fn("hold/keep", pid_macro([
        "# 每秒：失明别掉，人别飘走",
        "execute unless entity @s[tag=rpg.ob.hold] run return 0",
        "gamemode spectator @s",
        "effect give @s minecraft:blindness infinite 0 true",
        "execute unless entity @s[y=%d,dy=2] run function %s/hold/tp_go with storage rpg:onboard tmp" % (HOLD_Y - 1, P),
    ]))


# ---------------------------------------------------------------------------- 世界观旁白 + 配乐
def bar(kind):
    return "rpg:ob_%s_$(id)" % kind      # 每名玩家自己的两条字幕血条（宏 id = rpg_fg_id）


def intro():
    """黑屏里的世界观旁白（用户 2026-11-23）：照序章的字幕做法，两条粉色 Boss 血条只剩名字，
    中文在上、英文在下；配音挑好了就跟着放（onboard_text.py）。聊天栏有「跳过」。"""
    import onboard_text as OT
    plan, total = OT.timeline()
    fn("intro/start", pid_macro([
        "# 进入旁白（as 玩家）；已经在放就不重来（「重新打开」点到这里时）",
        "execute if entity @s[tag=rpg.ob.intro] run return 0",
        "tag @s add rpg.ob.intro",
        "scoreboard players set @s rpg_ob_it 0",
        "function %s/intro/bars with storage rpg:onboard tmp" % P,
        "function %s/music/intro" % P,
        "tellraw @s %s" % J(["", t("[破碎大陆] ", C_GOLD, True), t("旁白约一分钟。", C_BODY),
                             {"text": "[跳过旁白]", "color": C_GOLD, "underlined": True, "bold": False, "italic": False,
                              "click_event": {"action": "run_command", "command": "/trigger %s set 98" % DO}}]),
    ]))
    bars = []
    for kind in ("zh", "en"):             # 先加的在上面
        bars += ["$bossbar add %s \"\"" % bar(kind),
                 "$bossbar set %s name \"\"" % bar(kind),
                 "$bossbar set %s color pink" % bar(kind),
                 "$bossbar set %s value 0" % bar(kind),
                 "$bossbar set %s players @s" % bar(kind),
                 "$bossbar set %s visible true" % bar(kind)]
    fn("intro/bars", bars)
    fn("intro/unbars", ["$bossbar remove %s" % bar("zh"), "$bossbar remove %s" % bar("en")])
    tick = ["scoreboard players add @s rpg_ob_it 1"]
    for at, x, hold_t in plan:
        lid = x["id"].lower()
        zh, en = OT.bar_names(x)
        body = ["$bossbar set %s name %s" % (bar("zh"), J(zh)), "$bossbar set %s name %s" % (bar("en"), J(en))]
        if OT.voiced(x):
            body.append("playsound rpg:vo.onboard.%s voice @s ~ ~ ~ 1 1" % lid)
        fn("intro/l_%s" % lid, body)
        tick.append("execute if score @s rpg_ob_it matches %d run function %s/intro/l_%s with storage rpg:onboard tmp" % (at, P, lid))
        parts = OT.PT.split_en(x["en"])
        for i in range(1, len(parts)):
            _zh, en_i = OT.bar_names(x, i)
            fn("intro/l_%s_%d" % (lid, i), ["$bossbar set %s name %s" % (bar("en"), J(en_i))])
            tick.append("execute if score @s rpg_ob_it matches %d run function %s/intro/l_%s_%d with storage rpg:onboard tmp"
                        % (at + int(hold_t * i / len(parts)), P, lid, i))
        tick.append("execute if score @s rpg_ob_it matches %d run function %s/intro/blank with storage rpg:onboard tmp" % (at + hold_t, P))
    tick.append("execute if score @s rpg_ob_it matches %d.. run function %s/intro/end" % (total, P))
    # 计时之前先把 tmp.id 放好：每一句都是宏
    fn("intro/tick", pid_macro(tick))
    fn("intro/blank", ["$bossbar set %s name \"\"" % bar("zh"), "$bossbar set %s name \"\"" % bar("en")])
    fn("intro/stop", pid_macro([
        "# 收起旁白：字幕血条、配音、旁白配乐",
        "tag @s remove rpg.ob.intro",
        "function %s/intro/unbars with storage rpg:onboard tmp" % P,
        "stopsound @s voice",
        "function %s/music/stop" % P,
    ]))
    fn("intro/end", [
        "# 旁白放完或跳过：到欢迎页起名",
        "function %s/intro/stop" % P,
        "scoreboard players set @s %s %d" % (O, ST_NAME),
        "playsound minecraft:block.enchantment_table.use master @s ~ ~ ~ 0.6 0.7",
        "function %s/show" % P,
    ])
    # 旁白和起名之间的文字都在资源包的语言文件里（数据包里带原文作 fallback）
    if RP:
        OT.write_lang(RP)
        n = OT.vo_sounds(RP)
        print("onboard intro: %d lines, %d voiced, %.1f s" % (len(plan), n, total / 20.0))


def music():
    import prologue_text as PT
    for k, name in MUSIC.items():
        src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bgm_ref", name + ".ogg")
        ticks = int(PT.ogg_seconds(src) * 20) + 1 if os.path.isfile(src) else 2400
        fn("music/" + name.split("_")[1], [
            "stopsound @s record",
            "stopsound @s music",
            "playsound rpg:bgm.%s record @s ~ ~ ~ 1 1" % name,
            "scoreboard players set @s rpg_ob_mi %d" % k,
            "scoreboard players set @s rpg_ob_mt %d" % ticks,
        ])
    fn("music/tick", [
        "# 放完自己循环（as 玩家）",
        "scoreboard players remove @s rpg_ob_mt 1",
        "execute if score @s rpg_ob_mt matches 1.. run return 0",
    ] + ["execute if score @s rpg_ob_mi matches %d run return run function %s/music/%s" % (k, P, name.split("_")[1])
         for k, name in MUSIC.items()])
    fn("music/stop", ["stopsound @s record rpg:bgm.%s" % name for name in MUSIC.values()] + [
        "scoreboard players set @s rpg_ob_mi 0", "scoreboard players set @s rpg_ob_mt 0"])


# ---------------------------------------------------------------------------- 序章
def prologue():
    src = io.open(os.path.join(FUNC, "prologue", "start.mcfunction"), encoding="utf-8").read().split("\n")
    sel = "tag @a[distance=..16,gamemode=!spectator,limit=4,sort=nearest] add rpg.pr.join"
    assert sel in src, "prologue/start 改过了，序章入口要跟着改"
    lines = ["# 只带这一名新人进序章（改自 rpg:prologue/start；忙的时候由 pro/try 排队）"]
    for ln in src:
        if not ln or ln.startswith("#") or "return run tellraw" in ln:
            continue
        lines.append("tag @s add rpg.pr.join" if ln == sel else ln)
    fn("pro/go", lines)
    fn("pro/try", [
        "scoreboard players set @s rpg_ob_t 0",
        "execute if score #state rpg_pr matches 1.. run return run function %s/pro/wait" % P,
        "execute if score #fight rpg_mk matches 1 run return run function %s/pro/wait" % P,
        "tag @s remove rpg.ob.hold",
        "effect clear @s minecraft:blindness",
        "tag @s add rpg.ob.pro",
        "function %s/pro/go" % P,
    ])
    fn("pro/wait", [
        "execute unless entity @s[tag=rpg.ob.hold] run function %s/hold/enter" % P,
        "execute unless entity @s[tag=rpg.ob.queued] run function %s/pro/busy" % P,
        "tag @s add rpg.ob.queued",
    ])
    pro_body = [t("一千年前，路西法与他的领主们在这片大陆上同神的军队开战。", C_BODY), NL,
                t("序章让你亲历那一战：过场、群战，最后是米迦勒。约十分钟。", C_BODY), NL, NL,
                t("现在不看也可以：之后随时在玩家面板点「序章」进入。", C_MUTED)]
    fn("pro/ask", [dialog("序章 · 一千年前", pro_body, [("进入序章", C_GOLD, 1), ("先跳过", C_BODY, 2)])])
    fn("pro/ask_press", [
        "execute if score #do %s matches 1 run scoreboard players set @s %s %d" % (O, O, ST_PRO),
        "execute if score #do %s matches 1 run return run function %s/pro/try" % (O, P),
        "execute unless score #do %s matches 2 run return 0" % O,
        "scoreboard players set @s %s %d" % (O, ST_CARD),
        "function %s/show" % P,
    ])
    fn("pro/busy", [dialog("序章 · 一千年前", [
        t("序章正被其他人游玩（同一时间只能开一场）。", C_BODY), NL, NL,
        t("可以在黑暗里等一会儿，空出来就自动进入；也可以先跳过，之后在玩家面板点「序章」进入。", C_MUTED)],
        [("继续等待", C_BODY, 1), ("先跳过", C_GOLD, 2)])])
    fn("pro/busy_press", [
        "execute unless score #do %s matches 2 run return 0" % O,
        "tag @s remove rpg.ob.queued",
        "scoreboard players set @s %s %d" % (O, ST_CARD),
        "function %s/show" % P,
    ])
    fn("pro/req", [
        "# 玩家面板「序章」按钮（trigger rpg_pro_go，任何人随时可以进；as 玩家）",
        "scoreboard players set @s rpg_pro_go 0",
        "execute if entity @s[tag=rpg.ob] run return 0",
        "execute if entity @s[tag=rpg.pr] run return 0",
        "execute if score #state rpg_pr matches 1.. run return run %s" % say("序章正被其他人游玩，同一时间只能开一场，稍后再试。"),
        "execute if score #fight rpg_mk matches 1 run return run %s" % say("有一场米迦勒战正在进行，结束后再进入序章。"),
        "function %s/pro/go" % P,
    ])
    fn("pro/after", [
        "# 序章结束、被中止或中途掉线后还原（接在 rpg:prologue/iso/restore 末尾）：进黑屏，下一步",
        "tag @s remove rpg.ob.pro",
        "tag @s remove rpg.ob.queued",
        "execute unless score @s %s matches %d run return 0" % (O, ST_PRO),
        "scoreboard players set @s %s %d" % (O, ST_CARD),
        "function %s/hold/enter" % P,
        "tag @s add rpg.ob.wait",
        "scoreboard players set @s rpg_ob_t 0",
    ])


# ---------------------------------------------------------------------------- 显示与按钮分派
def show_and_press():
    stages = [(ST_NAME, "name/show"), (ST_ASK, "pro/ask"), (ST_CARD, "card/show"), (ST_DRAW, "ident/ask"), (ST_IDENT, "ident/show"),
              (ST_WEAPON, "tut/weapon"), (ST_MADE, "tut/made_show"), (ST_WASH, "tut/wash"), (ST_WASH_PICK, "tut/wash_show"),
              (ST_GILD, "tut/gild"), (ST_GILD_DONE, "tut/gild_show"), (ST_INLAY, "tut/inlay"), (ST_RUNE, "tut/runes"),
              (ST_STONE, "tut/stones"), (ST_END, "tut/end")]
    fn("show", ["tag @s remove rpg.ob.wait",
                 "# 新手流程里不再问要不要看序章（用户 2026-11-23）：停在这一步的老存档直接去名字卡",
                 "execute if score @s %s matches %d run scoreboard players set @s %s %d" % (O, ST_ASK, O, ST_CARD),
                 "execute if score @s %s matches %d run return run function %s/intro/start" % (O, ST_INTRO, P),
                 "# 旁白之后的流程都配同一首曲子",
                 "execute unless score @s rpg_ob_mi matches 2 run function %s/music/flow" % P,
                 "execute if score @s %s matches %d if entity @s[tag=rpg.ob.queued] run return run function %s/pro/busy" % (O, ST_PRO, P)] +
       ["execute if score @s %s matches %d run return run function %s/%s" % (O, s, P, f) for s, f in stages])
    fn("press", [
        "scoreboard players operation #do %s = @s %s" % (O, DO),
        "scoreboard players set @s %s 0" % DO,
        "# 旁白里聊天栏的「跳过」",
        "execute if score #do %s matches 98 if score @s %s matches %d run return run function %s/intro/end" % (O, O, ST_INTRO, P),
        "execute if score #do %s matches 98 run return 0" % O,
        "execute if score #do %s matches 99 run return run function %s/show" % (O, P),
        CLICK,
        "execute if score @s %s matches %d run return run function %s/name/press" % (O, ST_NAME, P),
        "execute if score @s %s matches %d run return run function %s/pro/ask_press" % (O, ST_ASK, P),
        "execute if score @s %s matches %d run return run function %s/pro/busy_press" % (O, ST_PRO, P),
        "execute if score @s %s matches %d run return run function %s/card/press" % (O, ST_CARD, P),
        "execute if score @s %s matches %d run return run function %s/ident/draw" % (O, ST_DRAW, P),
        "execute if score @s %s matches %d run return run function %s/tut/start" % (O, ST_IDENT, P),
        "execute if score @s %s matches %d run return run function %s/tut/weapon_press" % (O, ST_WEAPON, P),
        "execute if score @s %s matches %d run return run function %s/tut/to_wash" % (O, ST_MADE, P),
        "execute if score @s %s matches %d run return run function %s/tut/wash_roll" % (O, ST_WASH, P),
        "execute if score @s %s matches %d run return run function %s/tut/wash_pick" % (O, ST_WASH_PICK, P),
        "execute if score @s %s matches %d run return run function %s/tut/gild_do" % (O, ST_GILD, P),
        "execute if score @s %s matches %d run return run function %s/tut/to_inlay" % (O, ST_GILD_DONE, P),
        "execute if score @s %s matches %d run return run function %s/tut/inlay_press" % (O, ST_INLAY, P),
        "execute if score @s %s matches %d run return run function %s/tut/rune_press" % (O, ST_RUNE, P),
        "execute if score @s %s matches %d run return run function %s/tut/stone_press" % (O, ST_STONE, P),
        "execute if score @s %s matches %d run return run function %s/finish" % (O, ST_END, P),
    ])


# ---------------------------------------------------------------------------- 欢迎 + 昵称
def name():
    # 世界观已经在前面的旁白里讲过了（intro），欢迎页只留名字和问题
    head = [t(S.WELCOME_HE, C_GOLD, True), NL, t(S.WELCOME_LATIN, C_MUTED, italic=True), NL, NL,
            t("在这里，你会被怎样称呼？", C_NAME)]
    actions = [("就这样称呼我", C_GOLD, {"type": "minecraft:dynamic/run_command",
                                       "template": "/function %s/name/set {n:\"$(nick)\"}" % P}),
               ("用我的游戏名", C_BODY, 2)]
    inputs = [{"type": "minecraft:text", "key": "nick", "label": t("昵称", C_BODY), "width": 220, "max_length": 16}]
    fn("name/show", [dialog("欢迎来到" + S.WELCOME_ZH, head, actions, inputs)])
    fn("name/retry", [dialog("欢迎来到" + S.WELCOME_ZH, head + [NL, NL, t("名字不能是空的，也不能带引号或反斜杠。", C_WARN)], actions, inputs)])
    fn("name/set", [
        "# 对话框传回的昵称（宏 n）。只认流程里、停在这一步的人",
        "execute unless score @s %s matches %d run return 0" % (O, ST_NAME),
        CLICK,
        "$data modify storage rpg:onboard tmp.n set value \"$(n)\"",
        "execute if data storage rpg:onboard tmp{n:\"\"} run return run function %s/name/retry" % P,
        "function %s/name/keep" % P,
    ])
    fn("name/press", [
        "# 「用我的游戏名」",
        "execute unless score #do %s matches 2 run return 0" % O,
        "loot replace entity @s weapon.mainhand loot %s/head_of" % P,
        "data modify storage rpg:onboard tmp.n set from entity @s SelectedItem.components.\"minecraft:profile\".name",
        "item replace entity @s weapon.mainhand with minecraft:air",
        "execute unless data storage rpg:onboard tmp.n run data modify storage rpg:onboard tmp.n set value \"无名旅人\"",
        "function %s/name/keep" % P,
    ])
    fn("name/keep", pid_macro([
        "function %s/name/store with storage rpg:onboard tmp" % P,
        "function %s/card/roll" % P,
        "# 起好名字直接去名字卡（序章入口从新手流程里拿掉了，用户 2026-11-23；玩家面板的「序章」按钮还在）",
        "scoreboard players set @s %s %d" % (O, ST_CARD),
        "playsound minecraft:block.enchantment_table.use master @s ~ ~ ~ 0.8 0.8",
        "function %s/show" % P,
    ]))
    fn("name/store", ["$data modify storage rpg:onboard p$(id).nick set from storage rpg:onboard tmp.n"])
    # 玩家自己的头颅 → 读出游戏名（不需要任何权限）
    path = os.path.join(DP, "data", "rpg", "loot_table", "onboard", "head_of.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"pools": [{"rolls": 1, "entries": [{"type": "minecraft:item", "name": "minecraft:player_head",
                                                          "functions": [{"function": "minecraft:fill_player_head", "entity": "this"}]}]}]},
                  fh, ensure_ascii=False, indent=1)


# ---------------------------------------------------------------------------- 全名、家族、国家
def card():
    roll = []
    for key, lst in (("given", S.GIVEN), ("house", S.HOUSES), ("nation", S.NATIONS)):
        roll += ["execute store result storage rpg:onboard tmp.r int 1 run random value 0..%d" % (len(lst) - 1),
                 "data modify storage rpg:onboard tmp.k set value \"%s\"" % key,
                 "function %s/card/pick with storage rpg:onboard tmp" % P]
    # 中间名：一半的人有，是一个字母（onboard_spec.MIDDLE_*）
    n = len(S.MIDDLE_LETTERS)
    span = int(round(n / S.MIDDLE_CHANCE)) - 1
    roll += ["function %s/card/nomid with storage rpg:onboard tmp" % P,
             "execute store result storage rpg:onboard tmp.r int 1 run random value 0..%d" % span,
             "data modify storage rpg:onboard tmp.k set value \"mid\"",
             "execute if data storage rpg:onboard tmp{r:%s} run return 0" % "X"]
    roll.pop()
    roll += ["execute store result score #mr %s run data get storage rpg:onboard tmp.r" % O,
             "execute if score #mr %s matches ..%d run function %s/card/pick with storage rpg:onboard tmp" % (O, n - 1, P)]
    fn("card/nomid", ['$data modify storage rpg:onboard p$(id).mid set value ""'])
    fn("card/roll", pid_macro(roll))
    fn("card/pick", ["$data modify storage rpg:onboard p$(id).$(k) set from storage rpg:onboard names.$(k)[$(r)]"])
    body = [t("命运为你写下了这些：", C_BODY), NL, NL,
            t("名号　", C_MUTED), t("$(nick)", C_NAME, True), NL,
            t("全名　", C_MUTED), t("$(given)$(mid)·$(house)", C_GOLD, True), NL,
            t("家族　", C_MUTED), t("$(house)家族", C_NAME), NL,
            t("国家　", C_MUTED), t("$(nation)", C_NAME), NL, NL,
            t("不满意可以重新生成；确定之后就不能再换了。", C_MUTED)]
    fn("card/show", pid_macro(["function %s/card/show_m with storage rpg:onboard tmp" % P]))
    fn("card/show_m", ["$function %s/card/dlg with storage rpg:onboard p$(id)" % P])
    fn("card/dlg", ["$" + dialog("你的名字", body, [("就是这个名字", C_GOLD, 1), ("重新生成", C_BODY, 2)])])
    fn("card/press", [
        "execute if score #do %s matches 2 run function %s/card/roll" % (O, P),
        "execute if score #do %s matches 2 run playsound minecraft:item.book.page_turn master @s ~ ~ ~ 1 1" % O,
        "execute if score #do %s matches 2 run return run function %s/show" % (O, P),
        "execute unless score #do %s matches 1 run return 0" % O,
        "scoreboard players set @s %s %d" % (O, ST_DRAW),
        "function %s/show" % P,
    ])


# ---------------------------------------------------------------------------- 身份
def identity():
    fn("ident/ask", [dialog("身份", [
        t("破碎大陆上，每个人生来就带着一种身份。", C_BODY), NL,
        t("有人一生都碰不到魔力；有人生在缝隙里；有人侍奉神；有人身上留着领主的印记。", C_BODY), NL, NL,
        t("而圣子、圣灵与弥赛亚，世间各只有一位。", C_GOLD), NL, NL,
        t("身份只抽一次。", C_MUTED)], [("揭晓我的身份", C_GOLD, 1)])])
    uniq = {k: i for i, (i, k, _n, _c, _d) in enumerate(S.IDENTITIES)}
    code = {k: n for n, k, _a, _b, _c in S.IDENTITIES}
    lines = ["# 抽一次身份（万分比，onboard_spec.ODDS）",
             "execute if score @s rpg_ident matches 1.. run return run function %s/ident/done" % P,
             "execute store result score #r %s run random value 0..9999" % O]
    lo = 0
    for key, w in S.ODDS:
        hi = lo + w - 1
        if key == "unique":
            lines.append("execute if score #r %s matches %d..%d run function %s/ident/unique" % (O, lo, hi, P))
        else:
            lines.append("execute if score #r %s matches %d..%d run scoreboard players set @s rpg_ident %d" % (O, lo, hi, code[key]))
        lo = hi + 1
    lines += [
        "execute if score @s rpg_ident matches 4 store result score @s rpg_ident_sin run random value 1..7",
        "execute if score @s rpg_ident matches 5..7 run scoreboard players set @s rpg_messiah 1",
        "function %s/ident/done" % P,
    ]
    fn("ident/draw", lines)
    # 唯一身份：三选一；被抽走的顺延到下一个还空着的，三个都没了就是无知者
    u = ["scoreboard players set @s rpg_ident 1",
         "execute store result score #u %s run random value 0..2" % O]
    order = S.UNIQUE
    for start in range(3):
        for k in range(3):
            key = order[(start + k) % 3]
            u.append("execute if score #u %s matches %d if score @s rpg_ident matches 1 unless data storage rpg:onboard taken.%s "
                     "run function %s/ident/take_%s" % (O, start, key, P, key))
    fn("ident/unique", u)
    for key in order:
        fn("ident/take_" + key, [
            "scoreboard players set @s rpg_ident %d" % code[key],
            "execute store result storage rpg:onboard taken.%s int 1 run scoreboard players get @s rpg_fg_id" % key,
        ])
    fn("ident/done", [
        "scoreboard players set @s %s %d" % (O, ST_IDENT),
        "playsound minecraft:block.end_portal.spawn master @s ~ ~ ~ 0.5 1.4",
        "execute if score @s rpg_messiah matches 1 run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 0.8",
        "function %s/show" % P,
    ])
    show = []
    for n, key, name, colour, desc in S.IDENTITIES:
        if key == "sin":
            for p in ui.PILLARS:
                show.append("execute if score @s rpg_ident matches 4 if score @s rpg_ident_sin matches %d run return run %s" % (
                    p["n"], dialog("身份", [
                        t("你是", C_BODY), NL, NL, t("七大罪之仆", colour, True), t(" · ", C_MUTED),
                        t("%s之%s" % (p["who"], p["sin"]), p["lit"], True), NL, NL,
                        t("%s在你身上留下了印记，你身负%s的魔力。" % (p["who"], p["sin"]), C_BODY), NL, NL,
                        t("接下来，去为自己炼一身装备。", C_MUTED)], [("开始锻造", C_GOLD, 1)])))
        else:
            show.append("execute if score @s rpg_ident matches %d run return run %s" % (n, dialog("身份", [
                t("你是", C_BODY), NL, NL, t(name, colour, True), NL, NL, t(desc, C_BODY), NL, NL,
                t("接下来，去为自己炼一身装备。", C_MUTED)], [("开始锻造", C_GOLD, 1)])))
    fn("ident/show", show)


# ---------------------------------------------------------------------------- 锻造教学
def starter_item(key, base):
    """照锻造的无档出炉函数（forge/smelt/m/<件>_<档>）改出新手版：换底材、加纹饰、[启程] 前缀、规范 Lore。"""
    import re
    src = io.open(os.path.join(FUNC, "forge", "smelt", "m", "%s_%s.mcfunction" % (key, TIER)), encoding="utf-8").read().strip()
    assert src.count("\n") == 0 and "minecraft:%s[" % base in src, key
    if key in STARTER:
        item, pattern, material = STARTER[key]
        src = src.replace("minecraft:%s[" % base, "minecraft:%s[" % item, 1)
        extra = ',trim={pattern:"minecraft:%s",material:"minecraft:%s"},tooltip_display={hidden_components:["minecraft:trim"]}' % (pattern, material)
        src = src.replace("custom_data={rpg_forged:1b}", "custom_data={rpg_forged:1b}" + extra, 1)
        assert extra in src, key
    head = 'custom_name=["",'
    assert head in src, key
    src = src.replace(head, head + J(t(STARTER_PREFIX[0], STARTER_PREFIX[1], True)) + ",", 1)
    lore, n = re.subn(r"lore=\[\[.*?\]\],custom_data=", "lore=%s,custom_data=" % J([[""] + row for row in STARTER_LORE]).replace("\\", "\\\\"), src, count=1)
    assert n == 1, key
    return lore


def tutorial():
    fn("tut/start", ["scoreboard players set @s %s %d" % (O, ST_WEAPON), "function %s/show" % P])
    fn("tut/weapon", [dialog("锻造 · 魂火冶炼", [
        t("新装备都出自魂火冶炼：器胚加上主材，投进灵魂营火，残魂决定品质抽几次。", C_BODY), NL, NL,
        t("这一次材料由我们出，炼一身铁档的装备：头盔、胸甲、护腿、战靴，再加一把武器。", C_BODY), NL, NL,
        t("武器只有一把，选一种你想用的：", C_NAME)],
        [(name, C_NAME, 20 + k) for k, (_key, name, _kind, _b) in enumerate(WEAPONS)], columns=3)])
    press = ["execute unless score #do %s matches 20..%d run return 0" % (O, 19 + len(WEAPONS)),
             "scoreboard players operation @s rpg_ob_w = #do %s" % O,
             "scoreboard players remove @s rpg_ob_w 20",
             "playsound minecraft:block.blastfurnace.fire_crackle master @s ~ ~ ~ 1 0.6",
             "playsound minecraft:block.anvil.use master @s ~ ~ ~ 0.6 0.8"]
    for key, _n, _k, _b in ARMOR:
        press.append("function %s/tut/make_%s" % (P, key))
    for k, (key, _n, _kind, _b) in enumerate(WEAPONS):
        press.append("execute if score @s rpg_ob_w matches %d run function %s/tut/make_%s" % (k, P, key))
    press += ["scoreboard players set @s %s %d" % (O, ST_MADE), "function %s/show" % P]
    fn("tut/weapon_press", press)
    for key, _n, kind, _b in FS.SMELT_TYPES:
        slot = FS.ARMOR_SLOT[key] if kind == "armor" else "off"
        fn("tut/make_" + key, [
            "# 照 rpg:forge/smelt/make 炼一件%s（不弹出物品，直接放进玩家的格子）" % _n,
            "function rpg:forge/wb/new",
            "execute store result score #r rpg_fg run random value 0..%d" % (len(FS.NAME_PREFIXES) - 1),
            "execute store result storage rpg:forge nm.r int 1 run scoreboard players get #r rpg_fg",
            "function rpg:forge/smelt/prefix with storage rpg:forge nm",
            "scoreboard players set #souls rpg_fg 1",
            "scoreboard players set #best rpg_fg -100",
            "function rpg:forge/smelt/roll",
            "scoreboard players operation #q0 rpg_fg = #best rpg_fg",
            "function %s/tut/m_%s with storage rpg:forge nm" % (P, key),
            "execute as %s run function rpg:forge/init" % WS,
            "function rpg:forge/wb/save_%s" % slot,
            "function rpg:forge/wb/close",
        ])
    for key, _n, kind, bases in FS.SMELT_TYPES:
        fn("tut/m_" + key, [starter_item(key, bases[0])])
    made = [t("魂火吞下了材料，又吐出一身装备：", C_BODY), NL, NL]
    slots = (("head", "头盔"), ("chest", "胸甲"), ("legs", "护腿"), ("feet", "战靴"), ("offhand", "武器"))
    for slot, lab in slots:
        made += [t(lab + "　", C_MUTED), "@@%s@@" % slot, NL]
    made += [NL, t("护甲已经穿在身上，武器先放在副手，教学结束后交到你的主手。", C_MUTED)]
    dlg = dialog("锻造 · 出炉", made, [("下一步：洗炼", C_GOLD, 1)])
    for slot, _lab in slots:                 # 装备名本身就是文本组件：原样塞进对话框
        dlg = dlg.replace('"@@%s@@"' % slot, "$(%s)" % slot)
    fn("tut/made_show", ["data modify storage rpg:onboard made set value {}"] + [
        'data modify storage rpg:onboard made.%s set value {text:"—"}' % slot for slot, _l in slots] + [
        'data modify storage rpg:onboard made.%s set from entity @s equipment.%s.components."minecraft:custom_name"' % (slot, slot)
        for slot, _l in slots] + ["function %s/tut/made_dlg with storage rpg:onboard made" % P])
    fn("tut/made_dlg", ["$" + dlg])
    fn("tut/to_wash", ["scoreboard players set @s %s %d" % (O, ST_WASH), "function %s/show" % P])

    # 洗炼
    fn("tut/wash", [dialog("锻造 · 洗炼", [
        t("每件装备出炉时都抽了一个品质。洗炼钻能重抽一次品质，新旧两个结果由你二选一。", C_BODY), NL, NL,
        t("平时：副手拿装备，主手拿洗炼钻右键。", C_MUTED), NL,
        t("这一次免费，对你的武器洗炼一次。", C_NAME)], [("洗炼武器", C_GOLD, 1)])])
    fn("tut/wash_roll", [
        "function rpg:forge/wb/new",
        "function rpg:forge/wb/load_off",
        "execute unless data entity %s %s.pq store result entity %s %s.pq int 1 run random value %d..%d" % (WS, EQ, WS, EQ, FS.Q_MIN, FS.Q_MAX),
        "function rpg:forge/wb/save_off",
        "function rpg:forge/wb/close",
        "playsound minecraft:block.amethyst_block.resonate master @s ~ ~ ~ 1 1.2",
        "scoreboard players set @s %s %d" % (O, ST_WASH_PICK),
        "function %s/show" % P,
    ])
    fn("tut/wash_show", [
        "function rpg:forge/wb/new",
        "function rpg:forge/wb/load_off",
        "execute store result score #q rpg_fg run data get entity %s %s.q" % (WS, EQ),
        "execute store result score #pq rpg_fg run data get entity %s %s.pq" % (WS, EQ),
        "function rpg:forge/wb/close",
    ] + grade_lines("#q", "a") + grade_lines("#pq", "b") + [
        "function %s/tut/wash_dlg with storage rpg:forge d" % P,
    ])
    fn("tut/wash_dlg", ["$" + dialog("锻造 · 洗炼", [
        t("选择要保留的品质：", C_BODY), NL, NL,
        t("原结果　", C_MUTED), t("$(an) $(as)$(a)%", C_NAME, True), NL,
        t("新结果　", C_MUTED), t("$(bn) $(bs)$(b)%", C_GOLD, True)],
        [("保留新结果", C_GOLD, 3), ("保留原结果", C_BODY, 4)])])
    fn("tut/wash_pick", [
        "execute unless score #do %s matches 3..4 run return 0" % O,
        "scoreboard players operation #do rpg_fg = #do %s" % O,
        "function rpg:forge/wb/new",
        "function rpg:forge/wb/load_off",
        "function rpg:forge/op/wash/do",
        "function rpg:forge/wb/save_off",
        "function rpg:forge/wb/close",
        "scoreboard players set @s %s %d" % (O, ST_GILD),
        "function %s/show" % P,
    ])

    # 镀金
    fn("tut/gild", [dialog("锻造 · 镀金", [
        t("镀金箔会随机挑一条附魔，等级 +1，可以超过原版上限；装备上没有附魔时，随机附上一条。每件装备只能镀一次。", C_BODY), NL, NL,
        t("平时：副手拿装备，主手拿镀金箔右键。", C_MUTED), NL,
        t("这一次免费，给你的武器镀金。", C_NAME)], [("镀金", C_GOLD, 1)])])
    fn("tut/gild_do", [
        "function rpg:forge/wb/new",
        "function rpg:forge/wb/load_off",
        "data modify storage rpg:forge e set from entity %s %s" % (WS, EQ),
        "execute unless data storage rpg:forge e{gild:1b} run function rpg:forge/op/gild/do",
        "function rpg:forge/wb/save_off",
        "function rpg:forge/wb/close",
        "scoreboard players set @s %s %d" % (O, ST_GILD_DONE),
        "function %s/show" % P,
    ])
    fn("tut/gild_show", [
        "function rpg:forge/wb/new",
        "function rpg:forge/wb/load_off",
        "data modify storage rpg:onboard g set value {k:\"\",l:0}",
        "data modify storage rpg:onboard g.k set from entity %s %s.gk" % (WS, EQ),
        "data modify storage rpg:onboard g.l set from entity %s %s.gl" % (WS, EQ),
        "function rpg:forge/wb/close",
        "execute if data storage rpg:onboard g{k:\"\"} run return run %s" % dialog("锻造 · 镀金", [
            t("这把武器附不上任何附魔，镀金没有生效。", C_WARN)], [("下一步：镶嵌", C_GOLD, 1)]),
        "function %s/tut/gild_dlg with storage rpg:onboard g" % P,
    ])
    fn("tut/gild_dlg", ["$" + dialog("锻造 · 镀金", [
        t("金箔化进了刃里：", C_BODY), NL, NL,
        {"translate": "$(k)", "color": C_GOLD, "bold": True, "italic": False}, t("  → $(l) 级", C_GOLD, True)],
        [("下一步：镶嵌", C_GOLD, 1)])])
    fn("tut/to_inlay", ["scoreboard players set @s %s %d" % (O, ST_INLAY), "function %s/show" % P])

    # 符文 / 符石
    fn("tut/inlay", [dialog("锻造 · 镶嵌", [
        t("符文是被动效果，镶进符文槽（近战与弓弩 Lv.5 开第二个槽）。", C_BODY), NL,
        t("符石是主动技能：打怪攒能量，满了按 F 释放。每件武器只能镶一枚。", C_BODY), NL, NL,
        t("平时：副手拿装备，主手拿符文或符石右键。", C_MUTED), NL,
        t("这一次免费送你一枚，二选一：", C_NAME)], [("符文", C_GOLD, 1), ("符石", C_GOLD, 2)])])
    fn("tut/inlay_press", [
        "execute if score #do %s matches 1 run scoreboard players set @s %s %d" % (O, O, ST_RUNE),
        "execute if score #do %s matches 2 run scoreboard players set @s %s %d" % (O, O, ST_STONE),
        "function %s/show" % P,
    ])
    melee = [k for k, w in enumerate(WEAPONS) if w[2] == "melee"]
    lo, hi = min(melee), max(melee)
    for part, cond in (("melee", "matches %d..%d" % (lo, hi)), ("ranged", "matches %d.." % (hi + 1))):
        runes = [(i, r) for i, r in enumerate(FS.RUNES) if r["part"] == part]
        stones = [(i, s) for i, s in enumerate(FS.STONES) if s["part"] in (part, "any")]
        rb = [t("选一枚符文：", C_BODY), NL, NL]
        for _i, r in runes:
            rb += [t("[%s] " % r["name"], FS.PART_COLOUR[part], True), t(r["text"], C_BODY), NL]
        fn("tut/runes_" + part, [dialog("锻造 · 符文", rb, [("[%s]" % r["name"], FS.PART_COLOUR[part], 30 + i) for i, r in runes]
                                        + [("返回", C_MUTED, 9)], columns=3)])
        sb = [t("选一枚符石：", C_BODY), NL, NL]
        for _i, s in stones:
            sb += [t("[%s] " % s["name"], FS.STONE_COLOUR[s["id"]], True), t(s["text"], C_BODY), NL]
        fn("tut/stones_" + part, [dialog("锻造 · 符石", sb, [("[%s]" % s["name"], FS.STONE_COLOUR[s["id"]], 50 + i) for i, s in stones]
                                         + [("返回", C_MUTED, 9)], columns=3)])
    fn("tut/runes", ["execute if score @s rpg_ob_w matches %d..%d run return run function %s/tut/runes_melee" % (lo, hi, P),
                     "function %s/tut/runes_ranged" % P])
    fn("tut/stones", ["execute if score @s rpg_ob_w matches %d..%d run return run function %s/tut/stones_melee" % (lo, hi, P),
                      "function %s/tut/stones_ranged" % P])
    rp = ["execute if score #do %s matches 9 run scoreboard players set @s %s %d" % (O, O, ST_INLAY),
          "execute if score #do %s matches 9 run return run function %s/show" % (O, P),
          "scoreboard players set #ok %s 0" % O]
    for i, r in enumerate(FS.RUNES):
        okw = "if score @s rpg_ob_w matches %d..%d" % (lo, hi) if r["part"] == "melee" else ("if score @s rpg_ob_w matches %d.." % (hi + 1) if r["part"] == "ranged" else "if score #never %s matches 1" % O)
        rp.append("execute if score #do %s matches %d %s run function %s/tut/rune_%s" % (O, 30 + i, okw, P, r["id"]))
    rp += ["execute if score #ok %s matches 1 run scoreboard players set @s %s %d" % (O, O, ST_END),
           "function %s/show" % P]
    fn("tut/rune_press", rp)
    for r in FS.RUNES:
        fn("tut/rune_" + r["id"], [
            "function rpg:forge/wb/new",
            "function rpg:forge/wb/load_off",
            "data modify storage rpg:forge e set from entity %s %s" % (WS, EQ),
            "scoreboard players set #do rpg_fg 1",
            "scoreboard players set @s rpg_fg_arg2 0",
            "function rpg:forge/op/rune/do_%s" % r["id"],
            "function rpg:forge/wb/save_off",
            "function rpg:forge/wb/close",
            "scoreboard players set #ok %s 1" % O,
        ])
    sp = ["execute if score #do %s matches 9 run scoreboard players set @s %s %d" % (O, O, ST_INLAY),
          "execute if score #do %s matches 9 run return run function %s/show" % (O, P),
          "scoreboard players set #ok %s 0" % O]
    for i, s in enumerate(FS.STONES):
        if s["part"] == "any":
            okw = ""
        elif s["part"] == "melee":
            okw = "if score @s rpg_ob_w matches %d..%d " % (lo, hi)
        else:
            okw = "if score @s rpg_ob_w matches %d.. " % (hi + 1)
        sp.append("execute if score #do %s matches %d %srun function %s/tut/stone_%s" % (O, 50 + i, okw, P, s["id"]))
    sp += ["execute if score #ok %s matches 1 run scoreboard players set @s %s %d" % (O, O, ST_END),
           "function %s/show" % P]
    fn("tut/stone_press", sp)
    for st in FS.STONES:
        fn("tut/stone_" + st["id"], [
            "function rpg:forge/wb/new",
            "function rpg:forge/wb/load_off",
            "data modify storage rpg:forge e set from entity %s %s" % (WS, EQ),
            "scoreboard players set #do rpg_fg 1",
            "function rpg:forge/op/stone/do_%s" % st["id"],
            "function rpg:forge/wb/save_off",
            "function rpg:forge/wb/close",
            "scoreboard players set #ok %s 1" % O,
        ])

    fn("tut/end", [dialog("锻造 · 完成", [
        t("这一身装备是你的了。", C_NAME, True), NL, NL,
        t("以后要冶炼新装备，需要一堆", C_BODY), t("灵魂营火", C_GOLD, True),
        t("（普通营火不行）：主手拿器胚，对准灵魂营火右键，备好主材与残魂。", C_BODY), NL, NL,
        t("洗炼钻、镀金箔、符文、符石：副手拿装备，主手拿材料右键。", C_BODY), NL, NL,
        t("器胚与残魂从怪物身上掉落。", C_MUTED)], [("进入破碎大陆", C_GOLD, 1)])])


# ---------------------------------------------------------------------------- 结束
def finish():
    fn("finish", pid_macro([
        "# 教学完成：回到出生的位置，武器交到主手",
        "scoreboard players set @s %s %d" % (O, ST_DONE),
        "tag @s remove rpg.ob",
        "tag @s remove rpg.ob.hold",
        "tag @s remove rpg.ob.wait",
        "execute if entity @s[tag=rpg.ob.intro] run function %s/intro/stop" % P,
        "function %s/music/stop" % P,
        "effect clear @s",
        "gamemode survival @s",
        "execute if score @s rpg_ob_gm matches 1 run gamemode creative @s",
        "execute if score @s rpg_ob_gm matches 2 run gamemode adventure @s",
        "scoreboard players set @s rpg_ob_v 1",
        "function %s/back with storage rpg:onboard tmp" % P,
        "# 教学装备：格子原来空着就留在身上（武器进主手）；原来有东西的，教学装备掉在脚边，原物还回格子",
        "execute at @s run function %s/stash/take with storage rpg:onboard tmp" % P,
        "function %s/welcome with storage rpg:onboard tmp" % P,
        "playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.8 1",
    ]))
    fn("back", ["$function %s/back_m with storage rpg:onboard p$(id)" % P])
    fn("back_m", ["$execute in $(dim) run tp @s $(x) $(y) $(z)"])
    fn("welcome", ["$function %s/welcome_m with storage rpg:onboard p$(id)" % P])
    fn("welcome_m", [
        "title @s times 10 70 20",
        "$title @s subtitle %s" % J(t("$(given)$(mid)·$(house)　·　$(nation)", C_BODY, italic=True)),
        "$title @s title %s" % J(t("欢迎，$(nick)", C_GOLD, True)),
    ])
    fn("skip", ["# 不发装备，直接结束流程（as 玩家）", "function %s/finish" % P])


# ---------------------------------------------------------------------------- 老玩家的装备
STASH = (("head", "armor.head"), ("chest", "armor.chest"), ("legs", "armor.legs"), ("feet", "armor.feet"),
         ("off", "weapon.offhand"), ("main", "weapon.mainhand"))
TMP = "@e[type=minecraft:item_display,tag=rpg.ob.tmp,distance=..3,limit=1]"


def stash():
    """所有人都要走教学（用户 2026-11-23），老玩家身上已经穿戴的东西先收进 storage，结束时还回去。"""
    put = ["# 开局（as/at 玩家，宏 id）：护甲四格、副手、主手有东西就收起来，格子清空",
           "summon minecraft:item_display ~ ~ ~ {Tags:[\"rpg.ob.tmp\"]}"]
    for key, slot in STASH:
        put += ["execute if items entity @s %s * run item replace entity %s contents from entity @s %s" % (slot, TMP, slot),
                "$execute if items entity @s %s * run data modify storage rpg:onboard p$(id).stash.%s set from entity %s item" % (slot, key, TMP),
                "execute if items entity @s %s * run item replace entity @s %s with minecraft:air" % (slot, slot)]
    put.append("kill %s" % TMP)
    fn("stash/put", put)
    take = ["# 结束（as/at 玩家，宏 id）",
            "summon minecraft:item_display ~ ~ ~ {Tags:[\"rpg.ob.tmp\"]}"]
    for key, slot in STASH[:4]:
        take += ["$execute if data storage rpg:onboard p$(id).stash.%s if items entity @s %s * run function %s/stash/drop_%s" % (key, slot, P, key),
                 "$execute if data storage rpg:onboard p$(id).stash.%s run function %s/stash/back_%s with storage rpg:onboard tmp" % (key, P, key)]
    take += ["# 教学武器在副手：主手原来空着就交到主手，否则掉在脚边",
             "$execute if data storage rpg:onboard p$(id).stash.main if items entity @s weapon.offhand * run function %s/stash/drop_off" % P,
             "$execute unless data storage rpg:onboard p$(id).stash.main run item replace entity @s weapon.mainhand from entity @s weapon.offhand",
             "$execute unless data storage rpg:onboard p$(id).stash.main run item replace entity @s weapon.offhand with minecraft:air",
             "$execute if data storage rpg:onboard p$(id).stash.main run function %s/stash/back_main with storage rpg:onboard tmp" % P,
             "$execute if data storage rpg:onboard p$(id).stash.off if items entity @s weapon.offhand * run function %s/stash/drop_off" % P,
             "$execute if data storage rpg:onboard p$(id).stash.off run function %s/stash/back_off with storage rpg:onboard tmp" % P,
             "$data remove storage rpg:onboard p$(id).stash",
             "kill %s" % TMP]
    fn("stash/take", take)
    for key, slot in STASH:
        fn("stash/drop_" + key, [
            "summon minecraft:item ~ ~0.3 ~ {Item:{id:\"minecraft:stone\",count:1},PickupDelay:0,Tags:[\"rpg.ob.drop\"]}",
            "item replace entity @e[type=minecraft:item,tag=rpg.ob.drop,distance=..2,limit=1] contents from entity @s %s" % slot,
            "tag @e[type=minecraft:item,tag=rpg.ob.drop] remove rpg.ob.drop",
            "item replace entity @s %s with minecraft:air" % slot,
        ])
        fn("stash/back_" + key, [
            "$data modify entity %s item set from storage rpg:onboard p$(id).stash.%s" % (TMP, key),
            "item replace entity @s %s from entity %s contents" % (slot, TMP),
        ])


# ---------------------------------------------------------------------------- 面板一行 + 管理员
def panel_and_admin():
    names = {n: (name, colour) for n, _k, name, colour, _d in S.IDENTITIES}
    lines = ["# 「序章」按钮：任何人随时可以进（用户 2026-11-23）",
             "execute unless entity @s[tag=rpg.pr] run data modify storage rpg:panel ui.actions append value %s" % J(
                 {"label": {"text": "序章", "color": ui.BROADCAST_HOLY, "bold": True, "italic": False},
                  "action": {"type": "minecraft:run_command", "command": "/trigger rpg_pro_go set 1"}}),
             "execute unless score @s rpg_ident matches 1.. run return 0",
             "execute store result storage rpg:onboard tmp.id int 1 run scoreboard players get @s rpg_fg_id",
             "data modify storage rpg:onboard tmp.i set value {n:\"\",c:\"#FFFFFF\"}"]
    for n, (name, colour) in names.items():
        lines.append("execute if score @s rpg_ident matches %d run data modify storage rpg:onboard tmp.i set value {n:\"%s\",c:\"%s\"}" % (n, name, colour))
    for p in ui.PILLARS:
        lines.append("execute if score @s rpg_ident matches 4 if score @s rpg_ident_sin matches %d run data modify storage rpg:onboard tmp.i set value {n:\"七大罪之仆 · %s之%s\",c:\"%s\"}"
                     % (p["n"], p["who"], p["sin"], p["lit"]))
    lines += ["data modify storage rpg:onboard tmp.i.id set from storage rpg:onboard tmp.id",
              "function %s/panel_m with storage rpg:onboard tmp.i" % P]
    fn("panel", lines)
    # 身份名与颜色要和玩家记录一起进宏：先并到一起
    fn("panel_m", ["$data modify storage rpg:onboard tmp.row set from storage rpg:onboard p$(id)",
                   "$data modify storage rpg:onboard tmp.row.in set value \"$(n)\"",
                   "$data modify storage rpg:onboard tmp.row.ic set value \"$(c)\"",
                   "function %s/panel_line with storage rpg:onboard tmp.row" % P])
    fn("panel_line", ["$data modify storage rpg:panel ui.body append value %s" % J(
        ["", t("身份 ", "#9C9A94"), {"text": "$(in)", "color": "$(ic)", "bold": True, "italic": False},
         t("　$(given)$(mid)·$(house)", C_NAME), t("　$(nation)", "#9C9A94"), t("\n")])])
    fn("admin/new", [
        "# 把自己当新人重走一遍（管理员）；旁白放到一半也从头来",
        "execute if entity @s[tag=rpg.ob.intro] run function %s/intro/stop" % P,
        "function %s/admin/release" % P,
        "scoreboard players reset @s rpg_ident",
        "scoreboard players reset @s rpg_ident_sin",
        "scoreboard players reset @s rpg_messiah",
        "scoreboard players reset @s rpg_pr_done",
        "scoreboard players reset @s rpg_ob_v",
        "# 力跟着身份走：重抽身份时一起重分（add_sephira.py）",
        "scoreboard players reset @s rpg_force",
        "tag @s remove rpg.fallen",
        "tag @s remove rpg.ob.hold",
        "tag @s remove rpg.ob.wait",
        "tag @s remove rpg.ob.queued",
        "function %s/begin" % P,
    ])
    fn("admin/release", ["# 自己占着的唯一身份放回池子"] + [
        "execute if score @s rpg_ident matches %d run data remove storage rpg:onboard taken.%s" % (n, k)
        for n, k, _a, _b, _c in S.IDENTITIES if k in S.UNIQUE])
    fn("admin/skip", ["execute unless entity @s[tag=rpg.ob] run return 0", "function %s/finish" % P])
    fn("admin/free_unique", ["data remove storage rpg:onboard taken", "tellraw @s %s" % J(t("[破碎大陆] 圣子、圣灵、弥赛亚已放回池子", C_GOLD))])


# ---------------------------------------------------------------------------- 接到别的模块上
def patch(rel, guard, text, where="top"):
    path = os.path.join(FUNC, rel)
    s = io.open(path, encoding="utf-8").read()
    if guard in s:
        return
    if where == "top":
        s = text + s
    elif where == "end":
        s = s.rstrip("\n") + "\n" + text
    else:
        assert where in s, "%s 里找不到 %r" % (rel, where)
        s = s.replace(where, text + where, 1)
    io.open(path, "w", encoding="utf-8", newline="\n").write(s)


def wire():
    hook_tag(DP, "load", P + "/load", False)
    hook_tag(DP, "tick", P + "/tick", True)
    g = "rpg:onboard/pro/after"
    patch("prologue/iso/restore.mcfunction", g,
          "# 新手开局：序章之后进黑屏欢迎页（add_onboard.py）\nexecute if entity @s[tag=rpg.ob] run function %s\n" % g, "end")
    patch("hud/hud.mcfunction", "rpg.ob.hold",
          "# 新手开局的黑屏里不画状态栏（add_onboard.py）\nexecute if entity @s[tag=rpg.ob.hold] run return 0\n")
    patch("taint/step.mcfunction", "rpg.ob.hold",
          "# 新手开局的黑屏里不结算魔化（add_onboard.py）\nexecute if entity @s[tag=rpg.ob.hold] run return 0\n")
    patch("panel/open.mcfunction", "rpg:onboard/panel",
          "function rpg:onboard/panel\n", "function rpg:panel/ui/show")


def main():
    import shutil
    shutil.rmtree(OUT, ignore_errors=True)       # 重新生成，旧文件不留
    core()
    hold()
    intro()
    music()
    prologue()
    show_and_press()
    name()
    card()
    identity()
    tutorial()
    finish()
    stash()
    panel_and_admin()
    wire()
    print("onboard: %d functions" % COUNT)


if __name__ == "__main__":
    main()
