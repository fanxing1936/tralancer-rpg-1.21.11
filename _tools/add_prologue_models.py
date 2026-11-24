# -*- coding: utf-8 -*-
"""序章的演员外观、角色装备与过场特效贴图（Codex 交付，prologue_ref/models|art/）。

    python add_prologue_models.py ../resourcepack ../rpg

演员（prologue_models_prep.py 整理出的 prologue_<名字>_dungeons_ref/，走 display_mob 流水线）：
  带 rpg.pr.w.<名字> 的载体自动换装；动作 rpg:prologue_<名字>/anim/enter/<动作>（as 载体）。
  路西法另有被占据外观：rpg:prologue_lucifer/look/possessed 与 look/normal（换图集，同一套 UV；附身图集里蛇枪与
  常态甲件是透明的，暗甲只在附身图集里有像素）。
  座天使：打碎一只眼轮就把那只换成空模型：rpg:prologue_throne/wheel/<up|down|left|right>（as 载体）。
角色装备：四套 equippable 资产 rpg:prologue_<角色>（盔甲层、腿甲层、翅膀层，原版 64×32 格式）。
特效：rpg:prologue_fx/rift_0..7、smoke_0..7、blood_0..3，扁平物品模型（32×32，由序列帧按 REPORT 的坐标切出）。
"""
import io
import json
import os
import sys

from PIL import Image

from display_mob import wf, wj
from lord_look import LordLook

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "prologue_ref", "art")


def ev(*ids):
    return ["minecraft:" + i for i in ids]


STEP = {"sounds": {"step": (("脚步", "Footsteps"), ev("block.chain.step"))}}
HERO_BASE = [("idle", 4, True), ("walk", 2, True), ("run", 2, True)]
# 三位领主堕落前的天使形态（英雄骨架）：整套英雄动作 + talk / flee；贝利尔、玛门另有 showoff / hero / twirl
LORD_CLIPS = HERO_BASE + [("talk", 1, True), ("flee", 1, False), ("fold", 2, False), ("stun", 2, True), ("hurt", 1, False),
                          ("roll_b", 1, False), ("roll_f", 1, False), ("land", 1, False),
                          # Codex 2026-11-22 补的六段（LORD-ACTIONS-BRIEF.md）
                          ("kneel_down", 1, False), ("kneel_idle", 2, True), ("kneel_up", 1, False), ("bow", 1, False),
                          ("look_up", 1, False), ("shield", 1, False)]
LORD_EXTRA = [("showoff", 1, False), ("hero", 2, False), ("twirl", 2, False)]
LORD_HOLD = ("flee", "fold", "kneel_down", "look_up", "shield")

LOOKS = {
    "lucifer": dict(label="路西法（序章）", tag="rpg.prlu",
                    clips=HERO_BASE + [("address", 1, False), ("look_up", 1, False), ("seized", 1, False),
                                       ("pierced", 1, False), ("tear", 1, False), ("reach", 1, False),
                                       ("stomped", 1, False), ("pit_rise", 1, False)],
                    hold=("look_up", "seized", "reach", "stomped", "pit_rise", "tear")),
    "michael": dict(label="米迦勒（序章）", tag="rpg.prmi",
                    clips=HERO_BASE + [("land", 1, False), ("rise", 1, False), ("hero", 2, False), ("hurt", 1, False),
                                       ("slash1", 1, False), ("slash2", 1, False), ("sweep", 1, False), ("fold", 2, False),
                                       ("horn", 2, False), ("gong", 2, False), ("mighty", 2, False), ("kneel", 2, False),
                                       ("stun", 2, True), ("roll_b", 1, False), ("roll_f", 1, False), ("roll_l", 1, False),
                                       ("roll_r", 1, False), ("twirl", 2, False), ("showoff", 1, False), ("fall", 1, False),
                                       ("down", 2, True),
                                       ("dive_cry", 1, False), ("throw", 1, False), ("stomp", 1, False), ("look_down", 1, False)],
                    hold=("dive_cry", "look_down", "rise")),
    "angel": dict(label="天使士兵", tag="rpg.pran",
                  clips=HERO_BASE + [("slash1", 1, False), ("hurt", 1, False)], hold=()),
    "throne": dict(label="座天使", tag="rpg.prth", clips=[("idle", 2, True), ("blink", 1, False)], hold=(), walk="idle"),
    "beelzebub": dict(label="别西卜（序章）", tag="rpg.prbz", clips=LORD_CLIPS, hold=LORD_HOLD),
    "belial": dict(label="贝利尔（序章）", tag="rpg.prbl", clips=LORD_CLIPS + LORD_EXTRA, hold=LORD_HOLD),
    "mammon": dict(label="玛门（序章）", tag="rpg.prmm", clips=LORD_CLIPS + LORD_EXTRA, hold=LORD_HOLD),
}


CUT_ACTORS = ("lucifer", "michael", "beelzebub", "belial", "mammon")
CUT_SCALE = 0.0625


def look(key):
    c = LOOKS[key]
    lk = LordLook(key="prologue_" + key, lord=0, label=c["label"], tag=c["tag"], generator="add_prologue_models.py",
                  carriers="tag=rpg.pr.w.%s" % key, carrier_type=None, clips=c["clips"], sounds=STEP["sounds"],
                  cues={}, skills={}, arrive="idle")
    lk.mob.hold_clips = set(c.get("hold", ()))
    if key in CUT_ACTORS:
        # 过场演员：玩家在旁观模式里会看见隐身载体的半透明人形，所以载体缩到最小（scale 0.0625），
        # 乘客座位高度跟着缩（卫道士 2.0 格 × 0.0625）
        lk.mob.seat = 2.0 * CUT_SCALE
    if c.get("walk"):
        lk.mob.walk_clip = c["walk"]
    return lk


def part_names(rp, key):
    d = os.path.join(rp, "assets", "rpg", "models", "prologue_" + key)
    return sorted(f[:-5] for f in os.listdir(d) if f.endswith(".json"))


def lucifer_possessed(rp, dp):
    """被占据外观：每个部件的模型复制一份，贴图换成 atlas_possessed；look/possessed、look/normal 切换。"""
    src = os.path.join(HERE, "prologue_lucifer_dungeons_ref", "atlas_possessed.png")
    tex = os.path.join(rp, "assets", "rpg", "textures", "item", "prologue_lucifer")
    Image.open(src).save(os.path.join(tex, "atlas_possessed.png"))
    parts = part_names(rp, "lucifer")
    atlas = "rpg:item/prologue_lucifer/atlas_possessed"
    for p in parts:
        m = json.load(io.open(os.path.join(rp, "assets", "rpg", "models", "prologue_lucifer", p + ".json"), encoding="utf-8"))
        m["textures"] = {k: atlas for k in m.get("textures", {})} or {"0": atlas, "particle": atlas}
        wj(os.path.join(rp, "assets", "rpg", "models", "prologue_lucifer_possessed", p + ".json"), m)
        wj(os.path.join(rp, "assets", "rpg", "items", "prologue_lucifer_possessed", p + ".json"),
           {"model": {"type": "minecraft:model", "model": "rpg:prologue_lucifer_possessed/%s" % p}})
    func = os.path.join(dp, "data", "rpg", "function", "prologue_lucifer", "look")
    for name, folder in (("possessed", "prologue_lucifer_possessed"), ("normal", "prologue_lucifer")):
        wf(os.path.join(func, name + ".mcfunction"), ["# 路西法：%s（as 载体）。由 add_prologue_models.py 生成。"
                                                       % ("被敌基督占据" if name == "possessed" else "常态")] +
           ['execute on passengers if entity @s[tag=rpg.prlu.p.%s] run data modify entity @s '
            'item.components."minecraft:item_model" set value "rpg:%s/%s"' % (p, folder, p) for p in parts])
    return len(parts)


def throne_wheels(rp, dp):
    """眼轮由多个部件组成（wheel_<方向> 与 wheel_<方向>_segment_*），打碎时全部换成空模型。"""
    func = os.path.join(dp, "data", "rpg", "function", "prologue_throne", "wheel")
    parts = part_names(rp, "throne")
    for w in ("up", "down", "left", "right"):
        mine = [p for p in parts if p == "wheel_" + w or p.startswith(("wheel_%s_" % w, "blink_wheel_%s_" % w))]   # 含眼睑
        sel = 'execute on passengers if entity @s[tag=rpg.prth.p.%s] run data modify entity @s item.components."minecraft:item_model" set value '
        wf(os.path.join(func, w + ".mcfunction"), ["# 打碎眼轮 %s（as 座天使的载体）：换成空模型" % w] +
           [sel % p + '"rpg:empty"' for p in mine])
        wf(os.path.join(func, "restore_" + w + ".mcfunction"), [sel % p + '"rpg:prologue_throne/%s"' % p for p in mine])


def michael_bridge(rp, dp):
    """序章里打的米迦勒还是米迦勒 Boss（同一套骨骼、部件名与动作名），只是显形外观换成序章模型：
    #pro rpg_mk 为 1 时 rpg:michael/look/solid 改走 look/prologue（被藏起来的部件仍保持空模型；双肋没有序章版，沿用原来的）。"""
    mine = set(part_names(rp, "michael"))
    solid = sorted(f[:-5] for f in os.listdir(os.path.join(rp, "assets", "rpg", "models", "michael_solid")) if f.endswith(".json"))
    func = os.path.join(dp, "data", "rpg", "function", "michael", "look")
    lines = ["# 序章外观（as 米迦勒 Boss 的载体）。由 add_prologue_models.py 生成。"]
    for p in solid:
        model = ("rpg:prologue_michael/%s" % p) if p in mine else ("rpg:michael_solid/%s" % p)
        lines.append('execute on passengers if entity @s[tag=rpg.mkm.p.%s] unless data entity @s {item:{components:'
                     '{"minecraft:item_model":"rpg:empty"}}} run data modify entity @s item.components."minecraft:item_model" '
                     'set value "%s"' % (p, model))
    wf(os.path.join(func, "prologue.mcfunction"), lines)
    path = os.path.join(func, "solid.mcfunction")
    old = io.open(path, encoding="utf-8").read().splitlines()
    hook = "execute if score #pro rpg_mk matches 1 run return run function rpg:michael/look/prologue"
    if hook not in old:
        i = old.index("tag @s add rpg.mk.solid") + 1      # 显形标签照常打上，之后才分流
        wf(path, old[:i] + [hook] + old[i:])


def feather(rp):
    """奖励「米迦勒之羽」：rpg:prologue_feather。Codex 重绘的 prologue_ref/art/feather/feather.png 到了就用它，
    还没到就先沿用米迦勒 Boss 的羽毛贴图。返回用的是哪一张。"""
    new = os.path.join(ART, "feather", "feather.png")
    src = new if os.path.isfile(new) else os.path.join(rp, "assets", "rpg", "textures", "item", "michael_boss", "feather.png")
    Image.open(src).save(os.path.join(_mk(rp, "textures", "item"), "prologue_feather.png"))
    wj(os.path.join(rp, "assets", "rpg", "models", "item", "prologue_feather.json"),
       {"parent": "minecraft:item/generated", "textures": {"layer0": "rpg:item/prologue_feather"}})
    wj(os.path.join(rp, "assets", "rpg", "items", "prologue_feather.json"),
       {"model": {"type": "minecraft:model", "model": "rpg:item/prologue_feather"}})
    return "Codex" if src == new else "placeholder (michael_boss)"


def equipment(rp):
    """四套角色装备：assets/rpg/equipment/prologue_<角色>.json + 三层贴图。"""
    n = 0
    for role in ("lucifer", "beelzebub", "belial", "mammon"):
        for layer, f in (("humanoid", "humanoid"), ("humanoid_leggings", "leggings"), ("wings", "wings")):
            dst = os.path.join(rp, "assets", "rpg", "textures", "entity", "equipment", layer, "prologue_%s.png" % role)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            Image.open(os.path.join(ART, "pixel", "%s_%s.png" % (role, f))).save(dst)
            n += 1
        wj(os.path.join(rp, "assets", "rpg", "equipment", "prologue_%s.json" % role), {"layers": {
            "humanoid": [{"texture": "rpg:prologue_%s" % role}],
            "humanoid_leggings": [{"texture": "rpg:prologue_%s" % role}],
            "wings": [{"texture": "rpg:prologue_%s" % role}]}})
    return n


def fx(rp):
    """序列帧切成 32×32（坐标见 prologue_ref/art/fx/REPORT.md），做成扁平的物品模型。"""
    out = []
    for sheet, name, n, cell, x0, dx, y0 in (("rift_sheet.png", "rift", 8, 224, 24, 270, 246),
                                             ("green_smoke_sheet.png", "smoke", 8, 224, 24, 270, 246),
                                             ("blood_decals.png", "blood", 4, 448, 48, 543, 146)):
        im = Image.open(os.path.join(ART, "fx", sheet)).convert("RGBA")
        for i in range(n):
            tile = im.crop((x0 + dx * i, y0, x0 + dx * i + cell, y0 + cell)).resize((32, 32), Image.NEAREST)
            px = tile.load()
            for y in range(32):
                for x in range(32):
                    r, g, b, a = px[x, y]
                    px[x, y] = (r, g, b, 255 if a >= 128 else 0)
            tid = "%s_%d" % (name, i)
            tile.save(os.path.join(_mk(rp, "textures", "item", "prologue_fx"), tid + ".png"))
            wj(os.path.join(rp, "assets", "rpg", "models", "prologue_fx", tid + ".json"),
               {"parent": "minecraft:item/generated", "textures": {"layer0": "rpg:item/prologue_fx/" + tid}})
            wj(os.path.join(rp, "assets", "rpg", "items", "prologue_fx", tid + ".json"),
               {"model": {"type": "minecraft:model", "model": "rpg:prologue_fx/" + tid}})
            out.append(tid)
    return len(out)


def _mk(rp, *p):
    d = os.path.join(rp, "assets", "rpg", *p)
    os.makedirs(d, exist_ok=True)
    return d


def main():
    rp = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
    dp = sys.argv[2] if len(sys.argv) > 2 else "../rpg"
    counts = {}
    for key in LOOKS:
        lk = look(key)
        lk.main(rp, dp)
        counts[key] = len(lk.mob.parts)
    np_ = lucifer_possessed(rp, dp)
    throne_wheels(rp, dp)
    michael_bridge(rp, dp)
    neq = equipment(rp)
    nfx = fx(rp)
    print("prologue feather: %s" % feather(rp))
    print("prologue models: %s; lucifer possessed %d parts; equipment %d textures; fx %d frames"
          % (", ".join("%s %d" % kv for kv in counts.items()), np_, neq, nfx))


if __name__ == "__main__":
    main()
