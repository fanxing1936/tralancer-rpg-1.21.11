"""Re-evaluate finite visible-region texture evidence; never optimize or edit.

Fixed samples are stored in uv_audit_body_samples.json. This script re-reads
the original PNGs and fits one RGB affine lighting transform per sample set.
Nonzero residuals can support UV correspondence but never zero-difference
acceptance. Boundaries, alpha, hidden faces and original geometry are excluded.
"""
import base64
import hashlib
import io
import json
from pathlib import Path

import numpy as np
from PIL import Image

HERE=Path(__file__).resolve().parent
REF=HERE.parent


def main():
    manifest=json.loads((HERE/"uv_audit_body_samples.json").read_text(encoding="utf-8"))
    source=np.array(Image.open(REF/"T_MossySkeleton.png").convert("RGBA"))
    model_path=HERE/"mossy_skeleton_body.bbmodel"
    model_bytes=model_path.read_bytes()
    doc=json.loads(model_bytes)
    png=base64.b64decode(doc["textures"][0]["source"].split(",",1)[1])
    embedded=np.array(Image.open(io.BytesIO(png)).convert("RGBA"))
    results=[]
    for entry in manifest["cases"]:
        reference=np.array(Image.open(REF/entry["reference"]).convert("RGBA"))
        xy=np.array(entry["source_pixels_xy"],dtype=int)
        pq=np.array(entry["reference_pixels_xy"],dtype=int)
        x=source[xy[:,1],xy[:,0],:3].astype(float)
        y=reference[pq[:,1],pq[:,0],:3].astype(float)
        centered=x-x.mean(axis=0)
        slope=(centered*(y-y.mean(axis=0))).sum(axis=0)/np.maximum((centered**2).sum(axis=0),1e-12)
        intercept=y.mean(axis=0)-slope*x.mean(axis=0)
        residual=y-(x*slope+intercept)
        row=dict(entry)
        row.update({"samples":len(x),"source_sample_rgba":source[xy[:,1],xy[:,0]].tolist(),
                    "reference_sample_rgba":reference[pq[:,1],pq[:,0]].tolist(),
                    "lighting_slope_rgb":slope.tolist(),"lighting_intercept_rgb":intercept.tolist(),
                    "rmse_rgb_0_to_255":float(np.sqrt((residual**2).mean())),
                    "max_absolute_rgb_residual":float(np.abs(residual).max()),
                    "zero_difference_accepted":False,
                    "reason_not_accepted":"RGB centers only, fitted lighting not original lighting; nonzero residual; boundaries/alpha/whole-part geometry and hidden surfaces not verified."})
        results.append(row)
    matrix=[
        {"part":"头部", "supported":"north、参考图可见west、up的纹理像素中心排列", "unknown":"east、south、down；完整边界、原始几何/比例与原始光照", "accepted":False},
        {"part":"躯干", "supported":"Aiming中south下部43点、west下部17点", "unknown":"上部被遮挡区域；north、up、down；完整孔洞边界、几何厚度与原始姿态", "accepted":False},
        {"part":"双臂", "supported":"Standing画面右侧可见手臂一长面的18点；指定Sunken双臂共享UV记录", "unknown":"另一臂原作全表面；端面；Aiming伸出臂本次未稳定对应；原Mossy骨骼归属及肢体朝向", "accepted":False},
        {"part":"双腿", "supported":"Aiming远腿18点与近腿22点支持同一[42,18,44,30]区域的双侧镜像使用", "unknown":"其他长面、端面、被遮挡上缘；原Mossy骨骼归属与动态几何", "accepted":False},
        {"part":"所有隐藏面", "supported":"没有额外证据", "unknown":"原始网格、UV与对应视角缺失", "accepted":False},
        {"part":"骨架与比例", "supported":"使用给定Sunken骨架的文件来源可以追溯", "unknown":"未取得原Mossy网格；投影采样参数不是几何重建证明", "accepted":False},
    ]
    report={"model_sha256":hashlib.sha256(model_bytes).hexdigest(),
            "source_png_sha256":hashlib.sha256((REF/"T_MossySkeleton.png").read_bytes()).hexdigest(),
            "embedded_png_bytes_exact":png==(REF/"T_MossySkeleton.png").read_bytes(),
            "rgba_differing_pixels":int(np.any(source!=embedded,axis=2).sum()),
            "acceptance_policy":"Only exact original PNG bytes qualify as zero-difference. All affine RGB fits are correspondence evidence, not part acceptance. Unknown surfaces never pass.",
            "bilateral_exception_scope":"Only source-backed bilateral sharing, as allowed by the user. Given Sunken mappings are documented; no original full Mossy mesh was obtained.",
            "historical_alpha_difference":"100 alpha pixel changes in the earlier binary-alpha model were corrected by restoring original PNG bytes. Current RGBA difference is zero.",
            "registration_limit":"Finite ROI/candidate registration was stopped. Fixed center samples do not test borders/antialiasing/alpha and are not exact source mesh coordinates. No further optimization is performed by this script.",
            "parts_matrix":matrix,"visible_region_evidence":results}
    (HERE/"uv_audit_body_parts.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    lines=["# 苔藓骷髅逐部位证据：支持对应 ≠ 零差异验收","",
           "**当前唯一可称零差异的项目是内嵌原 PNG 文件：字节完全相等，RGBA 差异 0。没有任何完整身体部位获得零差异验收。**","",
           f"核验模型 SHA-256：`{report['model_sha256']}`","",
           "原先 100 处 alpha 二值化差异已由主任务恢复原 PNG 纠正；该差异仅保留为历史记录。原图所有 alpha 数据当前均在，不能把旧差异继续记为当前缺陷。","",
           "## 可见纹理的有限数值核验","",
           "以下从两张原作 PNG 取实际像素，与原纹理 texel 中心排列做有限仿射投影匹配，再拟合整组统一 RGB 光照。RMSE 非零；无法判明原作光照、抗锯齿等差异时，按用户标准仍未验证。采样只涉及像素中心，不验证完整边缘、alpha、实际立方体尺寸或隐藏面。候选已有限尝试并停止，没有无限优化来强求低误差。","",
           "| 位置 | 原图区域 | 样本 | RGB RMSE /255 | 证据范围 | 零差异验收 |","|---|---|---:|---:|---|---|"]
    for row in results:
        lines.append(f"| {row['part']} | `{row['source_uv']}` | {row['samples']} | {row['rmse_rgb_0_to_255']:.5f} | {row['coverage']} | **未通过** |")
    lines += ["","Aiming伸出手臂的候选未稳定对应，表中残差只记录失败尝试，不能作支持证据。其余低残差仅支持所列可见纹理区域的 UV 对应，不能用“已证实部件”“完全一致”“已验收”替代。","",
              "## 逐部位检查矩阵","","| 部位 | 有限支持 | 未能证实 / 不能通过项 | 验收 |","|---|---|---|---|"]
    for row in matrix:lines.append(f"| {row['part']} | {row['supported']} | {row['unknown']} | **未通过** |")
    lines += ["","## 共享 UV 的证据边界","",
              "指定 Sunken 文件明确记录左右臂与左右腿共用区域，这是有文件来源的事实，按用户澄清允许为唯一例外。腿部两块可见区域的数值样本也支持使用同一源区域的镜像方向，但仍有非零误差且只有部分可见表面。未取得原 Mossy 完整网格，因此不能宣称原 Mossy 全部左右表面或骨骼已经核验。","",
              "## 复现与下一步证据","",
              "运行 `python _tools/lucifer_ref/separate/uv_audit_body_parts.py` 可从原图重采样并重算残差；`uv_audit_body_samples.json` 保存固定源像素坐标与参考图坐标，`uv_audit_body_parts.json` 保存每点 RGBA、拟合参数和剩余差异。脚本不再次优化，不改模型或素材。","",
              "要完成用户要求的任意细差重做并验收，需要原 Mossy 几何/UV源文件或足以显示剩余面的可靠原作视角；未知面继续保持未验收，不能靠绘制、镜像推测或这张矩阵补出证据。",""]
    (HERE/"uv_audit_body_parts.md").write_text("\n".join(lines),encoding="utf-8")
    assert model_path.read_bytes()==model_bytes
    print(json.dumps({"png_bytes_exact":report["embedded_png_bytes_exact"],"rgba_differences":report["rgba_differing_pixels"],"parts_accepted":0,"sample_cases":len(results),"model_sha256":report["model_sha256"]}))


if __name__=="__main__":main()
