"""M3 制作入口：已确认 R2 静态工程 + 来源轨道 + 紫色图集，经 Blockbench 导出。

不被构建脚本调用。保存后的 .bbmodel 是事实来源；重建已有 M3 文件须显式允许。
"""
from __future__ import annotations
import argparse
import base64
import copy
import hashlib
import json
from pathlib import Path

from heart_of_ender_blockbench import BlockbenchMCP, REF
from heart_of_ender_geo import uid, verify_export

OUT = REF / "m3_motion"
ORDER = ("idle", "walk", "mortar", "cross_beam", "sink", "rise", "death")

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def baseline():
    OUT.mkdir(exist_ok=True)
    source = REF / "m2_endcaps/R2.bbmodel"
    target = OUT / "accepted_R2.bbmodel"
    if not target.exists():
        document = read(source)
        if document.get("animations"):
            raise ValueError("R2 基线应为已验收无动画模型")
        target.write_bytes(source.read_bytes())
        write(OUT / "accepted_R2.json", {
            "date": "2026-11-04", "decision": "用户选择 R2 并确认静态造型；授权 M3 动作和紫色调色",
            "source": "m2_endcaps/R2.bbmodel", "sha256": sha(target),
            "glow_mask": "44x44 RGBA 保持原样", "geometry_status": "accepted static baseline"})
    if sha(target) != read(OUT / "accepted_R2.json")["sha256"]:
        raise ValueError("已验收 R2 基线发生未登记变化")
    return target

def combine():
    base = baseline()
    document = copy.deepcopy(read(base))
    shell = read(OUT / "shell_motion.json")
    inner = read(OUT / "inner_motion.json")
    shell_clips = {c["name"]: c for c in shell["clips"]}
    # M3 原生复核后采用 C1：原静态肢根固定，仅旋转抬肢；不采用 C2 根位移。
    cross_study = read(OUT / "shell_cross_open_options.json")
    shell_clips["cross_beam"] = next(c["clip"] for c in cross_study["options"] if c["id"] == "C1")
    inner_clips = {c["name"]: c for c in inner["clips"]}
    groups = {g["name"]: g for g in document["groups"]}
    animations, info = [], []
    for name in ORDER:
        clip = shell_clips[name]
        tracks = list(clip["tracks"])
        if name in inner_clips:
            other = inner_clips[name]
            if other["length"] != clip["length"]:
                raise ValueError((name, "内外轨道长度不一致"))
            tracks += other["tracks"]
        if name == "death":
            # 从 R2 rest 几何算得：沿世界 -Y 下移，小人最高点在地面下再留 2 单位。
            # 父 shell_root 有 -12° Z rest，故局部位移包含 X；仅 position，无 scale/隐藏开关。
            tracks.append({"bone":"inner_root","channel":"position","keyframes":[
                {"time":0,"value":[0,0,0]}, {"time":3.2,"value":[0,0,0]},
                {"time":3.8,"value":[2.748977,-12.932920,0]},
                {"time":4.0,"value":[2.748977,-12.932920,0]}]})
        seen = set()
        animators = {}
        for track in tracks:
            bone, channel = track["bone"], track["channel"]
            if bone not in groups or channel not in ("rotation", "position"):
                raise ValueError((name, bone, channel))
            if (bone, channel) in seen:
                raise ValueError((name, bone, channel, "重复轨道"))
            seen.add((bone, channel))
            animator = animators.setdefault(groups[bone]["uuid"], {"name": bone, "type": "bone", "keyframes": []})
            times = set()
            for i, key in enumerate(track["keyframes"]):
                time = key["time"]
                if time in times or not 0 <= time <= clip["length"]+1e-6:
                    raise ValueError((name, bone, channel, time, "重复或越界时间"))
                times.add(time)
                values = key["value"]
                if len(values) != 3 or any(not isinstance(x, (int, float)) for x in values):
                    raise ValueError("关键帧必须是纯数字三元组")
                animator["keyframes"].append({"uuid": uid(f"M3/{name}/{bone}/{channel}/{i}"),
                    "channel": channel, "time": time, "color": -1,
                    "interpolation": key.get("interpolation", "linear"),
                    "data_points": [dict(zip("xyz", values))]})
        animations.append({"uuid": uid("M3/animation/"+name), "name": "animation."+name,
            "loop": "loop" if clip["loop"] else "once", "override": False,
            "length": clip["length"], "snapping": 25, "selected": False,
            "anim_time_update": "", "blend_weight": "", "start_delay": "", "loop_delay": "",
            "animators": animators})
        info.append({"name": name, "length": clip["length"], "loop": clip["loop"],
            "tracks": len(tracks), "keyframes": sum(len(t["keyframes"]) for t in tracks),
            "shell_evidence": clip["evidence"], "inner_evidence": inner_clips.get(name, {}).get("evidence", "推断/保持")})
    atlas = REF / "m3_material/atlas.png"
    document["textures"][0]["source"] = "data:image/png;base64,"+base64.b64encode(atlas.read_bytes()).decode()
    document["textures"][0]["name"] = "heart_of_ender_atlas_m3.png"
    document["animations"] = animations
    document["name"] = "heart_of_ender"
    document.setdefault("unhandled_root_fields", {})["heart_of_ender_stage"] = "M3 animation review; accepted R2 geometry"
    document["unhandled_root_fields"]["material_status"] = {
        "atlas": "m3_material/atlas.png", "color": "source-derived purple recoloring authorized 2026-11-04",
        "emission": "all material bones fullbright; no bloom; runtime validation pending M5",
        "mask": "44x44 RGBA preserved; no independent mask shader implemented"}
    return document, info

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--port", type=int, default=52907)
    ap.add_argument("--replace-authored", action="store_true")
    ap.add_argument("--baseline-only", action="store_true")
    args = ap.parse_args()
    baseline()
    if args.baseline_only:
        print("已保存用户确认的 R2 静态基线")
        return
    target = REF / "heart_of_ender.bbmodel"
    if read(target).get("unhandled_root_fields",{}).get("material_status",{}).get("version") in ("M3 material v2", "M3 material v3", "Final material v4"):
        raise ValueError("主稿已使用 M3 材质修订；旧动作入口不能覆盖。材质重建须使用对应版本的 material 脚本，新增动作须先显式迁移已保存的动画。")
    if read(target).get("animations") and not args.replace_authored:
        raise ValueError("已有 M3 动作；核对无额外手改后使用 --replace-authored")
    document, clips = combine()
    client = BlockbenchMCP(args.port)
    client.tool("create_project", {"name": "heart_of_ender_m3", "format": "bedrock"})
    serialized = json.dumps(document).replace("/", r"\u002f")
    client.evaluate("(function(){Codecs.project.parse("+serialized+");return {uuid:Project.uuid,animations:Animation.all.length};})()")
    result = client.tool("export_model", {"codec_id": "project", "options": {"raw": False}, "max_content_length": 2000000})
    payload = json.loads(next(x["text"] for x in result["content"] if x["type"] == "text"))
    if payload["truncated"]:
        raise ValueError("导出截断，未保存")
    actual = json.loads(payload["content"])
    audit = verify_export(document, actual)
    # 动作字段也必须验证，不能仅验证静态几何。
    if len(actual.get("animations", [])) != len(document["animations"]):
        raise ValueError("动作数量被导出改变")
    for expected, got in zip(document["animations"], actual["animations"]):
        for prop in ("name", "length", "loop"):
            if expected[prop] != got[prop]:
                raise ValueError((expected["name"], prop))
        for bone_id, animator in expected["animators"].items():
            a = {(k["channel"], k["uuid"]): k for k in animator["keyframes"]}
            b = {(k["channel"], k["uuid"]): k for k in got["animators"][bone_id]["keyframes"]}
            if a.keys() != b.keys():
                raise ValueError("导出改变关键帧集合")
            for key, k in a.items():
                if abs(k["time"]-b[key]["time"]) > 0.00000501 or k["interpolation"] != b[key]["interpolation"]:
                    raise ValueError("导出改变关键帧时间/插值")
                for axis in "xyz":
                    if abs(float(k["data_points"][0][axis])-float(b[key]["data_points"][0][axis])) > 0.00000501:
                        raise ValueError("导出改变动作值")
    # 保留 M2 历史基线和证据；不会用 M3 反写旧报告的像素核验。
    prior = REF / "m2_endcaps/R0.bbmodel"
    if not prior.exists() and not read(target).get("animations"):
        prior.write_bytes(target.read_bytes())
    target.write_text(payload["content"], encoding="utf-8")
    audit.update({"bbmodel_sha256": sha(target), "accepted_base_sha256": sha(baseline()),
                  "atlas_sha256": sha(REF / "m3_material/atlas.png"), "clips": clips,
                  "cross_shell_revision": "shell_cross_open_options.json / C1; static roots retained",
                  "animations_checked": True, "unrecorded_manual_edits": False})
    write(OUT / "authoring_audit.json", audit)
    client.evaluate("(function(){Project.save_path="+json.dumps(str(target))+";Project.saved=true;return true;})()")
    print(json.dumps({"model": str(target), "sha256": sha(target), "clips": clips}, ensure_ascii=False))

if __name__ == "__main__":
    main()
