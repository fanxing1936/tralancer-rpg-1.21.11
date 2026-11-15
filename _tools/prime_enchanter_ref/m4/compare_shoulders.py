"""Render the shoulder change and check shoulders against the head during raised fists."""

import argparse
from copy import deepcopy
import io
import json
from itertools import product
from pathlib import Path
import sys
from types import SimpleNamespace

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[1]
sys.path[:0] = [str(HERE.parent / 'm3'), str(TOOLS / 'lucifer_ref')]
from author import read, sha, write
import display_mob as dm
from render_static import append_box, font, render
from scale_motion import posed_matrix, read_clips


VIEWS = (
    ('近正面 · 垂臂', (-.26,.09,-1)),
    ('四分之三', (-.73, .23, -1)),
    ('侧面', (-1, 0, 0)),
    ('背面', (0, 0, 1)),
)
POSES = (
    ('召唤 · 双拳举起', 'summon', .58),
    ('过载 · 单拳蓄力', 'overcharge', 1.92),
    ('前冲重拳 · 放大峰值', 'forward_strike', 1.5),
    ('雷霆砸地 · 放大峰值', 'lightning_slam', 2.67),
)


def load(path):
    bones, png, _ = dm.load_bbmodel(SimpleNamespace(bbmodel=path))
    texture = np.array(Image.open(io.BytesIO(png)).convert('RGBA'))
    return bones, read_clips(read(path)), texture


def neutral(model):
    bones, clips, texture = model
    bones = deepcopy(bones)
    for name in ('body','head','right_arm','left_arm','right_hand','left_hand','right_leg','left_leg'):
        bones[name]['rotation'] = [0, 0, 0]
    return bones, {**clips, 'neutral': {'tracks': {}, 'loop': False}}, texture


def matrices(bones, clip, time):
    cache = {}
    return {name: np.asarray(posed_matrix(bones, name, clip, time, cache)) for name in bones}


def scene(model, clip_name, time):
    bones, clips, texture = model
    pose = matrices(bones, clips[clip_name], time)
    faces = []
    for name, bone in bones.items():
        for cube in bone['cubes']:
            append_box(faces, cube['from'], cube['to'], cube['faces'], pose[name], texture,
                       name == 'head_glow', cube['name'])
    return faces


def panel(before, after, rows, path, title):
    width, height = 450, 375
    sheet = Image.new('RGB', (width*2, 100+height*len(rows)), '#202733')
    draw = ImageDraw.Draw(sheet)
    draw.text((22, 12), title, fill='white', font=font(26))
    for column, label in enumerate(('调整前', '调整后')):
        draw.text((width*column+22, 60), label, fill='#b7e7ee', font=font(23))
    for i, (name, direction, clip, time, center, magnification) in enumerate(rows):
        y = 100+i*height
        for column, model in enumerate((before, after)):
            shot = render(scene(model, clip, time), direction, '', magnification,
                          np.array(center), (width, height+100))
            sheet.paste(shot.crop((0,50,width,height+50)), (width*column,y))
        draw.text((20, y+12), name, fill='white', font=font(20))
        draw.line((0,y,width*2,y), fill='#586777')
    sheet.save(path, quality=94, subsampling=0)


def vertices(cube, transform):
    corners = np.array(list(product(*zip(cube['from'], cube['to']))))
    return corners @ transform[:3,:3].T + transform[:3,3]


def separating_gap(a, b):
    # Test parallelepipeds, including shoulders deformed by the native scale tracks.
    edges_a = a[[4,2,1]]-a[0]
    edges_b = b[[4,2,1]]-b[0]
    axes = np.vstack((np.cross(edges_a, np.roll(edges_a,1,axis=0)),
                      np.cross(edges_b, np.roll(edges_b,1,axis=0)),
                      np.cross(edges_a[:,None,:], edges_b[None,:,:]).reshape(-1,3)))
    norms = np.linalg.norm(axes, axis=1)
    axes = (axes[norms>1e-9]/norms[norms>1e-9,None]).T
    pa, pb = a @ axes, b @ axes
    return float(np.max(np.maximum(pa.min(0)-pb.max(0), pb.min(0)-pa.max(0))))


def contact(model, clip, time):
    bones, clips, _ = model
    pose = matrices(bones, clips[clip], time)
    shoulder = [(cube['name'], vertices(cube, pose[bone]))
                for bone, data in bones.items() for cube in data['cubes'] if '_shoulder_' in cube['name']]
    head = [(cube['name'], vertices(cube, pose[bone]))
            for bone, data in bones.items() for cube in data['cubes']
            if cube['name'] in ('gray_head', 'long_nose', 'red_hat_shell',
                                'left_hat_flap', 'right_hat_flap', 'rear_hat_flap')]
    result = {}
    solid = {'gray_head', 'long_nose'}
    for side in ('left','right'):
        distances = [(separating_gap(a, b), u, v)
                     for u,a in shoulder for v,b in head if u.startswith(side)]
        result[side] = {
            group: dict(zip(('gap','shoulder','head'), min(row for row in distances if (row[2] in solid)==is_solid)))
            for group,is_solid in (('solid_face',True),('hat',False))
        }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('before', type=Path)
    parser.add_argument('after', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--title', default='首席附魔师 · 青蓝肩罩前后对照')
    args = parser.parse_args()
    before, after = load(args.before), load(args.after)
    args.output.mkdir(parents=True, exist_ok=True)
    neutral_before, neutral_after = neutral(before), neutral(after)
    standing = [(name,d,'neutral',0,(0,25,0),12.7) for name,d in VIEWS]
    panel(neutral_before, neutral_after, standing, args.output/'shoulders-before-after.jpg', args.title)
    panel(neutral_before, neutral_after, standing[:1], args.output/'shoulders-closeup.jpg', args.title)
    panel(before, after, [(f'{label} · {time:.2f} 秒',(-.77,.25,-1),clip,time,
                           (0,20 if clip != 'lightning_slam' else 15,0),8)
                          for label,clip,time in POSES], args.output/'shoulders-raised-fists.jpg', args.title)
    rows = []
    for label,clip,time in POSES:
        rows.append(dict(clip=clip, time=time, before=contact(before,clip,time), after=contact(after,clip,time)))
    sweeps = {}
    for clip in ('summon','overcharge'):
        length = after[1][clip]['length']
        times = sorted(set(np.round(np.arange(0,length,.025),6)) | {length})
        sweeps[clip] = {variant: [(float(t),contact(model,clip,t)) for t in times]
                        for variant,model in (('before',before),('after',after))}
    write(args.output/'shoulder-clearance.json',
          dict(before_sha256=sha(args.before), after_sha256=sha(args.after), poses=rows, sweeps=sweeps,
               method='Model-space separating axes. Positive means a separating axis; negative is box overlap. Hat shell contains transparent pixels.'))
    print(json.dumps(rows, ensure_ascii=False))


if __name__ == '__main__':
    main()
