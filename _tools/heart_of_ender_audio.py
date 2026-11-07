"""动作声音登记；正式 HE 薄生成器读取并传入 Mob。

文件身份来自 Wiki Sounds 原链接；具体动作同步点是作者推断，原 GIF 无音轨。
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOUND_DIR = HERE / "heart_of_ender_ref" / "sounds"

def numbered(stem, count):
    return [f"{stem}-{i:03d}.ogg" for i in range(1, count+1)]

SOUNDS = {
    "vessel_voice": (("末影之心：低吼", "Heart of Ender growls"), numbered("Sfx_boss_ArchvesselVesselVoice", 6), None),
    "inner_voice": (("大灾厄村民：低吟", "Arch-Illager moans"), numbered("Sfx_boss_ArchvesselArchieVoice", 10), None),
    "death": (("末影之心：消散", "Heart of Ender fades"), ["Sfx_boss_ArchvesselDeath.ogg"], None),
    "fourside": (("末影之心：十字光束蓄势", "Heart of Ender readies cross beams"), numbered("Sfx_boss_ArchvesselFourside", 4), None),
    "hurt": (("末影之心：受伤", "Heart of Ender hurts"), numbered("Sfx_boss_ArchvesselHurt", 8), None),
    "mortar": (("末影之心：吐息", "Heart of Ender launches a barrage"), numbered("Sfx_boss_ArchvesselMortarBarrage", 4), None),
    "mortar_land": (("末影弹：落地", "Ender mortar lands"), numbered("Sfx_boss_ArchvesselMortarLand", 3), None),
    "mortar_explode": (("末影弹：碎裂", "Ender mortar shatters"), [f"Sfx_mob_witchBottleBreak-{i:03d}_soundWave.ogg" for i in range(1, 4)], None),
    "orb_death": (("末影弹：消失", "Ender orb disappears"), ["Sfx_boss_archVesselOrbDeath-003.ogg"], None),
    "step": (("末影之心：爬行", "Heart of Ender crawls"), numbered("Sfx_boss_ArchvesselStep", 4), None),
    "tele_in": (("末影之心：升起", "Heart of Ender rises"), ["Sfx_boss_ArchvesselTeleIn.ogg"], None),
    "tele_out": (("末影之心：沉地", "Heart of Ender sinks"), ["Sfx_boss_ArchvesselTeleOut.ogg"], None),
    "ambient_loop": (("末影之心：环境低鸣", "Heart of Ender hums"), ["Sfx_env_archVessel2dAmbientLoop.ogg"], None),
}

CUES = {
    "idle": [],
    "walk": [(float(t), "step", 0.65, 1.0) for t in range(8)],
    # 作者推断的 A/C/E 与 B/D/F 交替支撑，每组三肢落地只放一声；不是原作步点。
    "mortar": [(1.2, "mortar", 1.2, 1.0)],
    "cross_beam": [(1.0, "fourside", 1.2, 1.0)],
    "sink": [(0.4, "tele_out", 1.0, 1.0)],
    "rise": [(0.2, "tele_in", 1.0, 1.0)],
    "death": [],
}
ENTER_CUES = {
    "idle": [("vessel_voice", 0.7, 1.0)],
    "walk": [("inner_voice", 0.6, 1.0)],
    "death": [("death", 1.2, 1.0)],
}

UNBOUND = {
    "hurt": "不制作受伤或玩法逻辑；留作归档",
    "mortar_land": "弹体和落地特效不属于本次模型动作",
    "mortar_explode": "弹体和爆炸特效不属于本次模型动作",
    "orb_death": "弹体不属于本次模型动作",
    "ambient_loop": "避免缺少停止机制时反复叠加环境长音；当前只归档",
}

def validate():
    files = [p for event in SOUNDS.values() for p in event[1]]
    assert len(files) == 47 and len(set(files)) == 47
    assert all((SOUND_DIR / p).is_file() for p in files)
    for clip, cues in CUES.items():
        assert all(event in SOUNDS for _, event, _, _ in cues), clip
    for clip, cues in ENTER_CUES.items():
        assert all(event in SOUNDS for event, _, _ in cues), clip
    return {"sound_events": len(SOUNDS), "files": len(files), "status": "sources verified; bound event subset consumed by add_heart_of_ender.py"}

if __name__ == "__main__":
    print(validate())
