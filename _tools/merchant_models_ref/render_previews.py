"""重绘四位商人的待机预览和双眼近景。运行 python -B render_previews.py。"""

import io
import math
from pathlib import Path
import sys
from types import SimpleNamespace

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
sys.path.insert(0, str(TOOLS))
import display_mob
from guide_renders.soft_render import UV_AT
from lucifer_ref.render_static import camera_basis, cube_face_vertices, font, point_transform, triangle

MERCHANTS = (("smith", "铁匠"), ("mystery", "神秘商人"),
             ("luxury", "奢侈品商人"), ("travel", "迷途商人"))
BACKGROUND = "#272b30"
TRIANGLES = ([0, 1, 2], [0, 2, 3])


def idle_scene(model):
    mob = SimpleNamespace(bbmodel=str(model), anim_from=None, key=model.stem)
    bones, png, resolution = display_mob.load_bbmodel(mob)
    texture = np.asarray(Image.open(io.BytesIO(png)).convert("RGBA"))
    uv_scale = np.array(texture.shape[1::-1]) / [resolution["width"], resolution["height"]]
    idle = display_mob.load_animations(mob)["idle"]
    cache, faces, eyes = {}, [], []
    for name, bone in bones.items():
        world = np.asarray(display_mob.posed_matrix(bones, name, idle, 0, cache))
        for cube in bone["cubes"]:
            matrix = world @ display_mob.about(cube["origin"], cube["rotation"])
            inflate = cube.get("inflate", 0)
            corners = cube_face_vertices(np.array(cube["from"]) - inflate, np.array(cube["to"]) + inflate)
            for side, data in cube["faces"].items():
                if data.get("texture") is None:
                    continue
                points = point_transform(matrix, corners[side])
                u0, v0, u1, v1 = data["uv"]
                uv = np.array([((u0, u1)[u], (v0, v1)[v])
                               for u, v in UV_AT[data.get("rotation", 0)]]) * uv_scale
                faces.append((points, uv))
                if "_eyepupil_" in name:
                    eyes.append(points.mean(axis=0))
    return faces, texture, np.mean(eyes, axis=0)


def view(scene, yaw, pitch, size, closeup=False):
    faces, texture, eyes = scene
    a, p = map(math.radians, (yaw, pitch))
    camera = camera_basis([-math.sin(a) * math.cos(p), math.sin(p), math.cos(a) * math.cos(p)])
    all_points = np.concatenate([points for points, _ in faces]) @ camera.T
    bounds = np.ptp(all_points, axis=0)
    center = (all_points.max(axis=0) + all_points.min(axis=0)) / 2
    width, height = size
    scale = .91 * min(width / bounds[0], height / bounds[1])
    if closeup:
        # Frame the eyes from their posed geometry. Include the brow, nose and headwear.
        center = eyes @ camera.T
        center[1] += .17
        scale = width / 2.08

    rgb = np.zeros((height, width, 3), dtype=np.uint8)
    depth = np.full((height, width), -np.inf)
    light = np.array([-.40, .70, .59])
    light /= np.linalg.norm(light)
    for points, uv in faces:
        normal = np.cross(points[3] - points[0], points[1] - points[0])
        if normal @ camera[2] <= 1e-10:
            continue
        shade = .73 + .27 * max(0, normal @ light / np.linalg.norm(normal))
        screen = points @ camera.T - center
        screen[:, 0] = width / 2 + screen[:, 0] * scale
        screen[:, 1] = height / 2 - screen[:, 1] * scale
        for indices in TRIANGLES:
            triangle(rgb, depth, screen[indices], uv[indices], texture, shade)
    alpha = np.isfinite(depth).astype(np.uint8) * 255
    return Image.fromarray(np.dstack((rgb, alpha)))


def main():
    lineup = Image.new("RGB", (1040, 320), BACKGROUND)
    closeups = Image.new("RGB", (1040, 466), BACKGROUND)
    title_font = font(22)
    for column, (kind, label) in enumerate(MERCHANTS):
        key = "merchant_" + kind
        folder = TOOLS / (key + "_dungeons_ref")
        scene = idle_scene(folder / (key + ".bbmodel"))
        full = view(scene, 18, 12, (512, 512))
        full.save(folder / "preview.png")
        thumb = full.resize((262, 262), Image.Resampling.LANCZOS)
        x = column * 260
        lineup.paste(thumb, (x - 1, 4), thumb)
        ImageDraw.Draw(lineup).text((x + 130, 286), label, font=title_font, fill="#e9e5dc", anchor="mm")
        ImageDraw.Draw(closeups).text((x + 130, 23), label, font=title_font, fill="#e9e5dc", anchor="mm")
        for row, (yaw, pitch) in enumerate(((0, 0), (18, 12))):
            face = view(scene, yaw, pitch, (244, 198), closeup=True)
            closeups.paste(face, (x + 8, 46 + 212 * row), face)
    lineup.save(HERE / "merchants.png")
    closeups.save(HERE / "eyes.png")


if __name__ == "__main__":
    main()
