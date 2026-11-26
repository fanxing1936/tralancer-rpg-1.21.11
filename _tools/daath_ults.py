# -*- coding: utf-8 -*-
"""达阿特的影子：五个大招、绝境、两个结局（docs/DAATH-DESIGN.md §4.6～4.9）。"""
import math

import onboard_spec as OB
from daath_frame import SK, start
from daath_lib import *  # noqa: F401,F403
from daath_lib import (B, DARK, DUST, DUST_D, LIGHTC, LOOK, ME, MID, NEAR, NEW, O, SIL, SIL_I, UNIT, WHITE, WHITE_I, anim, at, beam, burst, every, face, fx, light_pillar,
                       line, lines_at, msg, ring, ripple, shards, shock, snd, span, title, txt, ui, w, wave)
from daath_lib import dummy
from daath_moves import end_at, hit, slashes, tag_near
from daath_world import LAMPS, lamp_xy, POOL_R

ULTS = {(1, 1): "reflect", (1, 2): "ten", (2, 1): "ask", (2, 2): "clash", (2, 3): "shatter"}
CTR = "execute at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] run "


def build():
    for (st, i), n in ULTS.items():
        w("ult/%d_%d" % (st, i), ["tag @s add rpg.dt.u%d" % i, "function %s/eye/off" % B, "function %s/ult/%s" % (B, n)])

    # ------------------------------------------------ 倒影：从你脚下刺上来，四次
    w("ult/reflect", start("reflect") + [anim("vanish"), "data merge entity @s {NoAI:1b,Invulnerable:1b}"] + title("倒影", "Inversio") + line("S06") + [snd("rpg:daath.splinter", 1.2, 0.8), snd("entity.generic.splash", 1.4, 0.4)])
    re_ = [span(1, 20, "particle minecraft:squid_ink ~ ~0.3 ~ 0.6 0.2 0.6 0.04 8"), at(20, "function %s/reflect/hide" % B),
           "execute if score @s rpg_dt_t matches 24..200 at %s run particle %s ~ ~0.03 ~ 0.5 0.01 0.5 0 5" % (ME, DUST_D)]
    t = 50
    for gap in (34, 30, 26, 24):
        re_ += [at(t - 14, "execute at %s run function %s/reflect/mark" % (ME, B)), at(t, "function %s/reflect/spike" % B)]
        t += gap
    re_ += [at(t, "function %s/reflect/out" % B)]
    w("sk/reflect", re_)
    w("reflect/hide", ["tag @s add rpg.dt.hid", "execute on passengers if entity @s[type=minecraft:item_display] run data merge entity @s {view_range:0f}"])
    w("reflect/mark", ["# 倒影举剑：记住这一刻你站的地方（慢 0.7 秒）；站在灯下没有倒影", "execute if entity @e[type=minecraft:marker,tag=rpg.dt.pool,distance=..6] run return 0",
                       "summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.dt.fx\",\"rpg.dt.rm\"]}", "scoreboard players set @e[type=minecraft:marker,tag=rpg.dt.rm,distance=..0.5] rpg_dt_life 30",
                       "scoreboard players set @e[type=minecraft:marker,tag=rpg.dt.rm,distance=..0.5] rpg_dt_kd 0"] + fx.decal("ring", 3.2, WHITE, life=15) + dec("crack_mirror", 3.0, life=15) + [
        snd("block.sculk_sensor.clicking", 1, 0.5, 32)])
    w("reflect/spike", ["execute at @e[type=minecraft:marker,tag=rpg.dt.rm,distance=..60] run function %s/reflect/hit" % B, "kill @e[type=minecraft:marker,tag=rpg.dt.rm,distance=..60]"])
    w("reflect/hit", ["tag @a[distance=..1.7,%s] add rpg.dt.hit" % NEAR] + hit(12) + seq("ink", 4.2, "~ ~1.7 ~", "vertical") + seq("splash", 2.6, "~ ~0.8 ~", "vertical") + ripple() + [
        "particle minecraft:squid_ink ~ ~1 ~ 0.3 1 0.3 0.05 24", snd("rpg:daath.execute", 1.2, 0.9), snd("entity.generic.splash", 1, 0.7)])
    w("reflect/out", ["tag @s remove rpg.dt.hid", "execute on passengers if entity @s[type=minecraft:item_display] run data merge entity @s {view_range:1.5f}",
                      CTR + "tp @s ~ ~ ~-4", "data merge entity @s {Invulnerable:0b}", "scoreboard players set #s %s 60" % O, "function %s/stun" % B, "function %s/look/lit" % LOOK, "function %s/step/fx" % B])

    # ------------------------------------------------ 十影：九个假的，一个眼睛亮着
    w("ult/ten", start("ten") + [anim("twirl")] + title("十影", "Decem Umbrae") + line("S07") + ["function %s/lamp/all_out" % B, snd("block.beacon.deactivate", 1.2, 0.5), "data merge entity @s {NoAI:1b,Invulnerable:1b}"])
    tn = [span(1, 24, "particle minecraft:squid_ink ~ ~0.6 ~ 0.6 0.8 0.6 0.05 8"), at(24, "function %s/ten/spread" % B), at(26, "execute store result score @s rpg_dt_i run random value 0..9"),
          "execute if score @s rpg_dt_t matches 27 run function %s/ten/mine" % B,
          "execute if score @s rpg_dt_t matches 28..66 if entity @s[tag=rpg.dt.found] run return run function %s/ten/broken" % B,
          at(67, "function %s/ten/rush" % B), at(84, "function %s/ten/end" % B)]
    w("sk/ten", tn)
    sp = ["# 十根柱前各站一个剪影（item_display 光柱），本体藏进去", "execute on passengers if entity @s[type=minecraft:item_display] run data merge entity @s {view_range:0f}", "tag @s add rpg.dt.hid"]
    for i in range(10):
        x, z = lamp_xy(i, 15.5)
        sp += [CTR + "execute positioned ~%.2f ~2 ~%.2f run %s" % (x, z, ln) for ln in dummy(("rpg.dt.fx", "rpg.dt.ten", "rpg.dt.t%d" % i))]
    sp += [CTR + "execute as @e[type=minecraft:item_display,tag=rpg.dt.ten,distance=..30] at @s facing entity %s feet rotated ~ 0 run rotate @s ~ ~" % ME,
           "scoreboard players set @e[type=minecraft:item_display,tag=rpg.dt.ten,distance=..60] rpg_dt_life 80", "scoreboard players set @e[type=minecraft:item_display,tag=rpg.dt.ten,distance=..60] rpg_dt_kd 0"]
    w("ten/spread", sp + [snd("rpg:daath.mirror", 1.4, 0.8)])
    mine = ["# 真身：站到第 #i 个的位置；只有它有白眼睛"]
    for i in range(10):
        x, z = lamp_xy(i, 15.5)
        mine.append("execute if score @s rpg_dt_i matches %d %s tp @s ~%.2f ~ ~%.2f" % (i, CTR[len("execute "):].replace("run ", "run"), x, z))
        mine.append("execute if score @s rpg_dt_i matches %d run kill @e[type=minecraft:item_display,tag=rpg.dt.t%d,distance=..60]" % (i, i))
    w("ten/mine", mine + ["data merge entity @s {Invulnerable:0b}", "execute at @s run " + face(), "execute on passengers if entity @s[type=minecraft:item_display] run data merge entity @s {view_range:1.5f}",
                          "tag @s remove rpg.dt.hid", "tag @s add rpg.dt.seek", anim("guard")])
    w("ten/broken", ["# 找对了：其余立刻散掉", "tag @s remove rpg.dt.found", "tag @s remove rpg.dt.seek", "execute as @e[type=minecraft:item_display,tag=rpg.dt.ten,distance=..60] at @s run particle minecraft:smoke ~ ~1 ~ 0.3 0.6 0.3 0.02 10",
                     "kill @e[type=minecraft:item_display,tag=rpg.dt.ten,distance=..60]", "scoreboard players set #s %s 60" % O, "function %s/stun" % B, snd("block.glass.break", 1.4, 1.0)])
    w("ten/rush", ["tag @s remove rpg.dt.seek", "execute as @e[type=minecraft:item_display,tag=rpg.dt.ten,distance=..60] at @s run tp @s %s" % ME, "execute at %s run function %s/ten/fx" % (ME, B), "tag %s add rpg.dt.hit" % ME] + hit(16) + [snd("entity.player.attack.strong", 1.4, 0.6)])
    w("ten/fx", burst("~ ~1 ~", 4, DARK) + shock(MID, 8) + slashes(3.6, pos="~ ~1.2 ~"))
    w("ten/end", ["kill @e[type=minecraft:item_display,tag=rpg.dt.ten,distance=..60]", "function %s/sk/end" % B, anim("idle")])

    # ------------------------------------------------ 问：三盏灯下三个答案，只有一个是真的
    w("ult/ask", start("ask") + [anim("mighty"), "data merge entity @s {NoAI:1b,Invulnerable:1b}", CTR + "tp @s ~ ~ ~"] + title("认识你自己", "Nosce te ipsum", WHITE) + line("S11", 2) + [
        "function %s/lamp/all_out" % B, "function %s/ask/make" % B, snd("block.bell.resonate", 1.2, 0.6)])
    qs = []
    ident = {i: n for i, _k, n, _c, _d in OB.IDENTITIES}
    lords = ["没有立约", "路西法", "利维坦", "亚巴顿", "别西卜", "萨麦尔", "贝利尔", "玛门"]
    pillars = {0: "没有选柱", 1: "严厉柱", 2: "慈悲柱", 3: "中柱"}
    force = {0: "没有力", 1: "圣力", 2: "魔力", 3: "圣力与魔力"}
    # (题目, 读数, 名单或 None（数字题）)
    cat = [("你是谁？", "rpg_ident", [ident.get(i, "没有身份") for i in range(8)], 1), ("你和谁立了约？", "rpg_pact", lords, 0), ("你选了哪一根柱？", "rpg_pillar", [pillars[i] for i in range(4)], 0),
           ("你的力从哪里来？", "rpg_force", [force[i] for i in range(4)], 0)]
    num = [("你杀过多少精英？", "rpg_el_kill"), ("你完成过几次裁决？", "rpg_ex_rites"), ("你死过几次？", "rpg_dt_de"), ("你的阅历是多少？", "rpg_ex_xp")]
    mk = ["# 抽一道题，三个答案放进 t.a0 t.a1 t.a2（a0 是真的），再打乱", "execute store result score #q %s run random value 0..%d" % (O, len(cat) + len(num) - 1)]
    for i in range(len(cat) + len(num)):
        mk.append("execute if score #q %s matches %d run function %s/ask/q%d" % (O, i, B, i))
    for i, (q, sco, names, base) in enumerate(cat):
        n = len(names)
        ls = ["data modify storage rpg:daath t.q set value \"%s\"" % q, "scoreboard players set #v %s 0" % O, "execute store result score #v %s run scoreboard players get %s %s" % (O, ME, sco),
              "execute store result score #r %s run random value 1..%d" % (O, max(1, n - 2 - base)), "scoreboard players set #mod %s %d" % (O, n),
              "scoreboard players operation #v1 %s = #v %s" % (O, O), "scoreboard players operation #v1 %s += #r %s" % (O, O), "scoreboard players operation #v2 %s = #v1 %s" % (O, O), "scoreboard players add #v2 %s 1" % O]
        for a in ("#v1", "#v2"):
            ls.append("scoreboard players operation %s %s %%= #mod %s" % (a, O, O))
        if base:
            ls += ["execute if score #v1 %s matches 0 run scoreboard players add #v1 %s 1" % (O, O), "execute if score #v2 %s matches 0 run scoreboard players add #v2 %s 2" % (O, O),
                   "execute if score #v1 %s = #v %s run scoreboard players add #v1 %s 1" % (O, O, O), "execute if score #v2 %s = #v %s run scoreboard players add #v2 %s 1" % (O, O, O),
                   "execute if score #v2 %s = #v1 %s run scoreboard players add #v2 %s 1" % (O, O, O),
                   "execute if score #v1 %s matches %d.. run scoreboard players set #v1 %s 1" % (O, n, O), "execute if score #v2 %s matches %d.. run scoreboard players set #v2 %s 2" % (O, n, O)]
        for j, (nm) in enumerate(names):
            for k, v in (("a0", "#v"), ("a1", "#v1"), ("a2", "#v2")):
                ls.append("execute if score %s %s matches %d run data modify storage rpg:daath t.%s set value \"%s\"" % (v, O, j, k, nm))
        w("ask/q%d" % i, ls)
    for i, (q, sco) in enumerate(num):
        w("ask/q%d" % (len(cat) + i), ["data modify storage rpg:daath t.q set value \"%s\"" % q, "scoreboard players set #v %s 0" % O, "execute store result score #v %s run scoreboard players get %s %s" % (O, ME, sco),
                                       "execute store result score #r %s run random value 1..4" % O, "scoreboard players operation #v1 %s = #v %s" % (O, O), "scoreboard players operation #v1 %s += #r %s" % (O, O),
                                       "execute store result score #r %s run random value 1..3" % O, "scoreboard players operation #v2 %s = #v %s" % (O, O), "scoreboard players operation #v2 %s -= #r %s" % (O, O),
                                       "execute if score #v2 %s matches ..-1 run scoreboard players operation #v2 %s = #v1 %s" % (O, O, O), "execute if score #v2 %s = #v1 %s run scoreboard players add #v2 %s 2" % (O, O, O)] +
          ["execute store result storage rpg:daath t.%s int 1 run scoreboard players get %s %s" % (k, v, O) for k, v in (("a0", "#v"), ("a1", "#v1"), ("a2", "#v2"))])
    mk += ["execute store result score @s rpg_dt_q run random value 0..2",
           "function %s/ask/show with storage rpg:daath t" % B]
    w("ask/make", mk)
    # 三个位置：12 格外，相隔 120°；真的在第 rpg_dt_q 个
    pos = [(11 * math.cos(2 * math.pi * k / 3 - math.pi / 2), 11 * math.sin(2 * math.pi * k / 3 - math.pi / 2)) for k in range(3)]
    show = ["$title %s times 5 60 10" % ME, "$title %s subtitle {\"text\":\"$(q)\",\"color\":\"%s\",\"italic\":false}" % (ME, WHITE), "$title %s title {\"text\":\"\"}" % ME,
            "$tellraw %s [\"\",{\"text\":\"〖\",\"color\":\"#7C8593\",\"bold\":true},{\"selector\":\"%s\",\"color\":\"#FFFFFF\",\"bold\":true},{\"text\":\"〗　\",\"color\":\"#7C8593\",\"bold\":true},{\"text\":\"$(q)\",\"color\":\"%s\",\"bold\":false}]" % (ME, ME, ui.BROADCAST_NAME)]
    for q in range(3):
        for k in range(3):
            a = (k - q) % 3
            show.append("$execute if score @s rpg_dt_q matches %d at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] positioned ~%.2f ~ ~%.2f run function %s/ask/card {x:\"$(a%d)\",k:%d}" % (q, pos[k][0], pos[k][1], B, a, k))
    w("ask/show", show)
    w("ask/card", ["$summon minecraft:text_display ~ ~2.6 ~ {Tags:[\"rpg.dt.fx\",\"rpg.dt.card\",\"rpg.dt.cnew\"],text:{\"text\":\"$(x)\",\"color\":\"#FFFFFF\",\"bold\":true},background:-1441722342,billboard:\"center\",brightness:{sky:15,block:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,2f,2f],right_rotation:[0f,0f,0f,1f]}}",
                   "$summon minecraft:marker ~ ~ ~ {Tags:[\"rpg.dt.fx\",\"rpg.dt.card\",\"rpg.dt.cnew\",\"rpg.dt.k$(k)\",\"rpg.dt.km\"]}",
                   "scoreboard players set @e[tag=rpg.dt.cnew,distance=..4] rpg_dt_life 170", "scoreboard players set @e[tag=rpg.dt.cnew,distance=..4] rpg_dt_kd 0", "tag @e[tag=rpg.dt.cnew,distance=..4] remove rpg.dt.cnew"] +
      dec("seal_question", 6, life=130, kind="spinf", tags=("rpg.dt.card",)) + fx.decal("ring", 6, WHITE, pos="~ ~0.07 ~", life=130, tags=("rpg.dt.card",)) + [snd("block.amethyst_block.chime", 1, 0.8)])
    ak = every(20) + ["execute if score @s rpg_dt_t matches 10..110 if score #m %s matches 0 run %s" % (O, snd("block.note_block.hat", 0.8, 0.8)), at(122, "function %s/ask/judge" % B), end_at(176)]
    w("sk/ask", ak)
    jd = ["# 判：站在真的那张牌 3.2 格里"]
    for q in range(3):
        jd.append("execute if score @s rpg_dt_q matches %d at @e[type=minecraft:marker,tag=rpg.dt.k%d,distance=..60,limit=1] if entity @a[tag=rpg.dt.me,distance=..3.2] run tag @s add rpg.dt.right" % (q, q))
    jd += ["execute as @e[type=minecraft:marker,tag=rpg.dt.km,distance=..60] at @s run function %s/ask/burst" % B]
    for q in range(3):
        jd.append("execute if score @s rpg_dt_q matches %d at @e[type=minecraft:marker,tag=rpg.dt.k%d,distance=..60,limit=1] run function %s/ask/truth" % (q, q, B))
    jd += ["data merge entity @s {Invulnerable:0b}", "execute if entity @s[tag=rpg.dt.right] run return run function %s/ask/yes" % B, "function %s/ask/no" % B]
    w("ask/judge", jd)
    w("ask/burst", ["particle minecraft:squid_ink ~ ~1.5 ~ 1.2 1.2 1.2 0.1 60 force", snd("entity.generic.explode", 0.6, 1.2)] + shock(MID, 7))
    w("ask/truth", light_pillar(LIGHTC) + ["particle minecraft:end_rod ~ ~1.5 ~ 0.8 1.2 0.8 0.05 40 force"])
    w("ask/yes", ["tag @s remove rpg.dt.right"] + line("S12", 2) + ["kill @e[tag=rpg.dt.card,distance=..60]", "scoreboard players set #s %s 100" % O, "function %s/stun" % B, snd("block.beacon.power_select", 1, 1.4)])
    w("ask/no", line("S13", 2) + ["kill @e[tag=rpg.dt.card,distance=..60]", "tag %s add rpg.dt.hit" % ME] + hit(20) + ["function %s/sk/end" % B, "scoreboard players set @s rpg_dt_gap 30"])

    # ------------------------------------------------ 同一把剑：最后 0.6 秒出手，两把武器相撞
    w("ult/clash", start("clash") + ["function %s/weapon/pick_melee" % B, anim("mighty"), face(), "data merge entity @s {NoAI:1b,Invulnerable:0b}"] + title("同一把剑", "Idem Gladius", WHITE) + line("S14", 2) + [
        "function %s/clash/back" % B, "tag @s add rpg.dt.clash"])
    w("clash/back", ["# 退到 7 格外", "execute at %s facing entity @s feet rotated ~ 0 positioned ^ ^ ^7 if entity @e[type=minecraft:marker,tag=rpg.dt.c,distance=..22] run tp @s ~ ~ ~" % ME, face()])
    cl = [span(1, 58, face()), "execute if score @s rpg_dt_t matches 10..60 at @s run particle minecraft:end_rod ^ ^1.2 ^3.5 0.05 0.05 1.6 0 2"]
    for t in (10, 22, 34, 44, 52):
        cl.append(at(t, "function %s/clash/pulse" % B))
    cl += [at(52, "execute at %s run summon minecraft:interaction ~ ~-0.5 ~ {Tags:[\"rpg.dt.clk\"],width:4f,height:4f,response:0b}" % ME),
           span(53, 66, "execute if entity @s[tag=rpg.dt.window] run function %s/clash/listen" % B),
           at(67, "kill @e[type=minecraft:interaction,tag=rpg.dt.clk,distance=..60]"), at(52, "tag @s add rpg.dt.window"), at(52, "playsound minecraft:block.bell.use hostile @a[distance=..48] ~ ~ ~ 1 1.6"), at(60, anim("cl3")), at(66, "function %s/clash/fall" % B), end_at(96)]
    w("sk/clash", cl)
    w("clash/pulse", ["execute positioned ~ ~0.07 ~ run %s" % c for c in beam(0xFFFFFF, (0.3, 0.02, 7.0), (0, 0, 3.5))] + fx.born(10) + fx.twinkle("^-0.4 ^1.8 ^0.4", WHITE) + [snd("block.note_block.bell", 1, 0.6)])
    w("clash/fall", ["tag @s remove rpg.dt.window", "tag @s remove rpg.dt.clash", "execute at %s rotated ~ 0 run tp @s ^ ^ ^1.8" % ME, face(), tag_near(6)] + hit(24) + ["execute at %s run function %s/clash/boom" % (ME, B)])
    w("clash/boom", burst("~ ~1 ~", 5, WHITE) + shock(SIL, 12) + dec("crack_mirror", 8, life=60) + [snd("entity.generic.explode", 1, 0.8), snd("item.mace.smash_ground_heavy", 1.4, 0.6)])
    w("clash/win", ["# 相撞成功（as 影子）", "tag @s remove rpg.dt.window", "tag @s remove rpg.dt.clash", "execute at %s positioned ~ ~ ~ run function %s/clash/spark" % (ME, B),
                    "kill @e[type=minecraft:interaction,tag=rpg.dt.clk,distance=..60]", "scoreboard players set #s %s 80" % O, "function %s/stun" % B])
    w("clash/spark", burst("~ ~1.3 ~", 4.5, WHITE) + shards(12, 1.2, 0.8) + fx.decal("ring", 1, WHITE, kind="ringw") + [
        "particle minecraft:flash{color:16777215} ~ ~1.3 ~ 0 0 0 0 1 force", snd("item.shield.block", 1.4, 0.7), snd("block.bell.use", 1.4, 0.6), snd("item.mace.smash_ground", 1, 1.2)])
    # 挥空也算出手：近战打到任何东西 / 灯 / 交互体都算；另给一个跟随的交互体接住这一击
    w("clash/listen", ["execute at %s run tp @e[type=minecraft:interaction,tag=rpg.dt.clk,distance=..20] ~ ~-0.5 ~" % ME, "scoreboard players set #w %s 0" % O,
                       "execute as @e[type=minecraft:interaction,tag=rpg.dt.clk,distance=..30] if data entity @s attack run scoreboard players set #w %s 1" % O,
                       "execute as @e[type=minecraft:interaction,tag=rpg.dt.clk,distance=..30] if data entity @s interaction run scoreboard players set #w %s 1" % O,
                       "execute if score #w %s matches 1 run function %s/clash/win" % (O, B)])

    # ------------------------------------------------ 碎镜：二十四片，先亮的先翻
    w("ult/shatter", start("shatter") + [anim("gong"), "data merge entity @s {NoAI:1b,Invulnerable:1b}", CTR + "tp @s ~ ~ ~"] + title("碎镜", "Speculum Fractum", WHITE) + line("S15", 2) + [snd("block.glass.break", 1.6, 0.5)])
    # 场地切成 24 个扇形格：内圈 8（4～11 格）、外圈 16（11～23 格）；中间 4 格是稳的
    cells = [(1, k) for k in range(8)] + [(2, k) for k in range(16)]
    waves = [[c for j, c in enumerate(cells) if (j * 7 + (j // 8)) % 4 == g] for g in range(4)]
    sh = []
    for g in range(4):
        t0 = 24 + g * 30
        sh += [at(t0, CTR + "function %s/shatter/warn%d" % (B, g)), at(t0 + 22, CTR + "function %s/shatter/flip%d" % (B, g))]
    sh += ["execute if score @s rpg_dt_t matches 24..140 run particle minecraft:end_rod ~ ~0.5 ~ 1.2 0.2 1.2 0.01 2", at(150, "data merge entity @s {Invulnerable:0b}"), at(150, anim("kneel")), end_at(190)]
    w("sk/shatter", sh)
    for g in range(4):
        warn, flip = [], ["# 第 %d 批翻面" % (g + 1)]
        for ringn, k in waves[g]:
            n, r = (8, 7.5) if ringn == 1 else (16, 17)
            a = 2 * math.pi * k / n
            x, z = r * math.cos(a), r * math.sin(a)
            size = 5.6 if ringn == 1 else 7.0
            warn += ["execute positioned ~%.2f ~ ~%.2f run function %s/shatter/w%d" % (x, z, B, ringn)]
            flip += ["execute positioned ~%.2f ~ ~%.2f run function %s/shatter/f%d" % (x, z, B, ringn)]
            size
        w("shatter/warn%d" % g, warn + [snd("block.glass.step", 1.6, 0.6)])
        w("shatter/flip%d" % g, flip + ["execute as @a[tag=rpg.dt.hit] at @s run effect give @s minecraft:levitation 1 4 true"] + hit(12) + [snd("block.glass.break", 1.4, 0.7), snd("entity.generic.splash", 0.8, 0.5)])
    for ringn, size, rad in ((1, 5.4, 2.7), (2, 6.6, 3.2)):
        w("shatter/w%d" % ringn, dec("crack_mirror", size, life=22) + fx.decal("ring", size, MID, pos="~ ~0.07 ~", life=22))
        w("shatter/f%d" % ringn, ["tag @a[distance=..%s,%s] add rpg.dt.hit" % (rad, NEAR)] + [fx.disp("hexagon", pos="~ ~0.4 ~", scale=(size, 1, size), color=SIL_I)] + fx.born(kind="tile") + [
            "particle minecraft:block{block_state:\"minecraft:black_stained_glass\"} ~ ~0.4 ~ 1.2 0.4 1.2 0.2 20"])


def despair():
    """绝境「谁是影子」：走到它面前，潜行站住两秒。"""
    w("despair/begin", ["tag @s add rpg.dt.desp", "tag @s add rpg.dt.mute", "scoreboard players set @s rpg_dt_t 0", "scoreboard players set @s rpg_dt_i 0", "function %s/unit/refill" % B, "function %s/hp_low" % B,
                        "data merge entity @s {NoAI:1b,Invulnerable:1b}", "execute if score @s rpg_dt_sw matches 1.. run function %s/steal/lose_w" % B, "execute if score @s rpg_dt_sa matches 1.. run function %s/steal/lose_a" % B,
                        "function %s/eye/off" % B, "kill @e[type=minecraft:zombie,tag=rpg.dt.minion,distance=..60]", "stopsound %s record" % ME, anim("walk"), "effect give %s minecraft:blindness 1 0 true" % ME,
                        "execute as %s at @s run playsound minecraft:entity.warden.heartbeat record @s ~ ~ ~ 1 0.8" % ME] + title("谁是影子", "Quis Umbra", WHITE) + line("S16", 2))
    w("hp_low", ["# 绝境里血条停在一成", "scoreboard players operation @s rpg_dt_h = @s rpg_dt_mx", "function %s/bar/set" % B])
    d = ["scoreboard players add @s rpg_dt_t 1", face(),
         "execute unless entity @a[tag=rpg.dt.me,distance=..2.4] if score @s rpg_dt_t matches 30.. at @s run tp @s ^ ^ ^0.05"] + every(26) + [
        "execute if score #m %s matches 0 as %s at @s run playsound minecraft:entity.warden.heartbeat record @s ~ ~ ~ 1 0.7" % (O, ME),
        "execute at %s run particle minecraft:smoke ~ ~0.3 ~ 0.4 0.25 0.4 0.005 3" % ME,
        "execute if score #m %s matches 0 run particle minecraft:end_rod ~ ~1.1 ~ 0.4 0.8 0.4 0.005 3" % O,
        "title %s actionbar %s" % (ME, ui.row(ui.comp("它在等你走过去。潜行，站在它面前。", SIL)))] + lines_at(70, "S17", 2) + lines_at(130, "S18", 2) + [
        "execute unless entity @a[tag=rpg.dt.me,distance=..2.8,predicate=rpg:sneaking] run scoreboard players set @s rpg_dt_i 0",
        "execute if entity @a[tag=rpg.dt.me,distance=..2.8,predicate=rpg:sneaking] run scoreboard players add @s rpg_dt_i 1",
        "execute if score @s rpg_dt_i matches 40.. run return run function %s/despair/met" % B,
        "execute if score @s rpg_dt_t matches 240.. run function %s/despair/missed" % B]
    w("despair/tick", d)
    w("despair/met", ["tag @s remove rpg.dt.desp", "tag @s add rpg.dt.despdone", "function %s/end/begin" % B])
    w("despair/missed", ["# 没走过去：回一成血再打一轮；第三次直接进结局", "scoreboard players add @s rpg_dt_dsp 1", "execute if score @s rpg_dt_dsp matches 3.. run return run function %s/despair/met" % B,
                         "tag @s remove rpg.dt.desp", "tag @s remove rpg.dt.mute", "scoreboard players set @s rpg_dt_bgm 0", "function %s/sk/end" % B, "function %s/despair/heal" % B, anim("idle"), "scoreboard players set @s rpg_dt_gap 20"])
    w("despair/heal", ["scoreboard players operation #h %s = @s rpg_dt_mx" % O, "scoreboard players set #k %s 2" % O, "scoreboard players operation #h %s *= #k %s" % (O, O),
                       "scoreboard players operation @s rpg_dt_h = #h %s" % O, "function %s/bar/set" % B])

    # ------------------------------------------------ 结局：斩断 / 接纳
    w("end/begin", ["tag @s add rpg.dt.end", "tag @s remove rpg.dt.window", "scoreboard players set @s rpg_dt_t 0", "scoreboard players set @s rpg_dt_q 0", "data merge entity @s {NoAI:1b,Invulnerable:1b}",
                    "function %s/weapon/none" % B, "function %s/bar/zero" % B, "kill @e[tag=rpg.dt.fx,distance=..60]", anim("kneel"), "stopsound %s record" % ME,
                    "summon minecraft:interaction ~ ~ ~ {Tags:[\"rpg.dt.touch\"],width:1.6f,height:2.4f,response:1b}",
                    "execute as %s run %s" % (ME, msg([txt("它跪下了。攻击它，", SIL), txt("斩断", "#FF5A62", True), txt("；空手右键，", SIL), txt("接纳", "#62B8F0", True), txt("。", SIL)]))])
    w("bar/zero", ["scoreboard players set @s rpg_dt_h 0", "function %s/bar/set" % B])
    w("end/tick", ["scoreboard players add @s rpg_dt_t 1", "execute if score @s rpg_dt_q matches 1 run return run function %s/end/sever" % B, "execute if score @s rpg_dt_q matches 2 run return run function %s/end/accept" % B,
                   "execute if score @s rpg_dt_t matches ..20 run return 0",
                   "particle %s ~ ~0.8 ~ 0.4 0.6 0.4 0 1" % DUST,
                   "execute as @e[type=minecraft:interaction,tag=rpg.dt.touch,distance=..4,limit=1] if data entity @s attack run scoreboard players set @e[%s,tag=rpg.dt.it] rpg_dt_q 1" % UNIT,
                   "execute as @e[type=minecraft:interaction,tag=rpg.dt.touch,distance=..4,limit=1] if data entity @s interaction run scoreboard players set @e[%s,tag=rpg.dt.it] rpg_dt_q 2" % UNIT,
                   "execute if score @s rpg_dt_t matches 1200.. run scoreboard players set @s rpg_dt_q 2",
                   "execute if score @s rpg_dt_q matches 1.. run function %s/end/pick" % B])
    w("end/pick", ["kill @e[type=minecraft:interaction,tag=rpg.dt.touch,distance=..6]", "scoreboard players set @s rpg_dt_t 0", "execute unless score %s rpg_dt_die matches 1.. run scoreboard players operation %s rpg_dt_die = @s rpg_dt_q" % (ME, ME)])
    w("end/sever", lines_at(4, "S19", 2) + [at(4, "function %s/end/cut" % B), at(26, anim("fall")), span(30, 60, "function %s/end/flake" % B), at(62, "function %s/end/finish" % B)])
    w("end/cut", slashes(4, color=WHITE, pos="~ ~1.2 ~") + burst("~ ~1.2 ~", 3.4, WHITE) + shards(14, 0.8, 0.6) + [snd("block.glass.break", 1.6, 0.7), snd("entity.player.attack.crit", 1, 0.6)])
    w("end/flake", ["particle minecraft:end_rod ~ ~0.8 ~ 0.4 0.5 0.4 0.03 2", "particle %s ~ ~0.8 ~ 0.4 0.6 0.4 0 6" % DUST])
    w("end/accept", lines_at(6, "S20", 2) + [at(6, anim("hero")), span(10, 50, "execute facing entity %s feet rotated ~ 0 unless entity @a[tag=rpg.dt.me,distance=..0.6] run tp @s ^ ^ ^0.06 ~ ~" % ME),
                                             span(10, 60, "particle minecraft:end_rod ~ ~1 ~ 0.4 0.8 0.4 0.02 3"), at(52, "function %s/end/merge" % B), at(62, "function %s/end/finish" % B)])
    w("end/merge", ["execute at %s run function %s/end/mergefx" % (ME, B), "execute on passengers run data merge entity @s {view_range:0f}",
                    CTR + "function %s/arena/tree_lit" % B])
    w("end/mergefx", light_pillar(LIGHTC) + burst("~ ~1.1 ~", 4.4, "#FFF2A8") + ["particle minecraft:end_rod ~ ~1 ~ 0.5 1 0.5 0.15 80 force", snd("block.beacon.activate", 1.4, 1.2), snd("block.amethyst_block.resonate", 1.4, 0.8)])
    quote = ui.row(ui.comp("〖哥林多前书 13:12〗", ui.BROADCAST_HOLY, True), ui.comp(ui.GAP, ui.BROADCAST_BODY), ui.comp("我们如今仿佛对着镜子观看，模糊不清；到那时，就要面对面了。", ui.BROADCAST_NAME))
    w("end/finish", ["tellraw %s %s" % (ME, quote), "execute as %s run function %s/end/mine" % (ME, B), "scoreboard players set %s rpg_dt_ph 4" % ME, "scoreboard players set %s rpg_dt_pt 0" % ME, "function %s/unit/vanish" % B])
    w("end/mine", ["# 称号（第一次的选择算数）", "execute if score @s rpg_dt_die matches 1 run function rpg:quest/title/get_sever", "execute if score @s rpg_dt_die matches 2 run function rpg:quest/title/get_mirror"])
    for n in ("reflect", "ten", "ask", "clash", "shatter"):
        w("debug/ult/%s" % n, ["# 调试：立刻放这个大招（as/at 玩家）", "execute as @e[%s,distance=..80,limit=1,sort=nearest] at @s rotated ~ 0 run function %s/debug/as_%s" % (UNIT, B, n)])
        w("debug/as_%s" % n, ["tag @s add rpg.dt.it", "tag @p[tag=rpg.dt.in,distance=..90] add rpg.dt.me", "function %s/sk/end" % B, "function %s/ult/%s" % (B, n), "tag @a remove rpg.dt.me", "tag @s remove rpg.dt.it"])
    w("debug/stage2", ["# 调试：影子直接到一段底线", "execute as @e[%s,distance=..80,limit=1,sort=nearest] run function %s/debug/low" % (UNIT, B)])
    w("debug/low", ["scoreboard players set @s rpg_dt_h 10"])
    w("debug/despair", ["execute as @e[%s,distance=..80,limit=1,sort=nearest] at @s rotated ~ 0 run function %s/debug/as_despair" % (UNIT, B)])
    w("debug/as_despair", ["scoreboard players set @s rpg_dt_st 2", "function %s/debug/low" % B])
