# -*- coding: utf-8 -*-
"""城镇的地下城外观。运行 python add_town_models.py ../resourcepack ../rpg。"""

import argparse
import json
from pathlib import Path

import display_mob as dm
import dungeons_variant
from town_models_ref import props


HERE = Path(__file__).resolve().parent
NS = "rpg:town_models"
PART_TAG = "rpg.tw.model.part"
DRESS_TAG = "rpg.tw.model.dressing"
PROBE_TAG = "rpg.tw.model.probing"
NPC = "minecraft:villager"
ZOMBIE = "minecraft:zombie"
ADULT_SEAT = 1.95
ZOMBIE_SEAT = 2.0125

IDLE = ("idle", 2, True)
LOOK = ("look", 1, False)
TALK = ("talk", 1, False)
COMBAT = (IDLE, ("walk", 2, True), ("attack", 1, False))

# 载体由城镇及事件系统创建。巨型僵尸优先，普通空心人排除巨型标签。
ACTORS = (
    ("town_priest", "神父", NPC, "rpg.tnpc.priest", ADULT_SEAT, (IDLE, TALK)),
    ("town_elder", "长者", NPC, "rpg.tnpc.elder", ADULT_SEAT, (IDLE, LOOK)),
    ("town_bard", "吟游诗人", NPC, "rpg.tnpc.bard", ADULT_SEAT, (IDLE,)),
    ("town_watchman", "守夜人", NPC, "rpg.tnpc.watchman", ADULT_SEAT, (IDLE,)),
    ("town_witch", "女巫", NPC, "rpg.tnpc.witch", ADULT_SEAT, (IDLE,)),
    ("town_edgewalker", "边缘者", NPC, "rpg.tnpc.hood", ADULT_SEAT, (IDLE,)),
    ("town_inquisitor", "审判官", "minecraft:vindicator", "rpg.te.inq", 2.0, COMBAT),
    ("town_folk_a", "农妇", NPC, "rpg.tnpc.farmwife", ADULT_SEAT, (IDLE, LOOK)),
    ("town_folk_b", "农夫", NPC, "rpg.tnpc.farmer", ADULT_SEAT, (IDLE, LOOK)),
    ("town_folk_c", "少年", NPC, "rpg.tnpc.lad", ADULT_SEAT, (IDLE, LOOK)),
    ("town_child", "孩童", NPC, "rpg.tnpc.child", ADULT_SEAT * 0.5, (IDLE,)),
    ("town_hollow_big", "巨型空心人", ZOMBIE, "rpg.te.big", ZOMBIE_SEAT * 1.8, COMBAT),
    ("town_hollow", "空心人", ZOMBIE, "rpg.te.hol,tag=!rpg.te.big", ZOMBIE_SEAT, COMBAT),
)


def make_mob(index, actor):
    key, label, carrier, _, seat, clips = actor
    held = "lantern" if key == "town_watchman" else None
    mob = dm.Mob(
        key=key, label=label, generator=Path(__file__).name,
        bbmodel=HERE / f"{key}_dungeons_ref" / f"{key}.bbmodel",
        parts=[], glow=(), seat=seat, tag=f"rpg.tw.model.{key[5:]}",
        score=f"rpg_tw_m{index}", clips=clips, carrier=carrier, held=held,
        model_scale=0.7 if held else 1.0,
        walk_clip="walk" if clips == COMBAT else "idle",
        pose_cache=True, tick_rounding="ceil",
    )
    if not dungeons_variant.apply(mob):
        raise ValueError(f"{key} 缺少可用的地下城模型")
    names = {clip["clip"] for clip in mob.dungeons_variant["clips"]}
    if missing := {name for name, _, _ in clips} - names:
        raise ValueError(f"{key} 缺少动作 {', '.join(sorted(missing))}")
    if carrier == NPC and mob.turn != 180:
        raise ValueError(f"{key} 的友方外观需要 turn=180")

    # 先按标准 key 读取转换产物，再将所有游戏资源放进城镇外观命名路径。
    mob.key = f"town_models/{key}"
    mob.fn = f"rpg:{mob.key}"
    mob.tex = f"rpg:item/{mob.key}/atlas"
    return mob


def function(mob, name, lines):
    dm.wf(Path(mob.func) / f"{name}.mcfunction", lines)


def write_dress(mob, roster, first):
    fn = mob.fn
    function(mob, "dress", [
        "# 以载体执行，读取它自己的位置和朝向。",
        f"execute unless entity @s[type={mob.carrier}] run return 0",
        f"execute at @s run function {fn}/dress_at",
    ])
    parts = [
        "# 重复换装或换角色时，只替换当前载体的城镇模型乘客。",
        f"execute on passengers if entity @s[type=minecraft:item_display,tag={PART_TAG}] run kill @s",
    ]
    parts.extend(f"tag @s remove {other.tag}" for other in roster if other is not mob)
    parts.extend([
        f"tag @s add {mob.tag}",
        "effect give @s minecraft:invisibility infinite 0 true",
        f"tag @e[type={mob.carrier},tag={DRESS_TAG},distance=..1] remove {DRESS_TAG}",
        f"tag @s add {DRESS_TAG}",
    ])
    for part, comp in first:
        parts.append(f"execute summon minecraft:item_display run function {fn}/part/{part}")
        item = '{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"%s/%s"}}' % (fn, part)
        function(mob, f"part/{part}", [
            f'data merge entity @s {{Tags:["{PART_TAG}","{mob.tag}.part","{mob.tag}.p.{part}"],'
            f'item:{item},item_display:"none",teleport_duration:2,interpolation_duration:2,'
            f'view_range:1.5f,transformation:{dm.snbt_components(mob, comp)}}}',
            "rotate @s ~ 0",
            f"ride @s mount @e[type={mob.carrier},tag={DRESS_TAG},distance=..1,limit=1]",
        ])
    parts.extend([
        f"tag @s remove {DRESS_TAG}",
        f"function {fn}/anim/init",
        f"function {fn}/anim/enter/idle",
    ])
    function(mob, "dress_at", parts)


def write_animation_entries(mob):
    fn = mob.fn
    score, ticks = mob.clip_score, mob.t_score
    if mob.clips != COMBAT:
        # 固定村民只推进显式指定的动作，减少对载体 Pos 的读取。
        (Path(mob.anim) / "stride.mcfunction").unlink()
        function(mob, "load", [f"scoreboard objectives add {s} dummy" for s in (score, ticks)])
        function(mob, "anim/init", [f"scoreboard players set @s {s} 0" for s in (score, ticks)])
        function(mob, "anim/tick", [
            f"execute unless score @s {score} matches 0..{len(mob.clips) - 1} run function {fn}/anim/init",
        ] + [
            f"execute if score @s {score} matches {i} run return run function {fn}/anim/{name}/tick"
            for i, (name, _, _) in enumerate(mob.clips)
        ])
    for name, _, _ in mob.clips:
        function(mob, f"anim/{name}", [
            f"execute if entity @s[{mob.carrier_sel}] at @s run function {fn}/anim/enter/{name}",
        ])


def write_runtime(mob):
    fn = mob.fn
    dm.write_rig_runtime(mob, [
        f"execute as @e[{mob.carrier_sel}] at @s run function {fn}/follow",
    ])
    follow = [
        f"execute on passengers if entity @s[type=minecraft:item_display,tag={mob.tag}.part] run rotate @s ~ 0",
        f"function {fn}/anim/tick",
        f"execute unless predicate {fn}/invisible run effect give @s minecraft:invisibility infinite 0 true",
    ]
    if mob.clips == COMBAT:
        function(mob, "attack_probe", [
            "# 只观察原版 AI 的攻击。用目标的受击时间和最近攻击者确认命中归属。",
            f"tag @s add {PROBE_TAG}",
            f"execute on target if predicate {NS}/just_hurt on attacker if entity @s[tag={PROBE_TAG}] "
            f"at @s run function {fn}/anim/enter/attack",
            f"tag @s remove {PROBE_TAG}",
        ])
        follow.insert(2, f"execute unless score @s {mob.clip_score} matches 2 run function {fn}/attack_probe")
    function(mob, "follow", follow)
    dm.wj(Path(mob.dp) / "data/rpg/predicate" / mob.key / "invisible.json", {
        "condition": "minecraft:entity_properties", "entity": "this",
        "predicate": {"effects": {"minecraft:invisibility": {}}},
    })


def quat_mul(a, b):
    ax, ay, az, aw = a
    bx, by, bz, bw = b
    return [
        aw * bx + ax * bw + ay * bz - az * by,
        aw * by - ax * bz + ay * bw + az * bx,
        aw * bz + ax * by - ay * bx + az * bw,
        aw * bw - ax * bx - ay * by - az * bz,
    ]


def orient_lantern(mob, baked):
    """以原作武器挂点为提手，首帧竖直，后续照原作挂点旋转。"""
    rest = baked["idle"]["frames"][0][1][mob.held][1]
    undo_rest = [-rest[0], -rest[1], -rest[2], rest[3]]
    for clip in baked.values():
        for _, frame in clip["frames"]:
            position, rotation, scale = frame[mob.held]
            hanging = quat_mul(rotation, undo_rest)
            # 原版灯笼提手顶部位于 y=11，item_display 的模型中心位于 y=8。
            local = [0, -3 * scale[1] / 16, 0, 0]
            inverse = [-hanging[0], -hanging[1], -hanging[2], hanging[3]]
            offset = quat_mul(quat_mul(hanging, local), inverse)
            frame[mob.held] = ([x + dx for x, dx in zip(position, offset)], hanging, scale)
    dm.write_anim(mob, baked)
    dm.wj(Path(mob.rp) / "assets/rpg/items" / mob.key / f"{mob.held}.json", {
        "model": {"type": "minecraft:model", "model": "minecraft:block/lantern"},
    })
    return list(baked["idle"]["frames"][0][1].items())


def read_tag(path):
    if not path.exists():
        return {"replace": False, "values": []}
    doc = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(doc.get("values"), list):
        raise ValueError(f"函数标签缺少有效的 values 列表：{path}")
    return doc


def generate(rp, dp):
    roster = [make_mob(i, spec) for i, spec in enumerate(ACTORS)]
    data = Path(dp) / "data"
    town_tag = data / "rpg/tags/function/town_dress.json"
    dress_tag = read_tag(town_tag)
    for name in ("load", "tick"):
        tag = data / f"minecraft/tags/function/{name}.json"
        tag_doc = read_tag(tag)
        if not tag.exists():
            dm.wj(tag, tag_doc)

    dm.wf(data / "rpg/function/town_models/dress_any.mcfunction", [
        "# 按载体实体类型和角色标签选取一套外观。",
    ] + [
        f"execute if entity @s[type={carrier},tag={tag}] run return run function {mob.fn}/dress"
        for mob, (_, _, carrier, tag, _, _) in zip(roster, ACTORS)
    ])
    dm.wj(data / "rpg/predicate/town_models/just_hurt.json", {
        "condition": "minecraft:any_of", "terms": [
            {"condition": "minecraft:entity_properties", "entity": "this",
             "predicate": {"nbt": f"{{HurtTime:{tick}s}}"}}
            for tick in (9, 10)
        ],
    })
    for mob in roster:
        baked, first = dm.build(mob, rp, dp)
        if mob.held:
            first = orient_lantern(mob, baked)
        write_dress(mob, roster, first)
        write_animation_entries(mob)
        write_runtime(mob)
    props.generate(rp, dp)
    entry = f"{NS}/dress_any"
    existing_ids = [v.get("id") if isinstance(v, dict) else v for v in dress_tag["values"]]
    if entry not in existing_ids:
        dress_tag["values"].append(entry)
    dm.wj(town_tag, dress_tag)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rp", type=Path, nargs="?", default=Path("../resourcepack"))
    parser.add_argument("dp", type=Path, nargs="?", default=Path("../rpg"))
    args = parser.parse_args()
    generate(args.rp, args.dp)
