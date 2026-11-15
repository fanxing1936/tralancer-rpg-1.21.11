"""M3 独立动作探针：只生成 he_material_probe 包，不同步、不接入主包。

复用 display_mob.bake/part_model/SNBT 与已有材质探针的只读资源生成。
一只隐身零尺寸 armor_stand 搭载21个 item_display；七动作20Hz采样，无AI/战斗/特效。
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from types import SimpleNamespace

import display_mob as dm
import heart_of_ender_audio as audio
import heart_of_ender_material_probe as material

REF = material.REF
NS = material.NS
OUT = REF / "m3_material_v3/motion_probe"
OWNER = "heart_of_ender_motion_probe.py/v1"
CLIPS = ("idle", "walk", "mortar", "cross_beam", "sink", "rise", "death")
DIMS = ("overworld", "the_nether", "the_end")
CARRIER = f"type=minecraft:armor_stand,tag={NS}.carrier,distance=0.."
PART = f"type=minecraft:item_display,tag={NS}.part,distance=0.."
CLIP, TIME, RUN, TEMP, ID = ("he_probe_clip", "he_probe_t", "he_probe_run", "he_probe_tmp", "he_probe_id")
sha, jb = material.sha, material.json_bytes


def plan(args):
    files, static_report = material.plan(SimpleNamespace(model=args.model, parts=args.parts,
                                                         model_scale=1., ground_y=-4.66381))
    # Keep all existing resource paths and public static entry names. Replace
    # only this new, in-memory package's functions with the single-instance rig.
    files = {p: b for p, b in files.items() if p.startswith("resourcepack/")}
    files["datapack/pack.mcmeta"] = jb({"pack": {"description": "Heart of Ender M3 isolated animation probe",
                                                   "pack_format": 94, "min_format": [94, 1], "max_format": 94}})
    stub = SimpleNamespace(bbmodel=str(args.model.resolve()), anim_from=None, key=NS)
    bones, png, resolution = dm.load_bbmodel(stub)
    clips = dm.load_animations(stub)
    parts = material.assemble_parts(json.loads(args.parts.read_text(encoding="utf-8")), bones, clips)
    if tuple(clips) != CLIPS:
        raise ValueError(f"动作清单或顺序不符：{tuple(clips)}")
    mob = SimpleNamespace(key=NS, glow=set(bones), tex=f"{NS}:item/atlas", model_scale=1.,
                          seat=-4.66381 / 16., parts=parts, held=None,
                          clips=[(name, 1, name in ("idle", "walk")) for name in CLIPS])
    offsets = {part: dm.part_model(mob, bones, part, members, resolution)[1] for part, members in parts}
    baked = dm.bake(mob, bones, offsets, clips)
    audio.validate()
    events = sorted({e for name in CLIPS for _, e, _, _ in audio.CUES.get(name, ())}
                    | {e for name in CLIPS for e, _, _ in audio.ENTER_CUES.get(name, ())})
    sounds, langs = {}, {"zh_cn": {}, "en_us": {}}
    for event in events:
        subtitle, sources, extra = audio.SOUNDS[event]
        entries = []
        for source in sources:
            target = Path(source).stem.lower().replace("-", "_")
            files[f"resourcepack/assets/{NS}/sounds/heart_of_ender/{target}.ogg"] = (audio.SOUND_DIR/source).read_bytes()
            entries.append({**(extra or {}), "name": f"{NS}:heart_of_ender/{target}"})
        subkey = f"subtitles.{NS}.heart_of_ender.{event}"
        sounds[f"heart_of_ender.{event}"] = {"subtitle": subkey, "sounds": entries}
        for language, text in zip(langs, subtitle):
            langs[language][subkey] = text
    files[f"resourcepack/assets/{NS}/sounds.json"] = jb(sounds)
    for language, values in langs.items():
        files[f"resourcepack/assets/{NS}/lang/{language}.json"] = jb(values)

    def fn(name, lines):
        files[f"datapack/data/{NS}/function/{name}.mcfunction"] = ("\n".join(lines)+"\n").encode("utf-8")

    def each_dim(command):
        return [f"execute in minecraft:{dim} run {command}" for dim in DIMS]

    def sound(event, volume, pitch):
        return f"playsound {NS}:heart_of_ender.{event} hostile @a[distance=..48] ~ ~ ~ {volume:g} {pitch:g}"

    def cue_at(name, tick):
        return [sound(event, volume, pitch) for seconds, event, volume, pitch in audio.CUES.get(name, ())
                if int(round(seconds / dm.TICK)) == tick]

    def passenger(part, component):
        return ('{id:"minecraft:item_display",Tags:["%s.part","%s.p.%s"],'
                'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"%s:%s"}},'
                'item_display:"none",brightness:{block:15,sky:15},Rotation:[0f,0f],'
                'teleport_duration:0,interpolation_duration:0,view_range:3f,transformation:%s}'
                % (NS, NS, part, NS, part, dm.snbt_components(mob, component)))

    def spawn(name, clip_name, tick, playing):
        frame = dict(baked[clip_name]["frames"])[tick]
        passengers = ",".join(passenger(part, frame[part]) for part, _ in parts)
        summon = 'summon minecraft:armor_stand ~ ~ ~ {Tags:["%s.carrier"],Marker:1b,Invisible:1b,NoGravity:1b,NoBasePlate:1b,Silent:1b,Invulnerable:1b,Rotation:[0f,0f],Passengers:[%s]}' % (NS, passengers)
        fn(name, ["# 在函数调用点重建唯一模型；不依赖玩家执行者。", f"function {NS}:clear", summon,
                  f"execute as @e[{CARRIER},limit=1] at @s run function {NS}:internal/init/{name}"])
        init = [f"scoreboard players operation @s {ID} = #generation {ID}",
                f"scoreboard players set @s {CLIP} {CLIPS.index(clip_name)}",
                f"scoreboard players set @s {TIME} {tick}",
                f"scoreboard players set @s {RUN} {int(playing)}"]
        if playing:
            init += [sound(e, v, p) for e, v, p in audio.ENTER_CUES.get(clip_name, ())]
            init += cue_at(clip_name, tick)
        fn(f"internal/init/{name}", init)

    def dispatch(name, rows):
        if len(rows) <= 4:
            lines = [f"execute if score @s {TIME} matches {tick} run return run function {NS}:{target}"
                     for tick, target in rows]
        else:
            mid = len(rows)//2
            lines = [f"execute if score @s {TIME} matches ..{rows[mid-1][0]} run return run function {NS}:{name}_a",
                     f"function {NS}:{name}_b"]
            dispatch(name+"_a", rows[:mid])
            dispatch(name+"_b", rows[mid:])
        fn(name, lines)

    manifests = {}
    for name, clip in baked.items():
        rows, previous = [], None
        for tick, frame in clip["frames"]:
            commands = [f"# {name} @ {tick}/20 秒；公共 dm.bake 的本帧目标。"]
            for part, _ in parts:
                component = frame[part]
                if previous and all(abs(a-b) < 1e-4 for a, b in zip(component[0]+component[1], previous[part][0]+previous[part][1])):
                    continue
                commands.append(f"execute on passengers if entity @s[tag={NS}.p.{part}] run data merge entity @s "
                                + "{start_interpolation:0,interpolation_duration:1,transformation:"
                                + dm.snbt_components(mob, component)+"}")
            commands += cue_at(name, tick)
            target = f"anim/{name}/f{tick}"
            fn(target, commands)
            rows.append((tick, target))
            previous = frame
        dispatch(f"anim/{name}/at", rows)
        commands = [f"scoreboard players add @s {TIME} 1"]
        if clip["loop"]:
            commands += [f"execute if score @s {TIME} matches {clip['ticks']}.. run scoreboard players set @s {TIME} 0"]
        commands += [f"function {NS}:anim/{name}/at"]
        if not clip["loop"]:
            commands += [f"execute if score @s {TIME} matches {clip['ticks']}.. run scoreboard players set @s {RUN} 2"]
        fn(f"anim/{name}/tick", commands)
        spawn(f"play/{name}", name, 0, True)
        ticks = [t for t, _ in clip["frames"]]
        expected = list(range(clip["ticks"] if clip["loop"] else clip["ticks"]+1))
        if ticks != expected:
            raise ValueError(f"采样端点/20Hz不符：{name}")
        manifests[name] = {"clip_id": CLIPS.index(name), "length_seconds": clips[name]["length"],
                           "duration_ticks": clip["ticks"], "loop": clip["loop"], "sample_count": len(ticks),
                           "first_tick": ticks[0], "last_tick": ticks[-1], "step_ticks": 1,
                           "baked_components_sha256": sha(jb(clip["frames"])),
                           "finish": "wrap to frame0" if clip["loop"] else "hold final frame; he_probe_run=2"}

    for short, clip_name, seconds in material.POSES:
        spawn(f"spawn_{short}", clip_name, int(round(seconds/dm.TICK)), False)
        # Compatibility names are retained; the new probe intentionally has
        # only one model, so every per-pose clear now safely clears that model.
        fn(f"clear_{short}", [f"function {NS}:clear"])
    fn("spawn", [f"function {NS}:spawn_idle"])
    fn("play/cross", [f"function {NS}:play/cross_beam"])
    fn("internal/stop_sounds", [f"stopsound @a hostile {NS}:heart_of_ender.{event}" for event in events])
    fn("clear", ["# 仅本独立探针；加载中实体立即清理，旧未加载载体以代号失效。",
                 f"scoreboard players add #generation {ID} 1"]
       + each_dim(f"kill @e[{PART}]") + each_dim(f"kill @e[{CARRIER}]")
       + [f"function {NS}:internal/stop_sounds"])
    fn("internal/retire", [f"execute on passengers if entity @s[tag={NS}.part] run kill @s", "kill @s"])
    fn("internal/pause", [f"scoreboard players set @s {RUN} 0",
                           f"execute on passengers if entity @s[tag={NS}.part] run data merge entity @s {{start_interpolation:0,interpolation_duration:0}}"])
    fn("pause", each_dim(f"execute as @e[{CARRIER}] at @s run function {NS}:internal/pause")
       + [f"function {NS}:internal/stop_sounds"])
    # Finished clips cannot resume beyond their last frame; play restarts them.
    resume = []
    for name, clip in baked.items():
        end = clip["ticks"]-1
        condition = f"if score @s {CLIP} matches {CLIPS.index(name)}"
        if not clip["loop"]:
            condition += f" if score @s {TIME} matches ..{end}"
        resume.append(f"execute {condition} run scoreboard players set @s {RUN} 1")
    fn("internal/resume", resume)
    fn("resume", each_dim(f"execute as @e[{CARRIER}] at @s run function {NS}:internal/resume"))
    fn("internal/stop", [f"scoreboard players set @s {CLIP} 0", f"scoreboard players set @s {TIME} 0",
                          f"scoreboard players set @s {RUN} 0", f"function {NS}:anim/idle/f0",
                          f"function {NS}:internal/pause"])
    fn("stop", each_dim(f"execute as @e[{CARRIER}] at @s run function {NS}:internal/stop")
       + [f"function {NS}:internal/stop_sounds"])
    fn("internal/tick", [f"execute unless score @s {RUN} matches 1 run return 0"]
       + [f"execute if score @s {CLIP} matches {i} run return run function {NS}:anim/{name}/tick"
          for i, name in enumerate(CLIPS)])
    tick = []
    for dim in DIMS:
        tick.append(f"execute in minecraft:{dim} as @e[{CARRIER}] at @s unless score @s {ID} = #generation {ID} run function {NS}:internal/retire")
    tick += [f"scoreboard players set #count {TEMP} 0"]
    tick += each_dim(f"execute as @e[{CARRIER}] run scoreboard players add #count {TEMP} 1")
    tick += [f"execute if score #count {TEMP} matches 2.. run function {NS}:clear"]
    tick += each_dim(f"execute as @e[{CARRIER}] at @s run function {NS}:internal/tick")
    tick += each_dim(f"kill @e[{PART},predicate=!{NS}:riding]")
    fn("tick", tick)
    fn("load", ["# M3独立调试；reload清理旧探针，避免继续过期帧。"]
       + [f"scoreboard objectives add {name} dummy" for name in (CLIP, TIME, RUN, TEMP, ID)]
       + [f"scoreboard players add #generation {ID} 0", f"function {NS}:clear"])
    files[f"datapack/data/{NS}/predicate/riding.json"] = jb({"condition": "minecraft:entity_properties", "entity": "this",
        "predicate": {"vehicle": {"type": "minecraft:armor_stand", "nbt": '{Tags:["he_material_probe.carrier"]}'}}})
    for kind in ("load", "tick"):
        files[f"datapack/data/minecraft/tags/function/{kind}.json"] = jb({"values": [f"{NS}:{kind}"]})

    # Verify the actual generated references, shape, source bytes and all
    # float components before handing the package to the headless server test.
    function_names = {p.removeprefix(f"datapack/data/{NS}/function/").removesuffix(".mcfunction")
                      for p in files if p.endswith(".mcfunction")}
    for path, data in files.items():
        if path.endswith((".json", ".mcmeta")):
            json.loads(data)
        if path.endswith(".mcfunction"):
            for target in re.findall(r"\bfunction "+NS+r":([a-z0-9_/]+)", data.decode()):
                if target not in function_names:
                    raise ValueError(f"缺失函数：{path} -> {target}")
    for name in [f"play/{n}" for n in CLIPS] + [f"spawn_{n}" for n, _, _ in material.POSES]:
        data = files[f"datapack/data/{NS}/function/{name}.mcfunction"].decode()
        if data.count('id:"minecraft:item_display"') != 21 or data.count("summon minecraft:armor_stand ") != 1:
            raise ValueError(f"不是单载体21乘客：{name}")
    for clip in baked.values():
        for _, frame in clip["frames"]:
            for comp in frame.values():
                if not all(material.finite(v) for v in comp[0]+comp[1]):
                    raise ValueError("非有限烘焙值")
    for short, clip_name, seconds in material.POSES:
        frame = dict(baked[clip_name]["frames"])[int(round(seconds/dm.TICK))]
        for part, comp in frame.items():
            prior = static_report["poses"][short][part]
            if max(abs(a-b) for a, b in zip(comp[0], prior["translation"])) > 1e-9:
                raise ValueError("新探针与原静态探针位置不一致")
            dot = abs(sum(a*b for a, b in zip(comp[1], prior["left_rotation"])))
            if abs(dot-1) > 1e-8:
                raise ValueError("新探针与原静态探针旋转不一致")
    if sha(args.model.read_bytes()) != static_report["model_sha256"] or sha(Path(dm.__file__).read_bytes()) != static_report["display_mob_sha256"]:
        raise ValueError("生成期间源文件改变，请重建")
    if files[f"resourcepack/assets/{NS}/textures/item/atlas.png"] != png:
        raise ValueError("原PNG字节发生改变")
    report = {"stage": "M3 isolated animation review; not M4 or M5 main-pack integration", "namespace": NS,
        "model_path": str(args.model.resolve()), "model_sha256": static_report["model_sha256"],
        "texture_png_sha256": sha(png), "display_mob_sha256": static_report["display_mob_sha256"],
        "generator_sha256": sha(Path(__file__).read_bytes()), "part_count": len(parts), "parts": static_report["parts"],
        "clips": manifests, "sample_rate_hz": 20, "interpolation_ticks": 1,
        "carrier": {"type": "minecraft:armor_stand", "Marker": True, "invisible": True, "tag": NS+".carrier", "passengers": 21},
        "scores": {"clip": CLIP, "current_sample_tick": TIME, "run": RUN, "run_values": {"0": "paused/static/stopped", "1": "playing", "2": "finished"}, "generation": ID},
        "sound_events": events, "sounds_count": sum(len(audio.SOUNDS[e][1]) for e in events),
        "scale": 1, "research_ground_y": -4.66381,
        "validation": {"function_references_resolve": True, "single_invisible_carrier_21_passengers": True, "sample_ranges_exact": True,
                       "static_poses_match_prior_probe": True, "png_bytes_preserved": True, "sources_unchanged": True,
                       "server_function_load_test": "pending independent test", "real_game_motion_seen": False},
        "runtime_notes": ["play/clip立即应用第0帧，之后每tick先递增再应用下一帧；入口与tick发生于同一服务端tick时仍可能有正常一tick调度差。",
                          "idle/walk不重复末端样本，时长边界直接回0；单次包含末帧，应用后run=2保留姿态，不自动回idle。",
                          "暂停将客户端补间归零并停止本namespace声音；继续不重放enter声，长音不支持音频寻址恢复。",
                          "每次play/spawn清除原版三维度已加载旧实体；代号使未加载旧载体以后加载即失效。自定义维度不在扫描范围。",
                          "三维度扫描均以distance=0..限制本维度，避免无位置约束的@e跨维度重复计数；单载体专用vehicle谓词清理失去本载体的part；载体移除后下一个数据包tick清理已加载残留。",
                          "载体没有AI、移动/伤害/技能/掉落，调试播放与实际世界坐标体型绑定无关。",
                          "只生成新目录，不同步实例；真实函数加载、客户端动画/透明和声音效果由后续独立测试确认。"]}
    files["motion_probe_manifest.json"] = jb(report)
    files["README.md"] = ("# M3 独立动作调试包\n\n"
        f"输入SHA-256：`{report['model_sha256']}`；scale=1；隐身零尺寸 armor_stand + 21 item_display。原贴图字节未改。\n\n"
        "本目录只生成独立 he_material_probe 资源包/数据包，不接入RPG主包，不开始M4/M5。生成器不自动同步游戏。\n\n"
        "七动作命令：`/function he_material_probe:play/idle`、`play/walk`、`play/mortar`、`play/cross_beam`、`play/sink`、`play/rise`、`play/death`（后六项同样加 `/function he_material_probe:` 前缀）。\n\n"
        "每次 play 都清理旧模型并在调用点召唤；想放在前方4格可用 `/execute positioned ^ ^ ^4 run function he_material_probe:play/idle`。\n\n"
        "控制：`/function he_material_probe:pause`、`resume`、`stop`、`clear`（同一函数前缀）。pause冻结当前采样；resume继续下一采样；stop回idle0并停止；clear移除模型。单次动作末帧保留，须play重新开始，resume不会越过末帧。\n\n"
        "保留静态入口：`spawn_idle`（idle0）、`spawn_cross`（cross_beam2s）、`spawn_mortar`（mortar1.2s）；每次只留一组21部件。`clear_idle/cross/mortar`均清理唯一探针。\n\n"
        "采样20Hz，补间1tick；第0帧立即建立，循环无重复终帧，单次包含终帧。/reload清旧探针。载体移除后下一tick清孤儿，未加载旧载体下次加载按代号退役；扫描原版三个维度。\n\n"
        "声音来自已归档官方素材，具体同步点为推断；pause/stop/clear仅停止he_material_probe事件，不影响其它包。没有光束/弹体/粒子、玩法或背景循环音。\n\n"
        "离线已检查结构、引用、采样范围、数值和静态入口一致性；服务端与真实游戏动作效果需独立验证，不以离线检查代替。\n\n"
        "素材版权属于Mojang Studios；本项目非商业，与Mojang无关联。\n").encode("utf-8")
    return files, report


def write_owned(output, files):
    output = output.resolve()
    if output != OUT.resolve():
        raise ValueError(f"只允许写专属输出目录：{OUT}")
    marker = output/"GENERATED_FILES.json"
    previous = {}
    if marker.exists():
        record = json.loads(marker.read_text(encoding="utf-8"))
        if record.get("owner") != OWNER:
            raise ValueError("输出不是本生成器管理")
        previous = record["files"]
    for relative in set(previous) | set(files):
        path = (output/relative).resolve()
        if output not in path.parents:
            raise ValueError("输出路径越界")
        if path.exists() and (relative not in previous or sha(path.read_bytes()) != previous[relative]):
            raise ValueError(f"拒绝覆盖非本脚本输出/手改：{path}")
    output.mkdir(parents=True, exist_ok=True)
    for relative in set(previous)-set(files):
        path = (output/relative).resolve()
        if path.exists():
            path.unlink()
    for relative, data in files.items():
        path = output/relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    marker.write_bytes(jb({"owner": OWNER, "files": {p: sha(data) for p, data in sorted(files.items())}}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, default=REF/"m3_material_v3/heart_of_ender_material_v3.bbmodel")
    parser.add_argument("--parts", type=Path, default=REF/"m2_geometry/geometry_spec.json")
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    files, report = plan(args)
    if not args.check_only:
        write_owned(args.out, files)
    print(json.dumps({"files": len(files), "model_sha256": report["model_sha256"], "parts": report["part_count"],
                      "clips": report["clips"], "output": None if args.check_only else str(args.out.resolve())}, ensure_ascii=False))


if __name__ == "__main__":
    main()
