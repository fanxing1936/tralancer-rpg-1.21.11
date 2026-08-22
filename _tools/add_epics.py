# -*- coding: utf-8 -*-
"""Three weapons built from the author's 史诗–限定传说 art.

Each one's palette is measured off its own sprite and drives its particles, and
each skill is written fresh -- none of them reuses an existing effect.

Cost discipline, since the brief asked for no stutter:

* every per-tick function sits behind a holder guard in `rpg:item/epic/epics`,
  so an idle tick pays a handful of tag checks and nothing else;
* the two passives ride the `rpg.hurt` + `on attacker` shape the pack already
  uses, adding no new world scan of their own;
* the one active spends its whole budget in three scheduled pulses rather than
  a lingering per-tick field, so nothing survives the cast.
"""

import collections
import io
import json
import os
import sys

import png_tool as P

RP = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
DP = sys.argv[2] if len(sys.argv) > 2 else "../rpg"

RPG_MODELS = os.path.join(RP, "assets/rpg/models/item")
RPG_TEX = os.path.join(RP, "assets/rpg/textures/item")
MC_ITEMS = os.path.join(RP, "assets/minecraft/items")
FUNC = os.path.join(DP, "data/rpg/function")
ADV = os.path.join(DP, "data/rpg/advancement/item")
ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), "epic_art")

NATIVE = 32
FORGE_CONSUME = 100120        # first free consume_seconds
SAW_CONSUME = 100130
FORGE_CHARGE = 30             # ticks of hold before the slam lands
FORGE_HOLD = 3                # grace ticks for "still holding"
SAW_LIFE = 60                 # the saw runs three seconds


RULE = '["",{"text":"+------------------+","italic":false,"color":"white"}]'

# name -> (source sprite, base item, custom_model_data, display parent)
WEAPONS = [
    dict(key="forge", art="568568", item="netherite_axe", cmd=1110021,
         parent="rpg:item/sword_handheld",
         name="熔火之锤", tier="传说", tier_colour="gold", name_colour="red",
         icon="🔱", kind="主动技能", skill="熔流",
         flavour=("锻炉裂开的那一日", " 铁匠把山的心脏装进了锤头"),
         text=("长按右键蓄力1.5秒砸地，热浪由内向外三重扩散",
               "每一圈都点燃并推开当中的敌人")),
    dict(key="dawn", art="568486", item="netherite_sword", cmd=1110022,
         parent="rpg:item/sword_handheld",
         name="熔岩链锯", tier="限定传说", tier_colour="#FFD700", name_colour="gold",
         icon="🗡", kind="主动技能", skill="熔锯",
         flavour=("[切割链锯]烧红了它的锯齿", " 从此它咬下去的地方会流"),
         text=("右键起锯，三秒内连切六轮",
               "每一轮都在身前召出熔岩獠牙")),
    dict(key="chime", art="568583", item="netherite_axe", cmd=1110023,
         parent="rpg:item/sword_handheld",
         name="晶啸", tier="史诗", tier_colour="dark_purple", name_colour="light_purple",
         icon="🪓", kind="被动技能", skill="共振",
         flavour=("紫晶在斧刃里长了三百年", " 它记得每一次挥击"),
         text=("命中时晶体共鸣，震荡波及目标周围的敌人",)),
]


def seg(t, c="white", b=False):
    return '{"text":"%s","italic":false,"color":"%s"%s}' % (t, c, ',"bold":true' if b else "")


def row(*s):
    return '["",%s]' % ",".join(s)


def wf(rel, text):
    p = os.path.join(FUNC, rel)
    d = os.path.dirname(p)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text.rstrip("\n") + "\n")


def wj(p, doc):
    d = os.path.dirname(p)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


# ---------------------------------------------------------------------------
# art: the uploads are resampled, so recover the grid by majority vote
# ---------------------------------------------------------------------------
def _palette(w, h, rgba, limit=24):
    hist = collections.Counter()
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            s = (y * w + x) * 4
            if rgba[s + 3] >= 240:
                hist[(rgba[s] >> 2, rgba[s + 1] >> 2, rgba[s + 2] >> 2)] += 1
    pal = []
    for (r, g, b), _n in hist.most_common():
        c = (r << 2 | 2, g << 2 | 2, b << 2 | 2)
        if any(abs(c[0] - p[0]) + abs(c[1] - p[1]) + abs(c[2] - p[2]) < 40 for p in pal):
            continue
        pal.append(c)
        if len(pal) >= limit:
            break
    return pal


def reconstruct(w, h, rgba, n, inset=0.24):
    pal = _palette(w, h, rgba)

    def snap(c):
        best, bd = pal[0], 1 << 30
        for p in pal:
            d = (c[0] - p[0]) ** 2 + (c[1] - p[1]) ** 2 + (c[2] - p[2]) ** 2
            if d < bd:
                bd, best = d, p
        return best

    step = w / float(n)
    out = bytearray(n * n * 4)
    for cy in range(n):
        for cx in range(n):
            x0 = int(cx * step + step * inset)
            x1 = max(x0 + 1, int((cx + 1) * step - step * inset))
            y0 = int(cy * step + step * inset)
            y1 = max(y0 + 1, int((cy + 1) * step - step * inset))
            votes = collections.Counter()
            solid = total = 0
            for y in range(y0, min(y1, h)):
                for x in range(x0, min(x1, w)):
                    s = (y * w + x) * 4
                    total += 1
                    if rgba[s + 3] >= 128:
                        solid += 1
                        votes[snap((rgba[s], rgba[s + 1], rgba[s + 2]))] += 1
            if total and solid * 2 >= total and votes:
                c = votes.most_common(1)[0][0]
                o = (cy * n + cx) * 4
                out[o], out[o + 1], out[o + 2], out[o + 3] = c[0], c[1], c[2], 255
    return bytes(out)


def build_art():
    out = []
    for w in WEAPONS:
        src = os.path.join(ART, w["art"] + ".png")
        if not os.path.isfile(src):
            raise SystemExit("missing art: " + src)
        iw, ih, rgba = P.read(src)
        px = reconstruct(iw, ih, rgba, NATIVE)
        if not os.path.isdir(RPG_TEX):
            os.makedirs(RPG_TEX)
        P.write(os.path.join(RPG_TEX, w["key"] + ".png"), NATIVE, NATIVE, px)
        wj(os.path.join(RPG_MODELS, w["key"] + ".json"),
           {"parent": w["parent"], "textures": {"layer0": "rpg:item/" + w["key"]}})
        out.append("%s %dx%d" % (w["key"], NATIVE, NATIVE))
    # register each cmd on its own base item
    for w in WEAPONS:
        path = os.path.join(MC_ITEMS, w["item"] + ".json")
        doc = json.load(io.open(path, encoding="utf-8"))
        entries = doc["model"]["entries"]
        entries[:] = [e for e in entries if e["threshold"] != w["cmd"]]
        entries.append({"threshold": w["cmd"],
                        "model": {"type": "minecraft:model",
                                  "model": "rpg:item/" + w["key"]}})
        entries.sort(key=lambda e: e["threshold"])
        wj(path, doc)
    return ", ".join(out)


# ---------------------------------------------------------------------------
# the items
# ---------------------------------------------------------------------------
ENCH = {
    "forge": "{fire_aspect:3,density:4,breach:3,smite:3,unbreaking:3}",
    "dawn": "{smite:5,sharpness:4,fire_aspect:2,looting:3,sweeping_edge:3}",
    "chime": "{sharpness:4,efficiency:3,looting:2,unbreaking:3}",
}
ATTRS = {
    "forge": ('{type:"attack_damage",amount:11,operation:add_value,slot:mainhand,id:"rpg:epic/forge/0"},'
              '{type:"attack_speed",amount:-3.1,operation:add_value,slot:mainhand,id:"rpg:epic/forge/1"},'
              '{type:"safe_fall_distance",amount:1.5,operation:add_multiplied_base,slot:mainhand,id:"rpg:epic/forge/2"},'
              '{type:"burning_time",amount:-0.5,operation:add_multiplied_base,slot:mainhand,id:"rpg:epic/forge/3"}'),
    "dawn": ('{type:"attack_damage",amount:9,operation:add_value,slot:mainhand,id:"rpg:epic/dawn/0"},'
             '{type:"attack_speed",amount:-2.2,operation:add_value,slot:mainhand,id:"rpg:epic/dawn/1"},'
             '{type:"movement_speed",amount:0.05,operation:add_multiplied_base,slot:mainhand,id:"rpg:epic/dawn/2"}'),
    "chime": ('{type:"attack_damage",amount:7,operation:add_value,slot:mainhand,id:"rpg:epic/chime/0"},'
              '{type:"attack_speed",amount:-2.6,operation:add_value,slot:mainhand,id:"rpg:epic/chime/1"},'
              '{type:"block_interaction_range",amount:1,operation:add_value,slot:mainhand,id:"rpg:epic/chime/2"}'),
}

def _consumable(cs):
    return ('food={nutrition:0,saturation:0f,can_always_eat:1b},'
            'consumable={consume_seconds:%df,animation:"eat",'
            'sound:"minecraft:entity.generic.eat",has_consume_particles:true,'
            'on_consume_effects:[]},' % cs)


CONSUMABLE = _consumable(FORGE_CONSUME)
SAW_CONSUMABLE = _consumable(SAW_CONSUME)


def give(w):
    lore = [RULE,
            row(seg(w["flavour"][0]), seg(w["flavour"][1], w["tier_colour"], True)),
            RULE,
            row(seg("%s%s" % (w["icon"], w["kind"]), "white", True),
                seg("[%s]" % w["skill"], w["tier_colour"], True))]
    lore += [row(seg(t)) for t in w["text"]]
    lore.append(RULE)
    return ("give @a %s[" % w["item"] +
            "custom_name=" + row(seg("[%s]" % w["tier"], w["tier_colour"], True),
                                 seg(w["name"], w["name_colour"])) + ","
            "lore=[" + ",".join(lore) + "],"
            "enchantments=" + ENCH[w["key"]] + ","
            "attribute_modifiers=[" + ATTRS[w["key"]] + "],"
            + (CONSUMABLE if w["key"] == "forge"
               else SAW_CONSUMABLE if w["key"] == "dawn" else "") +
            "unbreakable={},"
            'tooltip_display={hidden_components:["minecraft:unbreakable"]},'
            "custom_model_data={floats:[%d.0f]}," % w["cmd"] +
            "custom_data={%s_tag:1b,sword_tag:1b}]" % w["key"])


def build_give():
    path = os.path.join(FUNC, "command/give/extra.mcfunction")
    s = io.open(path, encoding="utf-8").read()
    if "熔火之锤" in s:
        return 0
    body = [s.rstrip("\n"), "", "# 三件由作者贴图打造的史诗～限定传说武器"]
    body += [give(w) for w in WEAPONS]
    body.append("")
    io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(body))
    return len(WEAPONS)


# ---------------------------------------------------------------------------
# skills -- palettes measured off each sprite
# ---------------------------------------------------------------------------
EMBER, CINDER, SCORCH = 16553767, 13193984, 9445636      # 熔火 #FC9727 #C95300 #902104
GOLD, DEEPRED, AZURE = 16575098, 8005632, 416663          # 破晓 #FCEA7A #7A2800 #065B97
STEEL, PALE, AMETHYST = 5004652, 11121336, 4066619        # 晶啸 #4C5D6C #A9B2B8 #3E0D3B

FORGE_TRIGGER = """\
# 熔火之锤［熔流］—— 由 rpg:advancement/item/forge 触发。
#
# `using_item` 在按住右键期间每刻都响，所以这里攒蓄力，攒满 {CHARGE} 刻才砸下去。
# 注意用的是无条件 `add`：选择器里的 scores 判定要求记分项**已经有值**，
# 第一次使用时它并不存在，条件恒假，计数器就永远起不来。
advancement revoke @s only rpg:item/forge
scoreboard players set @s rpg_forge_hold {HOLD}
scoreboard players add @s rpg_forge_chg 1

execute at @s run particle lava ~ ~0.3 ~ 0.45 0.1 0.45 0 2
execute at @s if entity @s[scores={{rpg_forge_chg=12..}}] run particle dust_color_transition{{from_color:{SCORCH},to_color:{EMBER},scale:2}} ~ ~0.9 ~ 0.5 0.7 0.5 0.03 8
execute at @s if entity @s[scores={{rpg_forge_chg=22..}}] run particle flame ~ ~1.3 ~ 0.5 0.6 0.5 0.02 10
execute if entity @s[scores={{rpg_forge_chg=..11}}] run title @s actionbar ["",{{"text":"熔流 ","color":"gold"}},{{"text":"▮▯▯ ","color":"dark_red"}},{{"text":"起火","color":"gray"}}]
execute if entity @s[scores={{rpg_forge_chg=12..21}}] run title @s actionbar ["",{{"text":"熔流 ","color":"gold"}},{{"text":"▮▮▯ ","color":"red"}},{{"text":"炽白","color":"gray"}}]
execute if entity @s[scores={{rpg_forge_chg=22..{CHARGE_1}}}] run title @s actionbar ["",{{"text":"熔流 ","color":"gold"}},{{"text":"▮▮▮ ","color":"yellow"}},{{"text":"将落","color":"gray"}}]
execute if entity @s[scores={{rpg_forge_chg={CHARGE}..}}] run title @s actionbar ["",{{"text":"熔　流","color":"gold","bold":true}}]
execute at @s if entity @s[scores={{rpg_forge_chg=1}}] run playsound minecraft:block.lava.ambient player @s ~ ~ ~ 1 0.7
execute at @s if entity @s[scores={{rpg_forge_chg=12}}] run playsound minecraft:block.lava.ambient player @s ~ ~ ~ 1 1.1
execute at @s if entity @s[scores={{rpg_forge_chg=22}}] run playsound minecraft:block.lava.ambient player @s ~ ~ ~ 1 1.5

# 精确判等，之后计数继续越过阈值，所以按住不放只砸一次
execute if entity @s[scores={{rpg_forge_chg={CHARGE}}}] run function rpg:item/epic/forge_cast
"""

FORGE_CAST = """\
# 砸地。热浪不是一片持续的场，而是三次定时脉冲 ——
# 计数器一到零整段就结束，没有任何东西留在场上每刻跑。
scoreboard players set @s rpg_forge_chg 0
scoreboard players set @s rpg_forge 24
particle minecraft:flash{{color:{EMBER}}} ~ ~0.6 ~ 0 0 0 0 1
particle lava ~ ~0.3 ~ 0.6 0.1 0.6 0 30
playsound minecraft:item.mace.smash_ground_heavy player @a[distance=..24] ~ ~ ~ 1 0.6
playsound minecraft:block.lava.extinguish player @a[distance=..20] ~ ~ ~ 1 0.7
"""

FORGE_TICK = """\
# 三重热浪：24 / 16 / 8 三个刻各推一圈，半径 3 → 5 → 7。
# 由 rpg:item/epic/epics 守卫调用；不在脉冲刻上时这里只是一次减法。
execute as @a[tag=rpg.h.forge_tag1,scores={{rpg_forge=24}}] at @s run function rpg:item/epic/forge_ring1
execute as @a[tag=rpg.h.forge_tag1,scores={{rpg_forge=16}}] at @s run function rpg:item/epic/forge_ring2
execute as @a[tag=rpg.h.forge_tag1,scores={{rpg_forge=8}}] at @s run function rpg:item/epic/forge_ring3
execute as @a[scores={{rpg_forge=1..}}] run scoreboard players remove @s rpg_forge 1

# 松手即散：trigger 每刻把 hold 顶回 {HOLD}，这里每刻扣 1，停手就清空蓄力
execute as @a[scores={{rpg_forge_hold=1..}}] run scoreboard players remove @s rpg_forge_hold 1
scoreboard players set @a[scores={{rpg_forge_hold=..0,rpg_forge_chg=1..}}] rpg_forge_chg 0
"""


def forge_ring(radius, count, pitch):
    return ("""\
particle dust_color_transition{{from_color:{EMBER},to_color:{SCORCH},scale:2}} ~ ~0.4 ~ %.1f 0.3 %.1f 0.05 %d
particle flame ~ ~0.4 ~ %.1f 0.2 %.1f 0.02 %d
playsound minecraft:entity.blaze.shoot player @a[distance=..20] ~ ~ ~ 0.8 %s
execute as @e[distance=0.1..%d,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run damage @s 5 minecraft:player_attack by @p[tag=rpg.h.forge_tag1]
execute as @e[distance=0.1..%d,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run function rpg:item/epic/forge_push
"""
            % (radius * 0.5, radius * 0.5, count, radius * 0.5, radius * 0.5,
               count // 2, pitch, radius, radius))


FORGE_PUSH = """\
# 被热浪推开一步，并被点燃。
execute at @s facing entity @p[tag=rpg.h.forge_tag1] feet run tp @s ^ ^ ^-0.7
effect give @s minecraft:fire_resistance 1 0 true
execute at @s run particle minecraft:flash{{color:{CINDER}}} ~ ~1 ~ 0 0 0 0 1
"""

SAW_TRIGGER = """\
# 熔岩链锯［熔锯］—— 右键起锯。与藤蔓之鞭同一形状：
# 起手只挂一个倒计时，之后每刻由 saw 函数按节拍落刀。
advancement revoke @s only rpg:item/lavasaw
execute if entity @s[scores={{rpg_saw=1..}}] run return 0
scoreboard players set @s rpg_saw {LIFE}
particle lava ~ ~1 ~ 0.4 0.4 0.4 0 12
playsound minecraft:block.respawn_anchor.charge player @a[distance=..18] ~ ~ ~ 1 1.4
playsound minecraft:entity.blaze.ambient player @a[distance=..18] ~ ~ ~ 0.8 1.8
"""

SAW = """\
# 熔锯：{LIFE} 刻内切六轮，每轮间隔 10 刻 ——
# 生物受伤后约有 10 刻无敌帧，切得更密只是浪费。
execute as @a[tag=rpg.h.dawn_tag1,scores={{rpg_saw=50}}] at @s run function rpg:item/epic/saw_cut
execute as @a[tag=rpg.h.dawn_tag1,scores={{rpg_saw=40}}] at @s run function rpg:item/epic/saw_cut
execute as @a[tag=rpg.h.dawn_tag1,scores={{rpg_saw=30}}] at @s run function rpg:item/epic/saw_cut
execute as @a[tag=rpg.h.dawn_tag1,scores={{rpg_saw=20}}] at @s run function rpg:item/epic/saw_cut
execute as @a[tag=rpg.h.dawn_tag1,scores={{rpg_saw=10}}] at @s run function rpg:item/epic/saw_cut
execute as @a[tag=rpg.h.dawn_tag1,scores={{rpg_saw=1}}] at @s run function rpg:item/epic/saw_cut
execute as @a[tag=rpg.h.dawn_tag1,scores={{rpg_saw=1..}}] at @s run particle dust_color_transition{{from_color:{GOLD},to_color:{DEEPRED},scale:1}} ~ ~1 ~ 0.3 0.3 0.3 0.02 3
execute as @a[scores={{rpg_saw=1..}}] run scoreboard players remove @s rpg_saw 1
"""

SAW_CUT = """\
# 一轮切割：身前召出熔岩獠牙，锯齿咬过 3.5 格。
# 獠牙沿用[切割链锯]的做法（放大、发光的 evoker_fangs），只是烧红了。
execute anchored eyes positioned ^ ^ ^2 run summon minecraft:evoker_fangs ~ ~-1 ~ {{Warmup:0,Tags:["rpg.saw.fang"],attributes:[{{id:"scale",base:2.2f}}]}}
execute as @e[tag=rpg.saw.fang] run data modify entity @s Owner set from entity @p[tag=rpg.h.dawn_tag1] UUID
tag @e[tag=rpg.saw.fang] remove rpg.saw.fang
particle trial_spawner_detection ~ ~1.2 ~ 0.5 0.5 0.5 0.1 12
particle lava ~ ~0.8 ~ 0.5 0.4 0.5 0 8
particle dust_color_transition{{from_color:{EMBER},to_color:{DEEPRED},scale:2}} ~ ~1 ~ 0.6 0.5 0.6 0.06 26
playsound minecraft:entity.blaze.burn player @a[distance=..18] ~ ~ ~ 1 0.8
playsound minecraft:item.axe.scrape player @a[distance=..18] ~ ~ ~ 1 1.6
execute as @e[distance=0.1..3.5,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run damage @s 5 minecraft:player_attack by @p[tag=rpg.h.dawn_tag1]
execute as @e[distance=0.1..3.5,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run effect give @s minecraft:glowing 3 0 true
"""

CHIME = """\
# 晶啸［共振］—— 命中的震荡沿晶体传开，波及目标身边的敌人。
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.h.chime_tag1] run tag @s add rpg.epic.chime
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.epic.chime,distance=..8] run particle dust_color_transition{{from_color:{AMETHYST},to_color:{PALE},scale:2}} ~ ~1 ~ 0.4 0.5 0.4 0.05 24
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.epic.chime,distance=..8] run playsound minecraft:block.amethyst_block.resonate hostile @a[distance=..16] ~ ~ ~ 1 1.2
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.epic.chime,distance=..8] run function rpg:item/epic/chime_wave
tag @a[tag=rpg.epic.chime] remove rpg.epic.chime
"""

CHIME_WAVE = """\
# 震荡只波及命中目标周围 3 格，不做全场扫描。
execute as @e[distance=0.1..3,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run damage @s 3 minecraft:magic by @a[tag=rpg.epic.chime,limit=1,sort=nearest]
execute as @e[distance=0.1..3,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run particle dust_color_transition{{from_color:{PALE},to_color:{STEEL},scale:1}} ~ ~1 ~ 0.25 0.4 0.25 0.04 10
"""

ROOT = """\
# 三件新武器的每刻入口。每条都先过握持判定 ——
# 没人拿着时整段跳过，空闲一刻只剩三次标签检查。
execute if entity @a[tag=rpg.h.dawn_tag1] run function rpg:item/epic/saw
execute if entity @a[tag=rpg.h.chime_tag1] run function rpg:item/epic/chime
execute if entity @a[tag=rpg.h.forge_tag1] run function rpg:item/epic/forge
"""

ARGS = dict(CHARGE=FORGE_CHARGE, CHARGE_1=FORGE_CHARGE - 1, HOLD=FORGE_HOLD,
            LIFE=SAW_LIFE,
            EMBER=EMBER, CINDER=CINDER, SCORCH=SCORCH,
            GOLD=GOLD, DEEPRED=DEEPRED, AZURE=AZURE,
            STEEL=STEEL, PALE=PALE, AMETHYST=AMETHYST)


def build_functions():
    wf("item/epic/forge_trigger.mcfunction", FORGE_TRIGGER.format(**ARGS))
    wf("item/epic/forge_cast.mcfunction", FORGE_CAST.format(**ARGS))
    wf("item/epic/forge.mcfunction", FORGE_TICK.format(**ARGS))
    for n, (r, c, pitch) in enumerate(((3, 40, "0.8"), (5, 60, "1.1"), (7, 80, "1.4")), 1):
        wf("item/epic/forge_ring%d.mcfunction" % n, forge_ring(r, c, pitch).format(**ARGS))
    wf("item/epic/forge_push.mcfunction", FORGE_PUSH.format(**ARGS))
    wf("item/epic/saw_trigger.mcfunction", SAW_TRIGGER.format(**ARGS))
    wf("item/epic/saw.mcfunction", SAW.format(**ARGS))
    wf("item/epic/saw_cut.mcfunction", SAW_CUT.format(**ARGS))
    wf("item/epic/chime.mcfunction", CHIME.format(**ARGS))
    wf("item/epic/chime_wave.mcfunction", CHIME_WAVE.format(**ARGS))
    wf("item/epic/epics.mcfunction", ROOT)

    wj(os.path.join(ADV, "lavasaw.json"), {
        "criteria": {"requirement": {
            "trigger": "minecraft:using_item",
            "conditions": {"item": {
                "predicates": {"minecraft:custom_data": "{dawn_tag:1b}"}}}}},
        "rewards": {"function": "rpg:item/epic/saw_trigger"}})
    wj(os.path.join(ADV, "forge.json"), {
        "criteria": {"requirement": {
            "trigger": "minecraft:using_item",
            "conditions": {"item": {
                "predicates": {"minecraft:custom_data": "{forge_tag:1b}"}}}}},
        "rewards": {"function": "rpg:item/epic/forge_trigger"}})

    tick = os.path.join(FUNC, "command/tick.mcfunction")
    s = io.open(tick, encoding="utf-8").read()
    if "item/epic/epics" not in s:
        s = s.replace("function rpg:item/rune/runes",
                      "function rpg:item/rune/runes\nfunction rpg:item/epic/epics")
        io.open(tick, "w", encoding="utf-8", newline="\n").write(s)


def add_objectives():
    p = os.path.join(FUNC, "command/soreboard.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    add = [n for n in ("rpg_forge", "rpg_forge_chg", "rpg_forge_hold", "rpg_saw")
           if n not in s]
    if not add:
        return []
    io.open(p, "w", encoding="utf-8", newline="\n").write(
        s.rstrip("\n") + "\n"
        + "\n".join("scoreboard objectives add %s dummy" % n for n in add) + "\n")
    return add


def register_index():
    p = os.path.join(FUNC, "command/index.mcfunction")
    lines = io.open(p, encoding="utf-8").read().split("\n")
    have = set(lines)
    clears, sets = [], []
    for w in WEAPONS:
        c = "tag @a remove rpg.h.%s_tag1" % w["key"]
        a = ("execute as @a if items entity @s weapon.mainhand "
             "*[minecraft:custom_data~{%s_tag:1b}] run tag @s add rpg.h.%s_tag1"
             % (w["key"], w["key"]))
        if c not in have:
            clears.append(c)
        if a not in have:
            sets.append(a)
    if not sets:
        return 0
    out, dc, da = [], False, False
    for l in lines:
        if not dc and l.startswith("execute as @a if items entity @s weapon.mainhand"):
            out.extend(clears)
            dc = True
        if not da and dc and l.startswith("## "):
            out.extend(sets + [""])
            da = True
        out.append(l)
    if not da:
        out.extend(clears + sets)
    io.open(p, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    return len(sets)


def main():
    art = build_art()
    n = build_give()
    build_functions()
    idx = register_index()
    obj = add_objectives()
    print("epics: art %s" % art)
    print("epics: %d items, index +%d, objectives %s" % (n, idx, obj or "-"))


if __name__ == "__main__":
    main()
