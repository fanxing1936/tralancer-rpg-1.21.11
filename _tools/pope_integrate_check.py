"""只生成教皇产物，核验其他产物/共享注册项不变与重复生成确定性。"""
from __future__ import annotations

import base64
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_tools/pope_ref/m4/integration"
OWN = (
    "rpg/data/rpg/function/pope/", "rpg/data/rpg/predicate/pope/",
    "resourcepack/assets/rpg/models/pope/", "resourcepack/assets/rpg/items/pope/",
    "resourcepack/assets/rpg/textures/item/pope/", "resourcepack/assets/rpg/sounds/pope/",
)
SHARED = (
    "rpg/data/minecraft/tags/function/load.json",
    "rpg/data/minecraft/tags/function/tick.json",
    "resourcepack/assets/rpg/sounds.json",
    "resourcepack/assets/rpg/lang/zh_cn.json",
    "resourcepack/assets/rpg/lang/en_us.json",
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text("utf-8"))


def write(name, data):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", "utf-8")


def protected_files():
    result = {}
    for name in ("rpg", "resourcepack", "_tools"):
        for folder, dirs, files in os.walk(ROOT / name):
            dirs[:] = [d for d in dirs if d not in {"__pycache__", "node_modules", "pope_ref"}]
            if name == "_tools":
                # 研究素材目录含其他任务的历史构建副本，只核验共享工具源文件。
                # 原始素材与模型另由 independent_preintegration_audit 逐项核验。
                dirs[:] = []
            for file in files:
                path = Path(folder) / file
                rel = path.relative_to(ROOT).as_posix()
                if (rel in SHARED or rel.startswith(OWN) or file.startswith(("pope_", "add_pope_model"))
                        or path.suffix == ".pyc"):
                    continue
                result[rel] = sha(path)
    for file in ("docs/POPE-DESIGN.md", "_data_loot.json", "_guide_sections.json"):
        path = ROOT / file
        if path.exists():
            result[file] = sha(path)
    return result


def shared_others():
    result = {}
    for rel in SHARED:
        doc = read(ROOT / rel)
        if "/tags/" in rel:
            doc["values"] = [v for v in doc["values"] if not str(v).startswith("rpg:pope/")]
        else:
            doc = {k: v for k, v in doc.items()
                   if not k.startswith(("pope.", "subtitles.rpg.pope."))}
        result[rel] = doc
    return result


def output_hashes():
    result = {rel: sha(ROOT / rel) for rel in SHARED}
    for folder in OWN:
        for path in (ROOT / folder).rglob("*"):
            if path.is_file():
                result[path.relative_to(ROOT).as_posix()] = sha(path)
    return result


def validate_generated():
    ref = ROOT / "_tools/pope_ref"
    doc = read(ref / "pope.bbmodel")
    spec = read(ref / "m2/model_spec.json")
    meta = read(ref / "m3/clipmeta.json")
    audio = read(ref / "m3/audio_cues.json")
    atlas = ROOT / "resourcepack/assets/rpg/textures/item/pope/atlas.png"
    assert atlas.read_bytes() == base64.b64decode(doc["textures"][0]["source"].split(",", 1)[1])
    func = ROOT / "rpg/data/rpg/function/pope"
    summon = (func / "summon.mcfunction").read_text("utf-8")
    commands = [l for l in summon.splitlines() if l and not l.startswith("#")]
    assert len(commands) == 1 and commands[0].startswith("summon minecraft:vindicator ")
    assert summon.count('id:"minecraft:item_display"') == 12
    assert "Health:1000f" in summon
    assert 'attributes:[{id:"minecraft:max_health",base:1000f}]' in summon
    assert 'Tags:["rpg.pope"]' in summon
    assert "NoAI:" not in summon
    for name, _ in spec["parts"]:
        model = read(ROOT / ("resourcepack/assets/rpg/models/pope/" + name + ".json"))
        for el in model["elements"]:
            assert all(-16 <= v <= 32 for v in el["from"] + el["to"])
            assert (el.get("light_emission", 0) == 15) == (name == "staff_glow")
    clips = []
    for clip in meta["clips"]:
        name, idx = clip["name"], clip["id"]
        enter = (func / "anim/enter" / (name + ".mcfunction")).read_text("utf-8")
        assert "scoreboard players set @s rpg_pp_anim %d" % idx in enter
        step = 4 if name == "idle" else 1
        ticks = round(clip["length"] * 20)
        expected = set(range(0, ticks if clip["loop"] else ticks + 1, step))
        actual = {int(p.stem[1:]) for p in (func / "anim" / name).glob("f*.mcfunction")}
        assert expected == actual
        for sec, event, _, _ in audio["cues"].get(name, []):
            tick = round(sec * 20)
            matches = [p.stem for p in (func / "anim" / name).glob("f*.mcfunction")
                       if "playsound rpg:pope.%s " % event in p.read_text("utf-8")]
            assert matches == ["f%d" % tick], (name, event, matches)
        for event, _, _ in audio["enter_cues"].get(name, []):
            assert "playsound rpg:pope.%s " % event in enter
        clips.append({"id": idx, "name": name, "seconds": clip["length"],
                      "ticks": ticks, "sample_step": step, "frames": len(actual)})
    sound_doc = read(ROOT / "resourcepack/assets/rpg/sounds.json")
    assert len([k for k in sound_doc if k.startswith("pope.")]) == 17
    copies = 0
    for _, files, _ in audio["sounds"].values():
        for file in files:
            outname = Path(file).stem.lower().replace("-", "_") + ".ogg"
            assert sha(ref / "sounds" / file) == sha(ROOT / "resourcepack/assets/rpg/sounds/pope" / outname)
            copies += 1
    tick = read(ROOT / SHARED[1])["values"]
    assert tick.count("rpg:pope/tick") == tick.count("rpg:pope/tick_late") == 1
    assert tick.index("rpg:pope/tick") < tick.index("rpg:command/tick_end") < tick.index("rpg:pope/tick_late")
    for name in ("tick_dimension", "tick_late"):
        text = (func / (name + ".mcfunction")).read_text("utf-8")
        assert "@e[" in text
        assert "@e[" not in text.replace("@e[distance=0..,", ""), name + " 存在跨维度选择器"
    return {"model_sha256": sha(ref / "pope.bbmodel"), "parts": 12, "clips": clips,
            "sound_groups": 17, "sound_files_byte_identical": copies}


def main():
    baseline = protected_files()
    shared = shared_others()
    write("protected_before.json", baseline)
    write("shared_nonpope_before.json", shared)
    logs = []
    first = None
    for run in (1, 2):
        proc = subprocess.run([sys.executable, "-X", "utf8", "_tools/add_pope_model.py", "resourcepack", "rpg"],
                              cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        logs.append({"run": run, "exit_code": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr})
        write("generation_runs.json", logs)
        assert proc.returncode == 0, proc.stderr
        assert shared_others() == shared, "共享索引的非教皇条目发生变化"
        changed = [p for p, digest in baseline.items() if not (ROOT / p).exists() or sha(ROOT / p) != digest]
        write("protected_changes.json", changed)
        assert not changed, "保护路径发生变化: " + str(changed)
        outputs = output_hashes()
        if first is None:
            first = outputs
        else:
            assert outputs == first, "重复生成字节不一致"
    validation = validate_generated()
    validation.update(all_passed=True, protected_file_count=len(baseline),
                      shared_nonpope_entries_unchanged=True, deterministic_runs=2,
                      generated_file_count=len(first) - len(SHARED))
    write("output_hashes.json", first)
    write("integration_validation.json", validation)
    print(json.dumps(validation, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
