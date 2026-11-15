"""Build the static Prime Enchanter in Blockbench from the measured UVs."""

import base64
import hashlib
import json
from itertools import product
from pathlib import Path
from types import SimpleNamespace
import sys
from uuid import NAMESPACE_URL, uuid5

from PIL import Image

HERE = Path(__file__).resolve().parent
REF = HERE.parent
sys.path.insert(0, str(REF.parent))
from display_mob import bone_matrix, load_bbmodel, part_model
from pope_blockbench import BlockbenchMCP
from body import build_body

NAME = 'prime_enchanter_m2_static'
MODEL = REF / 'prime_enchanter.bbmodel'
TEXTURE = REF / 'originals/MCD2_Prime_Enchanter_(texture).png'
FACES = ('north', 'east', 'south', 'west', 'up', 'down')
PART_ROOTS = ('body', 'head', 'right_arm', 'left_arm', 'right_hand', 'left_hand',
              'right_leg', 'left_leg', 'cape_upper', 'cape_mid', 'cape_lower', 'hat_ribbons')


def uid(label):
    return str(uuid5(NAMESPACE_URL, 'tralancer:prime_enchanter:m2:' + label))


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


class Rig:
    def __init__(self):
        self.bones = {}
        self.cubes = []
        self.glow = set()
        self.bone('root', (0, 0, 0), None)

    def bone(self, name, pivot, parent='root', rotation=None):
        if name in self.bones or (parent is not None and parent not in self.bones):
            raise ValueError(f'Invalid or duplicate bone: {name}, parent {parent}')
        self.bones[name] = dict(name=name, uuid=uid('bone:' + name), origin=list(pivot),
                                parent=parent, rotation=list(rotation or (0, 0, 0)))

    def cube(self, bone, name, lo, hi, faces, origin=None, rotation=None):
        dimensions = [b - a for a, b in zip(lo, hi)]
        if bone not in self.bones or min(dimensions) < 0 or sum(d > 0 for d in dimensions) < 2:
            raise ValueError(f'Invalid cube bounds or bone: {name}')
        if any(rotation or ()):
            raise ValueError('display_mob reads rotation from bones only: ' + name)
        if set(faces) - set(FACES) or any(len(rect) != 4 or any(not 0 <= x <= 64 for x in rect)
                                         for rect in faces.values() if rect is not None):
            raise ValueError(f'Invalid faces: {name}')
        self.cubes.append({'name': name, 'uuid': uid('cube:' + name), 'bone': bone,
                           'from': list(lo), 'to': list(hi), 'origin': list(origin or (0, 0, 0)),
                           'rotation': [0, 0, 0], 'box_uv': False, 'autouv': 0,
                           'faces': {key: dict(uv=faces.get(key) or [0, 0, 0, 0],
                                               texture=0 if faces.get(key) is not None else None)
                                     for key in FACES}})

    def parts(self):
        parts = {p: [p] for p in PART_ROOTS}
        for name in dict.fromkeys(c['bone'] for c in self.cubes):
            if name in parts:
                continue
            parent = self.bones[name]['parent']
            if parent not in parts:
                raise ValueError('Rigid child needs a direct part root: ' + name)
            turns = [a for a in self.bones[name]['rotation'] if a]
            if len(turns) > 1 or any(abs(a) > 45 for a in turns):
                raise ValueError('Merged bone exceeds Java element rotation limits: ' + name)
            parts[parent].append(name)
        return list(parts.items())


def build_cloth(rig):
    # Fury Fist f132 and Launch f55: two leaves, two bending joints, both tips notched.
    # Both outside faces sample the second 7-pixel strip. The first strip supplies the inside.
    width = 5.35
    top, back = 23.65, 3.04
    sections = [('cape_upper', 5, -16), ('cape_mid', 6, -3), ('cape_lower', 7, 3)]
    parent, row = 'body', 2
    cloth_scale = 24 / 18
    for bone, length, angle in sections:
        rig.bone(bone, (0, top, back), parent, (angle, 0, 0))
        for label, left in [('right', 0.10), ('left', -width - 0.10)]:
            def panel(suffix, u0, v0, u1, v1):
                x0, x1 = left + width * u0 / 7, left + width * u1 / 7
                y0, y1 = top - (v1 - row) * cloth_scale, top - (v0 - row) * cloth_scale
                rig.cube(bone, f'{bone}_{label}{suffix}', (x0, y0, back - .028),
                         (x1, y1, back + .028),
                         {'north': [50 + u1, v0, 50 + u0, v1], 'south': [57 + u0, v0, 57 + u1, v1],
                          'west': [57 + u0, v0, 58 + u0, v1], 'east': [56 + u1, v0, 57 + u1, v1]})
            end = row + length
            if end == 20:
                panel('', 0, row, 7, 19)
                panel('_tip_left', 0, 19, 2, 20)
                panel('_tip_right', 5, 19, 7, 20)
            else:
                panel('', 0, row, 7, end)
        top -= length * cloth_scale
        row += length
        parent = bone

    # At rest the three bands trail just behind the crown, as in Idle frame 0.
    rig.bone('hat_ribbons', (0, 35.95, 4.09), 'head', (-43, 0, 0))
    for name, x, width, length, u, v, span in [
            ('right', 2.6, .7, 3.7, 43, 8, 12), ('middle', 0, 1.4, 5.6, 45, 0, 20),
            ('left', -2.6, .7, 3.7, 48, 8, 12)]:
        uw = 2 if name == 'middle' else 1
        y, z = 35.95, 4.09
        rig.cube('hat_ribbons', f'crown_band_{name}', (x - width / 2, y - length, z - .024),
                 (x + width / 2, y, z + .024),
                 {'north': [u + uw, v, u, v + span], 'south': [u, v, u + uw, v + span],
                  'west': [u, v, u + 1, v + span], 'east': [u + uw - 1, v, u + uw, v + span]})


def project_selector(pid):
    return ('const p=ModelProject.all.find(q=>q.uuid===' + json.dumps(pid) + ');'
            'if(!p||p.name!==' + json.dumps(NAME) + ')throw Error("M2 project identity mismatch");p.select();')


def posed_bounds(bones):
    points = []
    for name, bone in bones.items():
        matrix = bone_matrix(bones, name)
        for cube in bone['cubes']:
            for x, y, z in product(*zip(cube['from'], cube['to'])):
                points.append([sum(a*b for a,b in zip(row, (x,y,z,1))) for row in matrix[:3]])
    return [[min(p[i] for p in points) for i in range(3)],
            [max(p[i] for p in points) for i in range(3)]]


def main():
    if MODEL.exists() and json.loads(MODEL.read_text(encoding='utf-8')).get('animations'):
        raise ValueError('M2 must not replace the animated model')
    rig = Rig()
    build_body(rig)
    build_cloth(rig)
    parts = rig.parts()
    data = TEXTURE.read_bytes()
    with Image.open(TEXTURE) as im:
        if im.size != (64, 64) or im.mode != 'RGBA':
            raise ValueError('Expected original 64×64 RGBA texture')
    client = BlockbenchMCP()
    search = f'ModelProject.all.filter(p=>p.name==={json.dumps(NAME)}).map(p=>p.uuid)'
    try:
        found = client.evaluate(search)
    except RuntimeError as exc:
        if 'finishEdit' not in str(exc):
            raise
        found = []  # A fresh editor needs an initial project before MCP eval can run.
    if not found:
        client.tool('create_project', {'name': NAME, 'format': 'bedrock'})
        found = client.evaluate(search)
    if len(found) != 1:
        raise ValueError('Expected one isolated M2 authoring project')
    pid = found[0]
    prefix = project_selector(pid)
    author = '''
    if(Animation.all.length)throw Error('M2 authoring project already animated');
    for(const child of [...Outliner.root])child.remove();
    for(const tex of [...Texture.all])tex.remove();
    Project.texture_width=64;Project.texture_height=64;Project.box_uv=false;
    const t=new Texture({name:'prime_enchanter_atlas.png',uuid:input.textureId,uv_width:64,uv_height:64}).fromDataURL(input.png);
    t.add(false);t.width=64;t.height=64;
    const bones={};
    for(const g of input.bones){const {parent,...settings}=g;const b=new Group(settings,g.uuid);if(parent)b.addTo(bones[parent]);b.init();bones[g.name]=b;}
    for(const e of input.cubes){const {bone,...settings}=e;
      for(const f of Object.values(settings.faces))if(f.texture!==null)f.texture=t.uuid;
      new Cube(settings,e.uuid).addTo(bones[bone]).init();}
    Canvas.updateAll();
    return {uuid:p.uuid,cubes:Cube.all.length,bones:Group.all.length,animations:Animation.all.length};
    '''
    payload = dict(bones=list(rig.bones.values()), cubes=rig.cubes, textureId=uid('texture'),
                   png='data:image/png;base64,' + base64.b64encode(data).decode('ascii'))
    literal = json.dumps(payload).replace('/', r'\u002f')
    info = client.evaluate('(()=>{' + prefix + 'const input=' + literal + ';' + author + '})()')
    doc = client.evaluate('(()=>{' + prefix + 'return Codecs.project.compile({raw:true});})()')
    if isinstance(doc, str):
        doc = json.loads(doc)
    write_json(MODEL, doc)
    glow = sorted(rig.glow | {n for n in rig.bones if n.endswith('_glow')})
    mob = SimpleNamespace(bbmodel=MODEL, key='prime_enchanter', glow=set(glow), tex='rpg:item/prime_enchanter/atlas')
    bones, png, resolution = load_bbmodel(mob)
    assert png == data and resolution == {'width': 64, 'height': 64}
    assert len(doc['elements']) == len(rig.cubes) and not doc.get('animations')
    for part, members in parts:
        part_model(mob, bones, part, members, resolution)
    bounds = posed_bounds(bones)
    path = json.dumps(str(MODEL))
    client.evaluate('(()=>{' + prefix + 'p.save_path=' + path + ';p.saved=true;return true;})()')
    write_json(HERE / 'model_spec.json', dict(
        stage='M2', key='prime_enchanter', tag='rpg.prime_enchanter', score='rpg_pe',
        parts=parts, glow=glow, model_sha256=hashlib.sha256(MODEL.read_bytes()).hexdigest(),
        texture_sha256=hashlib.sha256(data).hexdigest(), rest_bounds=bounds,
        visible_faces=sum(face['texture'] is not None for c in rig.cubes for face in c['faces'].values()),
        groups=list(rig.bones.values()), elements=rig.cubes, blockbench=info))
    print(json.dumps({'model': str(MODEL), 'parts': len(parts), 'bounds': bounds, **info}))


if __name__ == '__main__':
    main()
