# -*- coding: utf-8 -*-
"""贝利尔（第六柱·色欲）的外观：Minecraft Dungeons 的腐化坩埚（Corrupted Cauldron）。

    python add_belial_model.py ../resourcepack ../rpg

用户 2026-11-12 选定（「那口锅」）。模型在 _tools/belial_lord_dungeons_ref/（dungeons_models.py 生成）：
锅里的药水原作就是品红紫，换成按第六柱色板画的发光药水贴图；坩埚原作朝 +z，显示时转 180°。
共用的换装逻辑在 lord_look.py。
  idle    原作待机（勺子在锅里搅）
  walk    自制「颠步」：原作没有行走，整口锅左右摇、每步跳起一点
  cast    BasicAttack：冒泡、吐出                —— sk6_2、sk6_3、sk6_5；降临
  summon  StrongAttack：猛震、旋转              —— sk6_1、sk6_4
  spin    IntenseSpin：狂转                     —— 终式蓄势
声音是原作的（minecraft.wiki 下载，_tools/dungeons_sounds/corrupted_cauldron）；颠步借原版锁链声。
"""
import os
import sys

from lord_look import LordLook

def wiki(group, stem, n, fmt="%s-%03d.ogg"):
    """Original Dungeons sounds from minecraft.wiki, kept under _tools/dungeons_sounds/<group>/."""
    return ["%s/%s" % (group, fmt % (stem, i)) for i in range(1, n + 1)]


LOOK = LordLook(
    key="belial_lord", lord=6, label="贝利尔", tag="rpg.bll", generator="add_belial_model.py",
    clips=[("idle", 4, True), ("walk", 2, True), ("cast", 1, False), ("summon", 1, False), ("spin", 2, False)],
    sounds={
        "idle": (("贝利尔：药水翻滚", "Belial's brew bubbles"), wiki("corrupted_cauldron", "Sfx_multi_bossCauldronIdle", 10, "%s-%03d_soundWave.ogg")),
        "hurt": (("贝利尔：受伤", "Belial hurts"), wiki("corrupted_cauldron", "Sfx_mob_bossCauldronHurt", 6, "%s-%03d_soundWave.ogg")),
        "death": (("贝利尔：倾覆", "Belial overturns"), wiki("corrupted_cauldron", "Sfx_mob_bossCauldronDeath", 1, "%s-%03d_soundWave.ogg")),
        "brew": (("贝利尔：吞咽", "Belial gulps"), wiki("corrupted_cauldron", "Sfx_mob_bossCauldronSwallowLightLayer", 1, "%s-%03d_soundWave.ogg")),
        "bubble": (("贝利尔：沸腾", "Belial boils over"), wiki("corrupted_cauldron", "Sfx_mob_bossCauldronAttackBubble", 2, "%s-%03d_soundWave.ogg")),
        "laugh": (("贝利尔：笑", "Belial laughs"), wiki("corrupted_cauldron", "Sfx_mob_bossCauldronAttackVoice", 4, "%s-%03d_soundWave.ogg")),
        "splash": (("贝利尔：咽下", "Belial swallows"), wiki("corrupted_cauldron", "Sfx_mob_bossCauldronSwallowBass", 3, "%s-%03d_soundWave.ogg")),
        "spin": (("贝利尔：狂转", "Belial whirls"), wiki("corrupted_cauldron", "Sfx_mob_bossCauldronAttackSpin", 3, "%s-%03d_soundWave.ogg")
                 + wiki("corrupted_cauldron", "Sfx_mob_bossCauldronVoiceSpin", 1, "%s-%03d_soundWave.ogg")),
        "wand": (("勺子搅动", "The ladle stirs"), wiki("corrupted_cauldron", "Sfx_multi_bossCauldronWandSpin", 1, "%s-%03d_soundWave.ogg")),
        "hop": (("贝利尔：颠动", "Belial hops"), ["minecraft:block.chain.place"]),
    },
    cues={"walk": [(0.2, "hop", 0.6, 0.6), (0.6, "hop", 0.6, 0.6)],
          "cast": [(0.16, "bubble", 1.0, 1.0), (0.82, "laugh", 1.0, 1.0), (1.36, "splash", 1.0, 1.0)],
          "summon": [(0.56, "brew", 1.0, 1.0), (3.13, "spin", 1.0, 1.0)],
          "spin": [(0.32, "spin", 1.2, 1.0), (1.58, "laugh", 1.2, 1.0)],
          "idle": [(0.08, "wand", 0.6, 1.0), (1.52, "wand", 0.6, 1.0), (2.96, "wand", 0.6, 1.0)]},
    skills={
        "sk6_1": ("summon", None),         # 令人跪下，7 格内
        "sk6_2": ("cast", None),           # 晕眩，8 格内
        "sk6_3": ("cast", None),           # 汲取，7 格内
        "sk6_4": ("summon", None),         # 凝视，8 格内
        "sk6_5": ("cast", None),           # 帷幕，10 格内
        "ult6_warn": ("spin", "laugh"),    # 终式蓄势
        "ult6": (None, "splash"),
    },
    arrive="cast", arrive_sound="laugh", gone_sound="death",
)
MOB = LOOK.mob

# 锅里的药水（用户 2026-11-12：「紫色汤药需要做发光纹理，要有发光效果」）。原作材质只有颜色，转出来只是一块
# 采到图集里一个纯色像素的平面。这里把这个面单独接一张 16×16、8 帧的动画发光贴图（.mcmeta），
# 元素本身已是 light_emission 15；再让锅口不时冒出发光的气泡。
GOO_PART = "belial_lord_liquid_012"
GOO_TEX = "rpg:item/belial_lord/goo"
GOO_FRAMES = 8
GOO_HEIGHT = 1.45            # blocks above the carrier's feet: the brew surface in the standing pose
RAMP = [(0x3A, 0x12, 0x4A), (0x5B, 0x2C, 0x6F), (0x8A, 0x1C, 0x8E), (0xB8, 0x00, 0xAC),
        (0xD9, 0x7A, 0xD9), (0xF2, 0xB8, 0xF0), (0xFF, 0xE8, 0xFF)]
BUBBLES = [(3, 4, 0), (11, 2, 3), (8, 10, 5), (13, 12, 2), (2, 13, 6), (6, 7, 1)]   # x, y, phase


def goo_frames():
    """A slow swirl of the ramp, with bubbles that swell, flash and pop over the 8 frames."""
    import math
    from PIL import Image
    sheet = Image.new("RGBA", (16, 16 * GOO_FRAMES))
    for f in range(GOO_FRAMES):
        a = f / GOO_FRAMES * 2 * math.pi
        for y in range(16):
            for x in range(16):
                dx, dy = x - 7.5, y - 7.5
                r = math.hypot(dx, dy)
                v = math.sin(math.atan2(dy, dx) * 2 + r * .7 - a) * .5 + .5      # swirl, 0..1
                i = 2 + int(round(v * 2))                                        # mid of the ramp
                if r > 7:
                    i -= 1                                                       # darker at the rim
                sheet.putpixel((x, y + 16 * f), RAMP[i] + (255,))
        for bx, by, ph in BUBBLES:
            stage = (f + ph) % GOO_FRAMES
            y0 = 16 * f
            if stage < 3:                       # swelling: a lit ring round a darker core
                for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    sheet.putpixel(((bx + ox) % 16, y0 + (by + oy) % 16), RAMP[4] + (255,))
                sheet.putpixel((bx, y0 + by), RAMP[2 + stage % 2] + (255,))
                sheet.putpixel(((bx - 1) % 16, y0 + (by - 1) % 16), RAMP[5] + (255,))
            elif stage == 3:                    # the pop: a white flash
                sheet.putpixel((bx, y0 + by), RAMP[6] + (255,))
                for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    sheet.putpixel(((bx + ox) % 16, y0 + (by + oy) % 16), RAMP[5] + (255,))
    return sheet


def glow_goo(rp, dp):
    import json
    from display_mob import wf, wj
    path = os.path.join(rp, "assets", "rpg", "models", "belial_lord", GOO_PART + ".json")
    with open(path, encoding="utf-8") as fh:
        model = json.load(fh)
    model["textures"]["1"] = GOO_TEX
    for el in model["elements"]:
        el["light_emission"] = 15
        el["shade"] = False
        for face in el["faces"].values():
            face["texture"] = "#1"
            face["uv"] = [0, 0, 16, 16]
    wj(path, model)
    tex = os.path.join(rp, "assets", "rpg", "textures", "item", "belial_lord", "goo.png")
    goo_frames().save(tex)
    wj(tex + ".mcmeta", {"animation": {"frametime": 3, "interpolate": True}})
    # glowing bubbles from the brew, now and then
    wj(os.path.join(dp, "data", "rpg", "predicate", "belial_lord", "bubble.json"),
       {"condition": "minecraft:random_chance", "chance": 0.12})
    follow = os.path.join(dp, "data", "rpg", "function", "belial_lord", "follow.mcfunction")
    with open(follow, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    lines += [
        "# 锅里的药水冒发光的气泡",
        "execute if predicate rpg:belial_lord/bubble run particle minecraft:dust{color:[0.85,0.48,0.85],scale:1.1} "
        "~ ~%.2f ~ 0.35 0.05 0.35 0 2 normal" % GOO_HEIGHT,
        "execute if predicate rpg:belial_lord/bubble run particle minecraft:witch ~ ~%.2f ~ 0.3 0.1 0.3 0 1 normal"
        % (GOO_HEIGHT + .1),
    ]
    wf(follow, lines)


if __name__ == "__main__":
    RP = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
    DP = sys.argv[2] if len(sys.argv) > 2 else "../rpg"
    LOOK.main(RP, DP)
    glow_goo(RP, DP)
