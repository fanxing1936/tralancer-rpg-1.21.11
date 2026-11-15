#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""教皇M3独立动作检查；只写m3/validation，不调用构建或修改模型。"""
import argparse
import base64
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import sys
from types import SimpleNamespace

sys.dont_write_bytecode = True
import display_mob as dm
from pope_validate_model import check_parts, require

HERE = Path(__file__).resolve().parent
REF = HERE / "pope_ref"
M3 = REF / "m3"
OUT = M3 / "validation"
BASELINE = OUT / "m2_static_baseline.json"
ORDER = ["idle", "walk", "attack", "summon", "cast", "appear", "teleport_in", "teleport_out", "whirlwind"]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical_hash(value):
    return digest(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def semantic_static(doc, spec):
    """排除编辑器选中状态、预览窗口和动画；保留所有实际几何/材质/父子关系。"""
    groups = [{"uuid": g["uuid"], "name": g["name"], "origin": g["origin"],
               "rotation": g.get("rotation") or [0, 0, 0]} for g in doc["groups"]]
    elements = []
    for e in doc["elements"]:
        elements.append({"uuid": e["uuid"], "name": e["name"], "type": e.get("type", "cube"),
                         "from": e["from"], "to": e["to"], "origin": e.get("origin", [0, 0, 0]),
                         "rotation": e.get("rotation") or [0, 0, 0], "inflate": e.get("inflate", 0),
                         "faces": {n: {"uv": f["uv"], "texture": f.get("texture"), "rotation": f.get("rotation", 0)}
                                   for n, f in e["faces"].items()}})

    def hierarchy(node):
        return {"uuid": node["uuid"], "children": [c if isinstance(c, str) else hierarchy(c) for c in node["children"]]}

    textures = [{"png_sha256": digest(base64.b64decode(t["source"].split(",", 1)[1], validate=True)),
                 "width": t.get("width"), "height": t.get("height"),
                 "uv_width": t.get("uv_width"), "uv_height": t.get("uv_height")} for t in doc["textures"]]
    return {"elements": sorted(elements, key=lambda e: e["uuid"]), "groups": sorted(groups, key=lambda g: g["uuid"]),
            "outliner": [hierarchy(n) for n in doc["outliner"]], "textures": textures, "resolution": doc["resolution"],
            "parts": spec["parts"], "glow": spec["glow"], "model_scale": spec["model_scale"]}


def capture_baseline(model, spec):
    data = model.read_bytes()
    doc = json.loads(data)
    require(not doc.get("animations"), "只能从0动画的已确认M2文件冻结静态基线")
    value = semantic_static(doc, spec)
    result = {"source_bbmodel_sha256": digest(data), "semantic_static_sha256": canonical_hash(value),
              "note": "M2已确认眼神B；语义字段含元素/UV/骨骼rest/层级/PNG/部件/scale，排除编辑器UI与动画。",
              "static_data": value}
    OUT.mkdir(parents=True, exist_ok=True)
    if BASELINE.exists():
        previous = load_json(BASELINE)
        require(previous["semantic_static_sha256"] == result["semantic_static_sha256"], "已有基线不同，禁止覆盖")
    else:
        BASELINE.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return result


def transform_point(matrix, point):
    return [sum(matrix[i][j] * point[j] for j in range(3)) + matrix[i][3] for i in range(3)]


def part_centers(bones, spec, resolution):
    mob = SimpleNamespace(key="pope", tex="rpg:item/pope/atlas", glow=set(spec["glow"]))
    result = {}
    for name, members in spec["parts"]:
        _, offset = dm.part_model(mob, bones, name, members, resolution)
        result[name] = {"bone": members[0], "unposed_center": [x + 8 for x in offset]}
    return result


def numeric(value):
    if isinstance(value, bool):
        return False
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def check_animation_schema(doc, metadata):
    animations = doc.get("animations", [])
    require([a["name"] for a in animations] == ["animation." + n for n in ORDER], "9段动画名称/顺序必须完全匹配接口")
    expected = {entry["name"]: entry for entry in metadata["clips"]}
    require(list(expected) == ORDER, "clipmeta的9段顺序不符")
    ids = {g["uuid"]: g["name"] for g in doc["groups"]}
    reports = []
    for animation in animations:
        name = animation["name"].split("animation.", 1)[1]
        length = animation["length"]
        require(numeric(length) and length > 0, "动作长度须正有限数值：" + name)
        require(abs(length - expected[name]["length"]) < 1e-8, "模型与clipmeta长度不符：" + name)
        require(abs(length * 20 - round(length * 20)) < 1e-8, "动作时长须可精确烘焙到0.05秒：" + name)
        loops = name in ("idle", "walk")
        require((animation.get("loop") == "loop") == loops, "动作循环标记不符：" + name)
        require(bool(expected[name]["loop"]) == loops, "clipmeta循环标记不符：" + name)
        if name.startswith("teleport_"):
            require(abs(length - .9) < 1e-8, "瞬移时长固定0.9秒")
        seen, key_count, times = set(), 0, {0.0, float(length)}
        for uid, animator in animation.get("animators", {}).items():
            require(uid in ids and animator.get("type", "bone") == "bone", "存在未知骨骼或效果动画器")
            for key in animator.get("keyframes", []):
                require(key["channel"] in ("rotation", "position"), "不支持的动作通道：" + key["channel"])
                require(key["interpolation"] in ("linear", "catmullrom", "step"), "不支持的插值")
                require(numeric(key["time"]) and 0 <= key["time"] <= length + 1e-8, "关键帧时刻越界")
                data = key["data_points"]
                require(len(data) == 1 and all(numeric(data[0].get(axis)) for axis in "xyz"), "关键帧须为一组纯数值XYZ，无Molang")
                require(all(not isinstance(data[0].get(axis), str) or not any(c in data[0][axis] for c in "eE") for axis in "xyz"),
                        "Blockbench会将科学计数字符串误解为Molang，关键帧禁止含e/E：%s/%s@%s" % (name, ids[uid], key["time"]))
                signature = (uid, key["channel"], float(key["time"]))
                require(signature not in seen, "同骨骼同通道同时间关键帧重复")
                seen.add(signature)
                key_count += 1
                times.add(float(key["time"]))
        require(key_count, "动作没有关键帧：" + name)
        for moment in expected[name].get("release_times", []):
            require(numeric(moment) and 0 <= moment <= length, "出手时刻越界")
        reports.append({"name": name, "length": length, "loop": loops, "keyframes": key_count, "key_times": sorted(times),
                        "release_times": expected[name].get("release_times", [])})
    return reports


def check_motion_matrices(bones, clips, centers):
    reports = []
    for name in ORDER:
        clip = clips[name]
        times = {i / 20 for i in range(round(clip["length"] * 20) + 1)}
        times.update(float(k[0]) for keys in clip["tracks"].values() for k in keys)
        for time in times:
            for bone in bones:
                matrix = dm.posed_matrix(bones, bone, clip, time)
                require(all(math.isfinite(v) for row in matrix for v in row), "动作矩阵有非有限值")
        row = {"clip": name, "sample_times": len(times), "bones": len(bones)}
        if name in ("idle", "walk"):
            errors = []
            for bone in bones:
                a, b = dm.posed_matrix(bones, bone, clip, 0), dm.posed_matrix(bones, bone, clip, clip["length"])
                errors.append(max(abs(a[i][j] - b[i][j]) for i in range(4) for j in range(4)))
            row["loop_endpoint_matrix_max_error"] = max(errors)
            require(max(errors) < 1e-6, name + " 首尾骨骼变换不闭合")
        reports.append(row)
    return reports


def check_whirlwind(bones, clips, centers, metadata):
    expected = metadata["whirlwind_end_center_model"]
    require(len(expected) == 3 and all(numeric(v) for v in expected), "必须显式给出末帧收拢中心")
    clip = clips["whirlwind"]
    rows = []
    for name, center in centers.items():
        matrix = dm.posed_matrix(bones, center["bone"], clip, clip["length"])
        actual = transform_point(matrix, center["unposed_center"])
        error = math.sqrt(sum((a - b) ** 2 for a, b in zip(actual, expected)))
        rows.append({"part": name, "center_model": actual, "target_error_model_units": error})
    largest = max(r["target_error_model_units"] for r in rows)
    require(largest < 1e-4, "whirlwind末帧部件中心未同点，最大误差%.9g模型单位" % largest)
    return {"target_model": expected, "time": clip["length"], "max_error_model_units": largest, "parts": rows,
            "limitation": "只证明12个刚性部件中心汇聚；无scale通道，部件实际体积没有消失。末姿之后共享管线会回idle，交接由玩法侧负责。"}


def check_audio(metadata):
    config = load_json(M3 / "audio_cues.json")
    sounds = config["sounds"]
    require(len(sounds) == 17, "音效注册须为17组")
    files = []
    for event, value in sounds.items():
        require(len(value) == 3 and len(value[0]) == 2 and value[1], "sounds条目不兼容共享管线：" + event)
        for name in value[1]:
            require(Path(name).name == name and name.endswith(".ogg"), "音效必须保留原OGG文件名")
            require((REF / "sounds" / name).read_bytes().startswith(b"OggS"), "OGG不存在或签名错误")
            require(not any(x in name.lower() for x in ("archvessel", "archvisage", "music", "bgm_")), "越界音效")
            files.append(name)
    require(len(files) == len(set(files)) == 39, "39段原音效须唯一注册")
    lengths = {entry["name"]: entry["length"] for entry in metadata["clips"]}
    release = {entry["name"]: entry.get("release_times", []) for entry in metadata["clips"]}
    for clip, cues in config["cues"].items():
        require(clip in lengths, "音效cue引用未知clip")
        for time, event, volume, pitch in cues:
            require(0 <= time <= lengths[clip] and event in sounds, "cue时间或事件错误")
            require(volume > 0 and pitch == 1, "本次原音效配置应保持pitch=1且音量为正")
        if clip in ("attack", "summon", "cast"):
            actual_release = [cue[0] for cue in cues if cue[1] in ("spell", "summon_mobs")]
            require(actual_release == release[clip], "音效出手时刻与clipmeta不符：" + clip)
    for clip, cues in config["enter_cues"].items():
        require(clip in lengths, "enter_cues引用未知clip")
        for event, volume, pitch in cues:
            require(event in sounds and volume > 0 and pitch == 1, "enter_cue不合法")
            require(not event.startswith("intro_"), "未授权自动播放intro长段")
    require(not config.get("automatic_intro_cues"), "不得自行启用intro长段")
    return {"events": len(sounds), "files": len(files), "automatic_intro_cues": False,
            "release_times": {name: release[name] for name in ("attack", "summon", "cast")},
            "duration_policy": config["duration_policy"], "runtime_status": "M4未接入；未播放音频"}


def check_source_hashes():
    inventory = load_json(REF / "m1/asset_validation.json")
    failures, checked = [], 0
    for row in inventory["assets"]:
        path = REF / row["path"]
        if not path.is_file() or digest(path.read_bytes()) != row["sha256"]:
            failures.append(row["path"])
        checked += 1
    require(not failures, "原素材SHA-256已变化或文件缺失：" + ", ".join(failures))
    require(checked == 59, "M1原素材基线应包含57下载和2引用贴图")
    return {"checked_assets": checked, "changed_assets": 0,
            "source_validation_sha256": digest((REF / "m1/asset_validation.json").read_bytes())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--capture-baseline", action="store_true")
    parser.add_argument("--model", type=Path, default=REF / "pope.bbmodel")
    parser.add_argument("--clipmeta", type=Path, default=M3 / "clipmeta.json")
    args = parser.parse_args()
    spec = load_json(REF / "m2/model_spec.json")
    if args.capture_baseline:
        result = capture_baseline(args.model, spec)
        print(json.dumps({k: v for k, v in result.items() if k != "static_data"}, ensure_ascii=True))
        return 0
    report = {"stage": "M3", "checks": {}, "ok": False, "in_game_verified": False}

    def run(name, function):
        try:
            details = function()
            report["checks"][name] = {"ok": True, "details": details}
            return details
        except Exception as exc:
            report["checks"][name] = {"ok": False, "error": str(exc)}
            return None

    try:
        binary = args.model.read_bytes()
        doc, metadata, baseline = json.loads(binary), load_json(args.clipmeta), load_json(BASELINE)
        report["bbmodel_sha256"] = digest(binary)
        report["clipmeta_sha256"] = digest(args.clipmeta.read_bytes())
        report["audio_cues_sha256"] = digest((M3 / "audio_cues.json").read_bytes())
        report["m2_model_spec_sha256"] = digest((REF / "m2/model_spec.json").read_bytes())
        value = semantic_static(doc, spec)
        report["semantic_static_sha256"] = canonical_hash(value)

        def static_check():
            require(report["semantic_static_sha256"] == baseline["semantic_static_sha256"], "静态几何/UV/材质/层级/部件与M2基线不同")
            return {"m2_source_sha256": baseline["source_bbmodel_sha256"], "semantic_static_sha256": baseline["semantic_static_sha256"]}

        run("静态数据不变", static_check)
        run("9段顺序与纯数值通道", lambda: check_animation_schema(doc, metadata))
        run("17组声音与出手cues", lambda: check_audio(metadata))
        run("59项原素材哈希不变", check_source_hashes)
        part_result = run("12部件与输出坐标", lambda: check_parts(args.model, doc, spec["parts"], spec["glow"]))
        if part_result:
            bones, part_rows = part_result
            require(len(part_rows) == 12, "本工程已确认12部件，不应悄然改数")
            report["checks"]["12部件与输出坐标"]["details"] = part_rows
            mob = SimpleNamespace(bbmodel=args.model, anim_from=None, key="pope")
            clips = dm.load_animations(mob)
            centers = part_centers(bones, spec, doc["resolution"])
            run("逐刻矩阵与循环闭合", lambda: check_motion_matrices(bones, clips, centers))
            run("whirlwind末帧收拢", lambda: check_whirlwind(bones, clips, centers, metadata))
        require(digest(args.model.read_bytes()) == report["bbmodel_sha256"], "模型在检查过程中被更新，需重跑")
        require(digest(args.clipmeta.read_bytes()) == report["clipmeta_sha256"], "clipmeta在检查过程中被更新，需重跑")
        require(digest((M3 / "audio_cues.json").read_bytes()) == report["audio_cues_sha256"], "音效配置在检查过程中被更新，需重跑")
    except (Exception, SystemExit) as exc:
        report["checks"]["输入与执行完整性"] = {"ok": False, "error": str(exc)}
    report["ok"] = bool(report["checks"]) and all(item["ok"] for item in report["checks"].values())
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "motion_validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    lines = ["# 教皇 M3 动作数值验证", "", "结果：" + ("通过" if report["ok"] else "未全部通过"), "",
             "模型 SHA-256：`%s`。" % report.get("bbmodel_sha256", "无法读取"), "",
             "| 检查 | 结果 | 说明 |", "|---|---|---|"]
    for name, check in report["checks"].items():
        lines.append("| %s | %s | %s |" % (name, "通过" if check["ok"] else "失败", check.get("error", "实测细节见JSON").replace("|", "/")))
    lines += ["", "本检查不证明视觉复刻，必须结合逐帧并排图。没有运行构建、玩法、资源包或专用服务器检查；未在真实游戏内看过。", "",
              "静态数据哈希排除编辑器UI和动画字段，保留实际几何、UV、骨骼rest/层级、PNG、部件与model_scale。", ""]
    (OUT / "MOTION_VALIDATION.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(json.dumps({"ok": report["ok"], "bbmodel_sha256": report.get("bbmodel_sha256"),
                      "problems": {k: v["error"] for k, v in report["checks"].items() if not v["ok"]}}, ensure_ascii=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
