# -*- coding: utf-8 -*-
"""Original skill logic for the five weapons built from the unused art.

Nothing here reuses an existing skill.  The arrow skills follow the shape the
pack already uses for 潮涌/不熄/毒药 (tag the arrow at the shooter, drive it in
flight, kill it on impact); the melee skills follow the `rpg.hurt` + `on attacker`
shape used by legend1.  Written straight into the optimised (tag=) form and
registered in rpg:command/index, so the per-tick NBT-scan count stays at zero.
"""

import io
import os
import re
import sys

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data/rpg/function")

# custom_data flag -> the tag rpg:command/index caches it under
SKILL_TAGS = ["deep_seek_tag", "mischief_tag", "rift_tag", "vine_tag", "truth_tag"]
# only the melee skills need a "did this player just deal damage" gate;
# rpg_vine_lash is the whip's follow-up counter and is plain dummy
OBJECTIVES = [
    ("truth", "minecraft.custom:minecraft.damage_dealt"),
    ("rpg_vine_lash", "dummy"),
]

# colours sampled straight out of the weapons' own textures, packed 0xRRGGBB
# (these two particles reject a 3-float colour; packed int is unambiguous)
LEAF_GREEN = 12835692   # #C3DB6C -- the vine whip's leaf colour, 46% of its pixels
GALE_GOLD = 16766519    # #FFD637 -- the burst gale bow's highlight gold

ARROW = "minecraft:arrow"


def w(rel, text):
    path = os.path.join(FUNC, rel)
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text.rstrip("\n") + "\n")


def impact_cleanup(tag):
    """Arrows in this pack are killed the moment they touch a block."""
    return "\n".join(
        "execute as @e[tag=%s] at @s unless block %s air run kill @s" % (tag, off)
        for off in ("~ ~-0.1 ~", "~ ~0.1 ~", "~0.1 ~ ~", "~-0.1 ~ ~",
                    "~ ~ ~-0.1", "~ ~ ~0.1"))


# ---------------------------------------------------------------------------
# 蔚蓝追寻者 · 深潜 -- drags what it hits downward and roots it
# ---------------------------------------------------------------------------
DEEP = """\
# 蔚蓝追寻者［深潜］
# 箭矢拖着深海的水压飞行；命中生物时把目标向下拽入"深渊"并短暂锚定。
execute as @e[type={A},tag=!rpg.deep] on origin if entity @s[tag=rpg.h.deep_seek_tag1] at @s run tag @e[type={A},distance=0..2] add rpg.deep
execute as @e[tag=rpg.deep] at @s run particle dust_color_transition{{from_color:[0.0,0.29,0.61],to_color:[0.20,0.85,0.95],scale:1}} ~ ~ ~ 0.12 0.12 0.12 0.1 6
execute as @e[tag=rpg.deep] at @s run particle bubble ~ ~ ~ 0.1 0.1 0.1 0.02 2
execute as @e[tag=rpg.deep] at @s if entity @e[distance=0.1..1.6,type=!{A}] unless entity @a[tag=rpg.h.deep_seek_tag1,distance=..1.6] run particle bubble_column_up ~ ~0.4 ~ 0.4 0.6 0.4 0.05 40
execute as @e[tag=rpg.deep] at @s if entity @e[distance=0.1..1.6,type=!{A}] unless entity @a[tag=rpg.h.deep_seek_tag1,distance=..1.6] run particle dust_color_transition{{from_color:[0.0,0.29,0.61],to_color:[0.20,0.85,0.95],scale:3}} ~ ~0.6 ~ 0.5 0.6 0.5 0.1 30
execute as @e[tag=rpg.deep] at @s if entity @e[distance=0.1..1.6,type=!{A}] unless entity @a[tag=rpg.h.deep_seek_tag1,distance=..1.6] run effect give @e[distance=..1.6,limit=1,sort=nearest,type=!{A}] minecraft:slowness 4 3 true
execute as @e[tag=rpg.deep] at @s if entity @e[distance=0.1..1.6,type=!{A}] unless entity @a[tag=rpg.h.deep_seek_tag1,distance=..1.6] run effect give @e[distance=..1.6,limit=1,sort=nearest,type=!{A}] minecraft:mining_fatigue 4 1 true
execute as @e[tag=rpg.deep] at @s if entity @e[distance=0.1..1.6,type=!{A}] unless entity @a[tag=rpg.h.deep_seek_tag1,distance=..1.6] run data merge entity @e[distance=..1.6,limit=1,sort=nearest,type=!{A}] {{Motion:[0d,-1.1d,0d]}}
execute as @e[tag=rpg.deep] at @s if entity @e[distance=0.1..1.6,type=!{A}] unless entity @a[tag=rpg.h.deep_seek_tag1,distance=..1.6] run playsound minecraft:ambient.underwater.enter player @a[distance=..12]
{K}
"""

# ---------------------------------------------------------------------------
# 稚弩 · 顽劣 -- no damage bonus at all, it just ruins the target's day
# ---------------------------------------------------------------------------
MISCHIEF = """\
# 稚弩［顽劣］
# 不加伤害：命中的目标被恶作剧缠上——眩晕、脱力，并在一段时间内无处可藏。
execute as @e[type={A},tag=!rpg.mis] on origin if entity @s[tag=rpg.h.mischief_tag1] at @s run tag @e[type={A},distance=0..2] add rpg.mis
execute as @e[tag=rpg.mis] at @s run particle dust_color_transition{{from_color:[1.0,0.45,0.85],to_color:[1.0,0.85,0.35],scale:1}} ~ ~ ~ 0.1 0.1 0.1 0.1 5
execute as @e[tag=rpg.mis] at @s if entity @e[distance=0.1..1.6,type=!{A}] unless entity @a[tag=rpg.h.mischief_tag1,distance=..1.6] run particle firework ~ ~0.6 ~ 0.4 0.4 0.4 0.12 40
execute as @e[tag=rpg.mis] at @s if entity @e[distance=0.1..1.6,type=!{A}] unless entity @a[tag=rpg.h.mischief_tag1,distance=..1.6] run particle happy_villager ~ ~0.8 ~ 0.5 0.5 0.5 0.1 20
execute as @e[tag=rpg.mis] at @s if entity @e[distance=0.1..1.6,type=!{A}] unless entity @a[tag=rpg.h.mischief_tag1,distance=..1.6] run effect give @e[distance=..1.6,limit=1,sort=nearest,type=!{A}] minecraft:nausea 6 0 true
execute as @e[tag=rpg.mis] at @s if entity @e[distance=0.1..1.6,type=!{A}] unless entity @a[tag=rpg.h.mischief_tag1,distance=..1.6] run effect give @e[distance=..1.6,limit=1,sort=nearest,type=!{A}] minecraft:weakness 8 1 true
execute as @e[tag=rpg.mis] at @s if entity @e[distance=0.1..1.6,type=!{A}] unless entity @a[tag=rpg.h.mischief_tag1,distance=..1.6] run effect give @e[distance=..1.6,limit=1,sort=nearest,type=!{A}] minecraft:glowing 10 0 true
execute as @e[tag=rpg.mis] at @s if entity @e[distance=0.1..1.6,type=!{A}] unless entity @a[tag=rpg.h.mischief_tag1,distance=..1.6] run playsound minecraft:entity.allay.item_thrown player @a[distance=..12]
{K}
"""

# ---------------------------------------------------------------------------
# 疾风迸发之弓 · 裂空 -- the only area-of-effect launcher among the bows
# ---------------------------------------------------------------------------
RIFT = """\
# 疾风迸发之弓［裂空］
# 箭矢命中处炸开一道风的裂隙，把周围三格内的一切掀上天并造成风压伤害。
execute as @e[type={A},tag=!rpg.rift] on origin if entity @s[tag=rpg.h.rift_tag1] at @s run tag @e[type={A},distance=0..2] add rpg.rift
execute as @e[tag=rpg.rift] at @s run particle dust_color_transition{{from_color:[1.0,0.94,0.62],to_color:[0.85,0.95,1.0],scale:1}} ~ ~ ~ 0.1 0.1 0.1 0.15 5
execute as @e[tag=rpg.rift] at @s if entity @e[distance=0.1..1.6,type=!{A}] unless entity @a[tag=rpg.h.rift_tag1,distance=..1.6] run particle minecraft:flash{{color:{GOLD}}} ~ ~0.7 ~ 0 0 0 0 1
execute as @e[tag=rpg.rift] at @s if entity @e[distance=0.1..1.6,type=!{A}] unless entity @a[tag=rpg.h.rift_tag1,distance=..1.6] run particle minecraft:flash{{color:{GOLD}}} ~ ~1.4 ~ 0 0 0 0 1
execute as @e[tag=rpg.rift] at @s if entity @e[distance=0.1..1.6,type=!{A}] unless entity @a[tag=rpg.h.rift_tag1,distance=..1.6] run particle gust_emitter_large ~ ~0.5 ~ 0 0 0 0 1
execute as @e[tag=rpg.rift] at @s if entity @e[distance=0.1..1.6,type=!{A}] unless entity @a[tag=rpg.h.rift_tag1,distance=..1.6] run particle sweep_attack ~ ~0.8 ~ 1.2 0.6 1.2 0 12
execute as @e[tag=rpg.rift] at @s if entity @e[distance=0.1..1.6,type=!{A}] unless entity @a[tag=rpg.h.rift_tag1,distance=..1.6] run execute as @e[distance=..3,type=!{A},type=!player] run damage @s 3 minecraft:player_attack by @a[tag=rpg.h.rift_tag1,limit=1,sort=nearest]
execute as @e[tag=rpg.rift] at @s if entity @e[distance=0.1..1.6,type=!{A}] unless entity @a[tag=rpg.h.rift_tag1,distance=..1.6] run data merge entity @e[distance=..3,limit=1,sort=nearest,type=!{A}] {{Motion:[0d,0.95d,0d]}}
execute as @e[tag=rpg.rift] at @s if entity @e[distance=0.1..1.6,type=!{A}] unless entity @a[tag=rpg.h.rift_tag1,distance=..1.6] run playsound minecraft:entity.breeze.wind_burst player @a[distance=..16]
{K}
"""

# ---------------------------------------------------------------------------
# 藤蔓之鞭 · 缠绕 -- reels the target in; nothing else in the pack pulls
# ---------------------------------------------------------------------------
VINE = """\
# 藤蔓之鞭［缠绕］—— 起手看浮标，之后每刻负责落鞭。
function rpg:item/extra/vine_trigger

#
# 每鞭间隔 10 刻：生物受伤后有约 10 刻无敌帧，连着每刻打只有第一下算数。
# 计数器从 60 倒数，在 50 / 40 / 30 / 20 / 10 / 1 六个刻落鞭，正好三秒六鞭。
execute as @e[scores={{rpg_vine_lash=50}}] run tag @s add rpg.vine.strike
execute as @e[scores={{rpg_vine_lash=40}}] run tag @s add rpg.vine.strike
execute as @e[scores={{rpg_vine_lash=30}}] run tag @s add rpg.vine.strike
execute as @e[scores={{rpg_vine_lash=20}}] run tag @s add rpg.vine.strike
execute as @e[scores={{rpg_vine_lash=10}}] run tag @s add rpg.vine.strike
execute as @e[scores={{rpg_vine_lash=1}}] run tag @s add rpg.vine.strike

execute as @e[tag=rpg.vine.strike] at @s run particle minecraft:tinted_leaves{{color:{LEAF}}} ~ ~0.9 ~ 0.45 0.55 0.45 0.02 24
execute as @e[tag=rpg.vine.strike] at @s run particle crit ~ ~0.9 ~ 0.3 0.35 0.3 0.12 10
execute as @e[tag=rpg.vine.strike] at @s run particle sweep_attack ~ ~0.9 ~ 0.2 0.2 0.2 0 1
execute as @e[tag=rpg.vine.strike] at @s if entity @a[tag=rpg.h.vine_tag1,distance=..20] run damage @s 2 minecraft:player_attack by @a[tag=rpg.h.vine_tag1,limit=1,sort=nearest]
execute as @e[tag=rpg.vine.strike] at @s unless entity @a[tag=rpg.h.vine_tag1,distance=..20] run damage @s 2 minecraft:player_attack
execute as @e[tag=rpg.vine.strike] at @s run title @a[tag=rpg.h.vine_tag1,limit=1,sort=nearest,distance=..20] actionbar ["",{{"text":"缠绕","color":"green","bold":true}},{{"text":" 鞭击命中","color":"white"}}]

# 音调逐鞭升高，一耳就能听出打到第几鞭
execute as @e[scores={{rpg_vine_lash=50}}] at @s run playsound minecraft:entity.player.attack.sweep player @a[distance=..16] ~ ~ ~ 1 0.8
execute as @e[scores={{rpg_vine_lash=40}}] at @s run playsound minecraft:entity.player.attack.sweep player @a[distance=..16] ~ ~ ~ 1 0.95
execute as @e[scores={{rpg_vine_lash=30}}] at @s run playsound minecraft:entity.player.attack.sweep player @a[distance=..16] ~ ~ ~ 1 1.1
execute as @e[scores={{rpg_vine_lash=20}}] at @s run playsound minecraft:entity.player.attack.sweep player @a[distance=..16] ~ ~ ~ 1 1.3
execute as @e[scores={{rpg_vine_lash=10}}] at @s run playsound minecraft:entity.player.attack.sweep player @a[distance=..16] ~ ~ ~ 1 1.5
execute as @e[scores={{rpg_vine_lash=1}}] at @s run playsound minecraft:entity.player.attack.sweep player @a[distance=..16] ~ ~ ~ 1 1.8

tag @e[tag=rpg.vine.strike] remove rpg.vine.strike
execute as @e[tag=rpg.vine.lash,scores={{rpg_vine_lash=1..}}] run scoreboard players remove @s rpg_vine_lash 1
tag @e[tag=rpg.vine.lash,scores={{rpg_vine_lash=..0}}] remove rpg.vine.lash
"""

# 鱼竿的抛投是物品类写死的行为，consumable 组件抢不过它 —— 右键永远在甩钩。
# 所以干脆把"甩出去的浮标"当成挥鞭动作本身：浮标一出现就换成一次鞭击，
# 随即把浮标收掉，鱼竿也就顺势弹回，看起来正是甩鞭又收鞭。
VINE_TRIGGER = """\
# 甩鞭：浮标即挥鞭。命中判定与收鞭都在同一刻完成，所以不会重复触发。
execute as @e[type=minecraft:fishing_bobber] on origin if entity @s[tag=rpg.h.vine_tag1,level=1..] at @s run function rpg:item/extra/vine_cast
execute as @e[type=minecraft:fishing_bobber] on origin if entity @s[tag=rpg.h.vine_tag1,level=..0] run playsound minecraft:entity.villager.no player @s
execute as @e[type=minecraft:fishing_bobber] on origin if entity @s[tag=rpg.h.vine_tag1] run tag @s add rpg.vine.reel
execute as @e[type=minecraft:fishing_bobber] at @s if entity @a[tag=rpg.vine.reel,distance=..48] run kill @s
tag @a[tag=rpg.vine.reel] remove rpg.vine.reel
"""

VINE_CAST = """\
# 甩鞭：消耗 1 级经验，把 6 格内的敌人全部拽近并挂上三秒连击
xp add @s -1 levels
tag @s add rpg.vine.src
particle minecraft:tinted_leaves{{color:{LEAF}}} ~ ~1 ~ 1.3 0.7 1.3 0.05 70
particle spore_blossom_air ~ ~1 ~ 1.3 0.7 1.3 0 20
playsound minecraft:block.cave_vines.break player @a[distance=..16] ~ ~ ~ 1 0.7
execute as @e[distance=0.1..6,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run function rpg:item/extra/vine_grab
tag @s remove rpg.vine.src
"""

VINE_GRAB = """\
# 每个被缠住的目标：拽近一步、钉住、挂上六鞭的计数
scoreboard players set @s rpg_vine_lash 60
tag @s add rpg.vine.lash
effect give @s minecraft:slowness 4 3 true
execute if entity @a[tag=rpg.vine.src,distance=1.6..8] facing entity @a[tag=rpg.vine.src,limit=1,sort=nearest] feet run tp @s ^ ^ ^1.6
particle minecraft:tinted_leaves{{color:{LEAF}}} ~ ~1 ~ 0.4 0.5 0.4 0.02 20
"""

# ---------------------------------------------------------------------------
# 求真之刃 · 洞悉 -- reads the victim's health straight off damage_action
# ---------------------------------------------------------------------------
TRUTH = """\
# 求真之刃［洞悉］
# 命中即显形；当目标生命值降到 20 以下，谎言散尽，追加一次真实伤害。
# 血量直接读 damage_action —— 那是 rpg:command/index 每刻已经抓好的，不额外开销。
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={{truth=0..}},tag=rpg.h.truth_tag1] run tag @s add rpg.truth.src
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.truth.src,distance=..7] run particle end_rod ~ ~1 ~ 0.3 0.5 0.3 0.02 18
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.truth.src,distance=..7] run effect give @s minecraft:glowing 6 0 true
execute as @e[tag=rpg.hurt,scores={{damage_action=..20}}] at @s if entity @a[tag=rpg.truth.src,distance=..7] run particle enchanted_hit ~ ~1 ~ 0.3 0.4 0.3 0 20
execute as @e[tag=rpg.hurt,scores={{damage_action=..20}}] at @s if entity @a[tag=rpg.truth.src,distance=..7] run particle dust_color_transition{{from_color:[1.0,0.95,0.8],to_color:[0.8,0.1,0.1],scale:2}} ~ ~1 ~ 0.4 0.5 0.4 0.1 30
execute as @e[tag=rpg.hurt,scores={{damage_action=..20}},type=!player] at @s if entity @a[tag=rpg.truth.src,distance=..7] run damage @s 4 minecraft:magic by @a[tag=rpg.truth.src,limit=1,sort=nearest]
execute as @e[tag=rpg.hurt,scores={{damage_action=..20}}] at @s if entity @a[tag=rpg.truth.src,distance=..7] run playsound minecraft:block.amethyst_block.resonate player @a[distance=..12]
tag @a[tag=rpg.truth.src] remove rpg.truth.src
scoreboard players reset * truth
"""

ROOT = """\
# 新锻装备的原创技能总入口。由 rpg:command/tick 每刻调用一次。
#
# 每条都先过一次守卫：没人拿着这件武器、场上也没有它留下的痕迹时，
# 整个函数直接跳过。空闲一刻的代价因此只是几次标签检查，而不是十几次全场遍历。
# 箭矢类的技能要在射手换手之后仍然把箭送完，所以第二个条件看的是箭上的标记；
# 藤蔓之鞭的连击标记落在任意生物上，没有类型可以先筛，
# 而它只持续三秒 —— 握持判定已经够用，就不再额外全场扫一遍。
execute if entity @a[tag=rpg.h.deep_seek_tag1] run function rpg:item/extra/deep_seek
execute unless entity @a[tag=rpg.h.deep_seek_tag1] if entity @e[type=minecraft:arrow,tag=rpg.deep] run function rpg:item/extra/deep_seek
execute if entity @a[tag=rpg.h.mischief_tag1] run function rpg:item/extra/mischief
execute unless entity @a[tag=rpg.h.mischief_tag1] if entity @e[type=minecraft:arrow,tag=rpg.mis] run function rpg:item/extra/mischief
execute if entity @a[tag=rpg.h.rift_tag1] run function rpg:item/extra/rift
execute unless entity @a[tag=rpg.h.rift_tag1] if entity @e[type=minecraft:arrow,tag=rpg.rift] run function rpg:item/extra/rift
execute if entity @a[tag=rpg.h.vine_tag1] run function rpg:item/extra/vine
execute if entity @a[tag=rpg.h.truth_tag1] run function rpg:item/extra/truth
"""


def build_functions():
    w("item/extra/deep_seek.mcfunction", DEEP.format(A=ARROW, K=impact_cleanup("rpg.deep")))
    w("item/extra/mischief.mcfunction", MISCHIEF.format(A=ARROW, K=impact_cleanup("rpg.mis")))
    w("item/extra/rift.mcfunction", RIFT.format(A=ARROW, GOLD=GALE_GOLD, K=impact_cleanup("rpg.rift")))
    w("item/extra/vine.mcfunction", VINE.format(LEAF=LEAF_GREEN))
    w("item/extra/vine_trigger.mcfunction", VINE_TRIGGER)
    w("item/extra/vine_cast.mcfunction", VINE_CAST.format(LEAF=LEAF_GREEN))
    w("item/extra/vine_grab.mcfunction", VINE_GRAB.format(LEAF=LEAF_GREEN))
    drop_vine_advancement()
    w("item/extra/truth.mcfunction", TRUTH.format())
    w("item/extra/skills.mcfunction", ROOT)


VINE_CONSUME = 100090


def drop_vine_advancement():
    """The consumable route never fires on a fishing rod; remove its leftovers."""
    for rel in ("../advancement/item/vine.json",):
        p = os.path.join(FUNC, rel)
        if os.path.isfile(p):
            os.remove(p)


def build_vine_advancement():
    import json
    adv = os.path.join(DP, "data/rpg/advancement/item")
    if not os.path.isdir(adv):
        os.makedirs(adv)
    doc = {"criteria": {"requirement": {
        "trigger": "minecraft:using_item",
        "conditions": {"item": {"components": {
            "minecraft:food": {"nutrition": 0, "saturation": 0, "can_always_eat": True},
            "minecraft:consumable": {
                "consume_seconds": float(VINE_CONSUME), "animation": "eat",
                "sound": "minecraft:entity.generic.eat",
                "has_consume_particles": True, "on_consume_effects": []}}}}}},
        "rewards": {"function": "rpg:item/extra/vine_trigger"}}
    with io.open(os.path.join(adv, "vine.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def hook_tick():
    """Run the skills once per tick, right after the built-in weapon handlers."""
    path = os.path.join(FUNC, "command/tick.mcfunction")
    s = io.open(path, encoding="utf-8").read()
    line = "function rpg:item/extra/skills"
    if line in s:
        return False
    s = s.replace("function rpg:item/bow/legend/hunter/hunter",
                  "function rpg:item/bow/legend/hunter/hunter\n\n" + line, 1)
    io.open(path, "w", encoding="utf-8", newline="\n").write(s)
    return True


def add_objectives():
    path = os.path.join(FUNC, "command/soreboard.mcfunction")
    s = io.open(path, encoding="utf-8").read()
    added = []
    block = []
    for o, crit in OBJECTIVES:
        if re.search(r"^scoreboard objectives add %s " % o, s, re.M):
            continue
        block.append("scoreboard objectives add %s %s" % (o, crit))
        added.append(o)
    if block:
        s = s.rstrip("\n") + "\n\n##新增装备技能\n" + "\n".join(block) + "\n"
        io.open(path, "w", encoding="utf-8", newline="\n").write(s)
    return added


def register_index():
    """Cache each new held-item flag the same way every other flag is cached."""
    path = os.path.join(FUNC, "command/index.mcfunction")
    lines = io.open(path, encoding="utf-8").read().split("\n")
    have = set(l for l in lines)
    clears, sets = [], []
    for t in SKILL_TAGS:
        tag = "rpg.h.%s1" % t
        c = "tag @a remove %s" % tag
        d = ("execute as @a if items entity @s weapon.mainhand "
             "*[minecraft:custom_data~{%s:1b}] run tag @s add %s" % (t, tag))
        if c not in have:
            clears.append(c)
        if d not in have:
            sets.append(d)
    if not clears and not sets:
        return 0
    out, done_c, done_s = [], False, False
    for i, l in enumerate(lines):
        # the clear block ends where the first `execute as @a if items` begins
        if not done_c and l.startswith("execute as @a if items entity @s weapon.mainhand"):
            out.extend(clears)
            done_c = True
        # the held-item set block ends at the blank line before the next heading
        if not done_s and done_c and l.startswith("## "):
            out.extend(sets)
            out.append("")
            done_s = True
        out.append(l)
    if not done_s:
        out.extend(sets)
    io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    return len(sets)


if __name__ == "__main__":
    build_functions()
    print("skill functions written: 6")
    print("objectives added: %s" % (", ".join(add_objectives()) or "(already present)"))
    print("tick hook added: %s" % hook_tick())
    print("index flags registered: %d" % register_index())
