# -*- coding: utf-8 -*-
"""路西法二阶段用到的原作静态道具：单个 item_display 就能显示的物品模型。

    python add_lucifer_props.py ../resourcepack

从本体提取，经 dungeons_conversion/generic.py 转换，对照图在 lucifer_props_ref/<名>/：

    quill  Dungeons/Content/Actors/Characters/Enemies/PoisonQuillVine/PoisonQuillVine_Quill
           树的毒刺弹（BP_JungleAbominationPoisonProj 用的网格），用作「禁果」「失乐园」的果核。
           模型以中心为原点，刺尖朝模型 +y；飞行时把 +y 转到实体前方（见 QUILL_ROTATION）。
    spike  Dungeons/Content/Effects/Flairs/RespawnFlairs/02/SM_Abomination_Vine
           原作藤臂的静态版，用作「失乐园」三圈破土的尖根。模型底部在原点，向上长。

显示尺寸与二阶段同一系数（0.0086339 格/厘米），所以 SCALE 就是二阶段的 model_scale。
"""

import json
import os
import shutil
import sys

import display_mob as dm

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "lucifer_props_ref")
KEY = "lucifer_props"
SCALE = 7.1949189027950968
QUILL_ROTATION = (0.7071068, 0, 0, 0.7071068)   # 绕 x 转 90°：模型 +y（刺尖）→ 实体前方 +z
PROPS = {"quill": "center", "spike": "base"}


def prop_model(name, anchor, rp):
    ref = os.path.join(REF, name)
    parts = json.load(open(os.path.join(ref, "parts.json"), encoding="utf-8"))
    if len(parts) != 1:
        raise SystemExit("%s: a prop must convert to one part, got %d" % (name, len(parts)))
    mob = dm.Mob(key=KEY, label=name, generator="add_lucifer_props.py",
                 bbmodel=os.path.join(ref, "lucifer_%s.bbmodel" % name),
                 parts=[(parts[0]["name"], parts[0]["bones"])],
                 glow=set(json.load(open(os.path.join(ref, "glow_bones.json"), encoding="utf-8"))),
                 seat=0, tag="rpg.lup", score="rpg_lup", clips=[], face_rotation=True)
    mob.paths(rp, rp)
    mob.tex = "rpg:item/%s/%s" % (KEY, name)
    bones, png, res = dm.load_bbmodel(mob)
    model, _k = dm.part_model(mob, bones, parts[0]["name"], parts[0]["bones"], res)
    # part_model centres the box on (8,8,8); a planted prop moves its base down to y=8 instead
    if anchor == "base":
        low = min(min(e["from"][1], e["to"][1]) for e in model["elements"])
        shift = 8 - low
        for e in model["elements"]:
            e["from"][1] = round(e["from"][1] + shift, 4)
            e["to"][1] = round(e["to"][1] + shift, 4)
            if "rotation" in e:
                e["rotation"]["origin"][1] = round(e["rotation"]["origin"][1] + shift, 4)
    tex = os.path.join(rp, "assets", "rpg", "textures", "item", KEY, name + ".png")
    os.makedirs(os.path.dirname(tex), exist_ok=True)
    with open(tex, "wb") as fh:
        fh.write(png)
    dm.wj(os.path.join(rp, "assets", "rpg", "models", KEY, name + ".json"), model)
    dm.wj(os.path.join(rp, "assets", "rpg", "items", KEY, name + ".json"), {
        "model": {"type": "minecraft:model", "model": "rpg:%s/%s" % (KEY, name),
                  "tints": [{"type": "minecraft:custom_model_data", "index": 0, "default": 16777215}]}})
    return len(model["elements"])


def main():
    rp = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "resourcepack")
    for sub in ("models", "items"):
        shutil.rmtree(os.path.join(rp, "assets", "rpg", sub, KEY), ignore_errors=True)
    counts = {name: prop_model(name, anchor, rp) for name, anchor in PROPS.items()}
    print("lucifer props: %s" % ", ".join("%s %d elements" % kv for kv in counts.items()))


if __name__ == "__main__":
    main()
