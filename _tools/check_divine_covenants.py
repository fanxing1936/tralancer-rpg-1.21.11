# -*- coding: utf-8 -*-
"""Static audit for the Old/New divine covenants and the Daath route.

The checks intentionally cover both the generator's shared item source and the
generated datapack.  That makes this script a regression gate for gameplay,
HUD integration and catalogue output, rather than only a file-presence check.
"""

import importlib.util
import io
import json
import os
import re
import sys


HERE = os.path.dirname(os.path.abspath(__file__))
DP = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "../rpg")
RP = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else "../resourcepack")
F = os.path.join(DP, "data/rpg/function")
LOOT = os.path.join(DP, "data/rpg/loot_table")
problems = []
_problem_set = set()
_function_cache = {}


def problem(message):
    if message not in _problem_set:
        _problem_set.add(message)
        problems.append(message)


def read_path(path, label=None):
    if not os.path.isfile(path):
        problem("missing file: " + (label or path))
        return ""
    try:
        with io.open(path, encoding="utf-8") as handle:
            return handle.read()
    except Exception as exc:
        problem("cannot read %s: %s" % (label or path, exc))
        return ""


def function_path(rel):
    return os.path.join(F, rel.replace("/", os.sep))


def read(rel):
    if rel not in _function_cache:
        path = function_path(rel)
        if not os.path.isfile(path):
            problem("missing function: " + rel)
            _function_cache[rel] = ""
        else:
            _function_cache[rel] = read_path(path, rel)
    return _function_cache[rel]


def active_lines(blob):
    return [line.strip() for line in blob.splitlines()
            if line.strip() and not line.lstrip().startswith("#")]


def require(blob, needle, message):
    if needle not in blob:
        problem(message)


def read_json(root, rel):
    path = os.path.join(root, rel.replace("/", os.sep))
    if not os.path.isfile(path):
        problem("missing JSON: " + rel)
        return None
    try:
        with io.open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except Exception as exc:
        problem("invalid JSON %s: %s" % (rel, exc))
        return None


def tag_values(document):
    if not isinstance(document, dict):
        return set()
    values = set()
    for value in document.get("values", []):
        if isinstance(value, str):
            values.add(value)
        elif isinstance(value, dict) and isinstance(value.get("id"), str):
            values.add(value["id"])
    return values


# -------------------------------------------------------------------------
# Runtime/objective wiring and the original Old -> Daath -> New route.

score = read("command/soreboard.mcfunction")
for name in (
        "rpg_lt_divine", "rpg_lt_div_cd", "rpg_lt_div_max", "rpg_lt_div_t",
        "rpg_lt_regen", "rpg_lt_auth", "rpg_lt_auth_t", "rpg_lt_judge",
        "rpg_lt_hp", "rpg_lt_max",
        "rpg_lt_owner", "rpg_lt_gather", "rpg_lt_claim", "rpg_lt_migrate"):
    if "scoreboard objectives add %s dummy" % name not in score:
        problem("missing objective: " + name)
if "scoreboard players set #hud_mini rpg_hud 5" not in score:
    problem("five-slot HUD constant is not initialized: #hud_mini rpg_hud 5")

runtime = read("exorcism.mcfunction")
for needle in ("function rpg:divine/player_tick", "function rpg:divine/judgment/scan",
               "function rpg:divine/gather/step"):
    require(runtime, needle, "runtime lacks: " + needle)
if "function rpg:ritual/life_tree/covenant_tick" in runtime:
    problem("retired all-round blessing is still active")

complete = read("ritual/life_tree/complete.mcfunction")
if not all(needle in complete for needle in
           ("give_old_covenant", "rpg_lt_claim", "旧约")):
    problem("ten-node completion does not uniquely award Old Covenant")
if "give_new_covenant" in complete:
    problem("ten-node completion still awards New Covenant directly")

route = read("ritual/life_tree/input.mcfunction")
for needle in ("rpg_true_cross:1b", "^-1.580", "tag=rpg.lt.complete",
               "function rpg:divine/gather/start"):
    require(route, needle, "Daath route lacks: " + needle)

gather = "\n".join(read(rel) for rel in (
    "divine/gather/start.mcfunction", "divine/gather/one.mcfunction",
    "divine/gather/finish.mcfunction", "divine/gather/reward.mcfunction"))
for needle in ("rpg.ritual.life_tree.cross", "facing entity",
               "rpg_lt_gather matches 24..", "kill @s", "new_covenant"):
    require(gather, needle, "Daath transformation lacks: " + needle)
if ("rpg.ritual.life_tree.cross" not in read("ritual/life_tree/clear.mcfunction") or
        "rpg.ritual.life_tree.cross" not in
        read("ritual/life_tree/clear_all.mcfunction")):
    problem("tree clearing can leak an in-progress True Cross display")


# -------------------------------------------------------------------------
# Dedicated divine-light damage type and Resistance bypass.

damage_type = read_json(DP, "data/rpg/damage_type/divine_light.json")
if isinstance(damage_type, dict):
    if damage_type.get("message_id") != "divine_light":
        problem("rpg:divine_light has the wrong message_id")
    if damage_type.get("scaling") != "never":
        problem("rpg:divine_light must use scaling=never")
    if damage_type.get("exhaustion") != 0 and damage_type.get("exhaustion") != 0.0:
        problem("rpg:divine_light must have zero exhaustion")

resistance_tag = read_json(
    DP, "data/minecraft/tags/damage_type/bypasses_resistance.json")
if isinstance(resistance_tag, dict):
    if resistance_tag.get("replace") is True:
        problem("bypasses_resistance must merge instead of replacing vanilla values")
    if "rpg:divine_light" not in tag_values(resistance_tag):
        problem("rpg:divine_light is absent from bypasses_resistance")

for rel in ("divine/damage/execute.mcfunction",
            "divine/damage/macro.mcfunction"):
    blob = read(rel)
    require(blob, "rpg:divine_light", rel + " does not use the dedicated damage type")

damage_dir = function_path("divine/damage")
if os.path.isdir(damage_dir):
    for root, _dirs, names in os.walk(damage_dir):
        for name in names:
            if not name.endswith(".mcfunction"):
                continue
            path = os.path.join(root, name)
            for number, line in enumerate(active_lines(read_path(path)), 1):
                if "minecraft:magic" in line:
                    rel = os.path.relpath(path, F).replace(os.sep, "/")
                    problem("legacy magic damage remains in %s:%d" % (rel, number))


# -------------------------------------------------------------------------
# Stage-one damage must be visible but must not bypass the 175 HP floor.

stage1 = read("inquest/stage1.mcfunction")
stage1_active = "\n".join(active_lines(stage1))
for needle in ("data get entity @s Health 100", "matches ..17499",
               "data merge entity @s {Health:175f}"):
    require(stage1_active, needle, "stage1 175 HP floor lacks: " + needle)
if "Health:420f" in stage1_active:
    problem("stage1 still resets the boss to 420 HP every tick")
for line in active_lines(stage1):
    match = re.search(r"effect give @s minecraft:resistance \d+ (\d+)", line)
    if match and int(match.group(1)) > 0:
        problem("stage1 still applies Resistance above level I")

stage1_apply = read("divine/damage/apply_stage1.mcfunction")
for needle in ("scoreboard players remove @s rpg_lt_hp 17500",
               "@s rpg_lt_max > @s rpg_lt_hp",
               "function rpg:divine/damage/apply_score"):
    require(stage1_apply, needle, "stage1 damage cap lacks: " + needle)

target_routes = (
    ("divine/damage/old_target.mcfunction", "old", 20),
    ("divine/damage/new_target.mcfunction", "beam", 25),
    ("divine/damage/field_target.mcfunction", "field", 15),
    ("divine/judgment/strike.mcfunction", "judgment", 20),
)
for target_rel, _ritual_name, _gain in target_routes:
    target = read(target_rel)
    require(target, "if score @s rpg_ex_stage matches 1 run function rpg:divine/damage/apply_stage1",
            target_rel + " does not route stage1 through the 175 HP cap")
    require(target, "unless score @s rpg_ex_stage matches 1 run function rpg:divine/damage/apply_score",
            target_rel + " does not retain normal damage outside stage1")

old_target = read("divine/damage/old_target.mcfunction")
execute_lines = [line for line in active_lines(old_target)
                 if "function rpg:divine/damage/execute" in line]
if not execute_lines or any("unless score @s rpg_ex_stage matches 1" not in line
                            for line in execute_lines):
    problem("Old Covenant execute can bypass the stage1 175 HP protection")


# -------------------------------------------------------------------------
# A bound boss converts all four divine attacks into ritual stability.

for target_rel, ritual_name, gain in target_routes:
    target = read(target_rel)
    route_call = ("execute if entity @s[tag=rpg.exorcism.bound] run return run "
                  "function rpg:divine/ritual/%s" % ritual_name)
    require(target, route_call,
            "%s does not short-circuit bound bosses into ritual/%s" %
            (target_rel, ritual_name))

    ritual_rel = "divine/ritual/%s.mcfunction" % ritual_name
    ritual = read(ritual_rel)
    for needle in ("tag @s add rpg.divine.ritual_subject", "tag=rpg.rite.anchor",
                   "rpg_rite_id", "function rpg:divine/ritual/%s_apply" % ritual_name,
                   "tag @s remove rpg.divine.ritual_subject"):
        require(ritual, needle, ritual_rel + " lacks: " + needle)
    if " rpg:divine_light" in ritual:
        problem(ritual_rel + " damages a bound boss instead of converting to stability")

    apply_rel = "divine/ritual/%s_apply.mcfunction" % ritual_name
    apply_blob = read(apply_rel)
    require(apply_blob, "scoreboard players add @s rpg_ex_stab %d" % gain,
            "%s does not add the intended %d stability" % (apply_rel, gain))
    require(apply_blob, "rpg_ex_stab matches 101..",
            apply_rel + " does not cap ritual stability at 100")


# -------------------------------------------------------------------------
# Target coverage, dual New Covenant skills and exact cooldown maxima.

old_invoke = read("divine/invoke_old.mcfunction")
beam_invoke = read("divine/invoke_new_beam.mcfunction")
field_invoke = read("divine/invoke_new_field.mcfunction")


def fly_target_count(blob, target_function):
    return sum(1 for line in active_lines(blob)
               if "tag=rpg.demon.fly" in line and target_function in line)


if fly_target_count(old_invoke, "rpg:divine/damage/old_target") < 1:
    problem("Old Covenant does not cover rpg.demon.fly")
if fly_target_count(beam_invoke, "rpg:divine/damage/new_target") < 20:
    problem("Creation Light does not cover rpg.demon.fly across all 20 beam samples")
if fly_target_count(field_invoke, "rpg:divine/damage/field_target") < 1:
    problem("Eden field does not cover rpg.demon.fly")

old_power = old_invoke + read("divine/damage/old_target.mcfunction")
for needle in ("distance=..10", "rpg_lt_hp <=", "#five rpg_lt_max",
               "damage/execute", "rpg.demon.minion"):
    require(old_power, needle, "Old Covenant power lacks: " + needle)

new_dispatch = read("divine/invoke_new.mcfunction")
predicate_line = ("execute if predicate rpg:sneaking run return run function "
                  "rpg:divine/invoke_new_field")
require(new_dispatch, predicate_line,
        "New Covenant crouch dispatch does not use the stable sneaking predicate")
if 'Pose:"CROUCHING"' in new_dispatch:
    problem("New Covenant still relies on the broken Pose NBT crouch test")
try:
    sneaking = read_json(os.path.join(DP, "data/rpg/predicate"), "sneaking.json")
    if sneaking.get("predicate", {}).get("flags", {}).get("is_sneaking") is not True:
        problem("rpg:sneaking predicate does not test is_sneaking=true")
except Exception as exc:
    problem("missing/invalid rpg:sneaking predicate: " + str(exc))
require(new_dispatch, "function rpg:divine/invoke_new_beam",
        "New Covenant lacks the normal Creation Light branch")

new_target = read("divine/damage/new_target.mcfunction")
for needle in ("^20", "tag=rpg.demon.minion", "tag=rpg.divine.hit"):
    require(beam_invoke, needle, "Creation Light beam lacks: " + needle)
for needle in ("rpg_lt_max /= #four", "scoreboard players add @s rpg_lt_max 1500"):
    require(new_target, needle, "Creation Light damage lacks: " + needle)

field_target = read("divine/damage/field_target.mcfunction")
for needle in ("distance=..8", "tag=rpg.demon.minion"):
    require(field_invoke, needle, "Eden field lacks: " + needle)
for needle in ("rpg_lt_max *= #three", "rpg_lt_max /= #twenty",
               "scoreboard players add @s rpg_lt_max 1000"):
    require(field_target, needle, "Eden field damage lacks: " + needle)


def check_cooldown(rel, expected):
    found = {"cd": [], "max": []}
    pattern = re.compile(
        r"^scoreboard players set @s rpg_lt_div_(cd|max) (-?\d+)$")
    for line in active_lines(read(rel)):
        match = pattern.match(line)
        if match:
            found[match.group(1)].append(int(match.group(2)))
    for key in ("cd", "max"):
        if found[key] != [expected]:
            problem("%s must set rpg_lt_div_%s exactly once to %d (found %s)" %
                    (rel, key, expected, found[key]))


for cooldown_rel, ticks in (
        ("divine/invoke_old.mcfunction", 600),
        ("divine/invoke_new_beam.mcfunction", 400),
        ("divine/invoke_new_field.mcfunction", 600),
        ("divine/borrow.mcfunction", 300)):
    check_cooldown(cooldown_rel, ticks)

player_tick = read("divine/player_tick.mcfunction")
for needle in ("rpg_lt_divine matches 1 run scoreboard players set @s rpg_lt_div_max 600",
               "rpg_lt_divine matches 2 run scoreboard players set @s rpg_lt_div_max 400",
               "unless score @s rpg_lt_div_cd matches 1.. run scoreboard players set @s rpg_lt_div_max 0"):
    require(player_tick, needle, "divine cooldown persistence lacks: " + needle)


# -------------------------------------------------------------------------
# Unified five-slot cooldown HUD and one-line actionbar ownership.


def hud_branch_score(line):
    match = re.search(r"\brpg_hud_p matches (\d+)\b", line)
    if match:
        return int(match.group(1))
    match = re.search(r"scores=\{[^}]*\brpg_hud_p=(\d+)\b", line)
    return int(match.group(1)) if match else None


def check_five_slot_hud(rel):
    branches = {}
    for line in active_lines(read(rel)):
        if "data modify storage rpg:hud" not in line or not ("▰" in line or "▱" in line):
            continue
        score_value = hud_branch_score(line)
        if score_value is None:
            problem(rel + " has a cooldown bar branch without an exact score")
            continue
        branches.setdefault(score_value, []).append(line)
    if set(branches) != set(range(6)):
        problem("%s must expose exactly HUD branches 0..5 (found %s)" %
                (rel, sorted(branches)))
    for value, lines in branches.items():
        if len(lines) != 1:
            problem("%s has %d branches for HUD value %d" % (rel, len(lines), value))
            continue
        if value not in range(6):
            # The branch-set error above already reports obsolete 6..10 rows.
            continue
        line = lines[0]
        filled = line.count("▰")
        empty = line.count("▱")
        if filled != value or empty != 5 - value:
            problem("%s value %d draws %d filled + %d empty slots, expected %d + %d" %
                    (rel, value, filled, empty, value, 5 - value))


for hud_rel in (
        "hud/pbar.mcfunction", "hud/divine_old.mcfunction",
        "hud/divine_beam.mcfunction", "hud/divine_field.mcfunction",
        "hud/divine_borrow.mcfunction"):
    check_five_slot_hud(hud_rel)

pbar = read("hud/pbar.mcfunction")
if "#hud_mini rpg_hud" not in pbar or "#hud_seg rpg_hud" in pbar:
    problem("seven-pillar cooldown HUD is not scaled with the shared five-slot constant")

divine_bar = read("hud/divine_bar.mcfunction")
for needle in ("rpg_lt_div_max", "#hud_mini rpg_hud",
               "rpg_lt_div_max matches 300", "rpg_lt_div_max matches 600",
               "function rpg:hud/divine_old", "function rpg:hud/divine_borrow",
               "function rpg:hud/divine_field", "function rpg:hud/divine_beam"):
    require(divine_bar, needle, "divine five-slot HUD dispatcher lacks: " + needle)

divine_root = function_path("divine")
if os.path.isdir(divine_root):
    actionbar_re = re.compile(r"(?:^|\s)title\s+\S+\s+actionbar(?:\s|$)")
    for root, _dirs, names in os.walk(divine_root):
        for name in names:
            if not name.endswith(".mcfunction"):
                continue
            path = os.path.join(root, name)
            for number, line in enumerate(active_lines(read_path(path)), 1):
                if actionbar_re.search(line):
                    rel = os.path.relpath(path, F).replace(os.sep, "/")
                    problem("direct actionbar bypasses the shared HUD in %s:%d" %
                            (rel, number))

cooling = read("divine/cooling.mcfunction")
for line in active_lines(cooling):
    if re.search(r"(?:^|\s)tellraw(?:\s|$)", line):
        problem("divine/cooling.mcfunction must not emit tellraw spam")
if "playsound" not in cooling:
    problem("divine/cooling.mcfunction lacks non-text cooldown feedback")


# -------------------------------------------------------------------------
# Passive effects, seven-pillar borrowing and renunciation.

old_tick = read("divine/old_tick.mcfunction")
if "400.." not in old_tick or "regeneration 1 0" not in old_tick:
    problem("Old Covenant 20-second regeneration pulse is malformed")
new_tick = read("divine/new_tick.mcfunction")
for effect in ("blindness", "darkness"):
    if "effect clear @s minecraft:" + effect not in new_tick:
        problem("New Covenant does not prevent " + effect)
if "rpg_lt_auth_t matches 40.." not in new_tick or "rpg_taint 0" not in new_tick:
    problem("New Covenant authority regeneration or corruption replacement is malformed")
if "scoreboard players set @s rpg_lt_auth 100" in active_lines(new_tick):
    problem("New Covenant refills authority every tick, making authority costs meaningless")
sign_new = read("divine/sign_new.mcfunction")
if "scoreboard players set @s rpg_lt_auth 100" not in sign_new:
    problem("signing New Covenant does not initialize authority to 100")

arm = read("divine/judgment/arm.mcfunction")
strike = read("divine/judgment/strike.mcfunction")
scan = read("divine/judgment/scan.mcfunction")
for needle in ("rpg_lt_auth matches 25..", "scoreboard players remove @s rpg_lt_auth 25",
               "scoreboard players set @s rpg_lt_judge 600"):
    require(arm, needle, "Final Judgment arming lacks: " + needle)
for needle in ("tag=rpg.hurt", "tag=rpg.demon", "rpg.demon.minion", "rpg.demon.fly"):
    require(scan, needle, "Final Judgment hit scan lacks: " + needle)
for needle in ("rpg_lt_hp <= @s rpg_lt_max", "#five rpg_lt_max",
               "scoreboard players add @s rpg_lt_max 1000", "minecraft:regeneration",
               "function rpg:divine/damage/execute"):
    require(strike, needle, "Final Judgment strike lacks: " + needle)

gift = read("divine/gift.mcfunction")
receive = read("divine/gift/receive.mcfunction")
for needle in ("rpg_lt_auth matches 35..", "scoreboard players remove @s rpg_lt_auth 35",
               "distance=..12", "function rpg:divine/gift/receive"):
    require(gift, needle, "Son's Gift lacks: " + needle)
for needle in ("minecraft:instant_health", "minecraft:regeneration",
               "minecraft:absorption", "minecraft:resistance"):
    require(receive, needle, "Son's Gift healing lacks: " + needle)

panel_tick = read("panel/tick.mcfunction")
panel_pact = read("panel/pact.mcfunction")
for value, function in ((9, "rpg:divine/judgment/arm"), (10, "rpg:divine/gift")):
    require(panel_tick, "rpg_panel matches %d run function %s" % (value, function),
            "player panel lacks authority dispatch %d" % value)
    require(panel_pact, "/trigger rpg_panel set %d" % value,
            "covenant panel lacks authority button %d" % value)
for rel in ("divine/authority/no_covenant.mcfunction",
            "divine/authority/insufficient.mcfunction",
            "divine/judgment/already_armed.mcfunction",
            "divine/gift.mcfunction", "divine/gift/no_target.mcfunction",
            "divine/gift/receive.mcfunction", "panel/pact.mcfunction"):
    if '"italic":true' in read(rel):
        problem("new authority UI contains off-style italic text: " + rel)

pact = read("pact/trigger.mcfunction")
borrow = read("divine/borrow.mcfunction")
if "rpg_lt_divine matches 2" not in pact or borrow.count("function rpg:pact/p") != 7:
    problem("New Covenant seven-pillar borrowing is incomplete")
if "rpg_taint" in borrow:
    problem("borrowed seven-pillar power still adds corruption")

renounce = read("divine/renounce.mcfunction")
if ("rpg.totem.lit" not in read("divine/trigger.mcfunction") or
        "rpg_lt_divine 0" not in renounce):
    problem("lit-totem renunciation route is incomplete")

status = read("hud/status.mcfunction")
authority = read("hud/authority.mcfunction")
if ("function rpg:hud/authority" not in status or
        "权柄" not in authority or "完整度" not in authority):
    problem("authority HUD does not replace corruption HUD")


# -------------------------------------------------------------------------
# One shared covenant component source for loot, commands and reissued books.

generator_path = os.path.join(HERE, "add_divine_covenants.py")
generator_source = read_path(generator_path, "_tools/add_divine_covenants.py")
tree_match = re.search(
    r"def build_tree_rewards_and_cross\(\):(?P<body>.*?)(?=\ndef [a-zA-Z_])",
    generator_source, re.S)
if not tree_match:
    problem("cannot locate build_tree_rewards_and_cross in the generator")
else:
    tree_body = tree_match.group("body")
    for needle in ("covenant_components(1, False)",
                   "covenant_components(2, False)"):
        require(tree_body, needle,
                "tree rewards do not use shared component source: " + needle)


def loot_components(document):
    if not isinstance(document, dict):
        return None
    for pool in document.get("pools", []):
        for entry in pool.get("entries", []):
            for function in entry.get("functions", []):
                if function.get("function") == "minecraft:set_components":
                    return function.get("components")
    return None


generator = None
try:
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    spec = importlib.util.spec_from_file_location(
        "rpg_divine_covenant_generator_for_audit", generator_path)
    generator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generator)
except Exception as exc:
    problem("cannot load shared covenant component source: " + str(exc))

for kind, name in ((1, "old_covenant"), (2, "new_covenant")):
    rel = "ritual/life_tree/%s.json" % name
    document = read_json(LOOT, rel)
    components = loot_components(document)
    if components is None:
        problem(rel + " lacks minecraft:set_components")
        continue
    required_keys = {
        "minecraft:custom_name", "minecraft:lore",
        "minecraft:custom_model_data", "minecraft:enchantment_glint_override",
        "minecraft:max_stack_size", "minecraft:food", "minecraft:consumable",
        "minecraft:custom_data",
    }
    missing_keys = required_keys.difference(components)
    if missing_keys:
        problem("%s lacks shared components: %s" %
                (rel, ", ".join(sorted(missing_keys))))
    if any(":" not in key for key in components):
        problem(rel + " contains an unnamespaced item component key")
    if generator is not None:
        expected = generator.covenant_components(kind, False)
        if components != expected:
            problem(rel + " diverges from covenant_components(%d, False)" % kind)

if generator is not None:
    extra = read("command/give/extra.mcfunction")
    sign_old = read("divine/sign_old.mcfunction")
    sign_new = read("divine/sign_new.mcfunction")
    reissue = read("divine/reissue.mcfunction")
    command_locations = (
        (1, False, extra, "command/give/extra.mcfunction"),
        (2, False, extra, "command/give/extra.mcfunction"),
        (1, True, sign_old, "divine/sign_old.mcfunction"),
        (2, True, sign_new, "divine/sign_new.mcfunction"),
        (1, True, reissue, "divine/reissue.mcfunction"),
        (2, True, reissue, "divine/reissue.mcfunction"),
        (1, False, renounce, "divine/renounce.mcfunction"),
        (2, False, renounce, "divine/renounce.mcfunction"),
    )
    parsed_variants = set()
    for kind, signed, blob, label in command_locations:
        expected_item = generator.covenant_item(kind, signed)
        if expected_item not in blob:
            problem("%s diverges from covenant_item(%d, %s)" %
                    (label, kind, signed))
        variant = (kind, signed)
        if variant in parsed_variants:
            continue
        parsed_variants.add(variant)
        try:
            import snbt
            start = expected_item.find("[")
            _block, end = snbt.parse_component_block(expected_item, start)
            if end != len(expected_item):
                problem("covenant_item(%d, %s) has trailing component syntax" %
                        (kind, signed))
        except Exception as exc:
            problem("invalid shared covenant_item(%d, %s) syntax: %s" %
                    (kind, signed, exc))


# -------------------------------------------------------------------------
# The catalogue must keep divine covenants and Kabbalah ritual items separate.

box_catalogue = read("command/give/box.mcfunction")
box_lines = box_catalogue.splitlines()


def box_section(label):
    indexes = [index for index, line in enumerate(box_lines)
               if line.startswith("## %s --" % label)]
    if len(indexes) != 1:
        problem("command/give/box must contain one independent %s section" % label)
        return []
    start = indexes[0] + 1
    end = len(box_lines)
    for index in range(start, len(box_lines)):
        if box_lines[index].startswith("## "):
            end = index
            break
    gives = [line for line in box_lines[start:end] if line.startswith("give ")]
    if not gives:
        problem("command/give/box %s section contains no shulker box" % label)
    return gives


divine_boxes = box_section("上位契约")
kabbalah_boxes = box_section("卡巴拉秘仪")
divine_blob = "\n".join(divine_boxes)
kabbalah_blob = "\n".join(kabbalah_boxes)

for line in divine_boxes:
    if "light_blue_shulker_box" not in line or '"text":"[上位契约]"' not in line:
        problem("上位契约 must use its own labelled light-blue shulker box")
for marker in ("rpg_divine_old:1b", "rpg_divine_new:1b"):
    require(divine_blob, marker, "上位契约 shulker box lacks: " + marker)

for line in kabbalah_boxes:
    if "magenta_shulker_box" not in line or '"text":"[卡巴拉秘仪]"' not in line:
        problem("卡巴拉秘仪 must use its own labelled magenta shulker box")
for marker in ("minecraft:flower_banner_pattern", "rpg_kabbalah_contract:1b",
               "minecraft:iron_nugget", "rpg_true_cross:1b"):
    require(kabbalah_blob, marker, "卡巴拉秘仪 shulker box lacks: " + marker)
for number in range(1, 11):
    marker = "rpg_sephirah:%db" % number
    require(kabbalah_blob, marker,
            "卡巴拉秘仪 shulker box lacks Sephirah %d" % number)
if any("rpg_kabbalah_contract:1b" in line or "rpg_sephirah:" in line or
       "rpg_true_cross:1b" in line for line in divine_boxes):
    problem("Kabbalah ritual items leaked into the 上位契约 shulker box")
if any("rpg_divine_old:1b" in line or "rpg_divine_new:1b" in line
       for line in kabbalah_boxes):
    problem("divine covenant books leaked into the 卡巴拉秘仪 shulker box")


# -------------------------------------------------------------------------
# Resource-pack presence and model dispatch.

for name in ("old_covenant", "new_covenant", "true_cross"):
    for rel in ("assets/rpg/textures/item/%s.png" % name,
                "assets/rpg/models/item/%s.json" % name):
        path = os.path.join(RP, rel.replace("/", os.sep))
        if not os.path.isfile(path) or os.path.getsize(path) == 0:
            problem("missing resource: " + rel)

for rel, threshold in (("enchanted_book.json", 1110038),
                       ("enchanted_book.json", 1110039),
                       ("iron_nugget.json", 1110001)):
    path = os.path.join(RP, "assets/minecraft/items", rel)
    try:
        with io.open(path, encoding="utf-8") as handle:
            blob = json.dumps(json.load(handle))
        if str(threshold) not in blob:
            problem("model dispatch lacks %s in %s" % (threshold, rel))
    except Exception as exc:
        problem("invalid item model %s: %s" % (rel, exc))


if problems:
    print("DIVINE COVENANT AUDIT FAIL")
    for entry in problems:
        print(" - " + entry)
    raise SystemExit(1)
print("DIVINE COVENANT AUDIT PASS")
