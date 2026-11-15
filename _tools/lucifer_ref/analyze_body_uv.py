"""Reproduce body alpha comparisons and source-render texel matching.

Run: python _tools/lucifer_ref/analyze_body_uv.py
Requires: numpy, scipy, Pillow, matplotlib. Source PNGs are never modified.
Outputs: UV_BODY_PIXEL_FITS.json and UV_BODY_PIXEL_EVIDENCE.png.
No model, animation, datapack, or shared files are written.
"""
import base64
import hashlib
import io
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.optimize import differential_evolution

HERE = Path(__file__).resolve().parent


def fit_face(reference, texture, uv, flip, bounds, popsize, maxiter):
    u, v, U, V = uv
    candidate = texture[v:V, u:U]
    if flip:
        candidate = candidate[:, ::-1]
    candidate = candidate.reshape(-1, 3)
    centered = candidate - candidate.mean(axis=0)
    yy, xx = np.mgrid[:8, :8]
    xx, yy = xx.flatten() + 0.5, yy.flatten() + 0.5

    def objective(params, details=False):
        ox, oy, ux, uy, vx, vy = params
        px = np.rint(ox + xx * ux + yy * vx).astype(int)
        py = np.rint(oy + xx * uy + yy * vy).astype(int)
        sampled = reference[py, px]
        slope = (centered * (sampled - sampled.mean(axis=0))).sum(axis=0)
        slope /= np.maximum((centered * centered).sum(axis=0), 1e-9)
        intercept = sampled.mean(axis=0) - slope * candidate.mean(axis=0)
        error = float(((sampled - (candidate * slope + intercept)) ** 2).mean())
        if details:
            return {
                "mse": error,
                "rmse": math.sqrt(error),
                "lighting_slope_rgb": slope.tolist(),
                "lighting_intercept_rgb": intercept.tolist(),
                "sampled_render_rgb": sampled.tolist(),
                "sample_positions_xy": np.column_stack([px, py]).tolist(),
            }
        return error

    result = differential_evolution(
        objective, bounds, seed=42, popsize=popsize, maxiter=maxiter,
        tol=0.001, polish=False,
    )
    return {
        "uv": uv, "flip_x": flip,
        "projection_ox_oy_ux_uy_vx_vy": result.x.tolist(),
        "optimizer": {"seed": 42, "popsize": popsize, "maxiter": maxiter,
                      "tol": 0.001, "polish": False, "bounds": bounds},
        **objective(result.x, details=True),
    }


def write_evidence(reference, texture, front, side):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager

    font = Path(r"C:\Windows\Fonts\msyh.ttc")
    if font.exists():
        font_manager.fontManager.addfont(str(font))
        plt.rcParams["font.family"] = "Microsoft YaHei"
    fig, axes = plt.subplots(2, 4, figsize=(16, 10.4), facecolor="#edf0e8")
    fig.suptitle("Mossy Skeleton：原图像素与继承 UV 的数值核验", fontsize=19, y=0.97)
    for row, (label, fit) in enumerate([("头正面 north", front), ("头侧面 west", side)]):
        u, v, U, V = fit["uv"]
        raw = texture[v:V, u:U]
        sampled = np.array(fit["sampled_render_rgb"]).reshape(8, 8, 3)
        points = np.array(fit["sample_positions_xy"])
        predicted = raw * np.array(fit["lighting_slope_rgb"])
        predicted += np.array(fit["lighting_intercept_rgb"])
        residual = np.sqrt(((sampled - predicted) ** 2).mean(axis=2))
        axes[row, 0].set_facecolor("#28302c")
        axes[row, 0].imshow(reference[:330, :330].astype(np.uint8))
        axes[row, 0].scatter(points[:, 0], points[:, 1], s=5, c="#ff9b3f")
        axes[row, 0].set_title(label + "：原作 64 点采样", pad=14)
        axes[row, 1].imshow(raw.astype(np.uint8), interpolation="nearest")
        axes[row, 1].set_title("原纹理 UV " + str(fit["uv"]), pad=14)
        axes[row, 2].imshow(sampled.astype(np.uint8), interpolation="nearest")
        axes[row, 2].set_title("原作渲染 64 点重排", pad=14)
        plot = axes[row, 3].imshow(residual, vmin=0, vmax=1, cmap="magma", interpolation="nearest")
        axes[row, 3].set_title("统一光照拟合后残差\nRMSE %.4f / 255" % fit["rmse"], pad=14)
        fig.colorbar(plot, ax=axes[row, 3], fraction=0.045)
        for column in range(4):
            axes[row, column].set_xticks([])
            axes[row, column].set_yticks([])
    fig.text(0.03, 0.035,
             "保留每个 texel 的排列；仅拟合整面仿射投影与统一 RGB 光照。原作渲染：Minecraft Dungeons / Mojang。\n"
             "该图证明正脸及可见头侧面的 UV 区域与方向，不替代未提供的原作背面网格。", fontsize=11)
    fig.subplots_adjust(left=0.03, right=0.97, top=0.89, bottom=0.12, hspace=0.32, wspace=0.2)
    fig.savefig(HERE / "UV_BODY_PIXEL_EVIDENCE.png", dpi=150)
    plt.close(fig)


def main():
    bbpath = HERE.parent / "sunken_skeleton_ref" / "sunken_skeleton.bbmodel"
    bb = json.loads(bbpath.read_text(encoding="utf-8"))
    source_bytes = base64.b64decode(bb["textures"][0]["source"].split(",", 1)[1])
    old = Image.open(io.BytesIO(source_bytes)).convert("RGBA")
    new = Image.open(HERE / "T_MossySkeleton.png").convert("RGBA")
    assert old.size == new.size == (64, 32)
    names = {"head", "body", "right_arm", "left_arm", "right_leg", "left_leg"}
    faces = []
    for cube in bb["elements"]:
        if cube["name"] not in names:
            continue
        for face, spec in cube["faces"].items():
            u, v, U, V = spec["uv"]
            crop = (min(u, U), min(v, V), max(u, U), max(v, V))
            a = np.array(old.crop(crop).getchannel("A"))
            b = np.array(new.crop(crop).getchannel("A"))
            faces.append({
                "cube": cube["name"], "face": face, "uv": spec["uv"],
                "raw_alpha_equal_fraction": float((a == b).mean()),
                "binary_alpha_128_equal_fraction": float(((a >= 128) == (b >= 128)).mean()),
            })
    texture = np.array(new.convert("RGB"), dtype=float)
    reference = np.array(Image.open(HERE / "MCD_Mossy_Skeleton.png").convert("RGB"), dtype=float)
    front = fit_face(reference, texture, [8, 8, 16, 16], False,
                     [(28, 36), (85, 100), (18, 20), (5, 10), (-0.5, 0.5), (17, 21)], 24, 300)
    alternatives = []
    for u in (0, 16, 24):
        for flip in (False, True):
            alternatives.append(fit_face(
                reference, texture, [u, 8, u + 8, 16], flip,
                [(179, 189), (145, 169), (13, 16), (-12, -7), (-0.5, 0.5), (18, 22)], 16, 180))
    best = min(alternatives, key=lambda item: item["mse"])
    report = {
        "method": "All 64 texel centers per face; affine image projection and one channel-wise RGB affine lighting transform.",
        "source_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in
                          (bbpath, HERE / "T_MossySkeleton.png", HERE / "MCD_Mossy_Skeleton.png")},
        "alpha_histogram": dict(Counter(np.array(new.getchannel("A")).flatten().tolist())),
        "body_faces": faces, "head_front": front,
        "head_side_best": best, "head_side_alternatives": alternatives,
        "limitations": "Only the front and visible head side are numerically matched. This is not an original Mojang mesh/UV export.",
    }
    (HERE / "UV_BODY_PIXEL_FITS.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_evidence(reference, texture, front, best)
    print(json.dumps({"front_rmse": front["rmse"], "side_rmse": best["rmse"],
                      "side_uv": best["uv"], "side_flip": best["flip_x"]}))


if __name__ == "__main__":
    main()
