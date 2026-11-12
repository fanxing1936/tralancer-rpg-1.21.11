# -*- coding: utf-8 -*-
"""萨麦尔（第五柱·暴怒）的外观：Minecraft Dungeons 的红石巨怪（Redstone Monstrosity）。

    python add_samael_model.py ../resourcepack ../rpg

用户 2026-11-12 选定（先给的红石傀儡被改掉）。模型在 _tools/samael_lord_dungeons_ref/（dungeons_models.py 生成）。
红石纹路和石头画在同一个面上，没法只让红色发光，所以不加发光。共用的换装逻辑在 lord_look.py。动作全是原作的：
  cast    BasicAttack，0.69 s 射出           —— sk5_1、sk5_3
  charge  StrongAttack，冲步后 0.82 s 重击   —— sk5_2、sk5_4
  summon  SlamAttack，0.95 s 双拳砸地        —— sk5_5
  super   LavaAttack，0.90 s 熔岩重击        —— 终式蓄势
  rise    Awaken，地裂苏醒、3.04 s 咆哮      —— 降临
"""
import sys

from lord_look import LordLook

def wiki(group, stem, n, fmt="%s-%03d.ogg"):
    """Original Dungeons sounds from minecraft.wiki, kept under _tools/dungeons_sounds/<group>/."""
    return ["%s/%s" % (group, fmt % (stem, i)) for i in range(1, n + 1)]


LOOK = LordLook(
    key="samael_lord", lord=5, label="萨麦尔", tag="rpg.sml", generator="add_samael_model.py",
    clips=[("idle", 4, True), ("walk", 2, True), ("cast", 1, False), ("charge", 1, False),
           ("summon", 1, False), ("super", 2, False), ("rise", 2, False)],
    sounds={
        "idle": (("萨麦尔：低沉的轰鸣", "Samael rumbles"), wiki("redstone_monstrosity", "Sfx_mob_rsMonstrosityIdle", 7, "%s-%03d_soundWave.ogg")),
        "hurt": (("萨麦尔：受伤", "Samael hurts"), wiki("redstone_monstrosity", "Sfx_mob_rsMonstrosityHurt", 4, "%s-%03d_soundWave.ogg")),
        "death": (("萨麦尔：崩塌", "Samael crumbles"), wiki("redstone_monstrosity", "Sfx_mob_rsMonstrosityDeath", 1, "%s-%03d_soundWave.ogg")),
        "step": (("萨麦尔：沉重的脚步", "Samael stomps"), wiki("redstone_monstrosity", "Sfx_mob_rsMonstrosityStep", 4, "%s-%03d_soundWave.ogg")),
        "attack": (("萨麦尔：射出熔岩", "Samael hurls lava"), wiki("redstone_monstrosity", "Sfx_mob_rsMonstrosityShoot", 3, "%s-%03d_soundWave.ogg")),
        "arm": (("萨麦尔：挥臂", "Samael swings"), wiki("redstone_monstrosity", "Sfx_mob_rsMonstrosityArm", 2, "%s-%03d_soundWave.ogg")),
        "roar": (("萨麦尔：怒吼", "Samael roars"), wiki("redstone_monstrosity", "Sfx_mob_rsMonstrosityGrowl", 1, "%s-%03d_soundWave.ogg")
                 + wiki("redstone_monstrosity", "Sfx_mob_rsMonstrosityShortGrowl", 1, "%s-%03d_soundWave.ogg")),
        "awaken": (("萨麦尔：苏醒", "Samael awakens"), wiki("redstone_monstrosity", "Sfx_mob_rsMonstrosityAwaken", 1, "%s-%03d_soundWave.ogg")),
        "charge": (("萨麦尔：蓄力低吼", "Samael gathers fury"), wiki("redstone_monstrosity", "Sfx_mob_rsMonstrosityVoiceCharge", 3, "%s-%03d_soundWave.ogg")),
        "slam": (("萨麦尔：砸地", "Samael slams the ground"), ["minecraft:item.mace.smash_ground_heavy"]),
    },
    cues={"walk": [(0.02, "step", 0.8, 1.0), (0.99, "step", 0.8, 1.0)],
          "cast": [(0.69, "attack", 1.0, 1.0), (1.18, "arm", 1.0, 1.0)],
          "charge": [(0.0, "roar", 0.8, 1.0), (0.82, "slam", 1.0, 0.8)],
          "summon": [(0.95, "slam", 1.0, 0.7)],
          "super": [(0.44, "charge", 1.0, 1.0), (0.9, "slam", 1.2, 0.6)],
          "rise": [(0.77, "slam", 0.8, 0.5), (3.04, "awaken", 1.2, 1.0)]},
    skills={
        "sk5_1": ("cast", None),           # 抛掷，7 格内命中
        "sk5_2": ("charge", None),         # 冲向最近的人、6 格内斩
        "sk5_3": ("cast", None),           # 魂火，8 格内
        "sk5_4": ("charge", None),         # 冲撞
        "sk5_5": ("summon", None),         # 重锤砸地
        "ult5_warn": ("super", "roar"),    # 终式蓄势
        "ult5": (None, "slam"),
    },
    arrive_sound=None, gone_sound="death",
)
MOB = LOOK.mob

if __name__ == "__main__":
    LOOK.main(sys.argv[1] if len(sys.argv) > 1 else "../resourcepack", sys.argv[2] if len(sys.argv) > 2 else "../rpg")
