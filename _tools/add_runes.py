# -*- coding: utf-8 -*-
"""More inlay runes (passive) and inlay stones (active) -- and the fix that
makes the stone subsystem work at all.

The pack shipped three 镶嵌符石 (剑气 / 风暴 / 烈焰) that could never do
anything, for two independent reasons:

* they carry no `add_weapon_tag`, so `rpg:command/com/add` -- the "drop the rune
  on the weapon" path -- skips them entirely; and
* their advancements fire on `minecraft:using_item` with `consume_seconds` of
  1000000 / 2000000 / 3000000, and **no item in the pack has any of those
  values**, so the trigger matched nothing even in principle.

Both are fixed here.  The stones get `add_weapon_tag` plus the `food` +
`consumable` pair their own advancement is waiting for, and `com/add` learns to
carry those two components across when a stone is inlaid -- so an inlaid weapon
actually becomes right-clickable and the charge starts counting.

The three original trigger functions also gained a holder check.  Without it,
charging any stone-bearing weapon fired every stone's effect at once, because
the charge scores were read with no test for which stone the player is holding.

New content: four passive runes and three active stones, all following the
existing shape exactly -- `quartz` base, the `[名]镶嵌符文/符石` name, the same
three-line lore body, and the `<flag>_tag:1b,add_weapon_tag:1b` custom_data
that the inlay path keys on.
"""

import io
import json
import os
import sys

import png_tool as P

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
RP = sys.argv[2] if len(sys.argv) > 2 else "../resourcepack"
RPG_MODELS = os.path.join(RP, "assets/rpg/models/item")
RPG_TEX = os.path.join(RP, "assets/rpg/textures/item")
MC_ITEMS = os.path.join(RP, "assets/minecraft/items")

# 1110001 / 1110002 / 1110003 are the pack's own; start above them
CMD0 = 1110011


def tint(w, h, rgba, hexa):
    """Recolour a sprite onto one hue, keeping its shading.

    Each pixel's luminance is preserved and used to walk a
    black -> accent -> white ramp, so the artwork's highlights and shadows
    survive and only the colour changes.
    """
    tr, tg, tb = (int(hexa[1:3], 16), int(hexa[3:5], 16), int(hexa[5:7], 16))
    out = bytearray(rgba)
    for i in range(w * h):
        o = i * 4
        if not out[o + 3]:
            continue
        lum = (0.299 * out[o] + 0.587 * out[o + 1] + 0.114 * out[o + 2]) / 255.0
        if lum <= 0.5:
            k = lum / 0.5
            r, g, b = tr * k, tg * k, tb * k
        else:
            k = (lum - 0.5) / 0.5
            r = tr + (255 - tr) * k
            g = tg + (255 - tg) * k
            b = tb + (255 - tb) * k
        out[o], out[o + 1], out[o + 2] = int(r), int(g), int(b)
    return bytes(out)


# Minecraft's named colours, so an original rune's own accent can drive its tint
NAMED = {
    "black": "#000000", "dark_blue": "#0000AA", "dark_green": "#00AA00",
    "dark_aqua": "#00AAAA", "dark_red": "#AA0000", "dark_purple": "#AA00AA",
    "gold": "#FFAA00", "gray": "#AAAAAA", "dark_gray": "#555555",
    "blue": "#5555FF", "green": "#55FF55", "aqua": "#55FFFF", "red": "#FF5555",
    "light_purple": "#FF55FF", "yellow": "#FFFF55", "white": "#FFFFFF",
}

# the twelve that shipped sharing two sprites: (name, kind)
ORIGINALS = [
    ("泣血", "rune"), ("重击", "rune"), ("幽深", "rune"), ("萤火", "rune"),
    ("守护", "rune"), ("不屈", "rune"), ("共死", "rune"), ("黑炎", "rune"),
    ("连发", "rune"),
    ("剑气", "stone"), ("风暴", "stone"), ("烈焰", "stone"),
]


def retint_originals(base):
    """Read each original's own accent out of its give line, tint its sprite to
    match, and point its custom_model_data at the new model."""
    import re
    s = io.open(GIVE, encoding="utf-8").read()
    lines = s.split("\n")
    cmd = CMD0 + len(RUNES) + len(STONES)
    done = 0
    for i, line in enumerate(lines):
        if "镶嵌符" not in line:
            continue
        m = re.search(r'\{"text":"\[([^\]"]+)\]","italic":false,"bold":true,'
                      r'"color":"([^"]+)"\},\{"text":"镶嵌符([文石])"', line)
        if not m:
            continue
        name, colour, kind_cn = m.group(1), m.group(2), m.group(3)
        if not any(name == n for n, _ in ORIGINALS):
            continue
        kind = "rune" if kind_cn == "文" else "stone"
        hexa = NAMED.get(colour, colour)
        if not hexa.startswith("#") or len(hexa) != 7:
            continue
        key = "orig%d" % cmd
        w, h, rgba = base[kind]
        P.write(os.path.join(RPG_TEX, "rune_%s.png" % key), w, h, tint(w, h, rgba, hexa))
        wj(os.path.join(RPG_MODELS, "rune_%s.json" % key),
           {"parent": "minecraft:item/generated",
            "textures": {"layer0": "rpg:item/rune_" + key}})
        lines[i] = re.sub(r"custom_model_data=\{floats:\[[0-9.]+f\]\}",
                          "custom_model_data={floats:[%d.0f]}" % cmd, line)
        _register_quartz(cmd, "rune_" + key)
        cmd += 1
        done += 1
    if done:
        io.open(GIVE, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    return done


_QUARTZ_PENDING = []


def _register_quartz(cmd, model):
    _QUARTZ_PENDING.append((cmd, model))


def _flush_quartz():
    path = os.path.join(MC_ITEMS, "quartz.json")
    doc = json.load(io.open(path, encoding="utf-8"))
    entries = doc["model"]["entries"]
    for cmd, model in _QUARTZ_PENDING:
        entries[:] = [e for e in entries if e["threshold"] != cmd]
        entries.append({"threshold": cmd,
                        "model": {"type": "minecraft:model",
                                  "model": "rpg:item/" + model}})
    entries.sort(key=lambda e: e["threshold"])
    wj(path, doc)


def build_art():
    """符文 borrow the scroll art, 符石 the stone art -- each in its own colour."""
    base = {}
    for kind, model in (("rune", "amethyst_shard"), ("stone", "quartz")):
        doc = json.load(io.open(os.path.join(RPG_MODELS, model + ".json"),
                                encoding="utf-8"))
        tex = doc["textures"]["layer0"].split(":")[-1]
        base[kind] = P.read(os.path.join(RP, "assets/rpg/textures", tex + ".png"))

    made = 0
    for kind, items in (("rune", RUNES), ("stone", STONES)):
        w, h, rgba = base[kind]
        for it in items:
            name = "rune_" + it["key"]
            P.write(os.path.join(RPG_TEX, name + ".png"), w, h,
                    tint(w, h, rgba, it["hexa"]))
            wj(os.path.join(RPG_MODELS, name + ".json"),
               {"parent": "minecraft:item/generated",
                "textures": {"layer0": "rpg:item/" + name}})
            made += 1

    path = os.path.join(MC_ITEMS, "quartz.json")
    doc = json.load(io.open(path, encoding="utf-8"))
    entries = doc["model"]["entries"]
    for it in RUNES + STONES:
        entries[:] = [e for e in entries if e["threshold"] != it["cmd"]]
        entries.append({"threshold": it["cmd"],
                        "model": {"type": "minecraft:model",
                                  "model": "rpg:item/rune_" + it["key"]}})
    entries.sort(key=lambda e: e["threshold"])
    wj(path, doc)
    return made, base
FUNC = os.path.join(DP, "data/rpg/function")
ADV = os.path.join(DP, "data/rpg/advancement/item")
GIVE = os.path.join(FUNC, "command/give/item.mcfunction")

RULE = '["",{"text":"+------------------+","italic":false,"color":"white"}]'


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


CONSUMABLE = ('food={{nutrition:0,saturation:0f,can_always_eat:1b}},'
              'consumable={{consume_seconds:{cs}f,animation:"eat",'
              'sound:"minecraft:entity.generic.eat",has_consume_particles:true,'
              'on_consume_effects:[]}},')

# ---------------------------------------------------------------------------
# 被动符文 -- inlaid onto a weapon, they just add a flag the tick path reads
# ---------------------------------------------------------------------------
RUNES = [
    dict(key="wilt", name="枯萎", colour="dark_gray", hexa="#5A6152", icon="🪓", part="剑",
         text="攻击时有1/4的概率使目标凋零5秒"),
    dict(key="sunder", name="裂甲", colour="#C0A080", hexa="#C0A080", icon="🪓", part="剑",
         text="攻击时破开护甲，目标虚弱且暴露6秒"),
    dict(key="ebb", name="逆潮", colour="#4FA8C8", hexa="#4FA8C8", icon="🛡", part="胸甲",
         text="生命低于30%时回涌，再生与抗性各6秒"),
    dict(key="pin", name="钉影", colour="#7A6BA8", hexa="#7A6BA8", icon="🏹", part="弓",
         text="箭矢命中后将目标钉在原地2.5秒"),
]

# ---------------------------------------------------------------------------
# 主动符石 -- inlaid, then charged by holding right-click
# ---------------------------------------------------------------------------
STONES = [
    dict(key="tide", name="寒潮", colour="#7FC8E0", hexa="#7FC8E0", part="剑", cs=4000000,
         charge=45, text="长按/右键蓄力掀起环形寒潮"),
    dict(key="quake", name="震地", colour="#B98A44", hexa="#B98A44", part="重锤", cs=5000000,
         charge=55, text="长按/右键蓄力砸地，震飞四周"),
    dict(key="shade", name="噬影", colour="#6B4FA0", hexa="#6B4FA0", part="剑", cs=7000000,
         charge=40, text="长按/右键蓄力遁入影中，自敌后重创"),
]

# the three that shipped broken: (flag, consume_seconds their advancement wants)
BROKEN = [("sweep_tag", 1000000), ("wind_tag", 2000000), ("flame_tag", 3000000)]


def give_rune(r):
    return ("give @a quartz["
            "custom_name=" + row(seg("[%s]" % r["name"], r["colour"], True),
                                 seg("镶嵌符文")) + ","
            "lore=[" + ",".join([
                RULE,
                row(seg("蕴含"), seg("[法力]", r["colour"], True), seg("的卷轴")),
                row(seg("镶嵌于"), seg("[%s]" % r["part"], r["colour"], True), seg("上")),
                RULE,
                row(seg("%s被动技能" % r["icon"], "white", True),
                    seg("[%s]" % r["name"], r["colour"], True)),
                row(seg(r["text"])),
                RULE]) + "],"
            "custom_model_data={floats:[%d.0f]}," % r["cmd"] +
            "custom_data={%s_tag:1b,add_weapon_tag:1b}]" % r["key"])


def give_stone(s):
    return ("give @a quartz["
            "custom_name=" + row(seg("[%s]" % s["name"], s["colour"], True),
                                 seg("镶嵌符石")) + ","
            "lore=[" + ",".join([
                RULE,
                row(seg("蕴含"), seg("[法力]", s["colour"], True), seg("的符石")),
                row(seg("镶嵌于"), seg("[%s]" % s["part"], s["colour"], True), seg("上")),
                RULE,
                row(seg("🔱镶嵌技能", "white", True),
                    seg("[%s]" % s["name"], s["colour"], True)),
                row(seg(s["text"])),
                RULE]) + "],"
            + CONSUMABLE.format(cs=s["cs"]) +
            "custom_model_data={floats:[%d.0f]}," % s["cmd"] +
            "custom_data={%s_tag:1b,add_weapon_tag:1b}]" % s["key"])


# ---------------------------------------------------------------------------
# the passive effects
# ---------------------------------------------------------------------------
WILT = """\
# 枯萎［被动］—— 攻击时四分之一的概率让目标凋零。
# 走 rpg.hurt + on attacker，与包里其余被动同一形状。
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.h.wilt_tag1] run scoreboard players set @s rpg_rune_roll 0
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.h.wilt_tag1] store result score @s rpg_rune_roll run random value 1..4
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.h.wilt_tag1,scores={rpg_rune_roll=1}] run tag @s add rpg.rune.wilt
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.rune.wilt,distance=..8] run effect give @s minecraft:wither 5 1 true
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.rune.wilt,distance=..8] run particle dust_color_transition{from_color:[0.16,0.16,0.16],to_color:[0.05,0.22,0.05],scale:2} ~ ~1 ~ 0.3 0.5 0.3 0.04 24
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.rune.wilt,distance=..8] run playsound minecraft:entity.wither.shoot hostile @a[distance=..16] ~ ~ ~ 0.5 1.6
tag @a[tag=rpg.rune.wilt] remove rpg.rune.wilt
"""

SUNDER = """\
# 裂甲［被动］—— 破开护甲：虚弱削弱其输出，发光让它无处可藏。
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.h.sunder_tag1] run tag @s add rpg.rune.sunder
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.rune.sunder,distance=..8] run effect give @s minecraft:weakness 6 1 true
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.rune.sunder,distance=..8] run effect give @s minecraft:glowing 6 0 true
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.rune.sunder,distance=..8] run particle crit ~ ~1 ~ 0.35 0.4 0.35 0.25 18
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.rune.sunder,distance=..8] run playsound minecraft:item.shield.break hostile @a[distance=..14] ~ ~ ~ 0.6 1.4
tag @a[tag=rpg.rune.sunder] remove rpg.rune.sunder
"""

EBB = """\
# 逆潮［被动］—— 生命跌破三成时回涌一次，之后要等 30 秒才会再涌。
# 血量直接读 damage_action：rpg:command/index 每刻已经抓好，零额外开销。
execute as @a[tag=rpg.h.ebb_tag1,scores={rpg_rune_ebb=1..}] run scoreboard players remove @s rpg_rune_ebb 1
execute as @a[tag=rpg.h.ebb_tag1,scores={rpg_rune_ebb=..0,damage_action=..5}] at @s run function rpg:item/rune/ebb_surge
"""

EBB_SURGE = """\
# 回涌：再生与抗性各 6 秒，然后压 30 秒冷却。
scoreboard players set @s rpg_rune_ebb 600
effect give @s minecraft:regeneration 6 1 true
effect give @s minecraft:resistance 6 0 true
particle dust_color_transition{from_color:[0.31,0.66,0.78],to_color:[0.85,0.95,1.0],scale:2} ~ ~1 ~ 0.5 0.8 0.5 0.05 50
particle splash ~ ~1 ~ 0.5 0.6 0.5 0.3 30
playsound minecraft:block.conduit.activate player @a[distance=..16] ~ ~ ~ 1 1.3
"""

PIN = """\
# 钉影［被动］—— 箭矢命中后把目标钉在原地。
execute as @e[type=minecraft:arrow,tag=!rpg.rune.pin] on origin if entity @s[tag=rpg.h.pin_tag1] at @s run tag @e[type=minecraft:arrow,distance=0..2] add rpg.rune.pin
execute as @e[tag=rpg.rune.pin] at @s run particle dust_color_transition{from_color:[0.48,0.42,0.66],to_color:[0.20,0.16,0.30],scale:1} ~ ~ ~ 0.08 0.08 0.08 0.02 3
execute as @e[tag=rpg.rune.pin] at @s if entity @e[distance=0.1..1.5,type=!minecraft:arrow] unless entity @a[tag=rpg.h.pin_tag1,distance=..1.5] run effect give @e[distance=..1.5,limit=1,sort=nearest,type=!minecraft:arrow] minecraft:slowness 3 4 true
execute as @e[tag=rpg.rune.pin] at @s if entity @e[distance=0.1..1.5,type=!minecraft:arrow] unless entity @a[tag=rpg.h.pin_tag1,distance=..1.5] run effect give @e[distance=..1.5,limit=1,sort=nearest,type=!minecraft:arrow] minecraft:mining_fatigue 3 2 true
execute as @e[tag=rpg.rune.pin] at @s if entity @e[distance=0.1..1.5,type=!minecraft:arrow] unless entity @a[tag=rpg.h.pin_tag1,distance=..1.5] run particle minecraft:flash{color:8022440} ~ ~0.8 ~ 0 0 0 0 1
execute as @e[tag=rpg.rune.pin] at @s if entity @e[distance=0.1..1.5,type=!minecraft:arrow] unless entity @a[tag=rpg.h.pin_tag1,distance=..1.5] run playsound minecraft:block.anvil.land hostile @a[distance=..14] ~ ~ ~ 0.5 1.8
execute as @e[tag=rpg.rune.pin] at @s unless block ~ ~ ~ air run kill @s
"""

RUNE_BODY = {"wilt": WILT, "sunder": SUNDER, "ebb": EBB, "pin": PIN}

# ---------------------------------------------------------------------------
# the active effects: charge on the advancement, fire from the tick path
# ---------------------------------------------------------------------------
CHARGE = """\
# {name}［蓄力］—— 由 rpg:advancement/item/{key} 在按住右键期间每刻触发。
# 与包里其余蓄力技能同一节拍：每响一次攒一格，攒满由 {key}_trigger 放出。
advancement revoke @s only rpg:item/{key}
scoreboard players add @s rpg_{key} 1
execute at @s run particle {p_charge} ~ ~1 ~ 0.4 0.6 0.4 0.03 6
"""

TIDE = """\
# 寒潮［主动］—— 攒满 {charge} 刻后掀起一圈寒潮。
# 守卫在 rpg:item/rune/runes 里，没人握着刻印此石的武器时整段跳过。
execute as @a[tag=rpg.h.tide_tag1,scores={{rpg_tide={charge}..}}] at @s run function rpg:item/rune/tide_burst
execute as @a[scores={{rpg_tide=1..}}] unless entity @s[tag=rpg.h.tide_tag1] run scoreboard players set @s rpg_tide 0
"""

TIDE_BURST = """\
# 环形寒潮：冻结、减速、外推。
scoreboard players set @s rpg_tide 0
particle dust_color_transition{from_color:[0.50,0.78,0.88],to_color:[0.90,0.98,1.0],scale:2} ~ ~0.6 ~ 3.2 0.4 3.2 0.06 120
particle snowflake ~ ~0.8 ~ 3 0.5 3 0.1 80
particle minecraft:flash{color:8374496} ~ ~1 ~ 0 0 0 0 1
playsound minecraft:block.glass.break player @a[distance=..20] ~ ~ ~ 1 0.7
playsound minecraft:entity.player.hurt_freeze player @a[distance=..20] ~ ~ ~ 1 0.9
execute as @e[distance=0.1..6,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run effect give @s minecraft:slowness 6 4 true
execute as @e[distance=0.1..6,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run effect give @s minecraft:mining_fatigue 6 2 true
execute as @e[distance=0.1..6,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run damage @s 5 minecraft:freeze
execute as @e[distance=0.1..6,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s facing entity @p[tag=rpg.h.tide_tag1] feet run tp @s ^ ^ ^-0.9
"""

QUAKE = """\
execute as @a[tag=rpg.h.quake_tag1,scores={{rpg_quake={charge}..}}] at @s run function rpg:item/rune/quake_burst
execute as @a[scores={{rpg_quake=1..}}] unless entity @s[tag=rpg.h.quake_tag1] run scoreboard players set @s rpg_quake 0
"""

QUAKE_BURST = """\
# 砸地：环形击飞并致盲。
scoreboard players set @s rpg_quake 0
particle block{block_state:"minecraft:deepslate"} ~ ~0.2 ~ 3 0.2 3 1 160
particle explosion ~ ~0.4 ~ 1.5 0.2 1.5 0 8
particle dust_color_transition{from_color:[0.73,0.54,0.27],to_color:[0.35,0.28,0.18],scale:3} ~ ~0.6 ~ 3 0.4 3 0.05 90
playsound minecraft:item.mace.smash_ground_heavy player @a[distance=..24] ~ ~ ~ 1 0.7
playsound minecraft:entity.generic.explode player @a[distance=..24] ~ ~ ~ 0.7 0.6
execute as @e[distance=0.1..6,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run damage @s 8 minecraft:player_attack by @p[tag=rpg.h.quake_tag1]
execute as @e[distance=0.1..6,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run effect give @s minecraft:blindness 5 0 true
execute as @e[distance=0.1..6,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run data merge entity @s {Motion:[0d,0.85d,0d]}
"""

SHADE = """\
execute as @a[tag=rpg.h.shade_tag1,scores={{rpg_shade={charge}..}}] at @s run function rpg:item/rune/shade_burst
execute as @a[scores={{rpg_shade=1..}}] unless entity @s[tag=rpg.h.shade_tag1] run scoreboard players set @s rpg_shade 0
"""

SHADE_BURST = """\
# 噬影：遁入影中，出现在最近敌人背后并重创。
# `facing entity … ` 后再 `^ ^ ^1.2` 就是"绕到它背后一步"。
scoreboard players set @s rpg_shade 0
particle smoke ~ ~1 ~ 0.4 0.7 0.4 0.05 40
particle dust_color_transition{from_color:[0.42,0.31,0.63],to_color:[0.08,0.05,0.14],scale:2} ~ ~1 ~ 0.5 0.8 0.5 0.05 60
playsound minecraft:entity.enderman.teleport player @a[distance=..20] ~ ~ ~ 1 0.8
execute if entity @e[distance=0.1..14,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,limit=1,sort=nearest] at @s facing entity @e[distance=0.1..14,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,limit=1,sort=nearest] feet positioned ^ ^ ^1.2 run tp @s ~ ~ ~
execute as @e[distance=0.1..3,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,limit=1,sort=nearest] at @s run damage @s 12 minecraft:magic by @p[tag=rpg.h.shade_tag1]
execute as @e[distance=0.1..3,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,limit=1,sort=nearest] at @s run particle minecraft:flash{color:7032224} ~ ~1 ~ 0 0 0 0 1
execute at @s run particle smoke ~ ~1 ~ 0.4 0.7 0.4 0.05 40
playsound minecraft:entity.player.attack.crit player @a[distance=..20] ~ ~ ~ 1 0.7
"""

STONE_TICK = {"tide": TIDE, "quake": QUAKE, "shade": SHADE}
STONE_BURST = {"tide": TIDE_BURST, "quake": QUAKE_BURST, "shade": SHADE_BURST}
P_CHARGE = {"tide": "snowflake", "quake": "crit", "shade": "smoke"}

OBJECTIVES = ["rpg_rune_roll", "rpg_rune_ebb", "rpg_tide", "rpg_quake", "rpg_shade"]


def build_gives():
    s = io.open(GIVE, encoding="utf-8").read()
    if "枯萎" in s:
        return 0
    lines = [s.rstrip("\n"), "", "##新增镶嵌符文（被动）"]
    lines += [give_rune(r) for r in RUNES]
    lines += ["", "##新增镶嵌符石（主动·蓄力）"]
    lines += [give_stone(t) for t in STONES]
    lines.append("")
    io.open(GIVE, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    return len(RUNES) + len(STONES)


def fix_broken_stones():
    """Give the three original stones the two things they were missing."""
    s = io.open(GIVE, encoding="utf-8").read()
    n = 0
    for flag, cs in BROKEN:
        # custom_data is not the last component on these lines -- custom_model_data
        # follows it -- so match the comma form, not a closing bracket.
        old = "custom_data={%s:1b}," % flag
        if old not in s:
            continue
        new = (CONSUMABLE.format(cs=cs)
               + "custom_data={%s:1b,add_weapon_tag:1b}," % flag)
        s = s.replace(old, new)
        n += 1
    if n:
        io.open(GIVE, "w", encoding="utf-8", newline="\n").write(s)
    return n


def carry_components_on_inlay():
    """`com/add` copied lore and custom_data but not food/consumable, so an
    inlaid stone could never make its weapon right-clickable."""
    p = os.path.join(FUNC, "command/com/add.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    if "minecraft:consumable set from" in s:
        return False
    mark = ("execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run "
            "data modify entity @s Item.components.minecraft:custom_data merge from "
            "entity @e[limit=1,distance=..1,type=minecraft:item,tag=rpg.i.add_weapon_tag1] "
            "Item.components.minecraft:custom_data")
    extra = "\n".join([
        "# 符石还要把 food / consumable 带过去，否则镶嵌完的武器仍然不能右键，",
        "# 那条 using_item 进度也就永远不会响 —— 原本三块符石失效的一半原因。",
        "execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s if data entity "
        "@e[limit=1,distance=..1,type=minecraft:item,tag=rpg.i.add_weapon_tag1] "
        "Item.components.minecraft:consumable run data modify entity @s "
        "Item.components.minecraft:food set from entity "
        "@e[limit=1,distance=..1,type=minecraft:item,tag=rpg.i.add_weapon_tag1] "
        "Item.components.minecraft:food",
        "execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s if data entity "
        "@e[limit=1,distance=..1,type=minecraft:item,tag=rpg.i.add_weapon_tag1] "
        "Item.components.minecraft:consumable run data modify entity @s "
        "Item.components.minecraft:consumable set from entity "
        "@e[limit=1,distance=..1,type=minecraft:item,tag=rpg.i.add_weapon_tag1] "
        "Item.components.minecraft:consumable",
    ])
    s = s.replace(mark, mark + "\n" + extra)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    return True


def guard_original_triggers():
    """Without a holder test, charging any stone fired all three effects."""
    n = 0
    for flag, sub in (("sweep_tag", "sweep"), ("wind_tag", "wind"),
                      ("flame_tag", "flame")):
        p = os.path.join(FUNC, "item/sword/main/%s/%s_trigger.mcfunction" % (sub, sub))
        if not os.path.isfile(p):
            continue
        s = io.open(p, encoding="utf-8").read()
        if "rpg.h.%s1" % flag in s:
            continue
        s = s.replace("@a[scores={%s=50..}]" % sub,
                      "@a[tag=rpg.h.%s1,scores={%s=50..}]" % (flag, sub))
        s = ("# 加上握持判定：原本没有这一条，攒满任何一块符石都会把三种效果一起放出。\n"
             + s)
        io.open(p, "w", encoding="utf-8", newline="\n").write(s)
        n += 1
    return n


def build_functions():
    for r in RUNES:
        wf("item/rune/%s.mcfunction" % r["key"], RUNE_BODY[r["key"]])
    wf("item/rune/ebb_surge.mcfunction", EBB_SURGE)
    for t in STONES:
        wf("item/rune/%s_charge.mcfunction" % t["key"],
           CHARGE.format(name=t["name"], key=t["key"], p_charge=P_CHARGE[t["key"]]))
        wf("item/rune/%s.mcfunction" % t["key"],
           STONE_TICK[t["key"]].format(charge=t["charge"]))
        wf("item/rune/%s_burst.mcfunction" % t["key"], STONE_BURST[t["key"]])
        wj(os.path.join(ADV, "%s.json" % t["key"]), {
            "criteria": {"requirement": {
                "trigger": "minecraft:using_item",
                "conditions": {"item": {
                    "predicates": {"minecraft:custom_data":
                                   "{%s_tag:1b}" % t["key"]}}}}},
            "rewards": {"function": "rpg:item/rune/%s_charge" % t["key"]}})

    body = ["# 镶嵌符文与符石的每刻入口。每条都先过握持判定 ——",
            "# 没人带着这枚刻印时整段跳过。", ""]
    for r in RUNES:
        body.append("execute if entity @a[tag=rpg.h.%s_tag1] run function "
                    "rpg:item/rune/%s" % (r["key"], r["key"]))
    body.append("execute unless entity @a[tag=rpg.h.pin_tag1] if entity "
                "@e[type=minecraft:arrow,tag=rpg.rune.pin] run function rpg:item/rune/pin")
    for t in STONES:
        body.append("execute if entity @a[tag=rpg.h.%s_tag1] run function "
                    "rpg:item/rune/%s" % (t["key"], t["key"]))
    wf("item/rune/runes.mcfunction", "\n".join(body))

    tick = os.path.join(FUNC, "command/tick.mcfunction")
    s = io.open(tick, encoding="utf-8").read()
    if "item/rune/runes" not in s:
        s = s.replace("function rpg:item/extra/skills",
                      "function rpg:item/extra/skills\nfunction rpg:item/rune/runes")
        io.open(tick, "w", encoding="utf-8", newline="\n").write(s)


def add_objectives():
    p = os.path.join(FUNC, "command/soreboard.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    add = [n for n in OBJECTIVES if n not in s]
    if add:
        io.open(p, "w", encoding="utf-8", newline="\n").write(
            s.rstrip("\n") + "\n"
            + "\n".join("scoreboard objectives add %s dummy" % n for n in add) + "\n")
    return add


def register_index():
    """Every new flag needs its held-item lookup in the per-tick index."""
    p = os.path.join(FUNC, "command/index.mcfunction")
    lines = io.open(p, encoding="utf-8").read().split("\n")
    have = set(lines)
    flags = [r["key"] for r in RUNES] + [t["key"] for t in STONES]
    clears, sets = [], []
    for f in flags:
        c = "tag @a remove rpg.h.%s_tag1" % f
        a = ("execute as @a if items entity @s weapon.mainhand "
             "*[minecraft:custom_data~{%s_tag:1b}] run tag @s add rpg.h.%s_tag1" % (f, f))
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
    for n, it in enumerate(RUNES + STONES):
        it["cmd"] = CMD0 + n
    art, base = build_art()
    fixed = fix_broken_stones()
    carried = carry_components_on_inlay()
    guarded = guard_original_triggers()
    n = build_gives()
    build_functions()
    idx = register_index()
    obj = add_objectives()
    retinted = retint_originals(base)
    _flush_quartz()
    print("runes: %d new items (%d 符文 + %d 符石), %d tinted sprites"
          % (n, len(RUNES), len(STONES), art))
    print("runes: repaired %d original stones, inlay carries components: %s, "
          "holder-guarded %d triggers" % (fixed, carried, guarded))
    print("runes: index flags +%d, objectives %s" % (idx, obj or "-"))
    print("runes: retinted %d original sprites" % retinted)


if __name__ == "__main__":
    main()
