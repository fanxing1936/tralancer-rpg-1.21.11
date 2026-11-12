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

UP = Path(r"D:\agent\dungeons_extract\upgrade")
E = "Dungeons/Content/Actors/Characters/Enemies/"
UNIT = 0.0192
D5 = "Dungeons/Content/Content_DLC5/Actors/Characters/Enemies/"
# 眼、眉、鼻并进头部：少几个实体（dungeons_variant.fold 检查能否合并）
FACE = ["nose", "l_eyepupil", "l_eyeiris", "r_eyepupil", "r_eyeiris", "l_eyebrow", "r_eyebrow"]
GLOW = {"cyan": lambda c: (c[:, 2] > 150) & (c[:, 1] > 110) & (c[:, 0] < 110)}

MODELS = {
    "leviathan": dict(root="necromancer", mesh=E + "SkeletonNecromancer/SK_SkeletonNecromancer", anims="necromancer",
                      # 用户要杖头发青光（2026-11-02 起的要求）；原作没有自发光图，按青色取
                      glow="cyan",
                      height=3.71, clips=[("SkeletonNecromancer_Idle", "idle", True),
                                          ("SkeletonNecromancer_Walk", "walk", True),
                                          ("SkeletonNecromancer_BasicAttack", "cast", False),
                                          ("SkeletonNecromancer_StrongAttack", "summon", False),
                                          ("SkeletonNecromancer_Novelty", "rise", False)]),
    "beelzebub": dict(root="nameless", mesh=E + "NamelessKing/SK_NamelessKing", anims="nameless",
                      height=3.71, clips=[("NamelessKing_Walk", "idle", True),
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
}


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
            a["material"] = cfg.get("attach_materials", {}).get(a["name"], a["material"])
    doc, report = G.convert(glb, meta, root, out, name=key, unit_scale=UNIT, glow_color=GLOW.get(cfg.get("glow")),
                            attachments=attachments)
    anims = cfg["anims"] if isinstance(cfg["anims"], list) else [cfg["anims"]]
    doc, clips = G.author(doc, meta, glb, [UP / a / "metadata" for a in anims], cfg["clips"])
    (out / (key + ".bbmodel")).write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    h = source_height_cm(cfg["root"], mesh)
    model_scale = cfg["height"] * 16 / (h * UNIT)
    config = {"model_scale": model_scale, "height_blocks": cfg["height"], "source_height_cm": h,
              "merge": cfg.get("merge", {}), "held_bone": cfg.get("held_bone"),
              "attachments": [{k: str(v) if k == "mesh" else v for k, v in a.items() if k != "matrix"} for a in attachments],
              "source": {"mesh": mesh, "export_root": str(root)}, "clips": clips, "conversion": report}
    (out / "model_config.json").write_text(json.dumps(config, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (out / "SOURCES.md").write_text(
        "# 来源\n\n从《Minecraft Dungeons》本体提取（只读），经 `_tools/dungeons_conversion/generic.py` 转换。\n\n"
        "- 网格：`%s`\n- 动作：%s\n\n版权归 Mojang 所有；本项目非商业，与 Mojang 无关联。\n"
        % (mesh + "".join("、`%s`（挂 %s）" % (Path(a["mesh"]).stem, a["attach"]) for a in attachments),
           "、".join("`%s`→%s" % (s, n) for s, n, _ in cfg["clips"])), encoding="utf-8")
    print("%-10s parts %-3d elements %-4d atlas %s scale %.4f  %s" % (
        key, report["display_parts"], report["elements"], report["atlas"], model_scale,
        ", ".join("%s %.2fs %.2fpx" % (c["clip"], c["seconds"], c["max_vertex_error_px"]) for c in clips)))
    return out


if __name__ == "__main__":
    for k in (sys.argv[1:] or list(MODELS)):
        build(k)
