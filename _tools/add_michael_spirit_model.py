"""Install Michael's original-source appearance and animations into the TRA packs."""

import argparse
import json
from pathlib import Path

import dungeons_variant
from display_mob import Mob, build, hook_tag, snbt_components, wf, wj, write_rig_runtime

HERE = Path(__file__).resolve().parent
KEY = "michael_spirit"
REF = HERE / f"{KEY}_dungeons_ref"
TAG = "rpg.mis"
CARRIER = f"rpg.{KEY}.carrier"
PREVIEW = f"rpg.{KEY}.preview"
SPINE = f"rpg.{KEY}.spine"
DUAL_RIB = f"rpg.{KEY}.dual_rib"
VINDICATOR = "minecraft:vindicator"
FN = f"rpg:{KEY}"
WEAPONS = ("spine", "rib_attack", "rib")
SPINE_CLIPS = {"idle", "walk", "run", "slash1", "slash2", "sweep"}
RIB_LOCOMOTION = {"rib_idle", "rib_walk", "rib_run"}
RIB_CLIPS = RIB_LOCOMOTION | {f"rib_slash{i}" for i in range(1, 7)}


def configured_mob(ref):
    cfg = json.loads((ref / "model_config.json").read_text(encoding="utf-8"))
    parts = json.loads((ref / "parts.json").read_text(encoding="utf-8"))
    walking = {"idle", "walk", "run"} | RIB_LOCOMOTION
    clips = [(row["clip"], 2 if row["clip"] in walking else 1, row["loop"])
             for row in cfg["clips"]]
    if not (SPINE_CLIPS | RIB_CLIPS).issubset(name for name, _, _ in clips):
        raise ValueError("Michael needs locomotion and the original attack sequence for each loadout")
    if not set(WEAPONS).issubset(row["name"] for row in parts):
        raise ValueError("Michael needs the spine and both hand positions for the rib")
    mob = Mob(key=KEY, label="米迦勒灵体", generator=Path(__file__).name,
              bbmodel=str(ref / f"{KEY}.bbmodel"), parts=[], glow=(),
              seat=2.0, tag=TAG, score="rpg_mis", clips=clips,
              model_scale=cfg["model_scale"], face_rotation=True, tick_rounding="ceil")
    mob.turn = cfg.get("turn", 0)
    parts = dungeons_variant.fold(mob, parts, cfg.get("merge", {}))
    mob.parts = [(row["name"], row["bones"]) for row in parts]
    return mob


def write_runtime(mob, first):
    folder = Path(mob.func)
    carrier_sel = f"type={VINDICATOR},tag={CARRIER}"

    def write(name, lines):
        wf(str(folder / f"{name}.mcfunction"), lines)

    weapon_parts = {}
    for part, _ in first:
        role = next((weapon for weapon in WEAPONS if part == weapon or part.startswith(f"{KEY}_{weapon}_")), None)
        if role:
            weapon_parts[part] = role

    dress = [
        f"execute unless entity @s[{carrier_sel},tag=!{TAG}] run return 0",
        f"data modify storage {FN} mount.uuid set from entity @s UUID",
        f"tag @s add {TAG}",
        "effect give @s minecraft:invisibility infinite 0 true",
    ]
    for part, transform in first:
        tags = json.dumps([f"{TAG}.part", f"{TAG}.p.{part}", f"{TAG}.new"], separators=(",", ":"))
        model = "rpg:empty" if part in weapon_parts else f"{FN}/{part}"
        dress.append(
            f"summon minecraft:item_display ~ ~ ~ {{Tags:{tags},"
            f'item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"{model}"}}}},'
            f'item_display:"none",teleport_duration:1,interpolation_duration:1,view_range:2f,'
            f"brightness:{{sky:15,block:15}},transformation:{snbt_components(mob, transform)}}}")
    new = f"type=minecraft:item_display,tag={TAG}.new,distance=..1"
    write("dress", dress + [
        f"execute as @e[{new}] run function {FN}/mount with storage {FN} mount",
        f"tag @e[{new}] remove {TAG}.new",
        f"data remove storage {FN} mount",
        f"execute if entity @s[tag={DUAL_RIB}] run function {FN}/weapon/dual_rib",
        f"execute unless entity @s[tag={DUAL_RIB}] run function {FN}/weapon/spine",
        f"function {FN}/anim/init",
        f"function {FN}/anim/enter/idle",
    ])
    write("mount", [f"$ride @s mount @e[{carrier_sel},nbt={{UUID:$(uuid)}},limit=1]"])
    write("undress", [
        f"execute on passengers if entity @s[type=minecraft:item_display,tag={TAG}.part] run kill @s",
        f"tag @s remove {TAG}",
        "effect clear @s minecraft:invisibility",
        *[f"scoreboard players reset @s {objective}" for objective in (
            mob.clip_score, mob.t_score, *[f"{mob.score}_{key}" for key in ("mv", "mc", "x", "z")])],
    ])
    write_rig_runtime(mob, [
        f"execute as @e[type={VINDICATOR},tag={TAG},tag=!{CARRIER}] at @s run function {FN}/undress",
        f"execute as @e[{carrier_sel},tag=!{TAG}] at @s run function {FN}/dress",
        f"execute as @e[{carrier_sel},tag={TAG}] at @s run function {FN}/follow",
    ])
    follow = folder / "follow.mcfunction"
    follow.write_text(follow.read_text(encoding="utf-8").replace(
        "execute on passengers run rotate @s ~ 0",
        f"execute on passengers if entity @s[type=minecraft:item_display,tag={TAG}.part] run rotate @s ~ 0"),
        encoding="utf-8", newline="\n")
    pred = Path(mob.dp) / "data" / "rpg" / "predicate" / KEY
    wj(str(pred / "invisible.json"), {
        "condition": "minecraft:entity_properties", "entity": "this",
        "predicate": {"effects": {"minecraft:invisibility": {}}},
    })
    write("tick_late", [
        f"execute as @e[{carrier_sel},tag={TAG}] unless predicate {FN}/invisible "
        "run effect give @s minecraft:invisibility infinite 0 true",
    ])
    hook_tag(mob.dp, "tick", f"{FN}/tick_late", False)

    def weapon_lines(visible):
        return [f"execute on passengers if entity @s[type=minecraft:item_display,tag={TAG}.p.{part}] "
                f'run data modify entity @s item.components."minecraft:item_model" set value '
                f'"{FN + "/" + part if role in visible else "rpg:empty"}"' for part, role in weapon_parts.items()]

    states = {"spine": ("spine",), "dual_rib": ("rib", "rib_attack")}
    remove_stale(folder / "weapon", set(states), ".mcfunction")
    remove_stale(folder / "play", {name for name, _, _ in mob.clips}, ".mcfunction")
    for state, visible in states.items():
        write(f"weapon/{state}", weapon_lines(visible))
    for clip, _, _ in mob.clips:
        profile = f",tag={DUAL_RIB}" if clip in RIB_CLIPS else f",tag=!{DUAL_RIB}" if clip in SPINE_CLIPS else ""
        if profile:
            entry = folder / "anim" / "enter" / f"{clip}.mcfunction"
            lines = entry.read_text(encoding="utf-8").splitlines()
            guard = (f"execute if entity @s[tag={DUAL_RIB}] run return run function {FN}/anim/enter/rib_idle"
                     if clip == "idle" else f"execute unless entity @s[{profile.lstrip(',')}] run return 0")
            lines.insert(1, guard)
            wf(str(entry), lines)
        write(f"play/{clip}", [
            f"execute if entity @s[{carrier_sel},tag={TAG}{profile}] run return run function {FN}/anim/enter/{clip}",
        ])
        write(f"debug/play/{clip}", [
            f"execute as @e[{carrier_sel},tag={TAG}{profile},sort=nearest,limit=1,distance=..32] "
            f"at @s run function {FN}/play/{clip}",
        ])
    clips = {clip: i for i, (clip, _, _) in enumerate(mob.clips)}
    init = folder / "anim" / "init.mcfunction"
    init_lines = init.read_text(encoding="utf-8").splitlines()
    init_lines.insert(2, f"execute if entity @s[tag={DUAL_RIB}] run scoreboard players set @s "
                        f"{mob.clip_score} {clips['rib_idle']}")
    wf(str(init), init_lines)
    tick = folder / "anim" / "tick.mcfunction"
    tick_lines = tick.read_text(encoding="utf-8").splitlines()
    locomotion_at = next(i for i, line in enumerate(tick_lines) if "/anim/stride" in line) + 1
    tick_lines[locomotion_at:locomotion_at] = [
        f"execute if score @s {mob.clip_score} matches {clips['rib_idle']} if score @s {mob.score}_mv matches 1.. "
        f"run return run function {FN}/anim/enter/rib_walk",
        f"execute if score @s {mob.clip_score} matches {clips['rib_walk']} if score @s {mob.score}_mv matches 0 "
        f"run return run function {FN}/anim/enter/rib_idle",
    ]
    wf(str(tick), tick_lines)
    for name, profile in (("spine", SPINE), ("dual_rib", DUAL_RIB)):
        write(f"debug/preview_{name}", [
            f'summon {VINDICATOR} ~ ~ ~ {{Tags:["{CARRIER}","{PREVIEW}","{profile}"],NoAI:1b,Silent:1b,'
            'PersistenceRequired:1b,Invulnerable:1b,CustomName:{text:"米迦勒",color:"#FF3300"},'
            'active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b}]}'
        ])
    write("debug/preview", [f"function {FN}/debug/preview_spine"])
    write("debug/clear", [
        f"execute as @e[{carrier_sel},tag={PREVIEW}] run function {FN}/debug/clear_one",
    ])
    write("debug/clear_one", [
        f"function {FN}/undress",
        "kill @s",
    ])


def generate(resourcepack, datapack, ref=REF):
    mob = configured_mob(ref)
    baked, first = build(mob, str(resourcepack), str(datapack))
    parts = {part for part, _ in mob.parts}
    for directory in ("items", "models"):
        remove_stale(resourcepack / "assets" / "rpg" / directory / KEY, parts, ".json")
    for part, _ in mob.parts:
        path = resourcepack / "assets" / "rpg" / "models" / KEY / f"{part}.json"
        model = json.loads(path.read_text(encoding="utf-8"))
        for element in model["elements"]:
            element["shade"] = False
        wj(str(path), model)
    write_runtime(mob, first)
    return mob, baked


def remove_stale(folder, expected_names, suffix):
    for file in folder.glob(f"*{suffix}"):
        if file.stem not in expected_names:
            file.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("resourcepack", nargs="?", type=Path, default=HERE.parent / "resourcepack")
    parser.add_argument("datapack", nargs="?", type=Path, default=HERE.parent / "rpg")
    parser.add_argument("--ref", type=Path, default=REF)
    args = parser.parse_args()
    generate(args.resourcepack, args.datapack, args.ref)


if __name__ == "__main__":
    main()
