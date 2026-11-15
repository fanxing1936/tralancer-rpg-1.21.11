"""Crop the exact published Prime Enchanter reference pixels for static review."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


OUT = Path(__file__).resolve().parent
REF = OUT.parent.parent
INTRO = "m1/motion/gameplay/intro"
VIDEO = "https://www.youtube.com/watch?v=KorV2SgmFWU"
WIKI = "https://minecraft.wiki/w/Dungeons_II:Prime_Enchanter"
META = "https://metabot.gg/en/minecraft-dungeons-2/bosses/the-prime-enchanter"


def entry(name, label, source, box, view, pose, notes, link, **extra):
    return {"name": name, "label": label, "source": source, "crop_xyxy": box,
            "view": view, "pose": pose, "notes": notes, "source_url": link, **extra}


REFERENCES = (
    entry("guard_3q", "Guard / front three-quarter", "originals/MCD2_Prime_Enchanter_Render.png",
          (148, 19, 767, 984), "前侧四分之三，高于头顶", "双拳抬起的静态拳架",
          "与本次模型的拳架最接近。全身完整且背景透明，便于核对头、肩、拳、腿的相对比例。"
          "画面仍有三维照明，摄影机参数未知。", WIKI, role="primary_guard"),
    entry("neutral_front", "Neutral / near front", "originals/Prime_Enchanter_render.webp",
          (96, 15, 417, 498), "近正面，稍转侧", "双臂自然下垂的中立姿",
          "画面干净且保留头脚。核对正面几何、胸衣不对称线条与腿面。"
          "来源清单按第三方静态渲染注明，拳架与披风张角不可直接比较。", META, role="geometry_front"),
    entry("guard_gif", "Idle / source frame 0", "m1/motion/frames/idle/0000.png",
          (0, 0, 288, 464), "前侧四分之三", "Idle 起始双拳架",
          "与主渲染的拳架、视角相近。源 GIF 左缘已贴近轮廓，未人为补像素。",
          WIKI, gif="originals/MCD2_Prime_Enchanter_Idle.gif", frame=0, seconds=0.0, role="guard_crosscheck"),
    entry("front_guard", "Cutscene / near front / 13.000 s", f"{INTRO}/f00780.png",
          (665, 169, 1245, 904), "近正面", "起身后右拳靠脸，左臂横挡",
          "保留原画中的蓝色粒子和场景照明。用于胸衣正面、头鼻及肩甲核对。"
          "头顶与脚已贴近原视频画框。", VIDEO, frame=780, seconds=13.0, role="game_front"),
    entry("side_guard", "Cutscene / side-front / 20.500 s", f"{INTRO}/f01230.png",
          (410, 164, 1275, 906), "侧前接近侧面", "双拳举起，黄拳横在胸前，青拳斜举",
          "核对鼻与头盔侧片、肩膀和拳套厚度。脚及头顶部分由原镜头裁切。"
          "透视与照明来自游戏过场。", VIDEO, frame=1230, seconds=20.5, role="game_side"),
    entry("side_rear", "Cutscene / side-rear / 15.500 s", f"{INTRO}/f00930.png",
          (774, 238, 1374, 886), "侧偏背", "迈步，黄拳前伸，披风下摆沿后侧落下",
          "全身较完整，可核对侧肩、分条披风和腿脚；与本次静态拳架姿势不同。",
          VIDEO, frame=930, seconds=15.5, role="game_side_full"),
    entry("rear", "Cutscene / near rear / 15.000 s", f"{INTRO}/f00900.png",
          (577, 180, 1447, 881), "近背面，少量侧面", "转身迈步，披风条带横向甩开",
          "最清楚的背面布料证据。核对披风条带内外侧和头巾带的接点，转身造成的张角不当作静态夹角。",
          VIDEO, frame=900, seconds=15.0, role="game_rear"),
    entry("emissive", "Cutscene / fist lighting / 14.500 s", f"{INTRO}/f00870.png",
          (570, 167, 1325, 915), "近正面", "转身落稳后举拳，双拳发光",
          "角色右拳为青、左拳为黄，额纹为青、眼睛为白。保留火花和光晕，供核对颜色分工。",
          VIDEO, frame=870, seconds=14.5, role="emissive_color"),
    entry("eyes", "Cutscene / eye detail / 10.300 s", f"{INTRO}/f00618.png",
          (245, 194, 1680, 888), "近正面特写", "睁眼时头部接近正向",
          "用于核对眉眼与长鼻。游戏中此时白眼受发光照亮，肤色受环境光影响。",
          VIDEO, frame=618, seconds=10.3, role="eyes"),
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def create_crops():
    records = {}
    for spec in REFERENCES:
        name = spec["name"]
        source = REF / spec["source"]
        result = OUT / f"{name}.png"
        with Image.open(source) as source_image:
            left, top, right, bottom = spec["crop_xyxy"]
            if not (0 <= left < right <= source_image.width and 0 <= top < bottom <= source_image.height):
                raise ValueError(f"Crop outside source: {source}")
            crop = source_image.crop(spec["crop_xyxy"])
            crop.save(result)
            with Image.open(result) as check:
                assert check.mode == crop.mode and check.tobytes() == crop.tobytes(), name
            records[name] = {**spec, "image": result.name, "source_size": list(source_image.size),
                             "crop_size": list(crop.size), "source_sha256": digest(source),
                             "crop_sha256": digest(result)}
    return records


def make_board(records):
    width, height, cols = 360, 327, 3
    board = Image.new("RGB", (width * cols, height * ((len(records) + cols - 1) // cols)), "#1e2733")
    draw = ImageDraw.Draw(board)
    for i, entry in enumerate(records.values()):
        x, y = i % cols * width, i // cols * height
        with Image.open(OUT / entry["image"]) as raw:
            frame = ImageOps.contain(raw.convert("RGBA"), (width - 16, height - 32),
                                     Image.Resampling.LANCZOS)
            board.paste(frame, (x + (width - frame.width) // 2, y + 4), frame)
        draw.text((x + 9, y + height - 22), entry["label"], fill="#eaf2ff")
    board.save(OUT / "REFERENCE_BOARD.jpg", quality=94, subsampling=0)


def make_notes(records):
    lines = [
        "# 首席附魔师静态模型对照素材",
        "",
        "优先用 Wiki 的近侧四分之三拳架图对照模型的头、肩、拳、腿与披风。近正面使用第三方静态渲染及原作过场，"
        "侧面和背面补充证据取自原作过场。场景镜头有透视、照明和姿态差，模型的正交预览用于检查几何。",
        "",
        "单张 PNG 裁剪保留解码后的原始像素和 alpha。总览板为了排版进行缩放，透明图置于统一底色。",
        "",
        "| 参考图 | 原图 | 画面或时间 | 证据范围 |",
        "|---|---|---|---|",
    ]
    for spec in records.values():
        seconds = f" {spec['seconds']:.3f} s" if "seconds" in spec else ""
        source = f"../../{spec['source']}"
        lines.append(f"| [{spec['name']}]({spec['image']}) | [原图]({source}) |"
                     f" {spec['view']}，{spec['pose']}{seconds} | {spec['notes']} |")
    lines.extend(["", "[九张参考图总览](REFERENCE_BOARD.jpg) · [裁剪坐标与源哈希](reference_metadata.json)",
                  "", "录像由 Video Game News 发布。游戏角色与画面版权归 Mojang 等权利人所有。"
                  "本项目仅作非商业模型复刻参考，与 Mojang 无关联。", ""])
    (OUT / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    records = create_crops()
    make_board(records)
    make_notes(records)
    (OUT / "reference_metadata.json").write_text(json.dumps(
        {"coordinates": "source pixel xyxy, right and bottom excluded",
         "single_reference_edit": "lossless crop of decoded source pixels",
         "references": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
