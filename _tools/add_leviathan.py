# -*- coding: utf-8 -*-
"""利维坦 -- the sixth demon weapon, a mace.

Same specification as the other five: `[DEVIL]` prefix in the demon's own
accent, a two-line epithet, one skill block, five enchantments, `unbreakable`
with the tooltip line hidden, `devil_tag` in custom_data.

The base is `minecraft:mace`, which -- unlike the fishing rod and the spear --
has **no right-click use action of its own** (the language file carries only
`subtitles.item.mace.smash_air` / `smash_ground`).  So the ordinary
`food` + `consumable` route works here, the same one 亚巴顿 uses.

Anchor and sea run through every part of it:

* the accent is `#123E7C`, a deep navy, per the brief.  The art itself is a
  bronze anchor gone green under water, so its own gold is used as the second
  particle colour -- the metal against the abyss.
* ［沉锚］ hurls the anchor ahead of the caster; where it bites, a whirlpool
  opens, dragging everything toward its heart and crushing it on a ten-tick
  beat (mobs have ~10 ticks of invulnerability, so a faster beat is wasted).
* thrown while airborne the anchor sinks deeper -- longer, heavier -- which is
  the mace's own from-a-height identity told as an anchor drop.
* `impaling` (its damage effect is generic, so it works off a trident) and
  `density` carry the theme into the enchantment list.
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

BASE = "mace"
CMD = 1110007          # first free custom_model_data on the mace
CONSUME = 100110       # first free consume_seconds
NATIVE = 32            # the art's own grid, recovered in build_texture()
THROW = 8              # how far ahead the anchor lands, in blocks
RADIUS = 7             # whirlpool radius
BEAT = 10              # ticks between crushes -- matches mob invulnerability
LIFE = 100             # whirlpool duration; deeper when thrown airborne
LIFE_DEEP = 160
COST = 10            # 每次施放献出的生命，直接扣，不走 damage
UNLUCK = 10          # 不幸持续秒数

ART = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "leviathan_art", "leviathan.png")

# ---------------------------------------------------------------------------
# palette: deep blue leads (代表色), the art's own gold answers it
# ---------------------------------------------------------------------------
ABYSS = 1195644       # #123E7C  深蓝 -- the brief's colour
TRENCH = 532802       # #081F42  darker still, for the whirlpool's throat
FOAM = 8374496        # #7FC8E0  sea foam
GOLD = 16559622       # #FCAE06  the anchor's metal, 15% of the sprite

P_ABYSS = "[0.071,0.243,0.486]"
P_TRENCH = "[0.031,0.122,0.259]"
P_FOAM = "[0.498,0.784,0.878]"
P_GOLD = "[0.988,0.682,0.024]"


def wj(path, doc):
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def wf(rel, text):
    path = os.path.join(FUNC, rel)
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text.rstrip("\n") + "\n")


# ---------------------------------------------------------------------------
# art -- the upload is resampled, so recover the grid by majority vote
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
    """Same recovery add_lucifer.py uses: each output cell takes the majority
    vote of its interior, snapped to the sprite's own palette, so blurred cell
    edges are outvoted by the solid middles."""
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


def build_texture():
    if not os.path.isfile(ART):
        raise SystemExit("missing anchor art: put the sprite at %s" % ART)
    if not os.path.isdir(RPG_TEX):
        os.makedirs(RPG_TEX)
    w, h, rgba = P.read(ART)
    px = reconstruct(w, h, rgba, NATIVE)
    P.write(os.path.join(RPG_TEX, "leviathan.png"), NATIVE, NATIVE, px)
    used = len(set(px[i * 4:i * 4 + 4] for i in range(NATIVE * NATIVE)
                   if px[i * 4 + 3]))
    return "%dx%d from %dx%d, %d colours" % (NATIVE, NATIVE, w, h, used)


def build_models():
    # huge_sword_handheld is scaled 2.06 for a thin diagonal greatsword; the
    # anchor fills its whole 32x32 sprite, so at that scale it swamps the hand.
    # sword_handheld (1.195) is the pack's best-tuned transform and the size a
    # one-handed mace actually wants.
    wj(os.path.join(RPG_MODELS, "leviathan.json"),
       {"parent": "rpg:item/sword_handheld",
        "textures": {"layer0": "rpg:item/leviathan"}})

    path = os.path.join(MC_ITEMS, BASE + ".json")
    doc = json.load(io.open(path, encoding="utf-8"))
    entries = doc["model"]["entries"]
    entries[:] = [e for e in entries if e["threshold"] != CMD]
    entries.append({"threshold": CMD,
                    "model": {"type": "minecraft:model",
                              "model": "rpg:item/leviathan"}})
    entries.sort(key=lambda e: e["threshold"])
    wj(path, doc)


# ---------------------------------------------------------------------------
# the item
# ---------------------------------------------------------------------------
DEVIL = "#123E7C"      # 利维坦's accent: 深蓝
RULE = '["",{"text":"+------------------+","italic":false,"color":"white"}]'


def seg(text, colour="white", bold=False):
    return ('{"text":"%s","italic":false,"color":"%s"%s}'
            % (text, colour, ',"bold":true' if bold else ""))


def row(*segs):
    return '["",%s]' % ",".join(segs)


LEVIATHAN = ("give @a %s[" % BASE +
             "custom_name=" + row(seg("[DEVIL]", DEVIL, True),
                                  seg("利维坦", "aqua")) + ","
             "lore=[" + ",".join([
                 RULE,
                 row(seg("深渊里的曲行蛇"), seg(" 以铁为干草的巨兽", DEVIL, True)),
                 row(seg("它使深海翻滚如锅"), seg(" 海之魔神利维坦", DEVIL, True)),
                 RULE,
                 row(seg("🪓主动技能"), seg("[沉锚]", DEVIL, True)),
                 row(seg("右键抛出巨锚，锚落处涌起漩涡")),
                 row(seg("漩涡将敌人拖向锚心并持续碾压；凌空抛锚沉得更深")),
                 row(seg("代价：每次献出"), seg("10点生命", DEVIL, True),
                     seg("，并背负"), seg("10秒不幸", DEVIL, True)),
                 RULE]) + "],"
             # all five work on a mace: breach/density/wind_burst are its own,
             # smite is #enchantable/weapon, and impaling's damage effect is
             # generic so it applies off a trident just fine
             "enchantments={density:5,breach:4,wind_burst:3,impaling:5,smite:3},"
             "attribute_modifiers=["
             '{type:"attack_damage",amount:13,operation:add_value,slot:mainhand,id:"rpg:devil/leviathan/0"},'
             '{type:"attack_speed",amount:-3.3,operation:add_value,slot:mainhand,id:"rpg:devil/leviathan/1"},'
             '{type:"entity_interaction_range",amount:1,operation:add_value,slot:mainhand,id:"rpg:devil/leviathan/2"},'
             # 锚的重量：走得慢，但砸下来不伤自己，且巨兽的体魄
             '{type:"movement_speed",amount:-0.2,operation:add_multiplied_base,slot:mainhand,id:"rpg:devil/leviathan/3"},'
             '{type:"safe_fall_distance",amount:2,operation:add_multiplied_base,slot:mainhand,id:"rpg:devil/leviathan/4"},'
             '{type:"max_health",amount:0.2,operation:add_multiplied_base,slot:mainhand,id:"rpg:devil/leviathan/5"}],'
             "food={nutrition:0,saturation:0f,can_always_eat:1b},"
             'consumable={consume_seconds:%df,animation:"eat",'
             'sound:"minecraft:entity.generic.eat",has_consume_particles:true,'
             "on_consume_effects:[]}," % CONSUME +
             "unbreakable={},"
             'tooltip_display={hidden_components:["minecraft:unbreakable"]},'
             "custom_model_data={floats:[%d.0f]}," % CMD +
             "custom_data={leviathan_tag:1b,sword_tag:1b,devil_tag:1b}]")


def build_give():
    path = os.path.join(FUNC, "command/give/extra.mcfunction")
    s = io.open(path, encoding="utf-8").read()
    if "利维坦" in s:
        return False
    body = [s.rstrip("\n"), "",
            "# 第六位恶魔：利维坦（重锤·主动技能［沉锚］）",
            LEVIATHAN, ""]
    io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(body))
    return True


def build_advancement():
    wj(os.path.join(ADV, "leviathan.json"), {
        "criteria": {"requirement": {
            "trigger": "minecraft:using_item",
            "conditions": {"item": {"components": {
                "minecraft:food": {"nutrition": 0, "saturation": 0,
                                   "can_always_eat": True},
                "minecraft:consumable": {
                    "consume_seconds": float(CONSUME), "animation": "eat",
                    "sound": "minecraft:entity.generic.eat",
                    "has_consume_particles": True, "on_consume_effects": []},
            }}}}},
        "rewards": {"function": "rpg:item/extra/leviathan_trigger"},
    })


# ---------------------------------------------------------------------------
# 沉锚 -- the skill
# ---------------------------------------------------------------------------
TRIGGER = """\
# 利维坦［沉锚］—— 由 rpg:advancement/item/leviathan 在右键使用时触发。
# 代价是血而不是经验，所以先量一次生命：不够就拒绝，而不是把人送走。
# （包里其余主动技能在付不起代价时也是这个反应，一声 villager.no。）
advancement revoke @s only rpg:item/leviathan
execute store result score @s rpg_levi_hp run data get entity @s Health
execute if entity @s[scores={{rpg_levi_hp=..{COST}}}] run playsound minecraft:entity.villager.no player @s
execute if entity @s[scores={{rpg_levi_hp={COST_1}..}}] run function rpg:item/extra/leviathan_cast
"""

CAST = """\
# 抛锚。`rotated ~ 0` 把俯仰归零，所以锚永远沿水平方向掷出 {THROW} 格，
# 不会因为抬头而飞上天 —— 锚是往下沉的东西。
# 血税：直接改写生命值，而不是 `damage`。
# `damage` 要过约 10 刻的无敌帧 —— 连点右键时代价会被整个吞掉，等于白嫖；
# 直接写 Health 则绕过护甲、抗性与无敌帧，每一次都实收 {COST} 点。
# 命中前已经在 trigger 里确认过生命高于 {COST}，所以不会把自己写死。
scoreboard players remove @s rpg_levi_hp {COST}
execute store result entity @s Health float 1 run scoreboard players get @s rpg_levi_hp
effect give @s minecraft:unluck {UNLUCK} 0 true
particle damage_indicator ~ ~1 ~ 0.3 0.4 0.3 0.2 12
playsound minecraft:entity.player.hurt_drown player @s ~ ~ ~ 1 0.7
tag @s add rpg.levi.cast
# 凌空抛锚沉得更深：脚下悬空就是"从高处砸下"，与重锤的本能一致
execute at @s if block ~ ~-1 ~ air run tag @s add rpg.levi.airborne
particle dust_color_transition{{from_color:{GOLD},to_color:{ABYSS},scale:1}} ~ ~1.1 ~ 0.3 0.4 0.3 0.02 16
playsound minecraft:block.chain.break player @a[distance=..24] ~ ~ ~ 1 0.6
playsound minecraft:item.mace.smash_air player @a[distance=..24] ~ ~ ~ 1 0.7
execute at @s rotated ~ 0 positioned ^ ^ ^{THROW} run function rpg:item/extra/leviathan_drop
tag @s remove rpg.levi.airborne
tag @s remove rpg.levi.cast
"""

DROP = """\
# 锚咬住海床，漩涡张开。
summon minecraft:marker ~ ~ ~ {{Tags:["rpg.levi.new"]}}
execute unless entity @a[tag=rpg.levi.airborne,distance=..24] run scoreboard players set @e[tag=rpg.levi.new] rpg_levi_time {LIFE}
execute if entity @a[tag=rpg.levi.airborne,distance=..24] run scoreboard players set @e[tag=rpg.levi.new] rpg_levi_time {LIFE_DEEP}
scoreboard players set @e[tag=rpg.levi.new] rpg_levi_beat {BEAT}
tag @e[tag=rpg.levi.new] add rpg.levi.anchor
tag @e[tag=rpg.levi.new] remove rpg.levi.new

particle minecraft:flash{{color:{FOAM}}} ~ ~0.6 ~ 0 0 0 0 1
particle splash ~ ~0.4 ~ 1.2 0.3 1.2 0.4 60
particle bubble_column_up ~ ~ ~ 1.4 0.2 1.4 0.05 50
particle dust_color_transition{{from_color:{ABYSS},to_color:{FOAM},scale:2}} ~ ~0.6 ~ 1.5 0.4 1.5 0.06 70
playsound minecraft:block.anvil_land hostile @a[distance=..28] ~ ~ ~ 1 0.5
playsound minecraft:entity.generic.splash hostile @a[distance=..24] ~ ~ ~ 1 0.6
"""

PULL = """\
# 每刻：把 {RADIUS} 格内的一切拖向锚心，并铺开漩涡的水纹。
# 漩涡要转满 5~8 秒，所以每刻的粒子必须省着用：
# 原本每刻 36 粒 × 100 刻 ≈ 3600 粒，客户端明显吃不消。现在每刻 13 粒。
particle dust_color_transition{{from_color:{TRENCH},to_color:{ABYSS},scale:2}} ~ ~0.3 ~ {RADIUS_F} 0.25 {RADIUS_F} 0.02 9
particle bubble_column_up ~ ~ ~ 0.8 0.1 0.8 0.03 3
particle dust_color_transition{{from_color:{ABYSS},to_color:{GOLD},scale:1}} ~ ~1.4 ~ 0.2 0.5 0.2 0.02 1
execute as @e[distance=1.2..{RADIUS},type=!player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:marker] at @s facing entity @e[tag=rpg.levi.anchor,limit=1,sort=nearest] feet run tp @s ^ ^ ^0.55
execute as @e[distance=..{RADIUS},type=!player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:marker] run effect give @s minecraft:slowness 2 2 true
"""

CRUSH = """\
# 每 {BEAT} 刻碾一次：生物受伤后约有 {BEAT} 刻无敌帧，打得更密只是浪费。
scoreboard players set @s rpg_levi_beat {BEAT}
particle minecraft:flash{{color:{ABYSS}}} ~ ~0.8 ~ 0 0 0 0 1
particle splash ~ ~0.5 ~ 1 0.3 1 0.3 14
playsound minecraft:entity.player.attack.crit hostile @a[distance=..20] ~ ~ ~ 1 0.6
execute as @e[distance=..{RADIUS},type=!player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:marker] at @s run damage @s 6 minecraft:drown
execute as @e[distance=..{RADIUS},type=!player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:marker] at @s run particle dust_color_transition{{from_color:{FOAM},to_color:{TRENCH},scale:2}} ~ ~1 ~ 0.3 0.5 0.3 0.05 10
"""

TICK = """\
# 漩涡的存续。由 rpg:item/extra/skills 守卫调用 ——
# 没人握着利维坦、场上也没有锚时整段跳过。
execute as @e[tag=rpg.levi.anchor] at @s run function rpg:item/extra/leviathan_pull
execute as @e[tag=rpg.levi.anchor] run scoreboard players remove @s rpg_levi_beat 1
execute as @e[tag=rpg.levi.anchor,scores={{rpg_levi_beat=..0}}] at @s run function rpg:item/extra/leviathan_crush
execute as @e[tag=rpg.levi.anchor,scores={{rpg_levi_time=1..}}] run scoreboard players remove @s rpg_levi_time 1
execute as @e[tag=rpg.levi.anchor,scores={{rpg_levi_time=..0}}] at @s run particle splash ~ ~0.4 ~ 1 0.3 1 0.3 40
execute as @e[tag=rpg.levi.anchor,scores={{rpg_levi_time=..0}}] run kill @s
"""

ARGS = dict(ABYSS=ABYSS, TRENCH=TRENCH, FOAM=FOAM, GOLD=GOLD,
            COST=COST, COST_1=COST + 1, UNLUCK=UNLUCK,
            THROW=THROW, RADIUS=RADIUS, RADIUS_F="%.1f" % (RADIUS * 0.5),
            BEAT=BEAT, LIFE=LIFE, LIFE_DEEP=LIFE_DEEP)


def build_functions():
    wf("item/extra/leviathan_trigger.mcfunction", TRIGGER.format(**ARGS))
    wf("item/extra/leviathan_cast.mcfunction", CAST.format(**ARGS))
    wf("item/extra/leviathan_drop.mcfunction", DROP.format(**ARGS))
    wf("item/extra/leviathan_pull.mcfunction", PULL.format(**ARGS))
    wf("item/extra/leviathan_crush.mcfunction", CRUSH.format(**ARGS))
    wf("item/extra/leviathan.mcfunction", TICK.format(**ARGS))

    path = os.path.join(FUNC, "item/extra/skills.mcfunction")
    s = io.open(path, encoding="utf-8").read()
    dispatch = (
        "execute if entity @a[tag=rpg.h.leviathan_tag1] "
        "run function rpg:item/extra/leviathan\n"
        "execute unless entity @a[tag=rpg.h.leviathan_tag1] "
        "if entity @e[type=minecraft:marker,tag=rpg.levi.anchor] "
        "run function rpg:item/extra/leviathan\n")
    if "item/extra/leviathan" not in s:
        io.open(path, "w", encoding="utf-8", newline="\n").write(
            s.rstrip("\n") + "\n" + dispatch)


def add_objectives():
    path = os.path.join(FUNC, "command/soreboard.mcfunction")
    s = io.open(path, encoding="utf-8").read()
    add = [n for n in ("rpg_levi_time", "rpg_levi_beat", "rpg_levi_hp")
           if n not in s]
    if add:
        io.open(path, "w", encoding="utf-8", newline="\n").write(
            s.rstrip("\n") + "\n"
            + "\n".join("scoreboard objectives add %s dummy" % n for n in add) + "\n")
    return add


def register_index():
    path = os.path.join(FUNC, "command/index.mcfunction")
    lines = io.open(path, encoding="utf-8").read().split("\n")
    have = set(lines)
    clear = "tag @a remove rpg.h.leviathan_tag1"
    add = ("execute as @a if items entity @s weapon.mainhand "
           "*[minecraft:custom_data~{leviathan_tag:1b}] run tag @s add rpg.h.leviathan_tag1")
    if add in have:
        return False
    out, done_clear, done_add = [], False, False
    for l in lines:
        if not done_clear and l.startswith("execute as @a if items entity @s weapon.mainhand"):
            if clear not in have:
                out.append(clear)
            done_clear = True
        if not done_add and done_clear and l.startswith("## "):
            out.extend([add, ""])
            done_add = True
        out.append(l)
    if not done_add:
        if clear not in have:
            out.append(clear)
        out.append(add)
    io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    return True


def main():
    art = build_texture()
    build_models()
    fresh = build_give()
    build_advancement()
    build_functions()
    indexed = register_index()
    obj = add_objectives()
    print("leviathan: art %s" % art)
    print("leviathan: base=%s cmd=%d consume=%d give=%s index=%s objectives=%s"
          % (BASE, CMD, CONSUME, "added" if fresh else "already present",
             "registered" if indexed else "present", obj or "-"))


if __name__ == "__main__":
    main()
