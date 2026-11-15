"""小人动作研究：读取原始 25 fps 帧，输出独立数字轨道；不修改 bbmodel。

眼/口质心是直接测量；从单视图恢复深度、手脚角度以及头身分配仍是推断。
输出限于 heart_of_ender_ref/m3_motion/inner_*，不访问 Blockbench 或公共管线。
"""
from __future__ import annotations

import csv
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import label
from scipy.spatial.transform import Rotation

ROOT = Path(__file__).resolve().parent
REF = ROOT / "heart_of_ender_ref"
OUT = REF / "m3_motion"
SOURCES = {"docile": ("MCD_Arch-Illager_Docile", 120),
           "anxious": ("MCD_Arch-Illager_Anxious", 200),
           "fourside": ("MCD_Arch-Illager_Fourside", 50)}
KEYS = {"docile": [0, 18, 32, 38, 50, 62, 72, 85, 90, 100, 112, 119],
        "anxious": [0, 22, 27, 35, 39, 45, 70, 76, 83, 97, 115, 140, 155, 179, 199],
        "fourside": list(range(50))}
POSE_NOTES = {
    "docile": {0: "初始前倾、双足分开、可见侧细臂下垂", 18: "下降且头身姿势改变", 32: "足底低位，头顶尚非最低",
               38: "亮轮廓重心最低附近，头顶条更直", 50: "开始回升，眼口白标记此刻不可见，偏移插值",
               62: "中间高度，头向左前倾", 72: "继续上浮，脚轮廓收拢", 85: "亮轮廓重心高点",
               90: "足底高点、双足再次分开", 100: "高位回落、足前伸", 112: "趋近初姿", 119: "原片末帧，下一循环回到s000"},
    "anxious": {0: "三分之四侧倾初态", 22: "上浮、冠更直", 27: "开始转侧", 35: "侧面、可见细臂朝画面左前伸",
                39: "侧面高位、双足后收", 45: "保持侧面开始下降", 70: "侧面保持尾段", 76: "回转，两眼重新展开",
                83: "近正面、前伸臂收回", 97: "正面低点、双足分开", 115: "正面结束并上浮", 140: "缓慢转回三分之四",
                155: "上浮高点", 179: "下降，细臂仍斜下", 199: "末帧细臂仍较s000展开，循环接缝保留差异"},
    "fourside": {0: "近直立、双侧细臂外展", 3: "向画面右倾", 4: "迅速回正", 6: "后仰、抬脸",
                 8: "前收、脚分开", 9: "大幅前俯、投影高度缩短", 10: "保留前俯", 11: "快速回弹",
                 13: "短暂正面", 16: "侧倾、双足折起", 19: "竖直略后仰", 21: "斜向侧摆",
                 25: "双臂近平伸、足张开", 27: "较正面、双臂展开", 28: "细臂快速下收", 31: "再次右倾抬脸",
                 34: "第二次后仰", 36: "反向摆动", 37: "第二次大幅前俯", 38: "迅速回弹",
                 42: "侧倾加深", 45: "大侧倾、低矮投影", 46: "快速回到直立；用可见宽冠轴测量，脸角保留为参考", 47: "回正之后轻摆；可见宽冠轴测量",
                 49: "结尾仍有斜姿，3秒后收势为推断"}}
# 对原生并排暴露的43..45末端误差，采用可达端点的负深度分支 E1。
# 只限制2D端点；不是原始关节数据。42的另一臂身份不定且对当前右肩不可达，保持原轨道；46不改。
ENDPOINT_E1 = {
    43: {"inner_arm_left": [100., 331.], "inner_arm_right": [231., 447.], "inner_leg_right": [214., 406.]},
    44: {"inner_arm_left": [94., 333.], "inner_arm_right": [280., 447.], "inner_leg_right": [220., 411.]},
    45: {"inner_arm_left": [94., 340.], "inner_arm_right": [294., 418.], "inner_leg_right": [225.07, 412.65]},
}
# 每行为：源帧、左臂前后、左臂外展、右臂前后、右臂外展、左腿前后、右腿前后、腿分开。
# 这些是按可见末端方向选定的刚体适配角；不是原始游戏骨骼数据。左右按已批准模型命名。
LIMBS = {
    "docile": [[0, -12, 8, -5, 4, -9, 8, 6], [18, -17, 12, -8, 5, -4, 2, 5],
               [32, -23, 18, -12, 5, 2, -7, 8], [38, -25, 20, -13, 6, 4, -8, 9],
               [50, -13, 11, -8, 4, -8, 5, 6], [62, -3, 1, -1, 2, -2, 10, 3],
               [72, 4, -2, 4, 0, 7, -3, 6], [85, 9, 4, 5, 1, 18, -5, 10],
               [90, 10, 8, 4, 2, 21, -8, 11], [100, 3, 10, 0, 4, 14, -2, 9],
               [112, -8, 9, -3, 5, -3, 6, 7], [119, -12, 8, -5, 4, -9, 8, 6]],
    "anxious": [[0, -8, 12, -3, 5, -6, 4, 7], [22, -6, 8, -2, 4, 1, -2, 6],
                [27, -16, 12, -8, 8, 2, -4, 7], [35, -78, 12, -38, 10, -25, -13, 9],
                [39, -80, 13, -40, 10, -27, -16, 10], [45, -76, 13, -38, 11, -14, -8, 8],
                [70, -66, 16, -31, 10, 6, -4, 10], [76, -56, 24, -24, 9, 9, -6, 12],
                [83, -36, 26, -14, 7, 8, -6, 12], [97, -14, 12, -5, 5, 1, -2, 9],
                [115, -10, 16, -4, 6, -2, 4, 7], [140, -18, 24, -8, 8, 10, -4, 10],
                [155, -17, 27, -9, 9, 9, -8, 11], [179, -20, 28, -9, 8, -3, 5, 10],
                [199, -21, 29, -10, 8, -7, 5, 9]],
    "fourside": [[0, -18, 73, -12, 72, 8, -15, 12], [3, -20, 76, -15, 70, -17, 8, 13],
                 [4, -18, 72, -12, 71, 0, -12, 12], [6, -22, 74, -13, 72, 15, -8, 14],
                 [8, -14, 78, -14, 72, -4, 21, 17], [9, -8, 54, -8, 55, -20, -6, 10],
                 [10, -7, 52, -7, 54, -18, -4, 10], [11, -16, 68, -12, 63, 15, -13, 13],
                 [13, -18, 72, -12, 49, 5, -16, 14], [16, -12, 78, -10, 74, -30, 13, 17],
                 [19, -18, 74, -13, 70, -7, 8, 10], [21, -20, 73, -14, 70, -17, -9, 12],
                 [25, -15, 85, -12, 84, 20, -15, 20], [27, -18, 80, -13, 77, 24, -18, 20],
                 [28, -5, 24, -2, 26, 4, -10, 13], [31, -20, 73, -15, 70, -9, 5, 12],
                 [34, -22, 76, -14, 74, 8, -15, 13], [36, -16, 71, -12, 70, -7, 8, 12],
                 [37, -8, 51, -8, 54, -23, -6, 10], [38, -16, 72, -13, 65, 19, -11, 16],
                 [42, -13, 82, -10, 78, -26, 15, 18], [45, -14, 79, -10, 75, -32, 12, 17],
                 [46, -18, 71, -12, 70, -9, 8, 13], [49, -18, 72, -12, 66, 3, -9, 14]],
}


def rmat(e):
    return Rotation.from_euler("xyz", e, degrees=True).as_matrix()


def angles(m):
    return Rotation.from_matrix(m).as_euler("xyz", degrees=True)


def clean(v):
    if isinstance(v, np.ndarray):
        return [round(float(x), 6) for x in v]
    return v


def components(mask, minimum=9):
    lab, count = label(mask, structure=np.ones((3, 3)))
    result = []
    for i in range(1, count + 1):
        yy, xx = np.where(lab == i)
        if len(xx) >= minimum:
            result.append({"area": len(xx), "center": np.array([xx.mean(), yy.mean()]),
                           "bbox": [int(xx.min()), int(yy.min()), int(xx.max()), int(yy.max())]})
    return sorted(result, key=lambda x: x["area"], reverse=True)


def measure_frame(path, previous):
    a = np.asarray(Image.open(path).convert("RGBA"))
    r, g, b, alpha = a.transpose(2, 0, 1)
    eye_mask = (alpha > 0) & (r < 250) & (g < 170) & (b > 230)
    eye = components(eye_mask)[:2]
    split = False
    if len(eye) == 1:
        yy, xx = np.where(eye_mask)
        points = np.column_stack((xx, yy))
        _, _, vt = np.linalg.svd(points-points.mean(axis=0), full_matrices=False)
        projected = points@vt[0]
        subset = projected < np.median(projected)
        eye = []
        for keep in (subset, ~subset):
            pts = points[keep]
            eye.append({"area": len(pts), "center": pts.mean(axis=0),
                        "bbox": [int(pts[:, 0].min()), int(pts[:, 1].min()), int(pts[:, 0].max()), int(pts[:, 1].max())]})
        split = True
    if len(eye) != 2:
        raise ValueError(f"眼形连通域不足两块：{path}")
    eye.sort(key=lambda x: x["center"][0])
    if previous is not None:
        direct = sum(np.linalg.norm(eye[i]["center"] - previous[i]) for i in range(2))
        reverse = sum(np.linalg.norm(eye[1-i]["center"] - previous[i]) for i in range(2))
        if reverse < direct:
            eye.reverse()
    ep = np.array([x["center"] for x in eye])
    whites = components((alpha > 0) & (r > 245) & (g > 245) & (b > 245))
    candidates = list(itertools.permutations(range(len(whites)), 2))
    pair = min(candidates, key=lambda p: sum(np.linalg.norm(whites[p[i]]["center"]-ep[i]) for i in range(2))) if candidates else []
    wp = np.array([whites[i]["center"] for i in pair]) if pair else None
    if wp is not None and np.max(np.linalg.norm(wp-ep, axis=1)) > 65:
        wp = None
    yy, xx = np.where((alpha > 0) & (np.max(a[:, :, :3], axis=2) > 128))
    crown_rows = []
    for cy in range(int(yy.min())+15, int(yy.min()+.27*(yy.max()-yy.min()))):
        cx = np.where(alpha[cy] > 0)[0]
        if len(cx):
            crown_rows.append([cy, float(cx.mean())])
    crown_rows = np.asarray(crown_rows)
    slope = float(np.polyfit(crown_rows[:, 0], crown_rows[:, 1], 1)[0])
    crown_axis = np.array([-slope, -1.]); crown_axis /= np.linalg.norm(crown_axis)
    return {"eye_centers": ep, "mouth_centers": wp, "connected_eye_split_inferred": split,
            "eye_areas": [x["area"] for x in eye], "eye_bboxes": [x["bbox"] for x in eye],
            "mouth_areas": [whites[i]["area"] for i in pair] if wp is not None else [],
            "mouth_measured": wp is not None,
            "crown_axis_screen": crown_axis,
            "crown_axis_method": "alpha轮廓顶部：y_min+15 到 y_min+0.27*轮廓高度，各行质心线性拟合；仅用于Docile/Anxious长条清楚的段",
            "bright_centroid": [float(xx.mean()), float(yy.mean())],
            "bright_bbox": [int(xx.min()), int(yy.min()), int(xx.max()), int(yy.max())]}, ep


def face_orientation(measure):
    """拟合正交面：两个标记间距/上下距离是适配假设，深度分支固定为参考可见侧。

    两个二维列向量用最大奇异值归一后补出深度；不引入任何 scale 动画。
    """
    ep, wp = measure["eye_centers"], measure["mouth_centers"]
    # 模型 +X 从画面右眼指向左眼；+Y 与白色口部标记相反。
    x = (ep[0] - ep[1]) / 2.45
    y = (ep.mean(axis=0) - wp.mean(axis=0)) / 0.60
    if measure.get("use_crown_axis"):
        y = np.array(measure["crown_axis_screen"])*np.linalg.norm(y)
    if "manual_face_quad_px" in measure:
        tl, tr, br, bl = np.array(measure["manual_face_quad_px"], dtype=float)
        x = ((tl-tr)+(bl-br))/2/4.2
        y = ((tl-bl)+(tr-br))/2/2.45
    a = np.column_stack((x, y))
    a[1] *= -1  # 画面 y 向下 -> 相机 y 向上
    scale = float(np.linalg.svd(a, compute_uv=False)[0])
    a /= scale
    xz = -math.sqrt(max(0, 1-float(a[:, 0]@a[:, 0])))
    yz = -float(a[:, 0]@a[:, 1]) / xz if abs(xz) > 1e-5 else math.sqrt(max(0, 1-float(a[:, 1]@a[:, 1])))
    axis_x = np.r_[a[:, 0], xz]
    axis_y = np.r_[a[:, 1], yz]
    axis_z = np.cross(axis_x, axis_y)
    raw = np.column_stack((axis_x, axis_y, axis_z))
    u, _, vt = np.linalg.svd(raw)
    rot = u@vt
    if np.linalg.det(rot) < 0:
        u[:, -1] *= -1
        rot = u@vt
    return rot, scale


def rotation_from_screen_axes(x_screen, y_screen, y_depth_sign=1):
    """屏幕方向+投影长度恢复正交轴；Y深度分支明确保留为推断。"""
    x_direction = np.array(x_screen, dtype=float)
    x_direction /= np.linalg.norm(x_direction)
    y = np.r_[y_screen, y_depth_sign*math.sqrt(max(0, 1-float(np.dot(y_screen, y_screen))))]
    z_per_x = -float(x_direction@y[:2])/y[2]
    magnitude = 1/math.sqrt(1+z_per_x*z_per_x)
    x = np.r_[x_direction*magnitude, z_per_x*magnitude]
    return np.column_stack((x, y, np.cross(x, y)))


def get_rig():
    path = REF / "m2_endcaps" / "R2.bbmodel"
    doc = json.loads(path.read_text(encoding="utf-8"))
    groups = {g["name"]: g for g in doc["groups"]}
    return path, groups


def build_source(stem, measures, groups, camera):
    parent = rmat(groups["shell_root"]["rotation"])
    root_pivot = np.array(groups["inner_root"]["origin"], dtype=float)
    head_pivot = np.array(groups["inner_head"]["origin"], dtype=float)
    camera_basis = np.array(camera["basis_right_up_viewer"])
    # 角度只用于头/躯干分配。总头方向由实测面部轴确定；不能由单视图证明关节深度。
    rotations, head_rotations = [], []
    for m in measures:
        rc, scale = face_orientation(m)
        world_head = camera_basis.T@rc
        local_head = parent.T@world_head
        rotations.append(angles(local_head))
        if "crown_manual_span_px" in m:
            # 这里用可见宽冠而不是左侧细臂。长度区间来自原帧观察，非精确原骨架。
            d = np.array(m["crown_manual_span_px"], dtype=float)
            y_projection = np.array([d[0], -d[1]])/(3.85*camera["pixels_per_unit"])
            x_line = m["eye_centers"][0]-m["eye_centers"][1]
            corrected = rotation_from_screen_axes([x_line[0], -x_line[1]], y_projection)
            local_head = parent.T@camera_basis.T@corrected
        head_rotations.append(local_head)
        m["fitted_face_pixels_per_unit"] = scale
    rotations = np.rad2deg(np.unwrap(np.deg2rad(np.asarray(rotations)), axis=0))
    first_rotation = rotations[0]
    raw = []
    rows = np.array(LIMBS[stem], dtype=float)
    for index, (measure, total_euler) in enumerate(zip(measures, rotations)):
        # 头部俯仰变化的 30% 保留为独立头动作；其余由根骨带动身体。
        root_euler = total_euler.copy()
        root_euler[0] -= 0.30 * (total_euler[0]-first_rotation[0])
        root_euler[2] -= 0.15 * (total_euler[2]-first_rotation[2])
        root_rot = rmat(root_euler)
        if stem == "fourside" and 42 <= index <= 45:
            # s045的躯干/腿大部分被头遮住；不能继续将身体长轴与头冠共线。
            # 隐藏侧姿态无法实测，此分支是按可见压缩范围给出的明确适配候选。
            camera_root = camera_basis@parent@root_rot
            amount = {42: .35, 43: .60, 44: .82, 45: 1.}[index]
            proposed = (1-amount)*camera_root[:2, 1]+amount*np.array([.10, .25])
            proposed *= min(1, .97/max(.97, np.linalg.norm(proposed)))
            camera_root = rotation_from_screen_axes(camera_root[:2, 0], proposed)
            root_rot = parent.T@camera_basis.T@camera_root
            root_euler = angles(root_rot)
            measure["body_occlusion_adaptation"] = {"amount": amount, "target_y_axis_projection": [.10, .25],
                "evidence": "s045躯干/腿被头遮住、投影大幅缩短；隐藏身体俯仰为推断，不是原骨骼测量"}
        head_local = root_rot.T@head_rotations[index]
        # 眼中心在源500画幅的位置；同一相机，不逐帧重新居中，不使用scale。
        eye_model = np.array([0.0, 1.25, 1.85])
        current_eye = root_rot@(head_pivot-root_pivot) + root_rot@head_local@(eye_model-head_pivot)
        world_eye = parent@(root_pivot+current_eye)
        delta_pixel = measure["eye_centers"].mean(axis=0)-np.array([250., 250.])
        desired_screen = np.array([delta_pixel[0], -delta_pixel[1], 0])/camera["pixels_per_unit"]
        actual_screen = camera_basis@(world_eye-np.array(camera["target"]))
        correction = desired_screen-actual_screen
        correction[2] = 0  # 单视图不给整体深度位移；只拟合相机平面。
        displacement = parent.T@camera_basis.T@correction
        values = {"inner_root:rotation": root_euler-np.array(groups["inner_root"]["rotation"]),
                  "inner_root:position": displacement,
                  "inner_head:rotation": angles(head_local)-np.array(groups["inner_head"]["rotation"]),
                  "inner_body:rotation": np.zeros(3)}
        limb = np.array([np.interp(index, rows[:, 0], rows[:, j]) for j in range(1, 8)])
        # 小人 +X 为模型左侧；外展时左右 Z 符号相反。rest 在导出时已加，下面是 delta。
        values["inner_arm_left:rotation"] = np.array([-limb[0], 0, limb[1]])
        values["inner_arm_right:rotation"] = np.array([-limb[2], 0, -limb[3]])
        values["inner_leg_left:rotation"] = np.array([limb[4], 0, limb[6]])
        values["inner_leg_right:rotation"] = np.array([limb[5], 0, -limb[6]])
        if stem == "fourside" and index in ENDPOINT_E1:
            measure["endpoint_unfitted_values"] = {name: values[name+":rotation"].copy() for name in ENDPOINT_E1[index]}
            measure["endpoint_fit_E1"] = []
            ancestor_rotation = parent@root_rot
            for name, target_px in ENDPOINT_E1[index].items():
                pivot = np.array(groups[name]["origin"], dtype=float)
                point = np.array([pivot[0], -2.6, 2.9]) if "arm" in name else np.array([-.72, -4.29, 1.95])
                vector = point-pivot
                length = np.linalg.norm(vector)
                world_pivot = parent@(displacement+root_pivot+root_rot@(pivot-root_pivot))
                old_screen = camera_basis@(world_pivot-np.array(camera["target"]))
                desired_screen = np.array([(target_px[0]-250)/camera["pixels_per_unit"], (250-target_px[1])/camera["pixels_per_unit"]])
                projected_delta = desired_screen-old_screen[:2]
                remaining = length*length-float(projected_delta@projected_delta)
                if remaining < 0:
                    raise ValueError(f"{stem} {index} {name} 端点在固定骨长下不可达")
                depth = -math.sqrt(remaining)  # E1：朝相机反方向，保留原生候选中较少翻转的一支。
                desired_local = ancestor_rotation.T@camera_basis.T@np.r_[projected_delta, depth]
                current = rmat(np.array(groups[name]["rotation"])+values[name+":rotation"])
                correction, _ = Rotation.align_vectors([desired_local/length], [current@vector/length])
                fitted = correction.as_matrix()@current
                values[name+":rotation"] = angles(fitted)-np.array(groups[name]["rotation"])
                world_endpoint = world_pivot+ancestor_rotation@fitted@vector
                actual_screen = camera_basis@(world_endpoint-np.array(camera["target"]))
                actual_px = np.array([250+actual_screen[0]*camera["pixels_per_unit"], 250-actual_screen[1]*camera["pixels_per_unit"]])
                measure["endpoint_fit_E1"].append({"bone": name, "target_px": target_px, "projected_px": clean(actual_px),
                    "projection_error_px": float(np.linalg.norm(actual_px-target_px)), "depth_from_pivot_toward_camera": depth,
                    "local_landmark": clean(point), "rotation_delta": clean(values[name+":rotation"]),
                    "evidence": "可见细臂末端中心约±5px；解剖左右/深度推断" if "arm" in name else "可见足部小亮区低置信对应；43/44手工约±8px，45白区质心，不当原关节位置"})
        raw.append({"frame": index, "values": values})
    return raw


def constrain_visible_crown(raw, measures, groups, camera):
    """Fourside宽冠方向+脸中心联合约束；保持根/身体旋转及头pivot。

    冠轴是手工识别宽冠后测的截面中心方向；不能用最高alpha点自动当冠。
    保留head原pivot连接，不给头加独立位移；由inner_root整体平移恢复源脸中心。
    """
    files = [OUT/"inner_crown_0_24.json", OUT/"inner_crown_landmarks_25_49.json"]
    landmarks = {}
    for path in files:
        for row in json.loads(path.read_text(encoding="utf-8"))["frames"]:
            if row["source_frame"] in landmarks:
                raise ValueError("重复冠轴源帧")
            landmarks[row["source_frame"]] = row
    if set(landmarks) != set(range(50)):
        raise ValueError("Fourside冠轴须覆盖全部50源帧；不可无记录补猜")
    parent = rmat(groups["shell_root"]["rotation"])
    rp = np.array(groups["inner_root"]["origin"], dtype=float)
    hp = np.array(groups["inner_head"]["origin"], dtype=float)
    head_rest = np.array(groups["inner_head"]["rotation"], dtype=float)
    basis = np.array(camera["basis_right_up_viewer"])
    ppu = camera["pixels_per_unit"]
    target = np.array(camera["target"])
    eye_proxy = np.array([0., 1.25, 1.85])
    crown_root, crown_tip = np.array([0., 2.65, 2.9]), np.array([0., 6.5, 2.9])
    records, new_angles = [], []
    def project(point):
        q = basis@(point-target)
        return np.array([250+q[0]*ppu, 250-q[1]*ppu])
    for row, m in zip(raw, measures):
        i, values = row["frame"], row["values"]
        mark = landmarks[i]
        root_rot = rmat(np.array(groups["inner_root"]["rotation"])+values["inner_root:rotation"])
        old_head = rmat(head_rest+values["inner_head:rotation"])
        ancestor = parent@root_rot
        old_camera = basis@ancestor@old_head
        span = np.array(mark["crown_tip_px"], dtype=float)-mark["crown_root_px"]
        desired_y = np.array([span[0], -span[1]])/(3.85*ppu)
        if np.linalg.norm(desired_y) >= 1:
            raise ValueError(f"冠轴{i}超出固定几何/相机可达投影，不可通过scale硬配")
        if mark["confidence"] == "low":
            # 09/10/37前俯宽冠边界不清，保留已单独审核的低置信先验，不同权硬拟合。
            head = old_head
            method = "low_confidence_prior_retained"
        else:
            sign = 1 if old_camera[2, 1] >= 0 else -1
            camera_head = rotation_from_screen_axes(old_camera[:2, 0], desired_y, sign)
            head = ancestor.T@basis.T@camera_head
            method = "visible_crown_axis_constrained_rotation_only"
        new_angles.append(angles(head))
        displacement = values["inner_root:position"]
        world_pivot = parent@(displacement+rp+root_rot@(hp-rp))
        old_eye_px = project(world_pivot+ancestor@old_head@(eye_proxy-hp))
        new_eye_px = project(world_pivot+ancestor@head@(eye_proxy-hp))
        uncorrected_eye_px = new_eye_px.copy()
        desired_eye_px = m["eye_centers"].mean(axis=0)
        shift_px = desired_eye_px-new_eye_px
        shift_world = basis.T@np.array([shift_px[0]/ppu, -shift_px[1]/ppu, 0.])
        shift_parent = parent.T@shift_world
        values["inner_root:position"] = displacement+shift_parent
        world_pivot += shift_world
        new_eye_px = project(world_pivot+ancestor@head@(eye_proxy-hp))
        cr = project(world_pivot+ancestor@head@(crown_root-hp))
        ct = project(world_pivot+ancestor@head@(crown_tip-hp))
        achieved = ct-cr
        direction_error = math.degrees(math.acos(float(np.clip((achieved@span)/(np.linalg.norm(achieved)*np.linalg.norm(span)), -1, 1))))
        record = {"source_frame": i, "target_time": 1+i/25, "landmark": mark, "method": method,
                  "source_axis_px": clean(span), "model_axis_px": clean(achieved),
                  "axis_direction_error_degrees": direction_error,
                  "axis_length_error_px": float(np.linalg.norm(achieved)-np.linalg.norm(span)),
                  "model_crown_root_px": clean(cr), "model_crown_tip_px": clean(ct),
                  "crown_root_position_error_px": float(np.linalg.norm(cr-mark["crown_root_px"])),
                  "eye_proxy_before_px": clean(old_eye_px), "eye_proxy_after_px": clean(new_eye_px),
                  "eye_proxy_before_root_correction_px": clean(uncorrected_eye_px),
                  "eye_proxy_change_px": float(np.linalg.norm(uncorrected_eye_px-old_eye_px)),
                  "eye_proxy_source_error_px": float(np.linalg.norm(new_eye_px-m["eye_centers"].mean(axis=0))),
                  "inner_root_position_correction": clean(shift_parent),
                  "inner_root_position_correction_length": float(np.linalg.norm(shift_parent)),
                  "inner_root_position_before": clean(displacement), "inner_root_position_after": clean(values["inner_root:position"]),
                  "head_position_added": [0., 0., 0.], "pivot_connection": "unchanged"}
        records.append(record); m["crown_constraint"] = record
        if i in ENDPOINT_E1:
            # 整人位置已变：从未拟合的原肢角重新求E1，不把旧端点旋转叠加一次。
            m["endpoint_fit_E1_before_root_recovery"] = m["endpoint_fit_E1"]
            m["endpoint_fit_E1"] = []
            for name, target_px in ENDPOINT_E1[i].items():
                pivot = np.array(groups[name]["origin"], dtype=float)
                point = np.array([pivot[0], -2.6, 2.9]) if "arm" in name else np.array([-.72, -4.29, 1.95])
                vector = point-pivot; length = np.linalg.norm(vector)
                world_joint = parent@(values["inner_root:position"]+rp+root_rot@(pivot-rp))
                joint_screen = basis@(world_joint-target)
                target_screen = np.array([(target_px[0]-250)/ppu, (250-target_px[1])/ppu])
                delta_screen = target_screen-joint_screen[:2]
                remaining = length*length-float(delta_screen@delta_screen)
                if remaining < 0:
                    raise ValueError(f"冠轴更新后{i}:{name}端点不可达；不得隐式缩放/平移关节")
                depth = -math.sqrt(remaining)
                desired_local = ancestor.T@basis.T@np.r_[delta_screen, depth]
                base = rmat(np.array(groups[name]["rotation"])+m["endpoint_unfitted_values"][name])
                correction, _ = Rotation.align_vectors([desired_local/length], [base@vector/length])
                fitted = correction.as_matrix()@base
                values[name+":rotation"] = angles(fitted)-np.array(groups[name]["rotation"])
                actual = project(world_joint+ancestor@fitted@vector)
                m["endpoint_fit_E1"].append({"bone": name, "target_px": target_px, "projected_px": clean(actual),
                    "projection_error_px": float(np.linalg.norm(actual-target_px)), "depth_from_pivot_toward_camera": depth,
                    "local_landmark": clean(point), "rotation_delta": clean(values[name+":rotation"]),
                    "evidence": "按新inner_root整体位置重算E1。可见手端约±5px；脚端/解剖对应低置信；没有改几何或固定骨长"})
    unwrapped = np.rad2deg(np.unwrap(np.deg2rad(np.array(new_angles)), axis=0))
    for row, absolute in zip(raw, unwrapped):
        row["values"]["inner_head:rotation"] = absolute-head_rest
    summary = {"inputs": [{"path": str(p.relative_to(REF)).replace("\\", "/"), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in files],
               "frames": records, "head_position_added_max": 0,
               "preserved": "根与身体rotation、head原pivot连接、静态几何、固定相机；仅头rotation+整人inner_root position联合纠正，43..45 E1按新位置重算，其余肢角不改。",
               "max_eye_proxy_change_px": max(r["eye_proxy_change_px"] for r in records),
               "max_inner_root_position_correction_length": max(r["inner_root_position_correction_length"] for r in records),
               "max_eye_proxy_source_error_px_after_root_recovery": max(r["eye_proxy_source_error_px"] for r in records),
               "max_crown_root_position_error_px": max(r["crown_root_position_error_px"] for r in records),
               "limitations": "冠轴相符不等于绝对冠根位置/脸像素均相符。根点/截面大小仍含静态适配误差；未为零眼误差拉开头身。"}
    (OUT/"inner_crown_constraints.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    return summary


def keyframe(time, value, stem, frame, inferred=False):
    return {"time": round(time, 8), "value": clean(value), "interpolation": "linear",
            "source_frame": frame if frame is not None else None,
            "evidence_id": f"{stem}:s{frame:03d}" if frame is not None else f"{stem}:transition-inferred",
            "evidence": "推断收势" if inferred else "有动图；二维标记实测，三维关节适配推断"}


def combine(stem, raw):
    name, length, loop = {"docile": ("idle", 16., True), "anxious": ("walk", 8., True), "fourside": ("cross_beam", 4., False)}[stem]
    timeline = []
    if stem == "docile":
        for cycle in range(3):
            timeline.extend((cycle*16/3+i/25/0.9, i, False) for i in KEYS[stem])
        timeline.append((16., 0, False))
    elif stem == "anxious":
        timeline = [(i/25, i, False) for i in KEYS[stem]]+[(8., 0, False)]
    else:
        timeline = [(0., None, True), (0.65, None, True)]+[(1+i/25, i, False) for i in KEYS[stem]]
        timeline += [(3., 49, False), (3.45, None, True), (4., None, True)]
    tracks = []
    for channel in raw[0]["values"]:
        bone, kind = channel.split(":")
        keys = []
        for time, frame, inferred in timeline:
            val = raw[frame]["values"][channel] if frame is not None else np.zeros(3)
            keys.append(keyframe(time, val, stem, frame, inferred))
        tracks.append({"bone": bone, "channel": kind, "keyframes": keys})
    key_poses = []
    mappings = []
    for time, frame, inferred in timeline:
        if frame is None:
            continue
        entry = {"time": round(time, 8), "source_frame": frame, "source_time": frame/25,
                 "source_path": f"frames/{SOURCES[stem][0]}/frame_{frame:04d}.png",
                 "evidence_id": f"{stem}:s{frame:03d}",
                 "notes": POSE_NOTES[stem].get(frame, "原片逐帧转折中间姿态，保留25fps采样，不额外平滑")}
        key_poses.append(entry)
        mappings.append({"clip": name, "target_time": round(time, 8), **entry})
    return {"name": name, "length": length, "loop": loop,
            "evidence": "有动图；头部二维面轴/位移测量，深度和四肢为受限骨架适配推断",
            "tracks": tracks, "key_poses": key_poses}, mappings


def annotate(stem, measures):
    selected = KEYS[stem]
    font = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 14)
    for page in range((len(selected)+19)//20):
        indices = selected[page*20:(page+1)*20]
        sheet = Image.new("RGB", (1250, 285*math.ceil(len(indices)/5)), (33, 36, 43))
        draw = ImageDraw.Draw(sheet)
        for cell, idx in enumerate(indices):
            a = Image.open(REF/"frames"/SOURCES[stem][0]/f"frame_{idx:04d}.png").convert("RGBA")
            bg = Image.new("RGBA", a.size, (81, 86, 99, 255)); bg.alpha_composite(a)
            overlay = ImageDraw.Draw(bg)
            for name, col in [("eye_centers", (70, 255, 140)), ("mouth_centers", (255, 90, 70))]:
                points = measures[idx][name]
                overlay.line([tuple(x) for x in points], fill=col, width=2)
                for x, y in points:
                    overlay.ellipse((x-4, y-4, x+4, y+4), outline=col, width=2)
            x, y = (cell%5)*250, (cell//5)*285
            sheet.paste(bg.resize((250, 250), Image.Resampling.NEAREST).convert("RGB"), (x, y))
            draw.text((x+6, y+254), f"{stem} s{idx:03d} / {idx/25:.2f}s", fill="white", font=font)
        sheet.save(OUT/f"inner_{stem}_measured_{page+1:02d}.png")


def refresh_endpoint_proposals():
    """仅刷新两深度候选；不运行轨道生成、不改主模型或已冻结轨道。"""
    motion_path = OUT / "inner_motion.json"
    model_path = REF / "heart_of_ender.bbmodel"
    motion_bytes, model_bytes = motion_path.read_bytes(), model_path.read_bytes()
    motion = json.loads(motion_bytes)
    model = json.loads(model_bytes)
    _, groups = get_rig()
    clip = next(c for c in motion["clips"] if c["name"] == "cross_beam")
    bb_clip = next(c for c in model["animations"] if c["name"] == "animation.cross_beam")
    camera = motion["review_camera"]
    basis = np.array(camera["basis_right_up_viewer"])
    target, ppu = np.array(camera["target"]), camera["pixels_per_unit"]
    parent = rmat(groups["shell_root"]["rotation"])
    rp = np.array(groups["inner_root"]["origin"])
    fits = json.loads((OUT / "inner_endpoint_fit.json").read_text(encoding="utf-8"))
    source_fit = {row["source_frame"]: {f["bone"]: f for f in row["fits"]} for row in fits["frames"]}
    frames, max_bb_error = [], 0.
    for frame, targets in ENDPOINT_E1.items():
        time = 1 + frame / 25
        values = {t["bone"] + ":" + t["channel"]: np.array(next(k["value"] for k in t["keyframes"] if abs(k["time"]-time) < 1e-8)) for t in clip["tracks"]}
        # 实际BB源文件仅允许已知的五位小数输出舍入，禁止候选引用陈旧轨道。
        for key, value in values.items():
            bone, channel = key.split(":")
            animator = next(a for a in bb_clip["animators"].values() if a["name"] == bone)
            keyframe = next(k for k in animator["keyframes"] if k["channel"] == channel and abs(k["time"]-time) < 5.01e-6)
            actual = np.array([float(keyframe["data_points"][0][axis]) for axis in "xyz"])
            error = float(np.max(np.abs(actual-value)))
            max_bb_error = max(max_bb_error, error)
            if error > 5.01e-6:
                raise ValueError(f"候选所引BB动画与冻结inner轨道不同：{frame} {key} {error}")
        root_rot = rmat(np.array(groups["inner_root"]["rotation"])+values["inner_root:rotation"])
        ancestor = parent @ root_rot
        proposals = []
        for ident, sign in (("E1_behind", -1), ("E2_front", 1)):
            overrides = []
            for name, target_px in targets.items():
                pivot = np.array(groups[name]["origin"], dtype=float)
                point = np.array(source_fit[frame][name]["local_landmark"])
                vector = point-pivot
                length = np.linalg.norm(vector)
                joint = parent@(values["inner_root:position"]+rp+root_rot@(pivot-rp))
                joint_screen = basis@(joint-target)
                desired_screen = np.array([(target_px[0]-250)/ppu, (250-target_px[1])/ppu])
                dxy = desired_screen-joint_screen[:2]
                remaining = length*length-float(dxy@dxy)
                if remaining < 0:
                    raise ValueError(f"{frame}:{name}在固定骨长下不可达")
                depth = sign*math.sqrt(remaining)
                rest = np.array(groups[name]["rotation"])
                base_delta = motion["measurements"]["fourside"][frame]["endpoint_unfitted_values"][name]
                base = rmat(rest+base_delta)
                if sign < 0:
                    delta = values[name+":rotation"]
                    if not np.array_equal(delta, source_fit[frame][name]["rotation_delta"]):
                        raise ValueError("E1最终拟合记录与冻结轨道不一致")
                    fitted = rmat(rest+delta)
                else:
                    goal = ancestor.T@basis.T@np.r_[dxy, depth]
                    correction, _ = Rotation.align_vectors([goal/length], [base@vector/length])
                    fitted = correction.as_matrix()@base
                    delta = angles(fitted)-rest
                screen = basis@(joint+ancestor@fitted@vector-target)
                actual_px = np.array([250+screen[0]*ppu, 250-screen[1]*ppu])
                overrides.append({"bone": name, "channel": "rotation", "value": clean(delta),
                    "absolute_rotation": clean(rest+delta), "target_px": target_px,
                    "projected_px": clean(actual_px), "projection_error_px": float(np.linalg.norm(actual_px-target_px)),
                    "local_landmark": clean(point), "depth_from_pivot_toward_camera": depth,
                    "rotation_change_from_unfitted_deg": float(np.rad2deg(Rotation.from_matrix(fitted@base.T).magnitude())),
                    "remaining_twist_deg": 0., "evidence": source_fit[frame][name]["evidence"]})
            proposals.append({"id": ident, "source_frame": frame, "time": time,
                "status": "current_main_draft_not_user_approved" if sign < 0 else "candidate_only_not_applied_or_native_rendered_for_this_revision",
                "overrides": overrides})
        frames.append({"source_frame": frame, "source_path": f"frames/MCD_Arch-Illager_Fourside/frame_{frame:04d}.png",
            "time": time, "inner_root_position": clean(values["inner_root:position"]),
            "inner_root_rotation": clean(values["inner_root:rotation"]), "proposals": proposals})
    result = {"schema_version": 2, "stage": "E1_is_frozen_main_draft_E2_is_review_candidate",
        "source_inner_motion_sha256": hashlib.sha256(motion_bytes).hexdigest(),
        "source_bbmodel_sha256": hashlib.sha256(model_bytes).hexdigest(),
        "source_endpoint_fit_sha256": hashlib.sha256((OUT/"inner_endpoint_fit.json").read_bytes()).hexdigest(),
        "source_model_vs_inner_max_numeric_error": max_bb_error,
        "camera": {**camera, "follow_bone": "shell_root"}, "model_scale": "unchanged",
        "method": "同一最新冠轴和整体root位置下保持肩/髋pivot及骨长：两深度分支为±sqrt(L²-dx²-dy²)。E1直接读取已冻结主轨道并与最终fit逐值核对；E2从原未拟合肢角求最小旋转，没有额外扭转。",
        "source_evidence": "43/44/45各自可见手端与足端；解剖左右/深度为推断，脚端低置信。E2新版未原生渲染，旧0c53版本候选对照仅历史资料，不能作为当前候选图片。",
        "frames": frames, "proposals": frames[-1]["proposals"]}
    native_dir = REF/"m3_preview/f45_options"
    native_evidence_path = native_dir/"evidence.json"
    if native_evidence_path.exists():
        native_evidence = json.loads(native_evidence_path.read_text(encoding="utf-8"))
        if native_evidence.get("main_bbmodel_sha256") == result["source_bbmodel_sha256"] and native_evidence.get("main_unchanged"):
            for proposal in result["proposals"]:
                option = next(row for row in native_evidence["options"] if row["id"] == proposal["id"])
                option_bytes = (native_dir/(proposal["id"]+".bbmodel")).read_bytes()
                if hashlib.sha256(option_bytes).hexdigest() != option["bbmodel_sha256"]:
                    raise ValueError("原生候选模型SHA与证据不符")
                option_clip = next(a for a in json.loads(option_bytes)["animations"] if a["name"] == "animation.cross_beam")
                for override in proposal["overrides"]:
                    animator = next(a for a in option_clip["animators"].values() if a["name"] == override["bone"])
                    key = next(k for k in animator["keyframes"] if k["channel"] == "rotation" and abs(k["time"]-proposal["time"]) < 5.01e-6)
                    values = np.array([float(key["data_points"][0][axis]) for axis in "xyz"])
                    if np.max(np.abs(values-override["value"])) > 5.01e-6:
                        raise ValueError("原生候选使用了不同的端点角度")
                proposal["native_rendered_this_revision"] = True
                if proposal["id"] == "E2_front":
                    proposal["status"] = "candidate_only_not_applied_native_rendered_for_source_frame45"
            result["native_frame45_evidence"] = {"path": str(native_evidence_path.relative_to(REF)).replace("\\", "/"),
                "sha256": hashlib.sha256(native_evidence_path.read_bytes()).hexdigest(), "model_overrides_verified": True}
            result["source_evidence"] = "43/44/45各自可见手端与足端；解剖左右/深度为推断，脚端低置信。45两分支已有同版原生对照且候选角度已核对；43/44的E2仍只有候选数据。E1暂选主稿，E2未写入主模型。"
    output = OUT/"inner_endpoint_proposals.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    assert motion_path.read_bytes() == motion_bytes and model_path.read_bytes() == model_bytes
    print(json.dumps({"output": str(output), "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "inner_motion_unchanged": True, "bbmodel_unchanged": True, "max_bb_numeric_error": max_bb_error}, ensure_ascii=False))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rig_path, groups = get_rig()
    fmap = json.loads((REF/"analysis_poses/frame_map.json").read_text(encoding="utf-8"))
    # 固定参考相机；人体深度分支和相机标定共同不可唯一确定，必须保留这个推断标签。
    yaw, elev = math.radians(-45), math.radians(25)
    viewer = np.array([math.sin(yaw)*math.cos(elev), math.sin(elev), -math.cos(yaw)*math.cos(elev)])
    right = np.cross(np.array([0., 1., 0.]), viewer); right /= np.linalg.norm(right)
    up = np.cross(viewer, right)
    basis = np.array([right, up, viewer])
    first, _ = measure_frame(REF/"frames"/SOURCES["docile"][0]/"frame_0000.png", None)
    first["use_crown_axis"] = True
    face_cam, _ = face_orientation(first)
    parent = rmat(groups["shell_root"]["rotation"])
    rp = np.array(groups["inner_root"]["origin"])
    head_world = basis.T@face_cam
    eye_world = parent@rp+head_world@(np.array([0., 1.25, 1.85])-rp)
    eye_pixel = first["eye_centers"].mean(axis=0)-np.array([250., 250.])
    target = eye_world-basis.T@np.array([eye_pixel[0], -eye_pixel[1], 0])/(500/12.6)
    camera = {"position": clean(target+viewer*60), "target": clean(target), "height": 12.6,
              "width": 500, "height_px": 500, "isolate_inner": True,
              "pixels_per_unit": 500/12.6, "basis_right_up_viewer": basis.tolist(),
              "status": "初版固定正交相机；需原生Blockbench同帧图核对，不是原作相机参数"}
    all_measures, all_maps, clips, hashes = {}, [], [], {}
    crown_summary = None
    for stem, (folder, count) in SOURCES.items():
        previous, measures = None, []
        assert fmap[stem]["samples25"] == count
        for index in range(count):
            path = REF/"frames"/folder/f"frame_{index:04d}.png"
            measured, previous = measure_frame(path, previous)
            measured.update({"source_frame": index, "time": index/25,
                             "storage_frame": fmap[stem]["sample_map"][index]["storage_frame"],
                             "use_crown_axis": stem in ("docile", "anxious")})
            if stem == "fourside" and index in (46, 47):
                measured["manual_face_quad_px"] = {
                    46: [[163, 200], [256, 184], [258, 264], [164, 280]],
                    47: [[191, 181], [283, 206], [267, 289], [175, 264]],
                }[index]
                measured["manual_face_quad_evidence"] = "同一原PNG可见脸面四角手工测点，边界约±4px；替代连通眼区拆分导致的不稳定面轴，不能当原始UV/骨骼"
            if stem == "fourside" and index in (9, 10, 37):
                measured["crown_manual_span_px"] = {9: [18, -31], 10: [20, -34], 37: [46, -48]}[index]
                measured["crown_manual_evidence"] = {
                    "source": "原500px帧正确alpha合成后两人独立复核；最高左细条更像手臂，未用作冠轴",
                    "root_px": [229, 278] if index in (9, 10) else [230, 283],
                    "tip_px": [247, 247] if index in (9, 10) else [276, 235],
                    "projection_length_interval_px": [25, 55] if index in (9, 10) else [45, 80],
                    "confidence": "low; 过曝冠根边界约±12–15px；s010沿相邻相似姿态适配",
                }
            measures.append(measured)
        measured_indices = [i for i, m in enumerate(measures) if m["mouth_measured"]]
        offsets = np.array([measures[i]["mouth_centers"]-measures[i]["eye_centers"] for i in measured_indices])
        for index, measured in enumerate(measures):
            if measured["mouth_measured"]:
                continue
            offset = np.array([[np.interp(index, measured_indices, offsets[:, j, k]) for k in range(2)] for j in range(2)])
            measured["mouth_centers"] = measured["eye_centers"]+offset
            measured["mouth_interpolation_note"] = "白色口形不可见/太小，眼口偏移在相邻可见帧间线性插值；非直接实测"
        raw = build_source(stem, measures, groups, camera)
        if stem == "fourside":
            crown_summary = constrain_visible_crown(raw, measures, groups, camera)
        clip, mapping = combine(stem, raw)
        clips.append(clip); all_maps.extend(mapping)
        all_measures[stem] = measures
        hashes[stem] = hashlib.sha256((REF/(folder+".gif")).read_bytes()).hexdigest()
        annotate(stem, measures)
    limitations = [
        "有动图不等于取得原骨骼数据；眼口质心和轮廓是直接测量，面部三维深度分支/相机/关节角分配为推断。",
        "实际左右按R2骨骼名；未镜像源图。隐藏侧手臂及脚的深度不能由这些单视图唯一确定。",
        "每条小人手臂和腿仅一根运动骨；不能独立复现肘、膝和脚踝弯折。",
        "眼间距2.45与眼口垂距0.60是平面拟合标尺假设；眼面中心几何代理[0,1.25,1.85]不代表当前UV已映射眼睛。源图高亮会改变可测边缘。拟合的像素尺度只作诊断，没有scale通道。",
        "Docile48..56及Anxious7..9、72..74、138..141、175..177的白口不可测，眼口偏移在前后可见帧间插值；Fourside46/47连通眼区按主轴中位拆分，这些不是直接实测双眼/口对应。",
        "Docile/Anxious的头顶条轴来自alpha顶部行中心拟合，限制Y轴方向；Fourside46/47用已记录脸面四角替代合并眼区的方向推断。手工脸角边界误差约±4px。",
        "Fourside09/10/37的宽冠在前俯时严重缩短：09可见冠轴约25–55px，37约45–80px。采用区间内代表测点并保留低置信标签；最高左细条是疑似手臂，未当冠。",
        "Fourside42..45身体逐步收入头部遮挡后方以匹配压缩投影；不可见的身体前倾为适配推断。单根腿无法复刻原图可能存在的膝弯。",
        "Fourside43/44/45按各自源末端做固定骨长旋转反投影，暂用原生候选E1负深度分支；E2仅供M3审阅。像素端点零数值误差不等于原关节精确，也不能消除既有骨厚残差。",
        "Fourside42的另一可见细臂端约(185±6,378±7)，解剖对应不定；冠轴修订前若配右肩相距约121px，超过95.24px臂长投影上限，未把足端冒充手端。新头向后的整体平移不改变42肢角；46快速回正时点与肢角保留。",
        "Fourside冠轴由两人逐帧识别宽冠后标注，纠正旧眼口轴假设造成的明确朝向偏差。原head pivot不动、不加head position；用inner_root整体平移恢复实测脸中心并重算43..45 E1，根/身体rotation及其他肢角保持。位移改变量与冠根残差单列inner_crown_constraints.json。",
        "头部俯仰变化的30%、侧倾变化的15%分给独立头骨，其余根骨；这是可回溯的适配推断。",
        "Anxious原片7.96秒与0秒手臂姿态不同；保留原末帧，再在8秒循环边界回到初态，接缝需实看。",
        "Fourside1..3秒来自全部50源帧；0..1和3..4秒收势为推断，不附原片帧号。25Hz到运行时20Hz仍有采样差异。",
        "源GIF的L形紫眼与白口不在当前已批准64贴图north灰面映射中，调色不能自动恢复它们；本脚本不改材质。",
        "未运行游戏；本文件不是最终视觉验收。需要原生Blockbench同刻并排后再修正。"
    ]
    result = {"schema_version": 1, "clips": clips, "review_camera": camera,
              "source_model": "m2_endcaps/R2.bbmodel", "source_model_sha256": hashlib.sha256(rig_path.read_bytes()).hexdigest(),
              "source_gif_sha256": hashes, "coordinate_rule": "纯数字Euler直接加R2 rest；position也直接加；没有Bedrock符号翻转、Molang、scale",
              "docile_retime": {"source_length": 4.8, "target_length": 16, "cycles": 3, "playback_speed": .9,
                                "period": 16/3, "speed_change_percent": -10., "period_change_percent": 11.111111},
              "crown_constraint_summary": {k: v for k, v in crown_summary.items() if k != "frames"},
              "measurements": all_measures, "limitations": limitations}
    def default(value):
        if isinstance(value, np.ndarray): return value.tolist()
        raise TypeError(type(value).__name__)
    (OUT/"inner_motion.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, default=default)+"\n", encoding="utf-8")
    (OUT/"inner_time_map.json").write_text(json.dumps(all_maps, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    endpoint_record = {"status": "E1 temporary M3 review draft; not user-approved final", "frames": [
        {"source_frame": i, "target_time": 1+i/25, "fits": all_measures["fourside"][i]["endpoint_fit_E1"]} for i in ENDPOINT_E1],
        "frame42": "肢角保持：另一手的解剖对应不定；旧头向版本中(185,378)对右肩约121px，超过固定臂长95.24px，未强配；新头向仅随整体root position移动", "frame46": "快回正时点/肢角保持，头向按可见冠轴修正",
        "method": "保持pivot/骨长/几何/相机/scale；反投影2D位移，depth=-sqrt(L²-dx²-dy²)，最小旋转将旧骨轴对齐目标"}
    (OUT/"inner_endpoint_fit.json").write_text(json.dumps(endpoint_record, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    with (OUT/"inner_time_map.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(all_maps[0])); writer.writeheader(); writer.writerows(all_maps)
    requests = {"views": {"inner": camera}, "frames": []}
    for stem, clip in zip(SOURCES, clips):
        rendered_source_frames = set()
        for pose in clip["key_poses"]:
            if stem == "docile" and pose["time"] >= 16/3: continue
            if pose["source_frame"] in rendered_source_frames: continue
            rendered_source_frames.add(pose["source_frame"])
            requests["frames"].append({"id": f"inner_{stem}_s{pose['source_frame']:03d}", "clip": clip["name"],
                                       "time": pose["time"], "view": "inner", "source_path": pose["source_path"]})
    (OUT/"inner_render_requests.json").write_text(json.dumps(requests, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    notes = ["# M3 体内小人动作轨道（待同帧视觉复核）", "", "三段均有动图。轨道依据源图标记测量制作，但深度、隐藏侧和受限刚体骨架仍含推断。", "",
             "Docile 120帧 / 4.8秒 → idle16秒的三个5.333333秒周期，播放速度90%（速度−10%，周期+11.111%）。",
             "Anxious 200帧 / 8秒 → walk8秒；Fourside 50帧 / 2秒 → cross_beam的1..3秒。", "",
             "绿色标记是逐帧紫眼连通域质心；红色标记是最近白色口部连通域质心。所有370帧均测量，关键姿态图只展示抽样。",
             "二维眼线及眼口偏移恢复一个正交面；负X深度分支按同一可见侧连续选择。投影不能证明唯一真实欧拉角。",
             "头身/手脚数字值均写入可复现脚本；不改主bbmodel、公共管线、材质或游戏数据。", "", "## 限制", ""]
    notes.extend(f"- {x}" for x in limitations)
    for stem, clip in zip(SOURCES, clips):
        notes += ["", f"## {stem}：有动图关键姿态", "", "| 源帧 | 源时间(s) | 本clip对应时间(s) | 可见姿态/推断备注 |", "|---|---:|---|---|"]
        for frame, description in POSE_NOTES[stem].items():
            times = [f"{x['time']:.6f}" for x in clip["key_poses"] if x["source_frame"] == frame]
            notes.append(f"| {frame} | {frame/25:.2f} | {' / '.join(times)} | {description} |")
    notes += ["", "## 原生预览迭代记录", "", "第一版6姿态原生对照揭示：固定近景整体偏小；Anxious前伸臂Rx符号反向；Fourside46的相连眼区使推定冠轴侧倾。",
              "现版固定相机高度12.6（全片一致）、修正前伸Rx正号，并让46/47的可见脸面四角决定轴向。Docile/Anxious使用可见冠条行质心轴限制方向。",
              "以上修改待下一轮原生并排确认；不能凭数据成功写出声称还原完成。"]
    notes += ["", "## 输出与复现", "", "在仓库根目录运行 `python _tools/heart_of_ender_inner_motion.py`。",
              "`inner_motion.json` 为待合并轨道；`inner_time_map.json/csv` 给原帧和目标时间；`inner_render_requests.json` 给500像素固定近景请求。",
              "当前相机是待核对初版，不能声称尚未产出的Blockbench图已通过视觉验收。", "", "原始素材版权归 Mojang Studios；本项目非商业，与 Mojang 无关联。来源与SHA见上级SOURCES.md。"]
    (OUT/"inner_REVIEW.md").write_text("\n".join(notes)+"\n", encoding="utf-8")
    print(json.dumps({"clips": [{"name": c["name"], "tracks": len(c["tracks"]), "keys_per_track": len(c["tracks"][0]["keyframes"])} for c in clips],
                      "measured_frames": sum(len(v) for v in all_measures.values()), "render_requests": len(requests["frames"])}, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--proposals-only", action="store_true", help="仅从已冻结轨道刷新E1/E2端点候选，不重建动画")
    if parser.parse_args().proposals_only:
        refresh_endpoint_proposals()
    else:
        main()
