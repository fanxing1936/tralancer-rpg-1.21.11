# -*- coding: utf-8 -*-
"""篡夺者战的特效素材，取自 Minecraft Dungeons 原作（docs/USURPER-DESIGN.md 第 6 节，用户要求优先用原作素材）。

    python add_usurper_fx_art.py ../resourcepack

源图在 _tools/usurper_fx_ref/（从本体导出，只读引用）：
  T_CastingTotem.png   灵魂图腾的遮罩贴图：顶上一排 14 个标准银河字母符文（附魔台那种），中央一个圆圈套三角的法阵。
                       白线黑底，原作在材质里加色叠加。
  fang/                唤魔者尖牙（SK_Evoker_Fang 的静止姿态），经 dungeons_conversion/generic.py 转换。
  crown/ pillar/ totem/ 二阶段的原作道具，同样经 generic.py 转换（2026-11-14）：
                       crown  商人的王冠 SM_Crown（贴图是豪华商人 T_Villager_LuxuryMerchant），按篡夺白金重着色；
                       pillar 地卜师石柱 SK_Geomancer_Pillar，按篡夺白金重着色，作神力超载的圣坛；
                       totem  不死图腾 SK_TotemOfUnDying，原色，致命一击被死亡保护挡下时转一下再碎。
  vfx/                 原作通用特效贴图（Effects/Materials/…）：一阶段的冲击环、星芒、神光等，
                       二阶段的电弧 T_ElectricArcs、直闪电 T_ElectricStraight、弧光 T_Slash_Grayscale /
                       T_Combat_LongSlash_GrayScale、方形冲击环 T_fullsquareEdgeless_15_spritesheet（原作
                       SM_SquareDonut 的贴图序列）、虚空风暴的闪电网 T_LightningSpline_1M。

这里把遮罩切成贴片：黑转透明，白线留白，颜色由物品染色（custom_model_data 第 0 号颜色）在运行时给。
贴片缩到 16×16（符文）或 32×32（法阵），按用户 2026-11-08 的要求，特效贴图只用 16 或 32 像素。
所罗门封印的六芒星就是原作这个三角法阵叠上转了 180° 的自己。

物品模型都是一张双面的发光平面（light_emission 15），中心在原点，平放或竖放由展示实体的变换决定。
"""
import io
import json
import os
import sys

import numpy as np
from PIL import Image

import display_mob as dm

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "usurper_fx_ref")
KEY = "usurper_fx"


def mask(img):
    """White-on-black mask -> white with alpha (the line strength)."""
    a = np.array(img.convert("L"), float)
    out = np.zeros(a.shape + (4,), np.uint8)
    out[..., :3] = 255
    out[..., 3] = np.clip(a, 0, 255).astype(np.uint8)
    return Image.fromarray(out)


def shrink(img, size):
    """Line art down to `size`: keep a texel if any source texel under it is lit (thin lines survive),
    then make it fully opaque (pixel art, no soft edges)."""
    a = np.array(img)[..., 3].astype(float)
    h, w = a.shape
    out = np.zeros((size, size, 4), np.uint8)
    for y in range(size):
        for x in range(size):
            block = a[y * h // size:(y + 1) * h // size, x * w // size:(x + 1) * w // size]
            if block.size and block.max() > 96:
                out[y, x] = (255, 255, 255, 255)
    return Image.fromarray(out)


def runes(src):
    """The 14 runes along the top: split on empty columns, each centred on a 16x16 tile."""
    strip = np.array(src.convert("L"))[:24]
    cols = strip.max(axis=0) > 60
    spans, start = [], None
    for x, on in enumerate(list(cols) + [False]):
        if on and start is None:
            start = x
        elif not on and start is not None:
            spans.append((start, x))
            start = None
    tiles = []
    for x0, x1 in spans:
        rows = np.where(strip[:, x0:x1].max(axis=1) > 60)[0]
        crop = src.crop((x0, rows.min(), x1, rows.max() + 1))
        m = mask(crop)
        tile = Image.new("RGBA", (16, 16))
        # source runes are about 10 x 14 px: they already fit; keep them crisp
        cw, ch = m.size
        s = min(1.0, 14.0 / max(cw, ch))
        if s < 1:
            m = m.resize((max(1, int(cw * s)), max(1, int(ch * s))), Image.NEAREST)
        arr = np.array(m); arr[..., 3] = np.where(arr[..., 3] > 96, 255, 0); m = Image.fromarray(arr)
        tile.alpha_composite(m, ((16 - m.width) // 2, (16 - m.height) // 2))
        tiles.append(tile)
    return tiles


def sigil(src):
    """The circle-and-triangle in the middle of the casting totem texture."""
    a = np.array(src.convert("L"))
    a[:40] = 0                                   # drop the rune strip
    ys, xs = np.where(a > 60)
    box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
    side = max(box[2] - box[0], box[3] - box[1])
    cx, cy = (box[0] + box[2]) // 2, (box[1] + box[3]) // 2
    crop = src.crop((cx - side // 2, cy - side // 2, cx - side // 2 + side, cy - side // 2 + side))
    return mask(crop)


def plane_model(texture, glow=True):
    """A ground decal: one up-facing plane through the model centre (item_display shades every other
    direction; up is full bright, display-render-facts)."""
    face = {"uv": [0, 0, 16, 16], "texture": "#0", "tintindex": 0}
    el = {"from": [0, 8, 0], "to": [16, 8, 16], "faces": {"up": face}, "shade": False}
    if glow:
        el["light_emission"] = 15
    return {"textures": {"0": texture, "particle": texture}, "elements": [el]}


def beam_model(texture):
    """A unit box, every face the scrolling beam texture; scaled along z to the beam's length."""
    face = {"uv": [0, 0, 16, 16], "texture": "#0", "tintindex": 0}
    faces = dict((k, dict(face)) for k in ("north", "south", "east", "west", "up", "down"))
    return {"textures": {"0": texture, "particle": texture},
            "elements": [{"from": [0, 0, 0], "to": [16, 16, 16], "light_emission": 15, "shade": False, "faces": faces}]}


# ---------------------------------------------------------------------------
# 原作通用特效贴图（Effects/Materials/…，usurper_fx_ref/vfx/，2026-11-14 导出）。
# 都是白色 + 透明度，运行时染色。两种缩法：
#   线稿（像素环、六边形、裂纹、爆环）：源像素有亮就留，细线不断，全不透明；
#   柔光（光晕盘、神光、漩涡、光束）：盒式滤波，保留透明度渐变。
# ---------------------------------------------------------------------------
VFX = os.path.join(REF, "vfx")
FONT_NAME = "usurper_fx"
GLYPH_BASE = 0xE300


def vfx(name):
    return Image.open(os.path.join(VFX, name + ".png")).convert("RGBA")


def cells(im, size):
    """Frames of a sheet laid out in `size` cells, row by row."""
    out = []
    for r in range(im.height // size):
        for c in range(im.width // size):
            out.append(im.crop((c * size, r * size, (c + 1) * size, (r + 1) * size)))
    return out


def line_art(im, size, threshold=60):
    """Keep a texel if any source texel under it is lit; white, opaque."""
    a = np.array(im)[..., 3].astype(float)
    h, w = a.shape
    out = np.zeros((size, size, 4), np.uint8)
    for y in range(size):
        for x in range(size):
            block = a[y * h // size:(y + 1) * h // size, x * w // size:(x + 1) * w // size]
            if block.size and block.max() > threshold:
                out[y, x] = (255, 255, 255, 255)
    return Image.fromarray(out)


def soft(im, size, gain=1.0):
    """Box filter onto the grid, alpha kept (scaled by gain); white."""
    small = im.resize((size, size), Image.BOX)
    a = np.array(small).astype(float)
    out = np.zeros((size, size, 4), np.uint8)
    out[..., :3] = 255
    out[..., 3] = np.clip(a[..., 3] * gain, 0, 255).astype(np.uint8)
    return Image.fromarray(out)


def square(im):
    """Pad to a square around the drawn part."""
    box = im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    im = im.crop(box)
    side = max(im.size)
    canvas = Image.new("RGBA", (side, side))
    canvas.paste(im, ((side - im.width) // 2, (side - im.height) // 2))
    return canvas


def glyph_frames():
    """name -> list of 16 or 32 px frames (font glyphs: unlit, tinted by the text colour)."""
    runes_ = runes(Image.open(os.path.join(REF, "T_CastingTotem.png")).convert("RGBA"))
    circle = cells(vfx("T_Circle_Full_15_spritesheet"), 16)[:4]
    dissolve = cells(vfx("T_fullcircle_dissolvedArc_15_spritesheet"), 16)[:6]
    stars = cells(vfx("T_Stars_16"), 16)
    rays = cells(vfx("T_GodRayLight"), 128)
    straight = vfx("T_ElectricStraight")
    return {
        "rune": runes_,                                                    # 附魔台符文
        "pop": [line_art(f, 16) for f in circle + dissolve],               # 像素小冲击环：长大 4 帧，碎散 6 帧
        "burst": [line_art(f, 32) for f in cells(vfx("T_fullcircle_explosion_64_spritesheet"), 64)],
        "star": [soft(f, 16, 1.3) for f in stars],                         # 四种星芒
        "ray": [soft(f, 32, 1.1) for f in rays],                           # 四种神光
        # 二阶段（篡夺白金）
        "spark": [line_art(f, 16, 40) for f in cells(vfx("T_ElectricArcs"), 32)],    # 十六种电弧
        "bolt": [bolt(straight.crop((c * 16, 0, c * 16 + 16, 128))) for c in range(4)],   # 四道竖直闪电
        "slash": [soft(square(vfx(n)), 32, 1.4) for n in ("T_Combat_LongSlash_GrayScale", "T_Slash_Grayscale")],
    }


def bolt(column):
    """A 16x128 lightning column -> 32x32: the bolt kept whole as an 8x32 line, centred (the glyph is
    stretched tall at run time)."""
    a = np.array(column)[..., 3]
    out = np.zeros((32, 32, 4), np.uint8)
    for y in range(32):
        for x in range(8):
            if a[y * 4:(y + 1) * 4, x * 2:(x + 1) * 2].max() > 40:
                out[y, 12 + x] = (255, 255, 255, 255)
    return Image.fromarray(out)


def decals():
    """name -> 32 px ground decal."""
    burst = cells(vfx("T_fullcircle_explosion_64_spritesheet"), 64)
    out = {
        "hexagon": line_art(vfx("T_HollowHexagonClean"), 32),
        "swirl": soft(vfx("T_MagicSymbolHiRes"), 32, 1.25),
        "glow": soft(vfx("T_MysteriousShapedCirclePixelated"), 32, 0.75),
        "ring": line_art(vfx("T_PixelHollowRadial_32"), 32),
        "cracks": line_art(vfx("T_Cracks"), 32, 40),
        "crescent": soft(square(vfx("T_Combat_Stab_Grayscale")), 32, 1.4),
    }
    for i, f in enumerate(burst):
        out["shock_%d" % i] = line_art(f, 32)
    # 二阶段：原作方形冲击环（SM_SquareDonut 的序列，16 px）与虚空风暴的闪电网
    for i, f in enumerate(cells(vfx("T_fullsquareEdgeless_15_spritesheet"), 16)):
        out["sq_%d" % i] = line_art(f, 16)
    out["storm"] = line_art(mask(vfx("T_LightningSpline_1M").crop((0, 0, 128, 128))), 32, 70)    # 黑底白线：先按亮度转透明
    return out


def bolt_strip(frames=4):
    """The authority line: the four straight bolts laid along u (the beam's length), 32x32 each, one
    frame a tick -> it flickers between them."""
    straight = vfx("T_ElectricStraight")
    strip = np.zeros((32 * frames, 32, 4), np.uint8)
    for f in range(frames):
        col = np.array(straight.crop((f * 16, 0, f * 16 + 16, 128)))[..., 3]
        for y in range(32):            # along the bolt -> u
            for x in range(8):         # across -> v, centred
                if col[y * 4:(y + 1) * 4, x * 2:(x + 1) * 2].max() > 40:
                    strip[f * 32 + 12 + x, y] = (255, 255, 255, 255)
    return Image.fromarray(strip)


def cross_beam_model(texture):
    """Two crossed planes along z (a vertical one and a flat one), texture u along z on both; length is
    the display's z scale.  Lightning reads from any side, unlike a box whose faces map u differently."""
    v = {"uv": [0, 0, 16, 16], "texture": "#0", "tintindex": 0}
    flat = dict(v, rotation=90)
    return {"textures": {"0": texture, "particle": texture}, "elements": [
        {"from": [8, 0, 0], "to": [8, 16, 16], "light_emission": 15, "shade": False,
         "faces": {"east": dict(v), "west": dict(v)}},
        {"from": [0, 8, 0], "to": [16, 8, 16], "light_emission": 15, "shade": False,
         "faces": {"up": dict(flat), "down": dict(flat)}}]}


def beam_strip(frames=8):
    """The Enchanter's beam material scrolls cloud noise along the beam (MI_EnchantedBeam -> T_Clouds_64):
    32x32 frames of that noise, shifted a step each, stacked into an .mcmeta animation."""
    noise = np.array(vfx("T_Clouds_64").resize((32, 32), Image.BOX))[..., 0].astype(float) / 255.0
    strip = np.zeros((32 * frames, 32, 4), np.uint8)
    for f in range(frames):
        n = np.roll(noise, f * 4, axis=0)
        strip[f * 32:(f + 1) * 32, :, :3] = 255
        strip[f * 32:(f + 1) * 32, :, 3] = np.clip((0.35 + 0.65 * n) * 235, 0, 255).astype(np.uint8)
    return Image.fromarray(strip)


def glyph_table():
    """name -> (first code point, size, frame count), in a fixed order shared with add_usurper_boss.py."""
    table, code = {}, GLYPH_BASE
    sizes = {"rune": 16, "pop": 16, "burst": 32, "star": 16, "ray": 32, "spark": 16, "bolt": 32, "slash": 32}
    counts = {"rune": 14, "pop": 10, "burst": 8, "star": 4, "ray": 4, "spark": 16, "bolt": 4, "slash": 2}
    for name in ("rune", "pop", "burst", "star", "ray", "spark", "bolt", "slash"):
        table[name] = (code, sizes[name], counts[name])
        code += 16
    return table


def glyph_text(name, frame=0):
    return chr(glyph_table()[name][0] + frame)


def write_item(rp, name, model):
    dm.wj(os.path.join(rp, "assets", "rpg", "models", KEY, name + ".json"), model)
    dm.wj(os.path.join(rp, "assets", "rpg", "items", KEY, name + ".json"), {
        "model": {"type": "minecraft:model", "model": "rpg:%s/%s" % (KEY, name),
                  "tints": [{"type": "minecraft:custom_model_data", "index": 0, "default": 16777215}]}})


# 篡夺白金（设计稿第 6 节；rpg_ui_style.WHITE_GOLD）：亮、中、深
WHITE_GOLD = ((0xFF, 0xF6, 0xDC), (0xF0, 0xCF, 0x7A), (0xB8, 0x90, 0x2F))


def white_gold(png):
    """Recolour by luminance onto the white-gold ramp (deep -> mid -> light); alpha kept."""
    im = Image.open(io.BytesIO(png)).convert("RGBA")
    a = np.array(im).astype(float)
    lum = (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]) / 255.0
    seen = a[..., 3] > 0
    lo, hi = np.percentile(lum[seen], (5, 95)) if seen.any() else (0.0, 1.0)
    t = np.clip((lum - lo) / max(hi - lo, 1e-6), 0, 1)[..., None]
    deep, mid, light = (np.array(c, float) for c in reversed(WHITE_GOLD))
    rgb = np.where(t < 0.5, deep + (mid - deep) * (t * 2), mid + (light - mid) * (t * 2 - 1))
    out = np.concatenate([rgb, a[..., 3:4]], axis=2).clip(0, 255).astype(np.uint8)
    buf = io.BytesIO()
    Image.fromarray(out).save(buf, "PNG")
    return buf.getvalue()


# 道具：名称 -> (锚点, 是否重着色为白金, 是否整体发光)。
# 都按 Dungeons 原尺寸换算：显示缩放 PROP_SCALE 时 1 厘米 = 0.01 格（同附魔师的 model_scale）。
PROPS = {"fang": ("base", False, False), "crown": ("center", True, True), "pillar": ("base", True, False),
         "totem": ("base", False, False)}
PROP_SCALE = 8.33


def prop_model(rp, name, anchor, recolour, glow):
    """A converted Dungeons prop as one item model, tinted through custom_model_data colour 0."""
    ref = os.path.join(REF, name)
    parts = json.load(open(os.path.join(ref, "parts.json"), encoding="utf-8"))
    bones = [b for p in parts for b in p["bones"]]
    mob = dm.Mob(key=KEY, label=name, generator="add_usurper_fx_art.py",
                 bbmodel=os.path.join(ref, "usurper_%s.bbmodel" % name), parts=[(name, bones)],
                 glow=set(bones) if glow else set(),
                 seat=0, tag="rpg.usfx", score="rpg_usfx", clips=[], face_rotation=True)
    mob.paths(rp, rp)
    mob.tex = "rpg:item/%s/%s" % (KEY, name)
    bones_, png, res = dm.load_bbmodel(mob)
    model, _k = dm.part_model(mob, bones_, name, bones, res)
    if anchor == "base":
        low = min(min(e["from"][1], e["to"][1]) for e in model["elements"])
        for e in model["elements"]:
            e["from"][1] = round(e["from"][1] + 8 - low, 4)
            e["to"][1] = round(e["to"][1] + 8 - low, 4)
            if "rotation" in e:
                e["rotation"]["origin"][1] = round(e["rotation"]["origin"][1] + 8 - low, 4)
    if recolour:
        png = white_gold(png)
    tex = os.path.join(rp, "assets", "rpg", "textures", "item", KEY, name + ".png")
    with open(tex, "wb") as fh:
        fh.write(png)
    write_item(rp, name, model)
    return len(model["elements"])


def main():
    rp = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "resourcepack")
    tex_dir = os.path.join(rp, "assets", "rpg", "textures", "item", KEY)
    os.makedirs(tex_dir, exist_ok=True)
    src = Image.open(os.path.join(REF, "T_CastingTotem.png")).convert("RGBA")
    # 发光体：字形（text_display，不受光照），白色，文字颜色染色
    table = glyph_table()
    providers = []
    font_dir = os.path.join(rp, "assets", "rpg", "textures", "font", KEY)
    os.makedirs(font_dir, exist_ok=True)
    for name, frames in glyph_frames().items():
        code, size, count = table[name]
        assert len(frames) == count, (name, len(frames))
        for i, im in enumerate(frames):
            assert im.size == (size, size), (name, im.size)
            im.save(os.path.join(font_dir, "%s_%d.png" % (name, i)))
            providers.append({"type": "bitmap", "file": "rpg:font/%s/%s_%d.png" % (KEY, name, i),
                              "height": size, "ascent": size // 2 - 3, "chars": [chr(code + i)]})
    dm.wj(os.path.join(rp, "assets", "rpg", "font", FONT_NAME + ".json"), {"providers": providers})
    # 地面贴花
    ds = decals()
    for name, im in ds.items():
        im.save(os.path.join(tex_dir, name + ".png"))
        write_item(rp, name, plane_model("rpg:item/%s/%s" % (KEY, name)))
    # 附魔光束
    beam_strip().save(os.path.join(tex_dir, "beam.png"))
    dm.wj(os.path.join(tex_dir, "beam.png.mcmeta"), {"animation": {"frametime": 2}})
    write_item(rp, "beam", beam_model("rpg:item/%s/beam" % KEY))
    rs = table["rune"]
    sg = sigil(src)
    shrink(sg, 32).save(os.path.join(tex_dir, "sigil.png"))
    write_item(rp, "sigil", plane_model("rpg:item/%s/sigil" % KEY))
    # Solomon's seal: the same sigil and itself turned half round -> a six-pointed star in the ring
    hexa = sg.copy(); hexa.alpha_composite(sg.rotate(180))
    shrink(hexa, 32).save(os.path.join(tex_dir, "hexagram.png"))
    write_item(rp, "hexagram", plane_model("rpg:item/%s/hexagram" % KEY))
    # 二阶段：权柄线（闪电，交叉双面）
    bolt_strip().save(os.path.join(tex_dir, "bolt_beam.png"))
    dm.wj(os.path.join(tex_dir, "bolt_beam.png.mcmeta"), {"animation": {"frametime": 1}})
    write_item(rp, "bolt_beam", cross_beam_model("rpg:item/%s/bolt_beam" % KEY))
    n = dict((name, prop_model(rp, name, *spec)) for name, spec in PROPS.items())
    print("usurper fx art: %d glyphs (rune, pop, burst, star, ray, spark, bolt, slash), %d decals + sigil + hexagram, "
          "beam + bolt_beam strips, props %s" % (len(providers), len(ds), ", ".join("%s %d" % kv for kv in n.items())))


if __name__ == "__main__":
    main()
