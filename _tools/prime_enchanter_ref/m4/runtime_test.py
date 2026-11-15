"""Exercise the full Prime Enchanter M4 data pack on vanilla Java 1.21.11."""

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import socket
import sys
import traceback
import zipfile


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from pope_server_check import EXPECTED_WARNINGS, OBJ, Server, transform


MOB = "rpg:prime_enchanter"
TAG = "rpg.prime_enchanter"
FUNCTIONS = "data/rpg/function/prime_enchanter"
DISPLAY = f"type=minecraft:item_display,tag={TAG}.part"
CARRIER = f"type=minecraft:vindicator,tag={TAG}"
INVISIBLE = '{active_effects:[{id:"minecraft:invisibility"}]}'
CLIPS = {
    "idle": 20, "walk": 18, "appear": 47, "death": 114, "forward_strike": 50,
    "fury_fist": 138, "launch": 79, "lightning_slam": 88, "overcharge": 72,
    "hurt": 46, "summon": 45,
}
LOOPS = {"idle", "walk"}
HIDDEN = {"appear": range(0, 5), "launch": range(23, 44)}
SCALE = 1.15
SCALE_SAMPLES = {
    "forward_strike": {29: ("right", (1, 1.4, 2)), 30: ("right", (1, 1.5, 2)),
                       32: ("right", (1, 1, 1))},
    "lightning_slam": {53: ("left", (1, 1.5, 2)), 55: ("left", (1, 1, 1))},
}
PART_NAMES = re.compile(r'"([a-z0-9_]+)"\s*:\s*(\{translation:\[[^}]+\})')
ERROR = re.compile(r"/ERROR\]|Whilst parsing|Parsing error|Failed to (?:load|execute|parse)|Couldn't (?:load|parse)|"
                   r"Unknown (?:function|or incomplete command)|Incorrect argument|Can't find element|"
                   r"Unexpected error while executing command")
TOLERANCE = 1e-6


def digest(path, algorithm="sha256"):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, algorithm).hexdigest()


def snapshot_frames(pack, parts):
    frames = {}
    for clip, duration in CLIPS.items():
        folder = pack / f"{FUNCTIONS}/anim/{clip}"
        state = {}
        frames[clip] = []
        for tick in range(duration + (clip not in LOOPS)):
            frame = (folder / f"f{tick}.mcfunction").read_text(encoding="utf-8")
            state.update({name: transform(snbt) for name, snbt in PART_NAMES.findall(frame)})
            if state.keys() != set(parts):
                raise ValueError(f"{clip} f{tick} must cover the 12 approved parts")
            frames[clip].append(dict(state))
    return frames


def normalized(values):
    length = math.sqrt(sum(value * value for value in values))
    return [value / length for value in values]


def transform_error(actual, expected):
    errors = {}
    for field, wanted in expected.items():
        values = actual[field]
        if field.endswith("rotation"):
            wanted = normalized(wanted)
            errors[field] = min(max(abs(a - b) for a, b in zip(values, wanted, strict=True)),
                                max(abs(a + b) for a, b in zip(values, wanted, strict=True)))
        else:
            errors[field] = max(abs(a - b) for a, b in zip(values, wanted, strict=True))
    return errors


class Probes:
    def __init__(self, server, parts, frames, report):
        self.server = server
        self.parts = parts
        self.frames = frames
        self.report = report

    def record(self, name, passed, **detail):
        self.report["checks"].append(dict(name=name, passed=passed, **detail))
        if not passed:
            print(f"FAIL {name}", flush=True)

    def commands(self, *commands):
        start = len(self.server.lines)
        self.server.barrier(*commands)
        return self.server.lines[start:]

    def assert_command(self, name, clause):
        lines = self.commands(
            f"scoreboard players set #assert {OBJ} 0",
            f"execute {clause} run scoreboard players set #assert {OBJ} 1",
            f"scoreboard players get #assert {OBJ}",
        )
        matches = [line for line in lines if "#assert has " in line]
        self.record(name, len(matches) == 1 and f"has 1 [{OBJ}]" in matches[0], clause=clause, output=matches)

    def count(self, name, clause, wanted):
        lines = self.commands(
            f"scoreboard players set #count {OBJ} 0",
            f"execute {clause} run scoreboard players add #count {OBJ} 1",
            f"scoreboard players get #count {OBJ}",
        )
        values = [int(match[1]) for line in lines if (match := re.search(r"#count has (\d+)", line))]
        self.record(name, values == [wanted], expected=wanted, actual=values, clause=clause)

    def spawn(self, dimension):
        prefix = f"execute in {dimension} positioned 8.5 90 8.5"
        select = f"@e[{CARRIER},distance=0..,limit=1]"
        self.commands(f"{prefix} run function {MOB}/summon",
                      f"execute in {dimension} run data merge entity {select} {{NoAI:1b,NoGravity:1b}}")
        self.count(f"{dimension}: one vindicator carrier", f"in {dimension} as @e[{CARRIER},distance=0..]", 1)
        self.count(f"{dimension}: 12 item display entities", f"in {dimension} as @e[{DISPLAY},distance=0..]", 12)
        self.count(f"{dimension}: exactly 12 direct passengers", f"in {dimension} as {select} on passengers", 12)
        for part in self.parts:
            self.count(f"{dimension}: direct display passenger {part}",
                       f"in {dimension} as {select} on passengers if entity @s[{DISPLAY},tag={TAG}.p.{part}]", 1)
        self.assert_command(f"{dimension}: current health = 1000",
                            f"in {dimension} as {select} if entity @s[nbt={{Health:1000f}}]")
        self.assert_command(f"{dimension}: invisible on spawn",
                            f"in {dimension} as {select} if entity @s[nbt={INVISIBLE}]")
        lines = self.commands(f"execute in {dimension} run attribute {select} minecraft:max_health base get")
        self.record(f"{dimension}: maximum health = 1000", any(re.search(r"\bis 1000(?:\.0)?\b", line) for line in lines),
                    output=lines)
        return f"in {dimension} as {select}"

    def enter(self, carrier, clip):
        self.commands(f"execute {carrier} at @s run function {MOB}/anim/enter/{clip}")

    def clock(self, carrier, clip, tick, suffix=""):
        self.assert_command(f"{carrier.split()[1]}: {clip} f{tick} clock{suffix}",
                            f"{carrier} if score @s rpg_pe_anim matches {list(CLIPS).index(clip)} "
                            f"if score @s rpg_pe_t matches {tick + 1}")

    def sample(self, carrier, clip, tick, *, visible=True, suffix=""):
        lines = self.commands(*[
            f"execute {carrier} on passengers if entity @s[{DISPLAY},tag={TAG}.p.{part}] run data get entity @s"
            for part in self.parts
        ])
        raw = [line.split("has the following entity data:", 1)[1] for line in lines
               if "has the following entity data:" in line]
        label = f"{carrier.split()[1]}: {clip} f{tick}{suffix}"
        if len(raw) != len(self.parts):
            self.record(f"{label} passenger data", False, expected=len(self.parts), actual=len(raw))
            return
        actual = {}
        errors = {}
        rendered = {}
        for part, text in zip(self.parts, raw, strict=True):
            actual[part] = transform(text)
            errors[part] = transform_error(actual[part], self.frames[clip][tick][part])
            correct_model = re.search(r'"minecraft:item_model":\s*"' + re.escape(f"{MOB}/{part}") + '"', text)
            item_present = (re.search(r'\bitem:\s*\{(?!\s*\})', text)
                            and not re.search(r'\bid:\s*"minecraft:air"', text))
            hidden_tag = f'"{TAG}.hidden"' in text
            rendered[part] = bool(correct_model and item_present and not hidden_tag) if visible else bool(
                not item_present and hidden_tag)
        maximum = max(error for fields in errors.values() for error in fields.values())
        self.record(f"{label} target transforms", maximum <= TOLERANCE, max_error=maximum,
                    expected=self.frames[clip][tick], actual=actual, field_errors=errors)
        self.record(f"{label} {'visible items' if visible else 'empty items'}", all(rendered.values()), parts=rendered)
        if tick in SCALE_SAMPLES.get(clip, {}):
            side, wanted = SCALE_SAMPLES[clip][tick]
            stretched = {side + "_arm", side + "_hand"}
            self.assert_scale(label, actual, {part: wanted if part in stretched else (1, 1, 1) for part in self.parts})
        elif clip == "idle" and tick == 0 and not suffix:
            self.assert_scale(label, actual, {part: (1, 1, 1) for part in self.parts})

    def assert_scale(self, label, actual, wanted):
        ratios = {part: sorted(abs(value) / SCALE for value in data["scale"]) for part, data in actual.items()}
        passed = all(abs(a - b) <= TOLERANCE for part in self.parts
                     for a, b in zip(ratios[part], wanted[part], strict=True))
        self.record(f"{label} scale relative to {SCALE}", passed, expected=wanted, actual=ratios)

    def walk_step(self, carrier, ticks):
        # The production stride detector samples every four ticks. Move once
        # per step of at most four ticks while it tracks a normal walk loop.
        while ticks:
            step = min(4, ticks)
            self.commands(f"execute {carrier} at @s run tp @s ~0.25 ~ ~")
            self.server.step(step)
            ticks -= step

    def play(self, carrier, clip, duration):
        last = duration - (clip in LOOPS)
        targets = {0, duration // 2, last, *SCALE_SAMPLES.get(clip, ())}
        hidden = HIDDEN.get(clip, ())
        if hidden:
            targets.update(tick for tick in (hidden[0] - 1, hidden[0], hidden[-1], hidden[-1] + 1) if tick >= 0)
        self.enter(carrier, clip)
        if clip == "walk":
            self.commands(f"execute {carrier} run scoreboard players set @s rpg_pe_mc 0",
                          f"execute {carrier} run scoreboard players set @s rpg_pe_mv 1")
        previous = 0
        for tick in sorted(targets | set(hidden)):
            if tick > previous:
                if clip == "walk":
                    self.walk_step(carrier, tick - previous)
                else:
                    self.server.step(tick - previous)
            if tick in targets:
                self.clock(carrier, clip, tick)
                self.sample(carrier, clip, tick, visible=tick not in hidden)
            else:
                self.count(f"{clip} f{tick}: all passenger items empty",
                           f"{carrier} on passengers if entity @s[{DISPLAY},tag={TAG}.hidden] unless data entity @s item.id",
                           len(self.parts))
            previous = tick
        if clip == "death":
            self.server.step(6)
            self.clock(carrier, clip, last, " after six more ticks")
            self.sample(carrier, clip, last, suffix=" after six more ticks")
        else:
            if clip == "walk":
                self.walk_step(carrier, 1)
            else:
                self.server.step(1)
            next_clip = clip if clip in LOOPS else "idle"
            self.clock(carrier, next_clip, 0, f" after {clip}")
            self.sample(carrier, next_clip, 0, suffix=f" after {clip}")
        print(f"Verified clip {clip}", flush=True)

    def run(self):
        for dimension in ("minecraft:overworld", "minecraft:the_nether"):
            self.commands(f"execute in {dimension} run forceload add 0 0")
        self.server.step(3)
        overworld = self.spawn("minecraft:overworld")
        self.server.step(1)
        self.clock(overworld, "idle", 0, " at initialization")
        self.commands(f"execute {overworld} run effect clear @s minecraft:invisibility")
        self.assert_command("fixture cleared invisibility", f"{overworld} unless entity @s[nbt={INVISIBLE}]")
        self.server.step(1)
        self.assert_command("next tick restores invisibility", f"{overworld} if entity @s[nbt={INVISIBLE}]")
        for clip, duration in CLIPS.items():
            self.play(overworld, clip, duration)
        self.enter(overworld, "appear")
        self.sample(overworld, "appear", 0, visible=False, suffix=" before interrupted entry")
        self.enter(overworld, "hurt")
        self.sample(overworld, "hurt", 0, suffix=" after interrupting hidden appear")
        nether = self.spawn("minecraft:the_nether")
        self.enter(overworld, "forward_strike")
        self.enter(nether, "summon")
        self.server.step(5)
        for carrier, clip in ((overworld, "forward_strike"), (nether, "summon")):
            self.clock(carrier, clip, 5, " with two dimensions active")
            self.sample(carrier, clip, 5, suffix=" with two dimensions active")
        for dimension, carrier in (("minecraft:overworld", overworld), ("minecraft:the_nether", nether)):
            self.commands(f"execute {carrier} run kill @s")
            self.server.step(23)
            self.count(f"{dimension}: no carrier after kill", f"in {dimension} as @e[{CARRIER},distance=0..]", 0)
            self.count(f"{dimension}: no item display after carrier kill", f"in {dimension} as @e[{DISPLAY},distance=0..]", 0)
            if carrier == overworld:
                self.count("Nether carrier retains its 12 passengers after Overworld kill",
                           f"{nether} on passengers if entity @s[{DISPLAY}]", 12)


def run(args):
    source = args.datapack.resolve()
    directory = args.run_directory.resolve()
    report_directory = args.output.resolve() if args.output else directory
    server_jar = args.server_jar.resolve()
    eula = args.eula_source.read_bytes()
    if not re.search(rb"(?im)^\s*eula\s*=\s*true\s*$", eula):
        raise ValueError("Provide an existing accepted eula.txt")
    server_sha1 = digest(server_jar, "sha1")
    if server_sha1 != "64bb6d763bed0a9f1d632ec347938594144943ed":
        raise ValueError("Server jar SHA-1 differs from Mojang's vanilla 1.21.11 release")
    if any(path == source or source in path.parents for path in (directory, report_directory)):
        raise ValueError("Run and report directories must be outside the input pack")
    parts = [part for part, _ in json.loads((HERE.parent / "m2/model_spec.json").read_bytes())["parts"]]
    if len(parts) != 12 or len(set(parts)) != 12:
        raise ValueError("Expected 12 distinct display parts in the approved M2 rig")

    pack = zipfile.Path(source) if source.is_file() else source
    if not (pack / "pack.mcmeta").is_file() or not (pack / f"{FUNCTIONS}/summon.mcfunction").is_file():
        raise ValueError("Input must be the full built data pack with pack.mcmeta at its root")
    frames = snapshot_frames(pack, parts)
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", args.port))
        port = sock.getsockname()[1]
    directory.mkdir(parents=True, exist_ok=False)
    target = directory / "packtest/datapacks" / ("tralancer-rpg.zip" if source.is_file() else "tralancer-rpg")
    target.parent.mkdir(parents=True)
    if source.is_file():
        shutil.copyfile(source, target)
    else:
        shutil.copytree(source, target)
    (directory / "eula.txt").write_bytes(eula)
    (directory / "server.properties").write_text("\n".join([
        "server-ip=127.0.0.1", f"server-port={port}", "online-mode=false", "enforce-secure-profile=false",
        "enable-rcon=false", "enable-query=false", "enable-status=false", "white-list=true",
        "pause-when-empty-seconds=0", "view-distance=2", "simulation-distance=2", "spawn-protection=0",
        "level-type=minecraft:flat", "level-seed=0", "generate-structures=false", "max-tick-time=120000",
        'generator-settings={"layers":[{"block":"minecraft:bedrock","height":1},{"block":"minecraft:stone","height":2}],"biome":"minecraft:plains"}',
        "",
    ]), encoding="utf-8")
    report = {
        "datapack": str(source), "datapack_zip_sha256": digest(source) if source.is_file() else None,
        "summon_sha256": hashlib.sha256((pack / f"{FUNCTIONS}/summon.mcfunction").read_bytes()).hexdigest(),
        "run_directory": str(directory), "server_jar": str(server_jar), "server_jar_sha1": server_sha1,
        "port": port, "checks": [], "clip_order": list(CLIPS), "tests_complete": False,
        "scope": "Unmodified full data pack, isolated fresh world, no client. Target entity NBT and loaded chunks only.",
        "test_controls": {"NoAI": True, "NoGravity": True, "tick_mode": "frozen, step at 20 TPS"},
    }
    server = None
    try:
        server = Server([args.java, "-Xmx2G", "-Dfile.encoding=UTF-8", "-jar", str(server_jar), "nogui",
                         "--world", "packtest"], directory)
        server.wait("Done (", timeout=240)
        probes = Probes(server, parts, frames, report)
        probes.record("vanilla Java server started in version 1.21.11",
                      any("Starting minecraft server version 1.21.11" in line for line in server.lines))
        pack_list = probes.commands("tick freeze", "tick rate 20", f"scoreboard objectives add {OBJ} dummy",
                                    "datapack list enabled")
        probes.record("built data pack enabled", any(f"file/{target.name}" in line for line in pack_list), output=pack_list)
        probes.run()
        report["tests_complete"] = True
    except Exception as exc:
        report["failure"] = {"type": type(exc).__name__, "message": str(exc), "traceback": traceback.format_exc()}
    finally:
        if server:
            report["server_exit_code"] = server.stop()
            report["function_or_command_errors"] = [line for line in server.lines if ERROR.search(line)]
            warnings = [line for line in server.lines if "/WARN]" in line]
            report["environment_warnings"] = [line for line in warnings if line.split("]: ", 1)[-1] in EXPECTED_WARNINGS]
            report["other_warnings"] = [line for line in warnings if line not in report["environment_warnings"]]
        report["passed"] = sum(check["passed"] for check in report["checks"])
        report["failed"] = [check["name"] for check in report["checks"] if not check["passed"]]
        report["success"] = (report["tests_complete"] and report.get("server_exit_code") == 0 and not report["failed"]
                             and not report.get("function_or_command_errors"))
        report_path = directory / "report.json"
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if report_directory != directory:
            report_directory.mkdir(parents=True, exist_ok=True)
            for evidence in (report_path, directory / "console.log"):
                if evidence.is_file():
                    shutil.copyfile(evidence, report_directory / evidence.name)
        print(json.dumps({key: report.get(key) for key in ("success", "passed", "failed", "failure", "server_exit_code",
                                                         "function_or_command_errors", "other_warnings")}), flush=True)
    return report["success"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--datapack", type=Path, required=True, help="Built data pack ZIP or directory")
    parser.add_argument("--run-directory", type=Path, required=True, help="New directory for the isolated world")
    parser.add_argument("--server-jar", type=Path, required=True, help="Mojang's vanilla Java 1.21.11 server.jar")
    parser.add_argument("--eula-source", type=Path, required=True, help="Path to an existing accepted eula.txt")
    parser.add_argument("--java", default="java")
    parser.add_argument("--port", type=int, default=0, help="Loopback port, automatic by default")
    parser.add_argument("--output", type=Path, help="Optional directory for a copy of the report and console log")
    sys.exit(0 if run(parser.parse_args()) else 1)


if __name__ == "__main__":
    main()
