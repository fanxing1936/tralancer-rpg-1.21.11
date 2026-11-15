#!/usr/bin/env python3
"""检查点 A：只校验/导出静态模型，不创建或烘焙任何动画、数据包函数。

用法：python _tools/lucifer_ref/validate_static.py --out <隔离目录>
输入：旁边的 lucifer.bbmodel 与 static_config.json。
导出使用原 display_mob 的几何和矩阵函数；不会修改该管线。
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import math
from pathlib import Path
import sys
import zipfile

from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(HERE.parent))
import display_mob as dm


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def numeric_vector(value, length, label):
    assert len(value) == length, f"{label}: expected {length} numbers"
    assert all(isinstance(v, (int, float)) and not isinstance(v, bool)
               and math.isfinite(v) for v in value), f"{label}: nonnumeric/nonfinite value"


def weapon_reference():
    """读取现有蛇矛和原版 parent，仅供预览，不生成/修改武器资产。"""
    from mc_env import JAR
    item_path = REPO / "resourcepack/assets/rpg/models/item/lucifer_in_hand.json"
    texture_path = REPO / "resourcepack/assets/rpg/textures/item/lucifer_in_hand.png"
    item = json.loads(item_path.read_text(encoding="utf-8"))
    parent_path = "assets/minecraft/models/item/spear_in_hand.json"
    with zipfile.ZipFile(JAR) as jar:
        parent_bytes = jar.read(parent_path)
    parent = json.loads(parent_bytes)
    image = Image.open(texture_path).convert("RGBA")
    transform = parent["display"]["thirdperson_righthand"]
    scaling = dm.ident()
    for axis, value in enumerate(transform["scale"]):
        scaling[axis][axis] = value
    x, y, z = transform["rotation"]
    # ItemTransform uses Quaternionf.rotationXYZ; bone matrices use ZYX.
    item_matrix = dm.mat_mul(dm.translate(*[v / 16 for v in transform["translation"]]),
                            dm.mat_mul(dm.rot_x(x), dm.mat_mul(dm.rot_y(y),
                            dm.mat_mul(dm.rot_z(z), scaling))))
    return {
        "model_path": str(item_path), "texture_path": str(texture_path),
        "texture_size": list(image.size),
        "texture_sha256": hashlib.sha256(texture_path.read_bytes()).hexdigest(),
        "model": item, "parent_jar": JAR, "parent_entry": parent_path,
        "parent_sha256": hashlib.sha256(parent_bytes).hexdigest(),
        "parent": parent,
        "display_context": "thirdperson_righthand",
        "thirdperson_transform": parent["display"]["thirdperson_righthand"],
        "thirdperson_matrix": item_matrix,
        "generated_model_center_matrix": dm.mat_mul(dm.scale(1 / 16), dm.translate(-8, -8, -8)),
        "preview_matrix_rule": (
            "Java rig coordinates = bone_matrix(right_arm) * translate(right_arm pivot) "
            "* VANILLA * HOLD * thirdperson_matrix * generated_model_center_matrix "
            "* generated sprite model coordinates."),
        "preview_geometry_note": (
            "parent=item/generated 没有存储 elements；客户端依 layer0 alpha 生成正反面和边缘。"
            "预览应使用现有 PNG 的 0..16 方形、y=16-v*16、z=7.5..8.5；"
            "以 (8,8,8) 为中心，应用第三人称 transform 再套 held 矩阵。"
            "不要写回或替换 add_lucifer.py 的武器模型。"),
        "hold_matrix": dm.HOLD, "vanilla_axis_matrix": dm.VANILLA,
    }


def validate(config_path, model_path, out):
    config = json.loads(config_path.read_text(encoding="utf-8"))
    doc = json.loads(model_path.read_text(encoding="utf-8"))
    assert not doc.get("animations"), "检查点 A 不允许用占位 clip 冒充动作"
    assert config["key"] == "lucifer_lord"
    assert config["tag"] == "rpg.lu"
    assert config["score"] == "rpg_lu"
    assert config.get("held", "weapon") == "weapon"
    assert config["seat"] == 2.0
    parts = config["parts"]
    if isinstance(parts, dict):
        parts = list(parts.items())
    assert len(parts) <= 12, f"部件数 {len(parts)} 超过 12"
    assert len({name for name, _ in parts}) == len(parts), "重复部件名"
    assert "weapon" in {name for name, _ in parts}
    assert next(members for name, members in parts if name == "weapon") == ["right_arm"]
    assert len({g["name"] for g in doc["groups"]}) == len(doc["groups"]), "骨骼名不唯一"
    source = doc["textures"][0]["source"]
    assert source.startswith("data:image/png;base64,"), "textures[0] 必须内嵌 PNG 图集"
    atlas = base64.b64decode(source.split(",", 1)[1], validate=True)
    image = Image.open(io.BytesIO(atlas))
    assert image.size == (doc["resolution"]["width"], doc["resolution"]["height"])
    for group in doc["groups"]:
        numeric_vector(group["origin"], 3, group["name"] + ".origin")
        numeric_vector(group.get("rotation", [0, 0, 0]), 3, group["name"] + ".rotation")
    faces = 0
    for element in doc["elements"]:
        name = element.get("name", element["uuid"])
        numeric_vector(element["from"], 3, name + ".from")
        numeric_vector(element["to"], 3, name + ".to")
        assert all(a <= b for a, b in zip(element["from"], element["to"])), name
        assert not any(element.get("rotation", [0, 0, 0])), f"{name}: 元素旋转不被 part_model 读取"
        for face, data in element["faces"].items():
            if data.get("texture") is None:
                continue
            assert data["texture"] in (0, doc["textures"][0].get("uuid")), f"{name}/{face}: 非 textures[0]"
            numeric_vector(data["uv"], 4, name + "/" + face)
            assert not data.get("rotation", 0), f"{name}/{face}: 面 UV rotation 不被管线读取"
            u0, v0, u1, v1 = data["uv"]
            assert 0 <= min(u0, u1) <= max(u0, u1) <= image.width, name + "/" + face
            assert 0 <= min(v0, v1) <= max(v0, v1) <= image.height, name + "/" + face
            faces += 1
    mob = dm.Mob(key=config["key"], label="路西法", generator="validate_static.py",
                 bbmodel=str(model_path), parts=parts, glow=config.get("glow", []),
                 model_scale=config["model_scale"], seat=config["seat"],
                 tag=config["tag"], score=config["score"], clips=[], held="weapon")
    bones, original_atlas, resolution = dm.load_bbmodel(mob)
    assert atlas == original_atlas
    used = [bone for part, members in parts if part != mob.held for bone in members]
    assert len(used) == len(set(used)), "几何骨骼重复合并进多个部件"
    uncovered = [name for name, bone in bones.items() if bone["cubes"] and name not in used]
    assert not uncovered, f"有几何未包含进任何部件：{uncovered}"
    models = []
    for part, members in parts:
        assert members and all(name in bones for name in members), part
        W = dm.bone_matrix(bones, members[0])
        if part == mob.held:
            matrix = dm.held_matrix(mob, bones, members[0], W)
            models.append({"name": part, "bones": members, "held": True,
                           "display_matrix": matrix, "components": dm.components(matrix, mob.model_scale)})
            continue
        for name in members[1:]:
            assert members[0] in dm.chain(bones, name), f"{part}/{name}: 不是主骨骼的子骨骼"
            rotation = bones[name]["rotation"]
            assert sum(bool(v) for v in rotation) <= 1, f"{part}/{name}: 多轴子骨骼旋转"
            assert all(abs(v) <= 45 for v in rotation), f"{part}/{name}: 子骨骼旋转超过 45 度"
        model, offset = dm.part_model(mob, bones, part, members, resolution)
        assert model["elements"], f"{part}: 空几何部件"
        matrix = dm.display_matrix(mob, bones, members[0], offset, W)
        write_json(out / "resourcepack/assets/rpg/models/lucifer_lord" / (part + ".json"), model)
        write_json(out / "resourcepack/assets/rpg/items/lucifer_lord" / (part + ".json"), {
            "model": {"type": "minecraft:model", "model": "rpg:lucifer_lord/" + part,
                      "tints": [{"type": "minecraft:custom_model_data", "index": 0, "default": 16777215}]}})
        models.append({"name": part, "bones": members, "held": False, "offset": offset,
                       "elements": len(model["elements"]),
                       "glow_elements": sum(e.get("light_emission", 0) == 15 for e in model["elements"]),
                       "display_matrix": matrix, "components": dm.components(matrix, mob.model_scale)})
    atlas_path = out / "resourcepack/assets/rpg/textures/item/lucifer_lord/atlas.png"
    atlas_path.parent.mkdir(parents=True, exist_ok=True)
    atlas_path.write_bytes(atlas)
    result = {
        "scope": "checkpoint_A_static_only", "status": "passed", "animation_count": 0,
        "runtime_functions_generated": 0, "part_count": len(parts),
        "element_count": len(doc["elements"]), "textured_face_count": faces,
        "atlas_size": list(image.size), "atlas_sha256": hashlib.sha256(atlas).hexdigest(),
        "bbmodel_sha256": hashlib.sha256(model_path.read_bytes()).hexdigest(),
        "config_sha256": hashlib.sha256(config_path.read_bytes()).hexdigest(),
        "model_scale": mob.model_scale, "seat": mob.seat, "parts": models,
        "not_verified": ["真实游戏内外观", "动态换装", "动作与技能", "载体移除/十分钟消散/驱魔后的运行时清理"],
    }
    write_json(out / "static_validation.json", result)
    write_json(out / "weapon_reference.json", weapon_reference())
    print(json.dumps({k: result[k] for k in ["scope", "status", "part_count", "element_count", "textured_face_count", "atlas_size"]}, ensure_ascii=False))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=HERE / "static_config.json")
    parser.add_argument("--model", type=Path, default=HERE / "lucifer.bbmodel")
    parser.add_argument("--out", type=Path, required=True, help="隔离导出目录，不允许指向仓库本身")
    args = parser.parse_args()
    output = args.out.resolve()
    assert output != REPO and output != REPO / "resourcepack", "不能覆盖共享仓库资源包"
    validate(args.config.resolve(), args.model.resolve(), output)
