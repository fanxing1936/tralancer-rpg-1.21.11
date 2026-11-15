# -*- coding: utf-8 -*-
"""篡夺者（达里奥·所罗门）一阶段的外观：Minecraft Dungeons 的附魔师（docs/USURPER-DESIGN.md）。

    python add_usurper_model.py ../resourcepack ../rpg

模型在 _tools/usurper_dungeons_ref/（dungeons_models.py 生成）：帽上宝石、袖口青边按颜色发光，
附魔书是骨骼模型自带的。换装对象是篡夺者战的载体（rpg.usb，add_usurper_boss.py 召唤），
不是七柱领主，所以用 LordLook 的 carriers；招式动作由战斗直接调用 rpg:usurper/anim/enter/<clip>：
  idle / walk
  attack   普攻，0.43 s 合书出手
  enchant  强化，0.14 s 抛书，1.63 s 灌注
  rise     闲置小动作，0.33 s 抛书，用作登场
声音是原作附魔师的（minecraft.wiki 下载，_tools/dungeons_sounds/enchanter/）。
二阶段载体打上 rpg.usb.s2，这里不再给它换装；外观交给首席附魔师（add_usurper_boss.py 的 look2/）。
"""
import sys

from lord_look import LordLook


def wiki(stem, n):
    """附魔师的原作音效（minecraft.wiki，2026-11-14 经用户同意下载，_tools/dungeons_sounds/enchanter/）。"""
    return ["enchanter/%s-%03d_soundWave.ogg" % (stem, i) for i in range(1, n + 1)]

LOOK = LordLook(
    key="usurper", lord=0, label="篡夺者", tag="rpg.usm", generator="add_usurper_model.py",
    carriers="type=minecraft:vindicator,tag=rpg.usb,tag=!rpg.usb.s2",      # 二阶段换成首席附魔师（rpg.usb.s2）
    clips=[("idle", 4, True), ("walk", 2, True), ("attack", 1, False), ("enchant", 1, False), ("rise", 2, False)],
    sounds={
        "idle": (("篡夺者：低语", "The Usurper murmurs"), wiki("Sfx_mob_enchanterIdle", 3)),
        "hurt": (("篡夺者：受伤", "The Usurper hurts"), wiki("Sfx_mob_enchanterHurt", 3)),
        "death": (("篡夺者：倒下", "The Usurper falls"), wiki("Sfx_mob_enchanterDeath", 3)),
        "close": (("合书", "A book snaps shut"), wiki("Sfx_ui_enchantBookClose", 1)),
        "attack": (("篡夺者：出手", "The Usurper strikes"), wiki("Sfx_mob_enchanterAttack", 3)),
        "prepare": (("篡夺者：蓄咒", "The Usurper gathers a spell"), wiki("Sfx_mob_enchanterPreAttack", 3)),
        "spell": (("篡夺者：施咒", "The Usurper casts"), wiki("Sfx_mob_enchanterSpell", 2)),
        "chime": (("附魔的鸣响", "Enchantment chimes"), wiki("Sfx_ui_enchantChime", 3)),
        "bladder": (("书页鼓动", "Pages flutter"), wiki("Sfx_ui_enchantBookBladder", 4)),
        "book": (("附魔书", "The tome hums"), wiki("Sfx_ui_enchantBook", 3)),
        "beam": (("附魔光束", "An enchanting beam"), wiki("Sfx_mob_enchanterBeam", 1)),
        "beam_loop": (("附魔光束持续", "The beam holds"), wiki("Sfx_mob_enchanterBeamLoop", 1)),
        "step": (("篡夺者：脚步", "The Usurper steps"), wiki("Sfx_player_stepGravel", 4)),
    },
    # 时刻取自原作动作的事件（model_config.json 的 notifies）
    cues={"walk": [(0.21, "step", 0.4, 1.0), (0.63, "step", 0.4, 1.0)],
          "attack": [(0.43, "close", 1.0, 1.0), (0.44, "attack", 1.0, 1.0)],
          "enchant": [(0.14, "prepare", 1.0, 1.0), (0.44, "bladder", 1.0, 1.0), (1.63, "chime", 1.0, 1.0),
                      (1.63, "spell", 1.0, 1.0), (2.37, "close", 1.0, 1.0)],
          "rise": [(0.33, "bladder", 1.0, 1.0), (0.49, "idle", 1.0, 1.0), (1.46, "bladder", 1.0, 1.0),
                   (2.34, "bladder", 1.0, 1.0), (4.43, "book", 1.0, 1.0)]},
    skills={}, arrive="rise", arrive_sound="prepare",
)
MOB = LOOK.mob

if __name__ == "__main__":
    LOOK.main(sys.argv[1] if len(sys.argv) > 1 else "../resourcepack", sys.argv[2] if len(sys.argv) > 2 else "../rpg")
