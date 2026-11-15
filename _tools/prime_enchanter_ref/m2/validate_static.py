"""Check the saved static model, sampled UVs, and its four on-disk previews."""

import csv
import hashlib
import io
import json
from types import SimpleNamespace

from PIL import Image

from make_static import HERE, MODEL, TEXTURE, load_bbmodel, part_model, posed_bounds, write_json


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    spec = json.loads((HERE / 'model_spec.json').read_text(encoding='utf-8'))
    doc = json.loads(MODEL.read_text(encoding='utf-8'))
    render = json.loads((HERE / 'preview/render_evidence.json').read_text(encoding='utf-8'))
    assert sha(MODEL) == spec['model_sha256'] == render['model_sha256']
    assert render['model_roundtrip'] and not doc.get('animations') and len(doc['textures']) == 1
    assert len(spec['parts']) == 12 and len(doc['groups']) == len(spec['groups'])
    mob = SimpleNamespace(bbmodel=MODEL, key=spec['key'], glow=set(spec['glow']),
                          tex='rpg:item/prime_enchanter/atlas')
    bones, png, resolution = load_bbmodel(mob)
    assert png == TEXTURE.read_bytes() and sha(TEXTURE) == spec['texture_sha256']
    assert posed_bounds(bones) == spec['rest_bounds']
    part_by_bone = {}
    for part, members in spec['parts']:
        built, _ = part_model(mob, bones, part, members, resolution)
        assert built['elements']
        for bone in members:
            assert bone not in part_by_bone
            part_by_bone[bone] = part
    atlas = Image.open(io.BytesIO(png)).convert('RGBA')
    rows = []
    for bone, row in bones.items():
        for cube in row['cubes']:
            assert not any(cube.get('rotation', ()))
            for side, face in cube['faces'].items():
                if face.get('texture') is None:
                    continue
                u, v, x, y = face['uv']
                assert face['texture'] == 0 and face.get('rotation', 0) == 0
                assert all(int(n) == n and 0 <= n <= 64 for n in (u, v, x, y))
                alpha = atlas.crop((min(u, x), min(v, y), max(u, x), max(v, y))).getchannel('A')
                assert alpha.getextrema()[1] == 255, (cube['name'], side)
                assert alpha.getextrema()[0] in (0, 255)
                rows.append((part_by_bone[bone], bone, cube['name'], side, u, v, x, y,
                             'mask' if alpha.getextrema()[0] == 0 else 'opaque'))
    assert len(rows) == spec['visible_faces']
    with (HERE / 'face_uv.csv').open('w', encoding='utf-8-sig', newline='') as fh:
        writer = csv.writer(fh)
        writer.writerow(('part', 'bone', 'cube', 'face', 'u0', 'v0', 'u1', 'v1', 'source_alpha'))
        writer.writerows(rows)
    for view, digest in render['image_sha256'].items():
        path = HERE / 'preview' / (view + '.png')
        assert sha(path) == digest
        with Image.open(path) as im:
            im.verify()
        with Image.open(path) as im:
            assert im.mode == 'RGBA' and im.getchannel('A').getbbox()
    assert sha(HERE / 'preview/neutral_detail.png') == render['detail_sha256']
    report = dict(all_passed=True, model_sha256=sha(MODEL), texture_sha256=sha(TEXTURE),
                  native_reopen=render['native']['version'], visible_faces=len(rows),
                  cubes=len(doc['elements']), parts=len(spec['parts']), bones=len(bones),
                  saved_animation_count=len(doc.get('animations', [])),
                  java_part_conversion_passed=True, view_count=len(render['image_sha256']),
                  in_game_verified=False)
    write_json(HERE / 'validation.json', report)
    print(json.dumps(report))


if __name__ == '__main__':
    main()
