# -*- coding: utf-8 -*-
"""天使长米迦勒与守望者的外观（docs/MICHAEL-DESIGN.md）。

    python add_michael_model.py ../resourcepack ../rpg

米迦勒   _tools/michael_dungeons_ref/（build_michael_model.py）：半透明灵体、六翼、脊骨与双肋骨。
         换装对象：带 rpg.mkwear 的实体（米迦勒战的载体 rpg.mkb）。看标签 rpg.mkm。
           rpg:michael/weapon/{spine,rib}      一阶段脊骨 / 二阶段双肋骨（带 rpg.mk.rib 时待机、走路换双刃版）
           rpg:michael/look/{spirit,solid,fade} 灵体（原样）/ 显形（更实）/ 消散（更淡）；只换没被藏起来的部件
           rpg:michael/wings/burn/<1..6>        六翼燃尽：烧掉一对翼（下、中、上，左右交替）
           rpg:michael/wings/restore            六翼复原
         颜色贴近用户的工程文件（2026-11-18「贴近工程文件，整体调暗一点」）：不开全亮，受正常光照和明暗；
         图集整体不透明度 ×%.1f、颜色 ×%.2f，让贴图本身的颜色压过身后的天空。
守望者   _tools/watchling_dungeons_ref/（dungeons_models.py 的 watchling）：漆黑半透明，十四只圣焰橙红的眼睛。
         换装对象：带 rpg.mkw 的实体，看标签 rpg.mkwm；全亮，眼睛才烧得起来。
"""
import io
import json
import os
import sys

import numpy as np
from PIL import Image

from display_mob import wf, wj
from lord_look import LordLook

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(io.open(os.path.join(HERE, "michael_dungeons_ref", "model_config.json"), encoding="utf-8"))
WINGS = CFG["wings"]
WING_PARTS = CFG["wing_parts"]
WEAPONS = {"spine": ("spine",), "rib": ("rib", "rib_attack")}
LOOKS = {"spirit": None, "solid": "michael_solid", "fade": "michael_fade"}
BRIGHT = "brightness:{sky:15,block:15},"
OPACITY, SHADE = 1.8, 0.7          # 米迦勒图集：不透明度与颜色的倍数
__doc__ = __doc__ % (OPACITY, SHADE)


def ev(*ids):
    return ["minecraft:" + i for i in ids]


# 导出器导不出原作音频，先用原版声音（docs/MICHAEL-DESIGN.md 第 5 节）
SOUNDS = {
    "hurt": (("米迦勒：受击", "Michael is struck"), ev("block.amethyst_block.hit")),
    "death": (("米迦勒：消散", "Michael fades"), ev("block.beacon.deactivate")),
    "flap": (("米迦勒：振翼", "Michael's wings beat"), ev("entity.phantom.flap")),
    "swing": (("脊骨：挥击", "The spine swings"), ev("item.trident.throw")),
    "slash": (("肋骨：斩", "A rib cuts"), ev("entity.player.attack.sweep")),
    "horn": (("米迦勒：吹号", "Michael sounds the trumpet"), ev("item.goat_horn.sound.0")),
    "gong": (("米迦勒：唱诵", "Michael chants"), ev("block.bell.use")),
    "chime": (("米迦勒：圣音", "A holy chime"), ev("block.amethyst_block.resonate")),
}

CLIPS = [("idle", 4, True), ("walk", 2, True), ("run", 2, True),
         ("slash1", 1, False), ("slash2", 1, False), ("sweep", 1, False),
         ("rib_idle", 4, True), ("rib_walk", 2, True), ("rib_run", 2, True)] + \
        [("rib_slash%d" % i, 1, False) for i in range(1, 7)] + \
        [("roll_f", 1, False), ("roll_b", 1, False), ("roll_l", 1, False), ("roll_r", 1, False),
         ("hurt", 1, False), ("fall", 1, False), ("down", 2, True),
         ("mighty", 2, False), ("hero", 2, False), ("kneel", 2, False), ("twirl", 2, False), ("showoff", 1, False),
         ("rise", 1, False), ("land", 1, False), ("stun", 2, True), ("horn", 2, False), ("gong", 2, False),
         ("fold", 2, False)]

LOOK = LordLook(
    key="michael", lord=0, label="米迦勒", tag="rpg.mkm", generator="add_michael_model.py",
    carriers="tag=rpg.mkwear", carrier_type=None, clips=CLIPS, sounds=SOUNDS,
    cues={"walk": [(0.2, "flap", 0.25, 1.2)], "rib_walk": [(0.2, "flap", 0.25, 1.3)],
          "slash1": [(0.25, "swing", 1.0, 1.1)], "slash2": [(0.3, "swing", 1.0, 1.0)], "sweep": [(0.3, "swing", 1.0, 0.8)],
          **{"rib_slash%d" % i: [(0.05, "slash", 0.9, 1.2 + 0.05 * i)] for i in range(1, 7)},
          "roll_f": [(0.05, "flap", 0.8, 0.9)], "roll_b": [(0.05, "flap", 0.8, 0.9)],
          "rise": [(0.1, "flap", 1.0, 0.7)], "fold": [(0.0, "flap", 1.0, 0.6)],
          "horn": [(0.4, "horn", 1.5, 1.0)], "gong": [(0.3, "gong", 1.2, 0.8)], "hero": [(0.2, "chime", 1.0, 0.9)]},
    skills={}, arrive="idle",
)
MOB = LOOK.mob
PARTS = [p for p, _ in MOB.parts]
WEAPON_PARTS = [p for ps in WEAPONS.values() for p in ps]

WATCH = LordLook(
    key="watchling", lord=0, label="守望者", tag="rpg.mkwm", generator="add_michael_model.py",
    carriers="tag=rpg.mkw", carrier_type=None,
    clips=[("idle", 2, True), ("walk", 2, True), ("attack", 1, False), ("heavy", 1, False),
           ("tp_out", 1, False), ("tp_in", 1, False), ("stun", 2, True)],
    sounds={"hurt": (("守望者：受击", "A watcher is struck"), ev("entity.enderman.hurt")),
            "death": (("守望者：熄灭", "A watcher goes dark"), ev("entity.enderman.death")),
            "tp": (("守望者：传送", "A watcher blinks"), ev("entity.enderman.teleport")),
            "swing": (("守望者：挥臂", "A watcher swings"), ev("entity.enderman.scream"))},
    cues={"attack": [(0.4, "swing", 0.6, 1.3)], "heavy": [(0.6, "swing", 0.8, 0.9)],
          "tp_out": [(0.0, "tp", 1.0, 1.0)], "tp_in": [(0.0, "tp", 1.0, 1.2)]},
    skills={}, arrive="tp_in",
)


def func(dp, *path):
    return os.path.join(dp, "data", "rpg", "function", *path) + ".mcfunction"


def brighten(dp, key):
    path = func(dp, key, "dress")
    lines = io.open(path, encoding="utf-8").read().rstrip("\n").split("\n")
    wf(path, [l.replace("view_range:1.5f,", "view_range:1.5f," + BRIGHT) if "summon minecraft:item_display" in l else l
              for l in lines])


# 手里的武器用玩家版的贴图（用户 2026-11-21「手里两把武器使用玩家版本的贴图……适配iris」）：
# 图集里这两块的轮廓和玩家手持贴图逐像素相同，直接贴回去；不透明度只有 0 / 255，光影包下不会半透明排序出错。
# 必须在 tone() 之后贴，solid 版也要贴（fade 版跟着身体一起淡掉）。
WEAPON_ART = {"michael_spine_in_hand": (128, 0), "michael_rib_in_hand": (160, 0)}


def paste_weapons(rp, arr):
    tex = os.path.join(rp, "assets", "rpg", "textures", "item")
    for name, (x, y) in WEAPON_ART.items():
        s = np.array(Image.open(os.path.join(tex, name + ".png")).convert("RGBA")).astype(float)
        h, w_ = s.shape[:2]
        assert ((arr[y:y + h, x:x + w_, 3] > 0) == (s[..., 3] > 0)).all(), "%s 的轮廓和图集对不上" % name
        assert set(np.unique(s[..., 3])) <= {0.0, 255.0}, "%s 有半透明像素" % name
        arr[y:y + h, x:x + w_] = s
    return arr


def tone(rp):
    """Michael's own atlas: more opaque and a little darker, closer to the project as seen in Blockbench."""
    path = os.path.join(rp, "assets", "rpg", "textures", "item", "michael", "atlas.png")
    a = np.array(Image.open(path).convert("RGBA")).astype(float)
    seen = a[..., 3] > 0
    a[..., :3] *= SHADE
    a[..., 3] = np.where(seen, np.minimum(235, a[..., 3] * OPACITY), 0)
    a = paste_weapons(rp, a)
    Image.fromarray(a.clip(0, 255).astype(np.uint8)).save(path)


def variants(rp):
    """atlas_solid / atlas_fade and a copy of every part model and item definition pointing at them."""
    tex = os.path.join(rp, "assets", "rpg", "textures", "item", "michael")
    a = np.array(Image.open(os.path.join(tex, "atlas.png")).convert("RGBA")).astype(float)
    seen = a[..., 3] > 0
    solid, fade = a.copy(), a.copy()
    top = max(a[..., 3][seen].max(), 1)
    solid[..., 3] = np.where(seen, 185 + 55 * a[..., 3] / top, 0)      # ~73%..94%
    fade[..., 3] = np.where(seen, np.maximum(4, a[..., 3] * 0.22), 0)     # ~2%..11%
    solid = paste_weapons(rp, solid)
    for name, arr in (("atlas_solid", solid), ("atlas_fade", fade)):
        Image.fromarray(arr.clip(0, 255).astype(np.uint8)).save(os.path.join(tex, name + ".png"))
    models = os.path.join(rp, "assets", "rpg", "models", "michael")
    for look, folder in LOOKS.items():
        if not folder:
            continue
        atlas = "rpg:item/michael/atlas_" + look
        for part in PARTS:
            m = json.load(io.open(os.path.join(models, part + ".json"), encoding="utf-8"))
            m["textures"] = {"0": atlas, "particle": atlas}
            wj(os.path.join(rp, "assets", "rpg", "models", folder, part + ".json"), m)
            wj(os.path.join(rp, "assets", "rpg", "items", folder, part + ".json"), {
                "model": {"type": "minecraft:model", "model": "rpg:%s/%s" % (folder, part),
                          "tints": [{"type": "minecraft:custom_model_data", "index": 0, "default": 16777215}]}})


def set_model(part, model, keep_hidden=True):
    guard = ' unless data entity @s {item:{components:{"minecraft:item_model":"rpg:empty"}}}' if keep_hidden else ""
    return ('execute on passengers if entity @s[tag=rpg.mkm.p.%s]%s run data modify entity @s '
            'item.components."minecraft:item_model" set value "%s"' % (part, guard, model))


def model_of(look, part):
    return "rpg:%s/%s" % (LOOKS[look] or "michael", part)


def datapack(dp):
    f = lambda *p: func(dp, "michael", *p)
    # looks: only parts that are showing (a hidden weapon or a burnt wing stays hidden)
    for look in LOOKS:
        wf(f("look", look), ["# 米迦勒：%s（as 载体）。由 add_michael_model.py 生成。" % {
            "spirit": "灵体（原样半透明）", "solid": "显形（更实）", "fade": "消散（更淡）"}[look],
            "tag @s remove rpg.mk.solid", "tag @s remove rpg.mk.fade"]
            + (["tag @s add rpg.mk.%s" % look] if look != "spirit" else [])
            + [set_model(p, model_of(look, p)) for p in PARTS])
    # weapons: the visible set gets the spirit model, then the current look is reapplied
    for state, shown in WEAPONS.items():
        lines = ["# 米迦勒手里拿%s（as 载体）。" % {"spine": "脊骨", "rib": "双肋骨"}[state]]
        lines += ["tag @s %s rpg.mk.rib" % ("add" if state == "rib" else "remove")]
        lines += [set_model(p, "rpg:michael/%s" % p if p in shown else "rpg:empty", keep_hidden=False) for p in WEAPON_PARTS]
        lines += ["execute if entity @s[tag=rpg.mk.solid] run function rpg:michael/look/solid",
                  "execute if entity @s[tag=rpg.mk.fade] run function rpg:michael/look/fade",
                  "function rpg:michael/anim/enter/idle"]
        wf(f("weapon", state), lines)
    # wings
    for i, wing in enumerate(WINGS, 1):
        wf(f("wings", "burn", str(i)), ["# 六翼燃尽：烧掉第 %d 片翼（%s）。as 载体。" % (i, wing)]
           + [set_model(p, "rpg:empty", keep_hidden=False) for p in WING_PARTS[wing]])
    wf(f("wings", "restore"), ["# 六翼复原（as 载体）。"]
       + [set_model(p, "rpg:michael/" + p, keep_hidden=False) for w in WINGS for p in WING_PARTS[w]]
       + ["execute if entity @s[tag=rpg.mk.solid] run function rpg:michael/look/solid",
          "execute if entity @s[tag=rpg.mk.fade] run function rpg:michael/look/fade"])
    # stage 2: idle and walk are the dual-blade ones
    ids = {c: i for i, (c, _s, _l) in enumerate(CLIPS)}
    for clip, rib in (("idle", "rib_idle"), ("walk", "rib_walk")):
        path = f("anim", "enter", clip)
        lines = io.open(path, encoding="utf-8").read().rstrip("\n").split("\n")
        lines.insert(1, "execute if entity @s[tag=rpg.mk.rib] run return run function rpg:michael/anim/enter/%s" % rib)
        wf(path, lines)
    path = f("anim", "tick")
    lines = io.open(path, encoding="utf-8").read().rstrip("\n").split("\n")
    at = next(i for i, l in enumerate(lines) if "matches 0 if score" in l)
    lines[at:at] = [
        "execute if score @s rpg_mkm_anim matches %d if score @s rpg_mkm_mv matches 1.. run return run function "
        "rpg:michael/anim/enter/rib_walk" % ids["rib_idle"],
        "execute if score @s rpg_mkm_anim matches %d if score @s rpg_mkm_mv matches 0 run return run function "
        "rpg:michael/anim/enter/rib_idle" % ids["rib_walk"]]
    wf(path, lines)
    # previews
    wf(f("debug", "preview"), [
        "# 预览米迦勒（一个站着不动的载体，不是战斗）。清掉用 /function rpg:michael/debug/clear",
        'summon minecraft:vindicator ~ ~ ~ {Tags:["rpg.mkwear","rpg.mk.preview"],NoAI:1b,Silent:1b,PersistenceRequired:1b,'
        'Invulnerable:1b,active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}'])
    wf(f("debug", "preview_watchling"), [
        "# 预览守望者。清掉用 /function rpg:michael/debug/clear",
        'summon minecraft:vindicator ~ ~ ~ {Tags:["rpg.mkw","rpg.mk.preview"],NoAI:1b,Silent:1b,PersistenceRequired:1b,'
        'Invulnerable:1b,active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}'])
    wf(f("debug", "clear"), ["execute as @e[tag=rpg.mk.preview] run function rpg:michael/debug/clear_one"])
    wf(f("debug", "clear_one"), ["execute on passengers run kill @s", "tp @s ~ -256 ~", "kill @s"])
    for clip, *_r in CLIPS:
        wf(f("debug", "play", clip), [
            "execute as @e[tag=rpg.mkm,tag=rpg.mk.preview,limit=1,sort=nearest] run function rpg:michael/anim/enter/%s" % clip])
    for clip, *_r in WATCH.mob.clips:
        wf(f("debug", "play_watchling", clip), [
            "execute as @e[tag=rpg.mkwm,tag=rpg.mk.preview,limit=1,sort=nearest] run function rpg:watchling/anim/enter/%s" % clip])
    for name in ("spine", "rib"):
        wf(f("debug", "weapon", name), [
            "execute as @e[tag=rpg.mkm,tag=rpg.mk.preview,limit=1,sort=nearest] run function rpg:michael/weapon/%s" % name])
    for look in LOOKS:
        wf(f("debug", "look", look), [
            "execute as @e[tag=rpg.mkm,tag=rpg.mk.preview,limit=1,sort=nearest] run function rpg:michael/look/%s" % look])
    for i in range(1, 7):
        wf(f("debug", "wings", "burn", str(i)), [
            "execute as @e[tag=rpg.mkm,tag=rpg.mk.preview,limit=1,sort=nearest] run function rpg:michael/wings/burn/%d" % i])
    wf(f("debug", "wings", "restore"), [
        "execute as @e[tag=rpg.mkm,tag=rpg.mk.preview,limit=1,sort=nearest] run function rpg:michael/wings/restore"])
    # a fresh look starts with the spine
    path = f("dress")
    lines = io.open(path, encoding="utf-8").read().rstrip("\n").split("\n")
    wf(path, lines + ["function rpg:michael/weapon/spine"])


if __name__ == "__main__":
    rp = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
    dp = sys.argv[2] if len(sys.argv) > 2 else "../rpg"
    LOOK.main(rp, dp)
    WATCH.main(rp, dp)
    brighten(dp, "watchling")        # 守望者全亮：眼睛要烧起来，身体是黑的，亮了也还是黑
    tone(rp)
    variants(rp)
    datapack(dp)
    print("michael look: %d parts (%d wing parts), watchling %d parts" % (
        len(PARTS), sum(len(v) for v in WING_PARTS.values()), len(WATCH.mob.parts)))
