"""Task-local raw-mask tint support; shared display_mob.py is untouched.

The embedded PNG remains the authoring source. White mask RGB is multiplied
by a source-sampled constant at render time; its alpha is never changed.
Only explicitly named element/face pairs receive an extra item tint slot.
"""
from __future__ import annotations

import json
from pathlib import Path

import display_mob as dm


def mask_records(document):
    records = document.get('unhandled_root_fields', {}).get('emissive_masks', [])
    elements = {e['uuid']: e for e in document['elements']}
    seen = set()
    for record in records:
        key = (record['element_uuid'], record['face'])
        if key in seen:
            raise ValueError(f'Duplicate emissive mask face: {key}')
        seen.add(key)
        face = elements[key[0]]['faces'][key[1]]
        if face.get('texture') != 0 or face['uv'] != record['atlas_rect']:
            raise ValueError(f'Mask metadata does not match actual face UV: {key}')
        rgb = record['tint_rgb']
        if len(rgb) != 3 or any(type(x) is not int or not 0 <= x <= 255 for x in rgb):
            raise ValueError(f'Invalid mask RGB: {rgb}')
    return records


def apply_item_tints(mob, bones):
    """After writing this mob's part models/items, apply declared raw masks."""
    document = json.loads(Path(mob.bbmodel).read_text('utf8'))
    records = mask_records(document)
    pending = {(r['element_uuid'], r['face']): r for r in records}
    written = []
    for part, members in mob.parts:
        if part == mob.held:
            continue
        ordered = [cube for bone in members for cube in bones[bone]['cubes']]
        selected = [(i, name, record) for i, cube in enumerate(ordered)
                    for (uuid, name), record in pending.items() if uuid == cube['uuid']]
        if not selected:
            continue
        model_path = Path(mob.rp)/'assets'/dm.NS/'models'/mob.key/(part+'.json')
        item_path = Path(mob.rp)/'assets'/dm.NS/'items'/mob.key/(part+'.json')
        model = json.loads(model_path.read_text('utf8'))
        item = json.loads(item_path.read_text('utf8'))
        tints = item['model'].setdefault('tints', [])
        if len(tints) != 1:
            raise ValueError('Run raw-mask tint processing exactly once after the ordinary model build')
        colors = {}
        for i, name, record in selected:
            element = model['elements'][i]
            if element.get('light_emission') != 15:
                raise ValueError('Raw mask must belong to an independent emissive bone')
            rgb = tuple(record['tint_rgb'])
            if rgb not in colors:
                colors[rgb] = len(tints)
                tints.append({'type': 'minecraft:constant', 'value': (rgb[0]<<16)+(rgb[1]<<8)+rgb[2]})
            element['faces'][name]['tintindex'] = colors[rgb]
            written.append({'part': part, 'element_uuid': record['element_uuid'],
                            'face': name, 'tint_rgb': list(rgb), 'tint_index': colors[rgb]})
        dm.wj(str(model_path), model)
        dm.wj(str(item_path), item)
    if len(written) != len(records):
        raise ValueError('Some raw mask faces were not exported into any part')
    return written
