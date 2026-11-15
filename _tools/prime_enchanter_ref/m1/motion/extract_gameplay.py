"""Extract original-frame references from Video Game News' public boss recording."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw
from imageio_ffmpeg import get_ffmpeg_exe


MOTION = Path(__file__).resolve().parent
SOURCE_URL = "https://www.youtube.com/watch?v=KorV2SgmFWU"
SOURCE_CREATOR = "Video Game News"
FPS = 60


def extract(source, at):
    args = [get_ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-ss", f"{at:.6f}", "-i",
            str(source), "-map", "0:v:0", "-frames:v", "1", "-threads", "1",
            "-c:v", "png", "-f", "image2pipe", "-"]
    raw = subprocess.run(args, check=True, capture_output=True).stdout
    image = Image.open(io.BytesIO(raw)).convert("RGB")
    if image.size != (1920, 1080):
        raise ValueError(f"Reference capture must be 1920x1080, got {image.size}")
    return image


def make_board(images, path):
    cols = 4
    w, h = 320, 180
    board = Image.new("RGB", (cols * w, ((len(images) + cols - 1) // cols) * (h + 18)), "#172130")
    draw = ImageDraw.Draw(board)
    for i, (at, image) in enumerate(images):
        x, y = i % cols * w, i // cols * (h + 18)
        board.paste(image.resize((w, h), Image.Resampling.LANCZOS), (x, y))
        draw.text((x + 5, y + h + 2), f"{at:07.3f}s  KorV2SgmFWU", fill="#f2f7ff")
    board.save(path, quality=92, subsampling=0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--times", nargs="+", type=float, required=True)
    parser.add_argument("--name", default="intro")
    args = parser.parse_args()
    with args.source.open("rb") as stream:
        video_sha = hashlib.file_digest(stream, "sha256").hexdigest()
    frame_dir = MOTION / "gameplay" / args.name
    frame_dir.mkdir(parents=True, exist_ok=True)
    images = []
    frame_records = []
    for at in args.times:
        index = round(at * FPS)
        at = index / FPS
        image = extract(args.source, at)
        target = frame_dir / f"f{index:05d}.png"
        image.save(target)
        images.append((at, image))
        frame_records.append({
            "time_seconds": at, "nominal_frame": index,
            "file": target.relative_to(MOTION).as_posix(),
            "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        })
    make_board(images, frame_dir / "contact.jpg")
    (frame_dir / "source.json").write_text(json.dumps({
        "url": SOURCE_URL, "creator": SOURCE_CREATOR, "video_sha256": video_sha,
        "stream": {"itag": 303, "size_px": [1920, 1080], "fps": FPS, "audio": False},
        "frames": frame_records,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
