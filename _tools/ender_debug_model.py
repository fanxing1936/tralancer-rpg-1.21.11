"""Heart of Ender / Arch-Visage 专用调试接入；不修改 display_mob 公共行为。

复用公共模型、矩阵、20 Hz 烘焙、SNBT 和声音输出；只拥有两个模型的目录。
载体为隐身零尺寸盔甲架；没有战斗标签、移动探测、AI、伤害或掉落。
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
from pathlib import Path

import display_mob as dm

KEYS = {"heart_of_ender", "arch_visage"}


def assemble_parts(spec, bones, clips):
    """显式部件加新刚性发光子骨；拒绝静默丢掉独立运动。"""
    parts = [(p["name"], list(p["bones"])) if isinstance(p, dict)
             else (p[0], list(p[1])) for p in spec]
    owner = {}
    if len({p for p, _ in parts}) != len(parts):
        raise ValueError("重复部件名")
    for part, members in parts:
        if not members:
            raise ValueError(f"空部件：{part}")
        for name in members:
            if name not in bones or name in owner:
                raise ValueError(f"骨骼不存在/重复归属：{name}")
            owner[name] = part
    by_part = dict(parts)
    for name, bone in bones.items():
        if name in owner or not bone["cubes"]:
            continue
        target = next((owner[n] for n in reversed(dm.chain(bones, name)[:-1]) if n in owner), None)
        if target is None:
            raise ValueError(f"几何骨没有归属：{name}")
        by_part[target].append(name)
        owner[name] = target
    for part, members in parts:
        root = members[0]
        if not any(bones[n]["cubes"] for n in members):
            raise ValueError(f"无几何部件：{part}")
        for name in members:
            for cube in bones[name]["cubes"]:
                if any(abs(v) > 1e-9 for v in (cube.get("rotation") or [0, 0, 0])):
                    raise ValueError(f"公共管线不处理独立cube rotation：{cube['name']}")
                for face in cube["faces"].values():
                    if face.get("texture") not in (None, 0):
                        raise ValueError("只接受 textures[0]")
            if name == root:
                continue
            if root not in dm.chain(bones, name)[:-1]:
                raise ValueError(f"合并骨不是部件子孙：{name}")
            rotation = bones[name]["rotation"]
            if sum(abs(v) > 1e-10 for v in rotation) > 1 or any(abs(v) > 45 for v in rotation):
                raise ValueError(f"合并rest超过单轴±45：{name}")
            rel = dm.bone_matrix(bones, name, stop=root)
            direct = dm.about(bones[name]["pivot"], rotation)
            if max(abs(rel[i][j] - direct[i][j]) for i in range(4) for j in range(4)) > 1e-8:
                raise ValueError(f"合并链有公共管线无法表达的中间rest：{name}")
            for clip in clips.values():
                for channel in ("position", "rotation"):
                    if any(any(abs(v) > 1e-9 for v in value)
                           for _, value, _ in clip["tracks"].get((name, channel), [])):
                        raise ValueError(f"合并骨有独立动作：{name}/{channel}")
    return parts


def _own_directory(path, root):
    nominal = Path(os.path.abspath(path))
    path, root = nominal.resolve(), Path(root).resolve()
    if path != nominal:
        raise ValueError(f"专属输出目录被链接重定向：{nominal}")
    if path == root or root not in path.parents:
        raise ValueError(f"输出路径越界：{path}")
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def _hook(dp, kind, entry, before_last=False):
    path = Path(dp) / "data/minecraft/tags/function" / (kind + ".json")
    if not path.exists():
        dm.wj(str(path), {"values": []})
    dm.hook_tag(str(dp), kind, entry, before_last)


def _runtime(mob, baked, initial_clip):
    fn, tg = mob.fn, mob.tag
    clip_score, time_score, run_score = mob.clip_score, mob.t_score, mob.score + "_run"
    id_score = mob.score + "_id"
    carrier = f"type=minecraft:armor_stand,tag={tg}"
    part_selector = f"type=minecraft:item_display,tag={tg}.part"

    def write(name, lines):
        dm.wf(str(Path(mob.func) / (name + ".mcfunction")), lines)

    def guarded(lines):
        return [f"execute unless entity @s[{carrier}] run return 0"] + lines

    def control(name, target):
        # 自己作为载体调用时严格只改自己；玩家/控制台按调用位置找本维度最近一只。
        write("debug/" + name, [
            f"execute if entity @s[{carrier}] at @s run return run function {fn}/{target}",
            f"execute as @e[{carrier},distance=..32,sort=nearest,limit=1] at @s run function {fn}/{target}",
        ])

    manifests = {}
    for index, (name, _, _) in enumerate(mob.clips):
        clip = baked[name]
        if clip["step"] != 1:
            raise ValueError("本专用调试层固定每tick采样，不改变公共STRIDE")
        last_sent, leaves = {}, []
        for tick, frame in clip["frames"]:
            lines = [f"# {name} @ {tick}/20 秒；实际bbmodel烘焙，非玩法。"]
            for part, _ in mob.parts:
                component = frame[part]
                if not all(math.isfinite(v) for v in component[0] + component[1]):
                    raise ValueError("非有限烘焙变换")
                # 与最近实际发送值比较，防止每步很小的运动累计后仍永远被跳过。
                if part in last_sent and all(abs(a-b) < 1e-4 for a, b in zip(component[0] + component[1], last_sent[part][0] + last_sent[part][1])):
                    continue
                lines.append(f"execute on passengers if entity @s[tag={tg}.p.{part}] run data merge entity @s "
                             + "{start_interpolation:0,interpolation_duration:1,transformation:"
                             + dm.snbt_components(mob, component) + "}")
                last_sent[part] = component
            lines += dm.cue_lines(mob, name, tick, 1)
            write(f"anim/{name}/f{tick}", lines)
            leaves.append((tick, f"{fn}/anim/{name}/f{tick}"))
        dm.dispatch_tree(mob, str(Path(mob.anim) / name / "at"), f"{fn}/anim/{name}/at", leaves)
        lines = [f"scoreboard players add @s {time_score} 1"]
        if clip["loop"]:
            lines.append(f"execute if score @s {time_score} matches {clip['ticks']}.. run scoreboard players set @s {time_score} 0")
        lines.append(f"function {fn}/anim/{name}/at")
        if not clip["loop"]:
            lines.append(f"execute if score @s {time_score} matches {clip['ticks']}.. run scoreboard players set @s {run_score} 2")
        write(f"anim/{name}/tick", lines)
        write(f"anim/enter/{name}", guarded([
            f"function {fn}/internal/stop_sounds",
            f"scoreboard players set @s {clip_score} {index}",
            f"scoreboard players set @s {time_score} 0",
            f"scoreboard players set @s {run_score} 1",
        ] + [dm.playsound(mob, e, v, p) for e, v, p in mob.enter_cues.get(name, ())] + [
            f"function {fn}/anim/{name}/f0",
            f"execute on passengers if entity @s[tag={tg}.part] run data merge entity @s {{interpolation_duration:0}}",
        ]))
        control("anim/" + name, "anim/enter/" + name)
        write("debug/play/" + name, [f"function {fn}/debug/anim/{name}"])
        ticks = [t for t, _ in clip["frames"]]
        if ticks != list(range(clip["ticks"] if clip["loop"] else clip["ticks"] + 1)):
            raise ValueError(f"不完整20Hz采样：{name}")
        manifests[name] = {"id": index, "ticks": clip["ticks"], "loop": clip["loop"],
                           "samples": len(ticks), "first_tick": ticks[0], "last_tick": ticks[-1]}

    # 已加载实体：@e不加位置条件会跨维度查一次，at @s切换到每只实体的真实维度。
    # 不把同一个无distance选择器在三个execute in里重复执行。
    write("tick", [
        f"execute as @e[{carrier}] at @s run function {fn}/follow",
        f"execute as @e[{part_selector}] unless predicate {fn}/riding run kill @s",
    ])
    write("follow", [
        f"execute on passengers if entity @s[tag={tg}.part] run rotate @s ~ 0",
        f"execute unless score @s {run_score} matches 1 run return 0",
    ] + [f"execute if score @s {clip_score} matches {i} run return run function {fn}/anim/{name}/tick"
         for i, (name, _, _) in enumerate(mob.clips)])
    # 只查类型：谓词里的 nbt 会把载体连同全部乘客序列化一遍，每个部件每刻一次。
    dm.wj(str(Path(mob.dp) / "data/rpg/predicate" / mob.key / "riding.json"), {
        "condition": "minecraft:entity_properties", "entity": "this",
        "predicate": {"vehicle": {"type": "minecraft:armor_stand"}}})
    write("load", ["# 只新增本模型计分板，reload不重置其它实体或clip。"] + [
        f"scoreboard objectives add {score} dummy" for score in (clip_score, time_score, run_score, id_score)
    ] + [f"scoreboard players add #next {id_score} 0"])

    first = baked[initial_clip]["frames"][0][1]
    passengers = []
    for part, _ in mob.parts:
        nbt = dm.passenger(mob, part, first[part])
        nbt = nbt.replace('item_display:"none",', 'item_display:"none",brightness:{block:15,sky:15},')
        nbt = nbt.replace("interpolation_duration:2", "interpolation_duration:0")
        passengers.append(nbt)
    write("debug/spawn", [
        "# 在调用点增加一只独立模型；scale=1为调试预览，不绑定任何已有生物。",
        'summon minecraft:armor_stand ~ ~ ~ {Tags:["%s","%s.new"],Marker:1b,Invisible:1b,NoGravity:1b,NoBasePlate:1b,Silent:1b,Invulnerable:1b,Rotation:[0f,0f],Passengers:[%s]}'
        % (tg, tg, ",".join(passengers)),
        f"execute as @e[{carrier},tag={tg}.new,distance=..0.01] at @s run function {fn}/internal/initialize",
    ])
    write("spawn", [f"function {fn}/debug/spawn"])
    write("internal/initialize", [
        f"tag @s remove {tg}.new",
        f"scoreboard players add #next {id_score} 1",
        f"scoreboard players operation @s {id_score} = #next {id_score}",
        f"scoreboard players operation #owner {id_score} = @s {id_score}",
        f"execute on passengers if entity @s[tag={tg}.part] run scoreboard players operation @s {id_score} = #owner {id_score}",
        f"function {fn}/anim/enter/{initial_clip}",
    ])
    # Minecraft stopsound没有发声实体过滤；只停止附近此模型事件，绝不停止其它模型声音。
    write("internal/stop_sounds", [f"stopsound @a[distance=..32] hostile {dm.sound_id(mob, e)}" for e in sorted(mob.sounds)])
    write("internal/pause", guarded([
        f"scoreboard players set @s {run_score} 0",
        f"execute on passengers if entity @s[tag={tg}.part] run data merge entity @s {{start_interpolation:0,interpolation_duration:0}}",
        f"function {fn}/internal/stop_sounds",
    ]))
    resume = []
    for index, (name, _, _) in enumerate(mob.clips):
        clip = baked[name]
        condition = f"if score @s {clip_score} matches {index}"
        if not clip["loop"]:
            condition += f" if score @s {time_score} matches ..{clip['ticks']-1}"
        resume.append(f"execute {condition} run scoreboard players set @s {run_score} 1")
    write("internal/resume", guarded(resume))
    write("internal/stop", guarded([
        f"scoreboard players set @s {clip_score} 0", f"scoreboard players set @s {time_score} 0",
        f"function {fn}/anim/idle/f0", f"function {fn}/internal/pause",
    ]))
    write("internal/clear", guarded([
        f"function {fn}/internal/stop_sounds",
        f"execute on passengers if entity @s[tag={tg}.part] run kill @s", "kill @s",
    ]))
    for name in ("pause", "resume", "stop", "clear"):
        control(name, "internal/" + name)
    write("debug/clear_all", [
        "# 所有已加载维度的本模型；不影响其它模型，未加载区块内实例不在命令范围。",
        f"execute as @e[{carrier}] at @s run function {fn}/internal/clear",
        f"kill @e[{part_selector}]",
    ])
    _hook(mob.dp, "tick", fn + "/tick", True)
    _hook(mob.dp, "load", fn + "/load")
    return manifests


def build_debug(mob, rp, dp, research_ground_y, initial_clip="idle"):
    if mob.key not in KEYS or mob.carrier != "minecraft:armor_stand":
        raise ValueError("专用helper仅接受HE/AV盔甲架调试载体")
    rp, dp = Path(rp).resolve(), Path(dp).resolve()
    source = Path(mob.bbmodel).read_bytes()
    pipeline = Path(dm.__file__).read_bytes()
    doc = json.loads(source)
    if len(doc.get("textures", [])) != 1 or not doc["textures"][0].get("source", "").startswith("data:image/png;base64,"):
        raise ValueError("必须是一张内嵌PNG图集")
    bones, png, resolution = dm.load_bbmodel(mob)
    clips = dm.load_animations(mob)
    mob.parts = assemble_parts(mob.parts, bones, clips)
    mob.glow = set(bones)  # 沿已确认材质探针：所有表面满光照，无bloom/shader替换。
    if [c[0] for c in mob.clips[:2]] != ["idle", "walk"]:
        raise ValueError("idle、walk必须排最前")
    if initial_clip not in {c[0] for c in mob.clips}:
        raise ValueError(f"未知初始调试clip：{initial_clip}")
    mob.paths(str(rp), str(dp))
    _own_directory(mob.func, dp)
    _own_directory(rp / "assets/rpg/models" / mob.key, rp)
    _own_directory(rp / "assets/rpg/items" / mob.key, rp)
    atlas = rp / "assets/rpg/textures/item" / mob.key / "atlas.png"
    atlas.parent.mkdir(parents=True, exist_ok=True)
    atlas.write_bytes(png)
    offsets = {}
    for part, members in mob.parts:
        model, offsets[part] = dm.part_model(mob, bones, part, members, resolution)
        dm.wj(str(rp / "assets/rpg/models" / mob.key / (part + ".json")), model)
        dm.wj(str(rp / "assets/rpg/items" / mob.key / (part + ".json")), {
            "model": {"type": "minecraft:model", "model": f"rpg:{mob.key}/{part}",
                      "tints": [{"type": "minecraft:custom_model_data", "index": 0, "default": 16777215}]}})
    # Root提供精确element/face元数据后，专属后处理无损引用44遮罩；不改公共管线。
    mask_tints = []
    if doc.get("unhandled_root_fields", {}).get("emissive_masks"):
        from heart_of_ender_emission import apply_item_tints
        mask_tints = apply_item_tints(mob, bones)
    baked = dm.bake(mob, bones, offsets, clips)
    if mob.sounds:
        dm.write_sounds(mob)
    manifests = _runtime(mob, baked, initial_clip)
    for name, details in manifests.items():
        details["source_length_seconds"] = clips[name]["length"]
        details["runtime_length_seconds"] = details["ticks"] * dm.TICK
    if Path(mob.bbmodel).read_bytes() != source or Path(dm.__file__).read_bytes() != pipeline:
        raise RuntimeError("生成中模型或公共管线改变，请重跑本生成器")
    report = {
        "generator": mob.generator, "model_sha256": hashlib.sha256(source).hexdigest(),
        "display_mob_sha256": hashlib.sha256(pipeline).hexdigest(),
        "texture_png_sha256": hashlib.sha256(png).hexdigest(), "parts": mob.parts,
        "part_count": len(mob.parts), "clips": manifests, "fullbright": True,
        "emissive_mask_faces": mask_tints,
        "carrier": "minecraft:armor_stand", "marker": True, "carrier_tag": mob.tag,
        "part_tag": mob.tag + ".part", "model_scale": mob.model_scale,
        "research_ground_y": research_ground_y, "effective_seat": mob.seat,
        "scoreboards": [mob.clip_score, mob.t_score, mob.score + "_run", mob.score + "_id"],
        "runtime": {
            "run_values": {"0": "paused/stopped", "1": "playing", "2": "finished"},
            "initial_clip": initial_clip,
            "sample_rate": 20, "once_finish": "hold final sample", "automatic_walk": False,
            "multi_instance": "scores per carrier; animation/clear only its direct passengers",
            "dimensions": "one global unrestricted @e query; at @s before local execution",
            "clear_scope": "loaded entities; removed carriers leave parts swept on next loaded tick",
            "debug_scope": "@s carrier, otherwise nearest within 32 blocks in current dimension",
            "sound_limit": "stopsound cannot filter emitting entity; nearby same-model sounds also stop",
        },
    }
    dm.wj(str(dp / (mob.key + "_debug_manifest.json")), report)
    print(f"{mob.key}: {len(mob.parts)} parts; debug-only; clips " + ", ".join(manifests))
    return report
