#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从教皇.bbmodel按共享矩阵数学导出挂点；不生成特效或玩法。"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
from types import SimpleNamespace

sys.dont_write_bytecode = True
import display_mob as dm
from pope_validate_motion import ORDER, load_json, transform_point, part_centers

HERE = Path(__file__).resolve().parent
REF = HERE / "pope_ref"
OUT = REF / "m3/validation"


def rounded(values):
    return [round(float(v), 8) for v in values]


def anchors(document):
    elements = {element["name"]: element for element in document["elements"]}
    ownership = {}
    group_ids = {group["uuid"]: group["name"] for group in document["groups"]}

    def visit(node):
        name = group_ids[node["uuid"]]
        for child in node["children"]:
            if isinstance(child, str):
                ownership[child] = name
            else:
                visit(child)

    for node in document["outliner"]:
        visit(node)

    def center(element):
        return [(a + b) / 2 for a, b in zip(element["from"], element["to"])]

    result = []
    for name, element_name in (("staff_tip", "staff_core"), ("right_hand", "right_hand"), ("left_hand", "left_hand"), ("head_top", "head_gray")):
        element = elements[element_name]
        point = center(element)
        if name == "head_top":
            point[1] = element["to"][1]
        result.append({"name": name, "bone": ownership[element["uuid"]], "element": element_name,
                       "local_unposed_point": point,
                       "status": ("权杖顶块几何中心，作为稳定发射锚点；不是每帧最高旋转角点，原作精确发射骨未知" if name == "staff_tip" else
                                  "头本体上表面中心，不含皇冠" if name == "head_top" else
                                  "手部几何中心，作为握点；原作手骨精确坐标未知")})
    return result


def attack_height_review(bones, clip, anchor, model_scale):
    """数值审查完整attack挂点轨迹，不给挂点加偏移或改动作。"""
    factor = model_scale / 16

    def point(time):
        return transform_point(dm.posed_matrix(bones, anchor["bone"], clip, time), anchor["local_unposed_point"])

    def height(time):
        return point(time)[1]

    def record(time):
        value = point(time)
        return {"time_seconds": round(time, 10), "posed_model_point": rounded(value),
                "height_model_units": value[1], "height_relative_to_carrier_feet_blocks": value[1] * factor,
                "minecraft_local_left_up_forward_blocks": rounded([-value[0] * factor, value[1] * factor, -value[2] * factor])}

    # 密集网格包含端点、源关键帧与20Hz烘焙时刻，另在每个局部谷值细化。
    times = {min(i / 1000, clip["length"]) for i in range(math.ceil(clip["length"] * 1000) + 1)}
    times.update(float(key[0]) for track in clip["tracks"].values() for key in track)
    times.update(i / 20 for i in range(round(clip["length"] * 20) + 1))
    times = sorted(times)
    values = [(time, height(time)) for time in times]
    candidates = list(values)
    golden = (math.sqrt(5) - 1) / 2
    for i in range(1, len(values) - 1):
        if values[i][1] <= values[i - 1][1] and values[i][1] <= values[i + 1][1]:
            left, right = times[i - 1], times[i + 1]
            a, b = right - golden * (right - left), left + golden * (right - left)
            ya, yb = height(a), height(b)
            for _ in range(45):
                if ya <= yb:
                    right, b, yb = b, a, ya
                    a = right - golden * (right - left)
                    ya = height(a)
                else:
                    left, a, ya = a, b, yb
                    b = left + golden * (right - left)
                    yb = height(b)
            time = (left + right) / 2
            candidates.append((time, height(time)))

    intervals = []
    start = 0.0 if values[0][1] < 0 else None
    for (left, yl), (right, yr) in zip(values, values[1:]):
        if (yl < 0) != (yr < 0):
            sign = yl < 0
            for _ in range(40):
                middle = (left + right) / 2
                if (height(middle) < 0) == sign:
                    left = middle
                else:
                    right = middle
            crossing = (left + right) / 2
            if yr < 0:
                start = crossing
            else:
                intervals.append([round(start, 10), round(crossing, 10)])
                start = None
    if start is not None:
        intervals.append([round(start, 10), clip["length"]])
    tick_times = [i / 20 for i in range(round(clip["length"] * 20) + 1)]
    return {"clip": "attack", "source": "同一.bbmodel及display_mob.posed_matrix，无人工挂点偏移",
            "method": "0.001秒密集网格并加入全部源关键帧；局部谷值黄金分割细化、过零点二分。最低值是数值估计，不是形式化连续全局下界证明。",
            "dense_sample_count": len(times), "dense_step_seconds": .001,
            "requested_moments": [record(time) for time in (.5, .6, .7)],
            "minimum_dense_sample": record(min(values, key=lambda item: item[1])[0]),
            "minimum_refined_estimate": record(min(candidates, key=lambda item: item[1])[0]),
            "minimum_20hz_source_sample": record(min(tick_times, key=height)),
            "below_feet_intervals_seconds": intervals,
            "risk_note": ("权杖顶块中心在部分前摆时刻低于载体脚底；载体落地时存在权杖穿地风险。出手三时刻为正不能证明整段不穿地。" if intervals else
                          "本次扫描未发现权杖顶块中心低于载体脚底；仍不证明完整权杖几何或其它部件不穿地。"),
            "limitations": "只检查staff_core中心相对载体脚底高度；不包含地形/载体移动、权杖棱角包围盒或实际客户端显示插值。未在真实游戏内看过。"}


def export_sockets(model_path, clipmeta_path):
    data = model_path.read_bytes()
    document = json.loads(data)
    spec = load_json(REF / "m2/model_spec.json")
    metadata = load_json(clipmeta_path)
    model_scale = spec["model_scale"]
    mob = SimpleNamespace(bbmodel=model_path, anim_from=None, key="pope")
    bones, _, _ = dm.load_bbmodel(mob)
    clips = dm.load_animations(mob)
    base = anchors(document)
    center_by_part = part_centers(bones, spec, document["resolution"])
    bone_part = {members[0]: name for name, members in spec["parts"]}
    carrier_seat = metadata.get("carrier_seat", 2.0)
    transform_mob = SimpleNamespace(model_scale=model_scale, seat=carrier_seat)
    conversion_errors = []
    meta = {row["name"]: row for row in metadata["clips"]}
    samples = []
    for name in ORDER:
        clip = clips[name]
        times = {0.0, float(clip["length"])}
        times.update(float(key[0]) for track in clip["tracks"].values() for key in track)
        times.update(float(t) for t in meta[name].get("sample_times", []))
        times.update(float(t) for t in meta[name].get("release_times", []))
        if name == "attack":
            times.update((.5, .6, .7))
        for time in sorted(times):
            if not math.isfinite(time) or not 0 <= time <= clip["length"] + 1e-8:
                raise ValueError("挂点采样时刻越界：%s %.9g" % (name, time))
            row = {"clip": name, "time": time,
                   "is_release_time": any(abs(time - t) < 1e-8 for t in meta[name].get("release_times", [])), "sockets": []}
            for anchor in base:
                world = dm.posed_matrix(bones, anchor["bone"], clip, time)
                point = transform_point(world, anchor["local_unposed_point"])
                local_blocks = [v * model_scale / 16 for v in point]
                forward = [-world[i][2] for i in range(3)]
                # 用实际display矩阵反算到脚底空间，独立核对seat补偿和R180符号。
                part = bone_part[anchor["bone"]]
                center = center_by_part[part]["unposed_center"]
                offset = [v - 8 for v in center]
                display = dm.display_matrix(transform_mob, bones, anchor["bone"], offset, world)
                item = [anchor["local_unposed_point"][i] - center[i] for i in range(3)]
                renderer_input = [-item[0] / 16, item[1] / 16, -item[2] / 16]
                displayed = transform_point(display, renderer_input)
                displayed[1] += carrier_seat
                expected_display = [-local_blocks[0], local_blocks[1], -local_blocks[2]]
                conversion_errors.append(max(abs(a - b) for a, b in zip(displayed, expected_display)))
                row["sockets"].append(dict(anchor, posed_model_point=rounded(point),
                                           posed_character_local_blocks=rounded(local_blocks),
                                           minecraft_local_left_up_forward_blocks=rounded([-local_blocks[0], local_blocks[1], -local_blocks[2]]),
                                           bone_forward_minus_z=rounded(forward),
                                           minecraft_bone_forward_left_up_forward=rounded([-forward[0], forward[1], -forward[2]])))
            samples.append(row)
    review_alerts = []
    for sample in samples:
        if sample["is_release_time"]:
            tip = next(socket for socket in sample["sockets"] if socket["name"] == "staff_tip")
            if tip["posed_character_local_blocks"][1] < -0.02:
                review_alerts.append({"clip": sample["clip"], "time": sample["time"], "socket": "staff_tip",
                                      "height_relative_to_carrier_feet_blocks": tip["posed_character_local_blocks"][1],
                                      "issue": "出手挂点低于载体脚底；如果载体落地，会从地面下发射。须视觉复核姿态，不能用数值矩阵通过替代。"})
    attack_review = attack_height_review(bones, clips["attack"], next(a for a in base if a["name"] == "staff_tip"), model_scale)
    if attack_review["below_feet_intervals_seconds"]:
        lowest = attack_review["minimum_refined_estimate"]
        review_alerts.append({"clip": "attack", "time": lowest["time_seconds"], "socket": "staff_tip",
                              "height_relative_to_carrier_feet_blocks": lowest["height_relative_to_carrier_feet_blocks"],
                              "issue": attack_review["risk_note"]})
    result = {"bbmodel_sha256": hashlib.sha256(data).hexdigest(),
              "clipmeta_sha256": hashlib.sha256(clipmeta_path.read_bytes()).hexdigest(),
              "audio_cues_sha256": hashlib.sha256((REF / "m3/audio_cues.json").read_bytes()).hexdigest(),
              "m2_model_spec_sha256": hashlib.sha256((REF / "m2/model_spec.json").read_bytes()).hexdigest(),
              "coordinate_system": "+Y up, facing -Z, character right +X; unscaled Java model units",
              "model_scale": model_scale, "carrier_seat": carrier_seat,
              "carrier_seat_status": "默认未缩放隐身卫道士的预期乘客座高；M4待运行时确认",
              "units_and_conversion": {
                  "local_unposed_point": "未摆姿的Java模型绝对坐标，与.bbmodel from/to使用同一空间，不是从骨轴起算的坐标",
                  "posed_model_point": "display_mob.posed_matrix乘未摆姿点，单位为模型单位",
                  "posed_character_local_blocks": "posed_model_point乘model_scale/16；相对角色脚底，仍为+X右,+Y上,-Z前",
                  "minecraft_local_left_up_forward_blocks": "[-x,+y,-z]乘model_scale/16；对应载体朝向下的^左 ^上 ^前，pitch按0；相对脚底不减seat",
                  "bone_forward_minus_z": "骨骼局部-Z变换后的单位向量，不断言这是原作弹道发射方向",
                  "seat_note": "挂点不是item_display NBT translation。座高仅用于display变换补偿，不应从脚底相对挂点再次扣除。",
              },
              "staff_tip_note": "接口名沿用staff_tip，语义为staff_core稳定中心。旋转时不追随每帧最高角点，以免挂点在不同角点间跳变。",
              "head_top_note": "头本体上表面中心，不是冠尖。",
              "direction_note": "能量弹方向应由玩法按目标/规则确定；骨骼-Z只供姿态参考。未生成弹体或特效。",
              "display_matrix_conversion_max_error_blocks": max(conversion_errors),
              "attack_staff_tip_height_review": attack_review,
              "review_alerts": review_alerts,
              "samples": samples}
    if result["display_matrix_conversion_max_error_blocks"] > 1e-7:
        raise ValueError("挂点坐标与实际display矩阵转换不一致")
    if hashlib.sha256(model_path.read_bytes()).hexdigest() != result["bbmodel_sha256"]:
        raise ValueError("导出时模型被更新，必须重跑")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, default=REF / "pope.bbmodel")
    parser.add_argument("--clipmeta", type=Path, default=REF / "m3/clipmeta.json")
    args = parser.parse_args()
    result = export_sockets(args.model, args.clipmeta)
    (REF / "sockets.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    OUT.mkdir(parents=True, exist_ok=True)
    summary = {"bbmodel_sha256": result["bbmodel_sha256"], "samples": len(result["samples"]),
               "clipmeta_sha256": result["clipmeta_sha256"], "audio_cues_sha256": result["audio_cues_sha256"],
               "m2_model_spec_sha256": result["m2_model_spec_sha256"],
               "display_matrix_conversion_max_error_blocks": result["display_matrix_conversion_max_error_blocks"],
               "sockets_per_sample": 4, "release_samples": [{"clip": r["clip"], "time": r["time"]} for r in result["samples"] if r["is_release_time"]],
               "clips": list(dict.fromkeys(r["clip"] for r in result["samples"])),
               "review_alerts": result["review_alerts"],
               "attack_staff_tip_height_review": result["attack_staff_tip_height_review"],
               "in_game_verified": False}
    (OUT / "socket_export.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    review = result["attack_staff_tip_height_review"]
    rows = ["# Attack 权杖顶端高度复核", "", "模型 SHA-256：`%s`。" % result["bbmodel_sha256"], "",
            "所有高度相对载体脚底；使用原模型矩阵，未添加挂点偏移。", "",
            "| 时刻（秒） | 高度（模型单位） | 高度（格） |", "|---|---|---|"]
    for item in review["requested_moments"]:
        rows.append("| %.2f | %.8f | %.8f |" % (item["time_seconds"], item["height_model_units"], item["height_relative_to_carrier_feet_blocks"]))
    minimum = review["minimum_refined_estimate"]
    tick_minimum = review["minimum_20hz_source_sample"]
    rows += ["", "完整片段最低数值估计：约 %.9f 秒，Y = %.8f 模型单位（%.8f 格）。" %
             (minimum["time_seconds"], minimum["height_model_units"], minimum["height_relative_to_carrier_feet_blocks"]), "",
             "0.05 秒源采样网格最低值：%.2f 秒，Y = %.8f 模型单位（%.8f 格）。" %
             (tick_minimum["time_seconds"], tick_minimum["height_model_units"], tick_minimum["height_relative_to_carrier_feet_blocks"]), "",
             "低于脚底的数值区间（秒）：`%s`。" % json.dumps(review["below_feet_intervals_seconds"]), "",
             review["risk_note"], "", review["method"], "", review["limitations"], ""]
    (OUT / "ATTACK_SOCKET_HEIGHT.md").write_text("\n".join(rows), encoding="utf-8", newline="\n")
    print(json.dumps(summary, ensure_ascii=True))


if __name__ == "__main__":
    main()
