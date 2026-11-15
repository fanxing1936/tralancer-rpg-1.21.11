#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""教皇 M2 静态模型的独立、只读验证。

仅报告写入 pope_ref/m2/validation；不调用 display_mob.build，不生成资源包。
模型/贴图/来源记录必须先存在。检查采用实际保存后的 .bbmodel，不以制作输入代替。
"""
import base64
from collections import Counter
import hashlib
import io
import json
import math
from pathlib import Path
import sys
from types import SimpleNamespace

sys.dont_write_bytecode = True

from PIL import Image

import display_mob

HERE = Path(__file__).resolve().parent
REF = HERE / "pope_ref"
M2 = REF / "m2"
OUTPUT = M2 / "validation"


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(value, message):
    if not value:
        raise ValueError(message)


def numeric_vector(value, length):
    return (isinstance(value, list) and len(value) == length
            and all(isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) for x in value))


def transform_pixels(image, operation):
    operations = {
        "identity": None,
        "rotate90_cw": Image.Transpose.ROTATE_270,
        "rotate180": Image.Transpose.ROTATE_180,
        "rotate270_cw": Image.Transpose.ROTATE_90,
        "flip_h": Image.Transpose.FLIP_LEFT_RIGHT,
        "flip_v": Image.Transpose.FLIP_TOP_BOTTOM,
    }
    require(operation in operations, "不支持的可追溯像素变换：" + str(operation))
    return image.copy() if operations[operation] is None else image.transpose(operations[operation])


def normalized_rect(rect, width, height, label):
    require(numeric_vector(rect, 4), label + " 不是4个有限数值")
    x0, y0, x1, y1 = rect
    require(x0 != x1 and y0 != y1, label + " 面积为零")
    result = [min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)]
    require(0 <= result[0] < result[2] <= width and 0 <= result[1] < result[3] <= height,
            label + " 越界：" + str(rect))
    return result


def check_texture(doc):
    textures = doc.get("textures", [])
    require(len(textures) == 1, "必须恰好1张纹理，由 textures[0] 读取")
    source = textures[0].get("source", "")
    require(source.startswith("data:image/png;base64,"), "textures[0].source 必须内嵌 PNG base64")
    binary = base64.b64decode(source.split(",", 1)[1], validate=True)
    require(binary.startswith(b"\x89PNG\r\n\x1a\n"), "内嵌贴图签名不是PNG")
    with Image.open(io.BytesIO(binary)) as im:
        im.verify()
    image = Image.open(io.BytesIO(binary)).convert("RGBA")
    resolution = doc.get("resolution", {})
    require([resolution.get("width"), resolution.get("height")] == list(image.size), "模型分辨率与PNG尺寸不一致")
    for key, size in (("width", image.width), ("height", image.height),
                      ("uv_width", image.width), ("uv_height", image.height)):
        if key in textures[0]:
            require(textures[0][key] == size, "纹理字段 %s 与 PNG 尺寸不一致" % key)
    return image, {"png_sha256": sha256(binary), "rgba_sha256": sha256(image.tobytes()), "size": list(image.size)}


def source_path(value):
    path = Path(value)
    if not path.is_absolute():
        path = HERE.parent / path if value.replace("\\", "/").startswith("_tools/") else REF / path
    path = path.resolve()
    allowed = {
        (HERE / "heart_of_ender_ref" / "MCD_Arch-Illager_(texture).png").resolve(),
        (REF / "T_SuperStaff.png").resolve(),
        (REF / "T_SuperCube.png").resolve(),
    }
    require(path in allowed, "图集引用不在本次指定的三张原始材质中：" + str(path))
    return path


def check_atlas_sources(atlas, placements):
    require(placements, "图集必须有来源布局记录")
    expected = Image.new("RGBA", atlas.size, (0, 0, 0, 0))
    covered = Image.new("1", atlas.size, 0)
    reports = []
    full_arch_preserved = False
    for item in placements:
        path = source_path(item["source_file"])
        original = Image.open(path).convert("RGBA")
        source_rect = normalized_rect(item["source_rect"], *original.size, "原始裁片")
        dest_rect = normalized_rect(item["atlas_rect"], *atlas.size, "图集放置")
        require(all(float(x).is_integer() for x in source_rect + dest_rect), "图集拼贴必须在整数像素边界")
        source_rect, dest_rect = list(map(int, source_rect)), list(map(int, dest_rect))
        op = item.get("transform", "identity")
        transformed = transform_pixels(original.crop(source_rect), op)
        require(transformed.size == (dest_rect[2] - dest_rect[0], dest_rect[3] - dest_rect[1]),
                "图集来源尺寸不符；不允许缩放或滤波")
        require(atlas.crop(dest_rect).tobytes() == transformed.tobytes(), "图集像素与原裁片不一致：" + path.name)
        occupied = covered.crop(dest_rect)
        if occupied.getbbox():
            old = expected.crop(dest_rect)
            for y in range(transformed.height):
                for x in range(transformed.width):
                    require(not occupied.getpixel((x, y)) or old.getpixel((x, y)) == transformed.getpixel((x, y)),
                            "图集不同来源覆盖冲突")
        expected.paste(transformed, tuple(dest_rect[:2]))
        covered.paste(1, tuple(dest_rect))
        if path.name == "MCD_Arch-Illager_(texture).png" and source_rect == [0, 0, 64, 64] and op == "identity":
            full_arch_preserved = True
        reports.append({"source_file": str(path), "source_png_sha256": sha256(path.read_bytes()),
                        "source_rect": source_rect, "atlas_rect": dest_rect, "transform": op,
                        "rgba_sha256": sha256(transformed.tobytes())})
    require(full_arch_preserved, "必须将64×64人物原图完整1:1保留在单图集")
    require(expected.tobytes() == atlas.tobytes(), "图集存在未登记像素，或未使用区不是全透明黑")
    return reports


def check_structure(doc):
    require(not doc.get("animations"), "M2静态阶段不得包含动画")
    groups, elements = doc.get("groups", []), doc.get("elements", [])
    require(groups and elements, "必须有骨骼和元素")
    all_ids = [x["uuid"] for x in groups + elements]
    require(len(set(all_ids)) == len(all_ids), "UUID重复")
    require(len({g["name"] for g in groups}) == len(groups), "骨骼名称重复")
    group_by_id = {g["uuid"]: g for g in groups}
    element_by_id = {e["uuid"]: e for e in elements}
    seen_groups, seen_elements = [], []

    def walk(node):
        require(isinstance(node, dict) and node.get("uuid") in group_by_id, "outliner 有未知骨骼")
        gid = node["uuid"]
        require(gid not in seen_groups, "outliner 骨骼重复或循环")
        seen_groups.append(gid)
        for child in node.get("children", []):
            if isinstance(child, str):
                require(child in element_by_id, "outliner 有未知元素")
                seen_elements.append(child)
            else:
                walk(child)

    for root in doc.get("outliner", []):
        walk(root)
    require(set(seen_groups) == set(group_by_id), "存在未入层级的骨骼")
    require(Counter(seen_elements) == Counter(element_by_id.keys()), "元素未唯一归属骨骼")
    for group in groups:
        require(numeric_vector(group.get("origin"), 3), "骨骼枢轴必须为有限数值")
        require(numeric_vector(group.get("rotation", [0, 0, 0]), 3), "骨骼旋转必须为有限数值")
    width, height = doc["resolution"]["width"], doc["resolution"]["height"]
    face_count = 0
    for element in elements:
        require(element.get("type", "cube") == "cube", "只接受立方体元素")
        require(numeric_vector(element.get("from"), 3) and numeric_vector(element.get("to"), 3), "元素端点不是有限数值")
        require(all(a <= b for a, b in zip(element["from"], element["to"])), "元素from/to倒置")
        require(all(abs(v) < 1e-9 for v in element.get("rotation", [0, 0, 0])), "元素旋转不会由共享管线读取")
        for face, details in element.get("faces", {}).items():
            require(face in ("north", "south", "east", "west", "up", "down"), "未知面名")
            if details.get("texture") is None:
                continue
            require(details["texture"] in (0, "0"), "仅可引用 textures[0]")
            require(details.get("rotation", 0) == 0, "face.rotation不会由共享管线转存")
            normalized_rect(details["uv"], width, height, element["name"] + "/" + face)
            face_count += 1
    return {"groups": len(groups), "elements": len(elements), "visible_faces": face_count, "animations": 0}


def check_parts(bbmodel, doc, parts, glow):
    require(1 <= len(parts) <= 12, "display部件数须为1..12")
    require(len({p[0] for p in parts}) == len(parts), "display部件名称重复")
    mob = SimpleNamespace(bbmodel=str(bbmodel), key="pope", tex="rpg:item/pope/atlas", glow=set(glow))
    bones, _, resolution = display_mob.load_bbmodel(mob)
    part_roots = {members[0] for _, members in parts if members}
    require({"crown", "staff", "staff_glow"}.issubset(part_roots), "皇冠/权杖/发光必须各有独立运动部件")
    require(bones["staff"]["parent"] == "left_hand", "权杖应跟随已核实的角色左手")
    require(bones["staff_glow"]["parent"] == "staff", "发光部分应跟随权杖")
    require(set(glow) == {"staff_glow"}, "当前有来源证据的发光仅为staff_glow")
    assignments = Counter()
    reports = []
    for part, members in parts:
        require(members and all(n in bones for n in members), "部件包含未知或空骨骼列表：" + part)
        root = members[0]
        require(bool(sum((bones[n]["cubes"] for n in members), [])), "不能生成空display部件：" + part)
        for name in members:
            assignments.update(c["uuid"] for c in bones[name]["cubes"])
            if name == root:
                continue
            require(root in display_mob.chain(bones, name), "合并骨骼必须是首骨骼的后代：" + name)
            rotation = bones[name]["rotation"]
            nonzero = [v for v in rotation if abs(v) > 1e-9]
            require(len(nonzero) <= 1 and all(abs(v) <= 45 for v in nonzero), "合并子骨骼旋转超出单轴±45°：" + name)
            rel = display_mob.bone_matrix(bones, name, stop=root)
            single = display_mob.about(bones[name]["pivot"], rotation)
            require(all(abs(rel[i][j] - single[i][j]) < 1e-8 for i in range(4) for j in range(4)),
                    "合并子骨骼存在不可由管线单元素旋转表达的祖先旋转：" + name)
        try:
            output, offset = display_mob.part_model(mob, bones, part, members, resolution)
        except SystemExit as exc:
            raise ValueError(str(exc)) from exc
        values = [v for e in output["elements"] for key in ("from", "to") for v in e[key]]
        require(all(-16 <= v <= 32 for v in values), "输出部件坐标越界：" + part)
        reports.append({"part": part, "bones": members, "elements": len(output["elements"]),
                        "center_offset": offset, "coordinate_min": min(values), "coordinate_max": max(values)})
    require(assignments == Counter(e["uuid"] for e in doc["elements"]), "元素没有恰好进入一个display部件")
    require(set(glow).issubset(bones), "glow包含未知骨骼")
    return bones, reports


def posed_bounds(bones, names):
    points = []
    for name in names:
        require(name in bones, "身高测量使用未知骨骼：" + name)
        matrix = display_mob.bone_matrix(bones, name)
        for element in bones[name]["cubes"]:
            inflation = element.get("inflate", 0)
            for corner in range(8):
                point = [element["to"][k] + inflation if corner & (1 << k)
                         else element["from"][k] - inflation for k in range(3)]
                points.append([sum(matrix[i][k] * point[k] for k in range(3)) + matrix[i][3] for i in range(3)])
    require(points, "身高测量没有几何")
    return [min(p[k] for p in points) for k in range(3)], [max(p[k] for p in points) for k in range(3)]


def check_metadata(doc, spec, model_hash):
    for key, value in {"stage": "M2_static", "key": "pope", "label": "教皇", "tag": "rpg.pope", "score": "rpg_pp"}.items():
        require(spec.get(key) == value, "固定字段不匹配：" + key)
    require(spec.get("model_sha256") == model_hash, "spec记录的模型SHA-256与当前.bbmodel不符")
    actual = {g["name"]: g for g in doc["groups"]}
    mismatches = []
    for entry in spec.get("groups", []):
        group = actual.get(entry["name"])
        if not group:
            mismatches.append(entry["name"] + ":骨骼不存在")
            continue
        for field, default in (("uuid", None), ("origin", None), ("rotation", [0, 0, 0])):
            if entry.get(field, default) != group.get(field, default):
                mismatches.append(entry["name"] + ":" + field)
    element_ids = {e["name"]: e["uuid"] for e in doc["elements"]}
    for entry in spec.get("elements", []):
        if element_ids.get(entry["name"]) != entry["uuid"]:
            mismatches.append(entry["name"] + ":element_uuid")
    require(not mismatches, "spec与保存后模型元数据不一致，共%d项：%s" % (len(mismatches), ", ".join(mismatches[:20])))
    return {"fixed_fields": True, "model_hash_matches": True, "saved_uuid_matches": True}


def check_face_provenance(doc, atlas, rows, check_uuids=True):
    require(isinstance(rows, list), "face_provenance必须为逐面列表")
    elements = {e["uuid"]: e for e in doc["elements"]}
    by_name = {e["name"]: e for e in doc["elements"]}
    require(len(by_name) == len(doc["elements"]), "元素名必须唯一，以便核对来源")
    recorded = set()
    mismatch = []
    decoded_sources = {}
    for row in rows:
        name, face = row["element_name"], row["face"]
        require((name, face) not in recorded, "来源记录重复：" + name + "/" + face)
        recorded.add((name, face))
        require(name in by_name, "来源记录引用未知元素：" + name)
        element = by_name[name]
        if row.get("element_uuid") != element["uuid"]:
            mismatch.append(name + "/" + face)
        details = element["faces"].get(face)
        require(details and details.get("texture") is not None, "来源记录引用不存在或跳过的面：" + name + "/" + face)
        require(details["uv"] == row["atlas_uv"], "来源UV与实际模型面不符：" + name + "/" + face)
        require(bool(row.get("flip_u", False)) == (details["uv"][2] < details["uv"][0]), "flip_u与UV端点方向不符")
        require(bool(row.get("flip_v", False)) == (details["uv"][3] < details["uv"][1]), "flip_v与UV端点方向不符")
        require(row.get("note") and row.get("status"), "每面必须保留取样理由与证据状态")
        path = source_path(row["source_file"])
        if path not in decoded_sources:
            decoded_sources[path] = Image.open(path).convert("RGBA")
        source = decoded_sources[path]
        rect = normalized_rect(row["source_rect"], *source.size, name + "/source")
        target = normalized_rect(row["atlas_uv"], *atlas.size, name + "/atlas")
        require(all(float(v).is_integer() for v in rect + target), "来源逐面矩形目前须为整数像素")
        pixels = transform_pixels(source.crop(list(map(int, rect))), row.get("transform", "identity"))
        actual = atlas.crop(list(map(int, target)))
        require(pixels.size == actual.size and pixels.tobytes() == actual.tobytes(),
                "逐面图集像素与原裁片变换不符：" + name + "/" + face)
    visible = {(e["name"], face) for e in doc["elements"] for face, f in e["faces"].items() if f.get("texture") is not None}
    require(recorded == visible, "来源记录与所有可见面不是一一对应：缺%d，多%d" % (len(visible - recorded), len(recorded - visible)))
    if check_uuids:
        require(not mismatch, "来源表UUID不匹配，共%d面；例如：%s" % (len(mismatch), ", ".join(mismatch[:8])))
    return {"visible_faces": len(visible), "recorded_faces": len(rows), "uuid_mismatched_faces": len(mismatch),
            "all_source_pixels_match": True, "flip_u_faces": sum(bool(r.get("flip_u")) for r in rows),
            "flip_v_faces": sum(bool(r.get("flip_v")) for r in rows),
            "omitted_texture_null_faces": sum(f.get("texture") is None for e in doc["elements"] for f in e["faces"].values())}


def check_height(bones, spec):
    names = spec["height_bones"]
    require("crown" in names and "right_leg" in names and "left_leg" in names, "身高测量必须覆盖冠与双腿")
    require(not ({"staff", "staff_glow"} & set(names)), "身体身高不能包括权杖")
    lo, hi = posed_bounds(bones, names)
    scale = spec["model_scale"]
    require(isinstance(scale, (int, float)) and scale > 0 and math.isfinite(scale), "model_scale必须正有限数值")
    blocks = (hi[1] - lo[1]) * scale / 16
    require(abs(blocks - 2.6) < 1e-6, "实际rest几何身高不是2.6格：%.9f" % blocks)
    feet_lo, _ = posed_bounds(bones, ["right_leg", "left_leg"])
    _, crown_hi = posed_bounds(bones, ["crown"])
    require(abs(feet_lo[1] - lo[1]) < 1e-6, "身体最低点不在脚底")
    require(abs(crown_hi[1] - hi[1]) < 1e-6, "身体最高点不在皇冠")
    require(abs(feet_lo[1]) < 1e-6, "模型脚底没有位于Y=0")
    if "rest_bounds" in spec:
        expected = spec["rest_bounds"]
        require(all(abs(a - b) < 1e-6 for actual, stated in zip((lo, hi), expected) for a, b in zip(actual, stated)),
                "spec rest_bounds与实际模型不符")
    return {"rest_bounds": [lo, hi], "model_units_height": hi[1] - lo[1],
            "model_scale": scale, "scaled_blocks_height": blocks, "feet_y": feet_lo[1], "crown_y": crown_hi[1],
            "note": "只验证已保存静态几何的数学高度；未验证真实游戏载体seat或视觉比例。"}


def write_reports(report):
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "model_validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    lines = ["# 教皇 M2 静态模型验证", "", "结果：" + ("全部结构检查通过。" if report["ok"] else "存在问题，尚未全部通过。"), "",
             "当前模型 SHA-256：`%s`。报告只对应这个版本。" % report["inputs"].get("pope.bbmodel", "未读取"), "",
             "本验证只读实际保存后的 .bbmodel、图集与逐面来源记录；没有调用 build，没有修改模型或资源包。", "",
             "| 检查 | 结果 | 说明 |", "|---|---|---|"]
    for name, result in report["checks"].items():
        note = result.get("error", "通过；详见 JSON 的实测数据")
        lines.append("| %s | %s | %s |" % (name, "通过" if result["ok"] else "失败", str(note).replace("|", "/")))
    lines += ["", "结构通过不等于视觉还原已通过。UV像素能追溯，只证明取自指定原图及所记矩形；不能证明该面语义、朝向或重建几何就是官方数据。", "",
              "本阶段无动画；未进行数据包/资源包构建、专用服务器加载、载体部件清理或真实游戏内验证。未在真实游戏内看过。", "",
              "复现：`python _tools/pope_validate_model.py`。报告只写 `pope_ref/m2/validation/`。", ""]
    (OUTPUT / "MODEL_VALIDATION.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main():
    report = {"stage": "M2_static", "ok": False, "inputs": {}, "checks": {}, "in_game_verified": False}
    files = {"pope.bbmodel": REF / "pope.bbmodel", "model_spec.json": M2 / "model_spec.json",
             "face_provenance.json": M2 / "face_provenance.json", "atlas.png": M2 / "atlas.png"}

    def run(name, fn):
        try:
            result = fn()
            report["checks"][name] = {"ok": True, "details": result}
            return result
        except Exception as exc:
            report["checks"][name] = {"ok": False, "error": str(exc)}
            return None

    try:
        binary = {name: path.read_bytes() for name, path in files.items()}
        report["inputs"] = {name: sha256(data) for name, data in binary.items()}
        doc, spec, provenance = [json.loads(binary[name]) for name in ("pope.bbmodel", "model_spec.json", "face_provenance.json")]
        run("固定配置与保存后元数据", lambda: check_metadata(doc, spec, report["inputs"]["pope.bbmodel"]))
        run("模型结构与零动画", lambda: check_structure(doc))
        texture = check_texture(doc)
        atlas, texture_result = texture
        report["checks"]["单张内嵌PNG"] = {"ok": True, "details": texture_result}

        def atlas_match():
            external = Image.open(io.BytesIO(binary["atlas.png"])).convert("RGBA")
            require(external.size == atlas.size and external.tobytes() == atlas.tobytes(), "外部atlas.png与内嵌图集像素不同")
            return {"rgba_pixels_equal": True}

        run("内嵌与外部图集一致", atlas_match)
        run("图集原像素追溯", lambda: check_atlas_sources(atlas, spec["atlas_sources"]))
        # 分别报告像素与UUID；原生保存重建UUID时仍可定位具体问题，不能以名字代替最终UUID校验。
        run("逐面来源像素与UV", lambda: check_face_provenance(doc, atlas, provenance, check_uuids=False))
        run("逐面来源真实UUID", lambda: check_face_provenance(doc, atlas, provenance, check_uuids=True))
        parts = run("部件预算与管线坐标", lambda: check_parts(files["pope.bbmodel"], doc, spec["parts"], spec["glow"]))
        if parts:
            bones, part_results = parts
            report["checks"]["部件预算与管线坐标"]["details"] = {"count": len(part_results), "parts": part_results}
            run("脚底至冠顶2.6格", lambda: check_height(bones, spec))
        changed = [name for name, path in files.items() if sha256(path.read_bytes()) != report["inputs"][name]]
        require(not changed, "验证期间输入被其他会话更新，结果需重跑：" + ", ".join(changed))
    except Exception as exc:
        report["checks"]["输入与执行完整性"] = {"ok": False, "error": str(exc)}
    report["ok"] = bool(report["checks"]) and all(result["ok"] for result in report["checks"].values())
    write_reports(report)
    print(json.dumps({"ok": report["ok"], "model_sha256": report["inputs"].get("pope.bbmodel"),
                      "problems": {k: v["error"] for k, v in report["checks"].items() if not v["ok"]}}, ensure_ascii=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
