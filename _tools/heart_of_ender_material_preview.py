"""独立 CPU 材质对照：直接读 bbmodel，不连接 Blockbench 或 Minecraft。

四个正交视角、最近邻 atlas、外侧正面、alpha >= 0.1、普通 alpha
混合及深度写入。全部表面以原始 RGB 全亮显示；无方向光、无 bloom。
此脚本只生成离线模拟图，不能证明 Minecraft 的真实透明排序或亮度。
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import io
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import display_mob as dm

REF = Path(__file__).resolve().parent / "heart_of_ender_ref"
BG = (55, 60, 70)
GENERATOR = "heart_of_ender_material_preview.py"
FACE_NAMES = ("north", "east", "south", "west", "up", "down")
NORMALS = {"north": [0, 0, -1], "east": [1, 0, 0], "south": [0, 0, 1],
           "west": [-1, 0, 0], "up": [0, 1, 0], "down": [0, -1, 0]}
VIEWERS = {"front": [0, 0, -1], "right_side": [1, 0, 0], "back": [0, 0, 1],
           "three_quarter": [-0.640856, 0.422618, -0.640856]}
LABELS = {"front": "正面", "right_side": "右侧", "back": "背面", "three_quarter": "四分之三"}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def normalized(value):
    value = np.asarray(value, dtype=np.float64)
    return value / np.linalg.norm(value)


def face_corners(lo, hi, name):
    """UV 顺序 TL, TR, BR, BL；与 CubeFace.UVToLocal 的六个分支一致。

    核对来源：本机 Blockbench app.asar 的 bundle.js.map 中
    ../js/outliner/types/cube.js。cross(BL-TL, TR-TL) 指向盒外。
    """
    x0, y0, z0 = lo
    x1, y1, z1 = hi
    return np.asarray({
        "north": [(x1, y1, z0), (x0, y1, z0), (x0, y0, z0), (x1, y0, z0)],
        "east": [(x1, y1, z1), (x1, y1, z0), (x1, y0, z0), (x1, y0, z1)],
        "south": [(x0, y1, z1), (x1, y1, z1), (x1, y0, z1), (x0, y0, z1)],
        "west": [(x0, y1, z0), (x0, y1, z1), (x0, y0, z1), (x0, y0, z0)],
        "up": [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)],
        "down": [(x0, y0, z1), (x1, y0, z1), (x1, y0, z0), (x0, y0, z0)],
    }[name], dtype=np.float64)


@dataclass
class Face:
    points: np.ndarray
    uv: np.ndarray
    name: str
    tint_rgb: tuple = (255, 255, 255)


@dataclass
class Model:
    faces: list[Face]
    atlas: np.ndarray
    resolution: np.ndarray
    evidence: dict


def load_model(path, clip_name, time):
    raw = path.read_bytes()
    doc = json.loads(raw)
    from heart_of_ender_emission import mask_records
    face_tints = {(r['element_uuid'], r['face']): tuple(r['tint_rgb']) for r in mask_records(doc)}
    if len(doc.get("textures", [])) != 1:
        raise ValueError("预览要求恰好一张 textures[0] 内嵌贴图")
    mob = SimpleNamespace(bbmodel=path, anim_from=None, key="heart_of_ender_preview")
    bones, png, resolution = dm.load_bbmodel(mob)
    animations = dm.load_animations(mob)
    if clip_name == "rest":
        clip = {"tracks": {}, "loop": False, "length": 0}
    else:
        if clip_name not in animations:
            raise ValueError(f"模型缺少动作 {clip_name}")
        clip = animations[clip_name]
        if time < 0 or time > clip["length"]:
            raise ValueError(f"时间 {time} 超出动作 {clip_name} 长度 {clip['length']}")
    atlas = np.asarray(Image.open(io.BytesIO(png)).convert("RGBA"))
    faces = []
    cube_count = 0
    skipped_null = 0
    for bone, definition in bones.items():
        matrix = np.asarray(dm.posed_matrix(bones, bone, clip, time))
        for cube in definition["cubes"]:
            cube_count += 1
            # These properties are not implemented by dm.part_model either;
            # refusing them prevents a plausible but incompatible preview.
            if any(cube.get("rotation") or [0, 0, 0]):
                raise ValueError(f"不支持元素自身旋转：{cube['name']}")
            if cube.get("stretch", [1, 1, 1]) != [1, 1, 1]:
                raise ValueError(f"不支持 stretch：{cube['name']}")
            lo = np.asarray(cube["from"], dtype=float) - cube.get("inflate", 0)
            hi = np.asarray(cube["to"], dtype=float) + cube.get("inflate", 0)
            if np.any(hi < lo):
                raise ValueError(f"反向盒子尺寸：{cube['name']}")
            for name, face in cube["faces"].items():
                if face.get("texture") is None:
                    skipped_null += 1
                    continue
                if face.get("texture") != 0 or face.get("rotation", 0) != 0:
                    raise ValueError(f"非第0贴图或旋转UV：{cube['name']}/{name}")
                local = face_corners(lo, hi, name)
                points = local @ matrix[:3, :3].T + matrix[:3, 3]
                uv = np.asarray(face["uv"], dtype=np.float64)
                if uv.shape != (4,) or not np.isfinite(uv).all() or not np.isfinite(points).all():
                    raise ValueError(f"非法坐标：{cube['name']}/{name}")
                faces.append(Face(points, uv, f"{bone}/{cube['name']}/{name}",
                                  face_tints.get((cube['uuid'], name), (255, 255, 255))))
    res = np.asarray([resolution["width"], resolution["height"]], dtype=float)
    if np.any(res <= 0):
        raise ValueError("非法贴图分辨率")
    evidence = {"path": str(path), "bbmodel_sha256": sha(raw), "embedded_png_sha256": sha(png),
                "decoded_rgba_sha256": sha(atlas.tobytes()), "atlas_size": list(atlas.shape[1::-1]),
                "uv_resolution": res.tolist(), "bone_count": len(bones), "cube_count": cube_count,
                "textured_face_count": len(faces), "skipped_null_faces": skipped_null,
                "posed_geometry_sha256": sha(np.concatenate([f.points for f in faces]).tobytes())}
    return Model(faces, atlas, res, evidence)


def camera(viewer, target, height, size, up=(0, 1, 0)):
    viewer = normalized(viewer)
    right = normalized(np.cross(up, viewer))
    up = normalized(np.cross(viewer, right))
    return {"target": list(target), "viewer": viewer.tolist(), "right": right.tolist(),
            "up": up.tolist(), "height": float(height), "size": int(size)}


def projection(points, cam):
    p = points - cam["target"]
    return np.column_stack((
        p @ cam["right"] * cam["size"] / cam["height"] + cam["size"] / 2,
        -p @ cam["up"] * cam["size"] / cam["height"] + cam["size"] / 2,
        p @ cam["viewer"]))


def shared_cameras(before, after, size):
    points = np.concatenate([f.points for model in (before, after) for f in model.faces])
    target = (points.min(axis=0) + points.max(axis=0)) / 2
    # One center and one scale across all four views AND both input models.
    # Account for projected off-center extrema, not just projected width.
    height = 0
    for viewer in VIEWERS.values():
        c = camera(viewer, target, 1, 1)
        offset = points - target
        height = max(height, float(np.abs(offset @ c["right"]).max() * 2),
                     float(np.abs(offset @ c["up"]).max() * 2))
    return {name: camera(v, target, height * 1.12, size) for name, v in VIEWERS.items()}


def render(model, cam):
    """Orthographic affine quad rasterization, avoiding a triangle seam.

    Draw far-to-near by quad center, retain only positive outward-normal dot
    viewer, then depth test/write each retained texel. This is one global
    buffer approximation, not a reproduction of Minecraft draw-call batches.
    """
    size = cam["size"]
    color = np.broadcast_to(np.asarray(BG, dtype=float), (size, size, 3)).copy()
    depth = np.full((size, size), -np.inf)
    visible = []
    stats = {"outward_faces_drawn": 0, "back_or_edge_faces_culled": 0,
             "degenerate_faces_skipped": 0, "retained_fragments": 0}
    for face in model.faces:
        normal = np.cross(face.points[3] - face.points[0], face.points[1] - face.points[0])
        if np.linalg.norm(normal) < 1e-12:
            stats["degenerate_faces_skipped"] += 1
            continue
        if float(normal @ cam["viewer"]) <= 1e-10:
            stats["back_or_edge_faces_culled"] += 1
            continue
        p = projection(face.points, cam)
        visible.append((float(p[:, 2].mean()), face, p))
    for _, face, p in sorted(visible, key=lambda item: item[0]):
        stats["outward_faces_drawn"] += 1
        x0, y0 = np.maximum(0, np.floor(p[:, :2].min(axis=0)).astype(int))
        x1, y1 = np.minimum(size, np.ceil(p[:, :2].max(axis=0)).astype(int))
        if x1 <= x0 or y1 <= y0:
            continue
        basis = np.column_stack((p[1, :2] - p[0, :2], p[3, :2] - p[0, :2]))
        if abs(np.linalg.det(basis)) < 1e-12:
            continue
        yy, xx = np.mgrid[y0:y1, x0:x1]
        query = np.stack((xx + 0.5 - p[0, 0], yy + 0.5 - p[0, 1]), axis=-1)
        st = query @ np.linalg.inv(basis).T
        keep = (st[..., 0] >= 0) & (st[..., 0] < 1) & (st[..., 1] >= 0) & (st[..., 1] < 1)
        u0, v0, u1, v1 = face.uv
        # Texel i has center i+.5; OpenGL nearest is floor(normalizedUV*size).
        u = np.floor((u0 + st[..., 0] * (u1 - u0)) * model.atlas.shape[1] / model.resolution[0]).astype(int)
        v = np.floor((v0 + st[..., 1] * (v1 - v0)) * model.atlas.shape[0] / model.resolution[1]).astype(int)
        sample = model.atlas[np.clip(v, 0, model.atlas.shape[0]-1), np.clip(u, 0, model.atlas.shape[1]-1)]
        alpha = sample[..., 3] / 255.0
        z = p[0, 2] + st[..., 0] * (p[1, 2] - p[0, 2]) + st[..., 1] * (p[3, 2] - p[0, 2])
        region_depth = depth[y0:y1, x0:x1]
        keep &= (alpha >= 0.1) & (z >= region_depth - 1e-9)
        # Standard source-over; declared raw-mask tint is a runtime RGB multiply.
        region_color = color[y0:y1, x0:x1]
        a = alpha[keep, None]
        region_color[keep] = (sample[..., :3][keep] * (np.asarray(face.tint_rgb) / 255.0)) * a + region_color[keep] * (1-a)
        region_depth[keep] = z[keep]
        stats["retained_fragments"] += int(keep.sum())
    result = np.clip(np.floor(color + 0.5), 0, 255).astype(np.uint8)
    occupied = np.isfinite(depth)
    stats["occupied_pixels"] = int(occupied.sum())
    if occupied.any():
        y, x = np.where(occupied)
        stats["occupied_bbox_xyxy"] = [int(x.min()), int(y.min()), int(x.max()+1), int(y.max()+1)]
    return result, stats


def self_checks():
    """Small renderer invariants, not tests that claim Minecraft equivalence."""
    checks = []
    atlas = np.asarray([[[255, 0, 0, 255], [0, 255, 0, 255]],
                        [[0, 0, 255, 255], [255, 255, 0, 255]]], dtype=np.uint8)
    for name in FACE_NAMES:
        points = face_corners([0, 0, 0], [1, 1, 1], name)
        normal = normalized(np.cross(points[3]-points[0], points[1]-points[0]))
        assert np.allclose(normal, NORMALS[name]), name
        c = camera(normal, points.mean(axis=0), 1, 8, up=points[0]-points[3])
        m = Model([Face(points, np.asarray([0, 0, 2, 2]), name)], atlas, np.asarray([2, 2]), {})
        pixels, stats = render(m, c)
        for row, col, expected in [(1, 1, atlas[0, 0, :3]), (1, 6, atlas[0, 1, :3]),
                                   (6, 1, atlas[1, 0, :3]), (6, 6, atlas[1, 1, :3])]:
            assert np.array_equal(pixels[row, col], expected), (name, row, col)
        reverse = camera(-normal, points.mean(axis=0), 1, 8, up=points[0]-points[3])
        assert render(m, reverse)[1]["occupied_pixels"] == 0, name
        m.faces[0].uv = np.asarray([2, 0, 0, 2])
        assert np.array_equal(render(m, c)[0][1, 1], atlas[0, 1, :3]), name
        checks.append(f"{name}: outward normal / four UV corners / mirrored U / back culling")
    p = face_corners([0, 0, 0], [1, 1, 1], "north")
    c = camera([0, 0, -1], p.mean(axis=0), 1, 8)
    far = Face(p + [0, 0, 1], np.asarray([0, 0, 1, 1]), "far_red")
    near = Face(p, np.asarray([1, 0, 2, 1]), "near_blue")
    tex = np.asarray([[[255, 0, 0, 255], [0, 0, 255, 128]]], dtype=np.uint8)
    m = Model([near, far], tex, np.asarray([2, 1]), {})
    assert np.array_equal(render(m, c)[0][4, 4], [127, 0, 128])
    tex[0, 1, 3] = 25
    assert np.array_equal(render(m, c)[0][4, 4], [255, 0, 0])
    tex[0, 1, 3] = 26
    assert np.array_equal(render(m, c)[0][4, 4], [229, 0, 26])
    checks.extend(["far-to-near normal alpha blending", "8-bit alpha25 discarded / alpha26 retained"])
    return checks


def font(size):
    try:
        return ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", size)
    except OSError:
        return ImageFont.load_default()


def png_bytes(image):
    output = io.BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


def write_outputs(output, files):
    output = output.resolve()
    if not output.is_relative_to(REF.resolve()) or output == REF.resolve():
        raise ValueError("输出必须是 heart_of_ender_ref 内的专属子目录")
    marker = output / "offline_preview_ownership.json"
    previous = json.loads(marker.read_text(encoding="utf-8")) if marker.exists() else {}
    if previous and previous.get("generator") != GENERATOR:
        raise ValueError("输出目录由另一生成器管理")
    for name in files:
        path = output / name
        if path.exists() and previous.get("files", {}).get(name) != sha(path.read_bytes()):
            raise ValueError(f"拒绝覆盖非本脚本文件或手改输出：{path}")
    output.mkdir(parents=True, exist_ok=True)
    for name, data in files.items():
        (output / name).write_bytes(data)
    marker.write_text(json.dumps({"generator": GENERATOR, "files": {k: sha(v) for k, v in files.items()}},
                                 ensure_ascii=False, indent=2)+"\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--before", type=Path, required=True)
    ap.add_argument("--after", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--size", type=int, default=800, help="单视图边长，700..900像素")
    ap.add_argument("--clip", default="idle", help="动作名或 rest；默认 idle")
    ap.add_argument("--time", type=float, default=0)
    args = ap.parse_args()
    if not 700 <= args.size <= 900:
        ap.error("--size 必须在700..900之间")
    for path in (args.before, args.after):
        if not path.resolve().is_relative_to(REF.resolve()):
            ap.error("输入模型必须位于 heart_of_ender_ref")
    checks = self_checks()
    before = load_model(args.before.resolve(), args.clip, args.time)
    after = load_model(args.after.resolve(), args.clip, args.time)
    cameras = shared_cameras(before, after, args.size)
    files, view_evidence = {}, {}
    title_font, small_font = font(24), font(18)
    for view, cam in cameras.items():
        images, stats = [], []
        for label, model in (("before", before), ("after", after)):
            pixels, statistics = render(model, cam)
            im = Image.fromarray(pixels)
            filename = f"{view}_{label}.png"
            files[filename] = png_bytes(im)
            images.append(im)
            stats.append(statistics)
        a, b = map(np.asarray, images)
        delta = np.abs(a.astype(np.int16)-b.astype(np.int16))
        comparison = Image.new("RGB", (2*args.size, args.size+80), BG)
        draw = ImageDraw.Draw(comparison)
        for index, (label, model, im) in enumerate(zip(("之前", "之后"), (before, after), images)):
            x = index*args.size
            draw.text((x+16, 9), f"{LABELS[view]} / {label} {model.evidence['bbmodel_sha256'][:12]}", font=title_font, fill="white")
            draw.text((x+16, 44), f"离线模拟 · 原色全亮 · 无泛光 · {args.clip} {args.time:g}s", font=small_font, fill=(215, 215, 215))
            comparison.paste(im, (x, 80))
        files[f"{view}_comparison.png"] = png_bytes(comparison)
        view_evidence[view] = {"camera": cam, "before": stats[0], "after": stats[1],
                               "changed_pixels": int(np.any(delta, axis=2).sum()),
                               "max_channel_difference": int(delta.max())}
        print(f"离线渲染 {view}: 前后变化 {view_evidence[view]['changed_pixels']} 像素", flush=True)
    evidence = {"engine": "independent Python/NumPy CPU orthographic rasterizer",
                "status": "OFFLINE SIMULATION; NOT Blockbench; NOT Minecraft; no bloom",
                "generator_sha256": sha(Path(__file__).read_bytes()), "pose": {"clip": args.clip, "time": args.time},
                "before": before.evidence, "after": after.evidence, "views": view_evidence,
                "self_checks": checks, "rendering": {"nearest_neighbor": True, "alpha_cutoff": 0.1,
                "culling": "draw outward-facing front faces; discard back and edge-on faces",
                "sorting": "all model quads in one list, mean view-depth far-to-near",
                "depth_test": "nearer-or-equal, depth write after alpha threshold", "blend": "SRC_ALPHA / ONE_MINUS_SRC_ALPHA",
                "lighting": "unlit atlas RGB with explicitly declared per-face constant mask tint; no exposure, directional shading or bloom",
                "background_rgb": list(BG), "source_changes": "none; source bbmodel and atlas read only"},
                "limitations": ["普通透明叠加仅模拟单批次按面中心排序；不证明游戏实体批次、交叉面和共面排序。",
                                "未模拟 Minecraft 方向光、光照贴图、雾、色彩空间转换、mipmap 或图集边缘缩进。",
                                "全亮原色方便比较微光像素；实际游戏可能更暗，没有泛光或动态照亮环境。",
                                "直接使用模型单位与 dm.posed_matrix；不是载体座高、世界体型或真实游戏截图。",
                                "拒绝非零元素旋转、UV旋转、stretch或第二贴图，避免偏离现有共用管线。"],
                "image_sha256": {name: sha(data) for name, data in files.items()}}
    if before.evidence["bbmodel_sha256"] == after.evidence["bbmodel_sha256"]:
        assert all(v["changed_pixels"] == 0 for v in view_evidence.values()), "同源自对照不一致"
        evidence["same_source_self_comparison"] = "pixel-identical in all four views"
    for path, model in ((args.before, before), (args.after, after)):
        assert sha(path.read_bytes()) == model.evidence["bbmodel_sha256"], "运行期间源模型发生变更"
    files["render_evidence.json"] = (json.dumps(evidence, ensure_ascii=False, indent=2)+"\n").encode("utf-8")
    write_outputs(args.out, files)
    print(json.dumps({"output": str(args.out.resolve()), "self_checks": len(checks),
                      "before_sha256": before.evidence["bbmodel_sha256"],
                      "after_sha256": after.evidence["bbmodel_sha256"], "files": len(files)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
