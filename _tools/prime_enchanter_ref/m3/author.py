"""Author the eleven GIF-based clips on the approved static rig in Blockbench."""

import argparse
import hashlib
import json
import sys
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

HERE = Path(__file__).resolve().parent
REF = HERE.parent
MODEL = REF / 'prime_enchanter.bbmodel'
BASE = HERE / 'accepted_m2.bbmodel'
NAME = 'prime_enchanter_m3_astra'
APPROVED_SHA = '9ba6a1c3c06e6bb3cf46b078ea81c3a4c5688e7201b5c82b12d58824c8e4d40d'
MOTION = REF / 'm1/motion'
ORDER = ('idle', 'walk', 'appear', 'death', 'forward_strike', 'fury_fist', 'launch',
         'lightning_slam', 'overcharge', 'hurt', 'summon')

sys.path.insert(0, str(REF.parent))
from pope_blockbench import BlockbenchMCP


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def js(data):
    return json.dumps(data, separators=(',', ':')).replace('/', r'\u002f')


def uid(label):
    return str(uuid5(NAMESPACE_URL, 'tralancer:prime_enchanter:m3:' + label))


def static_data(doc):
    return {key: doc[key] for key in ('resolution', 'outliner', 'groups', 'elements', 'textures')}


def numeric_tracks(doc):
    return [(
        a['name'], a['loop'], a['length'], {
            bone: sorted((k['channel'], k['time'], k['interpolation'],
                          tuple(float(k['data_points'][0][axis]) for axis in 'xyz'))
                         for k in track['keyframes'])
            for bone, track in a['animators'].items() if track['keyframes']
        },
    ) for a in doc['animations']]


def short_number(v):
    rounded = round(float(v), 5)
    return 0 if rounded == 0 else rounded


def continuous(angle, previous):
    return tuple(v + 360 * round((old - v) / 360) for v, old in zip(angle, previous))


def authored_motion():
    from astra_loop_cast_poses import POSES as loops
    from astra_strike_poses import POSES as strikes
    from astra_transition_poses import POSES as transitions
    from astra_strike_scale import POSITION as strike_positions, SCALE as strike_scale
    from astra_other_scale import POSITION as other_positions, SCALE as other_scale

    assert not (strike_scale.keys() & other_scale.keys())
    assert not (strike_positions.keys() & other_positions.keys())
    return loops | strikes | transitions, strike_scale | other_scale, strike_positions | other_positions


def make_animations(doc, poses, scales=None, positions=None):
    source_timing = read(MOTION / 'gif_timing.json')['clips']
    source_keys = read(MOTION / 'keyposes.json')['clips']
    groups = {g['name']: g for g in doc['groups']}
    spec = read(REF / 'm2/model_spec.json')
    allowed = {'root', *(part for part, _ in spec['parts'])}
    scales = scales or {}
    positions = positions or {}
    assert (scales.keys() | positions.keys()) <= set(ORDER)
    animations, meta = [], []
    for i, ((source, study), clip) in enumerate(zip(source_keys.items(), ORDER, strict=True)):
        assert study['name'] == clip
        times = {row['index']: row['start_ms'] for row in source_timing[source]['frames']}
        length = study['nominal_ticks'] / 20
        rows = sorted(poses[clip], key=lambda row: row[0])
        assert rows[0][0] == 0 and len({r[0] for r in rows}) == len(rows)
        assert {row['frame'] for row in study['keyposes']} <= {row[0] for row in rows}, clip
        keys = [(times[frame] / 1000, angles, position) for frame, angles, position in rows]
        for _, angles, position in keys:
            assert set(angles) <= allowed and len(position) == 3
        loop = clip in ('idle', 'walk')
        assert keys[-1][0] <= length
        if keys[-1][0] == length:
            if loop:
                keys[-1] = (length, *keys[0][1:])
        else:
            keys.append((length, *(keys[0][1:] if loop else keys[-1][1:])))
        animators = {}
        clip_scales = scales.get(clip, {})
        clip_positions = positions.get(clip, {})
        assert (clip_scales.keys() | clip_positions.keys()) <= allowed - {'root'}
        scale_frames = sorted({frame for track in clip_scales.values() for frame, _ in track})
        for bone in (n for n in groups if n in allowed):
            rest = tuple(groups[bone].get('rotation') or (0, 0, 0))
            rotations = []
            previous = rest
            for _, angles, _ in keys:
                previous = continuous(angles.get(bone, rest), previous)
                rotations.append(tuple(short_number(v-r) for v, r in zip(previous, rest)))
            key_times = [row[0] for row in keys]
            channels = {'rotation': list(zip(key_times, rotations, strict=True))}
            if bone == 'root':
                channels['position'] = [(row[0], tuple(short_number(v) for v in row[2])) for row in keys]
            for channel, extra, default in (('scale', clip_scales, (1,1,1)), ('position', clip_positions, (0,0,0))):
                if bone in extra:
                    track = [(times[f]/1000, tuple(short_number(v) for v in values)) for f, values in extra[bone]]
                    assert all(t0 < t1 for (t0,_), (t1,_) in zip(track, track[1:]))
                    assert track[0][1] == track[-1][1] == default and track[-1][0] <= length
                    if track[0][0] > 0:
                        track.insert(0, (0, default))
                    if track[-1][0] < length:
                        track.append((length, default))
                    channels[channel] = track
            keyframes = []
            for channel, track in channels.items():
                default = (1,1,1) if channel == 'scale' else (0,0,0)
                if all(v == default for _, v in track):
                    continue
                for j, (t, value) in enumerate(track):
                    keyframes.append(dict(uuid=uid(f'{clip}/{bone}/{channel}/{j}'), channel=channel,
                                          time=t, color=-1, interpolation='linear',
                                          data_points=[dict(zip('xyz', value))]))
            if keyframes:
                animators[groups[bone]['uuid']] = dict(name=bone, type='bone', keyframes=keyframes)
        animations.append(dict(uuid=uid(clip), name='animation.'+clip, loop='loop' if loop else 'once',
                               length=length, snapping=20, animators=animators))
        keyposes = {row['frame']: row for row in study['keyposes']}
        for frame in scale_frames:
            if frame not in keyposes:
                values = [f'{bone} {sx:g}×{sy:g}×{sz:g}' for bone, track in clip_scales.items()
                          for f, (sx, sy, sz) in track if f == frame and (sx,sy,sz) != (1,1,1)]
                label = '肢体缩放核对：' + '、'.join(values) if values else '缩放前后的原尺寸参照'
                keyposes[frame] = dict(frame=frame, start_ms=times[frame], pose=label)
        meta.append(dict(id=i, name=clip, source=source, gif=study['gif'], source_duration_ms=study['duration_ms'],
                         length=length, ticks=study['nominal_ticks'], loop=loop, source_sha256=source_timing[source]['sha256'],
                         keyposes=[keyposes[f] for f in sorted(keyposes)], cues=study['pose_cues'],
                         scale_bones=list(clip_scales),
                         scale_source_frames=[f for f in scale_frames if 0 < f < rows[-1][0]],
                         authored_source_frames=[r[0] for r in rows],
                         track_keys=sum(len(t['keyframes']) for t in animators.values())))
    return animations, meta


def select(project_id):
    return f'const p=ModelProject.all.find(q=>q.uuid==={js(project_id)}&&q.name==={js(NAME)});'


def native_export(base, animations, expected_current_sha):
    client = BlockbenchMCP()
    client.tool('create_project', {'name': NAME, 'format': 'bedrock'})
    parsed = client.evaluate(f'(()=>{{if(Project.name!=={js(NAME)})throw Error("Project identity");'
                             f'Codecs.project.parse({js(base)});Project.name={js(NAME)};'
                             'return {uuid:Project.uuid,version:Blockbench.version};})()')
    prefix = select(parsed['uuid']) + 'if(!p)throw Error("Project identity");p.select();'
    for animation in animations:
        client.evaluate('(()=>{' + prefix + 'new Animation(' + js(animation) + ').add();return Animation.all.length;})()')
    compiled = client.evaluate('(()=>{' + prefix + 'return Codecs.project.compile({raw:true});})()')
    assert static_data(base) == static_data(compiled), 'Static rig changed in native editor'
    assert numeric_tracks({'animations': animations}) == numeric_tracks(compiled), 'Native animation roundtrip changed keys'
    pending = MODEL.with_suffix('.bbmodel.pending')
    if sha(MODEL) != expected_current_sha:
        raise ValueError('Model changed during the Blockbench edit; kept the external change on disk')
    write(pending, compiled)
    pending.replace(MODEL)
    client.evaluate('(()=>{' + prefix + 'p.save_path=' + js(str(MODEL)) + ';p.saved=true;return true;})()')
    return parsed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected-current-sha', help='Exact checksum of the model being superseded')
    args = parser.parse_args()
    if not BASE.exists():
        if sha(MODEL) != APPROVED_SHA:
            raise ValueError('Current model is not the approved M2 file')
        BASE.write_bytes(MODEL.read_bytes())
    assert sha(BASE) == APPROVED_SHA
    expected_current_sha = args.expected_current_sha or APPROVED_SHA
    if sha(MODEL) != expected_current_sha:
        raise ValueError('Current model differs from the approved starting file or reviewed draft')
    base = read(BASE)
    poses, scales, positions = authored_motion()
    assert set(poses) == set(ORDER)
    animations, metadata = make_animations(base, poses, scales, positions)
    project = native_export(base, animations, expected_current_sha)
    report = dict(project=project, pose_revision='astra_ultra_scale', model_sha256=sha(MODEL),
                  accepted_m2_sha256=APPROVED_SHA, clips=metadata)
    write(HERE / 'clipmeta.json', report)
    print(json.dumps({k: v for k, v in report.items() if k != 'clips'}))


if __name__ == '__main__':
    main()
