"""Decode the 11 published Prime Enchanter GIFs and preserve source timing."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


MOTION = Path(__file__).resolve().parent
ORIGINALS = MOTION.parent.parent / "originals"
CLIPS = (
    ("idle", "Idle"), ("walk", "Walk"), ("spawn", "Spawn"), ("death", "Death"),
    ("forward_strike", "Forward_Strike"), ("fury_fist", "Fury_Fist"),
    ("launch", "Launch"), ("lightning_slam", "Lightning_Slam"), ("overcharge", "Overcharge"),
    ("staggered", "Staggered"), ("summon", "Summon"),
)


def read_frames(source: Path):
    frames = []
    rows = []
    cursor = 0
    with Image.open(source) as gif:
        if gif.format != "GIF":
            raise ValueError(f"Expected GIF: {source}")
        loops = gif.info.get("loop")
        size = list(gif.size)
        for index in range(gif.n_frames):
            gif.seek(index)
            frame = gif.convert("RGBA")
            frame.load()
            delay = gif.info.get("duration")
            if not isinstance(delay, int) or delay <= 0:
                raise ValueError(f"{source} frame {index} has no positive encoded delay")
            rows.append({
                "index": index, "start_ms": cursor, "delay_ms": delay,
                "alpha_bbox_px": frame.getchannel("A").getbbox(),
            })
            frames.append(frame)
            cursor += delay
    return frames, {"size_px": size, "gif_loop_metadata": loops, "duration_ms": cursor,
                    "last_frame_start_ms": rows[-1]["start_ms"], "frames": rows}


def sampled_rows(rows, duration, samples):
    positions = [round((duration - 1) * i / (samples - 1)) for i in range(samples)]
    return list(dict.fromkeys(max(r["index"] for r in rows if r["start_ms"] <= at) for at in positions))


def make_board(key, frames, rows, indices, path):
    width, height = 202, 193
    cols = 5
    image = Image.new("RGB", (width * cols, height * ((len(indices) + cols - 1) // cols)), "#171d26")
    draw = ImageDraw.Draw(image)
    for slot, index in enumerate(indices):
        x = slot % cols * width
        y = slot // cols * height
        tile = Image.new("RGBA", (width - 8, height - 24), "#353e4d")
        frame = ImageOps.contain(frames[index], (tile.width, tile.height), Image.Resampling.LANCZOS)
        tile.alpha_composite(frame, ((tile.width - frame.width) // 2, (tile.height - frame.height) // 2))
        image.paste(tile.convert("RGB"), (x + 4, y + 4))
        row = rows[index]
        draw.text((x + 7, y + height - 16), f"f{index:03d}  {row['start_ms']/1000:0.3f}s  {key}",
                  fill="#e8eff9")
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, quality=92, subsampling=0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--originals", type=Path, default=ORIGINALS)
    parser.add_argument("--output", type=Path, default=MOTION)
    parser.add_argument("--samples", type=int, default=20)
    parser.add_argument("--all-frames", action="store_true",
                        help="Save every decoded frame in addition to the source-time contact sheets.")
    args = parser.parse_args()
    if args.samples < 2:
        parser.error("--samples must be at least 2")
    missing = [source for _, name in CLIPS
               if not (source := args.originals / f"MCD2_Prime_Enchanter_{name}.gif").is_file()]
    if missing:
        parser.error("Missing original GIFs: " + ", ".join(p.name for p in missing))
    args.output.mkdir(parents=True, exist_ok=True)
    clips = {}
    for key, name in CLIPS:
        source = args.originals / f"MCD2_Prime_Enchanter_{name}.gif"
        frames, entry = read_frames(source)
        indices = sampled_rows(entry["frames"], entry["duration_ms"], args.samples)
        frame_dir = args.output / "frames" / key
        frame_dir.mkdir(parents=True, exist_ok=True)
        saved = list(range(len(frames))) if args.all_frames else []
        for index in saved:
            frames[index].save(frame_dir / f"{index:04d}.png")
        sheet = args.output / "contact_sheets" / f"{key}.jpg"
        make_board(key, frames, entry["frames"], indices, sheet)
        entry.update(source_file=source.name, sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                     sample_indices=indices, saved_indices=saved,
                     contact_sheet=sheet.relative_to(args.output).as_posix())
        clips[key] = entry
        print(f"{key:<16} {len(frames):>4} frames  {entry['duration_ms']/1000:7.3f} s  {entry['size_px']}")
    (args.output / "gif_timing.json").write_text(
        json.dumps({"timing_basis": "encoded GIF frame delays, including the last frame",
                    "clips": clips}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
