"""在教皇任务独占的快照中运行完整构建，不回写工作区或 Minecraft 实例。

用法：python _tools/pope_build_check.py --run
只准备快照：省略 --run。复用已登记快照：--existing --run。
build.sh 会删除并重建 rpg；因此本脚本从不在原仓库运行它。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_tools/pope_ref/m4/build"
WORK = ROOT / "_pope_m4_qa_20261105"
BASH = Path(r"C:\Program Files\Git\bin\bash.exe")
LARGE_REFS = {"pope_ref", "heart_of_ender_ref", "arch_visage_ref"}


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", "utf-8")


def linked(path):
    return path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction())


def safe_snapshot(path):
    """Check literal and resolved destinations before calling destructive builds."""
    path = Path(path).absolute()
    base = WORK.absolute()
    if linked(base) or linked(path) or base.resolve() != base:
        raise ValueError("隔离根不得为链接或目录联接: " + str(path))
    if path.parent != base or not path.name.startswith("build_"):
        raise ValueError("不是教皇专用构建快照: " + str(path))
    resolved = path.resolve()
    if resolved.parent != base.resolve() or resolved == ROOT:
        raise ValueError("快照路径越界: " + str(resolved))
    for name in ("rpg", "resourcepack", "_orig", "_orig_rp", "_tools"):
        target = path / name
        if linked(target) or target.resolve().parent != resolved:
            raise ValueError("构建目标必须为隔离根的直属非链接目录: " + str(target))
    return resolved


def copy_file(src, dst, inventory):
    before = sha(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    if sha(dst) != before or sha(src) != before:
        raise RuntimeError("快照期间输入发生变化，请重新创建快照: " + str(src))
    inventory[src.relative_to(ROOT).as_posix()] = before


def copy_tree(src, dst, inventory, skip=None):
    for directory, dirs, files in os.walk(src, followlinks=False):
        directory = Path(directory)
        dirs[:] = [name for name in dirs
                   if name not in {"__pycache__", ".pytest_cache", "node_modules"}
                   and not linked(directory / name)
                   and not (skip and skip(directory, name))]
        for name in files:
            source = directory / name
            if linked(source) or source.suffix == ".pyc":
                continue
            copy_file(source, dst / source.relative_to(src), inventory)


def prepare():
    if not (ROOT / "_tools/add_pope_model.py").is_file():
        raise ValueError("先完成 add_pope_model.py，再创建构建快照")
    dest = safe_snapshot(WORK / ("build_" + str(time.time_ns())))
    dest.mkdir(parents=True, exist_ok=False)
    inventory = {}
    # Build generators use root JSON/art metadata and these non-tool trees.
    for source in ROOT.iterdir():
        if source.is_file() and source.suffix.lower() not in {".zip", ".log"}:
            copy_file(source, dest / source.name, inventory)
    for name in ("_orig", "_orig_rp", "resourcepack", "rpg", "docs", "_art_audit", "_art_crops"):
        source = ROOT / name
        if source.is_dir():
            copy_tree(source, dest / name, inventory)
    copy_tree(ROOT / "_tools", dest / "_tools", inventory,
              skip=lambda directory, name: directory == ROOT / "_tools" and name in LARGE_REFS)

    exact = {
        "pope_ref": ["pope.bbmodel", "m2/model_spec.json", "m3/audio_cues.json", "m3/clipmeta.json"],
        "heart_of_ender_ref": ["heart_of_ender.bbmodel", "m2_geometry/geometry_spec.json"],
        "arch_visage_ref": ["arch_visage.bbmodel", "config.json"],
    }
    for ref, names in exact.items():
        source = ROOT / "_tools" / ref
        target = dest / "_tools" / ref
        for name in names:
            copy_file(source / name, target / name, inventory)
        # Keep small top-level metadata for thin configurations, not research media.
        for item in source.glob("*.json"):
            copy_file(item, target / item.name, inventory)
        if (source / "sounds").is_dir():
            copy_tree(source / "sounds", target / "sounds", inventory)

    marker = {
        "snapshot": str(dest), "source_root": str(ROOT), "created_at_ns": time.time_ns(),
        "purpose": "原始 rp_build.sh / build.sh / rp_validate.py 的隔离运行；无回写、无客户端同步",
        "excluded": "三套大型研究目录的抽帧/视频/报告、服务器世界、node_modules、缓存；保留精确构建输入",
        "copied_files": len(inventory), "build_inputs_sha256": inventory,
    }
    write(dest / "pope_build_snapshot.json", marker)
    write(OUT / "snapshot.json", marker)
    print("Prepared " + str(dest), flush=True)
    return dest


def run(snapshot):
    snapshot = safe_snapshot(snapshot)
    if not BASH.is_file():
        raise FileNotFoundError(BASH)
    marker = json.loads((OUT / "snapshot.json").read_text("utf-8"))
    if snapshot != Path(marker["snapshot"]).resolve():
        raise ValueError("未登记的隔离快照")
    local_marker = json.loads((snapshot / "pope_build_snapshot.json").read_text("utf-8"))
    if local_marker != marker:
        raise ValueError("快照登记信息不一致")

    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env.get("PATH", "")
    commands = [
        ("rp_build", [str(BASH), "_tools/rp_build.sh"]),
        ("build", [str(BASH), "_tools/build.sh"]),
        ("rp_validate", [sys.executable, "-X", "utf8", "_tools/rp_validate.py", "resourcepack"]),
    ]
    results = []
    for label, command in commands:
        safe_snapshot(snapshot)  # Immediately recheck both destructive targets.
        log = OUT / (label + ".log")
        start = time.monotonic()
        print("Starting " + label + " in isolated snapshot", flush=True)
        error = None
        with log.open("w", encoding="utf-8", newline="\n") as stream:
            try:
                proc = subprocess.run(command, cwd=snapshot, env=env, stdout=stream,
                                      stderr=subprocess.STDOUT, timeout=1800,
                                      creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
                code = proc.returncode
            except subprocess.TimeoutExpired:
                code, error = 124, "1800 秒构建超时"
        record = {
            "name": label, "command": command, "cwd": str(snapshot), "exit_code": code,
            "seconds": round(time.monotonic() - start, 2), "log": str(log),
            "log_sha256": sha(log), "error": error,
        }
        results.append(record)
        write(OUT / "build_results.json", {
            "snapshot": str(snapshot), "steps": results,
            "all_passed": len(results) == 3 and all(r["exit_code"] == 0 for r in results),
            "workspace_build_performed": False, "client_sync_performed": False,
        })
        print(json.dumps(record, ensure_ascii=False), flush=True)
        if code:
            print("\n".join(log.read_text("utf-8").splitlines()[-30:]), flush=True)
            raise SystemExit(code)
    print("All original build/validate entrypoints passed", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--existing", action="store_true")
    args = parser.parse_args()
    snapshot = (Path(json.loads((OUT / "snapshot.json").read_text("utf-8"))["snapshot"])
                if args.existing else prepare())
    if args.run:
        run(snapshot)
