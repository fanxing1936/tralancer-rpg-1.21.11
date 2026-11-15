# -*- coding: utf-8 -*-
"""首席附魔师的模型、显示部件与十一段动作。"""

import argparse
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from display_mob import Mob, build, hook_tag, load_bbmodel, passenger, wf, wj, write_rig_runtime


HERE = Path(__file__).resolve().parent
REF = HERE / 'prime_enchanter_ref'
MODEL = REF / 'prime_enchanter.bbmodel'
CLIPS = ('idle', 'walk', 'appear', 'death', 'forward_strike', 'fury_fist',
         'launch', 'lightning_slam', 'overcharge', 'hurt', 'summon')
DIMENSIONS = ('overworld', 'the_nether', 'the_end')
# Source GIF blank intervals, rounded to the nearest 20 TPS sample.
HIDDEN_TICKS = {'appear': (0, 5), 'launch': (23, 44)}
MAX_HEALTH = 1000
MODEL_SCALE = 1.15

# The M3 adapter reads the native rotation, translation and scale channels.
sys.path.insert(0, str(REF / 'm3'))
from scale_motion import read_clips, runtime_document


def configured_mob(spec, clips):
    if tuple(clips) != CLIPS or {name for name, clip in clips.items() if clip['loop']} != {'idle', 'walk'}:
        raise ValueError('Prime Enchanter animation order or loop flags differ from the runtime interface')
    return Mob(key='prime_enchanter', label='首席附魔师', generator=Path(__file__).name,
               bbmodel=MODEL, parts=spec['parts'], glow=spec['glow'], seat=2.0,
               model_scale=MODEL_SCALE, tag='rpg.prime_enchanter', score='rpg_pe',
               clips=[(name, 1, clip['loop']) for name, clip in clips.items()],
               face_rotation=True, hold_clips=('death',), pose_cache=True, bulk_pose=True)


def write_visibility(mob, root):
    """Blank the display item for source frames where the model leaves the GIF."""
    hidden = mob.tag + '.hidden'
    own_parts = f'execute on passengers if entity @s[type=minecraft:item_display,tag={mob.tag}.part]'
    wf(root / 'visibility/hide.mcfunction', [
        f'{own_parts} run tag @s add {hidden}',
        f'{own_parts} run data remove entity @s item',
    ])
    for part, _ in mob.parts:
        # Show uses the finished pose and snaps across the hidden flight interval.
        # Bulk poses read the part name from this item's custom_data.
        wf(root / f'visibility/show_{part}.mcfunction', [
            f'data merge entity @s {{start_interpolation:0,interpolation_duration:0,'
            f'item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"{mob.fn}/{part}",'
            f'"minecraft:custom_data":{{part:"{part}"}}}}}}}}',
            f'tag @s remove {hidden}',
        ])
    wf(root / 'visibility/show.mcfunction', [
        f'{own_parts} if entity @s[tag={hidden},tag={mob.tag}.p.{part}] run function {mob.fn}/visibility/show_{part}'
        for part, _ in mob.parts
    ])

    # An empty display cannot read its part key from the item. While it is hidden,
    # dispatch by tag, then restore the item after the destination pose is applied.
    for name, _step, _loop in mob.clips:
        interval = HIDDEN_TICKS.get(name)
        touched = {0} | (set(range(interval[0], interval[1]+1)) if interval else set())
        for tick in sorted(touched):
            frame = root / f'anim/{name}/f{tick}.mcfunction'
            lines = frame.read_text(encoding='utf-8').splitlines()
            lines = [line.replace(f'tag={mob.tag}.part]', f'tag={mob.tag}.part,tag=!{hidden}]') for line in lines]
            lines.extend([
                f'{own_parts} if entity @s[tag={hidden},tag={mob.tag}.p.{part}] '
                f'run function {mob.fn}/anim/apply {{part:"{part}"}}'
                for part, _ in mob.parts
            ])
            if interval and tick == interval[0]:
                lines.append(f'function {mob.fn}/visibility/hide')
            elif tick == 0 or (interval and tick == interval[1]):
                lines.append(f'function {mob.fn}/visibility/show')
            wf(frame, lines)


def write_datapack(mob, rest):
    root = Path(mob.func)
    passengers = []
    for part, components in rest:
        entity = passenger(mob, part, components)
        component = f'"minecraft:item_model":"{mob.fn}/{part}"'
        passengers.append(entity.replace(component, component+f',"minecraft:custom_data":{{part:"{part}"}}'))
    wf(root / 'summon.mcfunction', [
        '# 首席附魔师载体与模型部件。由 add_prime_enchanter_model.py 生成。',
        f'summon {mob.carrier} ~ ~ ~ {{Tags:["{mob.tag}"],Silent:1b,PersistenceRequired:1b,'
        f'CanPickUpLoot:0b,Health:{MAX_HEALTH}f,CustomName:{{text:"{mob.label}",color:"aqua"}},'
        f'active_effects:[{{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b}}],'
        f'attributes:[{{id:"minecraft:max_health",base:{MAX_HEALTH}d}}],Passengers:[{",".join(passengers)}]}}',
    ])
    write_rig_runtime(mob, [f'execute as @e[{mob.carrier_sel}] at @s run function {mob.fn}/follow'])
    follow = root/'follow.mcfunction'
    lines = follow.read_text(encoding='utf-8').splitlines()
    lines[1] = f'execute on passengers if entity @s[type=minecraft:item_display,tag={mob.tag}.part] run rotate @s ~ 0'
    wf(follow, lines)
    lines = (root/'tick.mcfunction').read_text(encoding='utf-8').replace('@e[', '@e[distance=0..,').splitlines()
    wf(root/'tick_dimension.mcfunction', lines)
    wf(root/'tick.mcfunction', [f'execute in minecraft:{d} run function {mob.fn}/tick_dimension' for d in DIMENSIONS])
    predicates = Path(mob.dp) / 'data/rpg/predicate' / mob.key
    wj(predicates/'riding.json', {'condition': 'minecraft:entity_properties', 'entity': 'this',
                                  'predicate': {'vehicle': {'type': mob.carrier, 'nbt': f'{{Tags:["{mob.tag}"]}}'}}})
    wj(predicates/'invisible.json', {'condition': 'minecraft:entity_properties', 'entity': 'this',
                   'predicate': {'effects': {'minecraft:invisibility': {}}}})
    wf(root/'tick_late.mcfunction', [
        f'execute in minecraft:{d} as @e[distance=0..,{mob.carrier_sel}] '
        f'unless predicate {mob.fn}/invisible run effect give @s minecraft:invisibility infinite 0 true'
        for d in DIMENSIONS
    ])
    hook_tag(mob.dp, 'tick', f'{mob.fn}/tick_late', False)
    write_visibility(mob, root)


def generate(resourcepack, datapack):
    doc = json.loads(MODEL.read_text(encoding='utf-8'))
    spec = json.loads((REF/'m2/model_spec.json').read_text(encoding='utf-8'))
    clips = read_clips(doc)
    mob = configured_mob(spec, clips)
    bones, _, _ = load_bbmodel(mob)
    # The first visible Launch frame is at 2.210s, after the 2.200s tick.
    runtime, mob.affine_parts = runtime_document(doc, bones, mob.parts, clips, {'launch': {44: 2.21}})
    with TemporaryDirectory(prefix='prime_enchanter_') as temp:
        mob.anim_from = Path(temp)/'animation.json'
        wj(mob.anim_from, runtime)
        baked, rest = build(mob, str(resourcepack), str(datapack))
    write_datapack(mob, rest)
    return baked


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('resourcepack', nargs='?', type=Path, default=HERE.parent/'resourcepack')
    parser.add_argument('datapack', nargs='?', type=Path, default=HERE.parent/'rpg')
    args = parser.parse_args()
    generate(args.resourcepack, args.datapack)
