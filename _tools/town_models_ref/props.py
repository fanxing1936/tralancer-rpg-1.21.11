"""地下城静态城镇道具。generate(rp, dp) 供城镇生成器调用。"""
import json
from pathlib import Path
import display_mob as dm

HERE = Path(__file__).resolve().parent
NAMES = ('pyre', 'cage', 'grave_a', 'grave_b', 'candles_a', 'candles_b', 'cauldron', 'bell', 'barrel', 'crate', 'crate_pile', 'cart')


def generate(rp, dp):
    report = {}
    for name in NAMES:
        ref = HERE.parent / (name + '_dungeons_ref')
        rows = json.loads((ref / 'parts.json').read_text(encoding='utf-8'))
        mob = dm.Mob(key='town_prop_' + name, label=name, generator='add_town_models.py',
                     bbmodel=str(ref / (name + '.bbmodel')), parts=[(r['name'], r['bones']) for r in rows],
                     glow=json.loads((ref / 'glow_bones.json').read_text()), seat=0,
                     tag='rpg.tw.prop.' + name, score='rpg_tp', clips=[])
        mob.turn = 0
        mob.model_scale = 0.16 / 0.0192
        bones, png, resolution = dm.load_bbmodel(mob)
        texture = Path(rp) / 'assets/rpg/textures/item' / mob.key / 'atlas.png'
        texture.parent.mkdir(parents=True, exist_ok=True)
        texture.write_bytes(png)
        lines = []
        for part, members in mob.parts:
            model, offset = dm.part_model(mob, bones, part, members, resolution)
            dm.wj(str(Path(rp) / 'assets/rpg/models' / mob.key / (part + '.json')), model)
            dm.wj(str(Path(rp) / 'assets/rpg/items' / mob.key / (part + '.json')), {
                'model': {'type': 'minecraft:model', 'model': 'rpg:' + mob.key + '/' + part}})
            transform = dm.snbt_components(mob, dm.affine_components(dm.display_matrix(mob, bones, members[0], offset), None))
            nbt = ('{Tags:["rpg.tw.prop","rpg.tw.prop.%s"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:%s/%s"}},transformation:%s}' % (name, mob.key, part, transform))
            lines.append('execute summon minecraft:item_display run function rpg:town_models/prop/setup/' + name + '/' + part)
            dm.wf(str(Path(dp) / 'data/rpg/function/town_models/prop/setup' / name / (part + '.mcfunction')), [
                'data merge entity @s ' + nbt,
                'rotate @s ~ ~',
            ])
        dm.wf(str(Path(dp) / 'data/rpg/function/town_models/prop' / (name + '.mcfunction')), lines)
        report[name] = {'entities': len(mob.parts)}
    return report

