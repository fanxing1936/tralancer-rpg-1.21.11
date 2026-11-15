"""M3 材质专用离线探针：不构建项目、不改公共管线、不自动同步游戏。

读取指定 bbmodel 的实际几何/内嵌RGBA/动画，生成独立 he_material_probe RP/DP。
每个静态姿态21个直接item_display，无载体、AI、tick或玩法。
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
from pathlib import Path
from types import SimpleNamespace

from PIL import Image

import display_mob as dm

ROOT = Path(__file__).resolve().parent
REF = ROOT / "heart_of_ender_ref"
PROBE_ROOT = REF / "m3_material_v2" / "probe"
NS = "he_material_probe"
POSES = (("idle", "idle", 0.), ("cross", "cross_beam", 2.), ("mortar", "mortar", 1.2))
OWNER = "heart_of_ender_material_probe.py/v1"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(obj):
    return (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def finite(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def assemble_parts(spec, bones, clips):
    parts = [(p["name"], list(p["bones"])) for p in spec["parts"]]
    if len(parts) != 21 or len({p for p, _ in parts}) != 21:
        raise ValueError("材质探针要求恰好21个独立部件")
    owner = {}
    for part, members in parts:
        for name in members:
            if name not in bones or name in owner:
                raise ValueError(f"部件骨骼不存在/重复：{name}")
            owner[name] = part
    by_part = dict(parts)
    # 新局部glow骨若没有独立运动，可合并到已存在的祖先部件，不新增display。
    for name, bone in bones.items():
        if name in owner or not bone["cubes"]:
            continue
        ancestors = dm.chain(bones, name)[:-1]
        target = next((owner[n] for n in reversed(ancestors) if n in owner), None)
        if target is None:
            raise ValueError(f"新带几何骨没有可合并部件：{name}")
        by_part[target].append(name)
        owner[name] = target
    for part, members in parts:
        root = members[0]
        if not any(bones[n]["cubes"] for n in members):
            raise ValueError(f"空展示部件：{part}")
        for name in members[1:]:
            if root not in dm.chain(bones, name)[:-1]:
                raise ValueError(f"合并骨不属于部件祖先：{part}/{name}")
            rotation = bones[name]["rotation"]
            if sum(abs(v) > 1e-10 for v in rotation) > 1 or any(abs(v) > 45 for v in rotation):
                raise ValueError(f"合并骨rest超出单轴±45限制：{name}")
            rel = dm.bone_matrix(bones, name, stop=root)
            direct = dm.about(bones[name]["pivot"], rotation)
            if max(abs(rel[i][j]-direct[i][j]) for i in range(4) for j in range(4)) > 1e-8:
                raise ValueError(f"合并链含额外中间rest变换，公共part_model不能表达：{name}")
            for clip in clips.values():
                for channel in ("position", "rotation"):
                    keys = clip["tracks"].get((name, channel), [])
                    if any(any(abs(v) > 1e-9 for v in value) for _, value, _ in keys):
                        raise ValueError(f"合并骨含独立动画，不能静默丢弃：{name}/{channel}")
    return parts


def plan(args):
    model_path = args.model.resolve(strict=True)
    model_bytes = model_path.read_bytes()
    pipeline_path = Path(dm.__file__).resolve()
    pipeline_bytes = pipeline_path.read_bytes()
    document = json.loads(model_bytes)
    if len(document.get("textures", [])) != 1:
        raise ValueError("只接受一张内嵌图集")
    if not document["textures"][0].get("source", "").startswith("data:image/png;base64,"):
        raise ValueError("textures[0]必须是内嵌PNG")
    stub = SimpleNamespace(bbmodel=str(model_path), anim_from=None, key=NS)
    bones, png, resolution = dm.load_bbmodel(stub)
    with Image.open(io.BytesIO(png)) as image:
        image.load()
        rgba = image.convert("RGBA")
    if rgba.size != (resolution["width"], resolution["height"]):
        raise ValueError("PNG尺寸与bbmodel resolution不一致")
    clips = dm.load_animations(stub)
    for _, clip, time in POSES:
        if clip not in clips or time > clips[clip]["length"]:
            raise ValueError(f"缺少所需姿态：{clip}@{time}")
    spec = json.loads(args.parts.read_text(encoding="utf-8"))
    parts = assemble_parts(spec, bones, clips)
    # 用只含所需字段的对象调用纯几何接口；不实例化/运行公共Mob构建。
    mob = SimpleNamespace(key=NS, glow=set(bones), tex=f"{NS}:item/atlas",
                          model_scale=args.model_scale, seat=0.)
    files, offsets, counts = {}, {}, {}
    files["resourcepack/pack.mcmeta"] = json_bytes({"pack": {
        "description": "Heart of Ender M3 material probe (not RPG integration)",
        "pack_format": 75, "min_format": [75, 0], "max_format": 75}})
    files["datapack/pack.mcmeta"] = json_bytes({"pack": {
        "description": "Heart of Ender M3 static material probe",
        "pack_format": 94, "min_format": [94, 1], "max_format": 94}})
    texture_path = f"resourcepack/assets/{NS}/textures/item/atlas.png"
    files[texture_path] = png
    for part, members in parts:
        model, offset = dm.part_model(mob, bones, part, members, resolution)
        if not model["elements"]:
            raise ValueError(f"部件没有模型元素：{part}")
        for element in model["elements"]:
            if not all(finite(v) and -16 <= v <= 32 for v in element["from"]+element["to"]):
                raise ValueError(f"部件坐标非法：{part}")
            if element.get("light_emission") != 15 or element.get("shade") is not False:
                raise ValueError(f"满光照标记缺失：{part}")
            for face in element["faces"].values():
                if not all(finite(v) and 0 <= v <= 16 for v in face["uv"]):
                    raise ValueError(f"UV超出单图集：{part}")
        offsets[part] = offset
        counts[part] = {"cubes": len(model["elements"]), "faces": sum(len(e["faces"]) for e in model["elements"]), "bones": members}
        files[f"resourcepack/assets/{NS}/models/{part}.json"] = json_bytes(model)
        files[f"resourcepack/assets/{NS}/items/{part}.json"] = json_bytes({"model": {
            "type": "minecraft:model", "model": f"{NS}:{part}",
            "tints": [{"type": "minecraft:constant", "value": 16777215}]}})
    matrices = {}
    for pose, clip_name, time in POSES:
        commands = [f"# M3材质静态探针；{clip_name} @ {time:g}s；21 displays；没有tick/载体/玩法。",
                    f"function {NS}:clear_{pose}"]
        matrices[pose] = {}
        for part, members in parts:
            world = dm.posed_matrix(bones, members[0], clips[clip_name], time)
            transform = dm.display_matrix(mob, bones, members[0], offsets[part], world)
            # 把既有研究地面平面放在调用点Y；不改变模型几何/动画，不决定最终Boss体型。
            transform[1][3] -= args.ground_y * args.model_scale / 16.
            if not all(finite(v) for row in transform for v in row):
                raise ValueError(f"非有限变换：{pose}/{part}")
            component = dm.components(transform, args.model_scale)
            matrices[pose][part] = {"matrix": transform, "translation": component[0], "left_rotation": component[1]}
            nbt = ('{Tags:["%s.part","%s.%s","%s.p.%s"],'
                   'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"%s:%s"}},'
                   'item_display:"none",brightness:{block:15,sky:15},'
                   'Rotation:[0f,0f],teleport_duration:0,interpolation_duration:0,'
                   'view_range:3f,transformation:%s}'
                   % (NS, NS, pose, NS, part, NS, part, dm.snbt_components(mob, component)))
            commands.append("summon minecraft:item_display ~ ~ ~ "+nbt)
        files[f"datapack/data/{NS}/function/spawn_{pose}.mcfunction"] = ("\n".join(commands)+"\n").encode("utf-8")
        files[f"datapack/data/{NS}/function/clear_{pose}.mcfunction"] = (
            f"kill @e[type=minecraft:item_display,tag={NS}.part,tag={NS}.{pose}]\n").encode("utf-8")
    files[f"datapack/data/{NS}/function/spawn.mcfunction"] = f"function {NS}:spawn_idle\n".encode()
    files[f"datapack/data/{NS}/function/clear.mcfunction"] = f"kill @e[type=minecraft:item_display,tag={NS}.part]\n".encode()
    # 检验实际序列化输出，不启动服务端或游戏；不声称已完成函数加载测试。
    for name, data in files.items():
        if name.endswith((".json", ".mcmeta")):
            json.loads(data)
    for pose, _, _ in POSES:
        data = files[f"datapack/data/{NS}/function/spawn_{pose}.mcfunction"].decode()
        if sum(line.startswith("summon minecraft:item_display ") for line in data.splitlines()) != 21:
            raise ValueError("召唤数量不是21")
    if model_path.read_bytes() != model_bytes or pipeline_path.read_bytes() != pipeline_bytes:
        raise RuntimeError("生成期间输入文件发生并发变化，请从新版本重新生成")
    alphas = rgba.getchannel("A").histogram()
    report = {"stage": "M3 isolated material probe; not M5 integration", "namespace": NS,
        "model_path": str(model_path), "model_sha256": sha(model_bytes),
        "display_mob_sha256": sha(pipeline_bytes), "texture_png_sha256": sha(png),
        "texture_rgba_sha256": sha(rgba.tobytes()), "atlas_size": list(rgba.size),
        "alpha_pixels": {"discarded_at_default_0_1": sum(alphas[:26]), "visible_translucent": sum(alphas[26:255]), "opaque": alphas[255]},
        "parts": counts, "part_count_per_pose": 21, "poses": matrices,
        "scale_for_probe_only": args.model_scale, "ground_y_for_probe_only": args.ground_y,
        "carrier": None, "tick_functions": [], "shader_overrides": [],
        "validation": {"single_embedded_png": True, "png_bytes_preserved": files[texture_path] == png,
            "json_parses": True, "part_bounds_and_uv_valid": True, "static_transforms_finite": True,
            "source_and_pipeline_unchanged": True, "real_game_seen": False, "server_function_load_test": False},
        "limitations": ["仅静态材质对照，不播放动作或检验载体移除清理", "满光照并不关闭原生item shader的法线方向光或产生bloom",
                        "未同步实例；仅用户批准同步后才可安装与实测", "透明排序、背面和alpha低端阈值尚未在真实游戏验证"]}
    files["probe_manifest.json"] = json_bytes(report)
    files["README.md"] = (f"# M3 独立材质探针\n\n输入：`{model_path}`\n\nSHA-256：`{sha(model_bytes)}`\n\n"
        "本目录仅供后续经用户批准的手动安装，不是M5正式接入。脚本没有同步任何实例。\n\n"
        "`resourcepack/` 与 `datapack/` 是各自独立的完整包。资源/数据格式分别75.0和94.1。\n\n"
        f"批准安装后：`/function {NS}:spawn_idle`、`/function {NS}:spawn_cross` 或 `/function {NS}:spawn_mortar`；统一清理 `/function {NS}:clear`。\n\n"
        "每次姿态21个直接展示实体；重召同姿态先清同姿态，其余姿态可留作并排，同时三组为63个。所有姿态共用同一part清理tag。没有载体、AI、tick、音效、战斗或掉落。\n\n"
        f"固定idle0秒/cross_beam2秒/mortar1.2秒。mortar用于观察张嘴时嘴内上下面的渐变。探针scale={args.model_scale:g}，研究地面Y={args.ground_y:g}放在调用点；这些不是最终Boss体型/载体决定。\n\n"
        "全部元素light_emission15、展示brightness15。Java仍有法线方向光、0.1 alpha阈值、背面剔除、深度写入与透明排序限制，见上级research/ENGINE_NOTES.md。\n\n"
        "离线仅核JSON、21部件、坐标/UV、有限变换及内嵌PNG原字节。未运行服务器函数加载测试，未在真实游戏内看过。\n\n"
        "原始素材版权属于Mojang Studios；本项目非商业，与Mojang无关联。\n").encode("utf-8")
    return files, report


def write_owned(output, files):
    output = output.resolve()
    root = PROBE_ROOT.resolve()
    roots = (root, (REF / "m3_material_v3" / "probe").resolve())
    if not any(output == r or r in output.parents for r in roots):
        raise ValueError(f"输出必须位于本任务独占探针目录：{roots}")
    manifest_path = output / "GENERATED_FILES.json"
    previous = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("owner") != OWNER:
            raise ValueError("输出目录不是本脚本所有，拒绝覆盖")
        previous = manifest["files"]
    # 任何删除/覆盖先验证绝对路径归属；不递归删除，拒绝覆盖外部手改。
    for relative in set(previous) | set(files):
        path = (output / relative).resolve()
        if output not in path.parents:
            raise ValueError("输出路径越界")
        if path.exists():
            if relative not in previous or sha(path.read_bytes()) != previous[relative]:
                raise ValueError(f"文件不是本脚本上次输出或已被修改，拒绝覆盖：{path}")
    output.mkdir(parents=True, exist_ok=True)
    for relative in set(previous)-set(files):
        path = (output/relative).resolve()
        if path.exists():
            path.unlink()
    for relative, data in files.items():
        path = output/relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    manifest_path.write_bytes(json_bytes({"owner": OWNER, "files": {p: sha(b) for p, b in sorted(files.items())}}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, required=True, help="实际内嵌图集且含idle/cross_beam/mortar的bbmodel")
    parser.add_argument("--parts", type=Path, default=REF/"m2_geometry/geometry_spec.json")
    parser.add_argument("--out", type=Path, default=PROBE_ROOT)
    parser.add_argument("--model-scale", type=float, default=1.)
    parser.add_argument("--ground-y", type=float, default=-4.66381, help="M3既有研究地面，仅用于探针放置")
    parser.add_argument("--check-only", action="store_true", help="仅在内存生成和检查，不写资源/数据包")
    args = parser.parse_args()
    if not finite(args.model_scale) or not 0 < args.model_scale <= 10 or not finite(args.ground_y):
        parser.error("探针scale须为0..10的有限正数，ground-y须为有限数")
    files, report = plan(args)
    if not args.check_only:
        write_owned(args.out, files)
    print(json.dumps({"check_only": args.check_only, "files": len(files), "part_count_per_pose": 21,
        "model_sha256": report["model_sha256"], "png_sha256": report["texture_png_sha256"],
        "validation": report["validation"], "output": None if args.check_only else str(args.out.resolve())}, ensure_ascii=False))


if __name__ == "__main__":
    main()
