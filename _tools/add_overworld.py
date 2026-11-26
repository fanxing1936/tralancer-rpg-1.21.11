# -*- coding: utf-8 -*-
"""主世界重做：19 个自定义群系的破碎大陆（10000×10000，外面是海），纯装饰地形。

用户决定（2026-11-26）：只生成这些群系、不保留任何原版结构（要塞也去掉）、没有矿物和任何洞穴、
主世界高度上限 1024、设世界边界、直接覆盖老存档的主世界。
地形与群系：overworld_world.py；大树（Planet Minecraft 公开树包，署名见 tree_ref/CREDITS.md）：overworld_trees.py。

用法：python add_overworld.py ../rpg ../resourcepack
"""
import io, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import overworld_world as OW  # noqa: E402

NS = "rpg"


def hook_load(rpg, entry):
    p = os.path.join(rpg, "data", "minecraft", "tags", "function", "load.json")
    doc = json.load(io.open(p, encoding="utf-8")) if os.path.exists(p) else {"replace": False, "values": []}
    if entry not in doc["values"]:
        doc["values"].append(entry)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with io.open(p, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def main(rpg, rp=None):
    n = OW.write(rpg)
    hook_load(rpg, "%s:overworld/border" % NS)
    msg = "overworld: %d worldgen files + grove templates; load hooks rpg:overworld/border" % n
    if rp:
        import overworld_trees, mc_env
        overworld_trees.yellow_leaves(rp, mc_env.JAR)
        msg += "; pale_oak_leaves -> yellow"
    print(msg)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
