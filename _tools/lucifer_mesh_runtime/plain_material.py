"""Plain material for the Lucifer phase-one mesh: no custom core shader.

The shader runtime (mesh_runtime.export_geometry + export_shaders) draws each source triangle as a
proxy rectangle whose face samples an 8x8 metadata block; a core shader reads the block and fetches
the real texel.  Without that shader (Iris / shader packs, or a pack built without it) every face
shows the green metadata pixel.  Here each proxy rectangle keeps the same geometry, but its face
gets a baked tile: the triangle's own texels, transparent outside the triangle, so vanilla item
rendering (alpha cut) shows the true surface under any renderer.

The left eye's emission (lucifer_eye_emission: two texels of the skeleton's head front) becomes a
small full-bright quad laid just in front of those texels.
"""
import math
import sys
import warnings
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.spatial.transform import Rotation

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from dungeons_conversion.generic import pack_tiles  # noqa: E402

EYE_LIFT = 0.02          # model units in front of the face
ALPHA_CUT = 128


def _bake_group(part, group, tex, K, scale=4):
    """One flat element over one or two coplanar triangles, its tile baked at `scale` tile pixels per
    source texel (nearest), transparent outside the triangles: crisp texels, no seam between the two."""
    P = lambda k: np.array(part['vertices'][k], float)
    f0 = group[0]
    p = np.array([P(k) for k in f0['vertices']])
    x = p[1] - p[0]; x /= np.linalg.norm(x)
    z = np.cross(p[1] - p[0], p[2] - p[0]); z /= np.linalg.norm(z)
    basis = np.array([x, np.cross(z, x), z]).T
    tris = []
    for f in group:
        pt = np.array([P(k) for k in f['vertices']])
        uv = _snap(np.array([f['uv'][k] for k in f['vertices']], float))
        tris.append((((pt - p[0]) @ basis)[:, :2], uv))
    allq = np.concatenate([t[0] for t in tris])
    lo, hi = allq.min(0), allq.max(0); span = hi - lo
    # texels per model unit along the plane axes, from the first triangle's affine map
    q0, uv0 = tris[0]
    m = np.linalg.lstsq(np.c_[q0, np.ones(3)], uv0, rcond=None)[0]
    dens = np.linalg.norm(m[:2], axis=1)
    w = int(min(64, max(2, math.ceil(span[0] * dens[0] * scale))))
    h = int(min(64, max(2, math.ceil(span[1] * dens[1] * scale))))
    xs = lo[0] + (np.arange(w) + .5) / w * span[0]
    ys = hi[1] - (np.arange(h) + .5) / h * span[1]
    xx, yy = np.meshgrid(xs, ys)
    th, tw = tex.shape[:2]
    out = np.zeros((h, w, 4), np.uint8)
    for q, uv in tris:
        bc = np.linalg.inv(np.vstack([q.T, np.ones(3)]))
        b = np.stack([xx, yy, np.ones_like(xx)], -1) @ bc.T
        inside = np.all(b >= -1e-3, axis=-1)
        src = b @ uv
        sx = np.clip(np.floor(src[..., 0] + 1e-4).astype(int), 0, tw - 1)
        sy = np.clip(np.floor(src[..., 1] + 1e-4).astype(int), 0, th - 1)
        out[inside] = tex[sy[inside], sx[inside]]
    out[..., 3] = np.where(out[..., 3] >= ALPHA_CUT, 255, 0)
    center = p[0] + basis[:, :2] @ ((lo + hi) / 2) - K
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        rot = Rotation.from_matrix(basis).as_euler('ZYX', degrees=True)[::-1]
    lower = center - np.r_[span / 2, 0]; upper = center + np.r_[span / 2, 0]
    if min(*lower, *upper) < -16 or max(*lower, *upper) > 32:
        raise ValueError('Java proxy bounds exceed -16..32')
    el = {'from': lower.tolist(), 'to': upper.tolist(),
          'rotation': {'origin': center.tolist(), **dict(zip('xyz', map(float, rot)))}, 'faces': {}, 'shade': False}
    return el, Image.fromarray(out)


def _snap(uv):
    """Source UVs carry tiny insets (1/1024 px) against bleeding; Java samples whole texels anyway."""
    r = np.round(uv)
    return np.where(abs(uv - r) < .01, r, uv)


def _quads(part):
    """Pair the triangles of a part back into the quads they were cut from: two triangles sharing an
    edge (by position: the source keeps separate vertices per triangle), in one plane, whose four
    corners carry an axis-aligned UV rectangle.  Returns ([(points 4x3, uvs 4x2, normal, face ids)],
    leftover faces)."""
    faces = part['faces']
    P = {k: np.array(v, float) for k, v in part['vertices'].items()}
    pos = lambda k: tuple(np.round(P[k], 4))
    edge_owner = {}
    for i, f in enumerate(faces):
        ks = [pos(k) for k in f['vertices']]
        for a_, b_ in ((ks[0], ks[1]), (ks[1], ks[2]), (ks[2], ks[0])):
            edge_owner.setdefault(frozenset((a_, b_)), []).append(i)
    used, quads, pairs = set(), [], []
    for edge, owners in edge_owner.items():
        if len(owners) != 2 or owners[0] in used or owners[1] in used:
            continue
        f1, f2 = faces[owners[0]], faces[owners[1]]
        corners = {}
        ok = True
        for f in (f1, f2):
            for k in f['vertices']:
                c = pos(k)
                uvv = _snap(np.array(f['uv'][k], float))
                if c in corners and np.max(abs(corners[c][1] - uvv)) > .01:
                    ok = False
                corners[c] = (P[k], uvv)
        if not ok or len(corners) != 4:
            continue
        n = []
        for f in (f1, f2):
            a_, b_, c_ = (P[k] for k in f['vertices'])
            v = np.cross(b_ - a_, c_ - a_); n.append(v / np.linalg.norm(v))
        if n[0] @ n[1] < 1 - 1e-5:
            continue
        pts = np.array([c[0] for c in corners.values()]); uvs = np.array([c[1] for c in corners.values()])
        if len(set(np.round(uvs[:, 0], 3))) != 2 or len(set(np.round(uvs[:, 1], 3))) != 2:
            pairs.append([f1, f2])          # a trapezoid / sheared face: baked as one tile
        else:
            quads.append((pts, uvs, n[0], [f1['source_face_id'], f2['source_face_id']]))
        used.update(owners)
    return quads, pairs + [[f] for i, f in enumerate(faces) if i not in used]


def _quad_element(pts, uvs, normal, K):
    """A flat element over the quad whose south face shows the source UV rectangle as is."""
    # x along the edge where v stays constant, y = normal x x
    i0 = 0
    j = next((j for j in range(1, 4) if abs(uvs[j, 1] - uvs[i0, 1]) < 1e-3), None)
    if j is None:
        return None
    x = pts[j] - pts[i0]; x /= np.linalg.norm(x)
    if abs(uvs[j, 0] - uvs[i0, 0]) < 1e-3:
        return None
    z = normal
    y = np.cross(z, x)
    basis = np.array([x, y, z]).T
    q = (pts - pts[0]) @ basis
    if np.max(abs(q[:, 2])) > 1e-4:
        return None
    lo, hi = q[:, :2].min(0), q[:, :2].max(0)
    def corner(cx, cy):
        k = int(np.argmin(np.hypot(q[:, 0] - cx, q[:, 1] - cy)))
        if np.hypot(q[k, 0] - cx, q[k, 1] - cy) > 1e-4:
            raise ValueError('not a rectangle')
        return uvs[k]
    try:
        tl, tr, bl = corner(lo[0], hi[1]), corner(hi[0], hi[1]), corner(lo[0], lo[1])
    except ValueError:
        return None
    if abs(tl[1] - tr[1]) > 1e-3 or abs(tl[0] - bl[0]) > 1e-3:
        return None
    center = pts[0] + basis[:, :2] @ ((lo + hi) / 2) - K
    span = hi - lo
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        rot = Rotation.from_matrix(basis).as_euler('ZYX', degrees=True)[::-1]
    lower = center - np.r_[span / 2, 0]
    upper = center + np.r_[span / 2, 0]
    if min(*lower, *upper) < -16 or max(*lower, *upper) > 32:
        raise ValueError('Java proxy bounds exceed -16..32')
    el = {'from': lower.tolist(), 'to': upper.tolist(),
          'rotation': {'origin': center.tolist(), **dict(zip('xyz', map(float, rot)))}, 'faces': {}, 'shade': False}
    return el, (tl[0], tl[1], tr[0], bl[1])


def export_geometry_plain(rig, rp, key):
    eye = rig.doc.get('lucifer_eye_emission', {})
    eye_faces = set(eye.get('source_face_ids', []))
    eye_texels = eye.get('texels', [])
    eye_rgb = tuple(eye.get('preview_color_srgb8', [168, 85, 247]))
    textures = [np.array(im.convert('RGBA')) for _, im in rig.images]
    tiles, pending, parts, records, direct = [], [], [], [], []
    eye_done = False
    for part in rig.source_geometry():
        if part['texture'] == 5:
            raise ValueError('plain material does not handle wing meshes')
        v = np.array(list(part['vertices'].values()))
        K = (v.min(0) + v.max(0)) / 2 - 8
        els = []
        tex = textures[part['texture']]
        double = part.get('render_sides', rig.doc['textures'][part['texture']].get('render_sides')) == 'double'
        quads, leftover = _quads(part)
        for pts, uvs, normal, ids in quads:
            made = _quad_element(pts, uvs, normal, K)
            if made is None:
                leftover.append([f for f in part['faces'] if f['source_face_id'] in ids])
                continue
            el, rect = made
            direct.append((el, part['texture'], rect, double))
            els.append(el)
            records.append({'part': part['name'], 'source_face_ids': ids, 'direct_uv': True})
        # the glowing eye: a small full-bright quad over its texels, just in front of the head's face
        for f in part['faces']:
            if f['source_face_id'] not in eye_faces or not eye_texels or eye_done:
                continue
            p = np.array([part['vertices'][k] for k in f['vertices']], float)
            uv = np.array([f['uv'][k] for k in f['vertices']], float)
            z = np.cross(p[1] - p[0], p[2] - p[0]); z /= np.linalg.norm(z)
            # x along the texture's +u on this face, so the glow sits square on its texels
            to3d = lambda c: np.linalg.solve(np.vstack([uv.T, np.ones(3)]), np.r_[c, 1]) @ p
            x = to3d(uv[0] + [1, 0]) - to3d(uv[0]); x /= np.linalg.norm(x)
            basis = np.array([x, np.cross(z, x), z]).T
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                rot = Rotation.from_matrix(basis).as_euler('ZYX', degrees=True)[::-1]
            tx = np.array(eye_texels, float)
            ulo, uhi = tx.min(0), tx.max(0) + 1
            corners_uv = np.array([[ulo[0], ulo[1]], [uhi[0], ulo[1]], [ulo[0], uhi[1]], [uhi[0], uhi[1]]])
            # uv -> barycentric (affine over the planar face) -> 3D
            bary = np.linalg.solve(np.vstack([uv.T, np.ones(3)]), np.vstack([corners_uv.T, np.ones(4)])).T
            qe = (bary @ p - p[0]) @ basis
            elo, ehi = qe[:, :2].min(0), qe[:, :2].max(0)
            ec = p[0] + basis[:, :2] @ ((elo + ehi) / 2) + basis[:, 2] * EYE_LIFT - K
            espan = ehi - elo
            tiles.append(Image.new('RGBA', (len(eye_texels), 1), eye_rgb + (255,)))
            eel = {'from': (ec - np.r_[espan / 2, 0]).tolist(), 'to': (ec + np.r_[espan / 2, 0]).tolist(),
                   'rotation': {'origin': ec.tolist(), **dict(zip('xyz', map(float, rot)))},
                   'faces': {}, 'shade': False, 'light_emission': 15}
            pending.append((eel, len(tiles) - 1, True))
            els.append(eel)
            eye_done = True
        for group in leftover:
            el, tile = _bake_group(part, group, tex, K)
            tiles.append(tile)
            pending.append((el, len(tiles) - 1, double))
            els.append(el)
            records.append({'part': part['name'], 'source_face_ids': [f['source_face_id'] for f in group], 'baked': True})
        parts.append((part, K, els))
    used_textures = sorted({t for _, t, _, _ in direct})
    first = len(tiles)
    tiles += [rig.images[t][1].convert('RGBA') for t in used_textures]
    atlas, placements = pack_tiles(tiles)
    aw, ah = atlas.size
    for el, t, (u0, v0, u1, v1), double in direct:
        ox, oy = placements[first + used_textures.index(t)]
        uv = [(ox + u0) * 16 / aw, (oy + v0) * 16 / ah, (ox + u1) * 16 / aw, (oy + v1) * 16 / ah]
        el['faces']['south'] = {'uv': uv, 'texture': '#0', 'tintindex': 0}
        if double:
            el['faces']['north'] = {'uv': [uv[2], uv[1], uv[0], uv[3]], 'texture': '#0', 'tintindex': 0}
    for el, ti, double in pending:
        ox, oy = placements[ti]
        w, h = tiles[ti].size
        u0, v0, u1, v1 = ox * 16 / aw, oy * 16 / ah, (ox + w) * 16 / aw, (oy + h) * 16 / ah
        el['faces']['south'] = {'uv': [u0, v0, u1, v1], 'texture': '#0', 'tintindex': 0}
        if double:
            el['faces']['north'] = {'uv': [u1, v0, u0, v1], 'texture': '#0', 'tintindex': 0}
    out_parts = []
    import json
    for part, K, els in parts:
        model = {'textures': {'0': f'rpg:item/{key}/atlas', 'particle': f'rpg:item/{key}/atlas'}, 'elements': els}
        _js(rp / f'assets/rpg/models/{key}/{part["name"]}.json', model)
        _js(rp / f'assets/rpg/items/{key}/{part["name"]}.json',
            {'model': {'type': 'minecraft:model', 'model': f'rpg:{key}/{part["name"]}',
                       'tints': [{'type': 'minecraft:custom_model_data', 'index': 0, 'default': 16777215}]}})
        out_parts.append({k: part[k] for k in ['name', 'source_name', 'bone', 'mesh_uuid']}
                         | {'K': K.tolist(), 'triangles': len(els), 'quads': sum(len(e['faces']) for e in els)}
                         | ({'source_element_type': 'cube', 'source_cube_uuids': part['source_cube_uuids']}
                            if part.get('source_element_type') == 'cube' else {}))
    path = rp / f'assets/rpg/textures/item/{key}/atlas.png'
    path.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(path)
    return out_parts, records, {'material': 'plain', 'atlas_size_pixels': [aw, ah],
                                'direct_quads': len(direct), 'baked_faces': len(pending),
                                'eye_quad': eye_done}


def _js(path, doc):
    import json
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
