"""Check motion in a fresh Blockbench project and sample the Java bake in memory."""

import hashlib
import math
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace

from author import (APPROVED_SHA, BASE, HERE, MODEL, ORDER, REF, BlockbenchMCP, js,
                    authored_motion, make_animations, numeric_tracks, read, select, sha, static_data, write)
import display_mob as dm
from scale_motion import peak_times, posed_matrix, read_clips, runtime_document


SOCKETS = {
    'right_ice_fist': ('right_hand', (6, 10.42, 0), (0, -1, 0)),
    'left_electric_fist': ('left_hand', (-6, 10.42, 0), (0, -1, 0)),
    'head_core': ('head_glow', (0, 33, -4.04), (0, 0, -1)),
    'head_top': ('head', (0, 36.16, 0), (0, 1, 0)),
}


def rounded(point):
    return [round(v, 6) or 0 for v in point]


def transform(matrix, value, w):
    return [sum(row[k] * val for k, val in enumerate((*value, w))) for row in matrix[:3]]


def sockets(bones, clip, time):
    result = []
    cache = {}
    for name, (bone, point, direction) in SOCKETS.items():
        if bone.endswith('_hand'):
            side = bone.removesuffix('_hand')
            fist = next(c for c in bones[bone]['cubes'] if c['name'] == side + '_gray_fist')
            x, _, z = bones[bone]['pivot']
            point = (x, fist['from'][1], z)
        m = posed_matrix(bones, bone, clip, time, cache)
        axis = transform(m, direction, 0)
        length = math.hypot(*axis)
        result.append(dict(name=name, bone=bone, local_unposed_point=point,
                           posed_model_point=rounded(transform(m, point, 1)),
                           posed_model_direction=rounded([v/length for v in axis])))
    root = posed_matrix(bones, 'root', clip, time, cache)
    result.append(dict(name='ground_impact', bone='root', local_unposed_point=[0, 0, 0],
                       posed_model_point=rounded([root[0][3], 0, root[2][3]]),
                       posed_model_direction=[0, 1, 0],
                       note='取模型根投影到 y=0 的候选中心；实际地形与判定由玩法决定。'))
    return result


def reopen(client, doc):
    name = 'prime_enchanter_m3_verify'
    client.tool('create_project', {'name': name, 'format': 'bedrock'})
    # Read from the canonical path using the app's file reader, not in-memory animation data.
    script = '''
    (()=>{
      const p=Project;
      let files=[];
      Blockbench.read([path],{readtype:'text'},loaded=>{files=loaded;});
      if(!files.length)throw Error('Model file not readable');
      Codecs.project.parse(JSON.parse(files[0].content));
      Project.name=name;
      return {doc:Codecs.project.compile({raw:true}),uuid:p.uuid,version:Blockbench.version};
    })()
    '''
    outcome = client.evaluate('(()=>{const path='+js(str(MODEL))+';const name='+js(name)+';return '+script.strip()+';})()')
    assert static_data(doc) == static_data(outcome['doc'])
    assert numeric_tracks(doc) == numeric_tracks(outcome['doc'])
    return {'version': outcome['version'], 'uuid': outcome['uuid'], 'disk_read': True}


def quat_matrix(value):
    x, y, z, w = value
    return [[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w), 0],
            [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w), 0],
            [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y), 0],
            [0,0,0,1]]


def component_matrix(components):
    translation, left, scale, right = components
    diagonal = dm.ident()
    for axis, value in enumerate(scale):
        diagonal[axis][axis] = value
    return dm.mat_mul(dm.translate(*translation),
                      dm.mat_mul(quat_matrix(left), dm.mat_mul(diagonal, quat_matrix(right))))


def slerp(a, b, fraction):
    dot = sum(x*y for x,y in zip(a,b,strict=True))
    if dot < 0:
        dot, b = -dot, [-x for x in b]
    if dot > .9999:
        values = [x+(y-x)*fraction for x,y in zip(a,b,strict=True)]
        length = math.hypot(*values)
        return [v/length for v in values]
    angle = math.acos(min(1, dot))
    weights = (math.sin((1-fraction)*angle)/math.sin(angle), math.sin(fraction*angle)/math.sin(angle))
    return [weights[0]*x+weights[1]*y for x,y in zip(a,b,strict=True)]


def interpolate_display(first, last, fraction):
    return [slerp(a,b,fraction) if i in (1,3) else [x+(y-x)*fraction for x,y in zip(a,b,strict=True)]
            for i,(a,b) in enumerate(zip(first,last,strict=True))]


def wrist_gap(mob, bones, offsets, frames, clip, side):
    arm, hand = f'{side}_arm', f'{side}_hand'
    keys = clip['tracks'].get((arm,'scale'))
    if keys is None:
        return None
    changed = [i for i,(_,value,_) in enumerate(keys) if value != [1,1,1]]
    low, high = keys[changed[0]-1][0], keys[changed[-1]+1][0]
    points = {}
    for part in (arm, hand):
        k = offsets[part]
        model_to_item = dm.mat_mul(dm.scale(1/16), dm.mat_mul(dm.R180, dm.translate(*[-v-8 for v in k])))
        points[part] = transform(model_to_item, bones[hand]['pivot'], 1)
    maximum = 0.
    for (tick, before), (_, after) in zip(frames, frames[1:]):
        for fraction in (0., .25, .5, .75, 1.):
            if not low <= (tick+fraction)*dm.TICK <= high:
                continue
            a,b = [transform(component_matrix(interpolate_display(before[p],after[p],fraction)), points[p], 1)
                   for p in (arm,hand)]
            maximum = max(maximum, math.dist(a,b)*16/mob.model_scale)
    return maximum


def main():
    poses, scales, positions = authored_motion()

    doc = read(MODEL)
    assert sha(BASE) == APPROVED_SHA
    assert static_data(doc) == static_data(read(BASE))
    meta = read(HERE/'clipmeta.json')
    assert meta['pose_revision'] == 'astra_ultra_scale'
    assert meta['model_sha256'] == sha(MODEL)
    expected, regenerated_meta = make_animations(read(BASE), poses, scales, positions)
    assert numeric_tracks(doc) == numeric_tracks({'animations': expected})
    assert meta['clips'] == regenerated_meta
    evidence = read(HERE/'preview/render_evidence.json')
    assert evidence['model_sha256'] == sha(MODEL)
    assert tuple(evidence['clips']) == ORDER
    playback = read(HERE/'preview/playback_evidence.json')
    assert playback['model_sha256'] == sha(MODEL)
    assert tuple(playback['clips']) == ORDER
    spec = read(REF/'m2/model_spec.json')
    assert len(spec['parts']) == 12
    mob = SimpleNamespace(key='prime_enchanter', bbmodel=MODEL, anim_from=None, parts=spec['parts'],
                          glow=spec['glow'], tex='rpg:item/prime_enchanter/model', face_rotation=True,
                          clips=[(c['name'], 1, c['loop']) for c in meta['clips']], tick_rounding='round',
                          model_scale=1, seat=0, pose_cache=True, affine_parts=(), held=None)
    bones, texture, resolution = dm.load_bbmodel(mob)
    assert hashlib.sha256(texture).hexdigest() == spec['texture_sha256']
    clips = read_clips(doc)
    assert tuple(clips) == ORDER
    offsets = {part: dm.part_model(mob, bones, part, members, resolution)[1] for part, members in mob.parts}
    runtime, mob.affine_parts = runtime_document(doc, bones, mob.parts, clips)
    assert mob.affine_parts, 'Scale must reach the Java bake'
    with TemporaryDirectory(prefix='prime_enchanter_motion_') as temporary:
        mob.anim_from = Path(temporary)/'runtime.json'
        write(mob.anim_from, runtime)
        baked = dm.bake(mob, bones, offsets, dm.load_animations(mob))
    samples = [dict(clip='idle', event='rest', source_frame=0, time=0, suggested_tick=0,
                    sockets=sockets(bones, clips['idle'], 0))]
    result = []
    roots = {part: members[0] for part, members in mob.parts}
    allowed = {'root', *roots.values()}
    for c in meta['clips']:
        name = c['name']
        clip = clips[name]
        assert clip['length'] == c['ticks'] / 20 and clip['loop'] == c['loop'] == (name in ('idle', 'walk'))
        assert sha(REF/'originals'/c['gif']) == c['source_sha256']
        for (bone, channel), keys in clip['tracks'].items():
            assert bone in allowed
            assert keys[0][0] == 0 and keys[-1][0] == clip['length']
            assert len(keys) == len(set(t for t, _, _ in keys))
            assert all(math.isfinite(v) and interpolation == 'linear'
                       for _, value, interpolation in keys for v in value)
        if clip['loop']:
            for bone in bones:
                a = posed_matrix(bones, bone, clip, 0)
                b = posed_matrix(bones, bone, clip, clip['length'])
                assert max(abs(x-y) for u, v in zip(a, b) for x, y in zip(u, v)) < 1e-8
        frames = baked[name]['frames']
        assert baked[name]['ticks'] == c['ticks'] and len(frames) == c['ticks'] + (not c['loop'])
        matrix_error = 0.
        scaled_bake_frames = 0
        peaks = peak_times(clip)
        for tick, frame in frames:
            assert len(frame) == 12
            assert all(math.isfinite(v) for components in frame.values() for vector in components for v in vector)
            cache = {}
            has_scale = False
            for part in mob.affine_parts:
                components = frame[part]
                world = posed_matrix(bones, roots[part], clip, peaks.get(tick, tick*dm.TICK), cache)
                target = dm.display_matrix(mob, bones, roots[part], offsets[part], world)
                # Display NBT rounds each vector to five decimal places.
                actual = component_matrix([[round(value, 5) for value in vector] for vector in components])
                matrix_error = max(matrix_error, max(abs(x-y) for a,b in zip(target, actual) for x,y in zip(a,b)))
                has_scale |= any(abs(v-mob.model_scale)>1e-6 for v in components[2])
            scaled_bake_frames += has_scale
        assert matrix_error < 1e-4
        assert bool(scaled_bake_frames) == bool(c['scale_bones']), (name, scaled_bake_frames)
        gaps = {side: gap for side in ('right','left') if (gap := wrist_gap(mob,bones,offsets,frames,clip,side)) is not None}
        assert all(gap < .35 for gap in gaps.values()), (name, gaps)
        for cue in c['cues']:
            time = cue['start_ms']/1000
            samples.append(dict(clip=name, event=cue['event'], source_frame=cue['frame'], time=time,
                                suggested_tick=cue['suggested_tick'], basis=cue['basis'],
                                sockets=sockets(bones, clip, time)))
        rendered = evidence['clips'][name]
        assert rendered['samples'] == len(c['keyposes']) and rendered['matrix_error'] <= .0002
        assert rendered['source_blank_samples'] == rendered['model_blank_samples']
        movie = playback['clips'][name]
        assert movie['duration_ms'] == c['source_duration_ms']
        assert movie['sha256'] == sha(HERE/'preview'/name/'playback.webp')
        assert movie['source_blank_frames'] == movie['model_blank_frames'], (name, movie)
        for file, checksum in rendered['panels'].items():
            assert sha(HERE/'preview'/name/file) == checksum
        result.append(dict(clip=name, ticks=c['ticks'], baked_frames=len(frames), comparison_pairs=rendered['samples'],
                           playback_frames=movie['source_frames'], matched_blank_frames=movie['source_blank_frames'],
                           scale_bones=c['scale_bones'], scaled_bake_frames=scaled_bake_frames,
                           preserved_peak_source_times=peaks,
                           max_java_affine_matrix_error=matrix_error,
                           max_wrist_gap_model_units_during_scale=gaps,
                           max_blockbench_matrix_error=rendered['matrix_error']))
    client = BlockbenchMCP()
    reopened = reopen(client, doc)
    client.evaluate('(()=>{' + select(meta['project']['uuid']) + 'if(p){p.select();p.saved=true;}return true;})()')
    write(REF/'sockets.json', dict(bbmodel_sha256=sha(MODEL), coordinate_system='+Y up, facing -Z',
                                 units='unscaled model units; origin at model ground reference, 16 units per block at scale 1',
                                 model_scale=None, carrier_seat=None,
                                 carrier_yaw_zero='For default 180° base turn, from carrier feet: [-x,y,-z] * model_scale / 16.',
                                 note='原作没有提供发射骨或触发判定。拳、额纹和帽顶取自 M2 模型表面；样本按 GIF 帧起点求姿态。',
                                 samples=samples))
    write(HERE/'validation.json', dict(model_sha256=sha(MODEL), m2_static_payload_equal=True,
                                      original_texture_sha256=spec['texture_sha256'], part_count=12,
                                      authored_source_keyposes=sum(len(c['authored_source_frames']) for c in meta['clips']),
                                      animation_track_keys=sum(c['track_keys'] for c in meta['clips']),
                                      affine_parts=sorted(mob.affine_parts),
                                      native_reopen=reopened, clips=result, socket_samples=len(samples),
                                      java_bake_in_memory=True, real_game=False))
    print(f'Validated {len(result)} clips, {sum(r["comparison_pairs"] for r in result)} paired samples, '
          f'{sum(r["baked_frames"] for r in result)} Java bake frames, {len(samples)} socket sample times.')


if __name__ == '__main__':
    main()
