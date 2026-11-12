"""Generic Dungeons → display-rig conversion (any exported skeletal or static mesh).

Generalises phase2_static.py / animations.py, which were written for the Jungle
Abomination only, so other exported actors can be converted the same way:

* several materials per mesh: each primitive's material JSON names its albedo
  (and optional emissive) texture; every texture becomes its own atlas tile;
* static meshes (no skin) get one synthetic root bone;
* animations: any codec CUE4Parse decoded; explicit key-time arrays are used
  as given; additive clips are skipped and reported;
* mixed-skin surfaces are assigned rigidly to the triangle's dominant bone
  (no derived affine tracks);
* display parts: plane groups whose rest rotation relative to their bone is a
  single axis within ±45° merge into that bone's part (what display_mob allows),
  so the part count stays near the bone count;
* baked cutout tiles use about one sample per source texel, so the item atlas
  is not inflated.

Coordinates: unit_scale is Java model pixels per UE centimetre (keep it small so
every part stays inside the -16..32 model limit); the runtime display scale is
model_scale = blocks_per_cm * 16 / unit_scale.
"""
from __future__ import annotations

import base64
import hashlib
import json
import math
import uuid
from collections import defaultdict
from pathlib import Path

import numpy as np
from PIL import Image

import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parent))   # phase2_static imports source_math unqualified
from source_math import (C, _glb, about, build_bb_skeleton, euler_zyx_matrix, load_source, matrix_to_euler_zyx,  # noqa: E402
                         quat_matrix, transform_points, ue_to_java)
import animations as A  # noqa: E402
import source_math as _SM  # noqa: E402


def _stable_euler_zyx(rotation):
    """source_math.matrix_to_euler_zyx, and where it cannot rebuild the matrix (keys within ~1e-9 of
    gimbal lock, as in a Tower Guard clip) the better of two atan2 decompositions."""
    try:
        return _SM_matrix_to_euler_zyx(rotation)
    except ValueError:
        pass
    r = np.asarray(rotation, dtype=float)
    cy = math.hypot(r[0, 0], r[1, 0])
    y = math.atan2(-r[2, 0], cy)
    options = [np.degrees([math.atan2(r[2, 1], r[2, 2]), y, math.atan2(r[1, 0], r[0, 0])]),
               np.degrees([math.atan2(-r[1, 2], r[1, 1]), y, 0.])]
    out = min(options, key=lambda e: np.max(abs(euler_zyx_matrix(e) - r)))
    if np.max(abs(euler_zyx_matrix(out) - r)) > 1e-7:
        raise ValueError('ZYX decomposition failed to reconstruct the source rotation')
    return out


_SM_matrix_to_euler_zyx = _SM.matrix_to_euler_zyx
A.matrix_to_euler_zyx = _stable_euler_zyx
matrix_to_euler_zyx = _stable_euler_zyx  # noqa: F811
from phase2_static import canonical_basis, face_corners, indexed_components, plane_basis, rectangular_uv  # noqa: E402


def pack_tiles(tiles):
    """Shelf-pack into the smallest power-of-two square (phase2_static starts at 1024,
    which would put a 64x64 source texture into a 1024x1024 item-atlas sprite)."""
    size = 16
    while size <= 8192:
        x = y = row = 0
        placements, ok = [], True
        for tile in tiles:
            w, h = tile.size
            if w > size or h > size:
                ok = False
                break
            if x + w > size:
                x, y, row = 0, y + row, 0
            if y + h > size:
                ok = False
                break
            placements.append((x, y))
            x += w
            row = max(row, h)
        if ok:
            atlas = Image.new('RGBA', (size, size))
            for tile, pos in zip(tiles, placements):
                atlas.paste(tile, pos)
            return atlas, placements
        size *= 2
    raise ValueError('Atlas exceeds 8192 pixels')

NS = uuid.UUID('6f1f6b8e-2b7a-4f0c-9a53-1d2c0b7e9a41')
ALBEDO_KEYS = ('Texture', 'BaseColor', 'Base Color', 'Diffuse', 'Albedo', 'Color')
SKIP_TEXTURE = ('_S', '_N', '_M', '_R', '_Mask', 'Noise', 'Clouds', 'Specular')


def uid(text):
    return str(uuid.uuid5(NS, text))


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


# ---------------------------------------------------------------------------
# Materials
# ---------------------------------------------------------------------------
def texture_png(export_root, ue_path):
    """'Dungeons/Content/X/T_Y.T_Y' -> <export_root>/assets/Dungeons/Content/X/T_Y.png"""
    package = ue_path.split('.')[0]
    return Path(export_root) / 'assets' / (package + '.png')


def material_textures(export_root, material_name):
    """(albedo_png, emissive_png or None) named by a material/material-instance JSON."""
    found = list((Path(export_root) / 'assets').rglob(material_name + '.json'))
    if not found:
        raise FileNotFoundError('material JSON not exported: ' + material_name)
    textures = read(found[0]).get('Textures', {})
    albedo = None
    for key in ALBEDO_KEYS:
        if key in textures:
            albedo = textures[key]
            break
    if albedo is None:
        def skipped(path):
            tail = path.split('.')[-1]
            return any(tail.endswith(s) for s in SKIP_TEXTURE[:5]) or any(s in tail for s in SKIP_TEXTURE[5:])
        names = [v for k, v in textures.items() if not skipped(v) and 'Emiss' not in k]
        if not names and textures:
            names = list(textures.values())        # effect materials (e.g. a gradient orb): their only texture
        if not names:
            raise ValueError('no texture in ' + material_name)
        albedo = names[0]
    emissive = None
    for key, value in textures.items():
        tail = value.split('.')[-1]
        if 'Emiss' in key or tail.endswith('_E'):
            emissive = value
            break
    a = texture_png(export_root, albedo)
    e = texture_png(export_root, emissive) if emissive else None
    if not a.exists():
        raise FileNotFoundError('albedo texture not exported: ' + str(a))
    return a, (e if e and e.exists() else None)


# ---------------------------------------------------------------------------
# Source loading (skinned or static)
# ---------------------------------------------------------------------------
STATIC_META = {'bones': [{'index': 0, 'name': 'root', 'parent': -1, 'translation': [0, 0, 0],
                          'rotation': [0, 0, 0, 1], 'scale': [1, 1, 1]}]}


def load_static(mesh):
    document, accessor, blob = _glb(mesh)
    vertices, uvs, triangles, ranges = [], [], [], []
    vb = tb = 0
    for node in document['nodes']:
        if 'mesh' not in node:
            continue
        for primitive in document['meshes'][node['mesh']]['primitives']:
            pos = accessor(primitive['attributes']['POSITION']).astype(float)
            uv = accessor(primitive['attributes']['TEXCOORD_0']).astype(float)
            tri = accessor(primitive['indices']).reshape(-1, 3).astype(np.int64)
            material = document.get('materials', [])[primitive['material']].get('name') if 'material' in primitive else None
            vertices.append(pos); uvs.append(uv); triangles.append(tri + vb)
            ranges.append({'material': material, 'vertex_start': vb, 'vertex_count': len(pos),
                           'triangle_start': tb, 'triangle_count': len(tri)})
            vb += len(pos); tb += len(tri)
    pos = np.concatenate(vertices)
    n = len(pos)
    return {'mesh_sha256': hashlib.sha256(blob).hexdigest(), 'bones': STATIC_META['bones'],
            'vertices_ue_cm': pos[:, [0, 2, 1]] * 100., 'uv': np.concatenate(uvs),
            'triangles': np.concatenate(triangles), 'weights': np.ones((n, 1)),
            'joint_source_indices': np.zeros((n, 1), dtype=np.int64), 'primitive_ranges': ranges}


def load_any(mesh, meta=None):
    if meta is None:
        return load_static(mesh), STATIC_META
    meta_doc = read(meta) if not isinstance(meta, dict) else meta
    return load_source(mesh, meta_doc), meta_doc


# ---------------------------------------------------------------------------
# Skeleton with rest scale
# ---------------------------------------------------------------------------
def ue_world(bones, animated_local=None):
    """World matrices including each bone's rest scale (uniform scale assumed per bone)."""
    out = []
    for i, b in enumerate(bones):
        local = np.eye(4)
        rot = quat_matrix(b['rotation']) if animated_local is None else animated_local[i][0]
        pos = b['translation'] if animated_local is None else animated_local[i][1]
        local[:3, :3] = rot @ np.diag(b['scale'])
        local[:3, 3] = pos
        out.append(out[b['parent']] @ local if b['parent'] >= 0 else local)
    return np.asarray(out)


def world_scales(bones):
    """Uniform world scale of each bone (mean of its world axis lengths)."""
    w = ue_world(bones)
    return np.linalg.norm(w[:, :3, :3], axis=1).mean(axis=1)


def build_skeleton(meta, unit_scale):
    """Like source_math.build_bb_skeleton, but accepts non-unit rest scale: pivots come from the
    scaled world positions, Blockbench rotations from the orthonormal part of each world matrix."""
    import uuid as _uuid
    bones = meta['bones']
    world = ue_world(bones)
    pivots, bb_world, groups, rot_world = [], [], {}, []
    for i, b in enumerate(bones):
        m = world[i][:3, :3]
        u, _s, vt = np.linalg.svd(m)
        r = u @ vt
        if np.linalg.det(r) < 0:
            u[:, -1] *= -1
            r = u @ vt
        rj = C @ r @ C.T
        rot_world.append(rj)
        world_pivot = ue_to_java(world[i][:3, 3], unit_scale)
        parent = b['parent']
        # A Blockbench origin lives in the parent's rest (unrotated) space: parent_world @ origin
        # must land on the bone's world position, so map the world pivot back through the parent.
        pivot = transform_points(np.linalg.inv(bb_world[parent]), world_pivot) if parent >= 0 else world_pivot
        local = (rot_world[parent].T @ rj) if parent >= 0 else rj
        euler = matrix_to_euler_zyx(local)
        transform = (bb_world[parent] if parent >= 0 else np.eye(4)) @ about(pivot, euler_zyx_matrix(euler))
        pivots.append(pivot)
        bb_world.append(transform)
        groups[b['name']] = {'name': b['name'], 'origin': pivot.tolist(), 'rotation': euler.tolist(),
                             'uuid': str(_uuid.uuid5(NS, 'bone:' + b['name'])), 'export': True, 'visibility': True,
                             'isOpen': True, 'children': []}
    outliner = []
    for b in bones:
        g = groups[b['name']]
        if b['parent'] < 0:
            outliner.append(g)
        else:
            groups[bones[b['parent']]['name']]['children'].append(g)
    state = {'bone_names': [b['name'] for b in bones], 'bb_world': np.asarray(bb_world)}
    return groups, outliner, state


# ---------------------------------------------------------------------------
# Static conversion
# ---------------------------------------------------------------------------
def aligned_basis(points, triangles, owner_rotation):
    """In-plane axes along a boundary edge; of all boundary edges, the one whose basis lies
    closest to the owner bone's axes (a lone triangle would otherwise pick its diagonal)."""
    normal = np.cross(points[triangles[0, 1]] - points[triangles[0, 0]], points[triangles[0, 2]] - points[triangles[0, 0]])
    normal /= np.linalg.norm(normal)
    edges = defaultdict(int)
    for tri in triangles:
        for i in range(3):
            edges[tuple(sorted((int(tri[i]), int(tri[(i + 1) % 3]))))] += 1
    candidates = [e for e, n in edges.items() if n == 1] or list(edges)
    best = None
    for a, b in candidates:
        x = points[b] - points[a]
        x -= np.dot(x, normal) * normal
        if np.linalg.norm(x) < 1e-12:
            continue
        x /= np.linalg.norm(x)
        basis = canonical_basis(np.column_stack((x, np.cross(normal, x), normal)), owner_rotation)
        score = np.linalg.norm(owner_rotation.T @ basis - np.eye(3))
        if best is None or score < best[0] - 1e-9:
            best = (score, basis)
    return best[1]


def bake_tile(points, uv, triangles, axes, lo, hi, texture, samples_per_texel=2.0):
    a, b = axes
    xy = points[:, axes]
    dx, dy = hi[a] - lo[a], hi[b] - lo[b]
    th, tw = texture.shape[:2]
    density = np.zeros(2)
    for tri in triangles:
        p = xy[tri]
        coeff = np.linalg.solve(np.c_[p, np.ones(3)], uv[tri] * [tw, th])
        density = np.maximum(density, np.linalg.norm(coeff[:2], axis=1))
    width = max(2, int(math.ceil(dx * density[0] * samples_per_texel)))
    height = max(2, int(math.ceil(dy * density[1] * samples_per_texel)))
    # a surface whose UVs repeat the texture many times (a spear shaft) would bake a strip hundreds of
    # texels long; four repeats of the texture is plenty for a display model
    cap = min(512, 4 * max(tw, th))
    width, height = min(width, cap), min(height, cap)
    x = lo[a] + (np.arange(width) + .5) * dx / width
    y = hi[b] - (np.arange(height) + .5) * dy / height
    xx, yy = np.meshgrid(x, y)
    sample = np.stack([xx, yy, np.ones_like(xx)], axis=-1)
    result = np.zeros((height, width, texture.shape[2]), dtype=np.uint8)
    for tri in triangles:
        bary = sample @ np.linalg.inv(np.c_[xy[tri], np.ones(3)])
        mask = np.all(bary >= -1e-10, axis=-1)
        s = bary @ uv[tri]
        sx = np.floor(s[:, :, 0] * tw).astype(int) % tw
        sy = np.floor(s[:, :, 1] * th).astype(int) % th
        result[mask] = texture[sy[mask], sx[mask]]
    return Image.fromarray(result)


def matrix_quat(r):
    """3x3 rotation -> (x, y, z, w), the inverse of quat_matrix."""
    w = math.sqrt(max(0., 1 + r[0, 0] + r[1, 1] + r[2, 2])) / 2
    x = math.copysign(math.sqrt(max(0., 1 + r[0, 0] - r[1, 1] - r[2, 2])) / 2, r[2, 1] - r[1, 2])
    y = math.copysign(math.sqrt(max(0., 1 - r[0, 0] + r[1, 1] - r[2, 2])) / 2, r[0, 2] - r[2, 0])
    z = math.copysign(math.sqrt(max(0., 1 - r[0, 0] - r[1, 1] + r[2, 2])) / 2, r[1, 0] - r[0, 1])
    return [x, y, z, w]


def with_attachments(source, meta_doc, attachments):
    """Rigidly attached static meshes (blueprint.blueprint_attachments): each becomes a bone of its own,
    child of the bone it hangs on, so it animates with it and keeps a part name of its own."""
    meta_doc = dict(meta_doc)
    bones = [dict(b) for b in meta_doc['bones']]
    index = {b['name']: i for i, b in enumerate(bones)}
    for att in attachments:
        m = np.asarray(att['matrix'], dtype=float)
        s = float(np.cbrt(abs(np.linalg.det(m[:3, :3]))))
        bones.append({'name': att['name'], 'parent': index[att['bone']], 'translation': m[:3, 3].tolist(),
                      'rotation': matrix_quat(m[:3, :3] / s), 'scale': [s, s, s]})
        index[att['name']] = len(bones) - 1
    meta_doc['bones'] = bones
    world = ue_world(bones)
    src = dict(source)
    k = src['weights'].shape[1]
    vertices, uv, triangles, weights, joints = ([src['vertices_ue_cm']], [src['uv']], [src['triangles']],
                                                [src['weights']], [src['joint_source_indices']])
    ranges = list(src['primitive_ranges'])
    nv, nt = len(src['vertices_ue_cm']), len(src['triangles'])
    for att in attachments:
        static = load_static(att['mesh'])
        w = world[index[att['name']]]
        v = static['vertices_ue_cm'] @ w[:3, :3].T + w[:3, 3]
        vertices.append(v); uv.append(static['uv']); triangles.append(static['triangles'] + nv)
        wt = np.zeros((len(v), k)); wt[:, 0] = 1
        jt = np.zeros((len(v), k), dtype=np.int64); jt[:, 0] = index[att['name']]
        weights.append(wt); joints.append(jt)
        for r in static['primitive_ranges']:
            ranges.append(dict(r, material=att.get('material') or r['material'],
                               vertex_start=r['vertex_start'] + nv, triangle_start=r['triangle_start'] + nt))
        nv += len(v); nt += len(static['triangles'])
    src.update(vertices_ue_cm=np.concatenate(vertices), uv=np.concatenate(uv), triangles=np.concatenate(triangles),
               weights=np.concatenate(weights), joint_source_indices=np.concatenate(joints), primitive_ranges=ranges)
    return src, meta_doc


def convert(mesh, meta, export_root, out, *, name, unit_scale=.0192, part_prefix=None, emissive_threshold=60,
            material_textures_override=None, glow_color=None, glow_share=.3, attachments=()):
    """Write <out>/<name>.bbmodel, parts.json, glow_bones.json, atlas.png; return a report."""
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    prefix = part_prefix or name
    source, meta_doc = load_any(mesh, meta)
    if attachments:
        source, meta_doc = with_attachments(source, meta_doc, attachments)
    groups, outliner, state = build_skeleton(meta_doc, unit_scale)
    vertices = ue_to_java(source['vertices_ue_cm'], unit_scale)
    triangles = source['triangles']
    uv = source['uv']
    owners = source['joint_source_indices'][np.arange(len(vertices)), np.argmax(source['weights'], axis=1)]

    # material -> texture tile
    tex_index, tiles, tex_arrays, emissive_arrays, tri_texture = {}, [], [], [], np.zeros(len(triangles), dtype=int)
    for r in source['primitive_ranges']:
        mat = r['material']
        if mat not in tex_index:
            if material_textures_override and mat in material_textures_override:
                albedo, emissive = material_textures_override[mat]
            else:
                albedo, emissive = material_textures(export_root, mat)
            img = Image.open(albedo).convert('RGBA')
            tex_index[mat] = len(tiles)
            tiles.append(img)
            tex_arrays.append(np.array(img))
            if emissive is not None:
                e = Image.open(emissive).convert('RGB').resize(img.size, Image.NEAREST)
                emissive_arrays.append(np.array(e).max(axis=2))
            else:
                emissive_arrays.append(None)
        tri_texture[r['triangle_start']:r['triangle_start'] + r['triangle_count']] = tex_index[mat]
    n_textures = len(tiles)

    # surfaces: connected planar components per texture and owner
    surfaces = []
    for ids in indexed_components(triangles):
        by_tex = defaultdict(list)
        for t in ids:
            by_tex[int(tri_texture[t])].append(t)
        for tex, sub in by_tex.items():
            vids = np.unique(triangles[sub].ravel())
            p = vertices[vids]
            centered = p - p.mean(0)
            _, _, vh = np.linalg.svd(centered, full_matrices=False)
            planar = float(abs(centered @ vh[-1]).max()) <= unit_scale * .003
            # Rigid skinning: a planar piece belongs to the bone most of its vertices follow.
            # (Splitting a quad between bones would leave single triangles, whose longest edge
            # is the diagonal; that rotates the plane basis 45 degrees off the texture.)
            if planar:
                surfaces.append((sub, tex, int(np.bincount(owners[vids]).argmax())))
                continue
            # a box or other solid: one surface per plane (two triangles of a face -> one quad)
            planes = defaultdict(list)
            for t in sub:
                a, b, c = vertices[triangles[t]]
                n = np.cross(b - a, c - a)
                norm = np.linalg.norm(n)
                if norm < 1e-12:
                    continue
                n = n / norm
                key = (tuple(np.round(n, 3)), round(float(n @ a) / (unit_scale * .01), 0))
                planes[key].append(t)
            for tris in planes.values():
                pv = np.unique(triangles[tris].ravel())
                surfaces.append((tris, tex, int(np.bincount(owners[pv]).argmax())))

    elements, parts, records = [], [], []
    for sid, (ids, tex, owner) in enumerate(surfaces):
        vids = np.unique(triangles[ids].ravel())
        mapping = {int(v): i for i, v in enumerate(vids)}
        tri = np.array([[mapping[int(v)] for v in t] for t in triangles[ids]])
        p = vertices[vids]
        suv = uv[vids]
        owner_name = state['bone_names'][owner]
        owner_world = state['bb_world'][owner]
        basis = aligned_basis(p, tri, owner_world[:3, :3])
        texture = tex_arrays[tex]
        tsize = np.array([texture.shape[1], texture.shape[0]])
        # glow: share of emissive texels under the surface's UVs
        glow = False
        if emissive_arrays[tex] is not None:
            px = np.clip((suv * tsize).astype(int), 0, tsize - 1)
            lo_px, hi_px = px.min(0), px.max(0) + 1
            region = emissive_arrays[tex][lo_px[1]:hi_px[1], lo_px[0]:hi_px[0]]
            glow = region.size > 0 and float((region > emissive_threshold).mean()) > .5
        if not glow and glow_color is not None:
            # no emissive map: glow where the user asked for a colour (e.g. a staff gem)
            px = np.clip((suv * tsize).astype(int), 0, tsize - 1)
            lo_px, hi_px = px.min(0), px.max(0) + 1
            region = texture[lo_px[1]:hi_px[1], lo_px[0]:hi_px[0]].reshape(-1, 4)
            region = region[region[:, 3] > 127].astype(int)
            glow = len(region) > 0 and float(glow_color(region).mean()) >= glow_share
        part = None
        for candidate in parts:
            if candidate['owner'] == owner and candidate['glow'] == glow and np.max(abs(candidate['basis'] - basis)) < 2e-5:
                local = transform_points(candidate['inverse_world'], p)
                if min(np.ptp(local, axis=0)) < unit_scale * .003:
                    part = candidate
                    break
        if part is None:
            pname = '%s_%s_%03d' % (prefix, owner_name.lower(), len(parts))
            relative = owner_world[:3, :3].T @ basis
            rotation = matrix_to_euler_zyx(relative)
            pivot = np.array(groups[owner_name]['origin'])
            world = owner_world @ about(pivot, euler_zyx_matrix(rotation))
            group = {'name': pname, 'uuid': uid(name + ':bone:' + pname), 'origin': pivot.tolist(),
                     'rotation': rotation.tolist(), 'export': True, 'visibility': True, 'isOpen': False, 'children': []}
            groups[pname] = group
            groups[owner_name]['children'].append(group)
            part = {'name': pname, 'owner': owner, 'owner_bone': owner_name, 'basis': basis, 'glow': glow,
                    'inverse_world': np.linalg.inv(world), 'rotation': rotation}
            parts.append(part)
        local = transform_points(part['inverse_world'], p)
        lo = local.min(0); hi = local.max(0)
        flat = int(np.argmin(hi - lo))
        axes = [i for i in range(3) if i != flat]
        lo[flat] = hi[flat] = float(local[:, flat].mean())
        face_names = [('west', 'east'), ('down', 'up'), ('north', 'south')][flat]
        area = sum(np.linalg.norm(np.cross(local[t[1]] - local[t[0]], local[t[2]] - local[t[0]])) / 2 for t in tri)
        bbox_area = float(np.prod((hi - lo)[axes]))
        fills = bbox_area > 0 and abs(area - bbox_area) < max(1e-9, bbox_area * 1e-5)
        coeff = np.linalg.lstsq(np.c_[local[:, axes], np.ones(len(local))], suv, rcond=None)[0]
        uv_error = float(abs(np.c_[local[:, axes], np.ones(len(local))] @ coeff - suv).max())
        face_data, tile_index = {}, tex
        if fills and uv_error < 2e-6:
            for face in face_names:
                corner_uv = np.c_[face_corners(face, lo, hi)[:, axes], np.ones(4)] @ coeff * tsize
                data = rectangular_uv(corner_uv, 2e-3)
                if data is None:
                    face_data = {}
                    break
                face_data[face] = data
        if not face_data:
            tile = bake_tile(local, suv, tri, axes, lo, hi, texture)
            tile_index = len(tiles)
            tiles.append(tile)
            for face in face_names:
                fc = face_corners(face, lo, hi)
                tuv = np.c_[(fc[:, axes[0]] - lo[axes[0]]) / (hi[axes[0]] - lo[axes[0]]) * tile.width,
                            (hi[axes[1]] - fc[:, axes[1]]) / (hi[axes[1]] - lo[axes[1]]) * tile.height]
                face_data[face] = rectangular_uv(tuv)
        element_id = uid(name + ':element:' + ','.join(map(str, ids)))
        elements.append({'name': 'f%d' % sid, 'type': 'cube', 'uuid': element_id, 'from': lo.tolist(), 'to': hi.tolist(),
                         'origin': groups[part['name']]['origin'], 'rotation': [0, 0, 0], 'autouv': 0, 'faces': face_data,
                         'rescale': False, 'locked': False, 'visibility': True, 'export': True, 'color': sid % 8,
                         '_tile': tile_index})
        groups[part['name']]['children'].append(element_id)
        records.append({'element': element_id, 'part': part['name'], 'owner': owner_name, 'triangles': list(map(int, ids)),
                        'direct_uv': tile_index < n_textures, 'glow': glow})

    atlas, placements = pack_tiles(tiles)
    for el in elements:
        ox, oy = placements[el.pop('_tile')]
        for data in el['faces'].values():
            u0, v0, u1, v1 = data['uv']
            data['uv'] = [u0 + ox, v0 + oy, u1 + ox, v1 + oy]
            if not data.get('rotation'):
                data.pop('rotation', None)
    atlas.save(out / 'atlas.png')
    serialized = [{k: v for k, v in g.items() if k != 'children'} for g in groups.values()]

    def outline(node):
        return {'uuid': node['uuid'], 'children': [outline(c) if isinstance(c, dict) else c for c in node['children']]}

    doc = {'meta': {'format_version': '5.0', 'model_format': 'free', 'box_uv': False}, 'name': name,
           'model_identifier': name, 'visible_box': [0, 0, 0], 'variable_placeholders': '',
           'resolution': {'width': atlas.width, 'height': atlas.height}, 'elements': elements, 'groups': serialized,
           'outliner': [outline(n) for n in outliner],
           'textures': [{'path': 'atlas.png', 'name': 'atlas.png', 'uuid': uid(name + ':atlas'), 'id': '0',
                         'width': atlas.width, 'height': atlas.height, 'uv_width': atlas.width, 'uv_height': atlas.height,
                         'particle': True, 'visible': True, 'internal': True,
                         'source': 'data:image/png;base64,' + base64.b64encode((out / 'atlas.png').read_bytes()).decode()}],
           'animations': [], 'display_dungeons': {'generic': True, 'source_mesh_sha256': source['mesh_sha256'],
                                                  'unit_scale_java_pixels_per_ue_cm': unit_scale}}

    # display parts: plane groups merge into their bone where display_mob allows it
    display = defaultdict(list)
    separate = []
    for part in parts:
        rot = np.asarray(part['rotation'])
        big = [i for i in range(3) if abs(rot[i]) > 1e-3]
        if len(big) <= 1 and all(abs(rot[i]) <= 45 + 1e-3 for i in big):
            display[part['owner_bone']].append(part['name'])
        else:
            separate.append(part['name'])
    part_rows = [{'name': bone.lower(), 'bones': [bone] + members} for bone, members in display.items()]
    part_rows += [{'name': n, 'bones': [n]} for n in separate]
    glow = sorted(p['name'] for p in parts if p['glow'])
    (out / (name + '.bbmodel')).write_text(json.dumps(doc, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    (out / 'parts.json').write_text(json.dumps(part_rows, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    (out / 'glow_bones.json').write_text(json.dumps(glow) + '\n', encoding='utf-8')
    report = {'name': name, 'source_mesh_sha256': source['mesh_sha256'], 'triangles': int(len(triangles)),
              'all_triangles_covered_once': sorted(t for r in records for t in r['triangles']) == list(range(len(triangles))),
              'bones': len(source['bones']), 'plane_groups': len(parts), 'display_parts': len(part_rows),
              'elements': len(elements), 'direct_uv_elements': sum(r['direct_uv'] for r in records),
              'baked_elements': sum(not r['direct_uv'] for r in records), 'glow_groups': len(glow),
              'textures': {m: i for m, i in tex_index.items()}, 'atlas': list(atlas.size)}
    (out / 'conversion.json').write_text(json.dumps(report, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    return doc, report


# ---------------------------------------------------------------------------
# Animations
# ---------------------------------------------------------------------------
class Clip(A.SourceClip):
    """SourceClip without the Jungle-only codec / composite restrictions."""

    def __init__(self, path, bones, obj, sequence_obj):
        self.path = Path(path)
        self.payload = read(path)
        self.obj = obj
        self.original_name = obj['Name']
        self.name = self.original_name.lower()
        props = obj['Properties']
        self.length = float(props['SequenceLength'])
        self.kind = obj['Type']
        self.bones = bones
        self.by_name = {b['name']: b['index'] for b in bones}
        self.sequence = self.payload['sequences'][0]
        if self.sequence.get('IsAdditive'):
            raise ValueError('additive')
        self.num_frames = int(self.sequence['NumFrames'])
        self.start, self.end, self.rate, self.start_pos = 0., self.length, 1., 0.
        self.sequence_length = float(sequence_obj['Properties']['SequenceLength'])
        if self.kind == 'AnimComposite':
            seg = props['AnimationTrack']['AnimSegments'][0]
            self.start = float(seg['AnimStartTime']); self.end = float(seg['AnimEndTime'])
            self.rate = float(seg.get('AnimPlayRate', 1))
        tracks = {t['boneName']: t for t in self.sequence['tracks']}
        self.channels = []
        for b in bones:
            t = tracks.get(b['name'], {})
            row = {}
            for channel, rest in (('position', b['translation']), ('rotation', b['rotation'])):
                row[channel] = (A.source_key_times(t, channel, self.sequence_length, self.num_frames),
                                np.asarray(t.get(channel, []), dtype=float), np.asarray(rest, dtype=float))
            self.channels.append(row)
        self.pose_cache = {}

    def world(self, time):
        """UE world matrices at `time`, with each bone's rest scale (SourceClip omits scale)."""
        key = round(min(self.length, max(0., time)), 12)
        if key not in self.pose_cache:
            animated = [(quat_matrix(self.sample(i, 'rotation', key)), self.sample(i, 'position', key))
                        for i in range(len(self.bones))]
            self.pose_cache[key] = ue_world(self.bones, animated)
        return self.pose_cache[key]


def notifies(obj):
    """[(seconds, notify name, notify object)] from an AnimSequence's Notifies."""
    out = []
    for n in obj['Properties'].get('Notifies', []) or []:
        t = float(n.get('LinkValue', 0)) + float(n.get('TriggerTimeOffset', 0))
        ref = (n.get('Notify') or {}).get('ObjectName', '') or ''
        out.append((round(t, 4), n.get('NotifyName'), ref.split("'")[0] if ref else None))
    return sorted(out)


def anim_objects(metadata_dir):
    """{animation name: (tracks.json path, uobject dict)} under one or more exported metadata trees
    (several trees: a mob borrowing clips of another mob on the same skeleton)."""
    found = {}
    dirs = [metadata_dir] if isinstance(metadata_dir, (str, Path)) else list(metadata_dir)
    for tracks in (t for d in dirs for t in Path(d).rglob('*.tracks.json')):
        stem = tracks.name[:-len('.tracks.json')]
        obj_path = tracks.with_name(stem + '.uobject.json')
        if obj_path.exists() and stem not in found:
            found[stem] = (tracks, read(obj_path))
    return found


def author(document, meta, mesh, metadata_dir, clips, *, max_error_visual_pixels=.25, model_scale=1.):
    """clips: [(source animation name, new clip name, loop)]. Returns (document, report)."""
    doc = json.loads(json.dumps(document))
    groups, parents, rest_world = A._hierarchy(doc)
    unit_scale = float(doc['display_dungeons']['unit_scale_java_pixels_per_ue_cm'])
    source, meta_doc = load_any(mesh, meta)
    bones = source['bones']
    S = np.eye(4); S[:3, :3] = C * unit_scale; Sinv = np.linalg.inv(S)
    rest_ue = ue_world(bones)
    rest_h_inv = np.linalg.inv(S @ np.asarray(rest_ue) @ Sinv)
    # an animated offset lives in the parent's scaled space; Blockbench offsets are unscaled
    scales = world_scales(bones)
    parent_scale = {b['name']: (scales[b['parent']] if b['parent'] >= 0 else 1.) for b in bones}

    def make_channels(clip, extra):
        channels, counts = A._make_channels(clip, bones, groups, unit_scale, extra)
        for name, ch in channels.items():
            times, values = ch['position']
            ch['position'] = (times, np.asarray(values) * parent_scale[name])
        return channels, counts
    rest_bb = np.asarray([rest_world[b['name']] for b in bones])
    objects = anim_objects(metadata_dir)
    animations, reports = [], []
    for src_name, new_name, loop in clips:
        if src_name not in objects:
            raise KeyError('animation not exported: ' + src_name)
        tracks, obj = objects[src_name]
        seq_obj = obj
        if obj['Type'] == 'AnimComposite':
            seq_name = read(tracks)['sequences'][0]['Name']
            seq_obj = objects[seq_name][1]
        clip = Clip(tracks, bones, obj, seq_obj)
        clip.name = new_name
        extra, iterations = {}, 0
        for iterations in range(12):
            channels, counts = make_channels(clip, extra)
            checks = A._validate(channels, clip, source, groups, rest_bb, rest_h_inv, S, Sinv, unit_scale, model_scale)
            bad = [v for v in checks if max(v['bone_error_visual_pixels'], v['vertex_error_visual_pixels']) > max_error_visual_pixels * .8]
            if not bad:
                break
            added = 0
            for row in bad:
                time = row['time']
                for i, b in enumerate(bones):
                    times, values = channels[b['name']]['rotation']
                    value = A.sample_channel(times, values, time, [0, 0, 0]) + groups[b['name']].get('rotation', [0, 0, 0])
                    true = C @ quat_matrix(clip.sample(i, 'rotation', time)) @ C.T
                    if np.max(abs(euler_zyx_matrix(value) - true)) > 1e-10 and time not in extra.setdefault(i, set()):
                        extra[i].add(time); added += 1
            if not added:
                break
        animations.append(A._bb_animation(clip, channels, groups, loop, {}))
        reports.append({'clip': new_name, 'source': src_name, 'seconds': clip.length, 'loop': loop,
                        'ticks': int(math.ceil(clip.length * 20)),
                        'max_bone_error_px': max(x['bone_error_visual_pixels'] for x in checks),
                        'max_vertex_error_px': max(x['vertex_error_visual_pixels'] for x in checks),
                        'notifies': notifies(obj)})
    doc['animations'] = animations
    return doc, reports


def list_animations(metadata_dir):
    rows = []
    for name, (tracks, obj) in sorted(anim_objects(metadata_dir).items()):
        p = obj.get('Properties', {})
        rows.append({'name': name, 'type': obj.get('Type'), 'seconds': p.get('SequenceLength'),
                     'notifies': notifies(obj)})
    return rows
