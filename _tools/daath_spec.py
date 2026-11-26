# -*- coding: utf-8 -*-
"""达阿特试炼的表：武器类别、每一类的原作动作、形状与伤害（docs/DAATH-DESIGN.md）。

dungeons_models.py（转换）、add_daath_model.py（外观）、add_daath_fight.py（出招）都读这里。
"""

# 武器类别：键 → (编号, 中文, 判定物品的谓词（逐条或）)。编号 0 留给空手。
# 类别按顺序判，先中先得；细分类（细剑、长柄、双持、太刀、大剑）按本包的 custom_data 或名字落进来
CLASSES = {
    "fist": (0, "空手"),
    "sword": (1, "剑"),
    "axe": (2, "斧"),
    "mace": (3, "重锤"),
    "spear": (4, "矛"),
    "glaive": (5, "长柄"),
    "dagger": (6, "双刃"),
    "scythe": (7, "镰"),
    "bow": (8, "弓"),
    "crossbow": (9, "弩"),
}

# 出招：(动作名, 原作动作, 类别, 形状, 伤害%, 前冲)
#   形状 arc 扇形、wide 大扇形、spin 整圈、line 直线、smash 前方砸地、jab 贴身
#   出手时刻由 add_daath_model 按武器骨尖的速度峰算
H = [
    # 剑：钢剑、太刀、大剑、弯刀、细剑、珊瑚刃六路
    ("sw1", "SwordSwing_1", "sword", "arc", 7, 0.5), ("sw2", "SwordSwing_2", "sword", "arc", 7, 0.5),
    ("sw3", "SwordSwing_3", "sword", "wide", 11, 0.7),
    ("ka1", "KatanaCombo_1", "sword", "arc", 7, 0.9), ("ka2", "KatanaCombo_2", "sword", "arc", 7, 0.6),
    ("ka3", "KatanaCombo_3", "sword", "line", 11, 1.4),
    ("cl1", "ClaymoreCombo1", "sword", "wide", 10, 0.5), ("cl2", "ClaymoreCombo2", "sword", "wide", 10, 0.5),
    ("cl3", "ClaymoreCombo3", "sword", "smash", 14, 0.6),
    ("cu1", "CutlassCombo_1LeftToRight", "sword", "arc", 7, 0.5), ("cu2", "CutlassCombo_2LeftToRight_Alternative", "sword", "arc", 7, 0.5),
    ("ra1", "RapierCombo1Start", "sword", "line", 7, 1.0), ("ra2", "RapierCombo2_Left", "sword", "line", 6, 0.6),
    ("ra3", "RapierCombo2_Right", "sword", "line", 6, 0.6), ("ra4", "RapierCombo5Final", "sword", "line", 11, 1.2),
    ("co1", "CoralBladeCombo_1", "sword", "arc", 7, 0.5), ("co2", "CoralBladeCombo_2", "sword", "arc", 7, 0.5),
    ("co3", "CoralBladeCombo_3", "sword", "wide", 10, 0.6),
    # 斧：单斧、双斧旋身、骨棒
    ("ax1", "AxeCombo_1LeftToRight", "axe", "arc", 9, 0.5), ("ax2", "AxeCombo_2LeftToRight_Alternative", "axe", "arc", 9, 0.5),
    ("ax3", "AxeCombo_3SpinAttack", "axe", "spin", 14, 0.4),
    ("da1", "DoubleAxeCombo_SpinAttack1", "axe", "spin", 10, 0.6), ("da2", "DoubleAxeCombo_SpinAttack2", "axe", "spin", 12, 0.6),
    ("bc1", "BoneclubCombo1", "axe", "smash", 12, 0.5), ("bc2", "BoneclubCombo2", "axe", "wide", 12, 0.5),
    # 重锤
    ("ma1", "MaceSwing_1", "mace", "arc", 12, 0.4), ("ma2", "MaceSwing_2", "mace", "arc", 12, 0.4),
    ("ma3", "MaceSwing_3", "mace", "smash", 16, 0.4), ("ha1", "HammerCombo_1Strike_Separated_Composite", "mace", "smash", 18, 0.5),
    # 矛与长柄、棍
    ("sp1", "SpearCombo1", "spear", "line", 8, 0.8), ("sp2", "SpearCombo2", "spear", "line", 8, 0.8),
    ("sp3", "SpearCombo3", "spear", "line", 12, 1.2),
    ("bo1", "BoStaffCombo1_Left", "spear", "arc", 7, 0.5), ("bo2", "BoStaffCombo2_Right", "spear", "arc", 7, 0.5),
    ("bo3", "BoStaffCombo3_Swipe", "spear", "wide", 8, 0.5), ("bo4", "BoStaffCombo4_Smash", "spear", "smash", 11, 0.5),
    ("gl1", "GlaiveCombo_Attack1", "glaive", "arc", 8, 0.5), ("gl2", "GlaiveCombo_Attack2", "glaive", "arc", 8, 0.5),
    ("gl3", "GlaiveCombo_Attack3", "glaive", "wide", 12, 0.5),
    ("gu1", "BoStaffCombo5_Thrust1", "glaive", "line", 8, 0.8), ("gu2", "BoStaffCombo7_SpinAttack1", "glaive", "spin", 9, 0.5),
    # 双刃：双匕首、背刺、虚空刃、镰刀
    ("dg1", "DaggersComboDeluxe_1", "dagger", "jab", 4, 0.5), ("dg2", "DaggersComboDeluxe_2", "dagger", "jab", 4, 0.5),
    ("dg3", "DaggersComboDeluxe_3", "dagger", "jab", 4, 0.5), ("dg4", "DaggersComboDeluxe_4", "dagger", "jab", 4, 0.5),
    ("dg5", "DaggersComboDeluxe_5", "dagger", "jab", 4, 0.6), ("dg6", "DaggersComboDeluxe_6", "dagger", "arc", 6, 0.8),
    ("bs1", "BackstabberCombo_1", "dagger", "jab", 5, 0.8), ("bs2", "BackstabberCombo_2", "dagger", "jab", 5, 0.8),
    ("bs3", "BackstabberCombo_3", "dagger", "line", 8, 1.2),
    ("vb1", "VoidBladesCombo_1", "dagger", "arc", 5, 0.6), ("vb2", "VoidBladesCombo_2", "dagger", "arc", 5, 0.6),
    ("vb3", "VoidBladesCombo_3", "dagger", "spin", 7, 0.6),
    ("si1", "SicklesCombo1", "dagger", "jab", 4, 0.5), ("si4", "SicklesCombo4", "dagger", "arc", 5, 0.5), ("si6", "SicklesCombo6", "dagger", "spin", 7, 0.5),
    # 镰
    ("sc1", "ScytheCombo_1Scythe", "scythe", "wide", 10, 0.5), ("sc2", "ScytheCombo_2Scythe", "scythe", "wide", 12, 0.5),
    # 空手：拳套
    ("fi1", "GauntletsCombo1", "fist", "jab", 4, 0.5), ("fi2", "GauntletsCombo2", "fist", "jab", 4, 0.5),
    ("fi3", "GauntletsCombo3", "fist", "jab", 4, 0.5), ("fi4", "GauntletsCombo4", "fist", "jab", 4, 0.5),
    ("fi5", "GauntletsCombo5", "fist", "jab", 5, 0.6), ("fi6", "GauntletsCombo6", "fist", "smash", 8, 0.6),
]

# 弓弩与通用动作：(动作名, 原作动作, 循环)
C = [
    ("idle", "Idle", True), ("walk", "Run", True),
    ("bow", "Bow_Shoot", False), ("bow_draw", "Bow_Charge", False),
    ("xbow", "Crossbow_Shoot", False), ("xbow_load", "Crossbow_Load", False),
    ("roll_f", "DodgeRollForward", False), ("roll_b", "DodgeRollBackward", False),
    ("roll_l", "DodgeRollSidewayLeft", False), ("roll_r", "DodgeRollSidewayRight", False),
    ("cast", "EnchantersTome_Start", False), ("updraft", "UpdraftTome", False), ("shake", "Powershake", False),
    ("drink", "Drink", False), ("mighty", "Emote_MightySword", False), ("twirl", "Emote_TheTwirl", False), ("gong", "Gong", False),
    ("vanish", "TeleportInitiate_Start", False), ("land", "TeleportLanding", False), ("falling", "Falling", True),
    ("kneel", "Emote_KneelPose", False), ("hero", "Emote_HeroPose", False),
    ("hurt", "GetHitFront", False), ("stun", "Stun", True), ("fall", "DownedFloor_Initiate", False), ("down", "DownedFloored_Loop", True),
    ("guard", "ShowOff", False), ("throw", "SpinWheel_Throw", False), ("revive", "SupportRevive", False),
]
CLIPS = [("Player_Master_" + src, name, loop) for name, src, loop in C] + [("Player_Master_" + h[1], h[0], False) for h in H]
