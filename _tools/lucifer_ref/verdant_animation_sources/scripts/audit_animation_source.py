"""Independent read-only PSA/coordinate/retarget audit. Never writes a model.

reference_frame() also exposes the unadapted retarget reference for later payload
validation. Deliberately has no Blockbench imports and no model mutator.
"""
from pathlib import Path
import hashlib, json, struct, math
import numpy as np

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'necromancer_animation_source.json'
FROZEN_SHA256 = '930867a3022a9544915e48f83c192d18be970d29777e731b6b4bec9f478bfcd1'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def rotation(q):
    q = np.asarray(q, dtype=float)
    x, y, z, w = q / np.linalg.norm(q)
    v = np.array([x, y, z])
    cross = np.array([[0, -z, y], [z, 0, -x], [-y, x, 0]])
    return (w*w - v@v)*np.eye(3) + 2*np.outer(v, v) + 2*w*cross


def trs(p, r):
    m = np.eye(4)
    m[:3, :3], m[:3, 3] = r, p
    return m


def slerp(a, b, t):
    a, b = np.asarray(a, float), np.asarray(b, float)
    a, b = a/np.linalg.norm(a), b/np.linalg.norm(b)
    dot = float(a@b)
    if dot < 0:
        b, dot = -b, -dot
    if dot > .9995:
        q = a + (b-a)*t
        return q/np.linalg.norm(q)
    theta = math.acos(min(1., dot))
    return (math.sin((1-t)*theta)*a + math.sin(t*theta)*b) / math.sin(theta)


def source_pose(data, clip, seconds):
    """Clamped, unlooped original local samples and 35 world matrices."""
    a = next(x for x in data['animations'] if x['short_name'] == clip)
    f = min(max(seconds*a['anim_info']['anim_rate'], 0), a['anim_info']['num_raw_frames']-1)
    i, j, t = int(f), min(int(f)+1, a['anim_info']['num_raw_frames']-1), f-int(f)
    local, world = [], []
    for b, tr in zip(data['bones'], a['tracks_java']):
        p = (1-t)*np.array(tr['position_java_px'][i]) + t*np.array(tr['position_java_px'][j])
        q = slerp(tr['quaternion_java_xyzw_normalized_continuous'][i], tr['quaternion_java_xyzw_normalized_continuous'][j], t)
        m = trs(p, rotation(q))
        parent = b['parent_index']
        local.append(m)
        world.append(m if parent is None else world[parent]@m)
    return local, world


def retarget_pose(data, source_local, source_world):
    """World rotation delta; target rest local offsets + parent-basis local delta."""
    tw, tl = [], []
    target_parent_by_source = {m['source_index']: m['target_id'] for m in data['target_mapping']}
    for m in data['target_mapping']:
        si = m['source_index']
        b = data['bones'][si]
        sp = b['parent_index']
        tp = target_parent_by_source.get(sp)
        sr = np.array(b['psaReferenceWorldJava'])
        tr = np.array(m['target_restWorldJava'])
        rw = source_world[si][:3, :3] @ sr[:3, :3].T @ tr[:3, :3]
        parent_now = tw[tp] if tp is not None else np.eye(4)
        rs_parent = np.array(data['bones'][sp]['psaReferenceWorldJava'])[:3, :3] if sp is not None else np.eye(3)
        rt_parent = np.array(data['target_mapping'][tp]['target_restWorldJava'])[:3, :3] if tp is not None else np.eye(3)
        dp = source_local[si][:3, 3] - np.array(b['psaReferenceLocalJava']['translation'])
        pl = np.array(m['target_restLocalJava']['translation']) + rt_parent.T @ rs_parent @ dp
        ml = trs(pl, parent_now[:3, :3].T @ rw)
        tl.append(ml)
        tw.append(parent_now @ ml)
    return tl, tw


def reference_frame(data, clip, seconds):
    sl, sw = source_pose(data, clip, seconds)
    tl, tw = retarget_pose(data, sl, sw)
    return {'source_local': sl, 'source_world': sw, 'target_local': tl, 'target_world': tw}


def audit():
    assert sha(SOURCE) == FROZEN_SHA256, 'frozen source changed'
    data = json.loads(SOURCE.read_text(encoding='utf-8'))
    rows, markers = [], []
    C = np.array([[-1, 0, 0], [0, 0, 1], [0, 1, 0]], float)
    maxp = maxr = maxnorm = 0.
    for a in data['animations']:
        blob = Path(a['psa_path']).read_bytes()
        assert hashlib.sha256(blob).hexdigest() == a['psa_sha256']
        cursor, chunks = 0, {}
        while cursor < len(blob):
            label, version, size, count = struct.unpack_from('<20siii', blob, cursor)
            label = label.split(b'\0')[0].decode()
            chunks[label] = (cursor+32, size, count)
            cursor += 32 + size*count
        assert cursor == len(blob)
        offset, size, count = chunks['ANIMKEYS']
        raw = np.asarray(a['raw_keys_frame_major'], dtype='<f4')
        assert raw.tobytes() == blob[offset:offset+size*count], 'raw float bytes changed'
        assert raw.shape == (a['anim_info']['num_raw_frames'], 37, 8)
        info_offset = chunks['ANIMINFO'][0]
        assert struct.unpack_from('<f', blob, info_offset+152)[0] == a['anim_info']['anim_rate']
        for b, track in zip(data['bones'], a['tracks_java']):
            k = raw[:, b['psa_track_index'], :].astype(float)
            gotp = np.array(track['position_java_px'])
            errp = float(np.max(np.abs(gotp - .16*k[:, :3]@C.T)))
            maxp = max(maxp, errp)
            for source_q, converted_q in zip(k[:, 3:7], track['quaternion_java_xyzw_normalized_continuous']):
                r = rotation(source_q)
                expected = C @ (r if b['parent_index'] is None else r.T) @ C.T
                maxr = max(maxr, float(np.max(np.abs(rotation(converted_q)-expected))))
                maxnorm = max(maxnorm, abs(float(np.linalg.norm(converted_q))-1))
        for name in ['body', 'head', 'R_arm', 'L_arm', 'R_leg', 'L_leg']:
            b = next(x for x in data['bones'] if x['name'] == name)
            p = np.array(a['tracks_java'][b['index']]['position_java_px'])
            markers.append({'clip': a['short_name'], 'bone': name,
                            'local_position_range_px': np.ptp(p, axis=0).tolist(),
                            'max_abs_difference_from_psa_reference_px': float(np.max(np.abs(p-np.array(b['psaReferenceLocalJava']['translation']))))})
        rows.append({'clip': a['short_name'], 'frames': len(raw), 'tracks': 37, 'raw_float32_byte_match': True,
                     'key_count': count, 'sha256': a['psa_sha256']})
    # Validate exact rest preservation; this is an algebra check, not an animation acceptance claim.
    sl, sw = [], []
    for b in data['bones']:
        p = b['psaReferenceLocalJava']['translation']
        q = b['psaReferenceLocalJava']['quaternion']
        m = trs(p, rotation(q))
        sl.append(m)
        sw.append(m if b['parent_index'] is None else sw[b['parent_index']]@m)
    tl, tw = retarget_pose(data, sl, sw)
    zero_world = max(float(np.max(np.abs(m-np.array(row['target_restWorldJava'])))) for m,row in zip(tw,data['target_mapping']))
    zero_local = max(float(np.max(np.abs(m-trs(row['target_restLocalJava']['translation'], rotation(row['target_restLocalJava']['quaternion']))))) for m,row in zip(tl,data['target_mapping']))
    full_delta = []
    for a in data['animations']:
        per_bone = {}
        for f in range(a['anim_info']['num_raw_frames']):
            ref = reference_frame(data, a['short_name'], f/a['anim_info']['anim_rate'])
            for row, got in zip(data['target_mapping'], ref['target_world']):
                si = row['source_index']
                full = ref['source_world'][si] @ np.linalg.inv(np.array(data['bones'][si]['psaReferenceWorldJava'])) @ np.array(row['target_restWorldJava'])
                per_bone[row['target_name']] = max(per_bone.get(row['target_name'], 0), float(np.max(np.abs(got[:3,3]-full[:3,3]))))
        full_delta.append({'clip': a['short_name'], 'max_position_difference_full_SE3_vs_preserved_target_offsets_px_by_bone': per_bone})
    passed = maxp < 1e-12 and maxr < 1e-12 and maxnorm < 1e-12 and zero_world < 1e-10 and zero_local < 1e-10
    result = {'status': 'PASS' if passed else 'FAIL', 'scope': 'Raw PSA bytes, coordinate matrix algebra, zero-motion target rest preservation. Not native/visual/game animation validation.',
              'source': str(SOURCE), 'source_sha256': sha(SOURCE), 'clips': rows,
              'raw_total_keys': sum(r['key_count'] for r in rows),
              'java_position_matrix_max_error_px': maxp, 'java_rotation_matrix_max_error': maxr,
              'quaternion_unit_length_max_error': maxnorm,
              'zero_motion_target_world_matrix_max_error': zero_world,
              'zero_motion_target_local_matrix_max_error': zero_local,
              'marker_translation_observations': markers,
              'full_world_delta_comparison': full_delta,
              'recommendation': 'Preserve target local rest offsets plus source animated local-position delta transformed through parent bind bases. Do not infer that all J_* translations are static. Tiny source marker rotation errors can turn full SE3 retarget into an unwanted lever-arm translation.',
              'frozen_source_unchanged': sha(SOURCE) == FROZEN_SHA256}
    (ROOT/'necromancer_animation_source_audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ['clips','marker_translation_observations','full_world_delta_comparison']}, ensure_ascii=False, indent=2))
    assert passed


if __name__ == '__main__':
    audit()
