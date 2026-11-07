"""Arch-Visage：只读已归档配置/模型，接入独立调试外观与动作。"""
import json
import sys
from pathlib import Path

from display_mob import Mob
from ender_debug_model import build_debug

HERE = Path(__file__).resolve().parent
REF = HERE / "arch_visage_ref"


def main(rp=None, dp=None):
    rp, dp = rp or HERE.parent / "resourcepack", dp or HERE.parent / "rpg"
    config = json.loads((REF / "config.json").read_text(encoding="utf-8"))
    ground = config["research_ground_y"]
    mob = Mob(
        key="arch_visage", label="灾厄面容", generator="add_arch_visage.py",
        bbmodel=str(REF / "arch_visage.bbmodel"), parts=config["parts"],
        glow=config.get("glow", []), carrier="minecraft:armor_stand",
        seat=config.get("seat", ground / 16.), model_scale=3., tag="rpg.av", score="rpg_av",
        clips=config["clips"], sounds=config.get("sounds", {}),
        sound_dir=str((REF / config.get("sound_dir", "../heart_of_ender_ref/sounds")).resolve()),
        cues=config.get("cues", {}), enter_cues=config.get("enter_cues", {}),
    )
    return build_debug(mob, rp, dp, ground, config.get("debug_recommended_clip", "idle"))


if __name__ == "__main__":
    main(*sys.argv[1:])
