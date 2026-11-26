# -*- coding: utf-8 -*-
"""达阿特的影子的外观（docs/DAATH-DESIGN.md §6）：原作玩家英雄的骨架与约九十段动作，身上穿的是挑战者自己的盔甲。

    python add_daath_model.py ../resourcepack ../rpg

部件：
  身体六块   皮肤压成近黑（daath_ref/shadow_skin.png，make_skin() 从原作皮肤改色）
  盔甲九块   放挑战者那件盔甲的真物品，只换 item_model 到 rpg:daath/a/<底材>/<块>：
             盒子模型的 UV 直接指原版盔甲贴图；染色读 dyed_color，纹饰读 minecraft:trim
             盔甲块和它盖着的身体块带同一个部件标签，动作一并走，不多一行指令
  武器两块   主副手，真物品
  头颅       二段换成玩家头颅（rpg:daath/face/on）
原版盔甲贴图的布局就是 64×64 皮肤的上半张，所以面的 UV 从皮肤坐标换算：
make_uv() 用坐标着色的皮肤转换过一次，把每个面对应的皮肤矩形存进 daath_ref/uv.json（一次性，随包提交）。
"""
import io
import json
import os
import sys

import display_mob as dm
import daath_spec as S
from display_mob import wf, wj
from lord_look import LordLook

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "daath_ref")
UVJ = os.path.join(REF, "uv.json")
TAG = "rpg.dtm"
BASE_PARTS = ("head", "body", "l_arm", "r_arm", "l_leg", "r_leg")


def ev(*ids):
    return ["minecraft:" + i for i in ids]


def ogg(stem, n):
    return ["daath/" + stem % i + ".ogg" for i in range(1, n + 1)]


SOUNDS = {
    "hurt": (("影：受击", "The shadow is struck"), ev("block.glass.hit")),
    # 原作音效（minecraft.wiki，2026-11-25 用户同意下载，_tools/dungeons_sounds/daath/）
    "flash1": (("影：闪", "The shadow flickers"), ogg("D6_sfx_item_shadowFlash_activate1_%03d", 3)),
    "flash2": (("影：闪", "The shadow flickers"), ogg("D6_sfx_item_shadowFlash_activate2_%03d", 3)),
    "flash3": (("影：爆开", "The shadow bursts"), ogg("D6_sfx_item_shadowFlash_activate3_%03d", 3)),
    "execute": (("影：攫取", "The shadow seizes"), ogg("D6_sfx_shadowFeastExecute-%03d", 5)),
    "splinter": (("影：碎裂", "The shadow splinters"), ogg("D6_sfx_shadowSplinterActivate-%03d", 3)),
    "shot": (("影：放箭", "The shadow looses a bolt"), ogg("D6_sfx_wpn_shadowCbow_shot_%03d", 3)),
    "impact": (("影箭：命中", "A shadow bolt strikes"), ogg("D6_sfx_wpn_shadowCbow_impact_%03d", 3)),
    "mirror": (("影：入镜", "The shadow enters the glass"), ogg("DLC_sfx_mob_illusionerMirror-%03d", 2)),
    "step": (("影：脚步", "Steps on black water"), ev("entity.generic.splash")),
}

# 盔甲块 → (盖着的身体块, 槽位, 贴图层, 放大像素)；像素是皮肤的一格
PIECES = {
    "helmet": ("head", "head", "humanoid", 1.0),
    "chest": ("body", "chest", "humanoid", 1.01),
    "chest_l": ("l_arm", "chest", "humanoid", 1.0),
    "chest_r": ("r_arm", "chest", "humanoid", 1.0),
    "waist": ("body", "legs", "humanoid_leggings", 0.51),
    "legs_l": ("l_leg", "legs", "humanoid_leggings", 0.5),
    "legs_r": ("r_leg", "legs", "humanoid_leggings", 0.5),
    "boot_l": ("l_leg", "feet", "humanoid", 1.0),
    "boot_r": ("r_leg", "feet", "humanoid", 1.0),
}


class Look(LordLook):
    def __init__(self):
        super().__init__(
            key="daath", lord=0, label="影", tag=TAG, generator="add_daath_model.py", carriers="tag=rpg.dtwear", carrier_type=None,
            clips=[(n, 2 if loop else 1, loop) for n, _s, loop in S.C] + [(h[0], 1, False) for h in S.H],
            sounds=SOUNDS, skills={}, arrive="idle", cues={})
        m = self.mob
        m.parts = self.fold(m)
        m.parts += [("weapon_r", ["J_R_Weapon"]), ("weapon_l", ["J_L_Weapon"])]
        m.held, m.held_left = "weapon_r", "weapon_l"
        m.held_ref = ("idle", 0.0)
        m.held_size = 1.0 / m.dungeons_variant["model_scale"]
        m.ambient = m.hurt = m.death = None
        m.hold_clips = {"down", "kneel", "fall"}
        m.cues = {"walk": [(0.35, "step", 0.12, 1.5), (0.9, "step", 0.12, 1.6), (1.45, "step", 0.12, 1.5), (2.0, "step", 0.12, 1.6)]}

    @staticmethod
    def fold(m):
        """六个身体块：原作的第二层（*_armor）不要，头的几片面并回头。"""
        parts = dict(m.parts)
        head = list(parts["head"])
        root = ["J_Head"] if "J_Head" not in head else []
        for p in parts:
            if p.startswith("daath_head_") and "armor" not in p:
                head += [b for b in parts[p] if b not in head]
        out = []
        for p in BASE_PARTS:
            out.append((p, root + head if p == "head" else parts[p]))
        return out

    def dress(self, first):
        m, t = self.mob, self.tag
        comp = dict(first)
        # 站姿的部件变换：十影、影傀摆静止的假影子用
        json.dump({p: dm.snbt_components(m, comp[p]) for p in BASE_PARTS}, io.open(os.path.join(REF, "idle.json"), "w", encoding="utf-8"), indent=1)
        lines = ["# 影子换装（as 载体，at 其脚下）：身体六块、盔甲九块、武器两块。", "tag @s add %s" % t, "tag @s add %s.dressing" % t]
        blank = '{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:empty"}}'

        def summ(tags, item, transform, disp="none"):
            return ('summon minecraft:item_display ~ ~ ~ {Tags:[%s],item:%s,item_display:"%s",brightness:{block:0,sky:0},'
                    'teleport_duration:2,interpolation_duration:2,view_range:1.5f,transformation:%s}'
                    % (",".join('"%s"' % x for x in tags), item, disp, dm.snbt_components(m, transform)))
        for part in BASE_PARTS:
            lines.append(summ((t + ".part", t + ".p." + part, t + ".body", t + ".new"),
                              '{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:daath/%s"}}' % part, comp[part]))
        for piece, (part, slot, _tex, _g) in PIECES.items():
            lines.append(summ((t + ".part", t + ".p." + part, t + ".arm", t + ".a." + piece, t + ".s." + slot, t + ".new"), blank, comp[part]))
        for part, disp in (("weapon_r", "thirdperson_righthand"), ("weapon_l", "thirdperson_lefthand")):
            lines.append(summ((t + ".part", t + ".p." + part, t + ".new"), blank, comp[part], disp))
        lines += ["execute as @e[type=minecraft:item_display,tag=%s.new,distance=..1] run ride @s mount @e[tag=%s.dressing,limit=1]" % (t, t),
                  "tag @e[type=minecraft:item_display,tag=%s.new,distance=..2] remove %s.new" % (t, t),
                  "tag @s remove %s.dressing" % t, "function rpg:daath/anim/init", "function rpg:daath/anim/enter/idle"]
        wf(os.path.join(m.func, "dress.mcfunction"), lines)


# 底材：物品前缀 → 贴图名
BASES = {"leather": "leather", "chainmail": "chainmail", "iron": "iron", "golden": "gold", "diamond": "diamond", "netherite": "netherite",
         "copper": "copper", "turtle": "turtle_scute"}
SLOT_ITEM = {"head": "helmet", "chest": "chestplate", "legs": "leggings", "feet": "boots"}
PATTERNS = ("sentry", "dune", "coast", "wild", "ward", "eye", "vex", "tide", "snout", "rib", "spire", "wayfinder", "shaper", "silence",
            "raiser", "host", "flow", "bolt")
MATERIALS = ("quartz", "iron", "netherite", "redstone", "copper", "gold", "emerald", "diamond", "lapis", "amethyst", "resin")
LIMB_MIRROR = {"l_arm": "r_arm", "r_leg": "l_leg"}
# 64×64 皮肤里各块的起点与宽高深（瘦臂 3 宽）
SKIN = {"head": (0, 0, 8, 8, 8), "body": (16, 16, 8, 12, 4), "r_arm": (40, 16, 3, 12, 4), "r_leg": (0, 16, 4, 12, 4),
        "l_arm": (32, 48, 3, 12, 4)}
# 原作把两条腿的 UV 叫反了：l_leg 用的是皮肤右腿那一块
SKIN["l_leg"], SKIN["r_leg"] = (0, 16, 4, 12, 4), (16, 48, 4, 12, 4)


def face_rects(u, v, w, h, d):
    """皮肤布局里一个盒子六面的矩形（x0, y0, x1, y1）。"""
    return {"right": (u, v + d, u + d, v + d + h), "front": (u + d, v + d, u + d + w, v + d + h),
            "left": (u + d + w, v + d, u + 2 * d + w, v + d + h), "back": (u + 2 * d + w, v + d, u + 2 * d + 2 * w, v + d + h),
            "top": (u + d, v, u + d + w, v + d), "bottom": (u + d + w, v, u + d + 2 * w, v + d)}


def armor_uv(part, rect):
    """rect：这个面在皮肤上的 [u0,v0,u1,v1]（可能翻转）→ 盔甲贴图的 UV（16 分制，图 64×32）。"""
    cx, cy = (rect[0] + rect[2]) / 2.0, (rect[1] + rect[3]) / 2.0
    name = next((n for n, (x0, y0, x1, y1) in face_rects(*SKIN[part]).items() if x0 <= cx <= x1 and y0 <= cy <= y1), None)
    if name is None:
        raise SystemExit("uv outside part %s: %s" % (part, rect))
    x0, y0, x1, y1 = face_rects(*SKIN[part])[name]
    src = LIMB_MIRROR.get(part, part)
    U, V = SKIN[src][:2]
    W, H, D = (4, 12, 4) if src in ("r_arm", "l_leg") else SKIN[src][2:]
    n2 = {"right": "left", "left": "right"}.get(name, name) if part in LIMB_MIRROR else name
    X0, Y0, X1, Y1 = face_rects(U, V, W, H, D)[n2]

    def m(x, y):
        fx, fy = (x - x0) / float(x1 - x0), (y - y0) / float(y1 - y0)
        if part in LIMB_MIRROR:
            fx = 1 - fx
        return X0 + fx * (X1 - X0), Y0 + fy * (Y1 - Y0)
    a, b = m(rect[0], rect[1]), m(rect[2], rect[3])
    return [round(x, 4) for x in (a[0] / 4.0, a[1] / 2.0, b[0] / 4.0, b[1] / 2.0)]


# ---------------------------------------------------------------- 一次性：坐标着色取 UV，再把皮肤压黑
def coded_skin():
    from PIL import Image
    im = Image.new("RGBA", (64, 64))
    for x in range(64):
        for y in range(64):
            im.putpixel((x, y), (x * 4, y * 4, 0, 255))
    im.save(os.path.join(REF, "shadow_skin.png"))


def make_uv():
    """daath_dungeons_ref 是用坐标着色的皮肤转换的时候跑：python add_daath_model.py uv"""
    from PIL import Image
    m = LOOK.mob
    bones, png, res = dm.load_bbmodel(m)
    im = Image.open(io.BytesIO(png)).convert("RGBA")
    out = {}
    for part, members in m.parts:
        if part not in BASE_PARTS:
            continue
        model, _K = dm.part_model(m, bones, part, members, res)
        rows = []
        for el in model["elements"]:
            faces = {}
            for k, f in el["faces"].items():
                u0, v0, u1, v1 = [c / 16.0 * res["width"] for c in f["uv"]]
                du, dv = (1 if u1 > u0 else -1), (1 if v1 > v0 else -1)
                # 图集里每块外面有一圈 0.5 像素的边：往里取
                a = im.getpixel((int(u0 + du * 1.0), int(v0 + dv * 1.0)))
                b = im.getpixel((int(u1 - du * 1.0), int(v1 - dv * 1.0)))
                faces[k] = {"a": [a[0] // 4, a[1] // 4], "b": [b[0] // 4, b[1] // 4], "size": [abs(u1 - u0), abs(v1 - v0)],
                            "rot": f.get("rotation", 0)}
            rows.append({"from": el["from"], "to": el["to"], "faces": faces})
        out[part] = rows
    json.dump(out, io.open(UVJ + ".raw", "w", encoding="utf-8"), indent=1)
    print("uv raw written")


def make_skin():
    from PIL import Image
    src = ("D:/agent/dungeons_extract/upgrade/daath/assets/Dungeons/Content/Actors/Characters/Player/Master/Skins/Valorie/"
           "T_Valorie_Skin.png")
    im = Image.open(src).convert("RGBA")
    px = im.load()
    for x in range(64):
        for y in range(64):
            r, g, b, a = px[x, y]
            if a:
                k = 0.45 + 0.35 * (0.3 * r + 0.59 * g + 0.11 * b) / 255.0
                px[x, y] = (int(34 * k), int(37 * k), int(46 * k), a)
    im.save(os.path.join(REF, "shadow_skin.png"))


LOOK = Look()

if __name__ == "__main__" and sys.argv[1] == "uv":
    make_uv()
    sys.exit()
if __name__ == "__main__" and sys.argv[1] in ("skin", "coded"):
    (make_skin if sys.argv[1] == "skin" else coded_skin)()
    sys.exit()


# ---------------------------------------------------------------- 盔甲块
PX = 0.12
HALF = {"head": (4, 4, 4), "body": (4, 2, 6), "l_arm": (1.5, 2, 6), "r_arm": (1.5, 2, 6), "l_leg": (2, 2, 6), "r_leg": (2, 2, 6)}
# 头的面在转换里有几片读不准，按躯干同样的朝向写死（y+ 前，z+ 上，x+ 右）
HEAD_FACES = [
    ("y", 1, {"up": [16, 16, 8, 8], "down": [16, 8, 8, 16]}), ("y", -1, {"down": [32, 8, 24, 16], "up": [32, 16, 24, 8]}),
    ("z", 1, {"north": [8, 8, 16, 0], "south": [16, 8, 8, 0]}), ("z", -1, {"north": [16, 0, 24, 8], "south": [24, 0, 16, 8]}),
    ("x", -1, {"west": [16, 8, 24, 16], "east": [16, 16, 24, 8]}), ("x", 1, {"west": [8, 8, 0, 16], "east": [8, 16, 0, 8]})]


def uv_table():
    """{块: [(轴, 正负, {面: ([u0,v0,u1,v1], 旋转)})]}，坐标是 64×64 皮肤像素。"""
    out = {"head": [(a, s, {k: (r, 90 if a == "x" else 0) for k, r in f.items()}) for a, s, f in HEAD_FACES]}
    raw = json.load(io.open(UVJ, encoding="utf-8"))
    for part in BASE_PARTS[1:]:
        rows = []
        for r in raw[part]:
            ax = next(i for i in range(3) if abs(r["from"][i] - r["to"][i]) < 1e-6)
            sign = 1 if r["from"][ax] > 8 else -1
            faces = {}
            for k, f in r["faces"].items():
                cx, cy = (f["a"][0] + f["b"][0]) / 2.0 + .5, (f["a"][1] + f["b"][1]) / 2.0 + .5
                x0, y0, x1, y1 = next(v for v in face_rects(*SKIN[part]).values() if v[0] <= cx <= v[2] and v[1] <= cy <= v[3])
                fu, fv = f["b"][0] >= f["a"][0], f["b"][1] >= f["a"][1]
                faces[k] = ([x0 if fu else x1, y0 if fv else y1, x1 if fu else x0, y1 if fv else y0], f["rot"])
            rows.append(("xyz"[ax], sign, faces))
        out[part] = rows
    return out


def box_model(part, grow, tex, tint, table):
    h = [HALF[part][i] * PX + grow * PX for i in range(3)]
    if part in ("l_arm", "r_arm"):
        h[0] += 0.5 * PX                    # 盔甲的袖子是 4 宽
    els = []
    for ax, sign, faces in table[part]:
        i = "xyz".index(ax)
        lo, hi = [8 - h[k] for k in range(3)], [8 + h[k] for k in range(3)]
        lo[i] = hi[i] = 8 + sign * h[i]
        f2 = {}
        for k, (rect, rot) in faces.items():
            f = {"uv": armor_uv(part, rect), "texture": "#0"}
            if rot:
                f["rotation"] = rot
            if tint:
                f["tintindex"] = 0
            f2[k] = f
        els.append({"from": [round(v, 4) for v in lo], "to": [round(v, 4) for v in hi], "faces": f2})
    return {"textures": {"0": tex, "particle": tex}, "elements": els}


def wjc(path, doc):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, separators=(",", ":"))
        fh.write("\n")


def armour(rp):
    import shutil
    table = uv_table()
    A = os.path.join(rp, "assets")
    for d in ("models/daath/a", "items/daath/a"):
        shutil.rmtree(os.path.join(A, "rpg", *d.split("/")), ignore_errors=True)
    ap = os.path.join(A, "minecraft", "atlases", "items.json")
    atlas = json.load(io.open(ap, encoding="utf-8"))
    atlas["sources"] = [s for s in atlas["sources"] if "entity/equipment" not in str(s.get("resource", "")) and
                        not any(str(t).startswith("minecraft:trims/entity/") for t in s.get("textures", []))]
    layers = ("humanoid", "humanoid_leggings")
    for layer in layers:
        for tex in sorted(set(BASES.values())) + ["leather_overlay"]:
            if layer == "humanoid_leggings" and tex == "turtle_scute":
                continue
            atlas["sources"].append({"type": "minecraft:single", "resource": "minecraft:entity/equipment/%s/%s" % (layer, tex)})
    # 变体名加 dt_ 前缀：和盔甲图集同名的变体客户端会警告
    perm = {"dt_" + m: "minecraft:trims/color_palettes/" + m for m in MATERIALS}
    perm["dt_holy"] = "rpg:trims/color_palettes/holy"
    atlas["sources"].append({"type": "minecraft:paletted_permutations",
                             "textures": ["minecraft:trims/entity/%s/%s" % (la, p) for la in layers for p in PATTERNS],
                             "palette_key": "minecraft:trims/color_palettes/trim_palette", "permutations": perm})
    wj(ap, atlas)
    n = 0
    mats = [("minecraft:" + m, m) for m in MATERIALS] + [(HOLY_ID, "holy")]
    for piece, (part, slot, layer, grow) in PIECES.items():
        for p in PATTERNS:
            for _mid, m in mats:
                wjc(os.path.join(A, "rpg", "models", "daath", "a", "t", piece, "%s_%s.json" % (p, m)),
                    box_model(part, grow + 0.04, "minecraft:trims/entity/%s/%s_dt_%s" % (layer, p, m), False, table))
                n += 1
        cases = [{"when": {"pattern": "minecraft:" + p, "material": mid},
                  "model": {"type": "minecraft:model", "model": "rpg:daath/a/t/%s/%s_%s" % (piece, p, m)}} for p in PATTERNS for mid, m in mats]
        trim = {"type": "minecraft:select", "property": "minecraft:component", "component": "minecraft:trim", "cases": cases,
                "fallback": {"type": "minecraft:empty"}}
        for base, tex in BASES.items():
            if base == "turtle" and slot != "head":
                continue
            wjc(os.path.join(A, "rpg", "models", "daath", "a", "b", piece, base + ".json"),
                box_model(part, grow, "minecraft:entity/equipment/%s/%s" % (layer, tex), base == "leather", table))
            layer0 = {"type": "minecraft:model", "model": "rpg:daath/a/b/%s/%s" % (piece, base)}
            ms = [layer0]
            if base == "leather":
                layer0["tints"] = [{"type": "minecraft:dye", "default": -6265536}]
                wjc(os.path.join(A, "rpg", "models", "daath", "a", "b", piece, "leather_overlay.json"),
                    box_model(part, grow + 0.01, "minecraft:entity/equipment/%s/leather_overlay" % layer, False, table))
                ms.append({"type": "minecraft:model", "model": "rpg:daath/a/b/%s/leather_overlay" % piece})
            wjc(os.path.join(A, "rpg", "items", "daath", "a", base, piece + ".json"),
                {"model": {"type": "minecraft:composite", "models": ms + [trim]}})
            n += 2
    # 头颅（二段）：把 8 格的头颅缩进头块里，竖轴从 y 转到 z
    wj(os.path.join(A, "rpg", "models", "daath", "face_base.json"), {
        "gui_light": "front", "textures": {"particle": "minecraft:block/soul_sand"},
        "display": {"fixed": {"rotation": [90, 180, 0], "translation": [0, 0, 0.48], "scale": [0.122, 0.122, 0.122]}}})
    wj(os.path.join(A, "rpg", "items", "daath", "face.json"), {
        "model": {"type": "minecraft:special", "base": "rpg:daath/face_base", "model": {"type": "minecraft:player_head"}}})
    return n


def eyes(rp):
    """影子的头上两颗白眼睛：贴在前面（y+），全亮。"""
    p = os.path.join(rp, "assets", "rpg", "models", "daath", "head.json")
    doc = json.load(io.open(p, encoding="utf-8"))
    # 没有眼睛的头：十影里的假影子、影傀用
    wj(p.replace("head.json", "head_blank.json"), doc)
    wj(os.path.join(rp, "assets", "rpg", "items", "daath", "head_blank.json"), {"model": {"type": "minecraft:model", "model": "rpg:daath/head_blank"}})
    doc["textures"]["w"] = "rpg:item/daath/eye"
    y = 8 + 4 * PX + 0.012
    for sx in (-1, 1):
        x0, x1 = sorted((8 + sx * 1 * PX, 8 + sx * 3 * PX))
        doc["elements"].append({"from": [round(x0, 4), round(y, 4), 7.88], "to": [round(x1, 4), round(y, 4), 8.0], "light_emission": 15,
                                "shade": False, "faces": {k: {"uv": [0, 0, 16, 16], "texture": "#w"} for k in ("up", "down")}})
    wj(p, doc)
    from PIL import Image
    Image.new("RGBA", (16, 16), (255, 255, 255, 255)).save(os.path.join(rp, "assets", "rpg", "textures", "item", "daath", "eye.png"))


# ---------------------------------------------------------------- 穿戴与武器（as 载体；挑战者带 rpg.dt.me）
def functions(dp):
    F = os.path.join(dp, "data", "rpg", "function", "daath")
    ME = "@a[tag=rpg.dt.me,limit=1]"
    wear = ["# 把挑战者（rpg.dt.me）的四件盔甲抄到影子身上（as 载体）"]
    for slot in SLOT_ITEM:
        wear.append("function rpg:daath/wear/%s" % slot)
        wf(os.path.join(F, "wear", slot + ".mcfunction"), [
            "# %s（as 载体）" % SLOT_ITEM[slot],
            "execute on passengers if entity @s[tag=%s.s.%s] run item replace entity @s contents from entity %s armor.%s" % (TAG, slot, ME, slot),
            "execute on passengers if entity @s[tag=%s.s.%s] run function rpg:daath/wear/fit_%s" % (TAG, slot, slot)])
        fit = ["# 按底材换成盔甲块模型（as 盔甲块）；认不出的（鞘翅、南瓜、自定义装备层）就不画"]
        for piece, (_part, s2, _la, _g) in PIECES.items():
            if s2 != slot:
                continue
            for base in BASES:
                if base == "turtle" and slot != "head":
                    continue
                fit.append("execute if entity @s[tag=%s.a.%s] if items entity @s contents minecraft:%s_%s run return run data modify entity @s "
                           "item.components.\"minecraft:item_model\" set value \"rpg:daath/a/%s/%s\"" % (TAG, piece, base, SLOT_ITEM[slot], base, piece))
        fit.append("execute if items entity @s contents * run data modify entity @s item.components.\"minecraft:item_model\" set value \"rpg:empty\"")
        wf(os.path.join(F, "wear", "fit_%s.mcfunction" % slot), fit)
    wf(os.path.join(F, "wear", "all.mcfunction"), wear)
    for name, val, zh in (("dark", 0, "变成黑影"), ("lit", 15, "显出真形")):
        wf(os.path.join(F, "look", name + ".mcfunction"), [
            "# 整个身子%s（as 载体）" % zh,
            "execute on passengers if entity @s[type=minecraft:item_display] run data merge entity @s {brightness:{block:%d,sky:%d}}" % (val, val)])
    wf(os.path.join(F, "face", "on.mcfunction"), [
        "# 二段：头换成挑战者自己的头（as 载体，挑战者带 rpg.dt.me）",
        "execute on passengers if entity @s[tag=%s.p.head,tag=%s.body] run function rpg:daath/face/set" % (TAG, TAG)])
    wf(os.path.join(F, "face", "set.mcfunction"), [
        "tag @s add rpg.dt.face",
        "execute as %s run loot replace entity @e[type=minecraft:item_display,tag=rpg.dt.face,limit=1] contents loot rpg:daath/head" % ME,
        "tag @s remove rpg.dt.face",
        "data modify entity @s item.components.\"minecraft:item_model\" set value \"rpg:daath/face\"",
        "data modify entity @s item_display set value \"fixed\""])
    wj(os.path.join(dp, "data", "rpg", "loot_table", "daath", "head.json"), {"type": "minecraft:generic", "pools": [{"rolls": 1, "entries": [
        {"type": "minecraft:item", "name": "minecraft:player_head", "functions": [{"function": "minecraft:fill_player_head", "entity": "this"}]}]}]})


def hits():
    """每段出招的出手刻：武器骨尖速度最大的那一刻（战斗用）。"""
    m = LOOK.mob
    bones, _png, _res = dm.load_bbmodel(m)
    clips = dm.load_animations(m)
    out = {}
    for h in S.H:
        clip = clips[h[0]]
        n = int(round(clip["length"] / dm.TICK))
        pts = []
        for t in range(n + 1):
            row = []
            for bone in ("J_R_Weapon", "J_L_Weapon"):
                W = dm.posed_matrix(bones, bone, clip, t * dm.TICK)
                q = list(bones[bone]["pivot"]) + [1]
                row.append([sum(W[i][k] * q[k] for k in range(4)) for i in range(3)])
            pts.append(row)
        sp = [max(sum((a[i] - b[i]) ** 2 for i in range(3)) for a, b in zip(pts[t], pts[t - 1])) for t in range(1, n + 1)]
        k = max(range(len(sp)), key=lambda i: sp[i]) + 1
        out[h[0]] = (max(2, k), n)
    return out


HOLY_ID = "rpg:holy"

if __name__ == "__main__":
    RP, DP = sys.argv[1], sys.argv[2]
    LOOK.main(RP, DP)
    eyes(RP)
    cnt = armour(RP)
    functions(DP)
    json.dump(hits(), io.open(os.path.join(REF, "hits.json"), "w", encoding="utf-8", newline="\n"), indent=1)
    print("daath model: %d armour models and items" % cnt)
