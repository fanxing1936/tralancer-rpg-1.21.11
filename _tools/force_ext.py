# -*- coding: utf-8 -*-
"""力与技能 · 第二部分（里程碑 B 第 7、8 步 + 里程碑 A 的三处遗留）。由 add_force.py 在最后调用：

  * 王冠终式：第 10 阶自动习得、不花点，单级，可放进对应那棵树的槽。
      圣力「哈利路亚」；圣子换成「审判」，圣灵换成「复活」（60 秒内倒下的队友，每 10 分钟一次）。
      魔力「堕天」；七大罪之仆换成本柱领主终式（晨星坠落 / 海渊回卷 / 无底坑 / 蝇王之宴 / 毒龙之怒 / 无主之契 / 金之枷）。
  * Boss 传承技：六本书，首杀必掉、之后每次 20%；读了就会，不占技能点，两棵树的槽都能放，按放进的那棵树付代价。
  * 身份能力（美丽阶起数值翻倍）：无知者阅历 +20% 与恶魔负面效果 −30%；边缘者空缺者 6 格显形、魔力技能冷却 −10%；
    神职者生命力 −30%（在 add_force.pay/h）；七罪之仆的罪性被动与本柱契约魔化减半；圣子对恶魔与亡灵 +25%；
    圣灵保惠师光环；弥赛亚特质：教皇的「收回契约」不来、每 20 分钟一次「第三日」。
  * 里程碑 A 遗留：严厉柱第 6 阶对 Boss +5%；燃尽时圣器保护失效；同化 50 起圣器保护减半（隔刻失效）。
  * Codex 的图（force_ref/art）：圣徽 / 罪印图标，圣链（6 帧）、断罪印天平（4 帧循环）、深渊之口（6 帧循环）。
"""
import io
import json
import os
import sys

import add_michael_fx_art as mart
import boss_fx
import rpg_ui_style as ui

F = None          # add_force 模块
P = O = None
HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "force_ref", "art")
VFX = "rpg:force_vfx/"

BOSS_NAME = {"pope": ("教皇", "#E8D9A8"), "usurper": ("篡夺者", "#E8E0F0"), "jacques": ("雅克", "#D8D2C4"),
             "saul": ("扫罗", "#B8A0A0"), "michael": ("米迦勒", "#FFE9A8"), "lucifer": ("路西法", "#5FD68C")}
LORD_FIN = {1: ("晨星坠落", "身后展开光翼，前方 30 格一线贯穿，伤害 16"),
            2: ("海渊回卷", "把 10 格内敌人卷到身边并缠住 3 秒，伤害 6（Boss 只受伤害）"),
            3: ("无底坑", "脚下开坑 6 秒：5 格内的敌人缓慢下陷，每秒 3 点伤害"),
            4: ("蝇王之宴", "蝇群 5 秒吞噬 8 格内的敌人，每秒 3 点伤害，按吞到的敌人回血"),
            5: ("毒龙之怒", "10 秒内每次受伤都向 4 格内反喷毒焰，伤害 4 并中毒"),
            6: ("无主之契", "魅惑准星上一个非 Boss 敌人为你作战 15 秒"),
            7: ("金之枷", "把准星目标铸成金像 3 秒，碎时 3 格内溅射伤害 10")}
POSITIVE = ["strength", "speed", "resistance", "regeneration", "absorption", "fire_resistance", "invisibility",
            "jump_boost", "haste", "health_boost"]
NEG_CUT = ["poison", "wither", "slowness", "weakness", "blindness", "nausea", "hunger", "mining_fatigue", "darkness",
           "levitation"]


def fn(name, lines):
    F.fn("x/" + name, lines)


def X(name):
    return "%s/x/%s" % (P, name)


def t(*a, **k):
    return F.t(*a, **k)


def say(parts):
    return F.say(parts)


def fail(m):
    return "function %s/fail/say {m:\"%s\"}" % (P, m)


def sef5(lines5, lines1):
    """美丽阶起换成 lines5，之前 lines1（数值翻倍）。"""
    return (["execute unless score @s rpg_sef matches 5.. run " + l for l in lines1] +
            ["execute if score @s rpg_sef matches 5.. run " + l for l in lines5])


# ============================================================================ 特效引擎
def engines():
    kinds = {"fade": dict(life=8, steps=[(4, 4, boss_fx.sc(0.01))]),
             "fadel": dict(life=16, steps=[(8, 8, boss_fx.sc(0.01))]),
             "burstf": dict(life=16, frames=("glyph", "burstf", 8, 2)),
             "eyeopen": dict(life=14, frames=("glyph", "eye", 6, 2)),
             "wings": dict(life=14, frames=("glyph", "wings", 6, 2)),
             "halo": dict(life=24, loop=("glyph", "halo", 6, 2)),
             "doverise": dict(life=40, loop=("glyph", "dove", 8, 2), steps=[(38, 36, "translation:[0f,6f,0f]")]),
             "mshock": dict(life=16, frames=("item", "rpg:michael_vfx/shock", 8, 2)),
             "mshockh": dict(life=16, frames=("item", "rpg:michael_vfx/shockh", 8, 2)),
             "chainv": dict(life=60, steps=[(59, 4, "scale:[1f,2.6f,1f]"), (6, 5, boss_fx.sc(0.01))]),
             "voidx": dict(life=80, frames=("item", VFX + "maw", 6, 3), steps=[(8, 7, boss_fx.flat_sc(0.01))])}
    w = lambda pre: (lambda path, lines: F.fn("x/" + pre + "/" + path, lines))
    xh = boss_fx.Fx(fn=P + "/x/h", tag="rpg.fo.xh", life="rpg_fo_life", kind="rpg_fo_kd", writer=w("h"),
                    kinds=kinds, arts=[(mart, mart.FONT)])
    xm = boss_fx.Fx(fn=P + "/x/m", tag="rpg.fo.xm", life="rpg_fo_life", kind="rpg_fo_kd", writer=w("m"),
                    kinds={"fade": kinds["fade"]})
    return xh, xm


def ride(lines):
    """把刚生成的特效挂到 @s 身上（跟着目标走），再出生。"""
    return [lines[0], "ride @e[tag=rpg.fo.xhnew,limit=1] mount @s"] + lines[1:]


# ============================================================================ Codex 的图
def art(rp):
    from PIL import Image
    if not rp or not os.path.isdir(ART):
        return 0
    tex = os.path.join(rp, "assets", "rpg", "textures", "item")
    n = 0

    def wj(path, doc):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(doc, fh, ensure_ascii=False, indent=2)

    def clean(im, size):
        im = im.convert("RGBA").resize((size, size), Image.NEAREST)
        px = im.load()
        for y in range(size):
            for x in range(size):
                r, g, b, a = px[x, y]
                px[x, y] = (r, g, b, 255) if a >= 128 else (0, 0, 0, 0)
        return im

    D = os.path.join(ART, "dungeons")

    def pad16(name, box=None, at=None):
        im = Image.open(os.path.join(D, name + ".png")).convert("RGBA")
        if box:
            im = im.crop(box)
        out = Image.new("RGBA", (16, 16))
        out.paste(im, at if at else ((16 - im.width) // 2, (16 - im.height) // 2))
        return out

    # 圣徽 / 罪印：16×16 手持物（绘图会话按地下城原图重绘的那两张）
    for key in ("holy_sigil", "sin_sigil"):
        src = os.path.join(ART, key + ".png")
        if not os.path.exists(src):
            continue
        dd = os.path.join(tex, "force")
        os.makedirs(dd, exist_ok=True)
        clean(Image.open(src), 16).save(os.path.join(dd, key + ".png"))
        wj(os.path.join(rp, "assets", "rpg", "models", "force", key + ".json"),
           {"parent": "minecraft:item/handheld", "textures": {"layer0": "rpg:item/force/" + key}})
        wj(os.path.join(rp, "assets", "rpg", "items", "force", key + ".json"),
           {"model": {"type": "minecraft:model", "model": "rpg:force/" + key}})
        n += 1
    d = os.path.join(tex, "force_vfx")
    os.makedirs(d, exist_ok=True)

    def item(name, model):
        wj(os.path.join(rp, "assets", "rpg", "models", "force_vfx", name + ".json"), model)
        wj(os.path.join(rp, "assets", "rpg", "items", "force_vfx", name + ".json"), {
            "model": {"type": "minecraft:model", "model": "rpg:force_vfx/" + name,
                      "tints": [{"type": "minecraft:custom_model_data", "index": 0, "default": 16777215}]}})

    face = {"uv": [0, 0, 16, 16], "texture": "#0", "tintindex": 0}

    def upright(tx):
        return {"textures": {"0": tx, "particle": tx},
                "elements": [{"from": [0, 0, 8], "to": [16, 16, 8], "shade": False, "light_emission": 15,
                              "faces": {"north": dict(face), "south": dict(face)}}]}

    # 以下全用地下城原包的图（用户 2026-11-23「找 codex 从地下城找到的文件使用」），只补透明边，不重画
    # 圣链：原色金链 T_Gold_Chain（链条在最左 5 列），居中成一股竖链
    pad16("T_Gold_Chain", box=(0, 0, 5, 16)).save(os.path.join(d, "chain.png"))
    item("chain", upright("rpg:item/force_vfx/chain"))
    # 断罪印：伤害光环的目标标记 T_DamageAuraTarget（四角括号），白图运行时染金
    pad16("T_DamageAuraTarget").save(os.path.join(d, "brand.png"))
    item("brand", upright("rpg:item/force_vfx/brand"))
    # 深渊之口：紫黑虚空扩散图集的前 6 格 + 完整像素螺旋
    sheet = Image.open(os.path.join(D, "T_Circle_Full_Void_15_spritesheet.png")).convert("RGBA")
    for i, (x, y) in enumerate([(0, 0), (16, 0), (32, 0), (48, 0), (0, 16), (16, 16)]):
        sheet.crop((x, y, x + 16, y + 16)).save(os.path.join(d, "maw_%d.png" % i))
        item("maw_%d" % i, mart.plane_model("rpg:item/force_vfx/maw_%d" % i))
    pad16("T_PixelSpiral").save(os.path.join(d, "spiral.png"))
    item("spiral", mart.plane_model("rpg:item/force_vfx/spiral"))
    return n + 9


# ============================================================================ 记分项与每刻
def core():
    objs = ["rpg_fo_cr", "rpg_fo_tk", "rpg_fo_wr", "rpg_fo_fe", "rpg_fo_ws", "rpg_fo_wt", "rpg_fo_px", "rpg_fo_pz",
            "rpg_fo_st", "rpg_fo_xl", "rpg_fo_xa", "rpg_fo_dn", "rpg_fo_3d", "rpg_fo_ai"]
    F.add_lines("load", ["scoreboard objectives add %s dummy" % o for o in objs] + [
        "scoreboard objectives add rpg_fo_d2 minecraft.custom:minecraft.damage_dealt",
        "scoreboard objectives add rpg_fo_dt minecraft.custom:minecraft.damage_taken",
        "scoreboard objectives add rpg_fo_dw minecraft.custom:minecraft.damage_taken",
        "scoreboard objectives add rpg_fo_kl minecraft.custom:minecraft.mob_kills",
        "scoreboard objectives add rpg_fo_die deathCount",
        "scoreboard players set #40 %s 40" % O,
    ])
    F.add_lines("tick", [
        "execute as @a[scores={rpg_fo_d2=1..}] at @s run function %s" % X("id/dealt"),
        "execute as @a[scores={rpg_fo_tk=1..}] at @s run function %s" % X("l/saul_tick"),
        "execute as @a[scores={rpg_fo_wr=1..}] at @s run function %s" % X("f/wrath_tick"),
        "execute as @a[scores={rpg_fo_fl=1..}] at @s run function %s" % X("f/fall_tick"),
        "execute as @e[tag=rpg.fo.gd] at @s run function %s" % X("f/gild_tick"),
        "execute as @e[tag=rpg.fo.xh] at @s run function %s" % X("h/fx/tick"),
        "execute as @e[tag=rpg.fo.xm] at @s run function %s" % X("m/fx/tick"),
    ], before="scoreboard players operation #m")
    F.add_lines("tick", [
        "execute as @e[tag=rpg.fo.ch] at @s run function %s" % X("f/charm_sec"),
        "execute as @a[scores={rpg_fo_fe=1..}] at @s run function %s" % X("f/feast_sec"),
    ])
    F.add_lines("sec", ["function %s" % X("id/sec")])


# ============================================================================ 技能页：王冠 · 传承
def pages():
    fill = ["# 终式名随身份换；传承技与终式的颜色、状态",
            "data modify storage rpg:force p.n25 set value \"哈利路亚\"",
            "execute if score @s rpg_ident matches 5 run data modify storage rpg:force p.n25 set value \"审判\"",
            "execute if score @s rpg_ident matches 6 run data modify storage rpg:force p.n25 set value \"复活\"",
            "data modify storage rpg:force p.d25 set value \"%s\"" % F.EX[25][3],
            "execute if score @s rpg_ident matches 5 run data modify storage rpg:force p.d25 set value \"前方 20 格大范围圣光，伤害 18（对恶魔与亡灵 ×1.5）\"",
            "execute if score @s rpg_ident matches 6 run data modify storage rpg:force p.d25 set value \"把 60 秒内倒下的一名队友拉回身边，半血复生（冷却 10 分钟）\"",
            "data modify storage rpg:force p.n26 set value \"堕天\"",
            "data modify storage rpg:force p.d26 set value \"%s\"" % F.EX[26][3]]
    for k, (nm, desc) in LORD_FIN.items():
        fill += ["execute if score @s rpg_ident matches 4 if score @s rpg_ident_sin matches %d run data modify storage rpg:force p.n26 set value \"%s\"" % (k, nm),
                 "execute if score @s rpg_ident matches 4 if score @s rpg_ident_sin matches %d run data modify storage rpg:force p.d26 set value \"%s\"" % (k, desc)]
    for n, kind, name, desc, fc, xc, cd, boss in F.EXTRA:
        if kind == "l":
            fill.append("data modify storage rpg:force p.n%d set value \"%s\"" % (n, name))
        fill += ["scoreboard players add @s %s 0" % F.kk(n),
                 "data modify storage rpg:force p.c%d set value \"%s\"" % (n, F.C_LOCK),
                 "data modify storage rpg:force p.l%d set value \"未习得\"" % n,
                 "execute if score @s %s matches 1.. run data modify storage rpg:force p.c%d set value \"%s\"" % (F.kk(n), n, F.C_GOLD),
                 "execute if score @s %s matches 1.. run data modify storage rpg:force p.l%d set value \"已习得\"" % (F.kk(n), n)]
    fn("page/fill", fill)

    press = []
    for tr in (1, 2):
        tname, tcol, item = F.TREES[tr]
        sl = "h" if tr == 1 else "m"
        fin = 25 if tr == 1 else 26
        rows = [fin] + [e[0] for e in F.EXTRA if e[1] == "l"]
        body = [t("技能点 ", F.C_MUTED), t("$(sp)", F.C_GOLD, True),
                t("　　%s的槽　Ⅰ " % item, F.C_MUTED), t("$(%s1)" % sl, tcol), t("　Ⅱ ", F.C_MUTED), t("$(%s2)" % sl, tcol),
                t("　Ⅲ ", F.C_MUTED), t("$(%s3)" % sl, tcol), F.NL,
                t("终式在王冠阶（第 10 阶）自动习得；传承技读 Boss 掉的传承书学会。都不花技能点。", "#797979"), F.NL]
        actions = []
        for n in rows:
            _n, kind, name, desc, fc, xc, cd, boss = F.EX[n]
            if kind == "l":
                bz, bcol = BOSS_NAME[boss]
                src = "击败%s掉落（首杀必掉，之后 20%%）" % bz
                cost = "力 %d · 圣徽付生命力 %d / 罪印付魔化 +%d · 冷却 %d 秒" % (fc, xc, xc, cd)
            else:
                src = "王冠阶自动习得"
                cost = ("力 %d · 生命力 %d · 冷却 %d 秒" % (fc, xc, cd)) if kind == "h" else ("力 %d · 冷却 %d 秒" % (fc, cd))
            body += [F.NL, {"text": "$(n%d)" % n, "color": "$(c%d)" % n, "bold": True, "italic": False},
                     t("  $(l%d)" % n, F.C_MUTED), t("　" + src, "#797979"), F.NL,
                     {"text": "$(d%d)" % n if kind != "l" else desc, "color": F.C_BODY, "italic": False}, F.NL,
                     t(cost, "#797979"), F.NL]
            actions.append({"label": {"text": "$(n%d) · $(l%d)" % (n, n), "color": "$(c%d)" % n, "bold": True, "italic": False},
                            "tooltip": t(src, F.C_MUTED), "width": 150, "action": F.trig(10 + tr)})
            for s in (1, 2, 3):
                code = (2000 if tr == 1 else 3000) + n * 10 + s
                actions.append({"label": t(F.ROMAN[s], tcol, True), "tooltip": t("放进%s的 %s 号槽" % (item, F.ROMAN[s]), F.C_MUTED),
                                "width": 74, "action": F.trig(code)})
                press.append("execute if score #do %s matches %d run return run function %s" % (O, code, X("slot/%s%d_%d" % (sl, n, s))))
                slot_fn(tr, n, s)
        actions += [{"label": t("圣力树", F.C_HOLY, True), "width": 150, "action": F.trig(1)},
                    {"label": t("魔力树", F.C_MANA, True), "width": 74, "action": F.trig(4)},
                    {"label": t("放进%s" % F.TREES[3 - tr][2], F.TREES[3 - tr][1], True), "width": 74, "action": F.trig(13 - tr)},
                    {"label": t("返回原质", F.C_GOLD, True), "width": 74,
                     "action": {"type": "minecraft:run_command", "command": "/trigger rpg_sef_do set 20"}}]
        doc = {"type": "minecraft:multi_action",
               "title": ["", t("技能 · ", F.C_MUTED), t("王冠 · 传承", F.C_GOLD, True), t("（放进%s的槽）" % item, F.C_MUTED)],
               "body": {"type": "minecraft:plain_message", "width": 330, "contents": [""] + body},
               "actions": actions, "columns": 4, "can_close_with_escape": True, "pause": False,
               "after_action": "close", "exit_action": {"label": t("合上", F.C_MUTED)}}
        F.fn("page/p%d" % (6 + tr), ["$dialog show @s " + F.J(doc)])
    fn("press", press)


def slot_fn(tr, n, s):
    sl = "h" if tr == 1 else "m"
    name = F.EX[n][2]
    fn("slot/%s%d_%d" % (sl, n, s), [
        "execute unless score @s %s matches 1.. run return run %s" % (F.kk(n), fail("还没习得「%s」" % name if n > 26 else "终式要到王冠阶（第 10 阶）")),
        "execute %s run return run %s" % (F.tree_ok(tr), fail("你没有%s" % F.TREES[tr][0]))] +
        ["execute if score @s %s matches %d run scoreboard players set @s %s 0" % (F.slot_obj(tr, s2), n, F.slot_obj(tr, s2)) for s2 in (1, 2, 3) if s2 != s] +
        ["scoreboard players set @s %s %d" % (F.slot_obj(tr, s), n),
         "playsound minecraft:ui.button.click player @s ~ ~ ~ 0.6 1.4"])


def autoslot(tr, n):
    return ["execute unless score @s %s matches 1.. run return run scoreboard players set @s %s %d" % (F.slot_obj(tr, s), F.slot_obj(tr, s), n)
            for s in (1, 2, 3)]


# ============================================================================ 施放：终式与传承技的 try
def tries():
    for n, kind, name, desc, fc, xc, cd, boss in F.EXTRA:
        L = ["# %s（as/at 施放者，#tree 是放它的那棵树）" % name,
             "execute unless score @s %s matches 1.. run return run %s" % (F.kk(n), fail("终式要到王冠阶（第 10 阶）") if n < 30 else fail("还没习得「%s」" % name))]
        cool = "execute if score @s %s > #now %s run " % (F.kc(n), O)
        L += [cool + "scoreboard players operation #s %s = @s %s" % (O, F.kc(n)),
              cool + "scoreboard players operation #s %s -= #now %s" % (O, O),
              cool + "scoreboard players add #s %s 19" % O,
              cool + "scoreboard players operation #s %s /= #20 %s" % (O, O),
              cool + "return run function %s/cd_say" % P]
        if n == 25:
            L += ["tag @s add rpg.fo.self",
                  "scoreboard players set #ok %s 1" % O,
                  "execute if score @s rpg_ident matches 6 unless entity @e[type=minecraft:player,tag=rpg.fo.down,tag=!rpg.fo.self] run scoreboard players set #ok %s 0" % O,
                  "tag @s remove rpg.fo.self",
                  "execute unless score #ok %s matches 1 run return run %s" % (O, fail("没有 60 秒内倒下的队友可以复活"))]
        L.append("scoreboard players set #fc %s %d" % (O, fc))
        if kind == "h":
            L += ["scoreboard players set #vc %s %d" % (O, xc * 10), "function %s/pay/h" % P]
        elif kind == "m":
            L += ["scoreboard players set #xc %s %d" % (O, xc),
                  "execute if score @s rpg_ident matches 4 run scoreboard players set #xc %s 8" % O,
                  "function %s/pay/m" % P]
        else:
            L += ["scoreboard players set #vc %s %d" % (O, xc * 10), "scoreboard players set #xc %s %d" % (O, xc),
                  "scoreboard players set #ok %s 0" % O,
                  "execute if score #tree %s matches 1 run function %s/pay/h" % (O, P),
                  "execute if score #tree %s matches 2 run function %s/pay/m" % (O, P)]
        L += ["execute unless score #ok %s matches 1 run return 0" % O,
              "scoreboard players set #c %s %d" % (O, cd * 20)]
        if n == 25:
            L.append("execute if score @s rpg_ident matches 6 run scoreboard players set #c %s 12000" % O)
        L += ["function %s/pay/cd" % P,
              "scoreboard players operation @s %s = #now %s" % (F.kc(n), O),
              "scoreboard players operation @s %s += #c %s" % (F.kc(n), O),
              "tag @s add rpg.fo.me",
              "function %s/sk/%d/do" % (P, n),
              "tag @s remove rpg.fo.me"]
        F.fn("sk/%d/try" % n, L)


# ============================================================================ 终式
def finishers(xh, xm):
    hit = "function %s/hit" % P
    E, NB = F.ENEMY, F.NOBOSS
    F.fn("sk/25/do", [
        "execute if score @s rpg_ident matches 5 run return run function %s" % X("f/judge"),
        "execute if score @s rpg_ident matches 6 run return run function %s" % X("f/revive"),
        "function %s" % X("f/hallelujah"),
    ])
    F.fn("sk/26/do", ["execute if score @s rpg_ident matches 4 if score @s rpg_ident_sin matches %d run return run function %s" % (k, X("f/lord%d" % k))
                      for k in LORD_FIN] + ["function %s" % X("f/fall")])
    # 哈利路亚
    fn("f/hallelujah", [
        "playsound minecraft:block.beacon.activate player @a[distance=..32] ~ ~ ~ 1.5 1.3",
        "playsound minecraft:block.bell.resonate player @a[distance=..32] ~ ~ ~ 1 1.6",
        "playsound minecraft:ui.toast.challenge_complete player @a[distance=..32] ~ ~ ~ 0.6 1.6",
        "particle minecraft:end_rod ~ ~1 ~ 6 1.5 6 0.05 200",
        "scoreboard players set #dmg %s 160" % O, "scoreboard players set #hm %s 15" % O,
        "execute as @e[%s,distance=..12] at @s run function %s" % (E, X("f/hal_one")),
        "effect give @a[distance=..12,gamemode=!spectator] minecraft:instant_health 1 3 true",
        "effect give @a[distance=..12,gamemode=!spectator] minecraft:regeneration 6 1 true",
        "execute as @a[distance=..12,gamemode=!spectator] at @s run function %s" % X("f/hal_ally"),
    ] + xh.decal("rpg:michael_vfx/shockh_0", 26, 0xFFFFFF, kind="mshockh") +
        xh.glyph("wings", 3.2, "white", pos="^ ^1.6 ^-1.8", kind="wings") +
        xh.glyph("burst", 3.0, "white", pos="^ ^2.4 ^4.5", kind="burst"))
    fn("f/hal_one", [hit, "particle minecraft:end_rod ~ ~1 ~ 0.2 0.8 0.2 0.1 12"] +
       xh.glyph("ray", 1.6, "white", pos="~ ~1 ~", kind="fadel", billboard="vertical"))
    fn("f/hal_ally", xh.glyph("halo", 1.1, "white", pos="~ ~2.3 ~", kind="halo"))
    # 审判（圣子）：前方锥形
    judge = ["playsound minecraft:item.trident.thunder player @a[distance=..32] ~ ~ ~ 1 1.4",
             "playsound minecraft:block.beacon.power_select player @a[distance=..32] ~ ~ ~ 1 0.8",
             "scoreboard players set #dmg %s 180" % O, "scoreboard players set #hm %s 15" % O]
    for k, r in ((3, 2.0), (6, 2.8), (9, 3.6), (12, 4.4), (15, 5.2), (18, 6.0)):
        judge.append("execute positioned ^ ^ ^%d run tag @e[%s,distance=..%s] add rpg.fo.jd" % (k, E, r))
        judge.append("particle minecraft:end_rod ^ ^1.2 ^%d %s 0.6 %s 0.02 %d" % (k, r / 2, r / 2, 12 + k * 2))
    judge += ["execute as @e[tag=rpg.fo.jd] at @s run function %s" % X("f/hal_one"),
              "tag @e[tag=rpg.fo.jd] remove rpg.fo.jd"]
    judge += xh.decal("rpg:michael_vfx/shockh_0", 16, 0xFFFFFF, pos="^ ^0.06 ^8", kind="mshockh")
    judge += xh.glyph("burst", 4.0, "white", pos="^ ^1.8 ^7", kind="burst")
    fn("f/judge", judge)
    # 复活（圣灵）
    fn("f/revive", [
        "tag @s add rpg.fo.self",
        "execute as @e[type=minecraft:player,tag=rpg.fo.down,tag=!rpg.fo.self,limit=1,sort=nearest] run function %s" % X("f/revive_one"),
        "tag @s remove rpg.fo.self",
        "playsound minecraft:block.beacon.activate player @a[distance=..32] ~ ~ ~ 1 1.6",
    ] + xh.glyph("dove", 2.0, "white", pos="^ ^1.6 ^1.6", kind="doverise"))
    fn("f/revive_one", [
        "tp @s @a[tag=rpg.fo.self,limit=1]",
        "tag @s remove rpg.fo.down",
        "scoreboard players set @s rpg_fo_dn 0",
        "effect give @s minecraft:instant_health 1 2 true",
        "effect give @s minecraft:resistance 5 2 true",
        "effect give @s minecraft:regeneration 10 1 true",
        "execute at @s run particle minecraft:totem_of_undying ~ ~1 ~ 0.4 0.8 0.4 0.3 40",
        "tellraw @a[distance=..64] " + F.J(["", t("[力] ", F.C_GOLD, True), {"selector": "@s"}, t(" 被圣灵从死亡里拉了回来。", F.C_BODY)]),
    ] + ["execute at @s run " + l for l in xh.glyph("halo", 1.2, "white", pos="~ ~2.3 ~", kind="halo")[:1]] +
        xh.glyph("halo", 1.2, "white", pos="~ ~2.3 ~", kind="halo")[1:])
    # 堕天
    fn("f/fall", [
        "scoreboard players operation @s rpg_fo_fl = #now %s" % O,
        "scoreboard players add @s rpg_fo_fl 200",
        "playsound minecraft:entity.wither.spawn player @a[distance=..32] ~ ~ ~ 0.5 1.6",
        "playsound minecraft:entity.phantom.flap player @a[distance=..16] ~ ~ ~ 1 0.6",
        "particle minecraft:smoke ^ ^1 ^-1.6 0.5 0.8 0.5 0.03 30",
        "title @s actionbar " + F.J(t("堕天：10 秒内魔力技能不耗力、不涨魔化", F.C_MANA, True)),
    ] + xh.glyph("wings", 3.2, "#8A5AB0", pos="^ ^1.6 ^-1.8", kind="wings") +
        xm.decal("sigil", 5, 0x5B2A86, life=40))
    fn("f/fall_tick", [
        "execute if score @s rpg_fo_fl <= #now %s run return run function %s" % (O, X("f/fall_end")),
        "particle minecraft:reverse_portal ^ ^1.2 ^-0.9 0.4 0.5 0.1 0.02 2",
        "particle minecraft:dust{color:[0.54,0.35,0.69],scale:1.0} ^-0.7 ^1.4 ^-0.8 0.1 0.2 0.1 0 1",
        "particle minecraft:dust{color:[0.54,0.35,0.69],scale:1.0} ^0.7 ^1.4 ^-0.8 0.1 0.2 0.1 0 1",
    ])
    fn("f/fall_end", [
        "scoreboard players set @s rpg_fo_fl 0",
        "scoreboard players add @s rpg_taint 20",
        "playsound minecraft:entity.wither.ambient player @s ~ ~ ~ 0.6 0.8",
        say([t("堕天结束 · 魔化 +20", F.C_MANA)]),
    ])
    lords(xh, xm)


def lords(xh, xm):
    hit = "function %s/hit" % P
    E, NB = F.ENEMY, F.NOBOSS
    col = dict((p["n"], p["lit"]) for p in ui.PILLARS)
    ci = lambda k: int(col[k][1:], 16)
    # 1 晨星坠落
    F.ray("lord1", 60, "particle minecraft:end_rod ~ ~ ~ 0 0 0 0 1 force", E,
          ["scoreboard players set #dmg %s 160" % O, "scoreboard players set #hm %s 10" % O, hit,
           "particle minecraft:dust{color:[0.37,0.84,0.55],scale:1.4} ~ ~1 ~ 0.3 0.6 0.3 0 20"], pierce=True)
    fn("f/lord1", ["playsound minecraft:entity.phantom.flap player @a[distance=..24] ~ ~ ~ 1 1.2",
                   "playsound minecraft:item.trident.thunder player @a[distance=..32] ~ ~ ~ 0.7 1.8",
                   "function %s/ray/lord1/go" % P] +
       xh.glyph("wings", 3.2, col[1], pos="^ ^1.6 ^-1.8", kind="wings") +
       xh.glyph("burst", 2.6, col[1], pos="^ ^1.6 ^4.5", kind="burst"))
    # 2 海渊回卷
    fn("f/lord2", ["playsound minecraft:entity.elder_guardian.curse player @a[distance=..24] ~ ~ ~ 0.6 1.2",
                   "playsound minecraft:ambient.underwater.enter player @a[distance=..24] ~ ~ ~ 1 0.6",
                   "particle minecraft:nautilus ~ ~1 ~ 5 1 5 0.5 160",
                   "particle minecraft:bubble_pop ~ ~0.5 ~ 5 0.3 5 0.05 80",
                   "scoreboard players set #dmg %s 60" % O, "scoreboard players set #hm %s 10" % O,
                   "execute as @e[%s,%s,distance=1.8..10] at @s run function %s" % (E, NB, X("f/lord2_pull")),
                   "execute as @e[%s,distance=..10] at @s run %s" % (E, hit),
                   "effect give @e[%s,%s,distance=..10] minecraft:slowness 3 9 true" % (E, NB),
                   "effect give @e[%s,%s,distance=..10] minecraft:jump_boost 3 250 true" % (E, NB)] +
       xm.decal("swirl", 14, ci(2), kind="spinr", life=40))
    fn("f/lord2_pull", ["execute at @a[tag=rpg.fo.me,limit=1] facing entity @s feet rotated ~ 0 run tp @s ^ ^ ^1.8",
                        "execute at @s run particle minecraft:bubble ~ ~1 ~ 0.3 0.5 0.3 0.1 12"])
    # 3 无底坑
    F.ground("pit", [
        "summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.fo.zone\",\"rpg.fo.znew\"]}",
        "scoreboard players set @e[type=minecraft:marker,tag=rpg.fo.znew] rpg_fo_k 63",
        "scoreboard players operation @e[type=minecraft:marker,tag=rpg.fo.znew] rpg_fo_end = #now %s" % O,
        "scoreboard players add @e[type=minecraft:marker,tag=rpg.fo.znew] rpg_fo_end 120",
        "tag @e[type=minecraft:marker,tag=rpg.fo.znew] remove rpg.fo.znew",
    ] + xm.decal("cracks", 10, ci(3), life=120) + xm.decal("swirl", 8, 0x2A2A30, pos="~ ~0.08 ~", kind="spin", life=120))
    fn("f/lord3", ["playsound minecraft:block.sculk_shrieker.shriek player @a[distance=..24] ~ ~ ~ 0.6 0.6",
                   "playsound minecraft:block.end_portal.spawn player @a[distance=..24] ~ ~ ~ 0.4 0.6",
                   "function %s/ground/pit/go" % P])
    fn("zone/pit", [
        "particle minecraft:sculk_soul ~ ~0.2 ~ 2.5 0.1 2.5 0.01 2",
        "particle minecraft:ash ~ ~0.5 ~ 2.5 0.4 2.5 0 6",
        "effect give @e[%s,distance=..5] minecraft:slowness 1 3 true" % E,
        "execute as @e[%s,%s,distance=..5] at @s if block ~ ~-0.2 ~ #rpg:force/pass run tp @s ~ ~-0.05 ~" % (E, NB),
        "execute unless score #zt %s matches 0 run return 0" % O,
        "scoreboard players operation #zt %s = @s rpg_fo_end" % O,
        "scoreboard players operation #zt %s -= #now %s" % (O, O),
        "scoreboard players operation #zt %s %%= #20 %s" % (O, O),
        "execute unless score #zt %s matches 0 run return 0" % O,
        "scoreboard players set #dmg %s 30" % O, "scoreboard players set #hm %s 10" % O,
        "execute as @e[%s,distance=..5] at @s run %s" % (E, hit),
    ])
    F.add_lines("zone/tick", ["execute if score @s rpg_fo_k matches 63 run function %s" % X("zone/pit"),
                              "execute if score @s rpg_fo_k matches 36 run function %s" % X("zone/star")])
    F.add_lines("zone/tick", ["execute if score @s rpg_fo_k matches 36 if score @s rpg_fo_end <= #now %s run function %s" % (O, X("zone/star_boom"))],
                before="execute if score @s rpg_fo_end <= #now")
    # 4 蝇王之宴
    fn("f/lord4", ["scoreboard players operation @s rpg_fo_fe = #now %s" % O, "scoreboard players add @s rpg_fo_fe 100",
                   "playsound minecraft:entity.bee.loop_aggressive player @a[distance=..24] ~ ~ ~ 1 0.5",
                   "particle minecraft:dust{color:[0.35,0.42,0.12],scale:0.6} ~ ~1.2 ~ 4 1 4 0 200"] +
       xm.decal("hexagram", 16, ci(4), kind="spin", life=100))
    fn("f/feast_sec", [
        "execute if score @s rpg_fo_fe <= #now %s run return run scoreboard players set @s rpg_fo_fe 0" % O,
        "particle minecraft:dust{color:[0.2,0.25,0.06],scale:0.5} ~ ~1.2 ~ 5 1 5 0 160",
        "playsound minecraft:entity.bee.loop_aggressive player @a[distance=..16] ~ ~ ~ 0.6 0.4",
        "scoreboard players set #dmg %s 30" % O, "scoreboard players set #hm %s 10" % O,
        "tag @s add rpg.fo.me",
        "execute store result score #n %s if entity @e[%s,distance=..8]" % (O, E),
        "execute as @e[%s,distance=..8] at @s run %s" % (E, hit),
        "tag @s remove rpg.fo.me",
        "execute if score #n %s matches 2.. run effect give @s minecraft:instant_health 1 0 true" % O,
        "execute if score #n %s matches 1 run effect give @s minecraft:regeneration 2 1 true" % O,
    ])
    # 5 毒龙之怒
    fn("f/lord5", ["scoreboard players operation @s rpg_fo_wr = #now %s" % O, "scoreboard players add @s rpg_fo_wr 200",
                   "scoreboard players set @s rpg_fo_dt 0",
                   "playsound minecraft:entity.ender_dragon.growl player @a[distance=..24] ~ ~ ~ 0.6 1.4",
                   "particle minecraft:flame ~ ~1 ~ 0.6 1 0.6 0.05 60"] +
       xh.glyph("fburn", 2.0, col[5], pos="^ ^1.2 ^3", kind="fadel"))
    fn("f/wrath_tick", [
        "execute if score @s rpg_fo_wr <= #now %s run return run scoreboard players set @s rpg_fo_wr 0" % O,
        "particle minecraft:dust{color:[1.0,0.36,0.32],scale:0.8} ~ ~1 ~ 0.3 0.6 0.3 0 1",
        "execute unless score @s rpg_fo_dt matches 1.. run return 0",
        "scoreboard players set @s rpg_fo_dt 0",
        "playsound minecraft:entity.blaze.shoot player @a[distance=..16] ~ ~ ~ 1 0.6",
        "particle minecraft:flame ~ ~1 ~ 2 0.5 2 0.05 60",
        "particle minecraft:dust{color:[0.48,0.85,0.3],scale:1.2} ~ ~1 ~ 2 0.5 2 0 30",
        "scoreboard players set #dmg %s 40" % O, "scoreboard players set #hm %s 10" % O,
        "tag @s add rpg.fo.me",
        "execute as @e[%s,distance=..4] at @s run %s" % (E, hit),
        "effect give @e[%s,distance=..4] minecraft:poison 3 1 true" % E,
        "tag @s remove rpg.fo.me",
    ])
    # 6 无主之契
    F.ray("charm", 48, "particle minecraft:dust{color:[0.85,0.48,0.85],scale:0.8} ~ ~ ~ 0 0 0 0 1 force",
          "%s,%s" % (E, NB), [
              "tag @s add rpg.ally", "tag @s add rpg.fo.ch",
              "scoreboard players operation @s rpg_fo_end = #now %s" % O, "scoreboard players add @s rpg_fo_end 300",
              "effect give @s minecraft:weakness 15 255 true", "effect give @s minecraft:glowing 15 0 true",
              "particle minecraft:heart ~ ~2 ~ 0.4 0.3 0.4 0 8",
              "playsound minecraft:entity.allay.item_given hostile @a[distance=..16] ~ ~ ~ 1 0.6"])
    fn("f/lord6", ["playsound minecraft:block.amethyst_block.resonate player @a[distance=..16] ~ ~ ~ 1 0.6",
                   "function %s/ray/charm/go" % P])
    fn("f/charm_sec", [
        "execute if score @s rpg_fo_end <= #now %s run return run function %s" % (O, X("f/charm_end")),
        "particle minecraft:witch ~ ~2.1 ~ 0.2 0.1 0.2 0 3",
        "tag @s add rpg.fo.chs",
        "execute as @e[%s,distance=..10,limit=1,sort=nearest] at @s run function %s" % (E, X("f/charm_bite")),
        "tag @s remove rpg.fo.chs",
    ])
    fn("f/charm_bite", ["damage @s 5 minecraft:mob_attack by @e[tag=rpg.fo.chs,limit=1]",
                        "particle minecraft:dust{color:[0.85,0.48,0.85],scale:1} ~ ~1 ~ 0.3 0.5 0.3 0 10"])
    fn("f/charm_end", ["tag @s remove rpg.ally", "tag @s remove rpg.fo.ch",
                       "effect clear @s minecraft:weakness", "effect clear @s minecraft:glowing",
                       "particle minecraft:smoke ~ ~1.5 ~ 0.3 0.4 0.3 0.02 12"])
    # 7 金之枷
    F.ray("gild", 48, "particle minecraft:wax_on ~ ~ ~ 0 0 0 0 1 force", E, [
        "tag @s add rpg.fo.gd",
        "scoreboard players operation @s rpg_fo_end = #now %s" % O, "scoreboard players add @s rpg_fo_end 60",
        "execute store result score @s rpg_fo_ai run data get entity @s NoAI",
        "scoreboard players set #b %s 0" % O] +
        ["execute if entity @s[tag=%s] run scoreboard players set #b %s 1" % (b, O) for b in F.BOSS_TAGS] + [
        "execute if score #b %s matches 0 run data merge entity @s {NoAI:1b}" % O,
        "execute if score #b %s matches 1 run effect give @s minecraft:slowness 3 4 true" % O,
        "effect give @s minecraft:glowing 3 0 true",
        "particle minecraft:block{block_state:\"minecraft:gold_block\"} ~ ~1 ~ 0.4 0.8 0.4 0 40",
        "playsound minecraft:block.anvil.place hostile @a[distance=..16] ~ ~ ~ 0.8 1.4"])
    fn("f/lord7", ["playsound minecraft:block.amethyst_cluster.place player @a[distance=..16] ~ ~ ~ 1 0.6",
                   "function %s/ray/gild/go" % P])
    fn("f/gild_tick", [
        "execute if score @s rpg_fo_end > #now %s run return run particle minecraft:wax_on ~ ~1 ~ 0.4 0.7 0.4 0 2" % O,
        "tag @s remove rpg.fo.gd",
        "execute if score @s rpg_fo_ai matches 0 run data merge entity @s {NoAI:0b}",
        "particle minecraft:block{block_state:\"minecraft:gold_block\"} ~ ~1 ~ 1.2 0.8 1.2 0 80",
        "playsound minecraft:block.glass.break hostile @a[distance=..16] ~ ~ ~ 1 0.6",
        "playsound minecraft:block.chain.break hostile @a[distance=..16] ~ ~ ~ 1 0.6",
        "scoreboard players set #dmg %s 100" % O, "scoreboard players set #hm %s 10" % O,
        "execute as @e[%s,distance=..3] at @s run %s" % (E, hit),
    ] + xm.decal("hexagon", 4, ci(7), life=20))


# ============================================================================ Boss 传承技
def legacy_item(n):
    _n, kind, name, desc, fc, xc, cd, boss = F.EX[n]
    bz, bcol = BOSS_NAME[boss]
    rule = t(ui.RULE_TEXT, ui.WHITE)
    lore = [rule, t("击败%s所得的传承" % bz, ui.GRAY), t(desc, ui.GRAY),
            t("读了就学会，不占技能点；圣徽、罪印的槽都能放", ui.GRAY),
            t("圣徽付生命力，罪印付魔化；没觉醒的无知者先收着", ui.MUTED), rule]
    return ("minecraft:paper[custom_name=%s,lore=%s,item_model=\"minecraft:enchanted_book\",max_stack_size=1,"
            "enchantment_glint_override=true,food={nutrition:0,saturation:0f,can_always_eat:1b},"
            "consumable={consume_seconds:1.2f,animation:\"none\",sound:\"minecraft:item.book.page_turn\","
            "has_consume_particles:false,on_consume_effects:[]},custom_data={rpg_legacy:%d}]"
            % (F.J(["", t("[传承]", F.C_GOLD, True), t(name, ui.WHITE)]), F.J(lore), n))


def legacy(xh, xm):
    hit = "function %s/hit" % P
    E, NB = F.ENEMY, F.NOBOSS
    by_boss = {}
    for n, kind, name, desc, fc, xc, cd, boss in F.EXTRA:
        if kind != "l":
            continue
        by_boss[boss] = n
        bz, bcol = BOSS_NAME[boss]
        F.wj(os.path.join(F.DP, "data", "rpg", "advancement", "force", "legacy_%d.json" % n), {
            "criteria": {"read": {"trigger": "minecraft:consume_item", "conditions": {
                "item": {"predicates": {"minecraft:custom_data": "{rpg_legacy:%d}" % n}}}}},
            "rewards": {"function": X("l/read_%d" % n)}})
        fn("l/read_%d" % n, [
            "advancement revoke @s only rpg:force/legacy_%d" % n,
            "execute unless score @s rpg_force matches 1.. run return run function %s" % X("l/back_%d" % n),
            "execute if score @s %s matches 1.. run return run function %s" % (F.kk(n), X("l/known_%d" % n)),
            "scoreboard players set @s %s 1" % F.kk(n),
            "execute if score @s rpg_force matches 1 run function %s" % X("l/auto1_%d" % n),
            "execute if score @s rpg_force matches 3 run function %s" % X("l/auto1_%d" % n),
            "execute if score @s rpg_force matches 2 run function %s" % X("l/auto2_%d" % n),
            "playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 1 0.8",
            "playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.4",
            "particle minecraft:enchant ~ ~1.2 ~ 0.5 0.8 0.5 0.6 60",
            say([t("读懂了", F.C_MUTED), t(bz, bcol, True), t("的传承：", F.C_MUTED), t(name, F.C_GOLD, True),
                 t("。在技能页「王冠 · 传承」里把它放进槽。", F.C_BODY)]),
        ])
        fn("l/auto1_%d" % n, autoslot(1, n))
        fn("l/auto2_%d" % n, autoslot(2, n))
        fn("l/back_%d" % n, ["give @s " + legacy_item(n), say([t("你还没有力，读不懂这本书。先收着，觉醒后再读。", F.C_MUTED)])])
        fn("l/known_%d" % n, ["give @s " + legacy_item(n), say([t("你已经会「%s」了。这本书可以留给别人。" % name, F.C_MUTED)])])
        fn("l/give_%d" % n, ["give @s " + legacy_item(n),
                             "playsound minecraft:item.book.put player @s ~ ~ ~ 1 0.8",
                             say([t("获得传承书 ", F.C_MUTED), t("传承 · " + name, F.C_GOLD, True)])])
        fn("l/drop_%s" % boss, [
            "# 首杀必掉，之后每次 20%",
            "execute if score @s rpg_bk_%s matches 1 run return run function %s" % (boss, X("l/give_%d" % n)),
            "execute store result score #r %s run random value 1..5" % O,
            "execute if score #r %s matches 1 run function %s" % (O, X("l/give_%d" % n)),
        ])
        F.patch("sephira/boss/cr_%s.mcfunction" % boss, X("l/drop_%s" % boss),
                "function %s\n" % X("l/drop_%s" % boss), "execute if score @s rpg_bk_%s matches 1 run return run" % boss)
    # 管理员：六本书
    F.fn("admin/legacy", ["give @s " + legacy_item(n) for n in sorted(by_boss.values())])

    # 31 信条（教皇）
    F.fn("sk/31/do", [
        "playsound minecraft:block.bell.use player @a[distance=..24] ~ ~ ~ 1 0.8",
        "playsound minecraft:block.beacon.power_select player @a[distance=..24] ~ ~ ~ 0.8 1.2",
        "effect give @a[distance=..8,gamemode=!spectator] minecraft:resistance 10 0 true",
        "execute as @a[distance=..8,gamemode=!spectator] run scoreboard players operation @s rpg_fo_cr = #now %s" % O,
        "scoreboard players add @a[distance=..8,gamemode=!spectator] rpg_fo_cr 200",
        "execute as @a[distance=..8,gamemode=!spectator] at @s run function %s" % X("f/hal_ally"),
        "particle minecraft:end_rod ~ ~0.2 ~ 4 0.1 4 0 60",
    ] + xh.decal("rpg:michael_vfx/ring_h", 16, 0xFFFFFF, life=40) +
        xh.decal("rpg:michael_vfx/seal_seraph", 6, 0xFFFFFF, pos="~ ~0.08 ~", kind="spin", life=40))
    fn("l/credo_sec", [
        "# 信条：力的回复翻倍（圣力每秒再 +2，魔力每秒再 +3）",
        "execute if score @s rpg_force matches 1 run scoreboard players add @s rpg_mana 2",
        "execute if score @s rpg_force matches 3 run scoreboard players add @s rpg_mana 2",
        "execute if score @s rpg_force matches 2 run scoreboard players add @s rpg_mana 3",
        "execute if score @s rpg_force matches 3 run scoreboard players add @s rpg_mana2 3",
        "particle minecraft:wax_on ~ ~2.2 ~ 0.2 0.1 0.2 0 2",
    ])
    # 32 篡夺（篡夺者）
    steal = ["tag @s add rpg.fo.hit", "scoreboard players set #st %s 0" % O]
    for e in POSITIVE:
        steal.append("execute if score #st %s matches 0 if entity @s[nbt={active_effects:[{id:\"minecraft:%s\"}]}] run function %s"
                     % (O, e, X("l/steal_" + e)))
        fn("l/steal_" + e, ["effect clear @s minecraft:" + e, "effect give @a[tag=rpg.fo.me,limit=1] minecraft:%s 10 0 true" % e,
                            "scoreboard players set #st %s 1" % O])
    steal += ["scoreboard players set #b %s 0" % O] + \
             ["execute if entity @s[tag=%s] run scoreboard players set #b %s 1" % (b, O) for b in F.BOSS_TAGS] + [
        "execute if score #b %s matches 0 run effect give @s minecraft:slowness 5 9 true" % O,
        "execute if score #b %s matches 0 run effect give @s minecraft:jump_boost 5 250 true" % O,
        "execute if score #b %s matches 0 run effect give @s minecraft:weakness 5 4 true" % O,
        "execute if score #st %s matches 1 run particle minecraft:totem_of_undying ~ ~1.2 ~ 0.3 0.5 0.3 0.2 16" % O,
        "playsound minecraft:entity.illusioner.mirror_move hostile @a[distance=..16] ~ ~ ~ 1 0.8"]
    F.ray("usurp", 48, "particle minecraft:dust{color:[0.9,0.88,0.95],scale:0.7} ~ ~ ~ 0 0 0 0 1 force", E,
          steal + xm.glyph("burst", 2.2, "#E8E0F0", pos="~ ~1 ~", kind="burst") + xm.slash("~ ~1.2 ~", "#A276BE", size=2.4))
    F.fn("sk/32/do", ["playsound minecraft:entity.evoker.prepare_attack player @a[distance=..16] ~ ~ ~ 1 1.2",
                      "function %s/ray/usurp/go" % P])
    # 33 圣殿誓约（雅克）：借友军雅克的召唤，不动号角的冷却
    F.fn("sk/33/do", [
        "scoreboard players add @s rpg_al_cd 0",
        "scoreboard players operation #al %s = @s rpg_al_cd" % O,
        "function rpg:jacques_ally/summon",
        "scoreboard players operation @s rpg_al_cd = #al %s" % O,
    ])
    # 34 千刀（扫罗）
    F.fn("sk/34/do", ["scoreboard players set @s rpg_fo_tk 8",
                      "playsound minecraft:item.trident.riptide_1 player @a[distance=..16] ~ ~ ~ 1 1.4"])
    fn("l/saul_tick", [
        "scoreboard players operation #q %s = #now %s" % (O, O),
        "scoreboard players operation #q %s %%= #5 %s" % (O, O),
        "execute unless score #q %s matches 0 run return 0" % O,
        "scoreboard players remove @s rpg_fo_tk 1",
        "playsound minecraft:entity.player.attack.sweep player @a[distance=..16] ~ ~ ~ 1 1.3",
        "particle minecraft:sweep_attack ^ ^1.1 ^1.8 0.6 0.3 0.6 0 3",
        "scoreboard players set #dmg %s 30" % O, "scoreboard players set #hm %s 10" % O,
        "tag @s add rpg.fo.me",
        "execute positioned ^ ^ ^2 as @e[%s,distance=..2.8] at @s run %s" % (E, hit),
        "tag @s remove rpg.fo.me",
        "execute if score @s rpg_fo_tk matches 0..1 run playsound minecraft:item.trident.return player @a[distance=..16] ~ ~ ~ 1 1.6",
    ] + ["execute if score @s rpg_fo_tk matches %d run %s" % (k, l) for k in range(8)
         for l in xm.slash("^%s ^1.1 ^3.4" % ("0.5" if k % 2 else "-0.5"), "#E6DFCF" if k % 2 else "#C0303C", size=1.2)[:1]] +
        xm.slash("^ ^1.2 ^1.6", "#E6DFCF", size=0.01)[1:])
    # 35 注视（米迦勒）
    F.fn("sk/35/do", [
        "playsound minecraft:block.beacon.power_select player @a[distance=..24] ~ ~ ~ 1 1.8",
        "playsound minecraft:entity.allay.ambient_without_item player @a[distance=..24] ~ ~ ~ 1 0.6",
        "tag @e[%s,distance=..16,limit=3,sort=nearest] add rpg.fo.gz" % E,
        "execute as @e[tag=rpg.fo.gz] at @s run function %s" % X("l/gaze_one"),
    ] + xh.glyph("eye", 0.8, "white", pos="^-1.4 ^2.6 ^2.2", kind="fadel", life=40) +
        xh.glyph("eye", 0.8, "white", pos="^ ^3 ^2.6", kind="fadel", life=40) +
        xh.glyph("eye", 0.8, "white", pos="^1.4 ^2.6 ^2.2", kind="fadel", life=40))
    fn("l/gaze_one", [
        "tag @s remove rpg.fo.gz",
        "tag @s add rpg.fo.mk",
        "scoreboard players operation @s rpg_fo_end = #now %s" % O,
        "scoreboard players add @s rpg_fo_end 160",
        "scoreboard players set @s rpg_fo_mk 20",
        "execute store result score @s rpg_fo_hp run data get entity @s Health 10",
        "effect give @s minecraft:glowing 8 0 true",
        "particle minecraft:end_rod ~ ~1.5 ~ 0.2 0.4 0.2 0.05 10",
    ] + ride(xh.glyph("eye", 0.9, "white", pos="~ ~ ~", trans=(0, 0.5, 0), life=160)))
    # 36 晨星（路西法）
    F.ray("star", 60, "particle minecraft:end_rod ~ ~ ~ 0 0 0 0 1 force", E, [], on_end=["function %s/ground/star/go" % P])
    F.ground("star", [
        "summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.fo.zone\",\"rpg.fo.znew\"]}",
        "scoreboard players set @e[type=minecraft:marker,tag=rpg.fo.znew] rpg_fo_k 36",
        "scoreboard players operation @e[type=minecraft:marker,tag=rpg.fo.znew] rpg_fo_end = #now %s" % O,
        "scoreboard players add @e[type=minecraft:marker,tag=rpg.fo.znew] rpg_fo_end 20",
        "tag @e[type=minecraft:marker,tag=rpg.fo.znew] remove rpg.fo.znew",
    ] + xh.decal("rpg:michael_vfx/ring_r", 10, 0xFFFFFF, life=20))
    F.fn("sk/36/do", ["playsound minecraft:entity.firework_rocket.launch player @a[distance=..24] ~ ~ ~ 1 0.5",
                      "function %s/ray/star/go" % P])
    star = ["scoreboard players operation #zt %s = @s rpg_fo_end" % O, "scoreboard players operation #zt %s -= #now %s" % (O, O)]
    for k in range(1, 21):
        star.append("execute if score #zt %s matches %d run particle minecraft:flame ~ ~%.1f ~ 0.3 0.3 0.3 0.02 14 force" % (O, k, k * 1.2))
        star.append("execute if score #zt %s matches %d run particle minecraft:end_rod ~ ~%.1f ~ 0.15 0.15 0.15 0 4 force" % (O, k, k * 1.2 + 0.6))
    star.append("execute if score #zt %s matches 10 run playsound minecraft:entity.blaze.shoot player @a[distance=..32] ~ ~ ~ 1 0.5" % O)
    fn("zone/star", star)
    fn("zone/star_boom", [
        "particle minecraft:explosion_emitter ~ ~1 ~ 0 0 0 0 1 force",
        "particle minecraft:flame ~ ~0.5 ~ 2.5 0.5 2.5 0.1 120 force",
        "particle minecraft:lava ~ ~0.5 ~ 2 0.2 2 0 30",
        "playsound minecraft:entity.generic.explode player @a[distance=..48] ~ ~ ~ 2 0.7",
        "scoreboard players set #dmg %s 140" % O, "scoreboard players set #hm %s 10" % O,
        "execute as @e[%s,distance=..5] at @s run function %s" % (E, X("l/star_one")),
    ] + xh.decal("rpg:michael_vfx/shock_0", 12, 0xFFFFFF, kind="mshock") +
        xh.decal("rpg:michael_vfx/scorch", 8, 0xFFFFFF, pos="~ ~0.08 ~", life=100))
    fn("l/star_one", [hit, "data merge entity @s {Fire:100s}"])


# ============================================================================ 身份能力
def identity():
    hit_no = "function %s/hit_no with storage rpg:force h" % P
    E = F.ENEMY
    pos_old = []
    for tr, model in ((1, "minecraft:nether_star"), (2, "minecraft:echo_shard")):
        pos_old += ["execute if items entity @s container.* *[minecraft:custom_data~{rpg_sigil:%d}] unless items entity @s container.* *[minecraft:custom_data~{rpg_sigil:%d},minecraft:item_model=\"rpg:force/%s\",minecraft:custom_name] run function %s"
                    % (tr, tr, "holy_sigil" if tr == 1 else "sin_sigil", X("mig/%d" % tr)),
                    "execute if items entity @s weapon.offhand *[minecraft:custom_data~{rpg_sigil:%d}] unless items entity @s weapon.offhand *[minecraft:custom_data~{rpg_sigil:%d},minecraft:item_model=\"rpg:force/%s\",minecraft:custom_name] run function %s"
                    % (tr, tr, "holy_sigil" if tr == 1 else "sin_sigil", X("mig/%d" % tr))]
        fn("mig/%d" % tr, ["clear @s *[minecraft:custom_data~{rpg_sigil:%d}]" % tr, "give @s " + F.sigil_item(tr)])
    sec = ["# 每秒（as/at 走完新手的玩家）"] + pos_old + [
        "tag @s remove rpg.fo.msh",
        "execute if score @s rpg_messiah matches 1 run tag @s add rpg.fo.msh",
        "# 王冠终式",
        "execute if score @s rpg_sef matches 10 if score @s rpg_force matches 1 unless score @s %s matches 1.. run function %s" % (F.kk(25), X("f/unlock_h")),
        "execute if score @s rpg_sef matches 10 if score @s rpg_force matches 3 unless score @s %s matches 1.. run function %s" % (F.kk(25), X("f/unlock_h")),
        "execute if score @s rpg_sef matches 10 if score @s rpg_force matches 2..3 unless score @s %s matches 1.. run function %s" % (F.kk(26), X("f/unlock_m")),
        "execute if score @s rpg_fo_cr > #now %s run function %s" % (O, X("l/credo_sec")),
        "# 倒下：60 秒内能被圣灵复活",
        "execute if score @s rpg_fo_die matches 1.. run function %s" % X("id/died"),
        "execute if entity @s[tag=rpg.fo.down] if score @s rpg_fo_dn <= #now %s run tag @s remove rpg.fo.down" % O,
    ] + ["execute if score @s rpg_ident matches %d run function %s" % (k, X("id/s%d" % k)) for k in (1, 2, 4, 6)]
    fn("id/sec", sec)
    fn("id/died", ["scoreboard players set @s rpg_fo_die 0", "tag @s add rpg.fo.down",
                   "scoreboard players operation @s rpg_fo_dn = #now %s" % O, "scoreboard players add @s rpg_fo_dn 1200"])
    for kind, tr, n in (("h", 1, 25), ("m", 2, 26)):
        fn("f/unlock_" + kind, [
            "scoreboard players set @s %s 1" % F.kk(n),
            "function %s/page/fill" % P,
            "function %s" % X("f/auto_" + kind),
            "playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1",
            "tellraw @s " + F.J(["", t("[力] ", F.C_GOLD, True), t("王冠阶 · 习得终式 ", F.C_MUTED),
                                 {"nbt": "p.n%d" % n, "storage": "rpg:force", "color": F.TREES[tr][1], "bold": True},
                                 t("。在技能页「王冠 · 传承」里放进槽。", F.C_BODY)]),
        ])
        fn("f/auto_" + kind, autoslot(tr, n))

    # 无知者
    # 逐条翻 active_effects（校验器不认 active_effects[{id:..}] 这种过滤写法）
    ALL = ["speed", "slowness", "haste", "mining_fatigue", "strength", "instant_health", "instant_damage", "jump_boost",
           "nausea", "regeneration", "resistance", "fire_resistance", "water_breathing", "invisibility", "blindness",
           "night_vision", "hunger", "weakness", "poison", "wither", "health_boost", "absorption", "saturation", "glowing",
           "levitation", "luck", "unluck", "slow_falling", "conduit_power", "dolphins_grace", "bad_omen",
           "hero_of_the_village", "darkness", "trial_omen", "raid_omen", "wind_charged", "weaving", "oozing", "infested",
           "breath_of_the_nautilus"]
    fn("id/cut", ["# 恶魔附近：新上身的负面效果时长 −30%（美丽阶起 −60%），每个效果只砍一次",
                  "data modify storage rpg:force r.l set from entity @s active_effects",
                  "function %s" % X("id/cut_loop")] +
       ["execute unless entity @s[tag=rpg.fo.p_%s] run tag @s remove rpg.fo.r_%s" % (e, e) for e in NEG_CUT] +
       ["tag @s remove rpg.fo.p_%s" % e for e in NEG_CUT])
    fn("id/cut_loop", [
        "execute unless data storage rpg:force r.l[0] run return 0",
        "data modify storage rpg:force r.c set from storage rpg:force r.l[0]",
        "data remove storage rpg:force r.l[0]",
        "data modify storage rpg:force r.c.n set string storage rpg:force r.c.id 10",
        "function %s" % X("id/cut_one"),
        "function %s" % X("id/cut_loop"),
    ])
    fn("id/cut_one", ["execute if data storage rpg:force r.c{n:\"%s\"} run return run function %s with storage rpg:force r.c" % (e, X("id/n/" + e))
                      for e in NEG_CUT])
    for e in NEG_CUT:
        fn("id/n/" + e, [
            "tag @s add rpg.fo.p_" + e,
            "execute if entity @s[tag=rpg.fo.r_%s] run return 0" % e,
            "tag @s add rpg.fo.r_" + e,
            "$scoreboard players set #t %s $(duration)" % O,
            "execute unless score #t %s matches 21.. run return 0" % O,
            "data modify storage rpg:force r.e set value \"%s\"" % e,
            "$data modify storage rpg:force r.a set value $(amplifier)",
            "execute unless score @s rpg_sef matches 5.. run scoreboard players operation #t %s *= #7 %s" % (O, O),
            "execute if score @s rpg_sef matches 5.. run scoreboard players operation #t %s *= #4 %s" % (O, O),
            "scoreboard players operation #t %s /= #10 %s" % (O, O),
            "scoreboard players operation #t %s /= #20 %s" % (O, O),
            "execute if score #t %s matches ..0 run scoreboard players set #t %s 1" % (O, O),
            "execute store result storage rpg:force r.s int 1 run scoreboard players get #t %s" % O,
            "effect clear @s minecraft:" + e,
            "function %s with storage rpg:force r" % X("id/regive"),
        ])
    fn("id/regive", ["$effect give @s minecraft:$(e) $(s) $(a) true"])
    fn("id/s1", [
        "# 无知者：阅历 +20%（美丽阶起 +40%）",
        "execute unless score @s rpg_fo_xl matches 0.. run scoreboard players operation @s rpg_fo_xl = @s rpg_ex_xp",
        "scoreboard players operation #d %s = @s rpg_ex_xp" % O,
        "scoreboard players operation #d %s -= @s rpg_fo_xl" % O,
        "execute if score #d %s matches 1.. run function %s" % (O, X("id/xp")),
        "scoreboard players operation @s rpg_fo_xl = @s rpg_ex_xp",
        "execute if entity @e[tag=rpg.demon,distance=..32,limit=1] run return run function %s" % X("id/cut"),
        "execute if entity @e[tag=rpg.demon.minion,distance=..32,limit=1] run function %s" % X("id/cut"),
    ])
    fn("id/xp", [
        "scoreboard players operation #d %s *= #20 %s" % (O, O),
        "execute if score @s rpg_sef matches 5.. run scoreboard players operation #d %s *= #2 %s" % (O, O),
        "scoreboard players operation @s rpg_fo_xa += #d %s" % O,
        "scoreboard players operation #q %s = @s rpg_fo_xa" % O,
        "scoreboard players operation #q %s /= #100 %s" % (O, O),
        "scoreboard players operation @s rpg_ex_xp += #q %s" % O,
        "scoreboard players operation @s rpg_fo_xa %%= #100 %s" % O,
    ])
    # 边缘者
    fn("id/s2", ["# 边缘者：空缺者在 6 格内始终显形",
                 "effect clear @e[tag=rpg.vacant,distance=..6] minecraft:invisibility",
                 "effect give @e[tag=rpg.vacant,distance=..6] minecraft:glowing 2 0 true"])
    # 七大罪之仆
    fn("id/s4", ["execute if score @s rpg_ident_sin matches %d run function %s" % (k, X("id/sin%d" % k)) for k in (1, 3, 4, 5)])
    fn("id/sin1", [
        "# 傲慢：满血时伤害 +10%（美丽阶起 +20%）",
        "attribute @s minecraft:attack_damage modifier remove rpg:fo_sin",
        "execute store result score #h %s run data get entity @s Health 10" % O,
        "execute store result score #mh %s run attribute @s minecraft:max_health get 10" % O,
        "execute unless score #h %s >= #mh %s run return 0" % (O, O),
    ] + sef5(["attribute @s minecraft:attack_damage modifier add rpg:fo_sin 0.2 add_multiplied_total"],
             ["attribute @s minecraft:attack_damage modifier add rpg:fo_sin 0.1 add_multiplied_total"]))
    fn("id/sin3", [
        "# 怠惰：站着不动 2 秒后抗性 I（美丽阶起 II）",
        "execute store result score #x %s run data get entity @s Pos[0] 10" % O,
        "execute store result score #z %s run data get entity @s Pos[2] 10" % O,
        "execute unless score #x %s = @s rpg_fo_px run scoreboard players set @s rpg_fo_st 0" % O,
        "execute unless score #z %s = @s rpg_fo_pz run scoreboard players set @s rpg_fo_st 0" % O,
        "execute if score #x %s = @s rpg_fo_px if score #z %s = @s rpg_fo_pz run scoreboard players add @s rpg_fo_st 1" % (O, O),
        "scoreboard players operation @s rpg_fo_px = #x %s" % O,
        "scoreboard players operation @s rpg_fo_pz = #z %s" % O,
        "execute unless score @s rpg_fo_st matches 2.. run return 0",
    ] + sef5(["effect give @s minecraft:resistance 2 1 true"], ["effect give @s minecraft:resistance 2 0 true"]))
    fn("id/sin4", [
        "# 暴食：击杀回复 2 点生命（美丽阶起 4 点）",
        "execute unless score @s rpg_fo_kl matches 1.. run return 0",
        "scoreboard players set @s rpg_fo_kl 0",
    ] + sef5(["effect give @s minecraft:instant_health 1 0 true"], ["effect give @s minecraft:regeneration 3 1 true"]))
    wr = ["# 暴怒：每次受伤 +2%（美丽阶起 +4%），最多 5 层；8 秒不受伤清零",
          "execute if score @s rpg_fo_dw matches 1.. run scoreboard players add @s rpg_fo_ws 1",
          "execute if score @s rpg_fo_dw matches 1.. run scoreboard players operation @s rpg_fo_wt = #now %s" % O,
          "scoreboard players set @s rpg_fo_dw 0",
          "execute if score @s rpg_fo_ws matches 6.. run scoreboard players set @s rpg_fo_ws 5",
          "scoreboard players operation #q %s = #now %s" % (O, O),
          "scoreboard players operation #q %s -= @s rpg_fo_wt" % O,
          "execute if score #q %s matches 160.. run scoreboard players set @s rpg_fo_ws 0" % O,
          "attribute @s minecraft:attack_damage modifier remove rpg:fo_sin"]
    for k in range(1, 6):
        wr += sef5(["execute if score @s rpg_fo_ws matches %d run attribute @s minecraft:attack_damage modifier add rpg:fo_sin %.2f add_multiplied_total" % (k, 0.04 * k)],
                   ["execute if score @s rpg_fo_ws matches %d run attribute @s minecraft:attack_damage modifier add rpg:fo_sin %.2f add_multiplied_total" % (k, 0.02 * k)])
    fn("id/sin5", wr)
    fn("id/greed", [
        "# 贪婪：残魂与器胚掉率 +50%（美丽阶起 +100%）——每次击杀按原掉率的一半再掷一次",
        "execute store result score #r %s run random value 1..1000" % O,
        "execute if score #r %s matches ..25 run loot give @s loot rpg:forge/item/soul" % O,
        "execute if score @s rpg_sef matches 5.. if score #r %s matches 26..50 run loot give @s loot rpg:forge/item/soul" % O,
        "execute if score #r %s matches 501..505 run loot give @s loot rpg:forge/item/blank" % O,
        "execute if score @s rpg_sef matches 5.. if score #r %s matches 506..510 run loot give @s loot rpg:forge/item/blank" % O,
    ])
    # 圣灵：保惠师光环
    fn("id/s6", [
        "# 保惠师：12 格内友方生命恢复（美丽阶起 II）；每 10 秒，圣力者生命力再 +1（美丽阶起 +2）",
        "scoreboard players operation #q %s = #now %s" % (O, O),
        "scoreboard players operation #q %s /= #20 %s" % (O, O),
        "scoreboard players operation #q2 %s = #q %s" % (O, O),
        "scoreboard players operation #q %s %%= #2 %s" % (O, O),
        "scoreboard players operation #q2 %s %%= #10 %s" % (O, O),
        "execute if score #q %s matches 0 run particle minecraft:end_rod ~ ~0.3 ~ 5 0.2 5 0 10" % O,
    ] + sef5(["execute if score #q %s matches 0 run effect give @a[distance=..12,gamemode=!spectator] minecraft:regeneration 3 1 true" % O,
              "execute if score #q2 %s matches 0 run scoreboard players add @a[distance=..12,scores={rpg_force=1}] rpg_vital 2" % O,
              "execute if score #q2 %s matches 0 run scoreboard players add @a[distance=..12,scores={rpg_force=3}] rpg_vital 2" % O],
             ["execute if score #q %s matches 0 run effect give @a[distance=..12,gamemode=!spectator] minecraft:regeneration 3 0 true" % O,
              "execute if score #q2 %s matches 0 run scoreboard players add @a[distance=..12,scores={rpg_force=1}] rpg_vital 1" % O,
              "execute if score #q2 %s matches 0 run scoreboard players add @a[distance=..12,scores={rpg_force=3}] rpg_vital 1" % O]) + [
        "execute if score #q2 %s matches 0 run scoreboard players set @a[distance=..12,scores={rpg_vital=101..}] rpg_vital 100" % O,
    ])

    # 近战命中的加成（嫉妒、色欲、圣子、严厉柱对 Boss）
    fn("id/dealt", [
        "scoreboard players operation #dd %s = @s rpg_fo_d2" % O,
        "scoreboard players set @s rpg_fo_d2 0",
        "execute unless score @s rpg_ident matches 4..5 unless score @s rpg_pillar matches 1 run return 0",
        "execute store result score #ph %s run data get entity @s Health 10" % O,
        "scoreboard players set #pct %s 0" % O,
        "tag @s add rpg.fo.me",
        "execute as @e[tag=rpg.hurt,type=!minecraft:player,distance=..8,limit=1,sort=nearest] at @s run function %s" % X("id/dealt_on"),
        "tag @s remove rpg.fo.me",
    ])
    me = "@a[tag=rpg.fo.me,limit=1,scores={%s}]"
    fn("id/dealt_on", [
        "execute if entity %s run function %s" % (me % "rpg_ident=4,rpg_ident_sin=2", X("id/envy")),
        "execute if entity %s run function %s" % (me % "rpg_ident=4,rpg_ident_sin=6", X("id/lust")),
        "execute if entity %s run function %s" % (me % "rpg_ident=5", X("id/son")),
        "execute if entity %s run function %s" % (me % "rpg_pillar=1,rpg_sef=6..", X("id/vsboss")),
        "execute unless score #pct %s matches 1.. run return 0" % O,
        "scoreboard players operation #dmg %s = #dd %s" % (O, O),
        "scoreboard players operation #dmg %s *= #pct %s" % (O, O),
        "scoreboard players operation #dmg %s /= #100 %s" % (O, O),
        "execute unless score #dmg %s matches 1.. run return 0" % O,
        "execute store result storage rpg:force h.d float 0.1 run scoreboard players get #dmg %s" % O,
        hit_no,
    ])
    fn("id/envy", [
        "execute store result score #th %s run data get entity @s Health 10" % O,
        "execute unless score #th %s > #ph %s run return 0" % (O, O),
        "scoreboard players add #pct %s 10" % O,
        "execute if entity %s run scoreboard players add #pct %s 10" % (me % "rpg_sef=5..", O),
    ])
    fn("id/lust", [
        "execute unless entity %s run effect give @s minecraft:weakness 1 0 true" % (me % "rpg_sef=5.."),
        "execute if entity %s run effect give @s minecraft:weakness 2 0 true" % (me % "rpg_sef=5.."),
        "particle minecraft:dust{color:[0.85,0.48,0.85],scale:0.8} ~ ~1.2 ~ 0.2 0.3 0.2 0 4",
    ])
    fn("id/son", [
        "function %s/unholy" % P,
        "execute unless score #u %s matches 1 run return 0" % O,
        "scoreboard players add #pct %s 25" % O,
        "execute if entity %s run scoreboard players add #pct %s 25" % (me % "rpg_sef=5..", O),
    ])
    fn("id/vsboss", ["execute if entity @s[tag=%s] run scoreboard players add #pct %s 5" % (b, O) for b in F.BOSS_TAGS])
    # 技能伤害的加成（hit 里调）：圣子对恶魔与亡灵、严厉柱第 6 阶对 Boss
    fn("id/spell_mod", [
        "execute if score #u %s matches 1 if entity %s run function %s" % (O, me % "rpg_ident=5", X("id/son_spell")),
        "execute if entity %s run function %s" % (me % "rpg_pillar=1,rpg_sef=6..", X("id/boss_spell")),
    ])
    fn("id/son_spell", [
        "execute unless entity %s run scoreboard players operation #d %s *= #125 %s" % (me % "rpg_sef=5..", O, O),
        "execute if entity %s run scoreboard players operation #d %s *= #150 %s" % (me % "rpg_sef=5..", O, O),
        "scoreboard players operation #d %s /= #100 %s" % (O, O),
    ])
    fn("id/boss_spell", ["scoreboard players set #b %s 0" % O] +
       ["execute if entity @s[tag=%s] run scoreboard players set #b %s 1" % (b, O) for b in F.BOSS_TAGS] + [
        "execute unless score #b %s matches 1 run return 0" % O,
        "scoreboard players operation #d %s *= #105 %s" % (O, O),
        "scoreboard players operation #d %s /= #100 %s" % (O, O)])
    # 第三日（弥赛亚特质）
    fn("id/third_day", [
        "# 受致命伤（打完剩 5 点以内）时原地半血复生，每 20 分钟一次",
        "execute if score @s rpg_fo_3d > #now %s run return 0" % O,
        "execute store result score #h %s run data get entity @s Health" % O,
        "execute unless score #h %s matches ..5 run return 0" % O,
        "scoreboard players operation @s rpg_fo_3d = #now %s" % O,
        "scoreboard players add @s rpg_fo_3d 24000",
        "effect give @s minecraft:instant_health 1 2 true",
        "effect give @s minecraft:resistance 3 4 true",
        "effect give @s minecraft:regeneration 6 1 true",
        "playsound minecraft:block.beacon.activate player @a[distance=..24] ~ ~ ~ 1 1.8",
        "particle minecraft:totem_of_undying ~ ~1 ~ 0.4 0.8 0.4 0.4 50",
        "title @s times 5 40 15",
        "title @s title " + F.J(t("第三日", F.C_GOLD, True)),
        "title @s subtitle " + F.J(t("你从死亡里站了起来（20 分钟一次）", F.C_MUTED)),
    ])


# ============================================================================ 接到别的模块上


def wire(xh):
    # 断罪印：天平牌跟着被标记的目标；圣链：链圈；深渊之口：地面獠牙
    brand = xh.disp(VFX + "brand", pos="~ ~ ~", scale=1.7, color=0xFFD85A, billboard="center", trans=(0, -0.95, 0))
    F.add_lines("ray/mark/hit", [brand, "ride @e[tag=rpg.fo.xhnew,limit=1] mount @s"] + xh.born(160))
    chains = []
    for yaw in (0, 60, 120):
        chains.append(xh.disp(VFX + "chain", pos="~ ~1 ~", scale=(1.0, 0.01, 1.0), yaw=yaw))
        chains += xh.born(kind="chainv")
    F.add_lines("ray/chain/hit", chains)
    F.add_lines("ground/abyss/at", xh.decal(VFX + "maw_0", 5, 0xFFFFFF, pos="~ ~0.1 ~", kind="voidx") +
                xh.decal(VFX + "spiral", 3.6, 0xA276BE, pos="~ ~0.12 ~", kind="spin", life=80))
    # 第三日
    F.patch("forge/hit/hurt_player.mcfunction", X("id/third_day"),
            "execute if score @s rpg_messiah matches 1 run function %s\n" % X("id/third_day"), "end")
    # 贪婪
    F.patch("forge/kill/credit.mcfunction", X("id/greed"),
            "execute if score @s rpg_ident matches 4 if score @s rpg_ident_sin matches 7 run function %s\n" % X("id/greed"), "end")
    # 与本柱签约：契约力量的魔化代价减半
    import re
    for rel in ("pact/invoke.mcfunction", "pact/depth/second.mcfunction", "pact/depth/avatar.mcfunction"):
        s = F.read(rel)
        if "rpg_ident_sin = @s rpg_pact" in s:
            continue
        m = re.search(r"^scoreboard players add @s rpg_taint (\d+)$", s, re.M)
        assert m, rel
        half = int(m.group(1)) // 2
        s = s[:m.end()] + ("\n# 七大罪之仆与本柱立约：魔化减半（force_ext.py）\n"
                           "execute if score @s rpg_ident matches 4 if score @s rpg_ident_sin = @s rpg_pact run "
                           "scoreboard players remove @s rpg_taint %d" % half) + s[m.end():]
        F.write(rel, s)
    # 弥赛亚：教皇「收回契约」不来
    rel = "pope_fight/boss/reclaim_done.mcfunction"
    s = F.read(rel)
    if "rpg.fo.msh" not in s:
        assert "@a[distance=.." in s
        F.write(rel, s.replace("@a[distance=..", "@a[tag=!rpg.fo.msh,distance=.."))
    # 里程碑 A：燃尽时圣器保护失效；同化 50 起减半（隔刻失效）
    F.patch("command/index_player.mcfunction", "rpg.burnt] run tag @s remove rpg.holy",
            "\n# 原质（force_ext.py）：燃尽时圣器保护失效；同化 50 起减半（奇数刻失效）\n"
            "execute if entity @s[tag=rpg.holy,tag=rpg.burnt] run tag @s remove rpg.holy\n"
            "execute store result score #odd %s run time query gametime\n"
            "scoreboard players operation #odd %s %%= #2 %s\n"
            "execute if entity @s[tag=rpg.holy] if score @s rpg_assim matches 50.. if score #odd %s matches 1 run tag @s remove rpg.holy\n"
            % (O, O, O, O), "end")


def validate():
    for k in (7, 8):
        body = io.open(os.path.join(F.OUT, "page", "p%d.mcfunction" % k), encoding="utf-8").read()
        doc = json.loads(body[len("$dialog show @s "):].strip())
        assert len(doc["actions"]) == 32, (k, len(doc["actions"]))
    for n in F.EX:
        assert os.path.exists(os.path.join(F.OUT, "sk", "%d" % n, "do.mcfunction")), n
        assert os.path.exists(os.path.join(F.OUT, "sk", "%d" % n, "try.mcfunction")), n
    for b in BOSS_NAME:
        assert X("l/drop_" + b) in F.read("sephira/boss/cr_%s.mcfunction" % b), b
    assert "rpg.fo.msh" in F.read("pope_fight/boss/reclaim_done.mcfunction")


def run(mod):
    global F, P, O
    F, P, O = mod, mod.P, mod.O
    rp = sys.argv[2] if len(sys.argv) > 2 else None
    n_art = art(rp) if rp else 0
    xh, xm = engines()
    core()
    pages()
    tries()
    finishers(xh, xm)
    legacy(xh, xm)
    identity()
    wire(xh)
    xh.build()
    xm.build()
    validate()
    print("force_ext: finishers, %d lord finishers, %d legacy skills, art files %d" % (len(LORD_FIN), 6, n_art))
