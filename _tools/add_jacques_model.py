# -*- coding: utf-8 -*-
"""圣殿大团长雅克的外观（docs/JACQUES-DESIGN.md）：原作玩家英雄网格、赫克斯皮肤、英雄铠甲，手持坟墓克星与竖琴弩。

    python add_jacques_model.py ../resourcepack ../rpg

模型在 _tools/jacques_dungeons_ref/（dungeons_models.py 的 jacques）：
  身体   SK_Player_Master，材质换成赫克斯 T_Hex
  盔甲   冠军铠甲的六件网格挂在玩家骨架的护甲插槽上，贴图换成英雄铠甲 T_HerosArmor（冠军铠甲第一个独特变体）
  近战   坟墓克星 SM_Glaive_Unique1，右手武器插槽
  远程   竖琴弩 SM_HarpCrossbow1～4（上弦的四个阶段），左手武器插槽；同一时刻只显示一个
动作全是原作玩家动作（长柄刀待机/行走/奔跑、坟墓克星三连、弩上弦/射击、翻滚、表情等），见 dungeons_models.py。
换装对象是雅克战的载体（rpg.jqb，add_jacques_boss.py 召唤），用 LordLook 的 carriers；
武器切换：rpg:jacques/weapon/{glaive,harp1..4,none}。
"""
import os
import sys

from display_mob import wf
from lord_look import LordLook

HERE = os.path.dirname(os.path.abspath(__file__))
WEAPONS = ("glaive", "harp1", "harp2", "harp3", "harp4")


def snd(stem, n, fmt="%s-%03d.ogg"):
    """Original Dungeons sounds from minecraft.wiki (_tools/dungeons_sounds/jacques/)."""
    return ["jacques/" + fmt % (stem, i) for i in range(1, n + 1)]


def ev(*ids):
    return ["minecraft:" + i for i in ids]


SOUNDS = {
    "hurt": (("雅克：受伤", "Jacques hurts"), ev("entity.player.hurt")),
    "death": (("雅克：倒下", "Jacques falls"), ev("entity.player.death")),
    # 原作音效（minecraft.wiki，2026-11-15 经用户同意下载，_tools/dungeons_sounds/jacques/）
    "swing1": (("坟墓克星：下劈", "Grave Bane strikes"), snd("Sfx_item_glaiveSwing", 5, "%s-%03d_soundWave.ogg")),
    "swing2": (("坟墓克星：再劈", "Grave Bane strikes again"), snd("Sfx_item_glaiveSwing", 5, "%s-%03d_soundWave.ogg")),
    "swing3": (("坟墓克星：横扫", "Grave Bane sweeps"), snd("Sfx_item_glaiveShing", 4, "%s-%03d_soundWave.ogg")),
    "load": (("竖琴弩：上弦", "Harp Crossbow loads"), snd("Sfx_item_scatterCrossbowUnique1Place", 3)),
    "fire": (("竖琴弩：放箭", "Harp Crossbow fires"), snd("Sfx_item_scatterCrossbowUnique1Shoot", 4)),
    "arrow": (("竖琴弩：箭落", "Harp bolts land"), snd("Sfx_item_scatterCrossbowUnique1Arrow", 1)),
    "roll": (("雅克：翻滚", "Jacques rolls"), ev("entity.player.attack.nodamage")),
    "horn": (("圣殿号角", "The Temple horn"), ev("event.raid.horn")),
    "step": (("雅克：脚步", "Armoured steps"), ev("block.chain.step")),
}

LOOK = LordLook(
    key="jacques", lord=0, label="雅克", tag="rpg.jqm", generator="add_jacques_model.py",
    # 战斗里的雅克是卫道士，召来的友军雅克是铁傀儡（add_jacques_ally.py）：两种载体都带 rpg.jqwear
    carriers="tag=rpg.jqwear", carrier_type=None,
    clips=[("idle", 4, True), ("walk", 2, True), ("run", 2, True),
           ("slash1", 1, False), ("slash2", 1, False), ("sweep", 1, False),
           ("load", 1, False), ("charge", 1, True), ("shoot", 1, False),
           ("roll_f", 1, False), ("roll_b", 1, False), ("horn", 1, False), ("gong", 1, False),
           ("mighty", 2, False), ("showoff", 1, False), ("kneel", 2, False), ("hero", 2, False),
           ("leap", 1, False), ("land", 1, False), ("curse", 1, False), ("stun", 2, True), ("hurt", 1, False),
           ("fall", 1, False), ("down", 2, True)],
    sounds=SOUNDS,
    # 时刻取自原作动作的事件（model_config.json 的 notifies：glaive_swing_Cue 等）
    cues={"walk": [(0.0, "step", 0.3, 1.0), (2.1, "step", 0.3, 1.0)],
          "run": [(0.17, "step", 0.3, 1.0), (0.71, "step", 0.3, 1.0), (1.27, "step", 0.3, 1.0), (1.8, "step", 0.3, 1.0)],
          "slash1": [(0.34, "swing1", 1.0, 1.0)], "slash2": [(0.45, "swing2", 1.0, 1.0)], "sweep": [(0.15, "swing3", 1.0, 0.9)],
          "load": [(0.07, "load", 1.0, 1.0)], "shoot": [(0.04, "fire", 1.0, 1.0)],
          "roll_f": [(0.1, "roll", 0.8, 0.8)], "roll_b": [(0.1, "roll", 0.8, 0.8)], "horn": [(0.1, "horn", 2.0, 1.0)]},
    skills={}, arrive="hero",
)
MOB = LOOK.mob

# 大卫的幽灵（二阶段）：同一套原作英雄网格，贴图转成半透明的白（ghost()）
DAVID = LordLook(
    key="david", lord=0, label="大卫的幽灵", tag="rpg.jqdm", generator="add_jacques_model.py",
    carriers="type=minecraft:vindicator,tag=rpg.jqd",
    clips=[("idle", 4, True), ("walk", 2, True), ("throw", 1, False), ("hero", 2, False)],
    sounds={"sling": (("大卫：甩出石子", "David slings a stone"), ev("item.trident.throw"))},
    cues={"throw": [(0.3, "sling", 1.2, 1.4)]}, skills={}, arrive="hero",
)


def weapons(dp):
    """rpg:jacques/weapon/<w> (as carrier): show that one weapon, hide the rest."""
    func = os.path.join(dp, "data", "rpg", "function", "jacques", "weapon")
    for show in WEAPONS + ("none",):
        lines = ["# 只显示%s（as 载体）。由 add_jacques_model.py 生成。" % ("一把武器：" + show if show != "none" else "：不拿武器")]
        for w in WEAPONS:
            model = "rpg:jacques/%s" % w if w == show else "rpg:empty"
            lines.append('execute on passengers if entity @s[tag=rpg.jqm.p.%s] run data modify entity @s '
                         'item.components."minecraft:item_model" set value "%s"' % (w, model))
        wf(os.path.join(func, show + ".mcfunction"), lines)
    # 换装后先只拿坟墓克星
    dress = os.path.join(dp, "data", "rpg", "function", "jacques", "dress.mcfunction")
    with open(dress, encoding="utf-8") as fh:
        text = fh.read().rstrip("\n").split("\n")
    i = text.index("function rpg:jacques/anim/init")
    text[i + 1:i + 1] = ["function rpg:jacques/weapon/glaive"]
    wf(dress, text)
    wf(os.path.join(dp, "data", "rpg", "function", "jacques", "debug", "preview.mcfunction"), [
        "# 预览雅克的外观：一个站着不动的载体（不是战斗）。清掉用 /function rpg:jacques/debug/clear",
        'summon minecraft:vindicator ~ ~ ~ {Tags:["rpg.jqb","rpg.jqwear","rpg.jqb.preview"],NoAI:1b,Silent:1b,PersistenceRequired:1b,'
        'Invulnerable:1b,active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}',
    ])
    wf(os.path.join(dp, "data", "rpg", "function", "jacques", "debug", "clear.mcfunction"), [
        "execute as @e[type=minecraft:vindicator,tag=rpg.jqb.preview] run function rpg:jacques/debug/clear_one"])
    wf(os.path.join(dp, "data", "rpg", "function", "jacques", "debug", "clear_one.mcfunction"), [
        "execute on passengers run kill @s", "tp @s ~ -256 ~", "kill @s"])
    for clip, *_r in LOOK.mob.clips:
        wf(os.path.join(dp, "data", "rpg", "function", "jacques", "debug", "play", clip + ".mcfunction"), [
            "execute as @e[tag=rpg.jqm,limit=1,sort=nearest] run function rpg:jacques/anim/enter/%s" % clip])


def ghost(rp):
    """David's atlas -> a pale blue-white, half transparent (partial alpha works on item models)."""
    from PIL import Image
    import numpy as np
    path = os.path.join(rp, "assets", "rpg", "textures", "item", "david", "atlas.png")
    a = np.array(Image.open(path).convert("RGBA")).astype(float)
    lum = (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]) / 255.0
    seen = a[..., 3] > 0
    t = 0.55 + 0.45 * lum
    a[..., 0], a[..., 1], a[..., 2] = 225 * t, 238 * t, 255 * t
    a[..., 3] = np.where(seen, 150, 0)
    Image.fromarray(a.clip(0, 255).astype(np.uint8)).save(path)


if __name__ == "__main__":
    rp = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
    dp = sys.argv[2] if len(sys.argv) > 2 else "../rpg"
    LOOK.main(rp, dp)
    weapons(dp)
    DAVID.main(rp, dp)
    ghost(rp)
    print("jacques look: %d parts, weapons %s" % (len(MOB.parts), ", ".join(WEAPONS)))
