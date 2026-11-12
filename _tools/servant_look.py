# -*- coding: utf-8 -*-
"""A lord's servants dressed in an extracted Dungeons model (dungeons_models.py -> <key>_dungeons_ref/).

Same shape as add_tower_wraith.py.  Only the look and voice change: the servants stay the illagers
add_demon_minions.py summons (`rpg.demon.minion.lordN`), with their health, AI, abilities, loot and
lifetime untouched.  Each tick any such servant not yet dressed gets `tag`, invisibility and the
display parts.  The servant's own vanilla mainhand item is drawn in the `weapon` part at the
original's weapon socket (Mob.held); the carrier keeps the item, its model set to rpg:empty.
When a player comes within reach and the move is off cooldown, a clip stands in for the illager's
own swing or shot: crossbow carriers and the evoker play `shoot` at range, the rest `attack` in melee.
An illusioner cannot be dressed (its renderer draws the body and its copies even while invisible);
add_demon_minions.py summons those hexers as pillagers instead.
"""

import os

import dungeons_variant
from display_mob import Mob, NS, build, hook_tag, playsound, snbt_components, wf, wj, write_rig_runtime

HERE = os.path.dirname(os.path.abspath(__file__))
SHOT_CD = 50                  # ticks between clips
SHOT_RANGE = 12               # blocks, crossbow carriers and the evoker
SWING_RANGE = 3.2             # blocks, everyone else
SHOOTERS = ("type=minecraft:pillager", "type=minecraft:evoker")


class ServantLook:
    def __init__(self, key, lord, label, tag, sounds, generator, cues=None, appear=None):
        self.key, self.lord, self.tag, self.appear = key, lord, tag, appear
        self.mob = Mob(
            key=key, label=label, generator=generator,
            bbmodel=os.path.join(HERE, key + "_dungeons_ref", key + ".bbmodel"), parts=[], glow=(),
            seat=2.0,           # vindicator, pillager and evoker share the illager seat
            tag=tag, score=tag.replace(".", "_"), carrier=None,
            clips=[("idle", 4, True), ("walk", 2, True), ("attack", 1, False), ("shoot", 1, False)],
            # an event's ids are .ogg files under sound_dir (originals from minecraft.wiki) or vanilla sound events
            sounds={e: (sub, ids, None if ids[0].endswith(".ogg") else {"type": "event"}) for e, (sub, ids) in sounds.items()},
            sound_dir=os.path.join(HERE, "dungeons_sounds"),
            cues=cues or {},
            hurt="hurt" if "hurt" in sounds else None, death="death" if "death" in sounds else None,
            ambient=("idle", 0.006) if "idle" in sounds else None, held="weapon",
        )
        if not dungeons_variant.apply(self.mob):
            raise SystemExit("%s: the extracted model is missing (python dungeons_models.py %s)" % (key, key))

    def write_datapack(self, baked, dp):
        m, t, fn = self.mob, self.tag, "rpg:" + self.mob.key
        servants = "tag=rpg.demon.minion.lord%d,tag=!%s,type=!minecraft:illusioner" % (self.lord, t)
        first = baked["idle"]["frames"][0][1]
        lines = [
            "# %s（as 罪仆，at 其脚下）。只加 %s 标签、隐身与部件，手上的物品不换，只把它的模型设成空的。" % (m.label, t),
            "tag @s add %s" % t,
            "tag @s add %s.dressing" % t,
            "effect give @s minecraft:invisibility infinite 0 true",
        ]
        for part, _ in m.parts:
            if part == m.held:
                lines.append(
                    'summon minecraft:item_display ~ ~ ~ {Tags:["%s.part","%s.p.%s","%s.new"],'
                    'item_display:"thirdperson_righthand",teleport_duration:2,interpolation_duration:2,'
                    'view_range:1f,transformation:%s}' % (t, t, part, t, snbt_components(m, first[part])))
                continue
            lines.append(
                'summon minecraft:item_display ~ ~ ~ {Tags:["%s.part","%s.p.%s","%s.new"],'
                'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:%s/%s"}},'
                'item_display:"none",teleport_duration:2,interpolation_duration:2,'
                'view_range:1f,transformation:%s}' % (t, t, part, t, m.key, part, snbt_components(m, first[part])))
        lines += [
            "execute as @e[type=minecraft:item_display,tag=%s.new,distance=..1] run "
            "ride @s mount @e[tag=%s.dressing,limit=1]" % (t, t),
            "# 手里的原版物品复制到 weapon 部件上画出来，载体自己的那份只把模型设成空的",
            "item replace entity @e[type=minecraft:item_display,tag=%s.new,tag=%s.p.weapon,distance=..1,limit=1] "
            "contents from entity @s weapon.mainhand" % (t, t),
            'item modify entity @s weapon.mainhand {function:"minecraft:set_components",'
            'components:{"minecraft:item_model":"rpg:empty"}}',
            "tag @e[type=minecraft:item_display,tag=%s.new,distance=..1] remove %s.new" % (t, t),
            "tag @s remove %s.dressing" % t,
            "scoreboard players set @s %s 0" % m.score,
            "function %s/anim/init" % fn,
        ]
        if self.appear:
            lines.append(playsound(m, self.appear, 1.0, 1.0, 24))
        wf(os.path.join(m.func, "dress.mcfunction"), lines)
        wf(os.path.join(m.func, "strike.mcfunction"), [
            "# 有人进了距离：持弩的与司祭远程出手，其余的近战。冷却借用 %s 的个体分数。" % m.score,
            "scoreboard players set @s %s %d" % (m.score, SHOT_CD),
        ] + ["execute if entity @s[%s] run return run function %s/anim/enter/shoot" % (s, fn) for s in SHOOTERS]
          + ["function %s/anim/enter/attack" % fn])
        ready = "execute if score @s %s matches ..0 unless score @s %s_anim matches 2..3 " % (m.score, m.score)
        near = "if entity @a[distance=..%s,gamemode=!spectator,gamemode=!creative,limit=1] run function %s/strike"
        write_rig_runtime(m, [
            "# %s每刻入口。任何途径召出的第 %d 柱罪仆（手动、仪式二阶段）都在这里换装。" % (m.label, self.lord),
            "execute if entity @e[%s,limit=1] as @e[%s] at @s run function %s/dress" % (servants, servants, fn),
            "execute if entity @e[tag=%s,type=!minecraft:item_display,limit=1] "
            "as @e[tag=%s,type=!minecraft:item_display] at @s run function %s/follow" % (t, t, fn),
        ], follow_extra=[
            "execute if score @s %s matches 1.. run scoreboard players remove @s %s 1" % (m.score, m.score),
        ] + [ready + "if entity @s[%s] " % s + near % (SHOT_RANGE, fn) for s in SHOOTERS]
          + [ready + "unless entity @s[%s] unless entity @s[%s] " % SHOOTERS + near % (SWING_RANGE, fn)])
        wj(os.path.join(dp, "data", NS, "predicate", m.key, "invisible.json"), {
            "condition": "minecraft:entity_properties", "entity": "this",
            "predicate": {"effects": {"minecraft:invisibility": {}}}})
        # the warden phase clears invisibility from whatever attacked something;
        # the servant's body is the model, so put it back after everything else
        wf(os.path.join(m.func, "tick_late.mcfunction"), [
            "# %s的身体是模型：载体始终隐身。" % m.label,
            "execute as @e[tag=%s,type=!minecraft:item_display] unless predicate %s/invisible "
            "run effect give @s minecraft:invisibility infinite 0 true" % (t, fn),
        ])
        hook_tag(dp, "tick", fn + "/tick_late", False)

    def main(self, rp, dp):
        baked, _ = build(self.mob, rp, dp)
        wj(os.path.join(rp, "assets", NS, "items", "empty.json"), {"model": {"type": "minecraft:empty"}})
        if os.path.isdir(os.path.join(dp, "data", NS, "function", "minion")):
            self.write_datapack(baked, dp)
