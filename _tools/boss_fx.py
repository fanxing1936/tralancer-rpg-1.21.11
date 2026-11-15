# -*- coding: utf-8 -*-
"""A small display-entity VFX kit for a boss fight, on the art add_usurper_fx_art.py writes
(font rpg:usurper_fx glyphs, rpg:usurper_fx/* item models; every sprite is white and tinted at run time).

Same rules as the Usurper fight (display-render-facts):
  glowing sprites are text_display glyphs (unlit, tinted by the text colour, billboarded);
  ground decals and solid props are item_display (up faces full bright), tinted through custom_model_data colour 0.
Every effect is born with a lifetime and a kind; <fn>/fx/tick (as each effect, each tick) counts the life down,
kills it at zero, and on the ticks a kind names swaps a frame or sends one interpolated data merge.

    fx = Fx(fn="rpg:jacques_boss", tag="rpg.jqb.fx", life="rpg_jq_life", kind="rpg_jq_kd", writer=w)
    lines = fx.glyph("burst", 3, "#F0CF7A", kind="burst")
    fx.build()          # writes fx/tick, fx/kind, fx/k/<kind>
"""

import add_usurper_fx_art as art

FONT = "rpg:usurper_fx"
NS = "rpg:usurper_fx"
ID = "[0f,0f,0f,1f]"


def color_int(c):
    return int(c.lstrip("#"), 16) if isinstance(c, str) else c


def gscale(name, blocks):
    """Scale that makes a glyph `blocks` wide (one glyph pixel is 0.025 block at scale 1)."""
    return round(blocks / (art.glyph_table()[name][1] * 0.025), 4)


def sc(s):
    return "scale:[%gf,%gf,%gf]" % (s if isinstance(s, tuple) else (s, s, s))


def flat_sc(s):
    return "scale:[%gf,1f,%gf]" % (s, s)


TW = gscale("star", 0.7)
RAY_W, RAY_H = gscale("ray", 1.6), gscale("ray", 4.2)
SLASH_K = gscale("slash", 2.4)
BOLT_W = 2.4
BOLT_K = gscale("bolt", BOLT_W)
BOLT_H = BOLT_K * 4

KINDS = {
    "spin": dict(extra=["tp @s ~ ~ ~ ~3 ~"]),
    "spinr": dict(extra=["tp @s ~ ~ ~ ~-2 ~"]),
    "pop": dict(life=10, frames=("glyph", "pop", 10, 1)),
    "burst": dict(life=16, frames=("glyph", "burst", 8, 2)),
    "shock": dict(life=16, frames=("item", "shock", 8, 2)),
    "sq": dict(life=8, frames=("item", "sq", 8, 1)),
    "twinkle": dict(life=10, steps=[(9, 3, sc(TW)), (4, 4, sc(0.01))]),
    "ray": dict(life=16, steps=[(15, 4, sc((RAY_W, RAY_H, RAY_W))), (6, 6, sc((0.01, RAY_H, 0.01)))]),
    "raylong": dict(life=60, steps=[(59, 8, sc((RAY_W, RAY_H, RAY_W))), (6, 6, sc((0.01, RAY_H, 0.01)))]),
    "spark": dict(life=8, frames=("glyph", "spark", 8, 1)),
    "sparkl": dict(life=60, frames=("glyph", "spark", 15, 4)),
    "bolt": dict(life=10, frames=("glyph", "bolt", 4, 2), steps=[(3, 3, "scale:[0.01f,%gf,0.01f]" % BOLT_H)]),
    "slashfx": dict(life=8, steps=[(7, 2, sc(SLASH_K * 1.25)), (3, 3, sc(0.01))]),
    "rise": dict(life=150, steps=[(149, 16, "translation:[0f,0f,0f]"), (14, 10, "translation:[0f,-3f,0f]")]),
}


class Fx:
    def __init__(self, fn, tag, life, kind, writer, kinds=None):
        self.fn, self.tag, self.life_obj, self.kind_obj, self.w = fn, tag, life, kind, writer
        self.new = tag + "new"
        self.kinds = dict(KINDS)
        self.kinds.update(kinds or {})
        self.ids = dict((n, i + 1) for i, n in enumerate(self.kinds))

    # ---- birth
    def born(self, life=None, kind=None):
        if kind and life is None:
            life = self.kinds[kind]["life"]
        return ["scoreboard players set @e[tag=%s] %s %d" % (self.new, self.life_obj, life),
                "scoreboard players set @e[tag=%s] %s %d" % (self.new, self.kind_obj, self.ids[kind] if kind else 0),
                "tag @e[tag=%s] remove %s" % (self.new, self.new)]

    def _tags(self, tags):
        return ",".join('"%s"' % x for x in (self.tag, self.new) + tuple(tags))

    def disp(self, model, pos="~ ~ ~", scale=1.0, color=0xFFFFFF, tags=(), billboard=None, trans=(0, 0, 0), tp=1, yaw=None,
             lrot=None, view=2):
        """A solid item_display (decal plane, beam box, prop), tinted; born with the new tag (follow with born())."""
        s = scale if isinstance(scale, tuple) else (scale, scale, scale)
        bb = ',billboard:"%s"' % billboard if billboard else ""
        if yaw is not None:
            bb += ",Rotation:[%sf,0f]" % yaw
        if ":" not in model:
            model = "%s/%s" % (NS, model)
        return ('summon minecraft:item_display %s {Tags:[%s],item:{id:"minecraft:paper",count:1,components:'
                '{"minecraft:item_model":"%s","minecraft:custom_model_data":{colors:[%d]}}},brightness:{sky:15,block:15},'
                'teleport_duration:%d,interpolation_duration:3,view_range:%gf,transformation:{translation:[%sf,%sf,%sf],'
                'left_rotation:%s,scale:[%sf,%sf,%sf],right_rotation:%s}%s}' % (
                    pos, self._tags(tags), model, color_int(color), tp, view, trans[0], trans[1], trans[2], lrot or ID,
                    s[0], s[1], s[2], ID, bb))

    def marker(self, pos, *tags):
        return "summon minecraft:marker %s {Tags:[%s]}" % (pos, self._tags(tags))

    def decal(self, name, size, color, pos="~ ~0.05 ~", kind=None, life=None, tags=(), yaw=None):
        """A ground decal (up-facing plane, `size` blocks across), born at once."""
        return [self.disp(name, pos=pos, scale=(size, 1, size), color=color, tags=tags, yaw=yaw)] + self.born(life, kind)

    def glyph(self, name, blocks, color, pos="~ ~ ~", frame=0, kind=None, life=None, tags=(), billboard="center",
              trans=(0, 0, 0), start=None, born_now=True, tpd=1):
        """A glowing sprite: one text_display glyph, tinted by the text colour."""
        k = gscale(name, blocks)
        s = start if start is not None else (k, k, k)
        if not isinstance(s, tuple):
            s = (s, s, s)
        line = ('summon minecraft:text_display %s {Tags:[%s],text:{text:"%s",font:"%s",color:"%s"},background:0,'
                'billboard:"%s",brightness:{sky:15,block:15},teleport_duration:%d,interpolation_duration:3,view_range:2f,'
                'transformation:{translation:[%sf,%sf,%sf],left_rotation:%s,scale:[%gf,%gf,%gf],right_rotation:%s}}'
                % (pos, self._tags(tags), art.glyph_text(name, frame), FONT, color, billboard, tpd, trans[0], trans[1], trans[2],
                   ID, s[0], s[1], s[2], ID))
        return [line] + (self.born(life, kind) if born_now else [])

    # ---- shorthands
    def twinkle(self, pos, color, frame=1):
        return self.glyph("star", 0.7, color, pos=pos, frame=frame, kind="twinkle", start=0.01)

    def ray(self, pos, color, long=False, tags=()):
        return self.glyph("ray", 1.6, color, pos=pos, billboard="vertical", kind="raylong" if long else "ray",
                          start=(RAY_W, 0.01, RAY_W), trans=(0, 2.1, 0), tags=tags)

    def bolt(self, pos, color):
        return self.glyph("bolt", BOLT_W, color, pos=pos, kind="bolt", billboard="vertical", start=(BOLT_K, BOLT_H, BOLT_K),
                          trans=(0, BOLT_W * 2, 0))

    def spark(self, pos, color, size=0.9, frame=0):
        return self.glyph("spark", size, color, pos=pos, frame=frame, kind="spark")

    def slash(self, pos, color, size=2.4, frame=0):
        return self.glyph("slash", size, color, pos=pos, frame=frame, kind="slashfx")

    def morph(self, selector, scale, ticks=4, decal_=False):
        return ("execute as @e[%s] run data merge entity @s {start_interpolation:0,interpolation_duration:%d,"
                "transformation:{%s}}" % (selector, ticks, flat_sc(scale) if decal_ else sc(scale)))

    # ---- runtime
    def build(self, extra_tick=()):
        """fx/tick (as each effect): life, then a kind's frame swap or interpolation step on its tick."""
        self.w("fx/tick", [
            "# 每个特效实体每刻（as/at 它）。",
            "scoreboard players remove @s %s 1" % self.life_obj,
            "execute if score @s %s matches ..0 run return run kill @s" % self.life_obj,
        ] + list(extra_tick) + [
            "execute if score @s %s matches 1.. run function %s/fx/kind" % (self.kind_obj, self.fn),
        ])
        self.w("fx/kind", ["execute if score @s %s matches %d run return run function %s/fx/k/%s" % (self.kind_obj, i, self.fn, n)
                           for n, i in self.ids.items()])
        for name, k in self.kinds.items():
            body = list(k.get("extra", []))
            for at_, ticks, frag in k.get("steps", []):
                body.append("execute if score @s %s matches %d run data merge entity @s "
                            "{start_interpolation:0,interpolation_duration:%d,transformation:{%s}}" % (self.life_obj, at_, ticks, frag))
            if "frames" in k:
                how, seq, count, step = k["frames"]
                for i in range(1, count):
                    at_ = k["life"] - i * step
                    if how == "glyph":
                        body.append("execute if score @s %s matches %d run data modify entity @s text.text set value \"%s\""
                                    % (self.life_obj, at_, art.glyph_text(seq, i)))
                    else:
                        body.append("execute if score @s %s matches %d run data modify entity @s "
                                    "item.components.\"minecraft:item_model\" set value \"%s/%s_%d\"" % (self.life_obj, at_, NS, seq, i))
            self.w("fx/k/%s" % name, body)
