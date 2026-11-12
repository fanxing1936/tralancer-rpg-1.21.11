# -*- coding: utf-8 -*-
"""玛门（第七柱·贪婪）的外观：Minecraft Dungeons 的猪灵商人（Piglin Merchant）。

    python add_mammon_model.py ../resourcepack ../rpg

用户 2026-11-12 按柱色（金橙）选定。模型在 _tools/mammon_lord_dungeons_ref/（dungeons_models.py 生成）；
key 叫 mammon_lord，因为 rpg:mammon/ 已经是罪器弓的。共用的换装逻辑在 lord_look.py。
  idle   商人自己的待机
  walk   普通猪灵的行走（按骨名搬到商人骨架上）
  cast   普通猪灵的投掷，身体扭转压到 45%    —— 清算
  summon 自制「聚金砸地」：举手聚金，0.75 s 砸地  —— 什一税、收缴、利息、金狱、黄金终审蓄势
  rise   商人的环顾，降临时播
声音是原作的（minecraft.wiki 下载，_tools/dungeons_sounds/piglin_merchant、piglin）。
"""
import sys

from lord_look import LordLook

def wiki(group, stem, n, fmt="%s-%03d.ogg"):
    """Original Dungeons sounds from minecraft.wiki, kept under _tools/dungeons_sounds/<group>/."""
    return ["%s/%s" % (group, fmt % (stem, i)) for i in range(1, n + 1)]


LOOK = LordLook(
    key="mammon_lord", lord=7, label="玛门", tag="rpg.mml", generator="add_mammon_model.py",
    clips=[("idle", 4, True), ("walk", 2, True), ("cast", 1, False), ("summon", 1, False), ("rise", 2, False)],
    sounds={
        "idle": (("玛门：嘟囔", "Mammon grunts"), wiki("piglin_merchant", "P4_sfx_mob_merchantPiglinMerchantIdle", 5)),
        "hurt": (("玛门：受伤", "Mammon hurts"), wiki("piglin_merchant", "P4_sfx_mob_merchantPiglinMerchantHurt", 3)),
        "death": (("玛门：倒下", "Mammon dies"), wiki("piglin_merchant", "P4_sfx_mob_merchantPiglinMerchantDeath", 4)),
        "admire": (("玛门：成交", "Mammon strikes a deal"), wiki("piglin_merchant", "P4_sfx_mob_merchantPiglinMerchantBuy", 3)),
        "angry": (("玛门：发怒", "Mammon snarls"), wiki("piglin", "D4_sfx_mob_piglinBruteAttack", 10)),
        "jealous": (("玛门：白给", "Mammon scoffs"), wiki("piglin_merchant", "P4_sfx_mob_merchantPiglinMerchantFree", 4)),
        "brute": (("玛门：怒吼", "Mammon roars"), wiki("piglin", "D4_sfx_mob_piglinBruteIdle", 9)),
        "celebrate": (("玛门：进货", "Mammon restocks"), wiki("piglin_merchant", "P4_sfx_mob_merchantPiglinMerchantRestock", 3)),
        "retreat": (("玛门：收摊", "Mammon closes shop"), wiki("piglin_merchant", "P4_sfx_mob_merchantPiglinMerchantClose", 4)),
        "open": (("玛门：开张", "Mammon opens shop"), wiki("piglin_merchant", "P4_sfx_mob_merchantPiglinMerchantOpen", 3)),
        "step": (("玛门：脚步", "Mammon steps"), wiki("piglin_merchant", "P4_sfx_mob_merchantPiglinMerchantStep", 5)),
    },
    cues={"walk": [(0.0, "step", 0.5, 0.8), (0.35, "step", 0.5, 0.8)],
          "summon": [(0.75, "brute", 1.0, 0.9)], "cast": [(0.45, "jealous", 1.0, 0.8)]},
    skills={
        "sk7_1": ("summon", "admire"),     # 什一税
        "sk7_2": ("summon", "angry"),      # 收缴
        "sk7_3": ("cast", None),           # 清算
        "sk7_4": ("summon", "admire"),     # 利息
        "sk7_5": ("summon", None),         # 金狱
        "ult7_warn": ("summon", "brute"),  # 黄金终审蓄势
        "ult7": (None, "celebrate"),       # 黄金终审
    },
    arrive_sound="open", gone_sound="retreat",
)
MOB = LOOK.mob

if __name__ == "__main__":
    LOOK.main(sys.argv[1] if len(sys.argv) > 1 else "../resourcepack", sys.argv[2] if len(sys.argv) > 2 else "../rpg")
