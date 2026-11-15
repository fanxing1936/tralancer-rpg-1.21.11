"""Run the unmodified server_test.py on the completed isolated Pope M4 build.

Uses a new localhost-only world, copies an already accepted EULA without
changing it, and preserves both the original tool output and the server log.
This is a full-pack loading smoke test, not client visual verification.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import socket
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_tools/pope_ref/m4/server_smoke"
BUILD_RESULT = ROOT / "_tools/pope_ref/m4/build/build_results.json"
WORK = ROOT / "_pope_m4_qa_20261105"
EULA = Path(r"D:\minecraft\本地部署\eula.txt")
PORT = 25676
EXPECTED_OFFLINE = {
    "**** SERVER IS RUNNING IN OFFLINE/INSECURE MODE!",
    "The server will make no attempt to authenticate usernames. Beware.",
    "While this makes the game possible to play without internet access, it also opens up the ability for hackers to connect with any username they choose.",
    'To change this, set "online-mode" to "true" in the server.properties file.',
}
POPE_TREES = (
    "rpg/data/rpg/function/pope", "rpg/data/rpg/predicate/pope",
    "resourcepack/assets/rpg/items/pope", "resourcepack/assets/rpg/models/pope",
    "resourcepack/assets/rpg/sounds/pope", "resourcepack/assets/rpg/textures/item/pope",
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def tree_hashes(path):
    return {p.relative_to(path).as_posix(): sha(p)
            for p in sorted(path.rglob("*")) if p.is_file()}


def pope_product_comparison(snapshot):
    rows = []
    for relative in POPE_TREES:
        live = tree_hashes(ROOT / relative)
        built = tree_hashes(snapshot / relative)
        rows.append({"path": relative, "workspace_files": len(live),
                     "isolated_files": len(built), "equal": live == built,
                     "missing_workspace": sorted(set(built) - set(live)),
                     "extra_workspace": sorted(set(live) - set(built)),
                     "different": [p for p in sorted(set(live) & set(built))
                                   if live[p] != built[p]],
                     "isolated_sha256": built})
    return {"all_equal": all(r["equal"] for r in rows),
            "file_count": sum(r["workspace_files"] for r in rows), "trees": rows}


def classify_console(text):
    known, unexpected, warnings, errors = [], [], [], []
    issue = re.compile(r"Whilst parsing|Parsing error|Failed to |Couldn't |Unknown |"
                       r"Invalid |ERROR|/WARN|Exception|Ambiguity|Missing|^WARNING:")
    for number, line in enumerate(text.splitlines(), 1):
        if not issue.search(line):
            continue
        message = re.sub(r"^.*?/WARN\]:\s*", "", line).strip()
        row = {"line": number, "text": line,
               "classification": "expected_localhost_offline_notice"
               if message in EXPECTED_OFFLINE else "unexpected"}
        if "/WARN" in line or line.startswith("WARNING:"):
            warnings.append(row)
        if re.search(r"ERROR|Exception|Whilst parsing|Parsing error|Failed to |Couldn't |Unknown |Invalid |Missing", line):
            errors.append(row)
        (known if message in EXPECTED_OFFLINE else unexpected).append(row)
    return {"known_environment_warnings": known, "unexpected_issues": unexpected,
            "all_warning_lines": warnings, "error_or_parse_lines": errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="Start after complete build approval")
    args = parser.parse_args()
    result = json.loads(BUILD_RESULT.read_text(encoding="utf-8"))
    snapshot = Path(result["snapshot"]).resolve()
    if not result.get("all_passed") or snapshot.parent != WORK.resolve():
        raise ValueError("A complete successful isolated build under the Pope QA directory is required")
    original = ROOT / "_tools/server_test.py"
    if (snapshot / "_tools/server_test.py").read_bytes() != original.read_bytes():
        raise ValueError("Isolated server_test.py differs from the original")
    products = pope_product_comparison(snapshot)
    write_json(OUT / "pope_product_comparison.json", products)
    if not products["all_equal"]:
        raise ValueError("Workspace Pope products differ from the completed isolated build")
    if not args.run:
        print(json.dumps({"prepared": True, "products_equal": True,
                          "product_files": products["file_count"], "server_started": False}))
        return

    eula = EULA.read_bytes()
    if not re.search(rb"(?im)^\s*eula\s*=\s*true\s*$", eula):
        raise ValueError("The existing EULA is not accepted; this script will not change it")
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", PORT))
    run = WORK / ("server_smoke_" + str(time.time_ns()))
    if run.resolve().parent != WORK.resolve() or run.exists():
        raise ValueError("Test directory must be new and inside the Pope QA root")
    run.mkdir(parents=True)
    (run / "eula.txt").write_bytes(eula)
    (run / "server.properties").write_text("\n".join([
        "server-ip=127.0.0.1", "server-port=" + str(PORT), "online-mode=false",
        "enable-rcon=false", "enable-query=false", "enforce-secure-profile=false",
        "pause-when-empty-seconds=0", "max-tick-time=120000", "view-distance=2",
        "simulation-distance=2", "spawn-protection=0", "level-type=minecraft:flat",
        'generator-settings={"layers":[{"block":"minecraft:bedrock","height":1},{"block":"minecraft:stone","height":2}],"biome":"minecraft:plains"}',
        "generate-structures=false", "motd=Pope M4 full pack smoke test", "",
    ]), encoding="utf-8")
    destination = run / "packtest/datapacks/rpg"
    shutil.copytree(snapshot / "rpg", destination)
    source_hashes = tree_hashes(snapshot / "rpg")
    copy_hashes = tree_hashes(destination)
    if copy_hashes != source_hashes:
        raise ValueError("Full-pack test copy differs from the completed build")
    write_json(OUT / "tested_pack_hashes.json", source_hashes)
    command = [sys.executable, "-X", "utf8", str(original), str(run), "240"]
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8",
               PYTHONDONTWRITEBYTECODE="1")
    env.pop("MC_PROBE_FILE", None)
    env.pop("MC_SPRINT_WAIT", None)
    started = time.time()
    timed_out = False
    console_path = OUT / "server_test_console.log"
    with console_path.open("w", encoding="utf-8", newline="\n") as stream:
        proc = subprocess.Popen(command, cwd=ROOT, env=env, stdout=stream,
                                stderr=subprocess.STDOUT,
                                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        print(json.dumps({"started": True, "pid": proc.pid, "port": PORT,
                          "run_directory": str(run), "pack_files": len(copy_hashes)}), flush=True)
        try:
            proc.wait(timeout=540)
        except subprocess.TimeoutExpired:
            timed_out = True
            # Only the process tree created by this invocation is stopped.
            subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                           stdout=stream, stderr=subprocess.STDOUT, check=False,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            proc.wait(timeout=30)
    output = console_path.read_text(encoding="utf-8")
    latest = run / "logs/latest.log"
    latest_copy = OUT / "server_latest.log"
    if latest.is_file():
        shutil.copyfile(latest, latest_copy)
        server_log = latest.read_text(encoding="utf-8", errors="replace")
    else:
        server_log = output.split("--- full console ---", 1)[-1]
    classification = classify_console(server_log)
    tool_classification = classify_console(output)
    enabled_lines = [line for line in server_log.splitlines() if "file/rpg" in line]
    record = {
        "command": command, "run_directory": str(run), "snapshot": str(snapshot),
        "build_result_sha256": sha(BUILD_RESULT), "port": PORT,
        "exit_code": proc.returncode, "timed_out": timed_out,
        "seconds": round(time.time() - started, 2),
        "reached_done": "server reached 'Done': True" in output,
        "datapack_enabled": any("file/rpg" in line and "enabled" in line for line in enabled_lines),
        "datapack_lines": enabled_lines, "pack_files": len(copy_hashes),
        "complete_pack_copy_verified": True,
        "pope_products_equal": products["all_equal"],
        "pope_product_file_count": products["file_count"],
        "original_script_sha256": sha(original),
        "script_matches_build_snapshot": sha(original) == sha(snapshot / "_tools/server_test.py"),
        "eula_source": str(EULA), "eula_source_unchanged": EULA.read_bytes() == eula,
        "eula_sha256": hashlib.sha256(eula).hexdigest(),
        "console": str(console_path), "console_sha256": sha(console_path),
        "server_log": str(latest_copy) if latest.is_file() else None,
        "server_log_sha256": sha(latest_copy) if latest.is_file() else None,
        "in_game_visual_verified": False, "client_sync_performed": False,
        "original_tool_output_classification": tool_classification,
        **classification,
    }
    record["ok"] = (not timed_out and proc.returncode == 0 and record["reached_done"]
                    and record["datapack_enabled"] and not classification["unexpected_issues"]
                    and not tool_classification["unexpected_issues"] and latest.is_file()
                    and record["script_matches_build_snapshot"] and record["eula_source_unchanged"])
    write_json(OUT / "server_test_result.json", record)
    print(json.dumps({"ok": record["ok"], "reached_done": record["reached_done"],
                      "datapack_enabled": record["datapack_enabled"],
                      "known_warnings": len(classification["known_environment_warnings"]),
                      "unexpected_issues": len(classification["unexpected_issues"]),
                      "result": str(OUT / "server_test_result.json")}, ensure_ascii=False), flush=True)
    if not record["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
