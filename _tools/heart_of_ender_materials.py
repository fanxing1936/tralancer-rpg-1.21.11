# -*- coding: utf-8 -*-
"""M1：校验末影之心原始素材，完整抽帧并生成带时间戳的对照索引。

只读 source_manifest.json 及原始素材；只写本脚本拥有的 validation.json、
frames/、contact_sheets/ 和两个 SOURCES.md。不生成或修改模型与运行时。
用法：python _tools/heart_of_ender_materials.py [--check-only]
--check-only 仍更新校验报告和署名清单，但不重新抽帧。
"""

from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
import math
import re
import struct
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = False
HERE = Path(__file__).resolve().parent
REF = HERE / "heart_of_ender_ref"
ARCH = HERE / "arch_visage_ref"
PAGE = "https://minecraft.wiki/w/Dungeons:Heart_of_Ender"
FPS = 25
GIF_EXPECTED = {
    "MCD_Heart_of_Ender_Idle.gif": (400, 16.0, 20),
    "MCD_Arch-Illager_Docile.gif": (120, 4.8, 10),
    "MCD_Arch-Illager_Anxious.gif": (200, 8.0, 10),
    "MCD_Arch-Illager_Fourside.gif": (50, 2.0, 5),
    "MCD_Arch-Visage_Spawn_Attack_in_game.gif": (122, 4.88, 5),
    "MCD_Arch-Visage_Spawn_Attack.gif": (150, 6.0, 5),
}
SIZE_EXPECTED = {
    "MCD_Decal_Puddle_(texture).png": (711, 711),
    "MCD_Heart_of_Ender_(glow_effect_texture).png": (44, 44),
    "T_ArchIllagerUndressed.png": (64, 64),
    "T_ArchIllagerUndressed_S.png": (64, 64),
    "MCD_Arch-Illager_(texture).png": (64, 64),
    "MCD_Arch-Illager_(shadow_texture).png": (64, 64),
    "MCD_Heart_of_Ender.png": (1000, 840),
    "MCD_Arch-Visage.png": (800, 800),
    **{name: (500, 500) for name in GIF_EXPECTED},
}
ARCH_ILLAGER_TEXTURES = {
    "T_ArchIllagerUndressed.png", "T_ArchIllagerUndressed_S.png",
    "MCD_Arch-Illager_(texture).png", "MCD_Arch-Illager_(shadow_texture).png",
}


def source_page(asset: dict, manifest: dict):
    return asset.get("source_page") or ("https://minecraft.wiki/w/Dungeons:Arch-Illager/Gallery"
                                       if asset["file"] in ARCH_ILLAGER_TEXTURES else manifest.get("page", PAGE))


def json_write(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def image_stats(im: Image.Image):
    arr = np.asarray(im.convert("RGBA"))
    alpha = arr[:, :, 3]
    unique, counts = np.unique(arr.reshape(-1, 4), axis=0, return_counts=True)
    order = np.argsort(counts)[::-1][:12]
    visible = arr[:, :, :3][alpha > 0]
    return {
        "statistics_scope": "静态图或动图第 0 帧，解码后的 RGBA 像素；不作颜色修正",
        "pixels": int(alpha.size),
        "alpha_min": int(alpha.min()), "alpha_max": int(alpha.max()),
        "alpha_definition": "alpha/255 为不透明度；透明度=1-alpha/255，不可混淆",
        "alpha_levels": [int(x) for x in np.unique(alpha)],
        "transparent_pixels": int((alpha == 0).sum()),
        "translucent_pixels": int(((alpha > 0) & (alpha < 255)).sum()),
        "opaque_pixels": int((alpha == 255).sum()),
        "unique_rgba_colors": len(unique),
        "mean_visible_rgb": [round(float(x), 4) for x in visible.mean(axis=0)] if len(visible) else [],
        "visible_rgb_max_at_most_16_pixels": int((visible.max(axis=1) <= 16).sum()) if len(visible) else 0,
        "most_common_rgba": [
            {"rgba": [int(x) for x in unique[n]], "pixels": int(counts[n])} for n in order
        ],
    }


def font(size: int):
    for path in (Path("C:/Windows/Fonts/consola.ttf"), Path("C:/Windows/Fonts/arial.ttf")):
        if path.is_file():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default(size=size)


def sheet(frames: list[tuple[Path, int, float]], out: Path, title: str, page: int, pages: int):
    # 240 px square image plus label; keep every overview/full-frame page <=25 tiles.
    cols, tile, label, gap, header = 5, 240, 30, 12, 62
    rows = math.ceil(len(frames) / cols)
    canvas = Image.new("RGB", (gap + cols * (tile + gap), header + rows * (tile + label + gap)), "#151923")
    draw = ImageDraw.Draw(canvas)
    draw.text((gap, 10), title, font=font(18), fill="white")
    draw.text((gap, 34), f"Page {page}/{pages} | sampled frame numbers and source timestamps", font=font(16), fill="#b7c4db")
    for n, (path, index, time) in enumerate(frames):
        x, y = gap + (n % cols) * (tile + gap), header + (n // cols) * (tile + label + gap)
        checker = Image.new("RGBA", (tile, tile), "#404650")
        checkdraw = ImageDraw.Draw(checker)
        for yy in range(0, tile, 20):
            for xx in range(0, tile, 20):
                if (xx // 20 + yy // 20) % 2:
                    checkdraw.rectangle((xx, yy, xx + 19, yy + 19), fill="#4a505b")
        with Image.open(path) as source:
            view = source.convert("RGBA")
            view.thumbnail((tile, tile), Image.Resampling.NEAREST)
            checker.alpha_composite(view, ((tile - view.width) // 2, (tile - view.height) // 2))
        canvas.paste(checker.convert("RGB"), (x, y))
        draw.text((x + 4, y + tile + 4), f"f{index:04d}   {time:05.2f}s", font=font(17), fill="#f1e9d6")
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out)


def paged_sheets(rows, folder: Path, prefix: str, title: str):
    pages = math.ceil(len(rows) / 25)
    for page in range(pages):
        sheet(rows[page * 25:(page + 1) * 25], folder / f"{prefix}_{page + 1:02d}.png", title, page + 1, pages)


def extract_gif(path: Path, record: dict, extract: bool):
    rows, durations, mapping = [], [], []
    folder = REF / "frames" / path.stem
    if extract:
        folder.mkdir(parents=True, exist_ok=True)
    elapsed_ms, next_sample_ms = 0, 0
    with Image.open(path) as gif:
        storage_frames = gif.n_frames
        for source_index in range(storage_frames):
            gif.seek(source_index)
            frame = gif.convert("RGBA")  # Pillow applies GIF disposal/compositing.
            frame.load()
            duration = gif.info.get("duration", 0)
            durations.append(duration)
            if duration <= 0:
                raise ValueError("GIF 存在缺失或非正帧时长")
            while next_sample_ms < elapsed_ms + duration:
                n = len(rows)
                target = folder / f"frame_{n:04d}.png"
                if extract:
                    frame.save(target)
                rows.append((target, n, next_sample_ms / 1000))
                mapping.append((n, next_sample_ms, source_index, elapsed_ms, duration))
                next_sample_ms += 40
            elapsed_ms += duration
    record.update({
        "storage_frames": storage_frames, "frames": len(rows), "sampled_frames_25fps": len(rows),
        "source_frame_durations_ms": durations,
        "duration_ms_histogram": dict(sorted(collections.Counter(durations).items())),
        "duration_seconds": sum(durations) / 1000,
        "storage_strict_25_fps": bool(durations) and all(x == 40 for x in durations),
        "resampled_strict_25_fps": True,
        "frame_time_definition": "零基采样帧 n，时间 n*0.04 s；按源帧累计duration选择覆盖此时刻的已合成帧，长持帧重复采样",
        "full_decode": "通过 Pillow 顺序解码全部帧，LOAD_TRUNCATED_IMAGES=False",
    })
    expected_count, expected_seconds, stride = GIF_EXPECTED[path.name]
    if len(rows) != expected_count or sum(durations) != round(expected_seconds * 1000) or any(x % 40 for x in durations):
        record["errors"].append(f"GIF 参数不符：预期40ms采样后 {expected_count} 帧/{expected_seconds}s，源延时应为40ms整数倍")
    if not record["storage_strict_25_fps"]:
        record["warnings"].append("源GIF采用变时长持帧；已按累计duration展开25fps，不能把存储索引直接乘0.04")
    if extract:
        with (folder / "frames.csv").open("w", encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(["sample_index", "time_seconds_25fps", "source_index", "source_start_seconds", "source_duration_ms", "file"])
            for n, time_ms, source_index, source_start_ms, duration in mapping:
                writer.writerow([n, f"{time_ms / 1000:.2f}", source_index, f"{source_start_ms / 1000:.2f}", duration, f"frame_{n:04d}.png"])
        selected = rows[::stride]
        if selected[-1] != rows[-1]:
            selected.append(rows[-1])
        output = REF / "contact_sheets" / path.stem
        paged_sheets(selected, output, "overview", f"{path.stem} | overview step={stride / FPS:.2f}s")
        paged_sheets(rows, output, "all_frames", f"{path.stem} | all 25 fps frames")
        record["extraction"] = {"frames": folder.relative_to(REF).as_posix(), "overview_stride_frames": stride,
                                "overview_pages": math.ceil(len(selected) / 25), "all_frames_pages": math.ceil(len(rows) / 25)}


def ogg_crc(data: bytes):
    table = []
    for n in range(256):
        value = n << 24
        for _ in range(8):
            value = ((value << 1) ^ (0x04C11DB7 if value & 0x80000000 else 0)) & 0xffffffff
        table.append(value)
    crc = 0
    for byte in data:
        crc = ((crc << 8) & 0xffffffff) ^ table[((crc >> 24) & 255) ^ byte]
    return crc


def ogg_metadata(path: Path):
    data = path.read_bytes()
    offset, pages, granules, sequence = 0, 0, [], []
    first_packet = bytearray()
    packet_done, saw_end = False, False
    while offset < len(data):
        if data[offset:offset + 4] != b"OggS" or len(data) - offset < 27:
            raise ValueError(f"OGG 页边界损坏：byte {offset}")
        count = data[offset + 26]
        if offset + 27 + count > len(data):
            raise ValueError("OGG 段表被截断")
        lacing = data[offset + 27:offset + 27 + count]
        length = 27 + count + sum(lacing)
        page = bytearray(data[offset:offset + length])
        if len(page) != length:
            raise ValueError("OGG 页被截断")
        expected_crc = struct.unpack_from("<I", page, 22)[0]
        page[22:26] = b"\0\0\0\0"
        if ogg_crc(page) != expected_crc:
            raise ValueError(f"OGG CRC 不符：page {pages}")
        granule = struct.unpack_from("<Q", page, 6)[0]
        if granule != 0xffffffffffffffff:
            granules.append(granule)
        sequence.append(struct.unpack_from("<I", page, 18)[0])
        saw_end |= bool(page[5] & 4)
        if not packet_done:
            pos = 27 + count
            for size in lacing:
                first_packet.extend(page[pos:pos + size])
                pos += size
                if size < 255:
                    packet_done = True
                    break
        pages += 1
        offset += length
    if first_packet[:7] != b"\x01vorbis":
        raise ValueError("未识别为 OGG Vorbis")
    if not saw_end or sequence != list(range(pages)):
        raise ValueError("OGG 缺失 EOS 或页序号不连续")
    channels = first_packet[11]
    sample_rate = struct.unpack_from("<I", first_packet, 12)[0]
    samples = max(granules)
    return {"codec": "vorbis", "channels": channels, "sample_rate": sample_rate,
            "samples_from_final_granule": samples, "duration_seconds": round(samples / sample_rate, 6),
            "ogg_pages": pages, "ogg_crc_all_pages_valid": True, "ogg_eos_present": saw_end}


def ffmpeg_binary():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        from shutil import which
        return which("ffmpeg")


def media_decode(path: Path, executable: str | None):
    if executable is None:
        return {"full_decode": "未验证：未找到 ffmpeg", "warnings": ["无可用解码器"]}
    process = subprocess.run([executable, "-hide_banner", "-nostdin", "-v", "info", "-xerror", "-i", str(path),
                              "-f", "null", "-"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    log = process.stderr.decode("utf-8", "replace")
    if process.returncode:
        raise ValueError("ffmpeg 全量解码失败：" + log[-1800:])
    metadata = [line.strip() for line in log.splitlines() if "Duration:" in line or "Stream #0:" in line][:6]
    warnings = [line.strip() for line in log.splitlines() if any(x in line.lower() for x in ("error", "corrupt", "invalid"))]
    return {"full_decode": "通过 ffmpeg -xerror 全量解码到 null", "decoder_metadata": metadata, "warnings": warnings}


def extract_video(path: Path, record: dict, executable: str | None):
    if not executable:
        record["warnings"].append("未抽取视频帧：无 ffmpeg")
        return
    folder = REF / "frames" / "Heart_of_Ender_idle_video"
    folder.mkdir(parents=True, exist_ok=True)
    # Select the first source frame at or after each integer second; retain actual pts_time.
    pattern = folder / "frame_%04d.png"
    process = subprocess.run([executable, "-hide_banner", "-nostdin", "-v", "info", "-y", "-i", str(path),
                              "-vf", "select='gte(t,selected_n)',showinfo", "-fps_mode", "vfr",
                              "-start_number", "0", str(pattern)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if process.returncode:
        raise ValueError("视频抽帧失败：" + process.stderr.decode("utf-8", "replace"))
    files = sorted(folder.glob("frame_*.png"))
    # Source is decoded/metadata-checked independently; these are 1-second visual reference samples only.
    times = [float(x) for x in re.findall(r"pts_time:([0-9.]+)", process.stderr.decode("utf-8", "replace"))]
    if len(times) != len(files):
        raise ValueError(f"视频帧数与pts时间数不符：{len(files)} vs {len(times)}")
    rows = [(frame, n, times[n]) for n, frame in enumerate(files)]
    with (folder / "frames.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["sample", "nominal_time_seconds", "actual_pts_seconds", "file", "note"])
        for frame, n, t in rows:
            writer.writerow([n, n, f"{t:.6f}", frame.name, "独立游戏内视频每秒参考，不替代16秒Idle GIF"])
    paged_sheets(rows, REF / "contact_sheets" / "Heart_of_Ender_idle_video", "overview", "Heart_of_Ender_idle.mp4 | 1-second reference samples")
    record["extraction"] = {"sample_count": len(rows), "nominal_step_seconds": 1,
                            "frames": folder.relative_to(REF).as_posix()}


def source_docs(manifest: dict, records: list[dict]):
    header = ["# 末影之心与 Arch-Visage 参考素材来源", "",
              "原作：Minecraft Dungeons 的 Heart of Ender、Arch-Visage 与体内的 Arch-Illager（Mojang Studios），版权归 Mojang 所有。",
              f"页面：<{manifest.get('page', PAGE)}>（Renders、Animations、Textures、Gallery、Sounds 与 Video；不下载 Music）。",
              "所有原始素材经浏览器从 minecraft.wiki 的 `/images/<文件名>` 取得，按原文件名保存。",
              "本项目非商业，与 Mojang 无关联。Minecraft Wiki 页面与贡献者作为整理来源一并致谢。", "",
              f"素材清单观察日期：{manifest.get('observed_date', '未记录')}。字节数与 SHA-256 根据本地实际文件重新计算；完整哈希与解码校验见 `validation.json`。",
              "校验范围为本地文件完整性、格式、可解码性与内容参数；未取得发行者校验值，SHA-256 仅为本地存档指纹，不代表与官方发布校验值比对通过。",
              "原始素材统一存于本目录；Arch-Visage 目录的来源表引用这些文件，避免原始素材出现多个副本。", "",
              "体内小人的四张贴图来源于 Arch-Illager/Gallery 的 Textures；`T_ArchIllagerUndressed_S.png` 被页面标为 shadow texture，不作为发光层使用。",
              "44×44 的 glow_effect_texture 是白色半透明效果遮罩，不是眼睛/嘴贴图。RGBA 的 alpha/255 表示不透明度（alpha=160 约为62.75%不透明、37.25%透明）。", "",
              "## 原始素材", "", "| 文件 | 字节 | SHA-256（前 16 位） | 来源页面 | 文件地址 |", "|---|---|---|---|---|"]
    for record in records:
        rel = Path(record["path"]).relative_to("heart_of_ender_ref").as_posix()
        digest = record.get("sha256", "未取得")[:16]
        header.append(f"| `{rel}` | {record.get('bytes', '缺失')} | `{digest}` | <{source_page(record, manifest)}> | <{record['url']}> |")
    header.extend(["", "## 由此派生（不是原始素材）", "", "| 文件 | 说明 |", "|---|---|",
                   "| `source_manifest.json` | 页面链接、文件原名、素材用途与页面行为中文摘要；下载来源索引 |",
                   "| `validation.json` | 文件字节、完整 SHA-256、图片颜色/透明度、GIF 帧时长、OGG CRC 和全量媒体解码检查 |",
                   "| `frames/<动图名>/frame_0000.png` 等 | Pillow 合成原始帧后，按累计duration展开25fps的 RGBA 帧；长持帧重复采样，无重绘、无缩放 |",
                   "| `frames/<动图名>/frames.csv` | 零基采样帧号、n×0.04 s、源存储索引、源帧累计时间与单帧时长 |",
                   "| `contact_sheets/<动图名>/overview_*.png` | 等间隔初筛索引，最近邻缩略图；不是最终动作关键姿态结论 |",
                   "| `contact_sheets/<动图名>/all_frames_*.png` | 每页最多25帧的完整逐帧索引，5列、240像素预览 |",
                   "| `frames/Heart_of_Ender_idle_video/` | 游戏内视频每秒参考帧，不能替代16秒Idle动图 |",
                   "| `analysis_texture/` | 原始贴图颜色/透明度核验、裁窗坐标和最近邻放大；研究数据，不是最终图集或bbmodel |",
                   "| `analysis_structure/` | 肢体计数、连接点、比例及遮挡问题的原图裁片/标注；结构研究，不是模型渲染 |",
                   "| `analysis_poses/` | 原始动作关键姿态选择、时间/帧索引与并排参考；动作研究，不是已完成动画 |",
                   "| `M1_REPORT.md` | M1素材、结构测量与动作依据的阶段报告，区分观测事实、推断与待确认项 |", "",
                   "`validation.json`、`frames/`、`contact_sheets/` 与本来源表由 `../heart_of_ender_materials.py` 生成；脚本不修改原始文件。",
                   "`analysis_texture/` 由 `../heart_of_ender_texture_study.py` 生成；`analysis_structure/`、`analysis_poses/` 与 `M1_REPORT.md` 是另行整理的研究材料，不由素材校验脚本重建。",
                   "Arch-Visage 两段GIF采用变时长存储：游戏内版92个存储帧展开为122帧，未采用版120个存储帧展开为150帧；均按累计延时映射，不把存储索引误当25fps序号。",
                   "M1 不包含 `.bbmodel`、重绘贴图、模型渲染或动画烘焙。", ""])
    (REF / "SOURCES.md").write_text("\n".join(header), encoding="utf-8")
    arch = ["# Arch-Visage 参考素材来源", "",
            "原作：Minecraft Dungeons 的 Arch-Visage（Mojang Studios），版权归 Mojang 所有。",
            f"页面：<{manifest.get('page', PAGE)}>。本项目非商业，与 Mojang 无关联。",
            "原始素材统一存档在 `../heart_of_ender_ref/`，保留原文件名。完整共用素材与校验见该目录的 `SOURCES.md`、`validation.json`。",
            "以 `MCD_Arch-Visage_Spawn_Attack_in_game.gif` 为动作依据；带眼睛版本仅作未采用版本参照。", "",
            "## 原始素材", "", "| 文件 | 字节 | SHA-256（前 16 位） | 来源页面 | 文件地址 |", "|---|---|---|---|---|"]
    for record in records:
        if ("arch-visage" in record["file"].lower() or "archvisage" in record["file"].lower()
                or record["file"] in ("MCD_Decal_Puddle_(texture).png", "MCD_Heart_of_Ender_(glow_effect_texture).png")):
            rel = "../" + record["path"]
            arch.append(f"| `{rel}` | {record.get('bytes', '缺失')} | `{record.get('sha256', '未取得')[:16]}` | <{source_page(record, manifest)}> | <{record['url']}> |")
    arch.extend(["", "## 由此派生（不是原始素材）", "", "| 文件 | 说明 |", "|---|---|",
                 "| `../heart_of_ender_ref/frames/MCD_Arch-Visage_Spawn_Attack_in_game/` | 游戏内版本完整122帧（预期25 fps，实际核验见 validation.json） |",
                 "| `../heart_of_ender_ref/contact_sheets/MCD_Arch-Visage_Spawn_Attack_in_game/` | 原始动作初筛及逐帧索引 |", "",
                 "Arch-Visage 共用的贴图、结构和动作研究见 `../heart_of_ender_ref/analysis_texture/`、`analysis_structure/`、`analysis_poses/` 与 `M1_REPORT.md`；这些研究材料不是bbmodel或最终动画。", "",
                 "M1 尚未制作 `arch_visage.bbmodel`；本清单不宣称模型或动画已完成。", ""])
    ARCH.mkdir(parents=True, exist_ok=True)
    (ARCH / "SOURCES.md").write_text("\n".join(arch), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    manifest = json.loads((REF / "source_manifest.json").read_text(encoding="utf-8"))
    executable = ffmpeg_binary()
    previous = {}
    if args.check_only and (REF / "validation.json").is_file():
        old = json.loads((REF / "validation.json").read_text(encoding="utf-8"))
        previous = {r["path"]: r for r in old.get("assets", [])}
    records = []
    for asset in manifest["assets"]:
        record = dict(asset, errors=[], warnings=[])
        record["source_page"] = source_page(asset, manifest)
        records.append(record)
        path = (HERE / asset["path"]).resolve()
        if not path.is_relative_to(REF.resolve()):
            raise ValueError(f"素材路径超出专用目录：{asset['path']}")
        if not path.is_file():
            record["errors"].append("文件尚未取得或不存在；如下载仍在进行请稍后重跑")
            continue
        data = path.read_bytes()
        record.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        if args.check_only and previous.get(asset["path"], {}).get("sha256") == record["sha256"]:
            if "extraction" in previous[asset["path"]]:
                record["extraction"] = previous[asset["path"]]["extraction"]
        try:
            if asset["category"] in ("image", "texture"):
                with Image.open(path) as im:
                    record.update(format=im.format, width=im.width, height=im.height, source_mode=im.mode)
                    if path.suffix.lower() != ".gif":
                        im.verify()
                with Image.open(path) as im:
                    im.load()
                    record["pixel_statistics"] = image_stats(im)
                    size = im.size
                if path.name in SIZE_EXPECTED and size != SIZE_EXPECTED[path.name]:
                    record["errors"].append(f"尺寸不符：预期 {SIZE_EXPECTED[path.name]}，实际 {size}")
                if path.suffix.lower() == ".gif":
                    extract_gif(path, record, not args.check_only)
                else:
                    record["full_decode"] = "通过 Pillow verify 与完整像素解码"
            elif asset["category"] == "sound":
                record.update(ogg_metadata(path))
                record.update(media_decode(path, executable))
            elif asset["category"] == "video":
                record.update(media_decode(path, executable))
                if not args.check_only:
                    extract_video(path, record, executable)
            else:
                raise ValueError(f"未知素材类型：{asset['category']}")
        except Exception as error:
            record["errors"].append(f"{type(error).__name__}: {error}")
        print(f"{'ERROR' if record['errors'] else 'OK'} {asset['file']}", flush=True)
    result = {
        "source_manifest": "source_manifest.json", "observation_date": manifest.get("observed_date"),
        "verification_scope": "本地完整性、格式、可解码性和参数检验；SHA-256为新算存档指纹，未与发行者提供的校验值比对",
        "generator": "../heart_of_ender_materials.py", "reference_fps": FPS,
        "decoder": executable,
        "summary": {"expected_assets": len(records), "present_assets": sum("sha256" in r for r in records),
                    "category_counts": dict(collections.Counter(r["category"] for r in records)),
                    "assets_with_errors": sum(bool(r["errors"]) for r in records),
                    "gif_frames": sum(r.get("frames", 0) for r in records),
                    "total_bytes": sum(r.get("bytes", 0) for r in records)},
        "assets": records,
    }
    json_write(REF / "validation.json", result)
    source_docs(manifest, records)
    print(json.dumps(result["summary"], ensure_ascii=False), flush=True)
    return 1 if result["summary"]["assets_with_errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
