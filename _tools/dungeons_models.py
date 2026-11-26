# -*- coding: utf-8 -*-
"""从本体导出转换「原作模型」变体（docs/DUNGEONS-UPGRADE-PROMPT.md 第二批）。

    python dungeons_models.py [key ...]

一次性的制作脚本，不进构建：读 D:/agent/dungeons_extract/upgrade/ 下的导出，
经 dungeons_conversion/generic.py 转成 _tools/<key>_dungeons_ref/，生成器再经
dungeons_variant.py 选用它。每个怪：

    mesh     骨骼网格（导出根目录下的相对路径，不带 .glb）
    anims    动作所在的导出根（共用骨架的怪，动作在别的目录）
    clips    [(原作动作, 现有动作名, 循环)]：保持现有动作名，技能钩子照常工作
    height   游戏内身高（格），取现有模型的实测值，碰撞箱和座位不用动

结果里 clips.json 记着每段的时长和原作事件时刻（声音、粒子、发射），
用来重新对准音效和出手时刻。
"""

import json
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from dungeons_conversion import generic as G  # noqa: E402
from dungeons_conversion import blueprint as BP  # noqa: E402
import numpy as np  # noqa: E402
from scipy.spatial.transform import Rotation  # noqa: E402
import daath_spec as DAATH  # noqa: E402

UP = Path(r"D:\agent\dungeons_extract\upgrade")
E = "Dungeons/Content/Actors/Characters/Enemies/"
UNIT = 0.0192
D5 = "Dungeons/Content/Content_DLC5/Actors/Characters/Enemies/"
D4 = "Dungeons/Content/Content_DLC4/Actors/Characters/"
# 眼、眉、鼻并进头部：少几个实体（dungeons_variant.fold 检查能否合并）
FACE = ["nose", "l_eyepupil", "l_eyeiris", "r_eyepupil", "r_eyeiris", "l_eyebrow", "r_eyebrow"]
GLOW = {"cyan": lambda c: (c[:, 2] > 150) & (c[:, 1] > 110) & (c[:, 0] < 110),
        "red": lambda c: (c[:, 0] > 170) & (c[:, 1] < 80) & (c[:, 2] < 80)}

MODELS = {
    "leviathan": dict(root="necromancer", mesh=E + "SkeletonNecromancer/SK_SkeletonNecromancer", anims="necromancer",
                      # 用户要杖头发青光（2026-11-02 起的要求）；原作没有自发光图，按青色取
                      glow="cyan",
                      # 用户 2026-11-14：调成普通骷髅大小
                      height=2.0, clips=[("SkeletonNecromancer_Idle", "idle", True),
                                          ("SkeletonNecromancer_Walk", "walk", True),
                                          ("SkeletonNecromancer_BasicAttack", "cast", False),
                                          ("SkeletonNecromancer_StrongAttack", "summon", False),
                                          ("SkeletonNecromancer_Novelty", "rise", False)]),
    "beelzebub": dict(root="nameless", mesh=E + "NamelessKing/SK_NamelessKing", anims="nameless",
                      # 杖头光球：原作是挂在武器插槽上的粒子（PS_Nameless_GravityStaff，沿杖 100 cm），转换里没有它。
                      # 照用户确认过的旧版做：三层套方块（半透明外层、白框、实心核心），斜立，绕杖身转
                      orb=dict(bone="J_R_Weapon", offset=(0, 0, -100), texture="dungeons_overrides/orb_beelzebub.png",
                               cubes=[(29.4, (0, 0, 8, 8)), (22.0, (8, 0, 14, 6)), (11.0, (14, 0, 17, 3))],
                               tilt=(45, 0, 35.26), spin=180),
                      # 用户 2026-11-14：调成普通骷髅大小
                      height=2.0, clips=[("NamelessKing_Walk", "idle", True),
                                          ("NamelessKing_Walk", "walk", True),
                                          ("NamelessKing_TeleportIn", "cast", False),
                                          ("NamelessKing_BasicAttack", "summon", False),
                                          ("NamelessKing_Awake", "rise", False)]),
    "abaddon": dict(root="wickedwraith", mesh=E + "Wicked_Wraith/SK_WickedWraith_01", anims="wickedwraith",
                    height=2.43, clips=[("wickedWraith_Idle", "idle", True),
                                        ("wickedWraith_Walk", "walk", True),
                                        ("wickedWraith_basicAttack", "cast", False),
                                        ("wickedWraith_CircularProjectileAttack", "spread", False)]),
    "pope": dict(root="archillager", mesh=E + "Illagers/ArchIllager/SK_ArchIllager", anims="archillager",
                 height=2.60, clips=[("ArchIllager_Idle", "idle", True),
                                     ("ArchIllager_Run", "walk", True),
                                     ("ArchIllager_BasicAttackJump_VFX", "attack", False),
                                     ("ArchIllager_SummonSingle_VFX", "summon", False),
                                     ("ArchIllager_SummonCircle_VFX", "cast", False),
                                     ("ArchIllager_LandingFinalBoss", "appear", False),
                                     # 原作命名和这里相反：TeleportOut 是现身（mirror_in、雷声、笑），
                                     # TeleportIn 是消失（spell_dissapear、mirror_out）
                                     ("ArchIllager_TeleportOut", "teleport_in", False),
                                     ("ArchIllager_TeleportIn", "teleport_out", False),
                                     ("ArchIllager_DefeatedInawhirlwind_VFX", "whirlwind", False)],
                 merge={"head": FACE}),
    # 小怪：动作可以借同一套骨架的别的怪（anims 给多个导出根）；held 物品挂在原作武器插槽上
    "vanguard": dict(root="vanguard", mesh=E + "SkeletonVanguard/SK_SkeletonVanguard", anims=["vanguard", "skeleton"],
                     # 盾牌是蓝图挂件（BP_DesertShield 挂右手武器插槽），头盔网格自带
                     blueprint=E + "SkeletonVanguard/BP_SkeletonVanguardCharacter", sockets=["skeleton"],
                     attach_names={"Shield": "shield"}, attach_skip=["SM_DesertArmor_Helmet", "Backpack"],
                     height=2.22, clips=[("Skeleton_Vanguard_Idle", "idle", True),
                                         ("Skeleton_Vanguard_Walk", "walk", True),
                                         ("Skeleton_Vanguard_Attack", "attack", False),
                                         ("Skeleton_GetHitFromTheFront", "break", False)]),
    "sunken_skeleton": dict(root="sunken", mesh=D5 + "SunkenSkeleton/SK_SunkenSkeleton", anims=["sunken", "skeleton", "vanguard"],
                            held_bone="J_R_Weapon",
                            height=2.56, clips=[("Skeleton_Idle", "idle", True),
                                               ("Skeleton_Walk", "walk", True),
                                               ("Skeleton_Vanguard_Attack", "attack", False),
                                               ("Skeleton_BasicAttack", "shoot", False)]),
    "tower_wraith": dict(root="towerwraith", mesh=E + "TowerWraith/SK_TowerWraith", anims=["towerwraith", "wraith"],
                         held_bone="J_R_Weapon",
                         height=2.08, clips=[("Wraith_Idle", "idle", True),
                                             ("Wraith_Walk2", "walk", True),
                                             ("Wraith_BasicAttack", "attack", False),
                                             ("TowerWraith_PoisonEmberAttack", "cast", False)]),
    # 玛门：猪灵商人（用户选定 2026-11-12）。商人本身只有两段待机；行走、出手借普通猪灵的动作，
    # 两套骨架同名骨的静止姿态一致，按骨名搬旋转（generic.retarget_tracks），脖子并进头
    "mammon_lord": dict(root="mammon", mesh=D4 + "Friendlies/PiglinMerchant/SK_PiglinMerchant", anims=["mammon"],
                   retarget={"piglin": {"source_meta": D4 + "Enemies/Piglin/SK_Piglin",
                                        "merge": {"J_Head": ["J_Neck", "J_Head"]}, "move": ["J_Root", "J_Body"],
                                        # 猪灵出手时整个身体大幅扭转，商人背着货架太夸张：身体转幅压到 45%
                                        "damp": {"J_Body": .45}}},
                   # 商人是友方 NPC，原作朝 +z（敌人朝 -z），显示时整体转 180°
                   turn=180,
                   height=3.2, clips=[("PiglinMerchant_Idle1", "idle", True),
                                      ("Piglin_WalkMelee", "walk", True, "piglin"),
                                      ("Piglin_Throw", "cast", False, "piglin"),
                                      ("PiglinMerchant_IdleLookAround", "rise", False)],
                   # 猪灵的近战是侧身大挥砍，套在背货架的商人身上像要摔倒；范围技能用自制的「聚金砸地」：
                   # 双手举过头聚金、后仰，0.75 s 砸向身前地面、前倾下蹲，再收回。
                   # 轴向（实测，模型朝 +z）：手臂 x 负 = 向前/向上抬，右臂 z 正 = 外展；身体、头 x 正 = 前倾；
                   # J_Root 位移在模型空间，y 负 = 下蹲。
                   custom_clips={"summon": dict(length=1.5, loop=False, keys={
                       "J_R_Arm": [(0, (0, 0, 0)), (.35, (-165, 0, 20)), (.55, (-170, 0, 22)), (.75, (-40, 0, 8)),
                                   (1.05, (-30, 0, 5)), (1.5, (0, 0, 0))],
                       "J_L_Arm": [(0, (0, 0, 0)), (.35, (-165, 0, -20)), (.55, (-170, 0, -22)), (.75, (-40, 0, -8)),
                                   (1.05, (-30, 0, -5)), (1.5, (0, 0, 0))],
                       "J_Body": [(0, (0, 0, 0)), (.35, (-12, 0, 0)), (.55, (-14, 0, 0)), (.75, (25, 0, 0)),
                                  (1.05, (18, 0, 0)), (1.5, (0, 0, 0))],
                       "J_Head": [(0, (0, 0, 0)), (.35, (-15, 0, 0)), (.55, (-18, 0, 0)), (.75, (10, 0, 0)),
                                  (1.05, (6, 0, 0)), (1.5, (0, 0, 0))],
                       "J_Root": [(0, None, (0, 0, 0)), (.55, None, (0, .1, 0)), (.75, None, (0, -.35, 0)),
                                  (1.05, None, (0, -.25, 0)), (1.5, None, (0, 0, 0))],
                   })}),
    # 萨麦尔（第五柱·暴怒）：红石巨怪（用户 2026-11-12 改定，原先给的红石傀儡不要）；红石部分按红色发光
    "samael_lord": dict(root="monstrosity", mesh=E + "RedStoneMonstrosity/SK_RedStoneMonstrosity", anims=["monstrosity"],
                        glow="red",
                        height=4.0, clips=[("RedStoneMonstrosity_Idle", "idle", True),
                                           ("RedStoneMonstrosity_Walk", "walk", True),
                                           ("RedStoneMonstrosity_BasicAttack", "cast", False),
                                           ("RedStoneMonstrosity_StrongAttack", "charge", False),
                                           ("RedStoneMonstrosity_SlamAttack_Composite", "summon", False),
                                           ("RedStoneMonstrosity_LavaAttack", "super", False),
                                           ("RedStoneMonstrosity_Awaken", "rise", False)]),
    # 贝利尔（第六柱·色欲）：腐化坩埚（用户选定 2026-11-12）。药水材质 MI_Goo 只有颜色（原作就是品红紫，
    # 线性 0.48/0/0.42），换成按柱色画的 16×16 药水贴图并发光。坩埚原作没有行走，自制「颠步」。
    "belial_lord": dict(root="batch3", mesh=E + "CauldronBoss/SK_CauldronBoss", anims=["batch3"],
                        material_override={"MI_Goo": ("dungeons_overrides/goo_belial.png", "dungeons_overrides/goo_belial.png")},
                        turn=180,       # 眼睛在 +z（同猪灵商人），显示时转过来
                        height=2.6, clips=[("CauldronBoss_Idle", "idle", True),
                                           ("CauldronBoss_BasicAttack_VFX", "cast", False),
                                           ("CauldronBoss_StrongAttack_VFX", "summon", False),
                                           ("CauldronBoss_IntenseSpin", "spin", False)],
                        # 颠步：整口锅左右摇、每步跳起一点（J_Root：z 正负 = 左右摇，位移 y = 上下）
                        custom_clips={"walk": dict(length=.8, loop=True, keys={
                            "J_Root": [(0, (0, 0, 0), (0, 0, 0)), (.2, (0, 0, 7), (0, .35, 0)), (.4, (0, 0, 0), (0, 0, 0)),
                                       (.6, (0, 0, -7), (0, .35, 0)), (.8, (0, 0, 0), (0, 0, 0))]})}),
    # 三位领主的罪仆（用户 2026-11-12：「把对应的罪仆模型也加上」），按领主的主题和柱色挑：
    "mammon_servant": dict(root="batch3", mesh=D4 + "Enemies/Piglin/SK_Piglin", anims=["batch3"],
                           # 金甲红衣的近战变体，最贴玛门的金橙
                           material_override={"MI_PiglinVariant0": "T_PiglinMeleeVariant2"},
                           turn=180,       # 猪灵也朝 +z
                           held_bone="J_R_Hand", height=2.0,
                           clips=[("Piglin_Idle", "idle", True), ("Piglin_WalkMelee", "walk", True),
                                  ("Piglin_MeleeAttack", "attack", False), ("Piglin_RangedAttack", "shoot", False)]),
    "belial_servant": dict(root="batch3", mesh=E + "Witch/SK_Witch", anims=["batch3"],
                           # 女巫和坩埚同一主题、同为紫色；手里的东西画在她捧药瓶的位置
                           held_bone="J_Potion", height=2.2,
                           clips=[("Witch_Idle", "idle", True), ("Witch_Walk", "walk", True),
                                  ("Witch_AttackThrow", "attack", False), ("Witch_Drink", "shoot", False)]),
    "samael_servant": dict(root="batch3", mesh="Dungeons/Content/Content_DLC3/Actors/Characters/Enemies/Illagers/Mountaineer/SK_Mountaineer_01",
                           anims=["batch3"],
                           # 红色变体（BP_MountaineerVariant2）：护肩、靴子按蓝图挂上；斧子不挂，手里画载体自己的武器
                           material_override={"M_Mountaineer": "T_MountaineerVariant2"},
                           blueprint="Dungeons/Content/Content_DLC3/Actors/Characters/Enemies/Illagers/Mountaineer/BP_MountaineerVariant2Character",
                           attach_names={"SM_Mountaineer_Boot_L": "l_boot", "SM_Mountaineer_Boot_R": "r_boot",
                                         "SM_Mountaineer_Shoulderpad_L": "l_pad", "SM_Mountaineer_Shoulderpad_R": "r_pad"},
                           attach_skip=["SM_Axe", "Backpack"], attach_materials_all="M_MountaineerVariant2",
                           held_bone="J_RWeapon", height=2.1, merge={"head": FACE},
                           clips=[("Mountaineer_Idle", "idle", True), ("Mountaineer_Walk", "walk", True),
                                  ("Mountaineer_Attack", "attack", False), ("Mountaineer_Brace", "shoot", False)]),
    # 米迦勒战的「众目」（docs/MICHAEL-DESIGN.md）：回响虚空的 Watchling（本体叫 WatcherOfTheEnd），
    # 网格是末影族共用的 SK_Enderling，动作是它自己的；身体保持原作的漆黑，眼睛换成米迦勒的圣焰橙红并发光（_tools/michael_boss_ref/watchling.png）
    "watchling": dict(root="watchling", mesh="Dungeons/Content/Content_DLC6/Actors/Characters/Enemies/Endling/SK_Enderling",
                      anims=["watchling"], height=2.9, glow="red", material_override={"MI_Endling": ("michael_boss_ref/watchling.png", None)},
                      clips=[("WatcherOfTheEnd_Idle", "idle", True), ("WatcherOfTheEnd_Walk", "walk", True),
                             ("WatcherOfTheEnd_BasicAttack", "attack", False), ("WatcherOfTheEnd_HeavyAttack", "heavy", False),
                             ("WatcherOfTheEnd_TeleportOut", "tp_out", False), ("WatcherOfTheEnd_TeleportIn", "tp_in", False),
                             ("WatcherOfTheEnd_Stun", "stun", True)]),
    # 第一柱 路西法的罪仆：苔藓骷髅（用户 2026-11-15）。原作没有单独网格，是普通骷髅换苔藓贴图；走路和出手用它自己的动作
    "lucifer_servant": dict(root="mossy", mesh=E + "Skeleton/SK_Skeleton", anims=["mossy"],
                            material_override={"MI_Skeleton": "T_MossySkeleton"},
                            held_bone="J_R_Weapon", height=2.0,
                            clips=[("Skeleton_Idle", "idle", True), ("MossySkeleton_Walk", "walk", True),
                                   ("MossySkeleton_BasicAttack", "shoot", False)],     # 拉弓放箭（原作）
                            # 骷髅原作只有弓箭动作；近战的罪仆用手摆的一记劈砍：右臂举过头顶，0.38 s 劈到身前
                            custom_clips={"attack": dict(length=.7, loop=False, keys={
                                "J_R_Arm": [(0, (0, 0, 0)), (.25, (150, 0, -8)), (.38, (40, 0, -4)), (.7, (0, 0, 0))],
                                "J_L_Spine": [(0, (0, 0, 0)), (.25, (0, 12, 0)), (.38, (0, -10, 0)), (.7, (0, 0, 0))]})}),
    # 用玩家英雄网格的几个（雅克、大卫、扫罗、老战友）都和玩家一样高：1.87 格（原版玩家模型 32 像素 × 0.9375；用户 2026-11-16）
    # 圣殿大团长雅克（docs/JACQUES-DESIGN.md）：原作玩家英雄网格 + 赫克斯皮肤 + 英雄铠甲（冠军铠甲第一个独特变体的贴图，
    # 网格是冠军铠甲的六件，各挂在玩家骨架的护甲插槽上）；坟墓克星挂右手武器插槽，竖琴弩四个上弦阶段挂左手武器插槽
    "jacques": dict(root="jacques", mesh=E.replace("Enemies/", "") + "Player/Master/SK_Player_Master", anims=["jacques"],
                    # 插槽取自原作骨架 Player_Master_Skeleton 的 SkeletalMeshSocket，组件变换取自 BP_ChampionsArmor；
                    # 竖琴弩先挂一副弓架骨骼 SK_BowRigTpose（BP_ScatterCrossbow_Unique1：左手武器插槽上，偏航 -90、翻转 180），
                    # 四个上弦阶段挂在弓架的 J_Bow1~4Socket 上（弓架根骨绕 X 转 -90）
                    socket_attach=[(n, "Dungeons/Content/Actors/Equipment/" + rel, bone, mat, xf) for n, rel, bone, mat, xf in (
                        ("armor", "Armor/ChampionsArmor/ChampionsArmor_ChampionsArmor", "J_Shoulders", "HEROS", []),
                        ("helmet", "Armor/ChampionsArmor/Helmet_ChampionsArmor", "J_Head", "HEROS",
                         [{"rel": {"RelativeScale3D": {"X": 1.1, "Y": 1.1, "Z": 1.1}}}]),
                        ("l_pauldron", "Armor/ChampionsArmor/L_Arm_ChampionsArmor", "J_L_Hand", "HEROS",
                         [{"rel": {"RelativeLocation": {"X": -4.0, "Y": -65.0, "Z": 0.0}}}]),
                        ("r_pauldron", "Armor/ChampionsArmor/R_Arm_ChampionsArmor", "J_R_Hand", "HEROS",
                         [{"rel": {"RelativeLocation": {"X": 7.0, "Y": 65.0, "Z": 0.0}}},
                          {"rel": {"RelativeRotation": {"Pitch": -2.7320755e-05, "Yaw": 3.096948e-05, "Roll": 179.99988}}}]),
                        ("l_greave", "Armor/ChampionsArmor/L_Leg_ChampionsArmor", "J_L_Foot", "HEROS", []),
                        ("r_greave", "Armor/ChampionsArmor/R_Leg_ChampionsArmor", "J_R_Foot", "HEROS",
                         [{"rel": {"RelativeRotation": {"Pitch": 0.0, "Yaw": 0.0, "Roll": 179.9998}}}]),
                        ("glaive", "MeleeWeapons/Glaive_Unique1/SM_Glaive_Unique1", "J_R_Weapon", "GLAIVE",
                         [{"rel": {"RelativeLocation": {"X": 0.0, "Y": 0.0165689, "Z": -6.0}}}])) + tuple(
                        ("harp%d" % k, "RangedWeapons/ScatterCrossbow_Unique1/SM_HarpCrossbow%d" % k, "J_L_Weapon", "HARP",
                         [{"rel": {"RelativeLocation": {"X": -2.8745855e-05, "Y": 35.12577, "Z": 15.999903},
                                   "RelativeRotation": {"Pitch": 0.0001844151, "Yaw": -89.999886, "Roll": 179.99997}}},
                          {"quat": [-0.70710678, 0.0, 0.0, 0.70710678]}]) for k in range(1, 5)) + (
                        # 英雄披风（BP_HeroCape：通用披风 SK_Cape 挂在肩膀骨上，材质换成金色披风 MI_RedstoneMonstrosityGoldenCape）。
                        # 原作披风靠物理下垂：静止姿势是平的，转 -90° 垂下，再绕竖轴转 180° 让带徽记的外面朝后
                        ("cape", "../Characters/Player/Capes/SK_Cape", "J_Shoulders", "CAPE", [{"rel": {"RelativeLocation": {"X": 0.0, "Y": 0.0, "Z": -26.0}}}, {"quat": [-0.70710678, 0.0, 0.0, 0.70710678]},
                         {"quat": [0.0, 0.0, 1.0, 0.0]}]),)],
                    material_override={"MI_Valorie": ("dungeons_overrides/jacques_hex.png", None), "HEROS": "T_HerosArmor", "GLAIVE": "T_Glaive_Unique1",
                                       "HARP": "T_HarpCrossbow", "CAPE": "T_RedstoneMonstrosityGoldenCape"},
                    height=1.87, merge={"head": ["mouth", "l_eye_pupil", "l_eye_iris", "r_eye_pupil", "r_eye_iris", "helmet",
                                                "jacques_head_000", "jacques_head_002", "jacques_head_011", "jacques_head_012",
                                                "jacques_head_armor_013"],
                                       "body": ["body_armor", "armor"], "l_arm": ["l_arm_armor", "l_pauldron", "jacques_l_pauldron_029"],
                                       "r_arm": ["r_arm_armor", "r_pauldron", "jacques_r_pauldron_031"],
                                       "l_leg": ["l_leg_armor", "l_greave"], "r_leg": ["r_leg_armor", "r_greave"]},
                    clips=[("Player_Master_Idle_Glaive", "idle", True), ("Player_Master_Walk_Glaive", "walk", True),
                           ("Player_Master_Run_Glaive", "run", True),
                           ("Player_Master_GlaiveUnique1Combo_Attack1", "slash1", False),
                           ("Player_Master_GlaiveUnique1Combo_Attack2", "slash2", False),
                           ("Player_Master_GlaiveUnique1Combo_Attack3", "sweep", False),
                           ("Player_Master_Crossbow_Load", "load", False), ("Player_Master_Crossbow_Charge", "charge", True),
                           ("Player_Master_Crossbow_Shoot", "shoot", False),
                           ("Player_Master_DodgeRollForward", "roll_f", False), ("Player_Master_DodgeRollBackward", "roll_b", False),
                           ("Player_Master_HornBlow", "horn", False), ("Player_Master_Gong", "gong", False),
                           ("Player_Master_Emote_MightySword", "mighty", False), ("Player_Master_ShowOff", "showoff", False),
                           ("Player_Master_Emote_KneelPose", "kneel", False), ("Player_Master_Emote_HeroPose", "hero", False),
                           ("Player_Master_TeleportInitiate_Start", "leap", False), ("Player_Master_TeleportLanding", "land", False),
                           ("Player_Master_Powershake", "curse", False), ("Player_Master_Stun", "stun", True),
                           ("Player_Master_GetHitFront", "hurt", False),
                           ("Player_Master_DownedFloor_Initiate", "fall", False), ("Player_Master_DownedFloored_Loop", "down", True)]),
    # 雅克战二阶段的大卫的幽灵：同一套原作英雄网格，不挂盔甲武器；贴图在 add_jacques_model.py 里转成半透明的白
    "david": dict(root="jacques", mesh=E.replace("Enemies/", "") + "Player/Master/SK_Player_Master", anims=["jacques"],
                  material_override={"MI_Valorie": "T_Hex"}, height=1.87,
                  merge={"head": ["mouth", "l_eye_pupil", "l_eye_iris", "r_eye_pupil", "r_eye_iris"]},
                  clips=[("Player_Master_Idle", "idle", True), ("Player_Master_Walk", "walk", True),
                         ("Player_Master_ShowOff", "throw", False), ("Player_Master_Emote_HeroPose", "hero", False)]),
    # 达阿特的影子（docs/DAATH-DESIGN.md）：原作玩家英雄网格，皮肤压成近黑（daath_ref/shadow_skin.png）。
    # 盔甲、武器、头颅都是玩家自己的物品，由 add_daath_model.py 挂上；动作表在 daath_spec.py（约九十段，全是原作玩家动作）
    "daath": dict(root="daath", mesh=E.replace("Enemies/", "") + "Player/Master/SK_Player_Master", anims=["daath"],
                  material_override={"MI_Valorie": ("daath_ref/shadow_skin.png", None)}, height=1.87, held_bone="J_R_Weapon",
                  merge={"head": ["mouth", "l_eye_pupil", "l_eye_iris", "r_eye_pupil", "r_eye_iris"]},
                  clips=DAATH.CLIPS),
    # 疯人王扫罗（docs/SAUL-DESIGN.md）：原作玩家英雄网格 + 织网者皮肤（wiki 叫 Web Crawler，本体是 Skins/Spider）
    # + 坚毅铠甲（强化锁甲的独特变体 BP_ReinforcedMail_Unique1：头盔、胸甲、护腿沿用强化锁甲网格，左右臂甲是它自己的，
    # 贴图全部换成 T_StalwartArmor）；千刀挂右手武器插槽（一代细剑 SM_Rapier，贴图按千刀配色重画）。
    # 插槽取自 Player_Master_Skeleton 的 SkeletalMeshSocket，组件变换取自 BP_ReinforcedMail_Unique1 / BP_Rapier。
    # 二阶段碎掉 helmet、l_pauldron（左臂甲连护肩，原作是一件），所以它们不并进别的部件
    "saul": dict(root="saul", mesh=E.replace("Enemies/", "") + "Player/Master/SK_Player_Master", anims=["saul", "jacques"],
                 socket_attach=[(n, "Dungeons/Content/" + rel, bone, mat, xf) for n, rel, bone, mat, xf in (
                     ("armor", "Actors/Equipment/Armor/ReinforcedMail/ReinforcedMailArmor_ReinforcedMail", "J_Shoulders", "STALWART",
                      [{"rel": {"RelativeRotation": {"Pitch": 0.0, "Yaw": 1.201487e-07, "Roll": 0.0},
                                "RelativeScale3D": {"X": 1.0, "Y": 1.0, "Z": 1.2}}}]),
                     ("helmet", "Actors/Equipment/Armor/ReinforcedMail/Helmet_ReinforcedMail", "J_Head", "STALWART",
                      [{"rel": {"RelativeScale3D": {"X": 1.05, "Y": 1.05, "Z": 1.05}}}]),
                     # 臂甲：原作网格是护肩 + 手上一大一小两块叠起来的护手，原点在手骨上、沿 -Y 往肩膀建好，挂手骨插槽。
                     # 英雄的手臂方块本身也跟着手骨走，所以臂甲挂手骨才和手臂一起动（挂上臂骨会在细剑招式里离开手臂）。
                     # 右臂甲在蓝图里是 Y 轴镜像（缩放 -1）；generic.with_attachments 把镜像折进网格、骨只取旋转
                     ("l_pauldron", "Actors/Equipment/Armor/ReinforcedMail_Unique1/L_Arm_StalwartArmor", "J_L_Hand", "STALWART",
                      [{"rel": {"RelativeRotation": {"Pitch": 0.00019598007, "Yaw": -179.9999, "Roll": 179.99997}}}]),
                     ("r_pauldron", "Actors/Equipment/Armor/ReinforcedMail_Unique1/R_Arm_StalwartArmor", "J_R_Hand", "STALWART",
                      [{"rel": {"RelativeRotation": {"Pitch": 0.00026750565, "Yaw": -179.99995, "Roll": 179.99998},
                                "RelativeScale3D": {"X": 1.0, "Y": -1.0, "Z": 1.0}}}]),
                     ("l_greave", "Actors/Equipment/Armor/ReinforcedMail/L_LegGuard_ReinforcedMail", "J_L_Foot", "STALWART",
                      [{"rel": {"RelativeLocation": {"X": 0.0, "Y": 0.0, "Z": -1.0}}}]),
                     ("r_greave", "Actors/Equipment/Armor/ReinforcedMail/R_LegGuard_ReinforcedMail", "J_R_Foot", "STALWART",
                      [{"rel": {"RelativeLocation": {"X": 0.0, "Y": 0.0, "Z": 1.0}, "RelativeScale3D": {"X": 1.0, "Y": -1.0, "Z": -1.0}}}]),
                     ("rapier", "Patch2/Actors/Equipment/MeleeWeapons/Rapier/SM_Rapier", "J_R_Weapon", "RAPIER",
                      [{"rel": {"RelativeLocation": {"X": 0.0, "Y": 0.0165689, "Z": -6.0}}},
                       {"rel": {"RelativeLocation": {"X": -3.9999695, "Y": 1.0803342e-05, "Z": -7.2436533},
                                "RelativeRotation": {"Pitch": 0.0, "Yaw": -90.00018, "Roll": 2.8501184e-08}}}]))],
                 material_override={"MI_Valorie": "T_Spider_Skin", "STALWART": "T_StalwartArmor",
                                    "RAPIER": ("saul_boss_ref/thousand_cuts.png", None)},
                 height=1.87, merge={"head": ["mouth", "l_eye_pupil", "l_eye_iris", "r_eye_pupil", "r_eye_iris",
                                             "saul_head_000", "saul_head_002", "saul_head_011", "saul_head_012", "saul_head_armor_013"],
                                    "body": ["body_armor", "armor"], "l_arm": ["l_arm_armor"],
                                    "l_pauldron": ["saul_l_pauldron_030"],
                                    "r_arm": ["r_arm_armor", "r_pauldron", "saul_r_pauldron_032"],
                                    "l_leg": ["l_leg_armor", "l_greave"], "r_leg": ["r_leg_armor", "r_greave"]},
                 clips=[("Player_Master_Idle_Katana", "idle", True), ("Player_Master_Walk_Katana", "walk", True),
                        ("Player_Master_Run_Katana", "run", True),
                        ("Player_Master_RapierCombo1Start", "thrust", False),
                        ("Player_Master_RapierCombo2_Left", "left", False),
                        ("Player_Master_RapierCombo2_Right", "right", False),
                        ("Player_Master_RapierCombo2_MiddleDouble", "double", False),
                        ("Player_Master_RapierCombo5Final", "final", False),
                        ("Player_Master_DodgeRollForward", "roll_f", False), ("Player_Master_DodgeRollBackward", "roll_b", False),
                        ("Player_Master_DodgeRollSidewayLeft", "roll_l", False), ("Player_Master_DodgeRollSidewayRight", "roll_r", False),
                        ("Player_Master_Emote_MightySword", "mighty", False), ("Player_Master_Emote_TheTwirl", "twirl", False),
                        ("Player_Master_Emote_Shadowboxing", "shadow", False),
                        ("Player_Master_Emote_KneelPose", "kneel", False), ("Player_Master_Emote_HeroPose", "hero", False),
                        ("Player_Master_Powershake", "web", False), ("Player_Master_ShowOff", "showoff", False),
                        ("Player_Master_TeleportInitiate_Start", "vanish", False), ("Player_Master_TeleportLanding", "land", False),
                        ("Player_Master_Stun", "stun", True), ("Player_Master_GetHitFront", "hurt", False),
                        ("Player_Master_DownedFloor_Initiate", "fall", False), ("Player_Master_DownedFloored_Loop", "down", True)]),
    # 扫罗对着空气练剑时对面那个看不见的老战友：原作英雄（默认皮肤），贴图在 add_saul_model.py 里转成半透明的白
    # 也用作扫罗的残影（残影剑阵、第三课·残影）：手里同一把千刀，贴图一起转成半透明的白
    "saul_ghost": dict(root="saul", mesh=E.replace("Enemies/", "") + "Player/Master/SK_Player_Master", anims=["saul"],
                       socket_attach=[("rapier", "Dungeons/Content/Patch2/Actors/Equipment/MeleeWeapons/Rapier/SM_Rapier", "J_R_Weapon", "RAPIER",
                                       [{"rel": {"RelativeLocation": {"X": 0.0, "Y": 0.0165689, "Z": -6.0}}},
                                        {"rel": {"RelativeLocation": {"X": -3.9999695, "Y": 1.0803342e-05, "Z": -7.2436533},
                                                 "RelativeRotation": {"Pitch": 0.0, "Yaw": -90.00018, "Roll": 2.8501184e-08}}}])],
                       material_override={"RAPIER": ("saul_boss_ref/thousand_cuts.png", None)},
                       height=1.87, merge={"head": ["mouth", "l_eye_pupil", "l_eye_iris", "r_eye_pupil", "r_eye_iris"]},
                       clips=[("Player_Master_Idle_Katana", "idle", True), ("Player_Master_Walk_Katana", "walk", True),
                              ("Player_Master_Emote_Shadowboxing", "shadow", False),
                              ("Player_Master_RapierCombo1Start", "thrust", False), ("Player_Master_RapierCombo5Final", "final", False),
                              ("Player_Master_DodgeRollForward", "roll_f", False)]),
    # 篡夺者（达里奥·所罗门）一阶段：附魔师（docs/USURPER-DESIGN.md）。附魔书是骨骼模型自带的，随「强化」飞出
    "usurper": dict(root="usurper", mesh=E + "Illagers/Enchanter/SK_IllagerEnchanter", anims=["usurper"],
                    glow="cyan", height=2.4, merge={"head": FACE},
                    clips=[("IllagerEnchanter_Idle", "idle", True),
                           ("IllagerEnchanter_Walk", "walk", True),
                           ("IllagerEnchanter_BasicAttack", "attack", False),     # 0.43 s 合书出手
                           ("IllagerEnchanter_Enchance", "enchant", False),       # 0.14 s 抛书，1.63 s 灌注
                           ("IllagerEnchanter_Novelty", "rise", False)]),        # 0.33 s 抛书，登场
    "tower_guard": dict(root="towerguard", mesh=E + "Illagers/RoyalGuard/SK_IllagerRoyalGuard", anims=["towerguard"],
                        blueprint=E + "Illagers/TowerGuard/BP_IllagerTowerGuardCharacter",
                        attach_names={"Shield": "shield", "SM_Mace": "spear", "SM_DesertArmor_Helmet": "helmet",
                                      "Armor_IllagerRoyalGuard": "armor", "L_Arm_IllagerRoyalGuard": "l_pauldron",
                                      "R_Arm_IllagerRoyalGuard": "r_pauldron", "L_Leg_IllagerRoyalGuard": "l_greave",
                                      "R_Leg_IllagerRoyalGuard": "r_greave"},
                        attach_skip=["Backpack"],
                        # 盾牌网格默认材质 MI_TowerGuardShieldEnchanted2 没导出；同贴图的 Enchanted 版
                        attach_materials={"shield": "MI_TowerGuardShieldEnchanted"},
                        height=2.31, merge={"head": FACE + ["helmet"]},
                        clips=[("IllagerRoyalGuard_Idle", "idle", True),
                               ("IllagerRoyalGuard_Walk_VFX", "walk", True),
                               ("TowerGuard_BasicAttack", "attack", False),
                               ("TowerGuard_ChargeAttack_Charging", "charge", True),
                               ("TowerGuard_ChargeAttack_NormalStop", "normal_stop", False),
                               ("TowerGuard_ChargeAttack_CollidedStop", "collide_stop", False),
                               ("TowerGuard_ChargeAttack_ShieldBroken", "shield_break", False),
                               ("IllagerRoyalGuard_Stun", "stun", True)]),
    # 圣卫的另外两种（用户 2026-11-14）：重盾（皇家卫兵原样）与术士（终末灾厄村民）
    "royal_guard": dict(root="royalguard", mesh=E + "Illagers/RoyalGuard/SK_IllagerRoyalGuard", anims=["royalguard"],
                        blueprint=E + "Illagers/RoyalGuard/BP_IllagerRoyalGuardCharacter",
                        attach_names={"Shield": "shield", "SM_Mace": "mace", "SM_DesertArmor_Helmet": "helmet",
                                      "Armor_IllagerRoyalGuard": "armor", "L_Arm_IllagerRoyalGuard": "l_pauldron",
                                      "R_Arm_IllagerRoyalGuard": "r_pauldron", "L_Leg_IllagerRoyalGuard": "l_greave",
                                      "R_Leg_IllagerRoyalGuard": "r_greave"},
                        height=2.31, merge={"head": FACE + ["helmet"]},
                        clips=[("IllagerRoyalGuard_Idle", "idle", True),
                               ("IllagerRoyalGuard_Walk", "walk", True),
                               ("IllagerRoyalGuard_BasicAttack", "attack", False),
                               ("IllagerRoyalGuard_Stun", "stun", True)]),
    # 终末灾厄村民：原作只在回响虚空结尾的预渲染动画里出现，本体没有它的模型或贴图（2026-11-14 扫过全部 354 张角色贴图）。
    # 开发者说它像唤魔者；网格与动作用原作唤魔者，袍子按动画改成褐色、去掉兜帽（dungeons_overrides/make_end_illager.py）
    "end_illager": dict(root="evoker", mesh=E + "Illagers/Evoker/SK_IllagerEvoker", anims=["evoker"],
                        material_override={"M_IllagerEvoker": ("dungeons_overrides/end_illager.png", None)},
                        height=2.2, merge={"head": FACE},
                        clips=[("IllagerEvoker_Idle", "idle", True),
                               ("IllagerEvoker_Walk", "walk", True),
                               ("IllagerEvoker_BasicAttack", "cast", False),
                               ("IllagerEvoker_StrongAttack", "strong", False),
                               ("IllagerEvoker_Summoning", "summon", False),
                               ("IllagerEvoker_NoveltyAnimation", "rise", False),
                               ("IllagerEvoker_GetHitFront", "hurt", False),
                               ("IllagerEvoker_Stun", "stun", True)]),
}


def custom_animation(doc, name, spec):
    """A hand-keyed Blockbench animation: keys {bone: [(time, rotation or None[, position])]}; rotations
    are degrees added to the bone's rest, positions an offset in the parent's space (display_mob)."""
    groups = {g["name"]: g for g in doc["groups"]}
    animators = {}
    for bone, keys in spec["keys"].items():
        frames = []
        for i, key in enumerate(keys):
            t, rot = key[0], key[1]
            pos = key[2] if len(key) > 2 else None
            for channel, value in (("rotation", rot), ("position", pos)):
                if value is None:
                    continue
                frames.append({"channel": channel, "data_points": [{a: str(v) for a, v in zip("xyz", value)}],
                               "uuid": G.uid("%s/%s/%s/%s/%d" % (doc["name"], name, bone, channel, i)), "time": float(t),
                               "color": -1, "interpolation": "linear"})
        animators[groups[bone]["uuid"]] = {"name": bone, "type": "bone", "rotation_global": False,
                                           "quaternion_interpolation": False, "keyframes": frames}
    return {"uuid": G.uid(doc["name"] + ":custom:" + name), "name": "animation." + name,
            "loop": "loop" if spec["loop"] else "once", "override": False, "length": spec["length"], "snapping": 24,
            "selected": False, "saved": True, "path": "", "scope": 0, "anim_time_update": "", "blend_weight": "",
            "start_delay": "", "loop_delay": "", "animators": animators}


def source_height_cm(root, mesh):
    rel = mesh.split("/")[-1]
    src, _ = G.load_any(UP / root / "assets" / (mesh + ".glb"), UP / root / "metadata" / mesh / (rel + ".meta.json"))
    v = src["vertices_ue_cm"]
    return float(v[:, 2].max() - v[:, 2].min())


def build(key):
    cfg = MODELS[key]
    root, mesh = UP / cfg["root"], cfg["mesh"]
    rel = mesh.split("/")[-1]
    glb = root / "assets" / (mesh + ".glb")
    meta = root / "metadata" / mesh / (rel + ".meta.json")
    out = HERE / ("%s_dungeons_ref" % key)
    if out.exists():
        shutil.rmtree(out)
    attachments = []
    if cfg.get("blueprint"):
        bone_names = [b["name"] for b in G.read(meta)["bones"]]
        attachments = BP.blueprint_attachments(root, cfg["blueprint"], bones=bone_names,
                                               socket_roots=[UP / r / "metadata" for r in cfg.get("sockets", [])],
                                               names=cfg.get("attach_names"), skip=cfg.get("attach_skip", ()))
        for a in attachments:
            a["material"] = cfg.get("attach_materials", {}).get(a["name"], cfg.get("attach_materials_all", a["material"]))
    # 挂在骨架插槽上的静态网格（原作玩家英雄的护甲、武器插槽）：(部件名, 导出根下的网格路径, 骨, 材质键[, 变换链])
    # 变换链按原作数据逐层相乘：{"rel": 组件或插槽的 Relative* 属性} 用 blueprint.relative，{"quat": 骨的静止旋转}
    for name, rel, bone, mat, *xf in cfg.get("socket_attach", ()):
        m = np.eye(4)
        for step in (xf[0] if xf else ()):
            if "rel" in step:
                m = m @ BP.relative(step["rel"])
            else:
                q = np.eye(4)
                q[:3, :3] = G.quat_matrix(step["quat"])
                m = m @ q
        attachments.append({"name": name, "mesh": root / "assets" / (rel + ".glb"), "bone": bone, "matrix": m,
                            "material": mat, "component": name, "attach": bone})
    if cfg.get("orb"):
        o = cfg["orb"]
        from PIL import Image as _Image
        tex = HERE / o["texture"]
        tw, th = _Image.open(tex).size
        spin = np.eye(4); spin[:3, 3] = o["offset"]
        tilt = np.eye(4); tilt[:3, :3] = Rotation.from_euler("xyz", o["tilt"], degrees=True).as_matrix()
        attachments.append({"name": "orb_spin", "bone": o["bone"], "matrix": spin, "child": {"name": "orb", "matrix": tilt},
                            "cubes": [{"size": c, "uv": uv} for c, uv in o["cubes"]], "texture_size": (tw, th),
                            "material": "__orb__", "attach": o["bone"], "mesh": "synthetic orb"})
        cfg.setdefault("material_override", {})["__orb__"] = (o["texture"], None)     # glows whole, below
    override = {}
    for mat, tex in cfg.get("material_override", {}).items():
        if isinstance(tex, tuple):      # files under _tools (a texture we drew)
            override[mat] = tuple(HERE / t if t else None for t in tex)
        else:                           # another exported texture of the same mob (a colour variant)
            override[mat] = (next((root / "assets").rglob(tex + ".png")), None)
    doc, report = G.convert(glb, meta, root, out, name=key, unit_scale=UNIT, glow_color=GLOW.get(cfg.get("glow")),
                            attachments=attachments, material_textures_override=override)
    if cfg.get("orb"):
        # every face of the orb is full-bright (glow_bones lists the plane groups under the orb bone)
        orb_groups = [g["name"] for g in doc["groups"] if g["name"].startswith(key + "_orb_")]
        glow = json.loads((out / "glow_bones.json").read_text(encoding="utf-8"))
        (out / "glow_bones.json").write_text(json.dumps(sorted(set(glow) | set(orb_groups))) + chr(10), encoding="utf-8")
    anims = cfg["anims"] if isinstance(cfg["anims"], list) else [cfg["anims"]]
    retarget = {}
    for name, rt in cfg.get("retarget", {}).items():
        src = rt["source_meta"]
        retarget[name] = dict(rt, source_bones=G.read(root / "metadata" / src / (src.split("/")[-1] + ".meta.json"))["bones"])
    doc, clips = G.author(doc, meta, glb, [UP / a / "metadata" for a in anims], cfg["clips"], retarget=retarget)
    if cfg.get("orb"):
        # the orb turns about the staff (UE +z of the socket is Blockbench local +y) in every clip;
        # whole quarter turns per clip so the loop has no seam (the cubes repeat every 90 degrees)
        uuid = next(g["uuid"] for g in doc["groups"] if g["name"] == "orb_spin")
        for anim in doc["animations"]:
            turns = max(1, round(cfg["orb"]["spin"] * anim["length"] / 90))
            anim["animators"][uuid] = {"name": "orb_spin", "type": "bone", "rotation_global": False,
                                       "quaternion_interpolation": False, "keyframes": [
                {"channel": "rotation", "data_points": [{"x": "0", "y": str(90 * turns * f), "z": "0"}],
                 "uuid": G.uid("%s/orb/%s/%d" % (key, anim["name"], f)), "time": anim["length"] * f,
                 "color": -1, "interpolation": "linear"} for f in (0, 1)]}
    for name, spec in cfg.get("custom_clips", {}).items():
        doc["animations"].append(custom_animation(doc, name, spec))
        clips.append({"clip": name, "source": "custom", "seconds": spec["length"], "loop": spec["loop"],
                      "ticks": int(spec["length"] * 20 + .999), "max_bone_error_px": 0., "max_vertex_error_px": 0.,
                      "notifies": []})
    (out / (key + ".bbmodel")).write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    h = source_height_cm(cfg["root"], mesh)
    model_scale = cfg["height"] * 16 / (h * UNIT)
    config = {"model_scale": model_scale, "height_blocks": cfg["height"], "source_height_cm": h, "turn": cfg.get("turn", 0),
              "merge": cfg.get("merge", {}), "held_bone": cfg.get("held_bone"),
              "attachments": [{k: str(v) if k == "mesh" else v for k, v in a.items() if k not in ("matrix", "child")} for a in attachments],
              "source": {"mesh": mesh, "export_root": str(root)}, "clips": clips, "conversion": report}
    (out / "model_config.json").write_text(json.dumps(config, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (out / "SOURCES.md").write_text(
        "# 来源\n\n从《Minecraft Dungeons》本体提取（只读），经 `_tools/dungeons_conversion/generic.py` 转换。\n\n"
        "- 网格：`%s`\n- 动作：%s\n\n版权归 Mojang 所有；本项目非商业，与 Mojang 无关联。\n"
        % (mesh + "".join("、`%s`（挂 %s）" % (Path(a["mesh"]).stem, a["attach"]) for a in attachments),
           "、".join("`%s`→%s" % (c[0], c[1]) for c in cfg["clips"])), encoding="utf-8")
    print("%-10s parts %-3d elements %-4d atlas %s scale %.4f  %s" % (
        key, report["display_parts"], report["elements"], report["atlas"], model_scale,
        ", ".join("%s %.2fs %.2fpx" % (c["clip"], c["seconds"], c["max_vertex_error_px"]) for c in clips)))
    return out


if __name__ == "__main__":
    for k in (sys.argv[1:] or list(MODELS)):
        build(k)
