# -*- coding: utf-8 -*-
"""A lord's look from an extracted Dungeons model (dungeons_models.py -> <key>_dungeons_ref/).

Only the look changes.  The lord stays the invisible vindicator that rpg:taint/lordN (and every
other path ending in `rpg_dm_lord N`: the seal escape, the debug summon) summons, with its tags,
health, skills, true-name inquest and exorcism untouched.  Each tick, any such vindicator not yet
dressed gets `tag` and the display parts; the parts carry only `<tag>.*` tags, so no `rpg.demon` /
`devil` selector sees them.  Same shape as add_leviathan_model.py.

    LordLook(key, lord, label, tag, clips, skills, sounds).main(rp, dp)

skills: {taint hook: (clip or None, sound event or None)}; the clip plays and the sound sounds when
the hook runs, appended to rpg:taint/<hook>.  sounds: {event: (subtitles, [vanilla event ids])}.
"""

import io
import os

import dungeons_variant
from display_mob import Mob, NS, build, hook_tag, playsound, snbt_components, wf, wj, write_rig_runtime

HERE = os.path.dirname(os.path.abspath(__file__))


class LordLook:
    def __init__(self, key, lord, label, tag, clips, skills, sounds, generator, arrive="rise",
                 arrive_sound=None, gone_sound=None, cues=None, enter_cues=None, carriers=None,
                 carrier_type="minecraft:vindicator"):
        """carriers: a selector for who gets dressed, instead of the lord-N vindicator (a boss that is
        not one of the seven, e.g. the Usurper); then skills / gone_sound are usually empty.
        carrier_type: the carriers' entity type; None when they come in more than one type (Jacques the boss is a
        vindicator, Jacques the ally an iron golem), then only the look tag picks them."""
        self.carriers = carriers
        self.ct = ("type=%s," % carrier_type) if carrier_type else ""
        self.key, self.lord, self.tag, self.skills = key, lord, tag, skills
        self.arrive, self.arrive_sound, self.gone_sound = arrive, arrive_sound, gone_sound
        self.mark = "# %s外观（%s）" % (label, generator)
        self.mob = Mob(
            key=key, label=label, generator=generator,
            bbmodel=os.path.join(HERE, key + "_dungeons_ref", key + ".bbmodel"), parts=[], glow=(),
            seat=2.0,           # the lord is a plain vindicator
            tag=tag, score=tag.replace(".", "_"), clips=clips,
            # an event's ids are .ogg files under sound_dir (originals from minecraft.wiki) or vanilla sound events
            sounds={e: (sub, ids, None if ids[0].endswith(".ogg") else {"type": "event"}) for e, (sub, ids) in sounds.items()},
            sound_dir=os.path.join(HERE, "dungeons_sounds"),
            cues=cues or {}, enter_cues=enter_cues or {},
            hurt="hurt" if "hurt" in sounds else None, death="death" if "death" in sounds else None,
            ambient=("idle", 0.006) if "idle" in sounds else None,
        )
        if not dungeons_variant.apply(self.mob):
            raise SystemExit("%s: the extracted model is missing (python dungeons_models.py %s)" % (key, key))

    # ------------------------------------------------------------------
    def dress(self, first):
        m, t = self.mob, self.tag
        lines = [
            "# %s换装（as 降临者，at 其脚下）。只加 %s 标签与部件，不碰其他标签与数值。" % (m.label, t),
            "tag @s add %s" % t,
            "tag @s add %s.dressing" % t,
        ]
        for part, comp in first:
            lines.append(
                'summon minecraft:item_display ~ ~ ~ {Tags:["%s.part","%s.p.%s","%s.new"],'
                'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:%s/%s"}},'
                'item_display:"none",teleport_duration:2,interpolation_duration:2,'
                'view_range:1.5f,transformation:%s}' % (t, t, part, t, m.key, part, snbt_components(m, comp)))
        lines += [
            "execute as @e[type=minecraft:item_display,tag=%s.new,distance=..1] run "
            "ride @s mount @e[%stag=%s.dressing,limit=1]" % (t, self.ct, t),
            "tag @e[type=minecraft:item_display,tag=%s.new,distance=..1] remove %s.new" % (t, t),
            "tag @s remove %s.dressing" % t,
            "function rpg:%s/anim/init" % m.key,
        ]
        if self.arrive_sound:
            lines.append(playsound(m, self.arrive_sound, 1.2, 0.8, 48))
        lines.append("function rpg:%s/anim/enter/%s" % (m.key, self.arrive))
        wf(os.path.join(m.func, "dress.mcfunction"), lines)

    def write_datapack(self, baked, dp):
        m, t, fn = self.mob, self.tag, "rpg:" + self.mob.key
        taint = os.path.join(dp, "data", NS, "function", "taint")
        first = baked[self.arrive]["frames"][0][1]
        self.dress([(p, first[p]) for p, _ in m.parts])
        lord = (self.carriers + ",tag=!" + t) if self.carriers else             "type=minecraft:vindicator,tag=rpg.advent,tag=!%s,scores={rpg_dm_lord=%d}" % (t, self.lord)
        write_rig_runtime(m, [
            "# %s每刻入口。任何召唤路径落地的第 %d 柱都在这里换装（含封印逃逸、调试召唤）。" % (m.label, self.lord),
            "execute if entity @e[%s,limit=1] as @e[%s] at @s run function %s/dress" % (lord, lord, fn),
            "execute if entity @e[%stag=%s,limit=1] as @e[%stag=%s] "
            "at @s run function %s/follow" % (self.ct, t, self.ct, t, fn),
        ], follow_extra=[
            "# 被法阵束缚时载体发光：部件一起发光",
            "execute if predicate %s/glowing unless entity @s[tag=%s.glow] run function %s/glow_on" % (fn, t, fn),
            "execute unless predicate %s/glowing if entity @s[tag=%s.glow] run function %s/glow_off" % (fn, t, fn),
        ])
        pred = os.path.join(dp, "data", NS, "predicate", m.key)
        for name, effect in (("glowing", "minecraft:glowing"), ("invisible", "minecraft:invisibility")):
            wj(os.path.join(pred, name + ".json"), {
                "condition": "minecraft:entity_properties", "entity": "this",
                "predicate": {"effects": {effect: {}}}})
        for name, on in (("glow_on", True), ("glow_off", False)):
            wf(os.path.join(m.func, name + ".mcfunction"), [
                "tag @s %s %s.glow" % ("add" if on else "remove", t),
                "execute on passengers if entity @s[type=minecraft:item_display] run data merge entity @s {Glowing:%db}"
                % (1 if on else 0),
            ])
        # after rpg:command/tick_end, the last thing that clears the lord's invisibility
        wf(os.path.join(m.func, "tick_late.mcfunction"), [
            "# %s的身体是模型：载体本身始终隐身（驱魔的显形只清隐身效果，没有逻辑读它）。" % m.label,
            "execute as @e[%stag=%s] unless predicate %s/invisible "
            "run effect give @s minecraft:invisibility infinite 0 true" % (self.ct, t, fn),
        ])
        hook_tag(dp, "tick", fn + "/tick_late", False)

        for hook, (clip, sound) in self.skills.items():
            lines = ["# %s 的外观与声音。由 %s 生成。" % (hook, m.generator)]
            if clip:
                lines.append("function %s/anim/enter/%s" % (fn, clip))
            if sound:
                lines.append("execute at @s run " + playsound(m, sound, 1.2, 1.0, 32))
            wf(os.path.join(m.func, "skill", hook + ".mcfunction"), lines)
            self._append(taint, hook, "execute if entity @s[tag=%s] run function %s/skill/%s" % (t, fn, hook))
        if self.gone_sound:
            self._prepend(taint, "advent_gone", [
                "execute if entity @s[tag=%s] at @s run %s" % (t, playsound(m, self.gone_sound, 1.2, 0.8, 32))])

    def _read(self, taint, name):
        path = os.path.join(taint, name + ".mcfunction")
        with io.open(path, encoding="utf-8") as fh:
            return path, fh.read().rstrip("\n").split("\n")

    def _append(self, taint, name, line):
        path, lines = self._read(taint, name)
        if self.mark in lines:
            return
        wf(path, lines + [self.mark, line])

    def _prepend(self, taint, name, new):
        """After the leading comment block."""
        path, lines = self._read(taint, name)
        if self.mark in lines:
            return
        i = 0
        while i < len(lines) and lines[i].startswith("#"):
            i += 1
        wf(path, lines[:i] + [self.mark] + new + lines[i:])

    def main(self, rp, dp):
        baked, _ = build(self.mob, rp, dp)
        if os.path.isdir(os.path.join(dp, "data", NS, "function", "taint")):
            self.write_datapack(baked, dp)
