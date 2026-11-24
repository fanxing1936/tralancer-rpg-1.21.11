# -*- coding: utf-8 -*-
"""把 Codex 交付的序章模型（prologue_ref/models/out/）整理成 display_mob 流水线认得的参考目录。

    python prologue_models_prep.py

每个演员一个 `_tools/prologue_<名字>_dungeons_ref/`：<key>.bbmodel、model_config.json、parts.json、glow_bones.json，
由 add_prologue_models.py 在构建时转成展示实体模型与动作函数。Codex 重新交付后再跑一次本脚本即可。

  prologue_michael  序章的米迦勒：Corrupted Defender + 重新解包的实体霜冻甲 + 六翼 + 脊骨（与米迦勒 Boss 同一套骨骼与部件）
  prologue_angel    天使士兵：同一份模型换 Sven 图集，只显示中间一对翼，不拿脊骨
  prologue_lucifer  路西法：Kelptomaniac + 全金属甲 + 蛇枪；被占据形态是另一张图集（atlas_possessed.png），同一套 UV
  prologue_throne   座天使：核心 + 四只眼轮（组名 wheel_up/down/left/right），1 模型像素 = 1 游戏像素
  prologue_beelzebub / prologue_belial / prologue_mammon  三位领主堕落前的天使形态（prefall/，英雄骨架，整套英雄动作 + talk / flee）

部件表：别人的模型沿用原参考目录的 parts.json；路西法和座天使按「每个带方块的组挂到最近的有动画的骨骼上，
能并进那根骨骼的显示就并（自身只绕一个轴转且不超过 45°，中间的组没有旋转），否则单独一个部件」生成。
"""
import base64
import io
import json
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "prologue_ref", "models", "out")


def rj(p):
    with io.open(p, encoding="utf-8") as fh:
        return json.load(fh)


def wj(p, o):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with io.open(p, "w", encoding="utf-8") as fh:
        json.dump(o, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def clips_of(doc):
    return [{"clip": a["name"].split(".", 1)[-1], "seconds": a.get("length", 0)} for a in doc.get("animations", [])]


def tree(doc):
    """name -> {parent, rotation, cubes}"""
    groups = {g["uuid"]: g for g in doc.get("groups", [])}
    info = {}

    def walk(nodes, parent):
        for n in nodes:
            if isinstance(n, dict):
                g = groups.get(n.get("uuid"), n)
                info[g["name"]] = {"parent": parent, "rotation": g.get("rotation", [0, 0, 0]), "cubes": 0}
                walk(n.get("children", []), g["name"])
            elif parent:
                info[parent]["cubes"] += 1
    walk(doc["outliner"], None)
    return info


def animated(doc):
    names = {g["uuid"]: g["name"] for g in doc.get("groups", [])}
    out = set()
    for a in doc.get("animations", []):
        for uid, an in (a.get("animators") or {}).items():
            for kf in an.get("keyframes", []):
                for dp in kf.get("data_points", []):
                    vals = [dp.get(k) for k in ("x", "y", "z")]
                    if any(v not in (None, "", 0, "0", 0.0) and str(v).strip() not in ("0", "0.0", "-0") for v in vals):
                        out.add(an.get("name") or names.get(uid))
    return out


def make_parts(doc, extra_roots=()):
    info, anim = tree(doc), animated(doc) | set(extra_roots)
    rows, separate = {}, []

    def single_axis(rot):
        big = [abs(v) for v in rot if abs(v) > 1e-3]
        return len(big) <= 1 and all(v <= 45 + 1e-3 for v in big)

    for name, g in info.items():
        if not g["cubes"]:
            continue
        owner, between, cur = None, [], name
        while cur:
            if cur in anim or info[cur]["parent"] is None:
                owner = cur
                break
            between.append(cur)
            cur = info[cur]["parent"]
        if owner == name:
            rows.setdefault(owner, [])
            continue
        mids = [b for b in between if b != name]
        if owner and single_axis(g["rotation"]) and all(not any(abs(v) > 1e-6 for v in info[b]["rotation"]) for b in mids):
            rows.setdefault(owner, []).append(name)
        else:
            separate.append(name)
    out = [{"name": b.lower(), "bones": [b] + [m for m in members if m != b]} for b, members in rows.items()]
    out += [{"name": n.lower(), "bones": [n]} for n in separate]
    seen = set()
    for r in out:                      # 部件名要唯一
        base, k = r["name"], 1
        while r["name"] in seen:
            k += 1
            r["name"] = "%s_%d" % (base, k)
        seen.add(r["name"])
    return out


def ref(key):
    return os.path.join(HERE, "prologue_%s_dungeons_ref" % key)


def place(key, doc, cfg, parts, glow=()):
    d = ref(key)
    os.makedirs(d, exist_ok=True)
    wj(os.path.join(d, "prologue_%s.bbmodel" % key), doc)
    cfg = dict(cfg)
    cfg["clips"] = clips_of(doc)
    wj(os.path.join(d, "model_config.json"), cfg)
    wj(os.path.join(d, "parts.json"), parts)
    wj(os.path.join(d, "glow_bones.json"), sorted(glow))
    with io.open(os.path.join(d, "SOURCES.md"), "w", encoding="utf-8") as fh:
        fh.write("# 序章演员 prologue_%s\n\n由 `_tools/prologue_models_prep.py` 从 `prologue_ref/models/out/`（Codex 交付，"
                 "说明见那里的 REPORT.md）整理而来；不要手改，重新交付后再跑一次那个脚本。\n" % key)
    print("prologue_%-10s %3d parts, %2d clips" % (key, len(parts), len(cfg["clips"])))


def main():
    mich_cfg = rj(os.path.join(HERE, "michael_dungeons_ref", "model_config.json"))
    mich_parts = rj(os.path.join(HERE, "michael_dungeons_ref", "parts.json"))

    # 序章的米迦勒：单持脊骨，不显示双肋
    doc = rj(os.path.join(OUT, "michael", "michael_prologue.bbmodel"))
    place("michael", doc, mich_cfg, [p for p in mich_parts if p["name"] not in ("rib", "rib_attack")])

    # 天使士兵：同一份模型换 Sven 图集；只留中间一对翼，不拿武器
    doc = rj(os.path.join(OUT, "michael", "michael_prologue.bbmodel"))
    png = open(os.path.join(OUT, "angel_soldier", "atlas.png"), "rb").read()
    for t in doc["textures"]:
        t["source"] = "data:image/png;base64," + base64.b64encode(png).decode()
    drop = {"rib", "rib_attack", "spine"} | {p["name"] for p in mich_parts
                                              if p["name"].startswith(("wing_upper", "wing_lower"))}
    place("angel", doc, mich_cfg, [p for p in mich_parts if p["name"] not in drop])

    # 路西法：两套外观同一份 UV，被占据的图集另存，由 add_prologue_models.py 做成第二套物品模型
    doc = rj(os.path.join(OUT, "lucifer", "lucifer.bbmodel"))
    place("lucifer", doc, mich_cfg, make_parts(doc, extra_roots=("J_Root",)))
    shutil.copyfile(os.path.join(OUT, "lucifer", "atlas_possessed.png"), os.path.join(ref("lucifer"), "atlas_possessed.png"))

    # 座天使：1 模型像素 = 1 游戏像素；四只眼轮各自是部件，代码按名字把打碎的那只换成空模型
    doc = rj(os.path.join(OUT, "throne", "throne.bbmodel"))
    tcfg = {"model_scale": 1.0, "height_blocks": 2.0, "turn": 0, "merge": {}, "held_bone": None}
    place("throne", doc, tcfg, make_parts(doc, extra_roots=("core", "wheel_up", "wheel_down", "wheel_left", "wheel_right")))

    # 三位领主：堕落前的天使形态（prefall/，英雄骨架 + 路西法侵染形态的三对黑羽，2026-11-22 交付），
    # 部件表按路西法同样的规则生成；配置沿用英雄骨架的缩放
    for key, src in (("beelzebub", "beelzebub"), ("belial", "belial_lord"), ("mammon", "mammon_lord")):
        doc = rj(os.path.join(OUT, src, "prefall", src + "_prefall.bbmodel"))
        place(key, doc, mich_cfg, make_parts(doc, extra_roots=("J_Root",)))

if __name__ == "__main__":
    main()
