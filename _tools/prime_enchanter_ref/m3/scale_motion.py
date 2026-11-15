"""Evaluate Prime Enchanter's Blockbench scale channels for the Java display pipeline."""

import argparse
import math
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

from author import MODEL, REF, read, write
import display_mob as dm


UNIT = (1, 1, 1)
ZERO = (0, 0, 0)


def read_clips(doc):
    names = {group['uuid']: group['name'] for group in doc['groups']}
    clips = {}
    for animation in doc['animations']:
        name = animation['name'].removeprefix('animation.')
        loop = animation['loop'] == 'loop'
        tracks = {}
        for uuid, animator in animation['animators'].items():
            for key in animator['keyframes']:
                channel = key['channel']
                if channel not in ('rotation', 'position', 'scale') or key['interpolation'] != 'linear':
                    raise ValueError(f'{name}: unexpected channel or interpolation on {names[uuid]}')
                point, = key['data_points']
                values = [float(point[axis]) for axis in 'xyz']
                if not all(math.isfinite(v) and (channel != 'scale' or v > 0) for v in values):
                    raise ValueError(f'{name}: invalid {channel} on {names[uuid]}')
                tracks.setdefault((names[uuid], channel), []).append((key['time'], values, 'linear'))
        for keys in tracks.values():
            keys.sort(key=lambda row: row[0])
        clips[name] = dict(length=animation['length'], loop=loop, tracks=tracks)
    return clips


def affected(bones, parts, clip):
    scaled = {bone for bone, channel in clip['tracks'] if channel == 'scale'}
    return {part: members[0] for part, members in parts if scaled.intersection(dm.chain(bones, members[0]))}


def peak_times(clip):
    """Map local scale extremes to the nearest Java tick, preferring the larger pose on ties."""
    peaks = {}
    for (_, channel), keys in clip['tracks'].items():
        if channel != 'scale':
            continue
        for (_, before, _), (source, value, _), (_, after, _) in zip(keys, keys[1:], keys[2:]):
            # Compare each axis separately so an early widening peak is kept before a later length peak.
            if not any(v > 1 and v >= a and v >= b and (v > a or v > b)
                       for a, v, b in zip(before, value, after, strict=True)):
                continue
            tick = round(source/dm.TICK)
            if tick not in peaks or math.prod(value) > math.prod(peaks[tick][1]):
                peaks[tick] = (source, value)
    return {tick: source for tick, (source, _) in peaks.items()}


def posed_matrix(bones, name, clip, time, cache=None):
    """Map absolute rest points through the posed Blockbench hierarchy."""
    if cache is None:
        cache = {}
    if name in cache:
        return cache[name]
    bone = bones[name]
    px, py, pz = bone['pivot']
    tracks = clip['tracks']

    def value(channel, default):
        keys = tracks.get((name, channel))
        return default if keys is None else dm.track_value(keys, time, clip['loop'])

    dx, dy, dz = value('position', ZERO)
    rotation = [rest + delta for rest, delta in zip(bone['rotation'], value('rotation', ZERO), strict=True)]
    stretch = dm.ident()
    for axis, v in enumerate(value('scale', UNIT)):
        stretch[axis][axis] = v
    local = dm.mat_mul(dm.translate(px+dx, py+dy, pz+dz),
                       dm.mat_mul(dm.euler(rotation), dm.mat_mul(stretch, dm.translate(-px, -py, -pz))))
    parent = bone['parent']
    cache[name] = dm.mat_mul(posed_matrix(bones, parent, clip, time, cache), local) if parent else local
    return cache[name]


def runtime_document(doc, bones, parts, clips, extra_sample_times=None):
    """Translate native scale keys into the shared pipeline's absolute affine track format."""
    runtime = {'groups': [{'uuid': g['uuid'], 'name': g['name']} for g in doc['groups']], 'animations': []}
    affine_parts = set()
    extra_sample_times = extra_sample_times or {}
    for original in doc['animations']:
        name = original['name'].removeprefix('animation.')
        clip = clips[name]
        animation = deepcopy(original)
        members = affected(bones, parts, clip)
        samples = peak_times(clip) | extra_sample_times.get(name, {})
        if members or samples:
            affine_parts.update(members)
            frames = range(round(clip['length']/dm.TICK)+1)
            # Resample the whole pose at the peak tick so the arm, shoulder and trunk share the same time.
            matrices = {roots[0]: [] for _, roots in parts}
            for tick in frames:
                time = tick*dm.TICK
                source_time = samples.get(tick, time)
                cache = {}
                for bone, keys in matrices.items():
                    keys.append([time, posed_matrix(bones, bone, clip, source_time, cache)])
            animation['dungeons_affine_tracks'] = matrices
        for animator in animation['animators'].values():
            animator['keyframes'] = [key for key in animator['keyframes'] if key['channel'] != 'scale']
        runtime['animations'].append(animation)
    return runtime, affine_parts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('--model', type=Path, default=MODEL)
    args = parser.parse_args()
    if args.output.resolve() == args.model.resolve():
        parser.error('output must differ from the editable model')
    doc = read(args.model)
    bones, _, _ = dm.load_bbmodel(SimpleNamespace(bbmodel=args.model))
    parts = read(REF/'m2/model_spec.json')['parts']
    runtime, affine_parts = runtime_document(doc, bones, parts, read_clips(doc))
    write(args.output, runtime)
    print('Use affine_parts:', ', '.join(sorted(affine_parts)))


if __name__ == '__main__':
    main()
