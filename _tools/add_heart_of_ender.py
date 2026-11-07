"""末影之心：模型、动作与声音。玩法在 add_pope_fight.py，这里不绑定已有生物。"""
import json
import sys
from pathlib import Path

from display_mob import Mob
from ender_debug_model import build_debug
from heart_of_ender_audio import SOUNDS, CUES, ENTER_CUES, SOUND_DIR

HERE = Path(__file__).resolve().parent
REF = HERE / "heart_of_ender_ref"
GROUND_Y = -4.66381
MODEL_SCALE = 2.5       # Boss 体型：约 6.6 格高；教皇战的判定体和锚点都按它算
NAMES = ("idle", "walk", "mortar", "cross_beam", "sink", "rise", "death")
FIGHT_EVENTS = ("hurt", "mortar_land", "mortar_explode")    # 动作之外，由教皇战直接播放


def main(rp=None, dp=None):
    rp, dp = rp or HERE.parent / "resourcepack", dp or HERE.parent / "rpg"
    geometry = json.loads((REF / "m2_geometry/geometry_spec.json").read_text(encoding="utf-8"))
    events = {e for cues in CUES.values() for _, e, _, _ in cues}
    events.update(e for cues in ENTER_CUES.values() for e, _, _ in cues)
    events.update(FIGHT_EVENTS)
    mob = Mob(
        key="heart_of_ender", label="末影之心", generator="add_heart_of_ender.py",
        bbmodel=str(REF / "heart_of_ender.bbmodel"),
        parts=geometry["parts"], glow=set(), carrier="minecraft:armor_stand",
        # Marker盔甲架乘客座高0；将研究地面平面放到调用点。
        seat=GROUND_Y / 16. * MODEL_SCALE, model_scale=MODEL_SCALE, tag="rpg.he", score="rpg_he",
        clips=[(name, 1, name in ("idle", "walk")) for name in NAMES],
        sounds={e: SOUNDS[e] for e in sorted(events)}, sound_dir=str(SOUND_DIR),
        cues=CUES, enter_cues=ENTER_CUES,
    )
    return build_debug(mob, rp, dp, GROUND_Y)


if __name__ == "__main__":
    main(*sys.argv[1:])
