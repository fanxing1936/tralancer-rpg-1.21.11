"""归档用户新指向图库的四份原始素材；只写 gallery_followup，不改模型。

读取主会话经原 Wiki 文件页下载的本地文件；保留 Downloads 原件。
Pillow 解码、原字节复制、GIF累计时序抽帧、最近邻研究裁图。
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

REF = Path(__file__).resolve().parent / "heart_of_ender_ref"
OUT = REF / "gallery_followup"
PAGE = "https://minecraft.wiki/w/Dungeons:Arch-Illager/Gallery"
GIF = "MCD_Arch-Illager_Idle_Highblock_Halls_(front_view).gif"
ASSETS = [
    ("MCD_Arch-Illager_Idle_Highblock_Halls_%28front_view%29.gif", GIF,
     "https://minecraft.wiki/images/MCD_Arch-Illager_Idle_Highblock_Halls_%28front_view%29.gif?50ec8&format=original"),
    ("MCD_Arch-Illager.png", "MCD_Arch-Illager.png",
     "https://minecraft.wiki/images/MCD_Arch-Illager.png?a3f08&format=original"),
    ("Arch-Illager_ghost_form_back.png", "Arch-Illager_ghost_form_back.png",
     "https://minecraft.wiki/images/Arch-Illager_ghost_form_back.png?25bdd&format=original"),
    ("Arch-Illager_defeated_in_a_whirlwind_lose_crowns.jpg", "Arch-Illager_defeated_in_a_whirlwind_lose_crowns.jpg",
     "https://minecraft.wiki/images/Arch-Illager_defeated_in_a_whirlwind_lose_crowns.jpg?1dcc7&format=original"),
]
BG = (55, 60, 70, 255)
CROPS = [
    ("render_head_and_crown", "MCD_Arch-Illager.png", [55, 0, 490, 635], "原渲染：头、冠、鼻"),
    ("render_face", "MCD_Arch-Illager.png", [55, 280, 490, 645], "原渲染：L形眉与白眼"),
    ("render_crown", "MCD_Arch-Illager.png", [195, 0, 435, 390], "冠：红色在上，蓝色在下"),
    ("ghost_back_head", "Arch-Illager_ghost_form_back.png", [345, 65, 675, 550], "背面：头后与冠后"),
    ("detached_crown", "Arch-Illager_defeated_in_a_whirlwind_lose_crowns.jpg", [665, 70, 1120, 430], "脱冠：头与冠分离"),
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def jb(doc):
    return (json.dumps(doc, ensure_ascii=False, indent=2)+"\n").encode("utf-8")


def font(size):
    return ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", size)


def png(im):
    stream = io.BytesIO()
    im.save(stream, format="PNG")
    return stream.getvalue()


def cell(im, label, width=500, height=560):
    result = Image.new("RGBA", (width, height), BG)
    ImageDraw.Draw(result).text((12, 10), label, font=font(19), fill="white")
    scale = min((width-20)/im.width, (height-52)/im.height)
    sized = im.convert("RGBA").resize((round(im.width*scale), round(im.height*scale)), Image.Resampling.NEAREST)
    result.alpha_composite(sized, ((width-sized.width)//2, 44+(height-44-sized.height)//2))
    return result


def make_sheet(images, labels, columns, width=500, height=560):
    sheet = Image.new("RGBA", (columns*width, ((len(images)+columns-1)//columns)*height), BG)
    for i, (im, label) in enumerate(zip(images, labels)):
        sheet.alpha_composite(cell(im, label, width, height), (i%columns*width, i//columns*height))
    return sheet.convert("RGB")


def build(download_dir):
    files, originals, metadata, input_hashes = {}, {}, [], {}
    for downloaded, name, url in ASSETS:
        src = download_dir/downloaded
        raw = src.read_bytes()
        input_hashes[str(src)] = sha(raw)
        with Image.open(io.BytesIO(raw)) as check:
            check.verify()
        with Image.open(io.BytesIO(raw)) as im:
            rec = {"file": "original/"+name, "downloaded_path": str(src), "bytes": len(raw), "sha256": sha(raw),
                   "source_page": PAGE, "url": url, "size": list(im.size), "format": im.format, "stored_frame_count": getattr(im, "n_frames", 1)}
            originals[name] = im.convert("RGBA")
            if im.format == "GIF":
                frames, durations, start = [], [], 0
                rows = []
                for index in range(im.n_frames):
                    im.seek(index)
                    frame = im.convert("RGBA")
                    frame.load()
                    duration = im.info.get("duration", 0)
                    if duration <= 0 or duration % 40:
                        raise ValueError(f"GIF延时不适合25fps：{index} {duration}")
                    for ms in range(0, duration, 40):
                        sample_index = len(frames)
                        frames.append(frame.copy())
                        rows.append([sample_index, (start+ms)/1000, index, start/1000, duration/1000])
                    durations.append(duration)
                    start += duration
                rec.update({"frame_durations_ms": durations, "duration_ms": start, "sample_rate_hz": 25,
                            "sample_count": len(frames), "first_and_last_rgba_equal": frames[0].tobytes() == frames[-1].tobytes()})
                for i, frame in enumerate(frames):
                    files[f"frames/front/frame_{i:04d}.png"] = png(frame)
                csvio = io.StringIO(newline="")
                writer = csv.writer(csvio, lineterminator="\n")
                writer.writerow(["sample_index", "time_s", "source_index", "source_start_s", "source_duration_s"])
                writer.writerows(rows)
                files["frames/front/frames.csv"] = csvio.getvalue().encode("utf-8")
                keys = list(range(0, len(frames), 10))
                files["derived/front_key_frames.png"] = png(make_sheet([frames[i] for i in keys],
                    [f"原帧{i:03d} / t={rows[i][1]:.2f}s" for i in keys], 4, 400, 450))
                # Original pixels only. Each crop rect is logged explicitly below.
                front_rect = [65, 0, 435, 335]
                front_keys = [0, 25, 50, 75, 100]
                files["derived/front_head_keys.png"] = png(make_sheet([frames[i].crop(front_rect) for i in front_keys],
                    [f"正面原帧{i:03d} / t={rows[i][1]:.2f}s" for i in front_keys], 3, 500, 500))
                rec["head_key_crops"] = {"source_rect_xyxy": front_rect, "indices": front_keys}
            metadata.append(rec)
        files["original/"+name] = raw

    crops, labels, crop_records = [], [], []
    for ident, name, rect, label in CROPS:
        crop = originals[name].crop(rect)
        files[f"derived/{ident}.png"] = png(crop)
        crops.append(crop)
        labels.append(label)
        crop_records.append({"file": f"derived/{ident}.png", "source_file": "original/"+name,
                             "source_rect_xyxy": rect, "resampling": "crop original pixels; board nearest-neighbor"})
    files["derived/structure_crops.png"] = png(make_sheet(crops, labels, 3, 500, 660))

    undressed = np.asarray(Image.open(REF/"T_ArchIllagerUndressed.png").convert("RGBA"))
    regular = np.asarray(Image.open(REF/"MCD_Arch-Illager_(texture).png").convert("RGBA"))
    region_checks = []
    for label, rect in [("head_north", [6, 6, 18, 13]), ("unassigned_corner", [0, 0, 6, 6]), ("crown", [36, 0, 52, 15])]:
        x0, y0, x1, y1 = rect
        a, b = undressed[y0:y1, x0:x1], regular[y0:y1, x0:x1]
        region_checks.append({"name": label, "source_rect_xyxy": rect, "same_rgba_in_regular_and_undressed": bool(np.array_equal(a, b)),
                              "rgba_sha256": sha(a.tobytes()), "unique_rgba": np.unique(a.reshape(-1, 4), axis=0).tolist()})
    # Exact texture coordinates of the existing north crown face's colored blocks.
    colored_pixels = {}
    for name, rect in [("red", [37, 8, 39, 10]), ("blue", [37, 12, 39, 14])]:
        x0, y0, x1, y1 = rect
        colored_pixels[name] = {"source_rect_xyxy": rect,
            "pixels": [{"xy": [x, y], "rgba": undressed[y, x].tolist()} for y in range(y0, y1) for x in range(x0, x1)]}
    report = {"source_page": PAGE, "source_capture": "root session read original Wiki page, last edited 2026-11-02; downloaded via file-page downloadMedia",
              "original_files": metadata, "crop_regions": crop_records, "texture_region_comparison": region_checks,
              "crown_north_uv_colored_pixels": colored_pixels,
              "verification": "Pillow format/decode validation plus newly computed local SHA-256; no publisher checksum supplied",
              "source_assets_are": "PNG/JPG renders/screenshots and GIF, not downloaded 3D geometry or rig",
              "model_changes": "none"}
    files["validation.json"] = jb(report)
    rows = [f"| `{r['file']}` | {r['bytes']} | `{r['sha256'][:16]}` | <{PAGE}> | <{r['url']}> |" for r in metadata]
    sources = "# 大灾厄村民图库补充素材来源\n\n原作：Minecraft Dungeons 的 Arch-Illager（Mojang Studios），版权归 Mojang 所有。\n\n"
    sources += f"页面：<{PAGE}>（主会话直接读取原页，页面最后编辑日期为2026-11-02）。\n\n"
    sources += "四文件由主会话经原 Wiki 文件页面下载，非旧镜像；本脚本仅复制原字节并保留 Downloads 原件。GIF归档名将URL编码括号恢复为实际括号。\n\n本项目非商业，与Mojang无关联。完整性指本地解码/格式与自算SHA校验，没有发行者校验值可供比对。\n\n## 原始素材\n\n"
    sources += "| 文件 | 字节 | SHA-256（前 16 位） | 来源页面 | 文件地址 |\n|---|---|---|---|---|\n"+"\n".join(rows)+"\n\n"
    sources += "## 由此派生（不是原始素材）\n\n| 文件 | 说明 |\n|---|---|\n"
    sources += "| `frames/front/` | 按累计帧延时25fps抽取的101帧PNG及时间CSV；实际4.04秒，未删除闭合帧 |\n"
    sources += "| `derived/front_key_frames.png`、`front_head_keys.png` | 关键原帧与头部裁图；只最近邻缩放和灰底排版 |\n"
    sources += "| `derived/structure_crops.png`及各裁图 | 新渲染、背面、脱冠截图的局部；坐标见validation.json |\n"
    sources += "| `validation.json` | 原件字节/hash/尺寸/完整GIF时序、源裁图坐标及旧贴图逐像素比较 |\n"
    sources += "| `GALLERY_REVIEW.md` | 人工查阅结论、可用证据与不能证明的边界；不是模型或动作修改 |\n"
    sources += "\n对照使用的既有原始64×64贴图位于父目录，来源和SHA见[原始素材清单](../SOURCES.md)。本次未下载旧镜像Arch-IllagerFace.png，也未把它认定为脸部UV。\n"
    files["SOURCES.md"] = sources.encode("utf-8")
    files["GALLERY_REVIEW.md"] = """# 大灾厄村民图库补充核对

四份新原图已复制到 `original/`，Downloads 原件保留，副本字节与来源文件完全相同。这里只做素材研究，没有修改模型、图集、骨骼、动作或游戏实例。

## 来源与完整性

本次依据主会话直接读取的 [原图库](https://minecraft.wiki/w/Dungeons:Arch-Illager/Gallery)（页面最后编辑于2026-11-02）与原 Wiki 文件页下载；不以旧镜像的文件名代替现页。四份文件通过 Pillow verify/解码，完整 SHA-256 与字节见 [validation.json](validation.json)，署名和原始下载地址见 [SOURCES.md](SOURCES.md)。这些校验是本地新算值，没有发行者校验值可比对。

| 文件 | 实测 | 用途 |
|---|---|---|
| `MCD_Arch-Illager.png` | 666×999 PNG | 头、鼻、粗眉、眼白、冠正面/侧面与冠顶轮廓 |
| `MCD_Arch-Illager_Idle_Highblock_Halls_(front_view).gif` | 500×500，101帧，每帧40ms | 正面眉眼、鼻、冠的相对布局；并非体内Docile动作 |
| `Arch-Illager_ghost_form_back.png` | 1073×846 PNG | 冠后、后脑及后衣片；含发光/粒子遮挡 |
| `Arch-Illager_defeated_in_a_whirlwind_lose_crowns.jpg` | 1920×1080 JPEG | 冠与头实际分离、露出的头顶；强紫色光照 |

GIF实际播放时长为 **4.04秒**。第0帧与第100帧解码RGBA完全相同；第100帧起点为4.00秒，所以“动作闭合端点4.00秒”和“文件含末端40ms的4.04秒”需区分。本次保留101帧，不为了凑4秒删除末帧。所有PNG与CSV按累计帧时长对应，时间为0.00..4.00秒。

图库及本次获取内容是渲染图、GIF与截图，**没有获得可下载3D几何、骨架或原始UV网格文件**。本次原页Textures未出现 `Arch-IllagerFace.png`，未下载或沿用旧镜像的这一条目，也不把墙画或脸图标认作模型贴图。

## 已看图可确认

1. **脸部语义需要纠正。** 静态渲染与正面GIF都显示，两条L形深色块是粗眉，其下细白条是眼白，长鼻位于两眼之间。它们与末影之心原渲染里的紫色L及白条形态一致，因此旧记录里的“L形紫眼/白口”不应继续作为建模语义。白条不是已经识别的嘴。
2. **冠的正背朝向可以用纹样锚定。** 正面是上红、下蓝；现原64贴图的冠正面候选 `[36,4,40,15)` 内，红色2×2块位于 `[37,8,39,10)`，蓝色2×2块位于 `[37,12,39,14)`。新渲染支持这一前向映射，而背面截图中没有这两个红蓝块。这里只确认可见纹样方向，不把视图比例当官方几何尺寸。
3. **冠与头是可分开的结构。** 脱冠截图明确显示冠离开头顶，露出的头顶仍是灰色皮肤；高质量渲染也能看到冠顶有起伏、内侧和空隙。它支持分别核对头/冠，不足以恢复原冠壁厚、顶齿真实网格或全部隐藏面。
4. **灰皮肤本体与眉眼应分开核对。** 当前模型 `inner_head_core` 的north UV `[6,6,18,13)` 只有三种灰色，不能独自呈现新图中高对比粗眉和白眼。当前没有独立眉/眼元素。新图能证实“当前缺了可见眉眼信息”，但单凭这些渲染不能区分原作是共面UV分片、独立薄面还是另一种网格/材质布局；不能直接宣称必须新增厚眉几何。

## 与本地原贴图逐像素对照

以下区域在 `T_ArchIllagerUndressed.png` 与 `MCD_Arch-Illager_(texture).png` 之间RGBA完全相同，已在本次重新计算验证：

| 区域 | 原64×64坐标，右下开区间 | 能支持什么 |
|---|---|---|
| 当前头正面 | `[6,6,18,13)` | 普通大灾厄村民的新正面图可用于灰纹方向核对 |
| 未分配角落 | `[0,0,6,6)` | 可以研究与粗眉/眼的关系，不能整块直接认定为完整脸 |
| 冠区域 | `[36,0,52,15)` | 穿着差异不妨碍冠纹样方向核对 |

角落 `(3,5)`、`(4,5)` 在辅助shadow贴图被单独标记，`(5,5)` 是白色源像素；事实与既有 [FACE_FORENSICS.md](../m3_material/FACE_FORENSICS.md) 一致。具体眉/眼到头面的分格与像素采样布局由另行的独立UV审计负责，本报告不把整块6×6镜像铺脸当作已确认方案。仅提高当前三灰色对比，也无法凭空得到白色眼纹。

## 图像与复现

- [正面关键原帧](derived/front_key_frames.png)：0.00、0.40…4.00秒；保留椅子/权杖以辨别该动画来源。
- [正面头部关键裁图](derived/front_head_keys.png)：第0/25/50/75/100帧，原图裁框 `[65,0,435,335)`。
- [结构重点并排](derived/structure_crops.png)：原渲染、冠正面、背面与脱冠；各裁框详见validation.json。
- [101帧时间映射](frames/front/frames.csv)：sample_index、time_s、source_index、source_start_s、source_duration_s。

图像派生只有裁切、灰底合成和最近邻缩放，没有重新着色、补画眉眼或增强发光。复现：在仓库目录运行 `python -X utf8 _tools/heart_of_ender_gallery_followup.py`，默认读取 `C:/Users/zhaoy/Downloads` 四原件，只写本目录。

## 边界

新素材中的普通版穿衣、持杖并坐在王座上，不能把它的衣袖、腿形或坐姿直接搬进体内小人。背面是幽灵形态、脱冠图受强紫色光和JPEG影响，不能从其屏幕颜色反推准确原材质RGB。现没有原始geometry或rig，绝对尺寸、隐藏面UV、冠顶厚度和眉眼网格仍需明确标为推断。外壳及已接受动作未改，本报告不是新模型验收。

原始素材版权属于Mojang Studios；本项目非商业，与Mojang无关联。
""".encode("utf-8")
    for path, digest in input_hashes.items():
        if sha(Path(path).read_bytes()) != digest:
            raise ValueError("Downloads原件在处理期间改变")
    return files, report


def write_owned(files):
    marker = OUT/"GENERATED_FILES.json"
    previous = json.loads(marker.read_text(encoding="utf-8"))["files"] if marker.exists() else {}
    for name in files:
        path = (OUT/name).resolve()
        if OUT.resolve() not in path.parents:
            raise ValueError("输出越界")
        if path.exists() and sha(path.read_bytes()) != previous.get(name):
            raise ValueError(f"拒绝覆盖手改或未登记文件：{path}")
    for name, raw in files.items():
        path = OUT/name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    marker.write_bytes(jb({"generator": Path(__file__).name, "files": {n: sha(v) for n, v in sorted(files.items())}}))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--downloads", type=Path, default=Path("C:/Users/zhaoy/Downloads"))
    args = ap.parse_args()
    files, report = build(args.downloads)
    write_owned(files)
    print(json.dumps({"output": str(OUT), "generated_files": len(files), "originals": report["original_files"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
