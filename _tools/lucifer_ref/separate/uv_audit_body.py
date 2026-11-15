"""Read-only source-texel audit of the six-cube Mossy Skeleton body.

Writes only sibling uv_audit_body.{json,md,png}. Does not rewrite the model,
texture, UVs, or duplicate source blocks. Reproduce with Python + numpy/Pillow/
matplotlib. Pixel footprint means UV rectangle coverage, not framebuffer use.
"""
from __future__ import annotations

import base64
from collections import Counter
import hashlib
import io
import json
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def plot_audit(original, coverage, out_path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    from matplotlib.colors import ListedColormap, BoundaryNorm
    from matplotlib.patches import Patch

    font = Path(r"C:\Windows\Fonts\msyh.ttc")
    if font.exists():
        font_manager.fontManager.addfont(str(font))
        plt.rcParams["font.family"] = "Microsoft YaHei"
    fig, axes = plt.subplots(2, 2, figsize=(16, 10.5), facecolor="#edf0e8")
    fig.suptitle("Mossy Skeleton 身体 UV：逐像素覆盖 / 复用审计", fontsize=20, y=0.97)
    y, x = np.indices(coverage.shape)
    checker = ((x + y) % 2).astype(float)
    checker = np.where(checker[..., None] > 0, [.28,.30,.28], [.20,.22,.20])
    alpha = original[:,:,3:4] / 255
    composited = original[:,:,:3] / 255 * alpha + checker * (1-alpha)
    axes[0,0].imshow(composited, interpolation="nearest", origin="upper")
    axes[0,0].set_title("原 T_MossySkeleton.png · 64×32", pad=13)
    cov_colors = ["#d5d9d0", "#4d92ad", "#b3438e"]
    axes[0,1].imshow(coverage, cmap=ListedColormap(cov_colors),
                     norm=BoundaryNorm([-.5,.5,1.5,2.5],3), interpolation="nearest")
    axes[0,1].set_title("UV 次数：未用 1104 / 一次 736 / 两次 208", pad=13)
    axes[0,1].legend(handles=[Patch(color=cov_colors[i],label=s) for i,s in
                              enumerate(["0 次", "1 次", "2 次（复用）"])],
                    loc="upper center", bbox_to_anchor=(.5,-.19), ncol=3, frameon=False)
    valid = original[:,:,3] >= 128
    effective = np.where(valid, coverage + 1, 0)
    eff_colors = ["#d5d9d0", "#d0392d", "#5b9b70", "#b3438e"]
    axes[1,0].imshow(effective, cmap=ListedColormap(eff_colors),
                     norm=BoundaryNorm([-.5,.5,1.5,2.5,3.5],4), interpolation="nearest")
    axes[1,0].set_title("有效皮肤 alpha≥128：750/750 已覆盖，其中 208 复用", pad=13)
    axes[1,0].legend(handles=[Patch(color=eff_colors[i],label=s) for i,s in
                              enumerate(["透明/低 alpha", "有效但未用（0）", "有效且一次", "有效且两次"])],
                    loc="upper center", bbox_to_anchor=(.5,-.19), ncol=2, frameon=False)
    unused = coverage == 0
    classes = np.zeros_like(coverage)
    classes[unused & (original[:,:,3] == 0)] = 1
    classes[unused & (original[:,:,3] > 0) & ~valid] = 2
    classes[unused & valid] = 3
    un_colors = ["#f0f2ed", "#969f97", "#df8b25", "#d0392d"]
    axes[1,1].imshow(classes,cmap=ListedColormap(un_colors),
                     norm=BoundaryNorm([-.5,.5,1.5,2.5,3.5],4), interpolation="nearest")
    axes[1,1].set_title("未用区：1095 全透明 + 9 个 alpha2/3 残留；有效皮肤 0", pad=13)
    axes[1,1].legend(handles=[Patch(color=un_colors[i],label=s) for i,s in
                              enumerate(["已用", "未用透明", "未用近透明", "未用有效（0）"])],
                    loc="upper center", bbox_to_anchor=(.5,-.19), ncol=2, frameon=False)
    for ax in axes.flat:
        ax.set_xlim(-.5,63.5);ax.set_ylim(31.5,-.5)
        ax.set_xticks(np.arange(0,64,8));ax.set_yticks(np.arange(0,32,4))
        ax.set_xticks(np.arange(-.5,64,1), minor=True)
        ax.set_yticks(np.arange(-.5,32,1), minor=True)
        ax.grid(which="minor", color="#26322c", linewidth=.25, alpha=.15)
        ax.tick_params(which="minor", length=0)
        ax.set_xlabel("u / 原图像素", labelpad=0);ax.set_ylabel("v / 原图像素")
    fig.text(.03,.035,"覆盖按当前 36 个面 UV 的整数 texel 区域统计；镜像 UV 仍引用同一源像素。未改模型，未复制素材块。",fontsize=11)
    fig.subplots_adjust(left=.055,right=.985,top=.90,bottom=.20,hspace=.70,wspace=.15)
    fig.savefig(out_path,dpi=150)
    plt.close(fig)


def main():
    model_path = HERE / "mossy_skeleton_body.bbmodel"
    source_path = HERE.parent / "T_MossySkeleton.png"
    source_model_path = HERE.parent.parent / "sunken_skeleton_ref/sunken_skeleton.bbmodel"
    doc = json.loads(model_path.read_text(encoding="utf-8"))
    olddoc = json.loads(source_model_path.read_text(encoding="utf-8"))
    original = np.array(Image.open(source_path).convert("RGBA"))
    embedded_png = base64.b64decode(doc["textures"][0]["source"].split(",",1)[1])
    embedded = np.array(Image.open(io.BytesIO(embedded_png)).convert("RGBA"))
    history_path = HERE / "history/mossy_skeleton_body_before_original_alpha.bbmodel"
    history = None
    if history_path.exists():
        history_doc = json.loads(history_path.read_text(encoding="utf-8"))
        history_png = base64.b64decode(history_doc["textures"][0]["source"].split(",",1)[1])
        history_image = np.array(Image.open(io.BytesIO(history_png)).convert("RGBA"))
        history = {"path": str(history_path), "sha256": digest(history_path),
                   "rgb_differing_pixels": int(np.any(history_image[:,:,:3] != original[:,:,:3], axis=2).sum()),
                   "alpha_differing_pixels": int((history_image[:,:,3] != original[:,:,3]).sum()),
                   "status": "Historical alpha modification; current source image restored."}
    height,width = original.shape[:2]
    assert (width,height) == (64,32) and doc["resolution"] == {"width":64,"height":32}
    assert len(doc["elements"]) == 6
    oldcubes = {c["name"]: c for c in olddoc["elements"]}
    coverage = np.zeros((height,width),dtype=int)
    owners = [[[] for x in range(width)] for y in range(height)]
    face_rows=[]
    for cube in doc["elements"]:
        for name,face in cube["faces"].items():
            if face.get("texture") is None:
                continue
            assert face["texture"]==0
            assert all(isinstance(v,(int,float)) and float(v).is_integer() for v in face["uv"])
            u,v,U,V = map(int,face["uv"])
            rect = [min(u,U),min(v,V),max(u,U),max(v,V)]
            x0,y0,x1,y1 = rect
            assert 0<=x0<=x1<=width and 0<=y0<=y1<=height
            owner = cube["name"] + "." + name
            coverage[y0:y1,x0:x1] += 1
            for yy in range(y0,y1):
                for xx in range(x0,x1):
                    owners[yy][xx].append(owner)
            face_rows.append({"face":owner,"uv":face["uv"],"rectangle_end_exclusive":rect,
                              "texels":(x1-x0)*(y1-y0),
                              "same_uv_as_sunken":face["uv"]==oldcubes[cube["name"]]["faces"][name]["uv"]})
    alpha=original[:,:,3]
    unused=coverage==0
    valid=alpha>=128
    reused=coverage>1
    shared=Counter(tuple(owners[y][x]) for y,x in zip(*np.nonzero(reused)))
    reuse_groups=[{"owners":list(k),"texels":v} for k,v in sorted(shared.items())]
    unused_low=[{"x":int(x),"y":int(y),"alpha":int(alpha[y,x]),"rgb":original[y,x,:3].tolist()}
                for y,x in zip(*np.nonzero(unused&(alpha>0)&~valid))]
    summary={"source_texels":int(coverage.size),"unique_uv_covered":int((coverage>0).sum()),
             "unused":int(unused.sum()),"once":int((coverage==1).sum()),
             "reused_unique_texels":int(reused.sum()),"max_reuse":int(coverage.max()),
             "face_texel_incidences":int(coverage.sum()),
             "valid_source_texels_alpha_ge_128":int(valid.sum()),
             "valid_used_once":int((valid&(coverage==1)).sum()),
             "valid_reused":int((valid&reused).sum()),"valid_unused":int((valid&unused).sum()),
             "unused_fully_transparent":int((unused&(alpha==0)).sum()),
             "unused_low_alpha":int((unused&(alpha>0)&~valid).sum()),
             "used_transparent":int(((coverage>0)&(alpha==0)).sum()),
             "used_low_alpha":int(((coverage>0)&(alpha>0)&~valid).sum())}
    report={"inputs_sha256":{str(p):digest(p) for p in (model_path,source_path,source_model_path)},
            "method":"Integer UV rectangles cover texels with min(u)<=x<max(u), min(v)<=y<max(v). Reversed UV endpoints still reference the same original pixels. Counts measure face-to-source reuse, not rendered pixel count.",
            "summary":summary,
            "embedded_texture":{"png_bytes_equal_to_source":embedded_png==source_path.read_bytes(),
                                "rgba_differing_pixels":int(np.any(embedded!=original,axis=2).sum()),
                                "rgb_equal_to_source":bool(np.array_equal(embedded[:,:,:3],original[:,:,:3])),
                                "alpha_equal_to_source":bool(np.array_equal(embedded[:,:,3],original[:,:,3])),
                                "alpha_exactly_source_threshold_128":bool(np.array_equal(embedded[:,:,3],np.where(valid,255,0)))},
            "historical_alpha_change":history,
            "all_36_face_uvs_equal_inherited_sunken":all(x["same_uv_as_sunken"] for x in face_rows),
            "face_uvs":face_rows,"coverage_counts_by_v_then_u":coverage.tolist(),
            "original_alpha_by_v_then_u":alpha.tolist(),"texel_owners_by_v_then_u":owners,
            "reuse_groups":reuse_groups,"unused_nonzero_alpha_texels":unused_low,
            "strict_no_source_texel_reuse_satisfied":False,
            "user_clarification":"Faithfulness takes priority. The sole allowed reuse exception is bilateral shared UV supported by the supplied Sunken skeleton source. This is not proof of a complete original Mossy mesh.",
            "all_reuse_within_documented_sunken_bilateral_exception":all(x["same_uv_as_sunken"] for x in face_rows),
            "every_valid_source_texel_used_satisfied":summary["valid_unused"]==0,
            "every_2048_texel_used_satisfied":summary["unused"]==0}
    (HERE/"uv_audit_body.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    lines=["# 苔藓骷髅身体：原图逐像素 UV 审计","",
           "**当前内嵌 PNG 与原 T_MossySkeleton.png 字节完全相等、RGBA 差异 0；这项可以称源纹理零差异。模型本身不据此获得零差异验收。** 有效皮肤内容全部已用；左右臂共享 104 个源像素、左右腿共享另外 104 个，均使用两次。共享直接有给定 Sunken 骨架的 UV 记录，属于用户最新允许的唯一例外；没有取得原 Mossy 全网格，不能将此说成原 Mossy 全部左右面已确认。","",
           "## 审计范围与方法","",f"当前模型 SHA-256：`{digest(model_path)}`",f"原图 SHA-256：`{digest(source_path)}`","",
           "只读取 `mossy_skeleton_body.bbmodel` 的 6 个方块、36 个面和 `T_MossySkeleton.png` 的 64×32 原图。UV 范围取最小端点包含、最大端点不包含，按每个整数 texel 记录引用它的面；UV 镜像或反向不会获得新源像素。统计是面到源像素的覆盖，不是最终屏幕绘制次数。","",
           "模型全部 36 个面 UV 与**给定的 Sunken 骨架**对应身体面完全相同。双臂改为中立姿势不改变 UV 统计。当前内嵌原 PNG 字节完全相等，RGB 和 alpha 均无差异。此前版本曾对 100 个像素做 alpha 二值化（RGB 无差异），该变更已纠正；历史模型保存在 `history/mossy_skeleton_body_before_original_alpha.bbmodel`。100 处差异是已纠正的历史事实，不能继续记为当前差异。","",
           "## 逐像素覆盖结果","","| 项目 | 像素数 |","|---|---:|",
           "| 原图总面积 | 2048 |","| UV 唯一覆盖面积 | 944 |","| 只被一个面引用 | 736 |","| 被两个面引用 | 208 |","| 未被任何面引用 | 1104 |","| 36 面合计 texel 引用次数 | 1152 |","",
           "| 原图内容分类 | 总量 | 未用 | 一次使用 | 两次使用 |","|---|---:|---:|---:|---:|",
           "| 有效内容 alpha≥128 | 750 | **0** | 542 | **208** |",
           "| 全透明 alpha=0 | 1250 | 1095 | 155 | 0 |",
           "| 近透明 alpha1..127 | 48 | 9 | 39 | 0 |","",
           "750 个有效像素的覆盖率为 100%；其中 208/750（27.73%）被左右对称肢体复用。未覆盖位置没有 alpha≥128 的皮肤内容。","",
           "## 复用区域与面配对","",
           "双臂区域：侧面 `[0,18,8,30)` 共 96 像素，加上顶/底 `[2,16,6,18)` 共 8 像素，合计 104。双腿区域：侧面 `[40,18,48,30)` 共 96，加上顶/底 `[42,16,46,18)` 共 8，合计 104。两组互不重叠，均为有效不透明内容。","",
           "| 引用同一源像素的面 | 共享像素数 |","|---|---:|"]
    for group in reuse_groups:lines.append("| `"+"` / `".join(group["owners"])+"` | "+str(group["texels"])+" |")
    lines += ["","## 未用区是否遗漏皮肤","",
              "1095 个未用像素完全透明，可确认为原始留白。其余 9 个仅 alpha=2 或 3（0.78% / 1.18% 不透明度），在 alpha≥128 的审计分类中不属于有效皮肤，但当前原 PNG 完整保留了这些值，并未修改。它们位于图块边缘且不形成不透明皮肤区域，符合导出残留的特征；未取得原作者导出记录，不能断言残留的具体来源。","",
              "| 原图坐标 (u,v) | alpha |","|---|---:|"]
    for row in unused_low:lines.append(f"| ({row['x']},{row['y']}) | {row['alpha']} |")
    lines += ["","## 新约束与原有要求如何解释","",
              "1. 用户已澄清以忠实原作为准，仅允许有原始依据的左右对称共享。当前 208 个共享像素全部能追溯至指定 Sunken 源骨架，按这项唯一例外记录，不再把消除它们作为目标。此依据不等于原 Mossy 网格证据。",
              "2. 全部 750 个 alpha≥128 有效皮肤像素已用；透明留白未额外贴到未知面或占位面上。原图数据本身全部保留，没有为了覆盖率去改变原图。",
              "3. 将共享区域复制到图集别处，只能让图集坐标不重叠，仍然重复利用同一源块，因此不算满足用户的新限制。",
              "4. 未知隐藏面、未取得的原始几何和未能判明的光照/抗锯齿差异均不得通过。可见纹理的非零残差数值拟合只能支持 UV 对应，不能写成像素完全一致、部件验收或整体完全还原。逐部位证据见 `uv_audit_body_parts.md/json`。","",
              "## 证据与复现","",
              "- `uv_audit_body.png`：原图、逐像素引用次数、有效内容覆盖、未用区分类四幅热图。",
              "- `uv_audit_body.json`：完整 32×64 覆盖矩阵、原 alpha 矩阵、每个 texel 的面归属和文件哈希。",
              "- `python _tools/lucifer_ref/separate/uv_audit_body.py`：重建审计输出，只写同目录 `uv_audit_body.*`。",
              "- 本次没有改模型、贴图、UV、骨骼，也没有通过复制源块绕过限制。",""]
    (HERE/"uv_audit_body.md").write_text("\n".join(lines),encoding="utf-8")
    plot_audit(original,coverage,HERE/"uv_audit_body.png")
    assert digest(model_path)==report["inputs_sha256"][str(model_path)]
    assert digest(source_path)==report["inputs_sha256"][str(source_path)]
    print(json.dumps(summary,ensure_ascii=False))


if __name__=="__main__":main()
