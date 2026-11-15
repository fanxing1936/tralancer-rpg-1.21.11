# -*- coding: utf-8 -*-
"""路西法、萨麦尔、贝利尔、玛门麾下的罪仆外观（用户 2026-11-12：「把对应的罪仆模型也加上」；路西法的 2026-11-15）。

    python add_lord_servants.py ../resourcepack ../rpg

按领主的主题和柱色挑的原作模型（dungeons_models.py 生成，共用逻辑在 servant_look.py）：
  第一柱 路西法 → 苔藓骷髅（Mossy Skeleton，普通骷髅换苔藓贴图）：idle / walk / 手摆的劈砍 / 原作拉弓
  第五柱 萨麦尔 → 登山者红色变体（Mountaineer，护肩、靴子按蓝图挂上）：idle / walk / Attack / Brace
  第六柱 贝利尔 → 女巫（Witch，和坩埚同一主题、同为紫色）：idle / walk / AttackThrow / Drink
  第七柱 玛门   → 猪灵近战变体（Piglin，金甲红衣）：idle / walk / MeleeAttack / RangedAttack
声音是原作的（minecraft.wiki 下载，_tools/dungeons_sounds/）；登山者的「稳住」和猪灵的脚步借原版。
"""
import sys

from servant_look import ServantLook


def ev(cn, en, *ids):
    """Vanilla sound events."""
    return ((cn, en), ["minecraft:" + i for i in ids])


def wiki(cn, en, group, stem, n, fmt="%s-%03d.ogg"):
    """Original Dungeons sounds from minecraft.wiki, kept under _tools/dungeons_sounds/<group>/."""
    return ((cn, en), ["%s/%s" % (group, fmt % (stem, i)) for i in range(1, n + 1)])


W = "%s-%03d_soundWave.ogg"


LOOKS = [
    # 第一柱 路西法 → 苔藓骷髅（用户 2026-11-15）：普通骷髅换苔藓贴图；原作只有弓箭动作，近战的劈砍是手摆的。
    # 原作骷髅的声音没下载，先借原版骷髅的
    ServantLook(
        key="lucifer_servant", lord=1, label="路西法罪仆", tag="rpg.lcs", generator="add_lord_servants.py",
        sounds={"idle": ev("路西法罪仆：骨响", "Pride servant rattles", "entity.skeleton.ambient"),
                "hurt": ev("路西法罪仆：受伤", "Pride servant hurts", "entity.skeleton.hurt"),
                "death": ev("路西法罪仆：散架", "Pride servant collapses", "entity.skeleton.death"),
                "swing": ev("路西法罪仆：劈砍", "Pride servant swings", "entity.player.attack.sweep"),
                "shoot": ev("路西法罪仆：放箭", "Pride servant shoots", "entity.skeleton.shoot"),
                "step": ev("路西法罪仆：脚步", "Pride servant steps", "entity.skeleton.step")},
        cues={"walk": [(0.19, "step", 0.3, 1.0), (0.56, "step", 0.3, 1.0)], "attack": [(0.3, "swing", 1.0, 0.9)],
              "shoot": [(0.9, "shoot", 1.0, 1.0)]},
    ),
    ServantLook(
        key="samael_servant", lord=5, label="萨麦尔罪仆", tag="rpg.sms", generator="add_lord_servants.py",
        sounds={"idle": wiki("萨麦尔罪仆：低吼", "Wrath servant growls", "mountaineer", "D3_sfx_mob_mountaineerIdle_New", 4),
                "hurt": wiki("萨麦尔罪仆：受伤", "Wrath servant hurts", "mountaineer", "D3_sfx_mob_mountaineerHurt_New", 5),
                "death": wiki("萨麦尔罪仆：倒下", "Wrath servant dies", "mountaineer", "D3_sfx_mob_mountaineerDeath_New", 4),
                "swing": wiki("萨麦尔罪仆：挥砍", "Wrath servant swings", "mountaineer", "D3_sfx_mob_mountaineerAttack_New", 4),
                "brace": ev("萨麦尔罪仆：稳住", "Wrath servant braces", "entity.vindicator.celebrate")},
        cues={"attack": [(0.38, "swing", 1.0, 0.8)], "shoot": [(0.92, "brace", 1.0, 0.9)]},
    ),
    ServantLook(
        key="belial_servant", lord=6, label="贝利尔罪仆", tag="rpg.bls", generator="add_lord_servants.py",
        sounds={"idle": wiki("贝利尔罪仆：窃笑", "Lust servant giggles", "witch", "Sfx_mob_witchIdle", 5, W),
                "hurt": wiki("贝利尔罪仆：受伤", "Lust servant hurts", "witch", "Sfx_mob_witchHurt", 3, W),
                "death": wiki("贝利尔罪仆：倒下", "Lust servant dies", "witch", "Sfx_mob_witchDeath", 3, W),
                "throw": wiki("贝利尔罪仆：抛药", "Lust servant throws", "witch", "Sfx_mob_witchThrow", 3, W),
                "drink": wiki("贝利尔罪仆：喝药", "Lust servant drinks", "witch", "Sfx_mob_witchDrink", 4, W)},
        cues={"attack": [(0.49, "throw", 1.0, 1.0)], "shoot": [(0.45, "drink", 1.0, 1.0)]},
    ),
    ServantLook(
        key="mammon_servant", lord=7, label="玛门罪仆", tag="rpg.mms", generator="add_lord_servants.py",
        sounds={"idle": wiki("玛门罪仆：哼哼", "Greed servant snorts", "piglin", "D4_sfx_mob_piglinIdle", 4),
                "hurt": wiki("玛门罪仆：受伤", "Greed servant hurts", "piglin", "D4_sfx_mob_piglinHurt", 3),
                "death": wiki("玛门罪仆：倒下", "Greed servant dies", "piglin", "D4_sfx_mob_piglinDeath", 3),
                "angry": wiki("玛门罪仆：发怒", "Greed servant snarls", "piglin", "D4_sfx_mob_piglinAttack", 3),
                "step": ev("玛门罪仆：脚步", "Greed servant steps", "entity.piglin.step")},
        cues={"walk": [(0.25, "step", 0.4, 1.0), (0.6, "step", 0.4, 1.0)], "attack": [(0.17, "angry", 1.0, 1.0)]},
    ),
]

if __name__ == "__main__":
    rp = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
    dp = sys.argv[2] if len(sys.argv) > 2 else "../rpg"
    for look in LOOKS:
        look.main(rp, dp)
