"""Reusable static source/Blockbench skeleton maths for Jungle Abomination.

Only static reference geometry is handled here; no bbmodel animation is authored.

    source = load_source(mesh_glb, skeleton_meta)
    groups, outliner, state = build_bb_skeleton(skeleton_meta, unit_scale=0.0192)
    java_vertices = ue_to_java(source['vertices_ue_cm'], state['unit_scale'])
    local_vertices = transform_points(state['bb_world_inverse'][bone_index], java_vertices)

groups maps original names to Blockbench group dictionaries; its children already
contain original child groups. Append element UUIDs to the owning group's children.
outliner is the list of root groups. state contains numpy matrices and verification.

Coordinate basis is Java=(-UE.X, UE.Z, -UE.Y). Default 0.0192 internal pixels/cm
combined with external model_scale=10 gives 0.192 final pixels/cm (root decides).
GLB joint quaternions and inverse-bind matrices are deliberately never used.

For future animation only: position offset = C*(t_local(t)-t_rest)*unit_scale;
rotation keys = unwrap(Euler_ZYX(C*R_local(t)*C^-1)) - rest_Euler. This module does
not sample source tracks or write animation keys.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct
from typing import Any
import uuid

import numpy as np

C = np.array([[-1., 0., 0.], [0., 0., 1.], [0., -1., 0.]])
DEFAULT_UNIT_SCALE = 0.0192
SCALE_TOLERANCE = 1e-6
UUID_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_URL, 'tralancer:lucifer_p2:source_skeleton')


def read_meta(meta: str | Path | dict[str, Any]) -> dict[str, Any]:
    if isinstance(meta, dict):
        return meta
    return json.loads(Path(meta).read_text(encoding='utf-8'))


def quat_matrix(quaternion) -> np.ndarray:
    q = np.asarray(quaternion, dtype=float)
    norm = np.linalg.norm(q)
    if not np.isfinite(norm) or norm < 1e-15:
        raise ValueError('Invalid source quaternion')
    x, y, z, w = q / norm
    return np.array([[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)],
                     [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w)],
                     [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y)]])


def euler_zyx_matrix(degrees) -> np.ndarray:
    x, y, z = np.radians(np.asarray(degrees, dtype=float))
    cx, cy, cz, sx, sy, sz = np.cos(x), np.cos(y), np.cos(z), np.sin(x), np.sin(y), np.sin(z)
    return np.array([[cz*cy, cz*sy*sx-sz*cx, cz*sy*cx+sz*sx],
                     [sz*cy, sz*sy*sx+cz*cx, sz*sy*cx-cz*sx],
                     [-sy, cy*sx, cy*cx]])


def matrix_to_euler_zyx(rotation) -> np.ndarray:
    """Return XYZ degrees whose Rz@Ry@Rx matches display_mob.euler()."""
    rotation = np.asarray(rotation, dtype=float)
    y = np.arcsin(np.clip(-rotation[2, 0], -1., 1.))
    if abs(np.cos(y)) > 1e-8:
        x = np.arctan2(rotation[2, 1], rotation[2, 2])
        z = np.arctan2(rotation[1, 0], rotation[0, 0])
    else:
        x = np.arctan2(-rotation[1, 2], rotation[1, 1])
        z = 0.
    result = np.degrees([x, y, z])
    if np.max(abs(euler_zyx_matrix(result)-rotation)) > 2e-8:
        raise ValueError('ZYX decomposition failed to reconstruct the source rotation')
    return result


def about(pivot, rotation_matrix) -> np.ndarray:
    pivot = np.asarray(pivot, dtype=float)
    result = np.eye(4)
    result[:3, :3] = rotation_matrix
    result[:3, 3] = pivot - rotation_matrix @ pivot
    return result


def transform_points(matrix, points) -> np.ndarray:
    points = np.asarray(points, dtype=float)
    one_point = points.ndim == 1
    points = np.atleast_2d(points)
    result = (np.asarray(matrix) @ np.c_[points, np.ones(len(points))].T).T[:, :3]
    return result[0] if one_point else result


def ue_to_java(points_cm, unit_scale=DEFAULT_UNIT_SCALE) -> np.ndarray:
    return np.asarray(points_cm, dtype=float) @ C.T * unit_scale


def source_world_matrices(meta, *, include_scale=True) -> np.ndarray:
    bones = read_meta(meta)['bones']
    result = []
    for index, bone in enumerate(bones):
        if bone['index'] != index or not -1 <= bone['parent'] < index:
            raise ValueError('Expected contiguous, parent-before-child source bone indices')
        local = np.eye(4)
        local[:3, :3] = quat_matrix(bone['rotation'])
        if include_scale:
            local[:3, :3] = local[:3, :3] @ np.diag(bone['scale'])
        local[:3, 3] = bone['translation']
        result.append(result[bone['parent']] @ local if bone['parent'] >= 0 else local)
    return np.array(result)


def _glb(path):
    blob = Path(path).read_bytes()
    magic, version, declared_length = struct.unpack_from('<4sII', blob)
    if magic != b'glTF' or version != 2 or declared_length != len(blob):
        raise ValueError('Expected a complete glTF 2.0 binary')
    offset, document, binary = 12, None, None
    while offset < len(blob):
        length, kind = struct.unpack_from('<II', blob, offset)
        data = blob[offset+8:offset+8+length]
        if kind == 0x4e4f534a: document = json.loads(data)
        elif kind == 0x004e4942: binary = data
        offset += 8+length
    if document is None or binary is None: raise ValueError('Missing JSON/BIN chunk')

    def accessor(index):
        item = document['accessors'][index]
        if 'sparse' in item: raise ValueError('Sparse GLB accessors are not supported by this source reader')
        view = document['bufferViews'][item['bufferView']]
        if view.get('buffer', 0) != 0: raise ValueError('External GLB buffer is unsupported')
        count = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT4': 16}[item['type']]
        dt = np.dtype({5120:'i1', 5121:'u1', 5122:'<i2', 5123:'<u2', 5125:'<u4', 5126:'<f4'}[item['componentType']])
        result = np.ndarray((item['count'], count), dt, buffer=binary,
            offset=view.get('byteOffset', 0)+item.get('byteOffset', 0),
            strides=(view.get('byteStride', dt.itemsize*count), dt.itemsize)).copy()
        if item.get('normalized'):
            result = result.astype(float) / np.iinfo(dt).max
            if dt.kind == 'i': result = np.maximum(result, -1.)
        return result
    return document, accessor, blob


def load_source(mesh: str | Path, meta: str | Path | dict[str, Any]) -> dict[str, Any]:
    """Read geometry/UV/weights and map skin slots by name to original UE bone indices.

    Returns numpy arrays: positions_gltf_m, vertices_ue_cm, uv, triangles,
    weights, joint_source_indices, source_ue_world, source_rotation_world.
    Triangle indices address the concatenated vertex arrays. No cooked GLB joint
    rotation, pivot or inverse-bind is used. Non-identity mesh-node placement is
    rejected rather than silently mixing its transform with source coordinates.
    """
    metadata = read_meta(meta)
    bones = metadata['bones']
    indices = {bone['name']: bone['index'] for bone in bones}
    if len(indices) != len(bones): raise ValueError('Source bone names must be unique')
    document, accessor, blob = _glb(mesh)
    parents = {child: i for i, node in enumerate(document['nodes']) for child in node.get('children', [])}
    vertices, uv_values, triangles, weights, joints, ranges = [], [], [], [], [], []
    vertex_base, triangle_base = 0, 0
    for node_index, node in enumerate(document['nodes']):
        if 'mesh' not in node: continue
        if node_index in parents or any(key in node for key in ('matrix','translation','rotation','scale')):
            raise ValueError('Expected the raw CUE4Parse mesh node to have identity placement and no parent')
        if 'skin' not in node: raise ValueError('Expected a source skeletal mesh')
        skin_names = [document['nodes'][i]['name'] for i in document['skins'][node['skin']]['joints']]
        skin_to_source = np.array([indices[name] for name in skin_names], dtype=np.int64)
        for primitive_index, primitive in enumerate(document['meshes'][node['mesh']]['primitives']):
            if primitive.get('mode',4) != 4: raise ValueError('Expected triangle primitives')
            attrs = primitive['attributes']
            pos = accessor(attrs['POSITION']).astype(float)
            uv = accessor(attrs['TEXCOORD_0']).astype(float)
            tri = accessor(primitive['indices']).reshape(-1,3).astype(np.int64)
            weight = accessor(attrs['WEIGHTS_0']).astype(float)
            joint = skin_to_source[accessor(attrs['JOINTS_0']).astype(np.int64)]
            if 'WEIGHTS_1' in attrs or 'JOINTS_1' in attrs:
                weight = np.c_[weight, accessor(attrs['WEIGHTS_1'])]
                joint = np.c_[joint, skin_to_source[accessor(attrs['JOINTS_1']).astype(np.int64)]]
            vertices.append(pos); uv_values.append(uv); triangles.append(tri+vertex_base)
            weights.append(weight); joints.append(joint)
            material = document.get('materials',[])[primitive['material']].get('name') if 'material' in primitive else None
            ranges.append({'node': node_index, 'primitive': primitive_index, 'material': material,
                'vertex_start': vertex_base, 'vertex_count':len(pos), 'triangle_start':triangle_base, 'triangle_count':len(tri)})
            vertex_base += len(pos); triangle_base += len(tri)
    if not vertices: raise ValueError('No source mesh primitives')
    pos = np.concatenate(vertices)
    max_influences = max(weight.shape[1] for weight in weights)
    weights = [np.pad(weight,((0,0),(0,max_influences-weight.shape[1]))) for weight in weights]
    joints = [np.pad(joint,((0,0),(0,max_influences-joint.shape[1]))) for joint in joints]
    return {'mesh_path': str(mesh), 'mesh_sha256':hashlib.sha256(blob).hexdigest(), 'meta':metadata, 'bones':bones,
        'positions_gltf_m':pos, 'vertices_ue_cm':pos[:,[0,2,1]]*100.,
        'uv':np.concatenate(uv_values), 'triangles':np.concatenate(triangles),
        'weights':np.concatenate(weights), 'joint_source_indices':np.concatenate(joints),
        'source_ue_world':source_world_matrices(metadata),
        'source_rotation_world':source_world_matrices(metadata,include_scale=False), 'primitive_ranges':ranges}


def build_bb_skeleton(meta, unit_scale=DEFAULT_UNIT_SCALE):
    """Return (groups_by_original_name, nested_outliner, static_skeleton_state)."""
    if not np.isfinite(unit_scale) or unit_scale <= 0: raise ValueError('unit_scale must be positive')
    metadata = read_meta(meta)
    bones = metadata['bones']
    source_world = source_world_matrices(metadata)
    rotation_world = source_world_matrices(metadata,include_scale=False)
    scale_deviation = max(abs(float(v)-1) for bone in bones for v in bone['scale'])
    if scale_deviation > SCALE_TOLERANCE:
        raise ValueError(f'Nontrivial source rest scale {scale_deviation}; BB group scale is not representable')
    pivots, local_rotations, local_eulers, bb_world, groups = [], [], [], [], {}
    for i, bone in enumerate(bones):
        parent = bone['parent']
        pivot = (pivots[parent] if parent >= 0 else np.zeros(3)) + ue_to_java(bone['translation'],unit_scale)
        rotation = C @ quat_matrix(bone['rotation']) @ C.T
        euler = matrix_to_euler_zyx(rotation)
        transform = (bb_world[parent] if parent >= 0 else np.eye(4)) @ about(pivot,euler_zyx_matrix(euler))
        pivots.append(pivot); local_rotations.append(rotation); local_eulers.append(euler); bb_world.append(transform)
        groups[bone['name']] = {'name':bone['name'], 'origin':pivot.tolist(), 'rotation':euler.tolist(),
            'uuid':str(uuid.uuid5(UUID_NAMESPACE,bone['name'])), 'export':True, 'visibility':True, 'isOpen':True, 'children':[]}
    outliner = []
    for bone in bones:
        group = groups[bone['name']]
        if bone['parent'] < 0: outliner.append(group)
        else: groups[bones[bone['parent']]['name']]['children'].append(group)
    rows=[]
    for i,bone in enumerate(bones):
        actual_pivot = transform_points(bb_world[i],pivots[i])
        expected_pivot = ue_to_java(source_world[i][:3,3],unit_scale)
        expected_rotation = C @ rotation_world[i][:3,:3] @ C.T
        difference = bb_world[i][:3,:3] @ expected_rotation.T
        angle = np.degrees(np.arctan2(np.linalg.norm([difference[2,1]-difference[1,2],
            difference[0,2]-difference[2,0],difference[1,0]-difference[0,1]])/2,
            np.clip((np.trace(difference)-1)/2,-1,1)))
        rows.append({'bone':bone['name'], 'index':i, 'parent':bones[bone['parent']]['name'] if bone['parent']>=0 else None,
            'bb_pivot':pivots[i].tolist(),'rest_euler_xyz_degrees':local_eulers[i].tolist(),
            'expected_world_pivot_java':expected_pivot.tolist(),'bb_world_pivot_java':actual_pivot.tolist(),
            'pivot_error_internal_pixels':float(np.linalg.norm(actual_pivot-expected_pivot)),
            'rotation_error_degrees':float(angle)})
    validation={'bone_count':len(bones), 'max_pivot_error_internal_pixels':max(row['pivot_error_internal_pixels'] for row in rows),
        'max_rotation_error_degrees':max(row['rotation_error_degrees'] for row in rows),
        'source_rest_scale_max_deviation':scale_deviation,
        'rest_scale_policy':'Canonicalized to 1 only within 1e-6, preserving raw TRS separately; larger scale rejected.', 'bones':rows}
    if validation['max_pivot_error_internal_pixels'] > unit_scale*1e-3 or validation['max_rotation_error_degrees'] > 1e-5:
        raise ValueError(f'Static source/BB reference mismatch: {validation}')
    state={'unit_scale':float(unit_scale),'basis_ue_to_java':C.copy(),'bone_names':[b['name'] for b in bones],
        'parent_indices':[b['parent'] if b['parent']>=0 else None for b in bones],
        'parents':{b['name']:bones[b['parent']]['name'] if b['parent']>=0 else None for b in bones},
        'pivots':np.array(pivots),'local_rest_rotations':np.array(local_rotations),'rest_euler_degrees':np.array(local_eulers),
        'bb_world':np.array(bb_world),'bb_world_inverse':np.linalg.inv(np.array(bb_world)),
        'source_ue_world':source_world,'source_rotation_world':rotation_world,'validation':validation}
    return groups,outliner,state


def jsonable(value):
    if isinstance(value,np.ndarray):return value.tolist()
    if isinstance(value,np.generic):return value.item()
    if isinstance(value,dict):return {key:jsonable(child) for key,child in value.items()}
    if isinstance(value,(list,tuple)):return [jsonable(child) for child in value]
    return value


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mesh',type=Path,required=True)
    parser.add_argument('--meta',type=Path,required=True)
    parser.add_argument('--unit-scale',type=float,default=DEFAULT_UNIT_SCALE)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--display-mob',type=Path)
    args=parser.parse_args()
    source=load_source(args.mesh,args.meta)
    groups,outliner,state=build_bb_skeleton(args.meta,args.unit_scale)
    vertex_java=ue_to_java(source['vertices_ue_cm'],args.unit_scale)
    roundtrip_error=0.
    for i,name in enumerate(state['bone_names']):
        owned=np.any((source['joint_source_indices']==i)&(source['weights']>0),axis=1)
        local=transform_points(state['bb_world_inverse'][i],vertex_java[owned])
        restored=transform_points(state['bb_world'][i],local)
        if len(restored):roundtrip_error=max(roundtrip_error,float(np.max(np.linalg.norm(restored-vertex_java[owned],axis=1))))
    validation=dict(state['validation'])
    validation['max_geometry_inverse_roundtrip_internal_pixels']=roundtrip_error
    if args.display_mob:
        namespace={'__name__':'source_static_validation_display_mob','__file__':str(args.display_mob)}
        exec(compile(args.display_mob.read_text(encoding='utf-8'),str(args.display_mob),'exec'),namespace)
        pipeline_bones={name:{'parent':state['parents'][name],'pivot':group['origin'],'rotation':group['rotation']} for name,group in groups.items()}
        per_bone=[]
        for i,name in enumerate(state['bone_names']):
            matrix=np.array(namespace['posed_matrix'](pipeline_bones,name,{'tracks':{},'loop':False},0.))
            per_bone.append({'bone':name,'max_matrix_difference':float(np.max(abs(matrix-state['bb_world'][i]))),
                'world_pivot_error_internal_pixels':float(np.linalg.norm(transform_points(matrix,state['pivots'][i])-ue_to_java(source['source_ue_world'][i][:3,3],args.unit_scale)))})
        validation['display_mob_independent_comparison']={'source':str(args.display_mob),'bones':per_bone,
            'max_matrix_difference':max(row['max_matrix_difference'] for row in per_bone),
            'max_pivot_error_internal_pixels':max(row['world_pivot_error_internal_pixels'] for row in per_bone)}
    report={'source_mesh':str(args.mesh),'source_meta':str(args.meta),'source_mesh_sha256':source['mesh_sha256'],
        'unit_scale':args.unit_scale,'basis':C.tolist(),'validation':validation,
        'vertices':len(vertex_java),'triangles':len(source['triangles']),
        'scope':'Static reference skeleton only; no animations authored. GLB joint transforms/IBM never used.'}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(jsonable(report),ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({key:value for key,value in validation.items() if key not in ('bones','display_mob_independent_comparison')},indent=2))


if __name__=='__main__':main()
