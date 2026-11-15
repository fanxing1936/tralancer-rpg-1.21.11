"""教皇 M4：在新的本机专用服务端世界实测模型接口，不写玩家实例。

输入必须是已构建的数据包目录；脚本不构建、不修改源包、不接受 EULA。
只复制一份已有 eula=true 文件，并只监听 127.0.0.1。Minecraft 客户端
未启动，因此结果不证明视觉还原度、客户端插值或音效听感。
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import shutil
import socket
import subprocess
import sys
import threading
import time
import traceback

from mc_env import JAVA, JAR, VJSON

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "pope_ref/m4/runtime"
OBJ = "pp_m4_test"
TAG = "rpg.pope"
PARTS = ["body", "head", "crown", "right_arm", "right_hand", "left_arm",
         "left_hand", "right_leg", "left_leg", "cape", "staff", "staff_glow"]
CLIPS = ["idle", "walk", "attack", "summon", "cast", "appear", "teleport_in",
         "teleport_out", "whirlwind"]
EXPECTED_WARNINGS = {
    "**** SERVER IS RUNNING IN OFFLINE/INSECURE MODE!",
    "The server will make no attempt to authenticate usernames. Beware.",
    "While this makes the game possible to play without internet access, it also opens up the ability for hackers to connect with any username they choose.",
    'To change this, set "online-mode" to "true" in the server.properties file.',
}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", "utf8")


def transform(text):
    result = {}
    for field in ["translation", "left_rotation", "scale", "right_rotation"]:
        match = re.search(r"\b" + field + r":\s*\[([^\]]+)\]", text)
        if not match:
            raise ValueError("实体缺少变换字段：" + field)
        result[field] = [float(x.strip().rstrip("fFdD")) for x in match.group(1).split(",")]
    return result


def classify_outcome(report, console):
    """Keep functional assertions separate from the stricter all-WARN gate.

    No warning is discarded. Only an exact, numeric Can't-keep-up message
    before the first model summon command is annotated as setup performance.
    This annotation does not make strict_success true.
    """
    lines = console.splitlines()
    first_summon = next((number for number, line in enumerate(lines, 1)
                        if line.startswith(">>> ") and line.endswith(" run function rpg:pope/summon")), None)
    performance = re.compile(r"^\[\d\d:\d\d:\d\d\] \[Server thread/WARN\]: Can't keep up! Is the server overloaded\? Running (\d+)ms or (\d+) ticks behind$")
    reports = []
    initial_count = next((row for row in report["checks"] if row["name"] == "召唤 1 个卫道士载体"), None)
    for number, line in enumerate(lines, 1):
        match = performance.fullmatch(line)
        if match and first_summon and number < first_summon:
            reports.append({"message": line, "console_line": number,
                "first_model_summon_command_line": first_summon,
                "milliseconds_behind": int(match.group(1)), "ticks_behind": int(match.group(2)),
                "phase": "首次 forceload 下界/末地区块；教皇模型召唤命令尚未执行",
                "no_carrier_evidence": {
                    "fresh_world_created_by_this_run": True,
                    "no_pope_summon_command_precedes_warning": True,
                    "first_spawn_total_carrier_count_is_one": bool(initial_count and initial_count["passed"]),
                    "limits": "未在 WARN 当刻直接查询零实体；证据为全新世界、首个模型召唤命令时序与其后的总数=1断言。"}})
    report["setup_performance_warnings"] = reports
    report["functional_success"] = bool(not report.get("failure") and report.get("tests_complete")
        and report.get("checks") and not report["failed"] and not report.get("function_or_command_errors")
        and report.get("server_exit_code") == 0)
    report["strict_success"] = report["functional_success"] and not report.get("unexpected_warnings")
    # Preserve the original meaning of success for existing report consumers.
    report["success"] = report["strict_success"]
    report["outcome_policy"] = "functional_success用于功能测试退出码；success/strict_success额外要求没有未豁免WARN。全部WARN原文保留。"


class Server:
    def __init__(self, command, run):
        self.lines, self.sequence = [], 0
        self.condition = threading.Condition()
        self.log = (run / "console.log").open("w", encoding="utf8", buffering=1)
        self.proc = subprocess.Popen(command, cwd=run, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
            encoding="utf8", errors="replace", bufsize=1,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))

        def pump():
            for line in self.proc.stdout:
                with self.condition:
                    self.lines.append(line.rstrip())
                    self.log.write(line)
                    self.condition.notify_all()

        self.reader = threading.Thread(target=pump, daemon=True)
        self.reader.start()

    def send(self, *commands):
        for command in commands:
            self.log.write(">>> " + command + "\n")
            self.proc.stdin.write(command + "\n")
        self.proc.stdin.flush()

    def wait(self, needle, start=0, timeout=30):
        deadline = time.monotonic() + timeout
        with self.condition:
            while time.monotonic() < deadline:
                found = next((line for line in self.lines[start:] if needle in line), None)
                if found:
                    return found
                if self.proc.poll() is not None:
                    raise RuntimeError("服务端提前退出：" + str(self.proc.returncode))
                self.condition.wait(min(.2, max(0, deadline - time.monotonic())))
        raise TimeoutError("等待服务端输出超时：" + needle)

    def barrier(self, *commands):
        self.sequence += 1
        token = f"POPE_M4_BARRIER_{self.sequence:04d}"
        start = len(self.lines)
        self.send(*commands, "say " + token)
        self.wait(token, start)

    def step(self, count):
        self.barrier(
            f"execute store result score #before {OBJ} run time query gametime",
            f"scoreboard players operation #target {OBJ} = #before {OBJ}",
            f"scoreboard players add #target {OBJ} {count}", f"tick step {count}")
        self.sequence += 1
        token = f"POPE_M4_STEP_{self.sequence:04d}"
        start = len(self.lines)
        deadline = time.monotonic() + max(20, count / 10)
        while time.monotonic() < deadline:
            self.send(f"execute store result score #now {OBJ} run time query gametime",
                f"execute if score #now {OBJ} >= #target {OBJ} run say {token}")
            try:
                self.wait(token, start, .4)
                return
            except TimeoutError:
                pass
        raise TimeoutError(f"无法推进 {count} 个服务器刻")

    def stop(self):
        if self.proc.poll() is None:
            try:
                self.send("stop")
                self.proc.wait(timeout=45)
            except (OSError, subprocess.TimeoutExpired):
                self.proc.kill()
                self.proc.wait(timeout=10)
        self.reader.join(5)
        self.log.close()
        return self.proc.returncode


class Tests:
    def __init__(self, server, pack, clips, report):
        self.server, self.pack, self.clips, self.report = server, pack, clips, report

    def check(self, condition, label, dimension="overworld"):
        self.server.sequence += 1
        token = f"POPE_M4_ASSERT_{self.server.sequence:04d}"
        start = len(self.server.lines)
        self.server.send(f"scoreboard players set #assert {OBJ} 0",
            f"execute in minecraft:{dimension} {condition} run scoreboard players set #assert {OBJ} 1",
            f"execute if score #assert {OBJ} matches 1 run say {token}_PASS",
            f"execute if score #assert {OBJ} matches 0 run say {token}_FAIL")
        line = self.server.wait(token, start)
        passed = token + "_PASS" in line
        self.report["checks"].append({"name": label, "passed": passed,
            "condition": condition, "dimension": dimension, "console": line})
        if not passed:
            print("FAIL " + label, flush=True)
        return passed

    def score(self, target, objective, value, label, dimension="overworld"):
        return self.check(f"if score {target} {objective} matches {value}", label, dimension)

    def count(self, selector, expected, label, dimension="overworld"):
        self.server.barrier(f"scoreboard players set #count {OBJ} 0",
            f"execute in minecraft:{dimension} as {selector} run scoreboard players add #count {OBJ} 1")
        return self.score("#count", OBJ, expected, label, dimension)

    def spawn(self, label, position="8.5 80 8.5", dimension="overworld"):
        prefix = f"execute in minecraft:{dimension} positioned {position}"
        self.server.barrier(prefix + " run function rpg:pope/summon",
            prefix + f" run tag @e[type=vindicator,tag={TAG},distance=..1,sort=nearest,limit=1] add {label}")
        sel = f"@e[type=vindicator,tag={label},distance=0..,limit=1]"
        # Test-only fixture freezes physical movement without changing the model
        # generator's carrier contract or adding any gameplay tags.
        self.server.barrier(f"execute in minecraft:{dimension} run data merge entity {sel} {{NoAI:1b,NoGravity:1b}}")
        return sel

    def enter(self, selector, clip, dimension="overworld"):
        self.server.barrier(f"execute in minecraft:{dimension} as {selector} at @s run function rpg:pope/anim/enter/{clip}")

    def frame(self, clip, tick, carrier, dimension="overworld"):
        expected = {}
        folder = self.pack / f"data/rpg/function/pope/anim/{clip}"
        frames = sorted((int(p.stem[1:]), p) for p in folder.glob("f*.mcfunction")
                        if re.fullmatch(r"f\d+", p.stem))
        for frame_tick, path in frames:
            if frame_tick > tick:
                break
            for line in path.read_text("utf8").splitlines():
                match = re.search(r"tag=rpg\.pope\.p\.([a-z0-9_]+)", line)
                if match and "transformation:" in line:
                    expected[match.group(1)] = transform(line.split("transformation:", 1)[1])
        if set(expected) != set(PARTS):
            raise ValueError("累计帧没有覆盖全部 12 部件")
        start = len(self.server.lines)
        self.server.barrier(*[
            f"execute in minecraft:{dimension} as {carrier} on passengers if entity @s[tag={TAG}.p.{part}] run data get entity @s transformation"
            for part in PARTS])
        outputs = [line for line in self.server.lines[start:] if "has the following entity data:" in line]
        if len(outputs) != len(PARTS):
            raise ValueError(f"实体变换返回数量错误：{len(outputs)}/12")
        samples = []
        for part, line in zip(PARTS, outputs):
            actual, target = transform(line), expected[part]
            errors = {}
            for field, wanted in target.items():
                if field.endswith("rotation"):
                    length = math.sqrt(sum(v * v for v in wanted))
                    wanted = [v / length for v in wanted]
                    errors[field] = min(max(abs(a-b) for a,b in zip(actual[field], wanted)),
                                        max(abs(a+b) for a,b in zip(actual[field], wanted)))
                else:
                    errors[field] = max(abs(a-b) for a,b in zip(actual[field], wanted))
            samples.append({"part": part, "target": target, "actual": actual, "errors": errors})
        error = max(value for sample in samples for value in sample["errors"].values())
        self.report["checks"].append({"name": f"{clip} f{tick}: 12 部件实际目标变换",
            "passed": error <= 1e-6, "maximum_error": error, "tolerance": 1e-6,
            "samples": samples, "dimension": dimension})

    def main(self):
        s = self.server
        for dim in ["overworld", "the_nether", "the_end"]:
            s.barrier(f"execute in minecraft:{dim} run forceload add 0 0 31 15")
        s.step(3)
        a = self.spawn("pope_m4_A")
        self.count(f"@e[type=vindicator,tag={TAG},distance=0..]", 1, "召唤 1 个卫道士载体")
        self.count(f"@e[type=item_display,tag={TAG}.part,distance=0..]", 12, "召唤 12 个部件")
        self.check(f"if entity {a[:-1]},nbt={{Health:1000f}}]", "载体初始血量 1000")
        s.barrier(f"execute store result score #health {OBJ} run attribute {a} minecraft:max_health base get",
                  f"execute store result score #passengers {OBJ} run data get entity {a} Passengers")
        self.score("#health", OBJ, 1000, "max_health=1000")
        self.score("#passengers", OBJ, 12, "12 部件真实骑乘载体")
        self.check(f"as {a} if predicate rpg:pope/invisible", "召唤后载体隐身")
        self.check(f"if entity {a[:-1]},nbt={{Silent:1b,PersistenceRequired:1b,CanPickUpLoot:0b}}]", "静音/持久/不捡物契约")
        self.check(f"unless entity {a[:-1]},tag=rpg.pf.boss]", "模型召唤不接入教皇玩法标签")
        for part in PARTS:
            self.count(f"@e[type=item_display,tag={TAG}.p.{part},distance=0..]", 1, "独立部件 " + part)
        s.step(2)
        self.score(a, "rpg_pp_anim", 0, "首次 tick 初始化 idle")
        # Guard against low-level passenger seating regressions: plain vindicator
        # measured seat is +2 blocks, separate from local animation transforms.
        s.barrier(f"execute store result score #carrier_y {OBJ} run data get entity {a} Pos[1] 100000",
            f"scoreboard players set #bad {OBJ} 0",
            f"execute as {a} on passengers store result score @s {OBJ} run data get entity @s Pos[1] 100000",
            f"execute as {a} on passengers run scoreboard players operation @s {OBJ} -= #carrier_y {OBJ}",
            f"execute as {a} on passengers unless score @s {OBJ} matches 200000 run scoreboard players add #bad {OBJ} 1")
        self.score("#bad", OBJ, 0, "12 部件载体座位高度 +2 格")
        s.barrier(f"effect clear {a} minecraft:invisibility")
        self.check(f"as {a} unless predicate rpg:pope/invisible", "测试确实清除隐身")
        s.step(1)
        self.check(f"as {a} if predicate rpg:pope/invisible", "tick_late 恢复载体隐身")
        for index, info in enumerate(self.clips):
            clip, ticks = info["name"], round(info["length"] * 20)
            self.enter(a, clip)
            self.score(a, "rpg_pp_anim", index, clip + " 片段编号")
            self.score(a, "rpg_pp_t", 1, clip + " 立即播首帧后 t=1")
            self.frame(clip, 0, a)
            # For walk, drive actual horizontal movement in four-tick strides
            # so the shared runtime's movement detector keeps the clip active.
            targets = sorted(set([ticks // 2, ticks - 1 if info["loop"] else ticks]))
            elapsed = 0
            if clip == "walk":
                s.barrier(f"scoreboard players set {a} rpg_pp_mc 0",
                          f"scoreboard players set {a} rpg_pp_mv 1")
            for target in targets:
                while elapsed < target:
                    advance = min(4 if clip == "walk" else target-elapsed, target-elapsed)
                    if clip == "walk":
                        s.barrier(f"execute as {a} at @s run tp @s ~0.25 ~ ~")
                    s.step(advance)
                    elapsed += advance
                self.score(a, "rpg_pp_anim", index, clip + f" 在第 {target} 刻仍保持片段")
                self.score(a, "rpg_pp_t", target + 1, clip + f" 第 {target} 刻计数")
                self.frame(clip, target, a)
            if info["loop"]:
                if clip == "walk":
                    s.barrier(f"execute as {a} at @s run tp @s ~0.25 ~ ~")
                s.step(1)
                self.score(a, "rpg_pp_t", 1, clip + " 周期结束回到首帧")
                self.score(a, "rpg_pp_anim", index, clip + " 周期保持编号")
                self.frame(clip, 0, a)
            else:
                s.step(1)
                self.score(a, "rpg_pp_anim", 0, clip + " 播完返回 idle")
                self.score(a, "rpg_pp_t", 1, clip + " 返回 idle 首帧")
                self.frame("idle", 0, a)
            print("已实测教皇 " + clip, flush=True)
        # Four isolated instances cover same-dimension and cross-dimension
        # ownership without adding owner IDs or changing the shared runtime.
        b = self.spawn("pope_m4_B", "24.5 80 8.5")
        c = self.spawn("pope_m4_C", dimension="the_nether")
        d = self.spawn("pope_m4_D", dimension="the_end")
        instances = [(a,"overworld","attack"), (b,"overworld","cast"),
                     (c,"the_nether","summon"), (d,"the_end","whirlwind")]
        for sel, dim, clip in instances:
            self.enter(sel, clip, dim)
        s.step(5)
        for sel, dim, clip in instances:
            self.score(sel, "rpg_pp_anim", CLIPS.index(clip), "四实例独立 " + dim + "/" + clip, dim)
            self.score(sel, "rpg_pp_t", 6, "每刻仅推进一次 " + dim + "/" + clip, dim)
            self.frame(clip, 5, sel, dim)
        s.barrier("kill " + a)
        s.step(23)
        self.count(f"@e[type=item_display,tag={TAG}.part,distance=0..]", 12, "只移除 A 载体后仅 B 的 12 部件保留")
        self.count(f"@e[type=item_display,tag={TAG}.part,predicate=!rpg:pope/riding,distance=0..]", 0, "A 移除后 0 孤儿")
        for sel, dim, clip in instances[1:]:
            self.count(f"@e[type=item_display,tag={TAG}.part,distance=0..]", 12, "删除 A 不影响 " + dim + "/" + clip, dim)
            s.barrier(f"execute in minecraft:{dim} run kill {sel}")
            s.step(23)
            self.count(f"@e[type=item_display,tag={TAG}.part,distance=0..]", 0, dim + " 仅删除载体后 0 残留", dim)
            self.count(f"@e[type=vindicator,tag={TAG},distance=0..]", 0, dim + " 载体清空", dim)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--datapack", type=Path, required=True)
    parser.add_argument("--run-directory", type=Path, required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--eula-source", type=Path, default=Path(r"D:\minecraft\本地部署\eula.txt"))
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    source, run, output = args.datapack.resolve(), args.run_directory.resolve(), args.output.resolve()
    if not (source / "data/rpg/function/pope/summon.mcfunction").is_file():
        raise ValueError("输入目录没有已生成的教皇模型数据包")
    if run.exists() or run == source or source in run.parents:
        raise ValueError("测试目录必须全新，且不得位于输入包内")
    eula = args.eula_source.read_bytes()
    if not re.search(rb"(?im)^\s*eula\s*=\s*true\s*$", eula):
        raise ValueError("没有可复用的已接受 EULA；脚本不会代为接受")
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", args.port))
    clips = json.loads((HERE / "pope_ref/m3/clipmeta.json").read_text("utf8"))["clips"]
    if [c["name"] for c in clips] != CLIPS:
        raise ValueError("M3 clip 顺序被改变")
    run.mkdir(parents=True)
    output.mkdir(parents=True, exist_ok=True)
    (run / "eula.txt").write_bytes(eula)
    (run / "server.properties").write_text("\n".join([
        "server-ip=127.0.0.1", f"server-port={args.port}", "online-mode=false",
        "enable-rcon=false", "enable-query=false", "enable-status=false",
        "enforce-secure-profile=false", "pause-when-empty-seconds=0",
        "max-tick-time=120000", "view-distance=2", "simulation-distance=2",
        "spawn-protection=0", "level-type=minecraft:flat", "generate-structures=false",
        'generator-settings={"layers":[{"block":"minecraft:bedrock","height":1},{"block":"minecraft:stone","height":2}],"biome":"minecraft:plains"}',
        "motd=Pope model isolated M4 runtime verification", ""]), "utf8")
    pack = run / "packtest/datapacks/tralancer-rpg"
    shutil.copytree(source, pack)
    # Full-pack parsing is retained, but gameplay must not own the same clip
    # clock during this model-only lifecycle test. The pristine full-pack smoke
    # test is performed separately with server_test.py. Only this disposable
    # world's tick tag is edited; source/build files are unchanged.
    tick_path = pack / "data/minecraft/tags/function/tick.json"
    tick_before = tick_path.read_bytes()
    tick_doc = json.loads(tick_before)
    removed = [value for value in tick_doc["values"]
               if (value.get("id") if isinstance(value, dict) else value) == "rpg:pope_fight/tick"]
    tick_doc["values"] = [value for value in tick_doc["values"] if value not in removed]
    write_json(tick_path, tick_doc)
    argv = sys.argv
    try:
        sys.argv = ["server_test.py", str(run)]
        spec = importlib.util.spec_from_file_location("pope_server_classpath", HERE / "server_test.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.argv = argv
    libraries = module.classpath(json.loads(Path(VJSON).read_text("utf8")))
    command = [JAVA, "-Xmx2G", "-Dfile.encoding=UTF-8", "-cp", os.pathsep.join(libraries),
        "net.minecraft.server.Main", "--nogui", "--universe", str(run), "--world", "packtest"]
    report = {"scope": "教皇模型 M4：完整数据包、全新世界、真实 1.21.11 专用服务端",
        "datapack_source": str(source), "run_directory": str(run), "bind": "127.0.0.1",
        "port": args.port, "java": JAVA, "client_jar": JAR, "model_sha256": sha(HERE / "pope_ref/pope.bbmodel"),
        "eula_source": str(args.eula_source), "eula_source_sha256": sha(args.eula_source),
        "source_summon_sha256": sha(source / "data/rpg/function/pope/summon.mcfunction"),
        "server_test_sha256": sha(HERE / "server_test.py"), "checks": [],
        "test_controls": {
            "removed_tick_entries_in_disposable_copy_only": removed,
            "source_tick_tag_sha256": hashlib.sha256(tick_before).hexdigest(),
            "test_tick_tag_sha256": sha(tick_path),
            "test_only_entity_fields": {"NoAI": True, "NoGravity": True},
            "tick_mode": "frozen, explicit tick step at normal 20 TPS",
            "walk_control": "test movement 0.25 blocks every four ticks; initial stride phase and movement flag reset",
            "gameplay_scope": "不是完整教皇战测试；全部玩法函数仍加载，只停用复制包中 pope_fight/tick 的注册"}}
    write_json(run / "launch.json", {"command": command, "evidence": report})
    server = None
    try:
        server = Server(command, run)
        server.wait("Done (", timeout=240)
        report["startup_done"] = True
        server.barrier("tick freeze", "tick rate 20", f"scoreboard objectives add {OBJ} dummy", "datapack list enabled")
        Tests(server, pack, clips, report).main()
        report["tests_complete"] = True
    except Exception as exc:
        report["failure"] = {"type": type(exc).__name__, "message": str(exc), "traceback": traceback.format_exc()}
    finally:
        if server:
            report["server_exit_code"] = server.stop()
            report["server_process_exited"] = server.proc.poll() is not None
            shutil.copyfile(run / "console.log", output / "console.log")
            pattern = re.compile(r"Whilst parsing|Parsing error|Failed to |Couldn't |Unknown |Invalid |ERROR|Exception|Missing|Unknown or incomplete command|Incorrect argument")
            report["function_or_command_errors"] = [line for line in server.lines if pattern.search(line)]
            warnings = [line for line in server.lines if "/WARN]" in line]
            report["known_environment_warnings"] = [line for line in warnings if line.split("]: ",1)[-1] in EXPECTED_WARNINGS]
            report["unexpected_warnings"] = [line for line in warnings if line not in report["known_environment_warnings"]]
        report["eula_source_unchanged"] = sha(args.eula_source) == report["eula_source_sha256"]
        report["passed"] = sum(row["passed"] for row in report["checks"])
        report["failed"] = [row for row in report["checks"] if not row["passed"]]
        classify_outcome(report, (run / "console.log").read_text("utf8") if server else "")
        report["limits"] = ["未在真实游戏内看过；没有客户端视觉、半透明排序、实际音效听感验证",
            "变换比较对象为实体保存的目标 NBT，不等于客户端插值姿势",
            "孤儿清理只证明本次已加载区块；没有声称清理所有卸载区块实体",
            "NoAI/NoGravity 仅测试夹具设置，生成器不因此拥有战斗 AI"]
        write_json(run / "report.json", report)
        write_json(output / "report.json", report)
        brief = {key: report.get(key) for key in ["success", "functional_success", "strict_success", "passed", "failure",
            "function_or_command_errors", "unexpected_warnings", "server_exit_code"]}
        brief["failed_checks"] = [row["name"] for row in report["failed"]]
        print(json.dumps(brief, ensure_ascii=False), flush=True)
    if not report["functional_success"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
