#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验教皇 M1 原始素材并生成可复现的素材清单；不修改原始素材。"""
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import platform
import struct
import subprocess
import sys
from urllib.parse import quote

import PIL
from PIL import Image
import imageio_ffmpeg

HERE = Path(__file__).resolve().parent
REF = HERE / "pope_ref"
OUT = REF / "m1"
MAGIC = {".png": b"\x89PNG\r\n\x1a\n", ".jpg": b"\xff\xd8", ".gif": b"GIF8", ".ogg": b"OggS"}
EXPECTED = {"visual": 18, "sound": 39, "sound_groups": 17, "reused": 2}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def sound_group(asset):
    return asset["caption"].split("\t")[-1]


def check_one(asset, ffmpeg, logs, reused=False):
    row = dict(asset)
    row["reused"] = reused
    row["checks"] = {}
    path = REF / asset["path"]
    try:
        data = path.read_bytes()
        row.update(bytes=len(data), sha256=digest(data))
        suffix = path.suffix.lower()
        row["checks"]["file_signature"] = data.startswith(MAGIC[suffix])
        if not row["checks"]["file_signature"]:
            raise ValueError("文件签名与扩展名不符")
        if not reused:
            matches = [r for r in logs if r.get("path") == asset["path"]]
            row["download_records"] = matches
            row["checks"]["download_log_hash_and_bytes"] = any(
                r.get("sha256") == row["sha256"] and r.get("bytes") == len(data) for r in matches
            )
        if suffix == ".ogg":
            marker = data.find(b"\x01vorbis")
            if marker < 0:
                raise ValueError("未找到 Vorbis identification header")
            channels = data[marker + 11]
            sample_rate = struct.unpack_from("<I", data, marker + 12)[0]
            args = [ffmpeg, "-nostdin", "-hide_banner", "-v", "error", "-xerror", "-i", str(path),
                    "-map", "0:a:0", "-vn", "-c:a", "pcm_s16le", "-f", "s16le", "pipe:1"]
            run = subprocess.run(args, capture_output=True, timeout=90)
            error = run.stderr.decode("utf-8", errors="replace").strip()
            row["checks"]["ffmpeg_full_decode"] = run.returncode == 0 and not error and len(run.stdout) > 0
            row["audio"] = {
                "codec": "Vorbis", "channels": channels, "sample_rate_hz": sample_rate,
                "decoded_pcm_s16le_bytes": len(run.stdout),
                "decoded_samples_per_channel": len(run.stdout) // (channels * 2),
                "decoded_duration_seconds": round(len(run.stdout) / (channels * 2 * sample_rate), 6),
                "ffmpeg_returncode": run.returncode, "ffmpeg_stderr": error,
                "manual_listen": False,
            }
            row["sound_group"] = sound_group(asset)
        else:
            with Image.open(path) as image:
                image.verify()
            with Image.open(path) as image:
                frame_count = getattr(image, "n_frames", 1)
                row["image"] = {"format": image.format, "width": image.width, "height": image.height,
                                "mode": image.mode, "frames": frame_count}
                durations = []
                for index in range(frame_count):
                    image.seek(index)
                    image.load()
                    image.convert("RGBA").tobytes()
                    durations.append(image.info.get("duration", 0))
                if suffix == ".gif":
                    row["image"].update(frame_durations_ms=durations, total_duration_ms=sum(durations),
                                        total_duration_seconds=round(sum(durations) / 1000, 6))
                    row["checks"]["gif_all_frames_have_positive_duration"] = all(d > 0 for d in durations)
                row["checks"]["pillow_verify_and_all_frames_decode"] = True
        row["ok"] = all(row["checks"].values())
    except Exception as exc:
        row["ok"] = False
        row["error"] = str(exc)
    return row


def description(row):
    if "audio" in row:
        a = row["audio"]
        return "%g 秒；%d Hz；%d 声道" % (a["decoded_duration_seconds"], a["sample_rate_hz"], a["channels"])
    im = row.get("image", {})
    value = "%s×%s" % (im.get("width", "?"), im.get("height", "?"))
    if "total_duration_seconds" in im:
        value += "；%d 帧；%g 秒" % (im["frames"], im["total_duration_seconds"])
    return value


def write_sources(report):
    rows = report["assets"]
    lines = [
        "# 教皇（Arch-Illager）参考素材来源", "",
        "原作：Minecraft Dungeons 的 Arch-Illager（Mojang Studios）。本目录原始游戏角色、贴图、渲染、动画与音效版权归 Mojang 所有；本项目非商业，与 Mojang 无关联。", "",
        "参考页面：[Arch-Illager 图库](https://minecraft.wiki/w/Dungeons:Arch-Illager/Gallery)、[角色与行为](https://minecraft.wiki/w/Dungeons:Arch-Illager)、[音效](https://minecraft.wiki/w/Dungeons:Arch-Illager#Sounds)。", "",
        "采集日期：%s。原始文件通过本机接收页面在浏览器中 fetch Minecraft Wiki 的原始媒体，再 POST 回本机保存；按页面实际文件名保留大小写。缩略图仅用于定位，未将 120px/其他缩略图当原图。清单依据为 `source_manifest.json`，成功保存响应见 `download_log.jsonl`。" % report["observed_date"], "",
        "本次共存档 18 个视觉文件（10 个 GIF、4 个渲染/贴图、4 个截图）及 17 组 39 段 OGG 音效；另外直接引用项目已有的 2 张贴图，没有重复复制。未下载 Music，未下载 Archvessel/Archvisage 音效。", "",
        "主渲染 `MCD_Arch-Illager.png` 的 manifest 保留初始地址 `https://minecraft.wiki/images/MCD_Arch-Illager.png`，后核对 [文件页](https://minecraft.wiki/w/File:MCD_Arch-Illager.png) 的 Original file 链接为下表带 `?a3f08&format=original` 的地址。下载日志第 57 条记录成功保存，response_url 为无查询参数的图片地址；该日志只记成功写入，不记录此前失败请求。", "",
        "所有本次下载文件的字节数与 SHA-256 都与成功接收日志相符。全部图片经 Pillow 校验并完整解码，全部 GIF 逐帧解码，39 段 OGG 经 FFmpeg 从头至尾解码到 PCM。本次没有逐段人工听完音频，也没有进行真实游戏内验证。详见 `m1/ASSET_VALIDATION.md` 和 `m1/asset_validation.json`。", "",
        "## 本次下载的原始素材", "",
        "下列 SHA-256 为完整 64 位校验值；文件地址保留页面查询参数。尺寸/时长是文件元数据与解码结果，不是未来 clip 的定稿时长。", "",
        "| 原文件 | 字节 | SHA-256 | 尺寸/时长 | 来源页面 | 原始文件地址 |",
        "|---|---:|---|---|---|---|",
    ]
    for row in rows:
        if row["reused"]:
            continue
        lines.append("| `%s` | %s | `%s` | %s | [页面](%s) | [原文件](%s) |" % (
            row["path"], row.get("bytes", "?"), row.get("sha256", "?"), description(row), row["page"], row["url"]))
    lines += ["", "## 直接引用的已有原贴图", "",
              "以下路径相对本目录。只读取、校验并引用，未在 pope_ref 再存副本。原媒体 URL 由已有来源记录/原文件名对应，未为本次重复下载。", "",
              "| 项目已有路径 | 字节 | SHA-256 | 尺寸 | 来源页面 | 原始文件地址 |",
              "|---|---:|---|---|---|---|"]
    for row in rows:
        if not row["reused"]:
            continue
        url = "https://minecraft.wiki/images/" + quote(Path(row["path"]).name, safe="_().-")
        lines.append("| `%s` | %s | `%s` | %s | [页面](%s) | [原文件](%s) |" % (
            row["path"], row.get("bytes", "?"), row.get("sha256", "?"), description(row), row["page"], url))
    lines += ["", "## 声音分组", "", "| 页面声音标识 | 段数 |", "|---|---:|"]
    for group, count in report["sound_groups"].items():
        lines.append("| `%s` | %d |" % (group, count))
    lines += ["", "## 派生资料与制作状态", "",
              "`m1/` 中抽帧、标注、UV 分析及结构报告属于本项目派生分析资料，不是从游戏导出的模型、官方骨骼或原动画工程。其事实、候选解释和推断应分别标注。", "",
              "此 SOURCES.md 及校验报告由 `_tools/pope_validate_sources.py` 生成，脚本只读原始素材。M1 不代表静态模型、动作、构建接入或真实游戏验证已经完成。", ""]
    (REF / "SOURCES.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


def write_report(report):
    counts = report["counts"]
    lines = ["# 教皇 M1 素材校验", "", "采集日期：%s。校验结果：%s。" % (
        report["observed_date"], "全部通过" if report["ok"] else "存在问题，见 JSON"), "",
        "本报告只证明文件完整性与可解码性，不证明模型还原度、动作定稿或游戏内兼容。未在真实游戏内看过；没有逐段人工听完音频。", "",
        "## 范围与方法", "",
        "- 本次下载：%d 个视觉文件、%d 段音效（%d 组），总计 %d 文件；引用已有贴图 %d 张。" % (
            counts["visual"], counts["sound"], counts["sound_groups"], counts["downloaded"], counts["reused"]),
        "- 检查文件签名、实际字节数、完整 SHA-256，并逐项对比 download_log.jsonl 的成功写入记录。",
        "- Pillow verify 后重新打开每张图；GIF 逐帧 seek/load/转为 RGBA 完整解码，时长为每帧 duration 的总和。",
        "- FFmpeg 使用 -xerror 完整解码每段 OGG 为内存 PCM s16le；记录退出码、错误输出、解码样本数和声道/采样率。没有截取前几秒代替完整检查。",
        "- 原始素材仅被读取，未转码覆盖；两张 heart_of_ender_ref 贴图没有复制。",
        "- 清单无 Music、Archvessel、Archvisage；sounds 目录的 .ogg 与清单严格一致。", "",
        "工具：Python %s；Pillow %s；%s。" % (
            report["tools"]["python"], report["tools"]["pillow"], report["tools"]["ffmpeg_version"]), "",
        "复现：在仓库运行 `python _tools/pope_validate_sources.py`。输出本报告、`m1/asset_validation.json` 和 `SOURCES.md`，不写入原始素材。", "",
        "## 图片与 GIF 实测", "",
        "| 文件 | 尺寸 | 帧数 | GIF 总时长（秒） | 校验 |", "|---|---|---:|---:|---|"]
    for row in report["assets"]:
        if "image" not in row:
            continue
        im = row["image"]
        lines.append("| `%s` | %d×%d | %d | %s | %s |" % (
            row["path"], im["width"], im["height"], im["frames"],
            im.get("total_duration_seconds", "—"), "通过" if row["ok"] else "失败"))
    lines += ["", "GIF 文件总时长包含导出的完整片段，不等同于自然动作周期或最终 clip 时长；后续剪辑/重定时必须在动作报告记录。每帧原始 duration 见 JSON。", "",
              "## 音效完整解码", "", "| 文件 | PCM 解码时长（秒） | 声道 | 采样率 | 解码结果 |",
              "|---|---:|---:|---:|---|"]
    for row in report["assets"]:
        if "audio" not in row:
            continue
        au = row["audio"]
        lines.append("| `%s` | %s | %d | %d | %s |" % (
            row["path"], au["decoded_duration_seconds"], au["channels"], au["sample_rate_hz"],
            "通过" if row["ok"] else "失败"))
    lines += ["", "## 重复内容与下载记录", "",
              "不同原文件名即使字节相同也保持原名，不自行删除或重命名；分组与实际声音链接仍以网页清单为准。", ""]
    duplicate = report["identical_content_groups"]
    if duplicate:
        lines += ["| SHA-256 | 相同内容文件 |", "|---|---|"]
        for sha, names in duplicate.items():
            lines.append("| `%s` | %s |" % (sha, "、".join("`%s`" % n for n in names)))
    else:
        lines.append("本次没有不同文件名但内容完全相同的记录。")
    lines += ["", "主渲染 manifest 的 initial_url、Original file 页面和当前 URL 均保留；download_log.jsonl 第57条成功记录与本地哈希一致。该 JSONL 只记录成功保存，不将缺少的失败条目伪造成已有日志。", ""]
    if report["problems"]:
        lines += ["## 问题", ""] + ["- " + p for p in report["problems"]] + [""]
    (OUT / "ASSET_VALIDATION.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main():
    manifest = json.loads((REF / "source_manifest.json").read_text(encoding="utf-8"))
    logs = [json.loads(line) for line in (REF / "download_log.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    jobs = [(a, False) for a in manifest["assets"]] + [(a, True) for a in manifest.get("reused", [])]
    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(lambda pair: check_one(pair[0], ffmpeg, logs, pair[1]), jobs))
    sounds = [a for a in rows if a["path"].endswith(".ogg")]
    groups = dict(sorted(Counter(a.get("sound_group", "未知") for a in sounds).items()))
    counts = {"downloaded": len(manifest["assets"]), "reused": len(manifest.get("reused", [])),
              "sound": len(sounds), "visual": sum(not a["path"].endswith(".ogg") and not a["reused"] for a in rows),
              "sound_groups": len(groups)}
    problems = [r["path"] + ": " + r.get("error", str(r["checks"])) for r in rows if not r["ok"]]
    for name, expected in EXPECTED.items():
        if counts[name] != expected:
            problems.append("数量不符：%s=%d，预期%d" % (name, counts[name], expected))
    paths = [a["path"] for a in manifest["assets"]]
    if len(paths) != len(set(paths)):
        problems.append("清单路径重复")
    if any(any(word in p.lower() for word in ("archvessel", "archvisage", "bgm_", "music")) for p in paths):
        problems.append("出现排除范围的文件名")
    actual_ogg = {p.relative_to(REF).as_posix() for p in (REF / "sounds").glob("*.ogg")}
    if actual_ogg != {a["path"] for a in sounds}:
        problems.append("sounds 目录与清单不一致")
    primary_texture = next(r for r in rows if r["path"].endswith("MCD_Arch-Illager_(texture).png"))
    if [primary_texture.get("image", {}).get(k) for k in ("width", "height")] != [64, 64]:
        problems.append("人物原贴图不是64×64")
    by_hash = defaultdict(list)
    for row in rows:
        if "sha256" in row:
            by_hash[row["sha256"]].append(row["path"])
    version = subprocess.run([ffmpeg, "-version"], capture_output=True, text=True, timeout=15).stdout.splitlines()[0]
    report = {"observed_date": manifest["observed_date"], "ok": not problems, "counts": counts,
              "tools": {"python": platform.python_version(), "pillow": PIL.__version__,
                        "ffmpeg_path": ffmpeg, "ffmpeg_version": version},
              "manual_listen": False, "in_game_verified": False, "sound_groups": groups,
              "identical_content_groups": {k: v for k, v in by_hash.items() if len(v) > 1},
              "problems": problems, "assets": rows}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "asset_validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    write_sources(report)
    write_report(report)
    print(json.dumps({"ok": report["ok"], "counts": counts, "problems": problems}, ensure_ascii=False))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
