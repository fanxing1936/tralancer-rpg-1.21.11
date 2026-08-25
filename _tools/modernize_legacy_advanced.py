# -*- coding: utf-8 -*-
"""Modernise the advanced half of the pre-upgrade weapon set.

This generator deliberately runs after modernize_legacy_weapons.py.  It owns
only the old socket runes plus saber / wukong / doctrine-axe hit bodies, so the
two migrations can evolve independently.
"""

from pathlib import Path
import sys

from modernize_legacy_weapons import LEGACY_LORE


DP = Path(sys.argv[1] if len(sys.argv) > 1 else "../rpg")
FUNC = DP / "data/rpg/function"


RUNE_LORE = {
    "sweep": "长按蓄力2.5秒，释放12格钢刃剑气",
    "wind": "长按蓄力2.5秒，消耗1级经验释放风弹",
    "flame": "长按蓄力2.5秒，消耗1级经验释放烈焰",
}

EPIC_LORE = {
    "攻击时附带灼烧且自身抗火": "命中后自身抗火2秒",
    "攻击时附带极寒效果": "命中减速并追加冻伤",
    "右键召唤涡流突刺对手": "长按蓄力0.5秒，向前贯出10格潮锋",
    "攻击附带发光效果": "命中使敌人凋零并显形2秒",
    "造成伤害后获得1s抗性": "命中后自身获得抗性2秒",
    "右键击飞5m内的敌人": "长按蓄力2.25秒，冻结5格敌人",
}


def replace_lore_texts(file: Path, changes: dict[str, str]) -> None:
    """Replace only exact text values, leaving the surrounding card JSON/SNBT."""
    src = file.read_text(encoding="utf-8")
    for old, new in changes.items():
        if old in src:
            assert src.count(old) == 1, "ambiguous lore source in %s: %s" % (file, old)
            src = src.replace(old, new, 1)
        else:
            assert new in src, "lore source missing in %s: %s" % (file, old)
    file.write_text(src, encoding="utf-8", newline="\n")


def patch_advanced_lore() -> None:
    """Align the second-circle cards with the generated advanced mechanics."""
    give_item = FUNC / "command/give/item.mcfunction"
    replace_lore_texts(give_item, {
        "长按/右键蓄力释放剑气": RUNE_LORE["sweep"],
        "长按/右键消耗一级经验释放风弹": RUNE_LORE["wind"],
        "长按/右键消耗一级经验释放烈焰弹": RUNE_LORE["flame"],
    })
    modifier_old = {
        "flame": "右键/长按消耗一级经验释放火焰弹",
        "sweep": "右键/长按释放剑气",
        "wind": "右键/长按消耗一级经验释放风弹",
    }
    for kind, old in modifier_old.items():
        replace_lore_texts(
            DP / "data/rpg/item_modifier/item/sword/main" / (kind + ".json"),
            {old: RUNE_LORE[kind]})

    replace_lore_texts(DP / "data/rpg/loot_table/trial/epic_sword.json",
                       EPIC_LORE)

    # The generated doctrine axe previously had no skill section at all.
    weapon = FUNC / "command/give/weapon.mcfunction"
    src = weapon.read_text(encoding="utf-8")
    if "纹饰决定命中效果：钻石缓速、黄金火伤" not in src:
        lines = src.splitlines()
        indices = [i for i, line in enumerate(lines)
                   if "教条战斧" in line and "custom_data={sword_tag:1b,axe_tag:1b" in line]
        assert len(indices) == 1, "doctrine axe card is not unique"
        i = indices[0]
        closing = ('["",{"text":"+------------------+","italic":false,'
                   '"color":"white"}]],enchantments')
        detail = (
            '["",{"text":"+------------------+","italic":false,"color":"white"}],'
            '["",{"text":"🪓纹饰技能","italic":false,"color":"white"},'
            '{"text":"[教条]","italic":false,"color":"aqua","bold":true}],'
            '["",{"text":"纹饰决定命中效果：钻石缓速、黄金火伤",'
            '"italic":false,"color":"white"}],'
            '["",{"text":"石英凋零、合金致盲、铜虚弱、青金显形、紫晶浮空",'
            '"italic":false,"color":"white"}],'
            '["",{"text":"铁增抗、红石疗愈、绿宝石加速",'
            '"italic":false,"color":"white"}],'
            '["",{"text":"+------------------+","italic":false,'
            '"color":"white"}]],enchantments')
        assert closing in lines[i], "doctrine axe lore insertion point missing"
        lines[i] = lines[i].replace(closing, detail, 1)
        src = "\n".join(lines) + ("\n" if src.endswith("\n") else "")
        weapon.write_text(src, encoding="utf-8", newline="\n")


def verify_joint_lore() -> None:
    weapon = (FUNC / "command/give/weapon.mcfunction").read_text(encoding="utf-8")
    assert len(LEGACY_LORE) == 17, "joint original-card matrix is not 17/17"
    for text in LEGACY_LORE.values():
        assert weapon.count(text) == 1, "original-card lore missing/not unique: " + text
    for text in RUNE_LORE.values():
        assert text in (FUNC / "command/give/item.mcfunction").read_text(encoding="utf-8")
    for text in EPIC_LORE.values():
        assert text in (DP / "data/rpg/loot_table/trial/epic_sword.json").read_text(encoding="utf-8")
    assert "纹饰决定命中效果：钻石缓速、黄金火伤" in weapon


def wf(rel: str, body: str) -> None:
    path = FUNC / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.rstrip() + "\n", encoding="utf-8", newline="\n")


def add_once(rel: str, marker: str, text: str) -> None:
    path = FUNC / rel
    src = path.read_text(encoding="utf-8")
    if marker not in src:
        path.write_text(src.rstrip() + "\n" + text.rstrip() + "\n",
                        encoding="utf-8", newline="\n")


def make_bar(slot: int, label: str, dark: str, bright: str) -> None:
    lines = ["# 旧镶嵌蓄力条；由统一 HUD 渲染，不直接争抢 actionbar。"]
    for n in range(11):
        full = "▰" * n
        empty = "▱" * (10 - n)
        comp = [
            "", {"text": label + " ", "italic": False, "color": dark},
            {"text": full, "italic": False, "color": bright},
            {"text": empty, "italic": False, "color": "dark_gray"},
            {"text": "  %d%%" % (n * 10), "italic": False, "color": "gray"},
        ]
        import json
        lines.append(
            "execute if entity @s[scores={rpg_hud_p=%d}] run title @s actionbar %s"
            % (n, json.dumps(comp, ensure_ascii=False, separators=(",", ":")))
        )
    wf("hud/s%d.mcfunction" % slot, "\n".join(lines))


def rune_charge(kind: str, slot: int) -> None:
    # Advancement callbacks are generic consumable callbacks.  The custom-data
    # check is therefore authoritative and prevents one old rune charging all
    # three meters at once.
    wf("item/sword/main/%s/%s.mcfunction" % (kind, kind), f"""
advancement revoke @s only rpg:item/{'wind_charge' if kind == 'wind' else kind}
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{{{kind}_tag:1b}}] run scoreboard players reset @s {kind}
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{{{kind}_tag:1b}}] run return 0
scoreboard players add @s {kind} 1
execute if score @s {kind} matches 51.. run scoreboard players set @s {kind} 50
scoreboard players set @s rpg_hud {slot}
scoreboard players operation @s rpg_hud_p = @s {kind}
scoreboard players operation @s rpg_hud_p /= #rune5 rpg_hud_p
scoreboard players set @s rpg_hud_t 3
execute at @s anchored eyes run particle enchant ^ ^ ^0.4 0.25 0.25 0.25 0.2 4 force @s
""")

    xp_gate = "" if kind == "sweep" else ",level=1.."
    fail = "" if kind == "sweep" else (
        f"execute as @a[scores={{{kind}=50..}},level=..0] "
        f"if items entity @s weapon.mainhand *[minecraft:custom_data~{{{kind}_tag:1b}}] "
        f"run function rpg:item/legacy_advanced/rune/{kind}_empty\n"
    )
    wf("item/sword/main/%s/%s_trigger.mcfunction" % (kind, kind), f"""
# 每位玩家只读自己的蓄力、经验和主手；不再生成靠 @p 猜主人的盔甲架。
execute as @a[scores={{{kind}=50..}}{xp_gate}] if items entity @s weapon.mainhand *[minecraft:custom_data~{{{kind}_tag:1b}}] run function rpg:item/legacy_advanced/rune/{kind}_release
{fail}""")


def rune_ray(kind: str, damage: int, particle: str, damage_type: str,
             extra: str = "") -> None:
    target = "@e[distance=..0.75,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:marker,type=!minecraft:armor_stand,limit=1,sort=nearest]"
    for step in range(1, 13):
        lines = [
            "particle %s ~ ~ ~ 0.12 0.12 0.12 0.02 3 force" % particle,
            "execute if entity %s run damage %s %d minecraft:%s by @s"
            % (target, target, damage, damage_type),
        ]
        if extra:
            lines.append("execute if entity %s run %s" % (target, extra.replace("$target", target)))
        if step < 12:
            lines.append(
                "execute unless entity %s if block ~ ~ ~ minecraft:air positioned ^ ^ ^1 run function rpg:item/legacy_advanced/rune/%s_ray_%d"
                % (target, kind, step + 1)
            )
        wf("item/legacy_advanced/rune/%s_ray_%d.mcfunction" % (kind, step), "\n".join(lines))


def rune_release(kind: str, sound: str, name: str, detail: str,
                 accent: str, soft: str, glint: str) -> None:
    xp = "" if kind == "sweep" else "xp add @s -1 levels\n"
    wf("item/legacy_advanced/rune/%s_release.mcfunction" % kind, f"""
# 即时射线始终保留 @s=施术玩家，伤害来源明确为 by @s。
scoreboard players set @s {kind} 0
{xp}playsound minecraft:{sound} player @s ~ ~ ~ 1 1
execute anchored eyes positioned ^ ^ ^1 run function rpg:item/legacy_advanced/rune/{kind}_ray_1
title @s actionbar ["",{{"text":"[{name}]","italic":false,"color":"{accent}","bold":true}},{{"text":"　{detail}","italic":false,"color":"{soft}"}},{{"text":" ✦","italic":false,"color":"{glint}"}}]
""")
    if kind != "sweep":
        wf("item/legacy_advanced/rune/%s_empty.mcfunction" % kind, f"""
scoreboard players set @s {kind} 0
title @s actionbar ["",{{"text":"法力枯竭","italic":true,"color":"gray"}},{{"text":" · 需要 1 级经验","italic":false,"color":"dark_gray"}}]
""")


def advanced_hits() -> None:
    # These bodies are called with @s = the hurt entity.  `on attacker` changes
    # executor but intentionally retains the victim position.
    wf("item/legacy_advanced/hit/saber_victim.mcfunction", """
# 无垠星空：受击者 -> 本次攻击者。随机数和全部增益都属于该攻击者。
tag @e[tag=rpg.legacy.advanced_target] remove rpg.legacy.advanced_target
tag @s add rpg.legacy.advanced_target
execute at @s on attacker if entity @s[scores={saber=0..},tag=rpg.h.saber_tag1] run function rpg:item/legacy_advanced/hit/saber
tag @s remove rpg.legacy.advanced_target
""")
    wf("item/legacy_advanced/hit/saber.mcfunction", """
execute store result score @s random run random value 1..10
execute if score @s random matches 1 run effect give @e[tag=rpg.legacy.advanced_target,limit=1] wither 10 4 true
execute if score @s random matches 1 run function rpg:effect/pseudo_explosion/owned_p2
execute if score @s random matches 1 run particle dust_color_transition{from_color:[1.0,0.36,0.83],to_color:[1.0,1.0,1.0],scale:1} ~ ~1 ~ 0.8 0.8 0.8 0.2 24
execute if score @s random matches 2 run effect give @e[tag=rpg.legacy.advanced_target,limit=1] wither 6 2 true
execute if score @s random matches 2 run particle soul_fire_flame ~ ~1 ~ 0.8 0.8 0.8 0.15 40
execute if score @s random matches 3 run effect give @e[tag=rpg.legacy.advanced_target,limit=1] slowness 4 4 true
execute if score @s random matches 3 run particle wax_off ~ ~1 ~ 0.8 0.8 0.8 0.2 36
execute if score @s random matches 4 at @e[tag=rpg.legacy.advanced_target,limit=1] run summon lightning_bolt
execute if score @s random matches 4 run particle soul ~ ~1 ~ 0.8 0.8 0.8 0.15 36
effect give @e[tag=rpg.legacy.advanced_target,limit=1] weakness 4 2 true
particle dust_color_transition{from_color:[1.0,0.36,0.83],to_color:[0.0,0.98,1.0],scale:2} ~ ~1 ~ 0.7 0.7 0.7 0.15 16
scoreboard players reset @s random
scoreboard players reset @s saber
""")

    wf("item/legacy_advanced/hit/wukong_victim.mcfunction", """
# 如意金箍棒：每个攻击者独立掷签，不读取或清空别人的 random。
tag @e[tag=rpg.legacy.advanced_target] remove rpg.legacy.advanced_target
tag @s add rpg.legacy.advanced_target
execute at @s on attacker if entity @s[scores={wukong=0..},tag=rpg.h.wukong_tag1] run function rpg:item/legacy_advanced/hit/wukong
tag @s remove rpg.legacy.advanced_target
""")
    wf("item/legacy_advanced/hit/wukong.mcfunction", """
execute store result score @s random run random value 1..5
execute if score @s random matches 1 run effect give @e[tag=rpg.legacy.advanced_target,limit=1] wither 5 3 true
execute if score @s random matches 1 run function rpg:effect/pseudo_explosion/owned_p3
execute if score @s random matches 1 run effect give @s resistance 2 3 true
execute if score @s random matches 1 run particle gust_emitter_small ~ ~1 ~ 0.6 0.6 0.6 0.1 8
execute if score @s random matches 2 run effect give @s instant_health 1 1 true
execute if score @s random matches 2 run particle totem_of_undying ~ ~1 ~ 0.8 0.8 0.8 0.2 28
execute if score @s random matches 3 run effect give @e[tag=rpg.legacy.advanced_target,limit=1] slowness 3 4 true
execute if score @s random matches 3 run particle enchant ~ ~1 ~ 0.8 0.8 0.8 0.2 28
effect give @e[tag=rpg.legacy.advanced_target,limit=1] wind_charged 6 2 true
particle dust_color_transition{from_color:[1.0,0.35,0.0],to_color:[1.0,1.0,1.0],scale:3} ~ ~1 ~ 0.8 0.8 0.8 0.15 20
damage @e[tag=rpg.legacy.advanced_target,limit=1] 4 minecraft:player_attack by @s
scoreboard players reset @s random
scoreboard players reset @s wukong
""")

    # 樱怒之日／漆黑之日 shared the same globally advanced sakura_step and
    # ownerless arrow rain.  Advance the combo only on this attacker's hits and
    # resolve the fourth cut immediately at the victim instead.
    wf("item/legacy_advanced/hit/sakura_victim.mcfunction", """
tag @e[tag=rpg.legacy.advanced_target] remove rpg.legacy.advanced_target
tag @s add rpg.legacy.advanced_target
execute at @s on attacker if entity @s[scores={sakura=0..},tag=rpg.h.sakura_tag1] run function rpg:item/legacy_advanced/hit/sakura
execute at @s on attacker if entity @s[scores={sakura=0..},tag=rpg.h.night_tag1] run function rpg:item/legacy_advanced/hit/night
tag @s remove rpg.legacy.advanced_target
""")
    tgt = "@e[tag=rpg.legacy.advanced_target,limit=1]"
    wf("item/legacy_advanced/hit/sakura.mcfunction", f"""
scoreboard players add @s sakura_step 1
execute if score @s sakura_step matches 5.. run scoreboard players set @s sakura_step 1
execute if score @s sakura_step matches 1 run particle sweep_attack ~ ~1 ~ 0.6 0.6 0.6 0.1 14
execute if score @s sakura_step matches 2 run particle dust_pillar{{block_state:{{Name:cherry_leaves}}}} ~ ~1 ~ 0.7 0.7 0.7 0.12 24
execute if score @s sakura_step matches 2 run effect give {tgt} wind_charged 3 1 true
execute if score @s sakura_step matches 3 run particle cherry_leaves ~ ~1.3 ~ 0.8 0.8 0.8 0.15 28
execute if score @s sakura_step matches 3 run effect give @s instant_health 1 0 true
execute if score @s sakura_step matches 4 run particle dust_color_transition{{from_color:[1.0,0.47,0.47],to_color:[1.0,1.0,1.0],scale:3}} ~ ~1 ~ 0.9 0.9 0.9 0.15 40
execute if score @s sakura_step matches 4 run damage {tgt} 8 minecraft:player_attack by @s
execute if score @s sakura_step matches 4 at {tgt} run summon lightning_bolt
execute if score @s sakura_step matches 4 run effect give @s resistance 1 3 true
execute if score @s sakura_step matches 4 run title @s actionbar ["",{{"text":"[樱怒]","italic":false,"color":"#FF6F91","bold":true}},{{"text":"　四景尽斩","italic":false,"color":"#FFD1DC"}},{{"text":" ✦","italic":false,"color":"#FFF0F5"}}]
particle cherry_leaves ~ ~1.2 ~ 0.45 0.7 0.45 0.08 7
damage {tgt} 2 minecraft:player_attack by @s
scoreboard players reset @s sakura
""")
    wf("item/legacy_advanced/hit/night.mcfunction", f"""
scoreboard players add @s sakura_step 1
execute if score @s sakura_step matches 5.. run scoreboard players set @s sakura_step 1
execute if score @s sakura_step matches 1 run effect give {tgt} levitation 1 1 true
execute if score @s sakura_step matches 2 run effect give {tgt} slowness 3 3 true
execute if score @s sakura_step matches 3 run effect give @s instant_health 1 1 true
execute if score @s sakura_step matches 4 run damage {tgt} 9 minecraft:magic by @s
execute if score @s sakura_step matches 4 run effect give {tgt} darkness 3 0 true
execute if score @s sakura_step matches 4 run title @s actionbar ["",{{"text":"[漆黑]","italic":false,"color":"#8155D9","bold":true}},{{"text":"　夜幕合拢","italic":false,"color":"#C5B1EB"}},{{"text":" ✦","italic":false,"color":"#F1EAFF"}}]
particle dust_color_transition{{from_color:[0.4,0.0,1.0],to_color:[0.0,0.0,0.0],scale:2}} ~ ~1 ~ 0.7 0.7 0.7 0.12 18
execute if entity @s[tag=rpg.e.offhand_sakura_tag1] run particle sweep_attack ~ ~1 ~ 0.5 0.5 0.5 0.1 8
scoreboard players reset @s sakura
""")
    wf("item/legacy_advanced/sakura_cleanup.mcfunction", """
# 兼容清理旧版已生成、没有主人可追溯的樱花箭；新版不再生成它们。
execute as @e[type=minecraft:spectral_arrow,tag=sakura_tag] at @s run particle dust_color_transition{from_color:[0.4,0.0,1.0],to_color:[0.0,0.0,0.0],scale:1} ~ ~ ~ 0.3 0.3 0.3 0.1 8
kill @e[type=minecraft:spectral_arrow,tag=sakura_tag]
""")

    wf("item/legacy_advanced/hit/axe_victim.mcfunction", """
# 教条战斧：纹饰由攻击者主手判定，效果只落在本次受击者或攻击者本人。
tag @e[tag=rpg.legacy.advanced_target] remove rpg.legacy.advanced_target
tag @s add rpg.legacy.advanced_target
execute at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] run function rpg:item/legacy_advanced/hit/axe
tag @s remove rpg.legacy.advanced_target
""")
    tgt = "@e[tag=rpg.legacy.advanced_target,limit=1]"
    cond = 'if items entity @s weapon.mainhand *[minecraft:trim~{material:"minecraft:%s"}]'
    lines = [
        f'execute {cond % "diamond"} run particle trial_spawner_detection_ominous ~ ~1 ~ 0.4 0.4 0.4 0.05 12',
        f'execute {cond % "diamond"} run effect give {tgt} slowness 2 2 true',
        f'execute {cond % "iron"} run particle dust_pillar{{block_state:{{Name:iron_block}}}} ~ ~1 ~ 0.5 0.5 0.5 0.1 18',
        f'execute {cond % "iron"} run effect give @s resistance 2 0 true',
        f'execute {cond % "gold"} run particle dust_color_transition{{from_color:[1.0,0.84,0.0],to_color:[1.0,0.64,0.0],scale:3}} ~ ~1 ~ 0.5 0.5 0.5 0.1 14',
        f'execute {cond % "gold"} run damage {tgt} 3 minecraft:in_fire by @s',
        f'execute {cond % "quartz"} run particle sweep_attack ~ ~1 ~ 0.4 0.4 0.4 0.1 10',
        f'execute {cond % "quartz"} run effect give {tgt} wither 2 1 true',
        f'execute {cond % "netherite"} run particle squid_ink ~ ~1 ~ 0.4 0.4 0.4 0.15 12',
        f'execute {cond % "netherite"} run effect give {tgt} darkness 3 0 true',
        f'execute {cond % "redstone"} run particle dust_pillar{{block_state:{{Name:redstone_block}}}} ~ ~1 ~ 0.5 0.5 0.5 0.1 14',
        f'execute {cond % "redstone"} run effect give @s instant_health 1 0 true',
        f'execute {cond % "copper"} run particle dust_color_transition{{from_color:[0.9,0.47,0.32],to_color:[0.31,0.72,0.59],scale:3}} ~ ~1 ~ 0.4 0.4 0.4 0.05 12',
        f'execute {cond % "copper"} run effect give {tgt} weakness 2 2 true',
        f'execute {cond % "emerald"} run particle dust_color_transition{{from_color:[0.09,0.85,0.38],to_color:[0.0,0.48,0.09],scale:3}} ~ ~1 ~ 0.4 0.4 0.4 0.05 12',
        f'execute {cond % "emerald"} run effect give @s speed 2 1 true',
        f'execute {cond % "lapis"} run particle ominous_spawning ~ ~1 ~ 0.4 0.4 0.4 0.05 10',
        f'execute {cond % "lapis"} run effect give {tgt} glowing 3 0 true',
        f'execute {cond % "amethyst"} run particle dust_color_transition{{from_color:[0.55,0.41,0.79],to_color:[0.33,0.22,0.53],scale:3}} ~ ~1 ~ 0.4 0.4 0.4 0.05 12',
        f'execute {cond % "amethyst"} run effect give {tgt} levitation 1 1 true',
    ]
    lines.append("scoreboard players reset @s axe")
    wf("item/legacy_advanced/hit/axe.mcfunction", "\n".join(lines))


def remove_retired_advanced_copies() -> None:
    """Remove old stand-alone duplicates after their reachable roots migrate."""
    retired = (
        "item/sword/legend/legend.mcfunction",
        "item/sword/legend/saber/saber.mcfunction",
        "item/sword/legend/saber/flame.mcfunction",
        "item/sword/legend/saber/particle.mcfunction",
        "item/sword/legend/saber/spark.mcfunction",
        "item/sword/legend/saber/sweep.mcfunction",
        "item/sword/legend/sakura/sakura.mcfunction",
        "item/sword/legend/wukong/wukong.mcfunction",
        "item/sword/legend/wukong/particle.mcfunction",
    )
    for rel in retired:
        file = FUNC / rel
        if file.is_file():
            file.unlink()


def patch_advanced_roots() -> None:
    """Replace pristine inline blocks, not children from an earlier build.

    The clean build runs this pass before opt_guard/opt_invert.  Writing old
    g7/g12/g16 child names therefore does not connect anything: those children
    only existed in an already-optimised working tree.  Patch the authoritative
    marker blocks first; later optimisers may split these small semantic calls
    without resurrecting the retired implementation.
    """
    legend = FUNC / "item/sword/legend/legend1.mcfunction"
    src = legend.read_text(encoding="utf-8")

    def replace_between(text: str, start: str, end: str, body: str) -> str:
        begin = text.index(start)
        finish = text.index(end, begin)
        return text[:begin] + body.rstrip() + "\n\n" + text[finish:]

    saber_marker = "##无垠星空／樱怒之日／漆黑之日（现代命中入口）"
    if saber_marker not in src:
        src = replace_between(src, "##无垠星空", "##亚巴顿", """
##无垠星空／樱怒之日／漆黑之日（现代命中入口）
execute as @e[tag=rpg.hurt] at @s run function rpg:item/legacy_advanced/hit/saber_victim
execute as @e[tag=rpg.hurt] at @s run function rpg:item/legacy_advanced/hit/sakura_victim
# 兼容清理旧存档中没有可追溯主人的樱花箭；新版不再生成它们。
execute if entity @e[type=minecraft:spectral_arrow,tag=sakura_tag] run function rpg:item/legacy_advanced/sakura_cleanup
""")
    wukong_marker = "##如意金箍棒（现代命中入口）"
    if wukong_marker not in src:
        src = replace_between(src, "##悟空", "##朗基努斯", """
##如意金箍棒（现代命中入口）
execute as @e[tag=rpg.hurt] at @s run function rpg:item/legacy_advanced/hit/wukong_victim
""")

    axe_marker = "##教条战斧（现代命中入口）"
    if axe_marker not in src:
        axe = src.index("##铁斧不同攻击效果")
        src = src[:axe] + """##教条战斧（现代命中入口）
execute as @e[tag=rpg.hurt] at @s run function rpg:item/legacy_advanced/hit/axe_victim
"""
    legend.write_text(src.rstrip("\n") + "\n", encoding="utf-8", newline="\n")


def epic_six() -> None:
    """Modernise the shared skills of the six epic_sword loot entries.

    Their random attributes, enchantments, names and lore remain in the loot
    table.  Only the common runtime is replaced here.
    """
    legend = FUNC / "item/sword/legend/legend1.mcfunction"
    src = legend.read_text(encoding="utf-8")
    if "##史诗武器（六件随机属性精英武器的共同运行时）" in src:
        return
    start = src.index("##史诗武器")
    end = src.index("##铁斧不同攻击效果", start)
    shared = """##史诗武器（六件随机属性精英武器的共同运行时）
# 属性随机仍由 rpg:trial/epic_sword 保留；这里只处理技能归属。
execute as @e[tag=rpg.hurt] at @s run function rpg:item/legacy_advanced/hit/epic_victim
function rpg:item/legacy_advanced/epic/tick

"""
    legend.write_text(src[:start] + shared + src[end:],
                      encoding="utf-8", newline="\n")

    # The active tick used to be duplicated in this standalone legacy file.
    # Keep a harmless compatibility entry for worlds/functions that call it.
    wf("item/sword/legend/epic/epic.mcfunction", """
# 兼容入口；权威实现与 tick 中的共同入口一致。
function rpg:item/legacy_advanced/epic/tick
""")

    wf("item/legacy_advanced/hit/epic_victim.mcfunction", """
# @s 是本次受击实体；四条入口都通过 on attacker 取得唯一技能持有者。
tag @e[tag=rpg.legacy.advanced_target] remove rpg.legacy.advanced_target
tag @s add rpg.legacy.advanced_target
execute at @s on attacker if entity @s[scores={sun=0..},tag=rpg.h.sun_tag1] run function rpg:item/legacy_advanced/hit/epic_sun
execute at @s on attacker if entity @s[scores={ice=0..},tag=rpg.h.ice_tag1] run function rpg:item/legacy_advanced/hit/epic_ice
execute at @s on attacker if entity @s[scores={steel=0..},tag=rpg.h.steel_tag1] run function rpg:item/legacy_advanced/hit/epic_steel
execute at @s on attacker if entity @s[scores={sea=0..},tag=rpg.h.sea_tag1] run function rpg:item/legacy_advanced/hit/epic_sea
tag @s remove rpg.legacy.advanced_target
""")
    tgt = "@e[tag=rpg.legacy.advanced_target,limit=1]"
    wf("item/legacy_advanced/hit/epic_sun.mcfunction", f"""
# 血煞弯刀：余烬护住挥刀者。
effect give @s fire_resistance 2 1 true
particle dust_color_transition{{from_color:[1.0,0.84,0.0],to_color:[1.0,0.2,0.0],scale:3}} ~ ~1 ~ 0.6 0.6 0.6 0.08 18
scoreboard players reset @s sun
""")
    wf("item/legacy_advanced/hit/epic_ice.mcfunction", f"""
# 严寒风暴／极寒之镰：寒意只落到本次受击者。
effect give {tgt} slowness 2 4 true
damage {tgt} 2 minecraft:freeze by @s
particle dust_color_transition{{from_color:[0.58,0.92,1.0],to_color:[1.0,1.0,1.0],scale:3}} ~ ~1 ~ 0.6 0.6 0.6 0.08 18
scoreboard players reset @s ice
""")
    wf("item/legacy_advanced/hit/epic_steel.mcfunction", """
# 三叉钢刀：钢躯反馈属于攻击者，不再被全局清分。
effect give @s resistance 2 0 true
particle dust_pillar{block_state:{Name:iron_block}} ~ ~1 ~ 0.6 0.6 0.6 0.08 18
scoreboard players reset @s steel
""")
    wf("item/legacy_advanced/hit/epic_sea.mcfunction", f"""
# 两把珊瑚斧共用潮蚀被动，目标固定为本次受击者。
effect give {tgt} wither 2 2 true
effect give {tgt} glowing 2 0 true
particle dust_color_transition{{from_color:[1.0,0.38,0.92],to_color:[1.0,0.78,0.0],scale:3}} ~ ~1 ~ 0.6 0.6 0.6 0.08 18
scoreboard players reset @s sea
""")

    # The two using_item callbacks now validate the actual custom-data tag.
    wf("item/sword/legend/epic/ice_trigger.mcfunction", """
advancement revoke @s only rpg:item/ice
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{ice_tag:1b}] run scoreboard players reset @s ice_step
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{ice_tag:1b}] run return 0
scoreboard players add @s ice_step 1
execute if score @s ice_step matches 46.. run scoreboard players set @s ice_step 45
scoreboard players set @s rpg_hud 13
scoreboard players operation @s rpg_hud_p = @s ice_step
scoreboard players operation @s rpg_hud_p /= #rune5 rpg_hud_p
scoreboard players set @s rpg_hud_t 3
execute at @s anchored eyes run particle enchant ^ ^ ^0.4 0.25 0.25 0.25 0.2 4 force @s
""")
    wf("item/sword/legend/epic/sea_trigger.mcfunction", """
advancement revoke @s only rpg:item/sea
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{sea_tag:1b}] run scoreboard players reset @s sea_step
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{sea_tag:1b}] run return 0
scoreboard players add @s sea_step 1
execute if score @s sea_step matches 11.. run scoreboard players set @s sea_step 10
scoreboard players set @s rpg_hud 14
scoreboard players operation @s rpg_hud_p = @s sea_step
scoreboard players set @s rpg_hud_t 3
execute at @s anchored eyes run particle enchant ^ ^ ^0.4 0.25 0.25 0.25 0.2 3 force @s
""")

    wf("item/legacy_advanced/epic/tick.mcfunction", """
# 玩家状态彼此隔离；达到阈值时只释放自己的技能。
execute as @a[scores={ice_step=45..}] if items entity @s weapon.mainhand *[minecraft:custom_data~{ice_tag:1b}] at @s run function rpg:item/legacy_advanced/epic/ice_release
execute as @a[scores={sea_step=10..}] if items entity @s weapon.mainhand *[minecraft:custom_data~{sea_tag:1b}] at @s run function rpg:item/legacy_advanced/epic/sea_release
""")
    wf("item/legacy_advanced/epic/ice_release.mcfunction", """
scoreboard players set @s ice_step 0
playsound minecraft:entity.player.hurt_freeze player @s ~ ~ ~ 1 0.8
particle dust_pillar{block_state:{Name:blue_ice}} ~ ~1 ~ 2.5 1 2.5 0.15 50 force
effect give @e[distance=0.1..5,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:marker,type=!minecraft:armor_stand] slowness 4 4 true
tag @e[tag=rpg.ice.cast] remove rpg.ice.cast
tag @s add rpg.ice.cast
execute as @e[distance=0.1..5,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:marker,type=!minecraft:armor_stand] run damage @s 6 minecraft:freeze by @a[tag=rpg.ice.cast,limit=1]
tag @s remove rpg.ice.cast
title @s actionbar ["",{"text":"[严寒风暴]","italic":false,"color":"#45C9E8","bold":true},{"text":"　冻原扩张","italic":false,"color":"#BDEFFF"},{"text":" ✦","italic":false,"color":"#F2FDFF"}]
""")

    # The coral thrust reuses an owner-preserving immediate ray, rather than a
    # persistent, globally named armour stand pointed at @p.
    target = "@e[distance=..0.75,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:marker,type=!minecraft:armor_stand,limit=1,sort=nearest]"
    for step in range(1, 11):
        body = [
            "particle dust_color_transition{from_color:[1.0,0.38,0.92],to_color:[1.0,0.78,0.0],scale:2} ~ ~ ~ 0.12 0.12 0.12 0.02 4 force",
            "execute if entity %s run damage %s 9 minecraft:drown by @s" % (target, target),
        ]
        if step < 10:
            body.append("execute unless entity %s if block ~ ~ ~ minecraft:air positioned ^ ^ ^1 run function rpg:item/legacy_advanced/epic/sea_ray_%d" % (target, step + 1))
        wf("item/legacy_advanced/epic/sea_ray_%d.mcfunction" % step, "\n".join(body))
    wf("item/legacy_advanced/epic/sea_release.mcfunction", """
scoreboard players set @s sea_step 0
playsound minecraft:weather.rain player @s ~ ~ ~ 1 1.4
execute anchored eyes positioned ^ ^ ^1 run function rpg:item/legacy_advanced/epic/sea_ray_1
title @s actionbar ["",{"text":"[珊瑚突刺]","italic":false,"color":"#E56DB8","bold":true},{"text":"　潮锋贯出","italic":false,"color":"#FFC4E6"},{"text":" ✦","italic":false,"color":"#FFF0F9"}]
""")

    make_bar(13, "严　寒", "dark_aqua", "aqua")
    make_bar(14, "珊　瑚", "dark_purple", "light_purple")


def main() -> None:
    assert FUNC.is_dir(), "not a datapack: %s" % DP

    make_bar(10, "烈　焰", "dark_red", "red")
    make_bar(11, "钢　刃", "dark_aqua", "aqua")
    make_bar(12, "风　暴", "dark_green", "green")
    rune_charge("flame", 10)
    rune_charge("sweep", 11)
    rune_charge("wind", 12)
    rune_ray("flame", 17, "flame", "in_fire")
    rune_ray("sweep", 13, "sweep_attack", "player_attack")
    rune_ray("wind", 12, "gust", "wind_charge",
             "effect give $target levitation 1 1 true")
    rune_release("flame", "entity.blaze.shoot", "烈焰", "焚尽前路",
                 "#FF5A36", "#FFC0AA", "#FFF0E8")
    rune_release("sweep", "entity.player.attack.crit", "钢刃", "剑气出鞘",
                 "#55C6E3", "#BFEAF4", "#F3FDFF")
    rune_release("wind", "entity.breeze.wind_burst", "风暴", "风弹离手",
                 "#59B94C", "#BFE4B5", "#F0FFE9")
    advanced_hits()
    remove_retired_advanced_copies()
    epic_six()
    patch_advanced_roots()
    patch_advanced_lore()

    # Every advanced hit body now consumes only its own attacker's criterion
    # and temporary random score.  The original root cleared every player's
    # values at the end of the tick, so simultaneous attacks could erase one
    # another before their branch ran.
    legend = FUNC / "item/sword/legend/legend1.mcfunction"
    src = legend.read_text(encoding="utf-8")
    sakura_preadd = ("execute as @a[scores={sakura=0..},tag=rpg.h.sakura_tag1] "
                     "at @s run scoreboard players add @s sakura_step 1")
    src = src.replace(sakura_preadd,
                      "# sakura_step 只由本次攻击者的命中分支推进")
    assert sakura_preadd not in src, "reachable root still pre-increments Sakura"
    for objective in ("random", "saber", "sakura", "wukong", "axe"):
        src = src.replace("scoreboard players reset * " + objective,
                          "# %s 由命中分支只清本次攻击者" % objective)
    for forbidden in ("reset * random", "reset * saber", "reset * sakura",
                      "reset * wukong", "reset * axe"):
        assert forbidden not in src, "advanced global reset survived: " + forbidden
    legend.write_text(src, encoding="utf-8", newline="\n")

    add_once("command/soreboard.mcfunction", "#rune5 rpg_hud_p",
             "# 旧镶嵌的 0..50 蓄力映射到十段 HUD。\n"
             "scoreboard players set #rune5 rpg_hud_p 5")

    hud = FUNC / "hud/hud.mcfunction"
    src = hud.read_text(encoding="utf-8")
    needle = "# 没有技能占用时才轮到持续状态行。"
    missing = []
    for slot in range(10, 15):
        line = ("execute if entity @s[scores={rpg_hud_t=1..,rpg_hud=%d}] "
                "run function rpg:hud/s%d" % (slot, slot))
        if line not in src:
            missing.append(line)
    if missing:
        dispatch = "# legacy-advanced HUD\n" + "\n".join(missing) + "\n\n"
        assert needle in src, "HUD insertion point missing"
        hud.write_text(src.replace(needle, dispatch + needle, 1),
                       encoding="utf-8", newline="\n")

    # Clean-order audit: generated hit bodies carry the exact victim through a
    # synchronous temporary tag.  They never re-select a nearby rpg.hurt entity.
    namespace = FUNC / "item/legacy_advanced"
    generated = "\n".join(p.read_text(encoding="utf-8")
                           for p in namespace.rglob("*.mcfunction"))
    assert "rpg.hurt,distance=..0.2" not in generated
    assert "scoreboard players reset *" not in generated
    assert "summon minecraft:tnt" not in generated
    assert "scoreboard players reset @s axe" in (
        namespace / "hit/axe.mcfunction").read_text(encoding="utf-8")
    ice_release = (namespace / "epic/ice_release.mcfunction").read_text(encoding="utf-8")
    assert "tag @s add rpg.ice.cast" in ice_release
    assert "run damage @s 6 minecraft:freeze by @a[tag=rpg.ice.cast,limit=1]" in ice_release
    root_text = legend.read_text(encoding="utf-8")
    assert sakura_preadd not in root_text
    assert "item/sword/legend/saber/" not in root_text
    assert "item/sword/legend/wukong/particle" not in root_text
    for hook in ("hit/saber_victim", "hit/sakura_victim",
                 "hit/wukong_victim", "hit/axe_victim"):
        assert ("rpg:item/legacy_advanced/" + hook) in root_text, \
            "clean-build legacy hook missing: " + hook
    for branch in ("sakura", "night"):
        body = (namespace / ("hit/%s.mcfunction" % branch)).read_text(encoding="utf-8")
        assert body.count("scoreboard players add @s sakura_step 1") == 1
    for rel in ("item/legacy_advanced/hit/saber_victim.mcfunction",
                "item/legacy_advanced/hit/wukong_victim.mcfunction",
                "item/legacy_advanced/hit/axe_victim.mcfunction",
                "item/legacy_advanced/hit/sakura_victim.mcfunction",
                "item/legacy_advanced/hit/epic_victim.mcfunction"):
        body = (FUNC / rel).read_text(encoding="utf-8")
        assert "tag @e[tag=rpg.legacy.advanced_target] remove" in body
        assert "tag @s add rpg.legacy.advanced_target" in body
        assert "tag @s remove rpg.legacy.advanced_target" in body

    # 金箍棒的右键 advancement 独立于旧命中副本；它不是可退休文件。
    wukong_fly = FUNC / "item/sword/legend/wukong/fly.mcfunction"
    assert wukong_fly.is_file(), "wukong using_item reward target was retired"

    verify_joint_lore()
    print("legacy advanced: 3 original cards + 6 epic loot weapons + doctrine trims + 3 runes; joint original Lore 17/17")


if __name__ == "__main__":
    main()
