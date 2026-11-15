# -*- coding: utf-8 -*-
"""M2 静态校验；只写 heart_of_ender_ref/m2_validation.json。

读取 .bbmodel、m2_geometry/geometry_spec.json、m2_atlas/atlas_regions.json，
调用 display_mob 的只读几何函数，不调用 build、不生成运行时或修改共用管线。
该校验不能代替 Blockbench 正/侧/背对照，也不宣称验证了游戏半透明表现。
"""
from __future__ import annotations

import argparse
import base64
from collections import Counter
import hashlib
import io
import json
import math
from pathlib import Path
import sys

from PIL import Image

# Avoid writing __pycache__ while importing the existing read-only pipeline.
sys.dont_write_bytecode = True
import display_mob

HERE = Path(__file__).resolve().parent
REF = HERE / "heart_of_ender_ref"
DEFAULT_MODEL = REF / "heart_of_ender.bbmodel"
DEFAULT_GEOMETRY = REF / "m2_geometry" / "geometry_spec.json"
DEFAULT_REGIONS = REF / "m2_atlas" / "atlas_regions.json"
REPORT = REF / "m2_validation.json"
REQUIRED_RAW = {
    "MCD_Heart_of_Ender_(glow_effect_texture).png": [44, 44],
    "T_ArchIllagerUndressed.png": [64, 64],
}


class Audit:
    def __init__(self):
        self.checks = []

    def check(self, passed, name, detail=None, *, warning=False):
        self.checks.append({"check": name, "passed": bool(passed),
                            "severity": "warning" if warning else "error", "detail": detail})
        return bool(passed)

    def error(self, name, error):
        self.check(False, name, f"{type(error).__name__}: {error}")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def source_path(value):
    path = (REF / value).resolve()
    if not path.is_relative_to(REF.resolve()):
        raise ValueError(f"路径超出末影之心专用目录：{value}")
    return path


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def rgba(path):
    with Image.open(path) as im:
        return im.convert("RGBA")


def finite_vector(value, length=3):
    return (isinstance(value, list) and len(value) == length and
            all(isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) for x in value))


def rectangle(value, size):
    return (finite_vector(value, 4) and all(float(x).is_integer() for x in value) and
            0 <= value[0] < value[2] <= size[0] and 0 <= value[1] < value[3] <= size[1])


def matrix_close(a, b):
    return all(abs(a[r][c] - b[r][c]) < 1e-8 for r in range(4) for c in range(4))


def normalize_config(spec):
    """Explicit schema adapter; geometry measurements do not replace bbmodel geometry."""
    parts = [(p["name"], p["bones"]) for p in spec["parts"]]
    glow = list(spec.get("glow_bones", []))
    configured_scale = spec.get("model_scale")
    return {"parts": parts, "glow": glow,
            "expected_part_count": int(spec.get("expected_part_count", 21)),
            "seat": float(spec.get("seat", 0.0)),
            "model_scale": 1.0 if configured_scale is None else float(configured_scale),
            "model_scale_status": "static_normalization_only_game_scale_undecided" if configured_scale is None else "configured"}


def verify_projection(audit, name, region, original, actual):
    """Independently replay the registered nearest sampling, without importing the atlas generator."""
    rule = region["sampling_rule"]
    h = rule["inverse_homography"]
    if len(h) != 3 or not all(finite_vector(row) for row in h):
        raise ValueError("无效3×3采样矩阵")
    quad = region["source_quad"]
    if len(quad) != 4 or not all(finite_vector(point, 2) for point in quad):
        raise ValueError("无效来源四边形")
    audit.check(rule.get("destination_coordinates") == "u=(pixel_x+0.5)/width; v=(pixel_y+0.5)/height" and
                rule.get("nearest") == "floor(source_coordinate + 0.5)" and rule.get("homogeneous_divide") is True,
                "projection_sampling_convention:" + name)

    def project(u, v):
        div = h[2][0] * u + h[2][1] * v + h[2][2]
        if abs(div) < 1e-12:
            raise ValueError("透视采样矩阵在目标区域出现零齐次分母")
        return ((h[0][0] * u + h[0][1] * v + h[0][2]) / div,
                (h[1][0] * u + h[1][1] * v + h[1][2]) / div)

    corner_error = max(abs(x - y) for uv, source in zip(((0, 0), (1, 0), (1, 1), (0, 1)), quad)
                       for x, y in zip(project(*uv), source))
    audit.check(corner_error < 1e-6, "projection_matrix_matches_source_quad:" + name, corner_error)
    mask = rule["source_mask"]
    rgb_min, alpha_min = mask["rgb_min"], mask["alpha_min"]
    rects, halfplanes = mask["union_rects"], mask.get("halfplanes_ax_by_c_ge_0", [])
    if (not finite_vector(rgb_min) or not isinstance(alpha_min, (int, float)) or
            any(not rectangle(r, original.size) for r in rects) or
            any(not finite_vector(hp) for hp in halfplanes)):
        raise ValueError("无效透视提取遮罩规则")
    audit.check(rule.get("discarded_rgba") == [0, 0, 0, 0], "projection_discards_to_transparent:" + name)
    expected = bytearray()
    retained = 0
    for y in range(actual.height):
        for x in range(actual.width):
            sx, sy = project((x + 0.5) / actual.width, (y + 0.5) / actual.height)
            sx, sy = math.floor(sx + 0.5), math.floor(sy + 0.5)
            if not (0 <= sx < original.width and 0 <= sy < original.height):
                raise ValueError(f"透视采样越界：({sx},{sy})")
            pixel = original.getpixel((sx, sy))
            keep = (all(pixel[i] >= rgb_min[i] for i in range(3)) and pixel[3] >= alpha_min and
                    any(r[0] <= sx < r[2] and r[1] <= sy < r[3] for r in rects) and
                    all(a * sx + b * sy + c >= 0 for a, b, c in halfplanes))
            expected.extend(pixel if keep else (0, 0, 0, 0))
            retained += int(keep)
    expected = bytes(expected)
    audit.check(expected == actual.tobytes(), "projection_source_pixels_exact_rgba:" + name,
                {"retained_pixels": retained, "total_pixels": actual.width * actual.height,
                 "independent_rgba_sha256": sha(expected),
                 "method": "按登记矩阵逐像素计算源坐标和最近邻；保留原RGBalpha，其余透明，不依赖生成器或缓存映射"})


def validate_face_mapping(audit, document, regions_doc, model_path):
    mapping_path = REF / "m2_face_uv.json"
    mapping = load_json(mapping_path)
    model_hash = sha(model_path.read_bytes())
    declared_hash = mapping.get("bbmodel_sha256") or mapping.get("source_bbmodel_sha256")
    if declared_hash:
        audit.check(declared_hash == model_hash, "face_mapping_declared_bbmodel_hash", declared_hash)
    records = mapping["faces"]
    groups = {g["uuid"]: g["name"] for g in document["groups"]}
    owners = {}

    def walk(node):
        for child in node.get("children", []):
            if isinstance(child, str):
                owners[child] = groups[node["uuid"]]
            else:
                walk(child)

    for node in document["outliner"]:
        walk(node)
    elements = {e["name"]: e for e in document["elements"]}
    audit.check(len(elements) == len(document["elements"]), "unique_element_names_for_mapping")
    expected_faces = {(e["name"], face) for e in document["elements"] for face, data in e.get("faces", {}).items()
                      if data.get("texture") is not None}
    recorded_faces = [(r["element"], r["face"]) for r in records]
    missing = sorted(expected_faces - set(recorded_faces))
    extra = sorted(set(recorded_faces) - expected_faces)
    duplicate = [list(key) for key, count in Counter(recorded_faces).items() if count != 1]
    audit.check(not missing and not extra and not duplicate, "face_mapping_exact_coverage",
                {"actual_nonnull_faces": len(expected_faces), "mapped_faces": len(records),
                 "missing": missing, "extra": extra, "duplicate": duplicate})
    regions = {r["name"]: r for r in regions_doc["regions"]}
    differences = []
    for record in records:
        key = (record["element"], record["face"])
        if key not in expected_faces:
            continue
        element = elements[record["element"]]
        uv = element["faces"][record["face"]]["uv"]
        difference = {"element": element["name"], "uuid": element["uuid"], "face": record["face"]}
        reasons = []
        if owners.get(element["uuid"]) != record["bone"]:
            reasons.append("actual_bone_differs")
        if not finite_vector(record.get("atlas_uv"), 4) or any(abs(a - b) > 1e-6 for a, b in zip(uv, record["atlas_uv"])):
            reasons.append("actual_uv_differs")
        if record.get("element_uuid") and record["element_uuid"] != element["uuid"]:
            reasons.append("declared_uuid_differs")
        region = regions.get(record["region"])
        if region is None:
            reasons.append("unknown_region")
        else:
            ax, ay, bx, by = region["atlas_rect"]
            left, right = sorted([uv[0], uv[2]])
            top, bottom = sorted([uv[1], uv[3]])
            if not (ax <= left <= right <= bx and ay <= top <= bottom <= by):
                reasons.append("uv_outside_declared_region")
            if record["source_file"] != region["source_file"]:
                reasons.append("declared_source_differs")
            if region["kind"] == "source_copy":
                sx, sy, ex, ey = region["source_rect"]
                scale_x, scale_y = region["scale"]
                flip_x, flip_y = region["flip"]
                source_uv = [(ex - (uv[i] - ax) / scale_x if flip_x else sx + (uv[i] - ax) / scale_x)
                             if i % 2 == 0 else
                             (ey - (uv[i] - ay) / scale_y if flip_y else sy + (uv[i] - ay) / scale_y)
                             for i in range(4)]
                if not finite_vector(record.get("source_uv"), 4) or any(abs(a - b) > 1e-6 for a, b in zip(source_uv, record["source_uv"])):
                    reasons.append("declared_source_uv_differs")
        if reasons:
            differences.append(dict(difference, reasons=reasons))
    audit.check(not differences, "face_mapping_matches_actual_bbmodel",
                {"bbmodel_sha256": model_hash, "mapping_sha256": sha(mapping_path.read_bytes()),
                 "matched_faces": len(records) - len(differences), "differences": differences,
                 "scope": "按实际元素name/UUID、outliner归属骨、导出UV及登记源区域核对；不从生成前document推定"})


def validate_atlas(audit, document, regions_doc):
    textures = document.get("textures", [])
    if not audit.check(len(textures) == 1, "single_embedded_texture", len(textures)):
        return None, []
    source = textures[0].get("source", "")
    if not audit.check(source.startswith("data:image/png;base64,"), "embedded_png_data_uri"):
        return None, []
    embedded = base64.b64decode(source.split(",", 1)[1], validate=True)
    with Image.open(io.BytesIO(embedded)) as im:
        atlas = im.convert("RGBA")
    resolution = document.get("resolution", {})
    audit.check(list(atlas.size) == [resolution.get("width"), resolution.get("height")],
                "bbmodel_resolution_matches_embedded_png", list(atlas.size))
    audit.check(list(atlas.size) == regions_doc.get("atlas_size"), "region_manifest_atlas_size", list(atlas.size))
    atlas_file = source_path(regions_doc["atlas_file"])
    external = rgba(atlas_file)
    audit.check(external.size == atlas.size and external.tobytes() == atlas.tobytes(),
                "embedded_atlas_matches_external_rgba", {"file": str(atlas_file), "embedded_png_sha256": sha(embedded)})

    names, rects, verified_raw, star_sources = [], [], set(), []
    for region in regions_doc["regions"]:
        name = region["name"]
        names.append(name)
        try:
            box = region["atlas_rect"]
            if not audit.check(rectangle(box, atlas.size), "atlas_region_bounds:" + name, box):
                continue
            box = [int(x) for x in box]
            rects.append((name, box))
            actual = atlas.crop(box)
            digest = sha(actual.tobytes())
            audit.check(digest == region.get("output_rgba_sha256"), "region_output_rgba_sha256:" + name, digest)
            original_file = source_path(region["source_file"])
            original = rgba(original_file)
            source_box = region["source_rect"]
            if not audit.check(rectangle(source_box, original.size), "source_region_bounds:" + name, source_box):
                continue
            source_box = [int(x) for x in source_box]
            cropped = original.crop(source_box)
            if region["kind"] == "source_copy":
                audit.check(sha(cropped.tobytes()) == region.get("source_rgba_sha256"),
                            "region_source_rgba_sha256:" + name, sha(cropped.tobytes()))
                scale = region.get("scale", [1, 1])
                flip = region.get("flip", [False, False])
                if not finite_vector(scale, 2) or min(scale) <= 0 or len(flip) != 2:
                    raise ValueError("非法scale/flip")
                dimensions = [cropped.width * scale[0], cropped.height * scale[1]]
                if any(abs(x - round(x)) > 1e-8 for x in dimensions):
                    raise ValueError("缩放后的尺寸不是整数")
                expected = cropped.resize(tuple(round(x) for x in dimensions), Image.Resampling.NEAREST)
                if flip[0]:
                    expected = expected.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                if flip[1]:
                    expected = expected.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                audit.check(region.get("resampling") == "nearest", "nearest_only:" + name)
                exact = actual.size == expected.size and actual.tobytes() == expected.tobytes()
                audit.check(exact, "source_copy_exact_rgba:" + name,
                            {"source_file": region["source_file"], "source_rect": source_box, "atlas_rect": box,
                             "scale": scale, "flip": flip, "rgba_sha256": digest})
                if original_file.name in REQUIRED_RAW:
                    full_size = REQUIRED_RAW[original_file.name]
                    unchanged = (list(original.size) == full_size and source_box == [0, 0, *full_size] and
                                 scale == [1, 1] and flip == [False, False] and exact and
                                 actual.tobytes() == original.tobytes())
                    audit.check(unchanged, "required_full_original_rgba:" + original_file.name)
                    if unchanged:
                        verified_raw.add(original_file.name)
                if original_file.name == "MCD_Decal_Puddle_(texture).png":
                    audit.check(source_box != [0, 0, original.width, original.height],
                                "star_window_is_crop_not_whole_texture:" + name, source_box)
                    star_sources.append({"name": name, "source_rect": source_box, "exact": exact})
            elif region["kind"] == "projection_extract":
                audit.check(bool(region.get("source_quad")) and bool(region.get("sampling_rule")),
                            "projection_provenance_registered:" + name)
                verify_projection(audit, name, region, original, actual)
            else:
                audit.check(False, "known_region_kind:" + name, region.get("kind"))
        except Exception as error:
            audit.error("atlas_region:" + name, error)
    audit.check(len(names) == len(set(names)), "unique_region_names")
    audit.check(verified_raw == set(REQUIRED_RAW), "both_required_raw_textures_preserved", sorted(verified_raw))
    audit.check(len(star_sources) >= 2 and all(r["exact"] for r in star_sources),
                "multiple_original_star_windows_verified", star_sources)
    overlaps = []
    for i, (a_name, a) in enumerate(rects):
        for b_name, b in rects[i + 1:]:
            if min(a[2], b[2]) > max(a[0], b[0]) and min(a[3], b[3]) > max(a[1], b[1]):
                overlaps.append([a_name, b_name])
    audit.check(not overlaps, "atlas_regions_do_not_overlap", overlaps)
    return atlas, rects


def validate_model(audit, document, spec, model_path, atlas, rects):
    config = normalize_config(spec)
    parts, glow = config["parts"], config["glow"]
    audit.check(math.isfinite(config["model_scale"]) and config["model_scale"] > 0,
                "static_transform_scale", {"math_scale": config["model_scale"], "status": config["model_scale_status"],
                                           "note": "null仅用1.0进行归一化静态矩阵检查，不把它当作游戏体型决定"})
    audit.check(not document.get("animations"), "m2_static_has_no_animations", len(document.get("animations", [])))
    audit.check(len(parts) == config["expected_part_count"], "expected_display_part_count",
                {"actual": len(parts), "expected": config["expected_part_count"], "glow_does_not_add_parts": True})
    audit.check(len({name for name, _ in parts}) == len(parts), "unique_part_names")
    groups, elements = document["groups"], document["elements"]
    audit.check(len({g["uuid"] for g in groups}) == len(groups), "unique_group_uuids")
    audit.check(len({g["name"] for g in groups}) == len(groups), "unique_bone_names")
    audit.check(len({e["uuid"] for e in elements}) == len(elements), "unique_element_uuids")
    group_ids, element_ids = {g["uuid"] for g in groups}, {e["uuid"] for e in elements}
    seen_groups, seen_elements = [], []

    def walk(node):
        if not isinstance(node, dict) or node.get("uuid") not in group_ids:
            raise ValueError("outliner含未知骨骼或根级未分组元素")
        seen_groups.append(node["uuid"])
        for child in node.get("children", []):
            if isinstance(child, str):
                if child not in element_ids:
                    raise ValueError("outliner含未知元素")
                seen_elements.append(child)
            else:
                walk(child)

    for node in document["outliner"]:
        walk(node)
    audit.check(Counter(seen_groups) == Counter(group_ids), "every_group_in_outliner_once")
    audit.check(Counter(seen_elements) == Counter(element_ids), "every_element_in_outliner_once")
    for group in groups:
        audit.check(finite_vector(group.get("origin")) and finite_vector(group.get("rotation", [0, 0, 0])),
                    "finite_bone_transform:" + group["name"])
    uv_errors, ignored_transform_errors, bounds_errors = [], [], []
    for element in elements:
        name = element.get("name", element["uuid"])
        if (element.get("type", "cube") != "cube" or
                any(float(v) != 0 for v in element.get("rotation", [0, 0, 0]))):
            ignored_transform_errors.append(name)
        if not finite_vector(element.get("from")) or not finite_vector(element.get("to")):
            bounds_errors.append(name)
        for face, values in element.get("faces", {}).items():
            if values.get("texture") is None:
                continue
            uv = values.get("uv")
            if values.get("texture") != 0 or not finite_vector(uv, 4) or values.get("rotation", 0) != 0:
                uv_errors.append({"element": name, "face": face, "reason": "非0贴图、无效UV或不被导出的面旋转"})
                continue
            left, right = sorted([uv[0], uv[2]])
            top, bottom = sorted([uv[1], uv[3]])
            if atlas is None or not (0 <= left <= right <= atlas.width and 0 <= top <= bottom <= atlas.height):
                uv_errors.append({"element": name, "face": face, "reason": "UV超出图集"})
            elif not any(b[0] <= left <= right <= b[2] and b[1] <= top <= bottom <= b[3] for _, b in rects):
                uv_errors.append({"element": name, "face": face, "reason": "UV未完全落在单个登记区域", "uv": uv})
    audit.check(not ignored_transform_errors, "only_cubes_without_ignored_element_rotations", ignored_transform_errors)
    audit.check(not bounds_errors, "finite_cube_coordinates", bounds_errors)
    audit.check(not uv_errors, "all_nonnull_faces_use_registered_single_atlas_regions", uv_errors)

    mob = display_mob.Mob(key="heart_of_ender", label="末影之心M2静态校验", generator=Path(__file__).name,
                          bbmodel=str(model_path), parts=parts, glow=glow, seat=config["seat"],
                          tag="rpg.he", score="rpg_he", clips=[], model_scale=config["model_scale"])
    bones, _, _ = display_mob.load_bbmodel(mob)
    merged_bones = [bone for _, members in parts for bone in members]
    unknown = sorted(set(merged_bones) - set(bones))
    audit.check(not unknown, "configured_bones_exist", unknown)
    duplicated = sorted(name for name, n in Counter(merged_bones).items() if n != 1)
    audit.check(not duplicated, "each_rendered_bone_owned_by_one_part", duplicated)
    unassigned = [name for name, bone in bones.items() if bone["cubes"] and name not in merged_bones]
    audit.check(not unassigned, "all_geometry_bones_assigned_to_parts", unassigned)
    audit.check(bool(glow) and all(name in bones and bones[name]["cubes"] for name in glow),
                "explicit_nonempty_glow_bones", glow)
    glow_roots = [part for part, members in parts if members and members[0] in glow]
    audit.check(not glow_roots, "glow_bones_rigidly_merged_no_extra_display", glow_roots)
    outputs = []
    for part, members in parts:
        try:
            if not members:
                raise ValueError("part没有首骨")
            root = members[0]
            if not any(bones[name]["cubes"] for name in members):
                raise ValueError("part没有元素，无法生成有限包围盒")
            for name in members[1:]:
                if root not in display_mob.chain(bones, name)[:-1]:
                    raise ValueError(f"合并骨{name}不是首骨{root}的后代")
                rot = bones[name]["rotation"]
                nonzero = [x for x in rot if abs(x) > 1e-8]
                if len(nonzero) > 1 or any(abs(x) > 45 for x in nonzero):
                    raise ValueError(f"合并骨{name}旋转必须单轴且不超过45度：{rot}")
                relative = display_mob.bone_matrix(bones, name, stop=root)
                direct = display_mob.about(bones[name]["pivot"], rot)
                if not matrix_close(relative, direct):
                    raise ValueError(f"合并骨{name}含额外祖先旋转，不能由part_model直接输出")
            generated, offset = display_mob.part_model(mob, bones, part, members, document["resolution"])
            bounds = [value for element in generated["elements"] for value in element["from"] + element["to"]]
            legal = all(math.isfinite(v) and -16 <= v <= 32 for v in bounds)
            audit.check(legal, "pipeline_part_bounds:" + part, {"min": min(bounds), "max": max(bounds), "offset": offset})
            expected_glow = sum(len(bones[name]["cubes"]) for name in members if name in glow)
            actual_glow = sum(element.get("light_emission") == 15 and element.get("shade") is False
                              for element in generated["elements"])
            audit.check(expected_glow == actual_glow, "pipeline_glow_elements:" + part,
                        {"expected": expected_glow, "actual": actual_glow})
            transform = display_mob.display_matrix(mob, bones, root, offset)
            audit.check(all(math.isfinite(v) for row in transform for v in row), "finite_display_matrix:" + part)
            outputs.append({"part": part, "bones": members, "elements": len(generated["elements"]),
                            "glow_elements": actual_glow, "offset": offset, "display_matrix": transform})
        except (Exception, SystemExit) as error:
            audit.error("pipeline_part:" + part, error)
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--geometry", type=Path, default=DEFAULT_GEOMETRY)
    parser.add_argument("--regions", type=Path, default=DEFAULT_REGIONS)
    args = parser.parse_args()
    audit = Audit()
    report = {"stage": "M2_static", "generator": Path(__file__).name,
              "scope": "静态模型格式、现有管线几何转换与图集像素来源；不包含动画、构建、游戏表现或视觉还原度判定",
              "limitations": ["44遮罩的原始RGBalpha保留检查不证明半透明实际渲染效果",
                              "透视采样按登记矩阵独立重算，可证明像素来源，不能证明四边形拟合等同原作UV",
                              "model_scale和seat仅使用配置值，未验证实际游戏体型或载体座高"],
              "inputs": {}, "parts": [], "checks": audit.checks}
    try:
        for name, path in (("bbmodel", args.model), ("geometry_spec", args.geometry), ("atlas_regions", args.regions)):
            path = path.resolve()
            if not path.is_relative_to(REF.resolve()):
                raise ValueError(f"输入超出专用目录：{path}")
            report["inputs"][name] = {"path": str(path), "sha256": sha(path.read_bytes())}
        document, spec, regions = load_json(args.model), load_json(args.geometry), load_json(args.regions)
        atlas, rects = validate_atlas(audit, document, regions)
        report["parts"] = validate_model(audit, document, spec, args.model, atlas, rects)
        validate_face_mapping(audit, document, regions, args.model)
    except (Exception, SystemExit) as error:
        audit.error("static_validation_exception", error)
    report["summary"] = {"checks": len(audit.checks),
                         "errors": sum(not c["passed"] and c["severity"] == "error" for c in audit.checks),
                         "warnings": sum(not c["passed"] and c["severity"] == "warning" for c in audit.checks),
                         "parts_checked": len(report["parts"])}
    report["passed"] = report["summary"]["errors"] == 0
    REF.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"report": str(REPORT), "passed": report["passed"], **report["summary"]}, ensure_ascii=False))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
