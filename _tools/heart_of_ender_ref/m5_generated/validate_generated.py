"""重跑正式HE/AV专用离线检查，限定本目录输出；不构建主包/同步实例。

必须传入已冻结模型的完整SHA。先验证输入，再各生成两遍比较字节，
随后重建所有已发送部件状态并与bbmodel重烘焙值比较。
本脚本位于m5_generated根；生成器只清理其下RP/DP的模型专属目录。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
TOOLS = BASE.parents[1]
sys.path.insert(0, str(TOOLS))
import display_mob as dm
import ender_debug_model as helper
import add_heart_of_ender as he
import add_arch_visage as av


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot():
    # 只统计两包；不把验证脚本/结果本身混入“生成器幂等文件数”。
    return {str(path.relative_to(BASE)): sha(path)
            for pack in (BASE / "resourcepack", BASE / "datapack")
            for path in pack.rglob("*") if path.is_file()}


def validate(expected_he, expected_av):
    rp, dp = BASE / "resourcepack", BASE / "datapack"
    inputs = [TOOLS / name for name in (
        "display_mob.py", "ender_debug_model.py", "add_heart_of_ender.py",
        "add_arch_visage.py", "heart_of_ender_emission.py",
        "heart_of_ender_ref/heart_of_ender.bbmodel", "arch_visage_ref/arch_visage.bbmodel",
        "arch_visage_ref/config.json")]
    inputs.append(Path(__file__).resolve())
    prior = {str(path): sha(path) for path in inputs}
    assert sha(TOOLS / "heart_of_ender_ref/heart_of_ender.bbmodel") == expected_he, "HE模型尚非指定冻结SHA"
    assert sha(TOOLS / "arch_visage_ref/arch_visage.bbmodel") == expected_av, "AV模型尚非指定冻结SHA"
    reports = [he.main(str(rp), str(dp)), av.main(str(rp), str(dp))]
    first = snapshot()
    he.main(str(rp), str(dp))
    av.main(str(rp), str(dp))
    second = snapshot()
    assert first == second, [k for k in first.keys() | second.keys() if first.get(k) != second.get(k)]
    assert prior == {str(path): sha(path) for path in inputs}, "生成期间输入有变"
    assert [r["model_sha256"] for r in reports] == [expected_he, expected_av]

    # 读取薄配置所构造的实际Mob，不再触发输出，也不复制配置常量。
    originals = [he.build_debug, av.build_debug]
    for mod in (he, av):
        mod.build_debug = lambda mob, *args, **kwargs: (mob, args, kwargs)
    results = []
    try:
        for mod, report in zip((he, av), reports):
            mob, _, _ = mod.main()
            doc = json.loads(Path(mob.bbmodel).read_text("utf8"))
            bones, png, res = dm.load_bbmodel(mob)
            clips = dm.load_animations(mob)
            mob.parts = helper.assemble_parts(mob.parts, bones, clips)
            mob.glow = set(bones)
            assert (rp / f"assets/rpg/textures/item/{mob.key}/atlas.png").read_bytes() == png
            offsets = {}
            elements = faces = 0
            tinted = []
            for part, members in mob.parts:
                expected, offsets[part] = dm.part_model(mob, bones, part, members, res)
                actual = json.loads((rp / f"assets/rpg/models/{mob.key}/{part}.json").read_text("utf8"))
                item = json.loads((rp / f"assets/rpg/items/{mob.key}/{part}.json").read_text("utf8"))
                ordered = [cube for name in members for cube in bones[name]["cubes"]]
                assert len(actual["elements"]) == len(ordered)
                for i, element in enumerate(actual["elements"]):
                    elements += 1
                    faces += len(element["faces"])
                    assert element["light_emission"] == 15 and element["shade"] is False
                    assert all(-16 <= v <= 32 for v in element["from"] + element["to"])
                    for face, value in element["faces"].items():
                        assert all(0 <= v <= 16 for v in value["uv"])
                        assert value["uv"] == expected["elements"][i]["faces"][face]["uv"]
                        if value["tintindex"]:
                            assert value["tintindex"] == 1
                            assert item["model"]["tints"][1] == {"type": "minecraft:constant", "value": 16765951}
                            tinted.append((ordered[i]["uuid"], face))
                assert item["model"]["tints"][0] == {"type": "minecraft:custom_model_data", "index": 0, "default": 16777215}
            assert set(tinted) == {(m["element_uuid"], m["face"]) for m in doc["unhandled_root_fields"]["emissive_masks"]}
            assert len(tinted) == 2 and elements == len(doc["elements"])
            baked = dm.bake(mob, bones, offsets, clips)
            root = dp / f"data/rpg/function/{mob.key}"
            functions = {path.relative_to(root).as_posix()[:-11]: path.read_text("utf8")
                         for path in root.rglob("*.mcfunction")}
            references = 0
            for name, text in functions.items():
                for target in re.findall(r"\bfunction " + re.escape(mob.fn) + r"/([a-z0-9_/]+)", text):
                    assert target in functions, (name, target)
                    references += 1
                commands = "\n".join(line for line in text.splitlines() if not line.startswith("#"))
                assert all(word not in commands for word in ("rpg.hurt", "rpg:taint", "particle ", "damage ", "minecraft:vindicator"))
            states = emitted = cues = 0
            worst = 0.
            pattern = re.compile(r"tag=" + re.escape(mob.tag) + r"\.p\.([a-z0-9_]+).*translation:\[([^]]+)\],left_rotation:\[([^]]+)\]")
            for name, clip in baked.items():
                state = {}
                for tick, frame in clip["frames"]:
                    text = functions[f"anim/{name}/f{tick}"]
                    actual_cues = [line for line in text.splitlines() if "playsound " in line]
                    assert actual_cues == dm.cue_lines(mob, name, tick, 1)
                    cues += len(actual_cues)
                    for line in text.splitlines():
                        match = pattern.search(line)
                        if match:
                            state[match[1]] = [float(v.rstrip("f")) for v in (match[2] + "," + match[3]).split(",")]
                            emitted += 1
                    assert set(state) == set(frame)
                    for part, component in frame.items():
                        error = max(abs(a - b) for a, b in zip(state[part], component[0] + component[1]))
                        worst = max(worst, error)
                        assert error < .000106, (name, tick, part, error)
                        states += 1
                expected_enter = [dm.playsound(mob, e, v, p) for e, v, p in mob.enter_cues.get(name, ())]
                assert [line for line in functions[f"anim/enter/{name}"].splitlines() if line.startswith("playsound ")] == expected_enter
                assert len(report["clips"]) == len(baked)
            assert functions["debug/spawn"].count('id:"minecraft:item_display"') == len(mob.parts)
            assert functions["debug/spawn"].count("brightness:{block:15,sky:15}") == len(mob.parts)
            assert "Marker:1b,Invisible:1b,NoGravity:1b" in functions["debug/spawn"]
            assert f'function {mob.fn}/anim/enter/{report["runtime"]["initial_clip"]}' in functions["internal/initialize"]
            assert "distance=..32,sort=nearest,limit=1" in functions["debug/pause"]
            assert "execute on passengers" in functions["internal/clear"]
            assert "anim/stride" not in functions
            sound_count = 0
            for _, files, _ in mob.sounds.values():
                for filename in files:
                    dest = Path(filename).stem.lower().replace("-", "_") + ".ogg"
                    assert (Path(mob.sound_dir) / filename).read_bytes() == (rp / f"assets/rpg/sounds/{mob.key}" / dest).read_bytes()
                    sound_count += 1
            for kind in ("load", "tick"):
                tags = json.loads((dp / f"data/minecraft/tags/function/{kind}.json").read_text("utf8"))["values"]
                assert tags.count(f"{mob.fn}/{kind}") == 1
                if kind == "tick":
                    assert tags.count(f"{mob.fn}/tick_late") == 1
            results.append({
                "key": mob.key, "model_sha256": report["model_sha256"], "parts": len(mob.parts),
                "elements": elements, "faces": faces, "clips": report["clips"], "functions": len(functions),
                "resolved_function_references": references, "part_states_checked": states,
                "transform_commands": emitted, "max_component_error": worst, "frame_cues": cues,
                "enter_cues": sum(len(value) for value in mob.enter_cues.values()),
                "byte_identical_sound_files": sound_count, "raw_mask_faces": len(tinted),
                "initial_clip": report["runtime"]["initial_clip"],
                "checks": ["single_png_preserved", "part_bounds", "uv_matches_source", "all_elements_fullbright",
                           "exact_mask_tints", "all_function_references", "no_gameplay_commands", "all_baked_states",
                           "frame_cues", "enter_cues", "passengers_fullbright", "correct_initial_clip", "scoped_controls",
                           "no_auto_walk", "source_sound_bytes", "unique_hooks"],
            })
    finally:
        he.build_debug, av.build_debug = originals
    json_count = 0
    for pack in (rp, dp):
        for path in pack.rglob("*.json"):
            json.loads(path.read_text("utf8"))
            json_count += 1
    result = {
        "scope": "M5 generated outputs only; no main pack build or instance write", "models": results,
        "two_runs_byte_identical": True, "identical_file_count": len(second), "json_files_parsed": json_count,
        "source_inputs_unchanged": True, "input_sha256": prior,
        "named_check_groups": sum(len(row["checks"]) for row in results) + 3,
        "server_test": "delegated to independent final_test; not claimed by this offline audit",
    }
    (BASE / "validation.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    print(json.dumps({k: v for k, v in result.items() if k not in ("input_sha256", "models")}, ensure_ascii=False, indent=2))
    print(json.dumps([{k: v for k, v in row.items() if k not in ("clips", "checks")} for row in results], ensure_ascii=False, indent=2))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected-he", required=True, help="已冻结HE完整SHA256")
    parser.add_argument("--expected-av", required=True, help="已冻结AV完整SHA256")
    options = parser.parse_args()
    validate(options.expected_he, options.expected_av)
