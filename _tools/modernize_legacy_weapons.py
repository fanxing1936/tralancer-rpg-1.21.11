# -*- coding: utf-8 -*-
"""Modernise the first batch of weapons inherited from the original pack.

The original implementations pre-date the newer Lucifer/Leviathan/rune skill
layout.  They live as unrelated blocks in ``legend1.mcfunction``, reset shared
vanilla-stat objectives with ``reset *``, and recover the struck entity with a
nearest-entity selector.  That is both difficult to extend and unsafe when two
players fight in the same place.

This pass replaces four especially old passive weapons with one guarded entry
point and small, named cast functions.  ``rpg.hurt`` is processed sequentially;
the current victim receives a temporary tag, then ``on attacker`` resolves the
actual player who dealt that hit.  No nearest-player guess and no global score
reset are involved.

Run after the 1.21.11 migration/optimisation and content generators, but before
``opt_actionbar.py``.  The four direct actionbar messages below are deliberate:
that later pass assigns them HUD message slots and keeps the one-output rule.
"""

from __future__ import print_function

import io
import os
import re
import sys


DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data", "rpg", "function")


def path(rel):
    return os.path.join(FUNC, rel.replace("/", os.sep))


def read(rel):
    return io.open(path(rel), encoding="utf-8").read()


def write(rel, body):
    p = path(rel)
    d = os.path.dirname(p)
    if not os.path.isdir(d):
        os.makedirs(d)
    io.open(p, "w", encoding="utf-8", newline="\n").write(
        body.rstrip("\n") + "\n")


def remove(rel):
    """Remove an explicitly retired generated function, if it still exists."""
    p = path(rel)
    if os.path.isfile(p):
        os.remove(p)


def replace_section(src, start, end, replacement):
    # The following generator may already have annotated the *end* marker
    # (for example ``##史诗武器（六件……）``).  Only the marker prefix is the
    # interface between passes; preserve whatever annotation follows it.
    pattern = r"(?ms)^##%s\s*$.*?(?=^##%s[^\r\n]*$)" % (
        re.escape(start), re.escape(end))
    out, count = re.subn(pattern, replacement.rstrip() + "\n\n", src, count=1)
    if count != 1:
        modern_marker = replacement.strip().splitlines()[0]
        if modern_marker.startswith("##") and modern_marker in src:
            return src
        raise AssertionError("legacy section not found: %s -> %s" % (start, end))
    return out


LEGACY_LORE = {
    # Only the effect sentence changes. Prefixes, names, narrative copy,
    # separators, component colours and the original one-line card shape stay
    # byte-for-byte as authored around it.
    "消耗3级经验射出潮涌之箭": "箭矢命中时托起敌人并使其显形",
    "攻击时有3/5的概率附带": "命中削弱敌人，四成概率唤出",
    "对5米内的所有生物释放斩击": "连击推进四幕；蓄力1.5秒斩击5格并扫箭",
    "攻击时附带连续切割效果": "命中撕开血痂，追加切割并使其虚弱",
    "消耗1/4生命获得短时间全方位增幅": "连续命中推进四景，第四击引雷并自护",
    "在箭矢命中后召唤火矢": "箭矢命中灼烧5秒并追加火焰伤害",
    "向前方释放三道龙卷风": "长按蓄力1.5秒，向前卷起三道风路",
    "攻击百分比伤害": "重击震裂目标，追加伤害并压低脚步",
    "副手手持时增加攻击伤害": "主手命中震裂敌人，副手持有时强化攻击",
    "右键武器可召唤筋斗云": "右键唤来筋斗云；命中时随机施展神通",
    "攻击时持续流血": "命中淬毒，第三次引爆积蓄的蛇毒",
    "拥有黑白两种攻击方式": "黑式破敌，白式回生，每次命中轮转",
    "攻击时附带灵魂收割": "命中收割灵魂，附加凋零与灵魂创伤",
    "释放灰烬并追加刀罡": "长按蓄力1.5秒，向前斩出三重灰烬刀罡",
    "射出箭矢附带剧毒": "射箭自损1心；命中毒爆3.5格敌人",
    "让范围7格的所有生物停止活动": "右键使7格敌人迟缓虚弱3秒；冷却1.5秒",
    "吸引被标记的敌人并追加斩杀": "命中标记6秒；蓄力1.5秒处决14格内印记",
}


def patch_lore():
    """Keep all 17 original card layouts; make only their effect line truthful."""
    rel = "command/give/weapon.mcfunction"
    src = read(rel)
    assert len(LEGACY_LORE) == 17, "the original-card lore matrix must stay 17/17"
    for old, new in LEGACY_LORE.items():
        if old not in src and new in src:
            continue
        if old not in src:
            raise AssertionError("weapon lore text not found: %s" % old)
        src = src.replace(old, new, 1)
    for new in LEGACY_LORE.values():
        if src.count(new) != 1:
            raise AssertionError("modern weapon lore is not unique: %s" % new)
    write(rel, src)


def patch_scoreboards():
    rel = "command/soreboard.mcfunction"
    src = read(rel).rstrip("\n")
    objectives = (
        "rpg_leg_cd",       # per-player passive proc throttle
        "rpg_pen_mode",     # black / white style of 风骨
        "rpg_venom",        # per-player poison build-up of 剧毒之牙
        "rpg_night_chg",    # 漆黑之刃 charge / hold
        "rpg_night_hold",
        "rpg_ashes_chg",    # 别西卜 charge / hold
        "rpg_ashes_hold",
        "rpg_wind_chg",     # 风之回响 charge / hold
        "rpg_wind_hold",
        "rpg_throne_chg",   # 朗基努斯 charge / hold and marked target time
        "rpg_throne_hold",
        "rpg_throne_mark",
        "rpg_throne_owner",
        "rpg_legacy_uid",   # stable player id for persistent throne marks
        "rpg_blil_cd",      # 贝利尔 right-click repeat gate
    )
    additions = [o for o in objectives if
                 ("scoreboard objectives add %s " % o) not in src]
    if additions:
        src += "\n\n# 老武器现代化：状态全部归玩家，不再 reset * 互踩\n"
        src += "\n".join("scoreboard objectives add %s dummy" % o
                         for o in additions)
    write(rel, src)


def patch_legacy_root():
    rel = "item/sword/legend/legend1.mcfunction"
    src = read(rel)
    src = replace_section(src, "别西卜", "贝利尔", """##别西卜（现代入口）
# 余烬改为 30 刻蓄力与无实体刀罡；旧命名载体已退役。""")
    src = replace_section(src, "贝利尔", "链锯", """##贝利尔（现代入口）
# 朝拜由独立 cast 函数处理，不再全局重置 blil。""")
    src = replace_section(src, "链锯", "漆黑之日", """##链锯（现代入口）
# 血痂已移入 rpg:item/legacy/weapons；不再使用 chainsaw/random 的全局 reset。""")
    src = replace_section(src, "高山", "风骨", """##高山（现代入口）
# 怒嚎已移入 rpg:item/legacy/weapons。""")
    src = replace_section(src, "风骨", "剧毒之牙", """##风骨（现代入口）
# 黑白二式已移入 rpg:item/legacy/weapons，式样状态按玩家保存。""")
    src = replace_section(src, "剧毒之牙", "无垠星空", """##剧毒之牙（现代入口）
# 淬毒已移入 rpg:item/legacy/weapons，毒层按攻击者保存。""")
    src = replace_section(src, "漆黑之日", "高山", """##漆黑之日（现代入口）
# 漆黑之刃改为 30 刻蓄力与一次定向斩击；旧每目标 TNT 循环已退役。""")
    src = replace_section(src, "亚巴顿", "风", """##亚巴顿（现代入口）
# 收割并入精确命中入口，不再让伤害递归写回 soul 统计。""")
    src = replace_section(src, "风", "悟空", """##风之回响（现代入口）
# 狂风改为 30 刻蓄力与三道无实体风路；旧命名载体已退役。""")
    src = replace_section(src, "朗基努斯", "史诗武器", """##朗基努斯（现代入口）
# 王座标记与处决均按玩家归属；旧最近玩家定向已退役。""")

    hook = "function rpg:item/legacy/weapons"
    if hook not in src:
        src = ("# 更新前旧武器的统一入口。实际无持有者时内部立即跳过。\n"
               + hook + "\n\n" + src.lstrip("\n"))
    write(rel, src)


def emit_functions():
    write("item/legacy/weapons.mcfunction", r"""# 更新前旧武器的统一热路径。
# 这些旧武器都无人持有时不扫描 rpg.hurt；有命中时只扫一遍，再由 on attacker
# 精确找出攻击者。冷却、黑白式、毒层全部是玩家自己的分数。
scoreboard players add @a rpg_leg_cd 0
scoreboard players add @a rpg_pen_mode 0
scoreboard players add @a rpg_venom 0
execute as @a[scores={rpg_leg_cd=1..}] run scoreboard players remove @s rpg_leg_cd 1

# 为需要跨刻保存目标的王座印分配稳定玩家号。每名新玩家独立进入函数，
# 所以不会出现同一刻加入的玩家拿到相同编号。
execute as @a unless score @s rpg_legacy_uid matches 1.. run function rpg:item/legacy/assign_uid

# 四个老主动技现在与沉锚/熔流用同一种 hold 状态机：trigger 每刻把
# hold 顶回 3，松手后三刻清空未满蓄力。贝利尔是瞬发，单独只走冷却。
scoreboard players add @a rpg_night_hold 0
scoreboard players add @a rpg_ashes_hold 0
scoreboard players add @a rpg_wind_hold 0
scoreboard players add @a rpg_throne_hold 0
execute as @a[scores={rpg_night_hold=1..}] run scoreboard players remove @s rpg_night_hold 1
execute as @a[scores={rpg_ashes_hold=1..}] run scoreboard players remove @s rpg_ashes_hold 1
execute as @a[scores={rpg_wind_hold=1..}] run scoreboard players remove @s rpg_wind_hold 1
execute as @a[scores={rpg_throne_hold=1..}] run scoreboard players remove @s rpg_throne_hold 1
scoreboard players set @a[scores={rpg_night_hold=..0,rpg_night_chg=1..}] rpg_night_chg 0
scoreboard players set @a[scores={rpg_ashes_hold=..0,rpg_ashes_chg=1..}] rpg_ashes_chg 0
scoreboard players set @a[scores={rpg_wind_hold=..0,rpg_wind_chg=1..}] rpg_wind_chg 0
scoreboard players set @a[scores={rpg_throne_hold=..0,rpg_throne_chg=1..}] rpg_throne_chg 0
scoreboard players add @a rpg_blil_cd 0
execute as @a[scores={rpg_blil_cd=1..}] run scoreboard players remove @s rpg_blil_cd 1

# 王座标记有自己的寿命；目标死亡、卸载或到时都不会留下活动实体。
execute as @e[tag=rpg.throne.mark,scores={rpg_throne_mark=1..}] run scoreboard players remove @s rpg_throne_mark 1
tag @e[tag=rpg.throne.mark,scores={rpg_throne_mark=..0}] remove rpg.throne.mark

execute if entity @a[tag=rpg.h.chainsaw_tag1] if entity @e[tag=rpg.hurt,limit=1] as @e[tag=rpg.hurt] at @s run function rpg:item/legacy/hit
execute unless entity @a[tag=rpg.h.chainsaw_tag1] if entity @a[tag=rpg.h.montain_tag1] if entity @e[tag=rpg.hurt,limit=1] as @e[tag=rpg.hurt] at @s run function rpg:item/legacy/hit
execute unless entity @a[tag=rpg.h.chainsaw_tag1] unless entity @a[tag=rpg.h.montain_tag1] if entity @a[tag=rpg.h.pen_tag1] if entity @e[tag=rpg.hurt,limit=1] as @e[tag=rpg.hurt] at @s run function rpg:item/legacy/hit
execute unless entity @a[tag=rpg.h.chainsaw_tag1] unless entity @a[tag=rpg.h.montain_tag1] unless entity @a[tag=rpg.h.pen_tag1] if entity @a[tag=rpg.h.potion_tag1] if entity @e[tag=rpg.hurt,limit=1] as @e[tag=rpg.hurt] at @s run function rpg:item/legacy/hit
execute unless entity @a[tag=rpg.h.chainsaw_tag1] unless entity @a[tag=rpg.h.montain_tag1] unless entity @a[tag=rpg.h.pen_tag1] unless entity @a[tag=rpg.h.potion_tag1] if entity @a[tag=rpg.h.soul_tag1] if entity @e[tag=rpg.hurt,limit=1] as @e[tag=rpg.hurt] at @s run function rpg:item/legacy/hit
execute unless entity @a[tag=rpg.h.chainsaw_tag1] unless entity @a[tag=rpg.h.montain_tag1] unless entity @a[tag=rpg.h.pen_tag1] unless entity @a[tag=rpg.h.potion_tag1] unless entity @a[tag=rpg.h.soul_tag1] if entity @a[tag=rpg.h.ashes_tag1] if entity @e[tag=rpg.hurt,limit=1] as @e[tag=rpg.hurt] at @s run function rpg:item/legacy/hit
execute unless entity @a[tag=rpg.h.chainsaw_tag1] unless entity @a[tag=rpg.h.montain_tag1] unless entity @a[tag=rpg.h.pen_tag1] unless entity @a[tag=rpg.h.potion_tag1] unless entity @a[tag=rpg.h.soul_tag1] unless entity @a[tag=rpg.h.ashes_tag1] if entity @a[tag=rpg.h.power_tag1] if entity @e[tag=rpg.hurt,limit=1] as @e[tag=rpg.hurt] at @s run function rpg:item/legacy/hit""")

    write("item/legacy/assign_uid.mcfunction", r"""scoreboard players add #next rpg_legacy_uid 1
scoreboard players operation @s rpg_legacy_uid = #next rpg_legacy_uid""")

    write("item/legacy/hit.mcfunction", r"""# 当前 @s 是这一刻真正受伤的实体。先清旧存档或中断执行遗留的临时目标；
# execute-as 对每个 rpg.hurt 实体顺序执行，因此同刻多场战斗也不会串目标。
tag @e[tag=rpg.legacy.target] remove rpg.legacy.target
tag @s add rpg.legacy.target
execute at @s on attacker if entity @s[type=minecraft:player,tag=rpg.h.chainsaw_tag1,scores={rpg_leg_cd=..0}] run function rpg:item/legacy/chainsaw
execute at @s on attacker if entity @s[type=minecraft:player,tag=rpg.h.montain_tag1,scores={rpg_leg_cd=..0}] run function rpg:item/legacy/mountain
execute at @s on attacker if entity @s[type=minecraft:player,tag=rpg.h.pen_tag1,scores={rpg_leg_cd=..0}] run function rpg:item/legacy/pen
execute at @s on attacker if entity @s[type=minecraft:player,tag=rpg.h.potion_tag1,scores={rpg_leg_cd=..0}] run function rpg:item/legacy/venom
execute at @s on attacker if entity @s[type=minecraft:player,tag=rpg.h.soul_tag1,scores={rpg_leg_cd=..0}] run function rpg:item/legacy/abaddon
execute at @s on attacker if entity @s[type=minecraft:player,tag=rpg.h.ashes_tag1,scores={rpg_leg_cd=..0}] run function rpg:item/legacy/ashes_hit
execute at @s on attacker if entity @s[type=minecraft:player,tag=rpg.h.power_tag1] run function rpg:item/legacy/throne_mark
tag @s remove rpg.legacy.target""")

    write("item/legacy/ashes_hit.mcfunction", r"""# 别西卜 · 普通攻击：恢复原作四段灰烬表现，但目标与攻击者都走精确归属。
# 不召唤命名盔甲架、不用 @p；五刻闸门也会拦住第四段追加伤害的递归事件。
scoreboard players set @s rpg_leg_cd 5
scoreboard players add @s ashes_level 1
execute if entity @s[scores={ashes_level=5..}] run scoreboard players set @s ashes_level 1
execute at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:large_smoke ~ ~1 ~ 0.45 0.55 0.45 0.08 20 force
execute at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:ash ~ ~1 ~ 0.4 0.5 0.4 0.05 18 force
execute as @e[tag=rpg.legacy.target,limit=1] run effect give @s minecraft:wither 2 0 true
execute if entity @s[scores={ashes_level=1}] at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:dust_pillar{block_state:{Name:"minecraft:deepslate_coal_ore"}} ~ ~1 ~ 0.45 0.55 0.45 0.15 24 force
execute if entity @s[scores={ashes_level=1}] run playsound minecraft:item.mace.smash_air player @s ~ ~ ~ 0.75 0.85
execute if entity @s[scores={ashes_level=2}] at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:sweep_attack ~ ~1 ~ 0.8 0.6 0.8 0 22 force
execute if entity @s[scores={ashes_level=2}] run playsound minecraft:item.mace.smash_ground player @s ~ ~ ~ 0.8 0.9
execute if entity @s[scores={ashes_level=3}] at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:squid_ink ~ ~1 ~ 0.65 0.7 0.65 0.08 38 force
execute if entity @s[scores={ashes_level=3}] run playsound minecraft:item.mace.smash_ground_heavy player @s ~ ~ ~ 0.8 0.75
execute if entity @s[scores={ashes_level=4}] at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:flash{color:7563296} ~ ~1 ~ 0 0 0 0 1 force
execute if entity @s[scores={ashes_level=4}] at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:dust_color_transition{from_color:[0.35,0.42,0.12],to_color:[0.08,0.08,0.05],scale:2.2} ~ ~1 ~ 0.8 0.9 0.8 0.06 55 force
execute if entity @s[scores={ashes_level=4}] run damage @e[tag=rpg.legacy.target,limit=1] 3 minecraft:magic by @s
execute if entity @s[scores={ashes_level=4}] run playsound minecraft:entity.blaze.shoot player @s ~ ~ ~ 0.9 0.55""")

    write("item/legacy/chainsaw.mcfunction", r"""# 切割链锯 · 血痂：稳定的一次追加切割；六刻闸门防止追加伤害递归触发。
scoreboard players set @s rpg_leg_cd 6
execute at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:dust{color:[0.55,0.02,0.02],scale:1.4} ~ ~1 ~ 0.45 0.55 0.45 0.08 18 force
execute at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:damage_indicator ~ ~1 ~ 0.3 0.4 0.3 0.1 8 force
execute as @e[tag=rpg.legacy.target,limit=1] run effect give @s minecraft:weakness 2 0 true
damage @e[tag=rpg.legacy.target,limit=1] 2 minecraft:player_attack by @s
playsound minecraft:block.grindstone.use player @s ~ ~ ~ 0.65 1.35
title @s actionbar ["",{"text":"[血痂]","italic":false,"color":"#C63D52","bold":true},{"text":"　锯齿咬住了血肉","italic":false,"color":"#E2A5AF"},{"text":" ✦","italic":false,"color":"#FFE8EC"}]""")

    write("item/legacy/mountain.mcfunction", r"""# 高山之啸 · 怒嚎：厚重、低频的震裂，而非旧版无差别最近实体 1 点伤害。
scoreboard players set @s rpg_leg_cd 12
execute at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:block{block_state:{Name:"minecraft:tuff"}} ~ ~0.8 ~ 0.6 0.35 0.6 0.12 32 force
execute at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:gust ~ ~1 ~ 0.35 0.25 0.35 0.08 8 force
execute as @e[tag=rpg.legacy.target,limit=1] run effect give @s minecraft:slowness 2 1 true
damage @e[tag=rpg.legacy.target,limit=1] 4 minecraft:sonic_boom by @s
playsound minecraft:item.mace.smash_ground player @s ~ ~ ~ 0.8 0.75
title @s actionbar ["",{"text":"[怒嚎]","italic":false,"color":"#D99A35","bold":true},{"text":"　山脊在刃下开裂","italic":false,"color":"#E5C88D"},{"text":" ✦","italic":false,"color":"#FFF2D2"}]""")

    write("item/legacy/pen.mcfunction", r"""# 风骨 · 着意：每次有效命中在黑、白二式之间轮转。
scoreboard players set @s rpg_leg_cd 5
execute if entity @s[scores={rpg_pen_mode=0}] run function rpg:item/legacy/pen_black
execute if entity @s[scores={rpg_pen_mode=1}] run function rpg:item/legacy/pen_white""")

    write("item/legacy/pen_black.mcfunction", r"""# 黑式破敌。
scoreboard players set @s rpg_pen_mode 1
execute at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:squid_ink ~ ~1 ~ 0.35 0.45 0.35 0.08 18 force
execute as @e[tag=rpg.legacy.target,limit=1] run effect give @s minecraft:weakness 3 1 true
damage @e[tag=rpg.legacy.target,limit=1] 3 minecraft:magic by @s
playsound minecraft:entity.squid.squirt player @s ~ ~ ~ 0.7 0.65
title @s actionbar ["",{"text":"[着意·黑]","italic":false,"color":"#727680","bold":true},{"text":"　墨锋破敌","italic":false,"color":"#AEB2BA"},{"text":" ✦","italic":false,"color":"#E8E9EC"}]""")

    write("item/legacy/pen_white.mcfunction", r"""# 白式回生。
scoreboard players set @s rpg_pen_mode 0
execute at @s run particle minecraft:cloud ~ ~1 ~ 0.3 0.45 0.3 0.03 15 force
effect give @s minecraft:instant_health 1 0 true
execute as @e[tag=rpg.legacy.target,limit=1] run effect give @s minecraft:glowing 2 0 true
playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 0.7 1.6
title @s actionbar ["",{"text":"[着意·白]","italic":false,"color":"#F2F2F2","bold":true},{"text":"　留白回生","italic":false,"color":"#D6D9DE"},{"text":" ✦","italic":false,"color":"#FFFFFF"}]""")

    write("item/legacy/venom.mcfunction", r"""# 剧毒之牙 · 淬毒：毒层属于攻击者，不会被另一名玩家重置或偷走。
scoreboard players set @s rpg_leg_cd 5
scoreboard players add @s rpg_venom 1
execute at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:dust_color_transition{from_color:[0.18,0.55,0.04],to_color:[0.72,0.95,0.16],scale:1.1} ~ ~1 ~ 0.35 0.45 0.35 0.06 12 force
execute as @e[tag=rpg.legacy.target,limit=1] run effect give @s minecraft:poison 3 0 true
playsound minecraft:entity.spider.hurt player @s ~ ~ ~ 0.55 1.35
execute if entity @s[scores={rpg_venom=3..}] run function rpg:item/legacy/venom_burst""")

    write("item/legacy/venom_burst.mcfunction", r"""# 第三次命中引爆蛇毒。
scoreboard players set @s rpg_venom 0
execute at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:entity_effect{color:65280} ~ ~1 ~ 0.55 0.65 0.55 0.2 30 force
execute as @e[tag=rpg.legacy.target,limit=1] run effect give @s minecraft:poison 5 1 true
damage @e[tag=rpg.legacy.target,limit=1] 5 minecraft:magic by @s
playsound minecraft:entity.breeze.death player @s ~ ~ ~ 0.75 1.7
title @s actionbar ["",{"text":"[淬毒]","italic":false,"color":"#5FAF2D","bold":true},{"text":"　三痕归一，蛇毒入骨","italic":false,"color":"#B7E37E"},{"text":" ✦","italic":false,"color":"#EEFFD5"}]""")

    write("item/legacy/abaddon.mcfunction", r"""# 亚巴顿 · 收割：一次明确归属的灵魂创伤，闸门阻断追加伤害递归。
scoreboard players set @s rpg_leg_cd 8
execute at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:sculk_soul ~ ~1 ~ 0.45 0.65 0.45 0.04 24 force
execute at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:trial_spawner_detection_ominous ~ ~1 ~ 0.35 0.5 0.35 0.05 12 force
execute as @e[tag=rpg.legacy.target,limit=1] run effect give @s minecraft:wither 4 1 true
damage @e[tag=rpg.legacy.target,limit=1] 4 minecraft:magic by @s
playsound minecraft:block.sculk_catalyst.bloom player @s ~ ~ ~ 0.8 0.55
title @s actionbar ["",{"text":"[收割]","italic":false,"color":"#33C7B5","bold":true},{"text":"　灵魂离壳一寸","italic":false,"color":"#9ED8D0"},{"text":" ✦","italic":false,"color":"#E8FFFB"}]""")

    write("item/legacy/throne_mark.mcfunction", r"""# 朗基努斯的普通命中刻下王座印，供主动技精确处决。
scoreboard players set @e[tag=rpg.legacy.target,limit=1] rpg_throne_mark 120
scoreboard players operation @e[tag=rpg.legacy.target,limit=1] rpg_throne_owner = @s rpg_legacy_uid
tag @e[tag=rpg.legacy.target,limit=1] add rpg.throne.mark
execute at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:dust_color_transition{from_color:[0.17,0.17,0.17],to_color:[1.0,0.2,0.0],scale:1.4} ~ ~1 ~ 0.25 0.45 0.25 0.03 10 force""")

    emit_active_functions()
    emit_projectile_functions()
    emit_hud()


def charge_trigger(adv, held_tag, charge, hold, hud_slot, particle, sound):
    """Common late-generation charge trigger, kept expanded in output."""
    return """# 旧主动技现代化：using_item 每刻推进一格，满 30 刻只触发一次。
advancement revoke @s only rpg:item/{adv}
execute if entity @s[tag={tag}] run scoreboard players set @s {hold} 3
execute if entity @s[tag={tag},scores={{{charge}=..29}}] run scoreboard players add @s {charge} 1
execute at @s if entity @s[tag={tag}] run particle {particle} ~ ~1 ~ 0.35 0.5 0.35 0.03 8
execute at @s if entity @s[tag={tag},scores={{{charge}=1}}] run playsound {sound} player @s ~ ~ ~ 0.7 0.7
execute at @s if entity @s[tag={tag},scores={{{charge}=15}}] run playsound {sound} player @s ~ ~ ~ 0.8 1.1
execute at @s if entity @s[tag={tag},scores={{{charge}=25}}] run playsound {sound} player @s ~ ~ ~ 0.9 1.5
execute if entity @s[tag={tag},scores={{{charge}=30}}] run function rpg:item/legacy/{adv}_cast
execute if entity @s[tag={tag}] run scoreboard players set @s rpg_hud {slot}
execute if entity @s[tag={tag}] run scoreboard players set @s rpg_hud_t 3
execute if entity @s[tag={tag}] run scoreboard players operation @s rpg_hud_p = @s {charge}
execute if entity @s[tag={tag}] run scoreboard players operation @s rpg_hud_p *= #hud_seg rpg_hud
execute if entity @s[tag={tag}] run scoreboard players operation @s rpg_hud_p /= #hud_full rpg_hud
execute if entity @s[scores={{rpg_hud_p=10..}}] run scoreboard players set @s rpg_hud_p 10""".format(
        adv=adv, tag=held_tag, charge=charge, hold=hold, slot=hud_slot,
        particle=particle, sound=sound)


def emit_active_functions():
    write("item/sword/legend/night/night.mcfunction", charge_trigger(
        "night", "rpg.h.night_tag1", "rpg_night_chg", "rpg_night_hold", 6,
        "minecraft:dust_color_transition{from_color:[0.4,0.0,1.0],to_color:[0.0,0.0,0.0],scale:1.4}",
        "minecraft:block.respawn_anchor.charge"))
    write("item/sword/legend/typhoon/trigger.mcfunction", charge_trigger(
        "typhoon", "rpg.h.typhoon_tag1", "rpg_wind_chg", "rpg_wind_hold", 7,
        "minecraft:dust_color_transition{from_color:[0.53,0.78,0.37],to_color:[1.0,1.0,1.0],scale:1.4}",
        "minecraft:item.trident.return"))
    write("item/sword/legend/ashes/trigger.mcfunction", charge_trigger(
        "ashes", "rpg.h.ashes_tag1", "rpg_ashes_chg", "rpg_ashes_hold", 8,
        "minecraft:dust_color_transition{from_color:[0.12,0.12,0.12],to_color:[0.45,0.1,0.02],scale:1.4}",
        "minecraft:item.mace.smash_air"))
    write("item/sword/legend/power/trigger.mcfunction", charge_trigger(
        "power", "rpg.h.power_tag1", "rpg_throne_chg", "rpg_throne_hold", 9,
        "minecraft:dust_color_transition{from_color:[0.17,0.17,0.17],to_color:[1.0,0.2,0.0],scale:1.4}",
        "minecraft:block.trial_spawner.ominous_activate"))

    write("item/legacy/night_cast.mcfunction", r"""# 漆黑之日 · 漆黑之刃：一次可读的环斩，不再对每个实体各召一枚 TNT。
scoreboard players set @s rpg_night_chg 31
tag @a[tag=rpg.night.source] remove rpg.night.source
tag @s add rpg.night.source
particle minecraft:flash{color:6684927} ~ ~1 ~ 0 0 0 0 1
particle minecraft:dust_color_transition{from_color:[0.4,0.0,1.0],to_color:[0.0,0.0,0.0],scale:2.2} ~ ~1 ~ 2.4 0.7 2.4 0.05 90 force
particle minecraft:sweep_attack ~ ~1 ~ 2 0.5 2 0 28 force
execute as @e[distance=0.1..5,type=!minecraft:player,type=!minecraft:item,type=!minecraft:experience_orb] run damage @s 8 minecraft:magic by @a[tag=rpg.night.source,limit=1]
kill @e[type=#minecraft:arrows,distance=..5]
playsound minecraft:entity.ender_dragon.shoot player @a[distance=..20] ~ ~ ~ 0.8 0.65
tag @s remove rpg.night.source
title @s actionbar ["",{"text":"[漆黑之刃]","italic":false,"color":"#8359D6","bold":true},{"text":"　夜幕合拢","italic":false,"color":"#C4AFE8"},{"text":" ✦","italic":false,"color":"#F1E9FF"}]""")

    write("item/legacy/typhoon_cast.mcfunction", r"""# 风之回响 · 狂风：三道横列风路，无 armor_stand、无 @p 定向。
scoreboard players set @s rpg_wind_chg 31
tag @a[tag=rpg.wind.source] remove rpg.wind.source
tag @s add rpg.wind.source
execute at @s positioned ^-2 ^ ^2 run function rpg:item/legacy/wind_lane
execute at @s positioned ^ ^ ^2 run function rpg:item/legacy/wind_lane
execute at @s positioned ^2 ^ ^2 run function rpg:item/legacy/wind_lane
tag @s remove rpg.wind.source
playsound minecraft:entity.breeze.shoot player @a[distance=..24] ~ ~ ~ 1 0.7
title @s actionbar ["",{"text":"[狂风]","italic":false,"color":"#63B94B","bold":true},{"text":"　三道风路并起","italic":false,"color":"#BEE5B2"},{"text":" ✦","italic":false,"color":"#F0FFE9"}]""")

    write("item/legacy/wind_lane.mcfunction", r"""# 每条风路沿施法者朝向推进三个脉冲；上下文中的 @s 仍是施法者。
execute positioned ^ ^ ^0 run function rpg:item/legacy/wind_pulse
execute positioned ^ ^ ^2 run function rpg:item/legacy/wind_pulse
execute positioned ^ ^ ^4 run function rpg:item/legacy/wind_pulse""")
    write("item/legacy/wind_pulse.mcfunction", r"""particle minecraft:gust_emitter_small ~ ~1 ~ 0.45 0.55 0.45 0.08 3 force
particle minecraft:dust_color_transition{from_color:[0.53,0.78,0.37],to_color:[1.0,1.0,1.0],scale:1.7} ~ ~1 ~ 0.7 0.8 0.7 0.04 18 force
execute as @e[distance=..1.7,type=!minecraft:player,type=!minecraft:item,type=!minecraft:experience_orb] run effect give @s minecraft:levitation 2 1 true
execute as @e[distance=..1.7,type=!minecraft:player,type=!minecraft:item,type=!minecraft:experience_orb] run effect give @s minecraft:wind_charged 4 0 true
execute as @e[distance=..1.7,type=!minecraft:player,type=!minecraft:item,type=!minecraft:experience_orb] run damage @s 3 minecraft:magic by @a[tag=rpg.wind.source,limit=1]""")

    write("item/legacy/ashes_cast.mcfunction", r"""# 别西卜 · 余烬：三段刀罡在同刻展开，不留下会串主人的命名盔甲架。
scoreboard players set @s rpg_ashes_chg 31
tag @a[tag=rpg.ashes.source] remove rpg.ashes.source
tag @s add rpg.ashes.source
execute at @s positioned ^ ^1 ^2 run function rpg:item/legacy/ashes_wave
execute at @s positioned ^-1 ^1 ^4 run function rpg:item/legacy/ashes_wave
execute at @s positioned ^1 ^1 ^6 run function rpg:item/legacy/ashes_wave
tag @s remove rpg.ashes.source
playsound minecraft:item.mace.smash_air player @a[distance=..24] ~ ~ ~ 1 0.55
playsound minecraft:block.fire.extinguish player @a[distance=..20] ~ ~ ~ 0.8 0.8
title @s actionbar ["",{"text":"[余烬]","italic":false,"color":"#C66A45","bold":true},{"text":"　三重刀罡穿过灰幕","italic":false,"color":"#D8AAA0"},{"text":" ✦","italic":false,"color":"#FFF0E8"}]""")
    write("item/legacy/ashes_wave.mcfunction", r"""particle minecraft:sweep_attack ~ ~ ~ 0.8 0.6 0.8 0 16 force
particle minecraft:large_smoke ~ ~ ~ 0.8 0.7 0.8 0.08 28 force
particle minecraft:squid_ink ~ ~ ~ 0.5 0.5 0.5 0.06 18 force
particle minecraft:ash ~ ~ ~ 0.8 0.65 0.8 0.05 30 force
particle minecraft:dust_color_transition{from_color:[0.35,0.42,0.12],to_color:[0.08,0.08,0.05],scale:1.7} ~ ~ ~ 0.65 0.55 0.65 0.04 22 force
execute as @e[distance=..1.8,type=!minecraft:player,type=!minecraft:item,type=!minecraft:experience_orb] run effect give @s minecraft:wither 4 1 true
execute as @e[distance=..1.8,type=!minecraft:player,type=!minecraft:item,type=!minecraft:experience_orb] run damage @s 6 minecraft:magic by @a[tag=rpg.ashes.source,limit=1]""")

    write("item/legacy/power_cast.mcfunction", r"""# 朗基努斯 · 王座：只审判最近六秒内被这类圣枪刻过印的目标。
scoreboard players set @s rpg_throne_chg 31
tag @a[tag=rpg.throne.source] remove rpg.throne.source
tag @s add rpg.throne.source
scoreboard players operation #caster rpg_throne_owner = @s rpg_legacy_uid
execute as @e[tag=rpg.throne.mark,distance=..14] if score @s rpg_throne_owner = #caster rpg_throne_owner at @s run function rpg:item/legacy/power_target
particle minecraft:flash{color:16724787} ~ ~1 ~ 0 0 0 0 1
particle minecraft:dust_color_transition{from_color:[0.17,0.17,0.17],to_color:[1.0,0.2,0.0],scale:2} ~ ~1 ~ 1.8 1 1.8 0.05 65 force
playsound minecraft:item.trident.thunder player @a[distance=..28] ~ ~ ~ 0.8 0.8
tag @s remove rpg.throne.source
title @s actionbar ["",{"text":"[王座]","italic":false,"color":"#FF3B1F","bold":true},{"text":"　受印者伏于枪下","italic":false,"color":"#FFB8A8"},{"text":" ✦","italic":false,"color":"#FFF0EC"}]""")
    write("item/legacy/power_target.mcfunction", r"""execute facing entity @a[tag=rpg.throne.source,limit=1] eyes run tp @s ^ ^ ^0.8
effect give @s minecraft:glowing 4 0 true
damage @s 8 minecraft:player_attack by @a[tag=rpg.throne.source,limit=1]
tag @s remove rpg.throne.mark""")

    write("item/sword/legend/blil/trigger.mcfunction", r"""# 贝利尔 · 朝拜：瞬发，但长按不会每刻重复结算。
advancement revoke @s only rpg:item/blil
execute if entity @s[tag=rpg.h.blil_tag1,scores={rpg_blil_cd=..0}] run function rpg:item/legacy/blil_cast""")
    write("item/legacy/blil_cast.mcfunction", r"""scoreboard players set @s rpg_blil_cd 30
tag @a[tag=rpg.blil.source] remove rpg.blil.source
tag @s add rpg.blil.source
particle minecraft:flash{color:6684825} ~ ~1 ~ 0 0 0 0 1
particle minecraft:dust_color_transition{from_color:[0.4,0.0,0.6],to_color:[0.0,0.0,0.0],scale:2.2} ~ ~1 ~ 3.5 0.8 3.5 0.06 100 force
execute as @e[distance=0.1..7,type=!minecraft:player,type=!minecraft:item,type=!minecraft:experience_orb] run effect give @s minecraft:slowness 3 10 true
execute as @e[distance=0.1..7,type=!minecraft:player,type=!minecraft:item,type=!minecraft:experience_orb] run effect give @s minecraft:weakness 3 3 true
execute as @e[distance=0.1..7,type=!minecraft:player,type=!minecraft:item,type=!minecraft:experience_orb] run damage @s 4 minecraft:magic by @a[tag=rpg.blil.source,limit=1]
playsound minecraft:entity.evoker.prepare_summon player @a[distance=..24] ~ ~ ~ 0.9 0.55
tag @s remove rpg.blil.source
title @s actionbar ["",{"text":"[朝拜]","italic":false,"color":"#9B6DE3","bold":true},{"text":"　暗之军团俯首","italic":false,"color":"#D3C0F0"},{"text":" ✦","italic":false,"color":"#F4ECFF"}]""")


def emit_projectile_functions():
    # Existing tick calls these three in order.  Keep exactly one gateway.
    write("item/bow/legend/bubble/bubble.mcfunction",
          "# 三把旧弓的统一投射物入口。\nfunction rpg:item/legacy/projectiles")
    write("item/bow/legend/burn/burn.mcfunction",
          "# 已并入 rpg:item/legacy/projectiles，避免同一箭每刻处理三遍。")
    write("item/bow/legend/hunter/hunter.mcfunction",
          "# 已并入 rpg:item/legacy/projectiles，避免同一箭每刻处理三遍。")

    write("item/legacy/projectiles.mcfunction", r"""# 首次见到箭时，优先读箭保存的发射武器快照；射后立即换手也不会丢技能。
execute as @e[type=#minecraft:arrows,tag=!rpg.legacy.seen,nbt={weapon:{components:{"minecraft:custom_data":{bubble_tag:1b}}}}] run tag @s add rpg.legacy.bubble
execute as @e[type=#minecraft:arrows,tag=!rpg.legacy.seen,nbt={weapon:{components:{"minecraft:custom_data":{burn_tag:1b}}}}] run tag @s add rpg.legacy.burn
execute as @e[type=#minecraft:arrows,tag=!rpg.legacy.seen,nbt={weapon:{components:{"minecraft:custom_data":{hunter_tag:1b}}}}] run tag @s add rpg.legacy.hunter
# 兼容没有 weapon 快照的旧世界箭：从实体自己的 origin 认领，而不是按附近玩家猜。
execute if entity @a[tag=rpg.h.bubble_tag1] as @e[type=#minecraft:arrows,tag=!rpg.legacy.seen,tag=!rpg.legacy.bubble] at @s on origin if entity @s[tag=rpg.h.bubble_tag1] run tag @e[type=#minecraft:arrows,distance=..0.01,limit=1,sort=nearest] add rpg.legacy.bubble
execute if entity @a[tag=rpg.h.burn_tag1] as @e[type=#minecraft:arrows,tag=!rpg.legacy.seen,tag=!rpg.legacy.burn] at @s on origin if entity @s[tag=rpg.h.burn_tag1] run tag @e[type=#minecraft:arrows,distance=..0.01,limit=1,sort=nearest] add rpg.legacy.burn
execute if entity @a[tag=rpg.h.hunter_tag1] as @e[type=#minecraft:arrows,tag=!rpg.legacy.seen,tag=!rpg.legacy.hunter] at @s on origin if entity @s[tag=rpg.h.hunter_tag1] run tag @e[type=#minecraft:arrows,distance=..0.01,limit=1,sort=nearest] add rpg.legacy.hunter
execute if entity @a[tag=rpg.h.hunter_tag1] as @e[type=#minecraft:arrows,tag=rpg.legacy.hunter,tag=!rpg.legacy.taxed] at @s on origin run damage @s 2 minecraft:magic
tag @e[type=#minecraft:arrows,tag=rpg.legacy.hunter] add rpg.legacy.taxed
tag @e[type=#minecraft:arrows,tag=!rpg.legacy.seen] add rpg.legacy.seen

execute as @e[type=#minecraft:arrows,tag=rpg.legacy.bubble] at @s run particle minecraft:dust_color_transition{from_color:[0.0,0.7,1.0],to_color:[0.56,0.97,1.0],scale:1.2} ~ ~ ~ 0.12 0.12 0.12 0.02 5 force
execute as @e[type=#minecraft:arrows,tag=rpg.legacy.burn] at @s run particle minecraft:flame ~ ~ ~ 0.12 0.12 0.12 0.02 5 force
execute as @e[type=#minecraft:arrows,tag=rpg.legacy.hunter] at @s run particle minecraft:dust_color_transition{from_color:[0.69,0.0,0.34],to_color:[0.26,0.64,0.93],scale:1.2} ~ ~ ~ 0.12 0.12 0.12 0.02 5 force

execute as @e[type=#minecraft:arrows,tag=rpg.legacy.bubble] at @s if entity @e[distance=..1.2,type=!minecraft:player,type=!minecraft:item,type=!#minecraft:arrows,limit=1] run function rpg:item/legacy/bubble_hit
execute as @e[type=#minecraft:arrows,tag=rpg.legacy.burn] at @s if entity @e[distance=..1.2,type=!minecraft:player,type=!minecraft:item,type=!#minecraft:arrows,limit=1] run function rpg:item/legacy/burn_hit
execute as @e[type=#minecraft:arrows,tag=rpg.legacy.hunter] at @s if entity @e[distance=..1.5,type=!minecraft:player,type=!minecraft:item,type=!#minecraft:arrows,limit=1] run function rpg:item/legacy/hunter_hit

# 扎进方块而没碰到实体也要收尾，不能让旧技能箭永久留在热路径。
kill @e[type=#minecraft:arrows,tag=rpg.legacy.bubble,nbt={inGround:1b}]
kill @e[type=#minecraft:arrows,tag=rpg.legacy.burn,nbt={inGround:1b}]
kill @e[type=#minecraft:arrows,tag=rpg.legacy.hunter,nbt={inGround:1b}]""")

    write("item/legacy/bubble_hit.mcfunction", r"""tag @e[tag=rpg.legacy.target] remove rpg.legacy.target
tag @e[distance=..1.2,type=!minecraft:player,type=!minecraft:item,type=!#minecraft:arrows,limit=1,sort=nearest] add rpg.legacy.target
execute as @e[tag=rpg.legacy.target,limit=1] run effect give @s minecraft:levitation 2 2 true
execute as @e[tag=rpg.legacy.target,limit=1] run effect give @s minecraft:glowing 2 0 true
particle minecraft:bubble_pop ~ ~ ~ 0.6 0.6 0.6 0.08 28 force
playsound minecraft:entity.generic.splash player @a[distance=..16] ~ ~ ~ 0.7 1.4
tag @e[tag=rpg.legacy.target,limit=1] remove rpg.legacy.target
kill @s""")
    write("item/legacy/burn_hit.mcfunction", r"""tag @e[tag=rpg.legacy.target] remove rpg.legacy.target
tag @e[distance=..1.2,type=!minecraft:player,type=!minecraft:item,type=!#minecraft:arrows,limit=1,sort=nearest] add rpg.legacy.target
execute as @e[tag=rpg.legacy.target,limit=1] run data merge entity @s {Fire:100s}
execute on origin run damage @e[tag=rpg.legacy.target,limit=1] 5 minecraft:on_fire by @s
particle minecraft:flame ~ ~ ~ 0.7 0.7 0.7 0.08 35 force
playsound minecraft:entity.blaze.shoot player @a[distance=..16] ~ ~ ~ 0.8 0.8
tag @e[tag=rpg.legacy.target,limit=1] remove rpg.legacy.target
kill @s""")
    write("item/legacy/hunter_hit.mcfunction", r"""tag @a[tag=rpg.hunter.source] remove rpg.hunter.source
execute on origin run tag @s add rpg.hunter.source
particle minecraft:flash{color:11534423} ~ ~ ~ 0 0 0 0 1
particle minecraft:squid_ink ~ ~ ~ 1 1 1 0.1 45 force
execute as @e[distance=..3.5,type=!minecraft:player,type=!minecraft:item,type=!#minecraft:arrows] run effect give @s minecraft:poison 5 1 true
execute as @e[distance=..3.5,type=!minecraft:player,type=!minecraft:item,type=!#minecraft:arrows] run damage @s 7 minecraft:magic by @a[tag=rpg.hunter.source,limit=1]
playsound minecraft:entity.generic.explode player @a[distance=..20] ~ ~ ~ 0.8 1.35
tag @a[tag=rpg.hunter.source] remove rpg.hunter.source
kill @s""")


def emit_hud():
    hud = read("hud/hud.mcfunction")
    anchor = "execute if entity @s[scores={rpg_hud_t=1..,rpg_hud=5}] run function rpg:hud/s5"
    if anchor not in hud:
        raise AssertionError("HUD skill dispatch anchor not found")
    additions = "\n".join(
        "execute if entity @s[scores={rpg_hud_t=1..,rpg_hud=%d}] run function rpg:hud/s%d" % (n, n)
        for n in range(6, 10))
    if "function rpg:hud/s6" not in hud:
        hud = hud.replace(anchor, anchor + "\n" + additions, 1)
    write("hud/hud.mcfunction", hud)

    specs = {
        6: ("漆黑之刃", "dark_purple", "light_purple"),
        7: ("狂　风", "green", "yellow"),
        8: ("余　烬", "dark_gray", "red"),
        9: ("王　座", "#ff3300", "white"),
    }
    for slot, (name, dark, bright) in specs.items():
        lines = ["# %s 的统一十格蓄力条。" % name]
        for i in range(11):
            full = "▰" * i
            empty = "▱" * (10 - i)
            comps = '["",{"text":"%s ","italic":false,"color":"%s"}' % (name, dark)
            if full:
                comps += ',{"text":"%s","italic":false,"color":"%s"}' % (full, bright)
            if empty:
                comps += ',{"text":"%s","italic":false,"color":"dark_gray"}' % empty
            comps += ',{"text":"  %d%%","italic":false,"color":"gray"}]' % (i * 10)
            lines.append("execute if entity @s[scores={rpg_hud_p=%d}] run title @s actionbar %s" % (i, comps))
        write("hud/s%d.mcfunction" % slot, "\n".join(lines))


def remove_retired_functions():
    """Delete dead pre-modernisation copies so audits cannot mistake them for live code."""
    retired = [
        # Old bow roots now have one gateway; these helpers carried public
        # bubble/burn/hunter tags without projectile ownership.
        "item/bow/legend/bubble/bubble/g0.mcfunction",
        "item/bow/legend/burn/burn/g0.mcfunction",
        "item/bow/legend/burn/burn/g1.mcfunction",
        "item/bow/legend/hunter/hunter/g0.mcfunction",
        # Stand-alone copies were never tick roots; legend1 duplicated them.
        "item/sword/legend/chainsaw/chainsaw.mcfunction",
        "item/sword/legend/montain/montain.mcfunction",
        "item/sword/legend/pen/pen.mcfunction",
        "item/sword/legend/potion/potion.mcfunction",
        "item/sword/legend/soul/soul.mcfunction",
        "item/sword/legend/ashes/ashes.mcfunction",
        "item/sword/legend/blil/blil.mcfunction",
        "item/sword/legend/typhoon/typhoon.mcfunction",
        "item/sword/legend/power/power.mcfunction",
    ]
    # opt_guard/opt_invert derive these from the removed legend1 sections.
    for n in (2, 3, 4, 5, 6, 10, 11, 13):
        retired.append("item/sword/legend/legend1/g%d.mcfunction" % n)
        retired.append("item/sword/legend/legend1/g%d_body.mcfunction" % n)
    for rel in retired:
        remove(rel)


def verify():
    root = read("item/sword/legend/legend1.mcfunction")
    for forbidden in (
            "scoreboard players reset * chainsaw",
            "scoreboard players reset * montain",
            "scoreboard players reset * pen",
            "scoreboard players reset * potion"):
        if forbidden in root:
            raise AssertionError("global legacy reset survived: " + forbidden)

    combined = "\n".join(read("item/legacy/" + f) for f in (
        "weapons.mcfunction", "hit.mcfunction", "chainsaw.mcfunction",
        "mountain.mcfunction", "pen.mcfunction", "pen_black.mcfunction",
        "pen_white.mcfunction", "venom.mcfunction", "venom_burst.mcfunction",
        "ashes_hit.mcfunction"))
    if "@p[" in combined or "scoreboard players reset *" in combined:
        raise AssertionError("new legacy architecture contains a global owner guess/reset")
    if "on attacker" not in combined or "rpg.legacy.target" not in combined:
        raise AssertionError("new legacy architecture lost exact hit ownership")
    if ("rpg.h.ashes_tag1" not in read("item/legacy/weapons.mcfunction") or
            "function rpg:item/legacy/ashes_hit" not in read("item/legacy/hit.mcfunction")):
        raise AssertionError("Beelzebub passive attack effects are unreachable")

    # Reachable B/C roots must not retain their old global entity names,
    # shared stat resets, or public projectile tags.  Do not reject every
    # ``@p`` here: the still-unmigrated epic/advanced section in legend1 owns
    # one until modernize_legacy_advanced.py runs immediately after this pass.
    # The advanced pass performs the final whole-scope owner audit.
    reachable = [
        "item/sword/legend/legend1.mcfunction",
        "item/sword/legend/night/night.mcfunction",
        "item/sword/legend/typhoon/trigger.mcfunction",
        "item/sword/legend/ashes/trigger.mcfunction",
        "item/sword/legend/power/trigger.mcfunction",
        "item/sword/legend/blil/trigger.mcfunction",
        "item/bow/legend/bubble/bubble.mcfunction",
        "item/bow/legend/burn/burn.mcfunction",
        "item/bow/legend/hunter/hunter.mcfunction",
    ]
    reachable_text = combined + "\n" + "\n".join(read(f) for f in reachable)
    for bad in ("name=ashes_", "name=typhoon_atk", "name=power_atk",
                "scoreboard players reset * ashes",
                "scoreboard players reset * blil",
                "scoreboard players reset * soul",
                "scoreboard players reset * typhoon",
                "scoreboard players reset * power"):
        if bad in reachable_text:
            raise AssertionError("reachable legacy owner hazard survived: " + bad)
    ownership_text = (read("item/legacy/throne_mark.mcfunction") + "\n"
                      + read("item/legacy/power_cast.mcfunction") + "\n"
                      + read("item/legacy/power_target.mcfunction") + "\n"
                      + read("item/legacy/projectiles.mcfunction"))
    if ("rpg_throne_owner" not in ownership_text or
            "on origin" not in ownership_text or
            "weapon:{components" not in ownership_text or
            "execute facing entity @a[tag=rpg.throne.source,limit=1]" not in ownership_text):
        raise AssertionError("persistent target/projectile ownership is not explicit")

    # Every synchronous temporary selector clears stale world state before it
    # publishes the current executor.  This also makes interrupted old saves
    # deterministic on their first modern tick.
    temp_pairs = (
        ("item/legacy/hit.mcfunction", "rpg.legacy.target", "tag @s add"),
        ("item/legacy/bubble_hit.mcfunction", "rpg.legacy.target", "tag @e[distance="),
        ("item/legacy/burn_hit.mcfunction", "rpg.legacy.target", "tag @e[distance="),
        ("item/legacy/night_cast.mcfunction", "rpg.night.source", "tag @s add"),
        ("item/legacy/typhoon_cast.mcfunction", "rpg.wind.source", "tag @s add"),
        ("item/legacy/ashes_cast.mcfunction", "rpg.ashes.source", "tag @s add"),
        ("item/legacy/power_cast.mcfunction", "rpg.throne.source", "tag @s add"),
        ("item/legacy/blil_cast.mcfunction", "rpg.blil.source", "tag @s add"),
        ("item/legacy/hunter_hit.mcfunction", "rpg.hunter.source", "execute on origin"),
    )
    for rel, tag, publish in temp_pairs:
        body = read(rel)
        clear = "tag @e[tag=%s] remove" % tag if tag == "rpg.legacy.target" else \
                "tag @a[tag=%s] remove" % tag
        if clear not in body or body.index(clear) > body.index(publish):
            raise AssertionError("temporary ownership is not stale-safe: " + rel)


def main():
    patch_lore()
    patch_scoreboards()
    patch_legacy_root()
    emit_functions()
    remove_retired_functions()
    verify()
    print("legacy weapons: 14/17 old cards modernised (A/B/C batches; D/E separate)")


if __name__ == "__main__":
    main()
