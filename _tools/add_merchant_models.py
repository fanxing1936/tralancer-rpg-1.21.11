# -*- coding: utf-8 -*-
"""地下城商人外观和原版动作。

    python add_merchant_models.py ../resourcepack ../rpg

四套源模型在 <key>_dungeons_ref/，交易、摆放及事件由 add_merchants.py 管理。
以村民执行 rpg:<key>/dress 换装，rpg:<key>/anim/<动作> 播放本实体的动作。
"""

import json
import os
import sys

import dungeons_variant
from display_mob import Mob, build, snbt_components, wf, wj, write_rig_runtime


HERE = os.path.dirname(os.path.abspath(__file__))
PART_TAG = "rpg.mer.model.part"
DRESS_TAG = "rpg.mer.model.dressing"
MERCHANTS = (
    ("smith", "铁匠", "rpg_msm"),
    ("mystery", "神秘商人", "rpg_mmy"),
    ("luxury", "奢侈品商人", "rpg_mlx"),
    ("travel", "迷途商人", "rpg_mtr"),
)
CLIPS = (("idle", 2, True), ("look", 1, False),
         ("bow", 1, False), ("examine", 1, False))


def merchant(kind, label, score):
    key = "merchant_" + kind
    mob = Mob(
        key=key, label=label, generator="add_merchant_models.py",
        bbmodel=os.path.join(HERE, key + "_dungeons_ref", key + ".bbmodel"),
        parts=[], glow=(), seat=1.95, tag="rpg.mer.model." + kind, score=score,
        carrier="minecraft:villager", clips=list(CLIPS), walk_clip="idle",
        tick_rounding="ceil", pose_cache=True,
    )
    if not dungeons_variant.apply(mob):
        raise SystemExit("%s: 缺少地下城源模型，或环境变量将模型设为 legacy" % key)
    names = set(c["clip"] for c in mob.dungeons_variant["clips"])
    if not all(name in names for name, _, _ in CLIPS):
        raise SystemExit("%s: 源模型缺少 idle/look/bow/examine 中的一段动作" % key)
    if mob.turn != 180:
        raise SystemExit("%s: 友方村民的 model_config.json 应指定 turn: 180" % key)
    return mob


def write_dress(mob, kind, first):
    fn = mob.fn
    wf(os.path.join(mob.func, "dress.mcfunction"), [
        "# 以目标村民执行；位置和朝向从载体读取。重复调用会重建本实体的外观。",
        "execute unless entity @s[type=minecraft:villager] run return 0",
        "execute at @s run function %s/dress_at" % fn,
    ])
    lines = [
        "# 清理这个村民的旧商人部件，保留原有交易数据与其他乘客。",
        "execute on passengers if entity @s[type=minecraft:item_display,tag=%s] run kill @s" % PART_TAG,
        "tag @s add rpg.mer",
    ]
    for other, _, _ in MERCHANTS:
        lines += ["tag @s remove rpg.mer." + other,
                  "tag @s remove rpg.mer.model." + other]
    lines += [
        "tag @s add rpg.mer." + kind,
        "tag @s add " + mob.tag,
        "data merge entity @s {NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,CanPickUpLoot:0b}",
        "effect give @s minecraft:invisibility infinite 0 true",
        "# 同一个函数顺序执行生成与挂载，重叠放置的商人也各自拥有部件。",
        "tag @e[type=minecraft:villager,tag=%s] remove %s" % (DRESS_TAG, DRESS_TAG),
        "tag @s add " + DRESS_TAG,
    ]
    for part, comp in first:
        lines.append("execute summon minecraft:item_display run function %s/part/%s" % (fn, part))
        wf(os.path.join(mob.func, "part", part + ".mcfunction"), [
            'data merge entity @s {Tags:["%s","%s.part","%s.p.%s"],'
            'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"%s/%s"}},'
            'item_display:"none",teleport_duration:2,interpolation_duration:2,'
            'view_range:1.5f,transformation:%s}'
            % (PART_TAG, mob.tag, mob.tag, part, fn, part, snbt_components(mob, comp)),
            "ride @s mount @e[type=minecraft:villager,tag=%s,limit=1]" % DRESS_TAG,
        ])
    lines += [
        "tag @s remove " + DRESS_TAG,
        "function %s/anim/init" % fn,
        "function %s/anim/enter/idle" % fn,
    ]
    wf(os.path.join(mob.func, "dress_at.mcfunction"), lines)


def write_animation_entries(mob):
    """固定 NPC 只播四段指定动作，单播片段结束由共享状态机切回 idle。"""
    fn, score = mob.fn, mob.clip_score
    os.remove(os.path.join(mob.anim, "stride.mcfunction"))
    wf(os.path.join(mob.anim, "tick.mcfunction"), [
        "# 每个载体独立记下片段和刻数。",
        "execute unless score @s %s matches 0..3 run function %s/anim/init" % (score, fn),
    ] + ["execute if score @s %s matches %d run return run function %s/anim/%s/tick"
         % (score, i, fn, name) for i, (name, _, _) in enumerate(CLIPS)])
    wf(os.path.join(mob.anim, "init.mcfunction"), [
        "scoreboard players set @s %s 0" % score,
        "scoreboard players set @s %s 0" % mob.t_score,
    ])
    wf(os.path.join(mob.func, "load.mcfunction"), [
        "# %s外观的每实体动画状态。" % mob.label,
        "scoreboard objectives add %s dummy" % score,
        "scoreboard objectives add %s dummy" % mob.t_score,
    ])
    for name, _, _ in CLIPS:
        lines = [
            "# 以这位%s为执行者播放 %s。" % (mob.label, name),
            "execute unless entity @s[%s] run return 0" % mob.carrier_sel,
            "execute at @s run function %s/anim/enter/%s" % (fn, name),
        ]
        sound = {"bow": "trade", "examine": "ambient"}.get(name)
        if sound:
            lines.append("execute at @s run playsound minecraft:entity.villager.%s neutral @a[distance=..16] ~ ~ ~ 1 1" % sound)
        wf(os.path.join(mob.anim, name + ".mcfunction"), lines)


def write_runtime(mob, kind, first):
    fn, tag = mob.fn, mob.tag
    write_dress(mob, kind, first)
    write_animation_entries(mob)
    selector = "type=minecraft:villager,tag=rpg.mer.%s,tag=!%s" % (kind, tag)
    write_rig_runtime(mob, [
        "# 为既有和新放置的%s补齐外观。" % mob.label,
        "execute as @e[%s] at @s run function %s/dress" % (selector, fn),
        "execute as @e[%s] at @s run function %s/follow" % (mob.carrier_sel, fn),
    ])
    # 仅旋转当前载体拥有的模型乘客，其他乘客由它们自己的逻辑处理。
    wf(os.path.join(mob.func, "follow.mcfunction"), [
        "# 骑乘负责位移，模型部件同步当前村民朝向。",
        "execute on passengers if entity @s[type=minecraft:item_display,tag=%s.part] run rotate @s ~ 0" % tag,
        "function %s/anim/tick" % fn,
        "execute unless predicate %s/invisible run effect give @s minecraft:invisibility infinite 0 true" % fn,
    ])
    wj(os.path.join(mob.dp, "data", "rpg", "predicate", mob.key, "invisible.json"), {
        "condition": "minecraft:entity_properties", "entity": "this",
        "predicate": {"effects": {"minecraft:invisibility": {}}},
    })


def ensure_tags(dp):
    # 支持给已有数据包增量生成，也支持在空目录做单独构建。
    for name in ("tick", "load"):
        path = os.path.join(dp, "data", "minecraft", "tags", "function", name + ".json")
        if not os.path.exists(path):
            wj(path, {"replace": False, "values": []})
        else:
            with open(path, encoding="utf-8") as fh:
                if not isinstance(json.load(fh).get("values"), list):
                    raise ValueError("无效函数标签文件：" + path)


def main(rp, dp):
    mobs = [(kind, merchant(kind, label, score)) for kind, label, score in MERCHANTS]
    ensure_tags(dp)
    for kind, mob in mobs:
        _baked, first = build(mob, rp, dp)
        write_runtime(mob, kind, first)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../resourcepack",
         sys.argv[2] if len(sys.argv) > 2 else "../rpg")
