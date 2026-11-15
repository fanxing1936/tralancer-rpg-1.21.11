"""Independent source glTF/bin -> actual saved armor bbmodel audit; no BB calls."""
import base64
from collections import Counter, deque
import hashlib
import io
import json
from pathlib import Path
import numpy as np
from PIL import Image

ROOT=Path(__file__).parent
DEST=Path(r'D:\agent\claude\github-create\tralancer-rpg-1.21.11\_tools\lucifer_ref\separate')
BB=DEST/'verdant_robe_original.bbmodel'
EXPECTED_HASH='9b925550ce92a88c28d8d8100d040fefaaca851c491aeae1a5af123cc6008354'
PLAYER=ROOT/'exported/Game/Actors/Characters/Player/Master/SK_Player_Master.gltf'
PNG=ROOT/'exported/Game/Actors/Equipment/Armor/EvocationRobe_Unique2/T_EvocationRobe_Unique2.png'
ASSEMBLY=ROOT/'verdant_assembly.json'
SIDECAR=ROOT/'verdant_for_blockbench_source_data.json'
DTYPE={5120:'<i1',5121:'<u1',5122:'<i2',5123:'<u2',5125:'<u4',5126:'<f4'}
WIDTH={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def decode(path):
    g=json.loads(path.read_text());blobs=[(path.parent/b['uri']).read_bytes() for b in g['buffers']]
    def read(i):
        a=g['accessors'][i];v=g['bufferViews'][a['bufferView']];dt=np.dtype(DTYPE[a['componentType']]);n=WIDTH[a['type']]
        return np.ndarray((a['count'],n),dtype=dt,buffer=blobs[v['buffer']],
            offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',n*dt.itemsize),dt.itemsize)).copy()
    return g,read


def qmat(q):
    x,y,z,w=q
    return np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],
        [2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],
        [2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])


def eulermat(v):
    x,y,z=np.radians(v);cx,sx=np.cos(x),np.sin(x);cy,sy=np.cos(y),np.sin(y);cz,sz=np.cos(z),np.sin(z)
    return np.array([[cz,-sz,0],[sz,cz,0],[0,0,1]])@np.array([[cy,0,sy],[0,1,0],[-sy,0,cy]])@np.array([[1,0,0],[0,cx,-sx],[0,sx,cx]])


def eulerq(v):
    x,y,z=np.radians(v)/2;cx,sx=np.cos(x),np.sin(x);cy,sy=np.cos(y),np.sin(y);cz,sz=np.cos(z),np.sin(z)
    return np.array([sx*cy*cz-cx*sy*sz,cx*sy*cz+sx*cy*sz,cx*cy*sz-sx*sy*cz,cx*cy*cz+sx*sy*sz])


def clip(poly,axis,value,greater):
    out=[]
    for i,p in enumerate(poly):
        q=poly[(i+1)%len(poly)];ip=p[axis]>=value if greater else p[axis]<=value;iq=q[axis]>=value if greater else q[axis]<=value
        if ip:out.append(p)
        if ip != iq:
            t=(value-p[axis])/(q[axis]-p[axis]);out.append(p+t*(q-p))
    return out


def tri_area_cell(tri,x,y):
    p=list(np.asarray(tri,float))
    for a,v,ge in [(0,x,True),(0,x+1,False),(1,y,True),(1,y+1,False)]:
        p=clip(p,a,v,ge)
        if len(p)<3:return 0.
    p=np.array(p);return abs(np.dot(p[:,0],np.roll(p[:,1],-1))-np.dot(p[:,1],np.roll(p[:,0],-1)))/2


def center_in_tri(t,x,y):
    p=np.array([x+.5,y+.5]);cross=[]
    for i in range(3):
        a=t[i];b=t[(i+1)%3];e=b-a;d=p-a;cross.append(e[0]*d[1]-e[1]*d[0])
    return min(cross)>=-1e-10 or max(cross)<=1e-10


def uv_coverage(source_parts,rgba):
    h,w=rgba.shape[:2];area_counts=np.zeros((h,w),int);center_counts=np.zeros((h,w),int);owners={};face_rows=[]
    for name,v,uv,idx in source_parts:
        for f in range(0,len(idx),2):
            # Original meshes pair successive triangles into source quad faces.
            tris=[uv[t] for t in idx[f:f+2]];alluv=np.concatenate(tris);lo=np.floor(alluv.min(axis=0)).astype(int);hi=np.ceil(alluv.max(axis=0)).astype(int)
            area_mask=np.zeros((h,w),bool);center_mask=np.zeros((h,w),bool)
            for y in range(max(0,lo[1]),min(h,hi[1])):
                for x in range(max(0,lo[0]),min(w,hi[0])):
                    area_mask[y,x]=any(tri_area_cell(t,x,y)>1e-12 for t in tris)
                    center_mask[y,x]=any(center_in_tri(t,x,y) for t in tris)
            owner=f'{name}:q{f//2}';area_counts+=area_mask;center_counts+=center_mask
            for y,x in zip(*np.where(area_mask)):owners.setdefault(f'{x},{y}',[]).append(owner)
            face_rows.append({'source_face':owner,'triangle_indices':[f,f+1],'uv_corners_by_triangle':[t.tolist() for t in tris],
                              'uv_bounds_pixels':np.r_[alluv.min(axis=0),alluv.max(axis=0)].tolist(),
                              'texel_cells_with_positive_area':int(area_mask.sum()),'texel_centers_inside':int(center_mask.sum())})
    alpha=rgba[:,:,3];black=(alpha>0)&np.all(rgba[:,:,:3]==0,axis=2);padding=np.zeros_like(black)
    queue=deque((y,x) for y,x in zip(*np.where(black)) if y in [0,h-1] or x in [0,w-1])
    while queue:
        y,x=queue.popleft()
        if padding[y,x]:continue
        padding[y,x]=True
        for yy,xx in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)]:
            if 0<=yy<h and 0<=xx<w and black[yy,xx] and not padding[yy,xx]:queue.append((yy,xx))
    effective=(alpha>0)&~padding
    masks={'transparent':alpha==0,'opaque_nonblack':(alpha>0)&~black,
           'edge_connected_opaque_black_padding_candidate':padding,'isolated_opaque_black':black&~padding,
           'effective_pattern_including_isolated_black':effective,'all_opaque':alpha>0,'all_pixels':np.ones((h,w),bool)}
    classes={}
    for label,mask in masks.items():
        classes[label]={'total':int(mask.sum()),'unused_positive_area':int((mask&(area_counts==0)).sum()),
                        'single_original_face_positive_area':int((mask&(area_counts==1)).sum()),
                        'multiple_original_faces_positive_area':int((mask&(area_counts>1)).sum()),
                        'unused_texel_center':int((mask&(center_counts==0)).sum())}
    unused=effective&(area_counts==0);seen=np.zeros_like(unused);components=[]
    for y,x in zip(*np.where(unused)):
        if seen[y,x]:continue
        q=deque([(y,x)]);pixels=[]
        while q:
            yy,xx=q.popleft()
            if seen[yy,xx]:continue
            seen[yy,xx]=True;pixels.append([int(xx),int(yy)])
            for y2,x2 in [(yy-1,xx),(yy+1,xx),(yy,xx-1),(yy,xx+1)]:
                if 0<=y2<h and 0<=x2<w and unused[y2,x2] and not seen[y2,x2]:q.append((y2,x2))
        a=np.array(pixels);components.append({'pixels':len(pixels),'bbox_half_open':np.r_[a.min(axis=0),a.max(axis=0)+1].tolist(),'coordinates':pixels})
    repeated={p:o for p,o in owners.items() if len(o)>1}
    return {'method':'UV0 triangle-cell positive-area intersection, unioned per original quad so its diagonal is not counted as reuse; also reports texel-center sampling. Atlas clipped to [0,64]^2, no unverified wrap extrapolation.',
            'padding_caveat':'Edge-connected opaque black is an operational padding-candidate class, not a proven material-use semantic. Never force every atlas pixel onto geometry.',
            'classes':classes,'effective_unused_components':components,'face_count':len(face_rows),'per_source_face_uv_table':face_rows,
            'positive_area_original_face_use_count_grid':area_counts.tolist(),'texel_center_original_face_use_count_grid':center_counts.tolist(),
            'original_repeated_texels_and_source_faces':repeated,'max_original_face_reuse':int(area_counts.max()),
            'original_reuse_conclusion':'Any overlap or unused texels reported here occur in the original Verdant mesh UVs. Do not change original UVs to force complete atlas usage or artificial uniqueness.'}


def main():
    saved=BB.read_bytes();bb=json.loads(saved);assembly=json.loads(ASSEMBLY.read_text());side=json.loads(SIDECAR.read_text())
    meshes={e['name']:e for e in bb['elements'] if e.get('type')=='mesh'};bones={e['name']:e for e in bb['elements'] if e.get('type')=='armature_bone'}
    arms=[e for e in bb['elements'] if e.get('type')=='armature'];elements={e['uuid']:e for e in bb['elements']};parents={}
    def tree(n,parent=None):
        uid=n if isinstance(n,str) else n['uuid'];parents[uid]=parent
        if isinstance(n,dict):
            for child in n.get('children',[]):tree(child,uid)
    for n in bb['outliner']:tree(n)
    player,pread=decode(PLAYER);jointnodes=player['skins'][0]['joints'];jointnames=[player['nodes'][i]['name'] for i in jointnodes]
    ibms=pread(player['skins'][0]['inverseBindMatrices']).astype(float);bind={name:np.linalg.inv(ibms[i].reshape(4,4,order='F')) for i,name in enumerate(jointnames)}
    rows=[];source_parts=[];all_weights=[];side_rows=[];D=np.diag([-16.,16.,-16.,1.])
    for part in assembly['parts']:
        path=Path(part['gltf']);g,read=decode(path);name=g['nodes'][0]['name'];mesh=meshes[name]
        p=g['meshes'][0]['primitives'][0];attrs=p['attributes'];v=read(attrs['POSITION']).astype(float);uv=read(attrs['TEXCOORD_0']).astype(float)*64;idx=read(p['indices']).reshape(-1,3).astype(int)
        M=np.array(part['mesh_local_gltf_to_java']);Mcheck=D@bind[part['bone']]@np.array(part['socket_local_gltf_matrix'])@np.array(part['component_local_gltf_matrix'])
        C=np.array([[.01,0,0,0],[0,0,.01,0],[0,.01,0,0],[0,0,0,1.]])
        cp=part['component_resolved_transform'];pitch,yaw,roll=np.radians(cp['rotation']['value'])
        def rx(a):return np.array([[1,0,0],[0,np.cos(a),-np.sin(a)],[0,np.sin(a),np.cos(a)]])
        def ry(a):return np.array([[np.cos(a),0,np.sin(a)],[0,1,0],[-np.sin(a),0,np.cos(a)]])
        def rz(a):return np.array([[np.cos(a),-np.sin(a),0],[np.sin(a),np.cos(a),0],[0,0,1]])
        cpue=np.eye(4);cpue[:3,:3]=rz(yaw)@ry(-pitch)@rx(-roll)@np.diag(cp['scale']['value']);cpue[:3,3]=cp['location']['value']
        cpcheck=C@cpue@np.linalg.inv(C)
        component_trs_delta=float(abs(cpcheck-np.array(part['component_local_gltf_matrix'])).max())
        expected=(M@np.c_[v,np.ones(len(v))].T).T[:,:3];keys=[f'v{i}' for i in range(len(v))];got=np.array([mesh['vertices'][k] for k in keys]);delta=got-expected
        recovered=(np.linalg.inv(M)@np.c_[got,np.ones(len(got))].T).T[:,:3];back_delta=recovered-v
        points=[{'vertex':f'v{i}','source_java':expected[i].tolist(),'saved_java':got[i].tolist(),'delta':delta[i].tolist()} for i in range(len(v)) if np.any(delta[i]!=0)]
        faces=list(mesh['faces'].items());ordered_diffs=[];topology_diffs=[];uv_diffs=[];tex_diffs=[];weight_diffs=[];face_mapping=[]
        for i,t in enumerate(idx):
            fid,f=faces[i];actual=[int(x[1:]) for x in f['vertices']]
            if actual!=t.tolist():ordered_diffs.append({'triangle':i,'expected':t.tolist(),'actual':actual})
            if not any(actual==t.tolist()[n:]+t.tolist()[:n] for n in range(3)):topology_diffs.append(i)
            for key in f['vertices']:
                vi=int(key[1:]);du=np.array(f['uv'][key])-uv[vi]
                if np.any(du!=0):uv_diffs.append({'triangle':i,'vertex':key,'source':uv[vi].tolist(),'saved':f['uv'][key],'delta':du.tolist()})
            if f.get('texture')!=0:tex_diffs.append(fid)
            face_mapping.append({'source_primitive':0,'source_triangle_index':i,'source_quad_index':i//2,
                'source_vertex_indices':t.tolist(),'native_face_uuid':fid,'native_vertex_keys':f['vertices'],
                'source_local_positions_gltf_m':v[t].tolist(),'source_uv0_pixels64':uv[t].tolist(),
                'saved_java_positions_by_native_key':{k:mesh['vertices'][k] for k in f['vertices']},
                'saved_uv_by_native_key':f['uv'],'saved_texture_index':f.get('texture')})
        for i in range(len(v)):
            wk=mesh['uuid'][:6]+':'+f'v{i}';actual={n:b.get('vertex_weights',{}).get(wk,0) for n,b in bones.items() if isinstance(b.get('vertex_weights'),dict) and b['vertex_weights'].get(wk,0)!=0}
            all_weights.append(wk)
            if actual!={part['bone']:1}:weight_diffs.append({'vertex':i,'expected':{part['bone']:1},'actual':actual})
        sp=next(x for x in side['parts'] if x['name']==name)['primitives'][0]
        attr_checks={a:bool(np.array_equal(read(i),np.array(sp['source_attributes'][a]))) for a,i in attrs.items()}
        side_rows.append({'mesh':name,'all_source_attributes_exact_in_sidecar':all(attr_checks.values()),'attribute_checks':attr_checks,
                          'source_triangle_indices_exact_in_sidecar':bool(np.array_equal(idx,np.array(sp['source_triangle_indices'])))})
        rows.append({'name':name,'semantic_part':part['part'],'native_mesh_uuid':mesh['uuid'],
            'source_gltf':str(path),'source_gltf_sha256':sha(path),'source_bin':part['bin'],'source_bin_sha256':sha(Path(part['bin'])),
            'mesh_local_gltf_to_java':M.tolist(),'source_to_native_triangle_face_mapping':face_mapping,
            'source_vertices':len(v),'saved_vertices':len(mesh['vertices']),'source_triangles':len(idx),'saved_triangles':len(faces),
            'source_vertex_keys_exact':set(keys)==set(mesh['vertices']),
            'position_max_abs_error_java_pixels':float(abs(delta).max()),'position_nonzero_delta_vertices':len(points),'position_differences':points,
            'inverse_assembly_source_space_max_abs_error_m':float(abs(back_delta).max()),
            'assembly_matrix_max_difference_vs_direct_binary_bind_composition':float(abs(M-Mcheck).max()),
            'component_matrix_max_error_vs_independent_euler_trs':component_trs_delta,
            'original_component_scale':cp['scale']['value'],
            'component_scale_baked_in_positions':True,
            'uv_max_abs_error_source_pixels':max((max(abs(x) for x in d['delta']) for d in uv_diffs),default=0),
            'uv_differing_face_corners':len(uv_diffs),'uv_differences':uv_diffs,
            'exact_triangle_index_order_differences':ordered_diffs,'topology_or_winding_differences':topology_diffs,
            'weight_differences':weight_diffs,'weight_provenance':'Derived rigid weight 1 to original socket bone. Original source is StaticMesh and has no skin weight attribute.',
            'texture_reference_differences':tex_diffs,'mesh_origin':mesh.get('origin'),'mesh_rotation':mesh.get('rotation'),
            'mesh_parent_is_armature':parents.get(mesh['uuid'])==arms[0]['uuid'],'binding_bone':part['bone']})
        source_parts.append((name,v,uv,idx))
    extra_weight_keys=[]
    for name,bone in bones.items():
        weights=bone.get('vertex_weights',{})
        if isinstance(weights,dict):
            extra_weight_keys += [{'bone':name,'key':k,'weight':v} for k,v in weights.items() if k not in all_weights]
    sourceparents={c:i for i,n in enumerate(player['nodes']) for c in n.get('children',[])};n2j={n:i for i,n in enumerate(jointnodes)};bone_rows=[];sw={};nw={}
    for ji,ni in enumerate(jointnodes):
        n=player['nodes'][ni];bone=bones[n['name']];origin=np.array(n.get('translation',[0,0,0]))*[-16,16,-16];q=np.array(n.get('rotation',[0,0,0,1]))*[-1,1,-1,1];qn=q/np.linalg.norm(q);sr=qmat(qn);nr=eulermat(bone['rotation']);aq=eulerq(bone['rotation'])
        if np.dot(aq,q)<0:aq=-aq
        pj=n2j.get(sourceparents.get(ni));parent_name=jointnames[pj] if pj is not None else arms[0]['name'];actual_parent=elements.get(parents.get(bone['uuid']),{}).get('name')
        sm=np.eye(4);sm[:3,:3]=sr;sm[:3,3]=origin;nm=np.eye(4);nm[:3,:3]=nr;nm[:3,3]=bone['origin'];sw[ji]=(sw[pj] if pj is not None else np.eye(4))@sm;nw[ji]=(nw[pj] if pj is not None else np.eye(4))@nm
        bone_rows.append({'name':n['name'],'expected_parent':parent_name,'actual_parent':actual_parent,'parent_matches':parent_name==actual_parent,
            'source_raw_quaternion_java':q.tolist(),'source_raw_quaternion_norm':float(np.linalg.norm(q)),
            'saved_euler_zyx_degrees':bone['rotation'],'source_local_origin_java':origin.tolist(),'saved_local_origin':bone['origin'],
            'local_origin_max_abs_error_java_pixels':float(abs(origin-np.array(bone['origin'])).max()),
            'rotation_matrix_max_error_vs_normalized_source':float(abs(sr-nr).max()),'raw_quaternion_component_max_error':float(abs(aq-q).max()),
            'hierarchy_world_origin_max_error_java_pixels':float(abs(sw[ji][:3,3]-nw[ji][:3,3]).max())})
    embedded=base64.b64decode(bb['textures'][0]['source'].split(',',1)[1]);source_png=PNG.read_bytes();rgba=np.array(Image.open(io.BytesIO(source_png)).convert('RGBA'));native_rgba=np.array(Image.open(io.BytesIO(embedded)).convert('RGBA'))
    tex={'path':str(PNG),'source_sha256':hashlib.sha256(source_png).hexdigest(),'embedded_sha256':hashlib.sha256(embedded).hexdigest(),
         'png_bytes_equal':embedded==source_png,'rgba_differing_pixels':int(np.any(rgba!=native_rgba,axis=2).sum()),
         'embedded_texture_count':len(bb['textures']),'resolution':bb['resolution'],
         'native_settings':{k:v for k,v in bb['textures'][0].items() if k not in ['source']}}
    texture_rows=[]
    for nt in bb['textures']:
        source_path=next((ROOT/'exported').rglob(nt['name']));raw=source_path.read_bytes();emb=base64.b64decode(nt['source'].split(',',1)[1])
        ra=np.array(Image.open(io.BytesIO(raw)).convert('RGBA'));ea=np.array(Image.open(io.BytesIO(emb)).convert('RGBA'))
        texture_rows.append({'name':nt['name'],'source_path':str(source_path),'source_sha256':hashlib.sha256(raw).hexdigest(),
            'embedded_sha256':hashlib.sha256(emb).hexdigest(),'png_bytes_equal':raw==emb,
            'rgba_differing_pixels':int(np.any(ra!=ea,axis=2).sum()),'saved_texture_id':nt['id'],'saved_uuid':nt['uuid']})
    coverage=uv_coverage(source_parts,rgba)
    summary={'meshes':len(meshes),'vertices':sum(r['saved_vertices'] for r in rows),'triangles':sum(r['saved_triangles'] for r in rows),'bones':len(bones),'armatures':len(arms),
        'source_vertex_keys_all_exact':all(r['source_vertex_keys_exact'] for r in rows),
        'position_max_abs_error_java_pixels':max(r['position_max_abs_error_java_pixels'] for r in rows),
        'inverse_source_space_max_abs_error_m':max(r['inverse_assembly_source_space_max_abs_error_m'] for r in rows),
        'uv_max_abs_error_source_pixels':max(r['uv_max_abs_error_source_pixels'] for r in rows),
        'exact_triangle_order_differences':sum(len(r['exact_triangle_index_order_differences']) for r in rows),
        'topology_or_winding_differences':sum(len(r['topology_or_winding_differences']) for r in rows),
        'weight_differing_vertices':sum(len(r['weight_differences']) for r in rows),'extra_weight_keys':len(extra_weight_keys),
        'mesh_parent_mismatches':sum(not r['mesh_parent_is_armature'] for r in rows),'bone_parent_mismatches':sum(not b['parent_matches'] for b in bone_rows),
        'bone_local_origin_max_abs_error_java_pixels':max(b['local_origin_max_abs_error_java_pixels'] for b in bone_rows),
        'bone_rotation_matrix_max_error_vs_normalized_source':max(b['rotation_matrix_max_error_vs_normalized_source'] for b in bone_rows),
        'bone_raw_quaternion_component_max_error':max(b['raw_quaternion_component_max_error'] for b in bone_rows),
        'bone_world_origin_max_error_java_pixels':max(b['hierarchy_world_origin_max_error_java_pixels'] for b in bone_rows),
        'png_bytes_equal':tex['png_bytes_equal'],'rgba_differing_pixels':tex['rgba_differing_pixels'],
        'all_two_texture_png_bytes_equal':len(texture_rows)==2 and all(t['png_bytes_equal'] for t in texture_rows),
        'all_texture_rgba_differing_pixels':sum(t['rgba_differing_pixels'] for t in texture_rows),
        'normals_tangents_uv1_sidecar_all_exact':all(r['all_source_attributes_exact_in_sidecar'] for r in side_rows),
        'actual_bbmodel_hash_matches_requested':hashlib.sha256(saved).hexdigest()==EXPECTED_HASH}

    summary['mesh_object_transforms_neutral']=all(m.get('origin',[0,0,0])==[0,0,0] and m.get('rotation',[0,0,0])==[0,0,0] and m.get('scale',[1,1,1])==[1,1,1] for m in meshes.values())
    summary['paired_triangles_share_one_diagonal_four_vertices']=all(len(idx)%2==0 and all(len(set(idx[i])&set(idx[i+1]))==2 and len(set(idx[i])|set(idx[i+1]))==4 for i in range(0,len(idx),2)) for name,v,uv,idx in source_parts)
    summary['component_matrix_max_error_vs_independent_euler_trs']=max(r['component_matrix_max_error_vs_independent_euler_trs'] for r in rows)
    summary['assembly_matrix_max_error_vs_direct_binary_bind']=max(r['assembly_matrix_max_difference_vs_direct_binary_bind_composition'] for r in rows)
    material=bb.get('dungeons_material_source',{})
    material_checks={
        'correct_original_material':material.get('original_material')=='/Game/Actors/Equipment/Armor/EvocationRobe_Unique2/MI_EvocationRobe_Unique2',
        'emissive_is_original_white':material.get('parameters',{}).get('Emissive')==[1,1,1],
        'natural_emissive_matches_serialized':material.get('parameters',{}).get('NaturalEmissive')==0.699999988079071,
        'effective_specular_texture_is_true':material.get('original_effective_switches',{}).get('SpecularTexture') is True,
        'auxiliary_hash_matches_original':material.get('source_auxiliary_png_sha256')==next(t['source_sha256'] for t in texture_rows if t['name'].endswith('_S.png')),
        'rendering_scope':'Metadata/source verification only. This audit does not execute the preview shader or certify full Unreal shading.'}
    report={'scope':'Independent original four mesh glTF/bin and player rig binary decode versus the actually saved Verdant bbmodel. No Blockbench operations; importer payload is not the source of truth.',
        'bbmodel':str(BB),'bbmodel_sha256':hashlib.sha256(saved).hexdigest(),'requested_hash':EXPECTED_HASH,
        'assembly':str(ASSEMBLY),'assembly_sha256':sha(ASSEMBLY),
        'player_source_gltf':str(PLAYER),'player_source_sha256':sha(PLAYER),'player_source_bin_sha256':sha(PLAYER.with_suffix('.bin')),
        'sidecar_sha256':sha(SIDECAR),'summary':summary,'parts':rows,'bones':bone_rows,'sidecar_validation':side_rows,'extra_weight_keys':extra_weight_keys,
        'textures':texture_rows,'saved_dungeons_material_metadata':material,'material_metadata_checks':material_checks,
        'original_uv_coverage':coverage,'conditional_assembly_status':assembly['status'],
        'nonuniform_scale_preservation':'Original Blueprint component TRS are baked in each original vertex; scalar scales are not substituted. The component matrix was independently reconstructed by UE Euler matrix products.',
        'geometry_acceptance':'Coordinates, original UV0, source triangle order and rigid binding are compared directly. Floating-point residuals and Euler normalization differences remain explicit.',
        'limits':['Normals, tangents and UV1 are exact in source sidecar; native importer does not consume them.',
            'Original StaticMesh has no skin weights. Weight 1 is the derived rigid attachment to the actual Blueprint socket/bone.',
            'Assembly uses original player binary inverse bind and actual component TRS; native Paperdoll skeletal assignment and reference-image runtime pose remain unproven.',
            'Omitted native component fields use explicitly documented standard defaults, not measured values.',
            'This file-only audit does not measure native bind deformation, animation, lighting, bloom, exposure, roughness or game runtime.',
            'Both original PNGs and static emissive metadata are verified, but metadata is not proof of executing the complete original shader. Effective switches use native compiled evidence, not all .props observations.'],
        'input_changed_during_validation':BB.read_bytes()!=saved}
    report['geometry_checks_pass']=all([
        summary['actual_bbmodel_hash_matches_requested'],(len(meshes),summary['vertices'],summary['triangles'],len(bones),len(arms))==(4,128,64,38,1),
        summary['source_vertex_keys_all_exact'],summary['mesh_object_transforms_neutral'],summary['paired_triangles_share_one_diagonal_four_vertices'],summary['position_max_abs_error_java_pixels']==0,summary['uv_max_abs_error_source_pixels']==0,
        summary['exact_triangle_order_differences']==0,summary['topology_or_winding_differences']==0,summary['weight_differing_vertices']==0,
        summary['extra_weight_keys']==0,summary['mesh_parent_mismatches']==0,summary['bone_parent_mismatches']==0,
        summary['all_two_texture_png_bytes_equal'],summary['normals_tangents_uv1_sidecar_all_exact'],
        summary['assembly_matrix_max_error_vs_direct_binary_bind']==0,summary['component_matrix_max_error_vs_independent_euler_trs']<1e-12,
        summary['bone_local_origin_max_abs_error_java_pixels']==0,summary['bone_rotation_matrix_max_error_vs_normalized_source']<1e-12,
        not report['input_changed_during_validation']])
    (DEST/'verdant_original_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Verdant Robe 原生保存独立回读核验','',f'文件：`{BB.name}`',f'SHA-256：`{report["bbmodel_sha256"]}`','',
        f'原始数据保真检查通过：**{report["geometry_checks_pass"]}**。直接解码四件原 glTF/bin 和原玩家骨架二进制 inverseBindMatrices，回读实际保存的 bbmodel；未以导入 JSON 替代原件真值，未操作 Blockbench。','',
        f'实际保存：{summary["meshes"]} Mesh、{summary["vertices"]} 顶点、{summary["triangles"]} 三角形、{summary["bones"]} 骨、{summary["armatures"]} Armature。','',
        '| 部件 | 顶点/三角 | 坐标最大差（Java 像素） | UV 差（原图像素） | 三角顺序差 | 权重差 |',
        '|---|---:|---:|---:|---:|---:|']
    for r in rows:lines.append(f'| {r["name"]} | {r["saved_vertices"]}/{r["saved_triangles"]} | {r["position_max_abs_error_java_pixels"]:.16g} | {r["uv_max_abs_error_source_pixels"]:.16g} | {len(r["exact_triangle_index_order_differences"])} | {len(r["weight_differences"])} |')
    lines += ['',f'反变换回原局部坐标的最大计算残差为 `{summary["inverse_source_space_max_abs_error_m"]:.16g}` 米。原 component 非均匀缩放已逐点烘入坐标；独立 UE Euler 矩阵重算 component TRS 最大残差 `{summary["component_matrix_max_error_vs_independent_euler_trs"]:.16g}`。保留残差原值，不改记为 0。',
        'JSON 包含全部 64 个三角形的原索引、原局部顶点、UV、native 面 UUID、实际保存坐标和纹理编号，另有 32 个原四边面 UV 覆盖表。',
        f'Mesh 父级差异 {summary["mesh_parent_mismatches"]}；骨父级差异 {summary["bone_parent_mismatches"]}。原件是 StaticMesh，依据实际骨/socket 建立的每点权重 1 属于派生刚性绑定，未冒称原件原有蒙皮权重。','',
        '## 骨架与纹理','',
        f'骨局部原点最大差 `{summary["bone_local_origin_max_abs_error_java_pixels"]:.16g}` Java 像素；Euler 矩阵相对归一化源四元数最大差 `{summary["bone_rotation_matrix_max_error_vs_normalized_source"]:.16g}`。',
        f'相对原十进制四元数的分量差 `{summary["bone_raw_quaternion_component_max_error"]:.16g}`；累计世界原点差 `{summary["bone_world_origin_max_error_java_pixels"]:.16g}` Java 像素。原 glTF 四元数并非严格单位，Euler 表示转换不能声称逐值相同。',
        f'原 Albedo 与原 S 两张 PNG 内嵌字节均相等：**{summary["all_two_texture_png_bytes_equal"]}**；RGBA 差异像素合计 **{summary["all_texture_rgba_differing_pixels"]}**。逐文件 SHA-256 见 JSON。',
        'S 贴图真实来源是 `EvocationRobe_Unique1/T_EvocationRobe_Unique1_S`，有本套 MI 引用依据；没有沿用 Root Rot 贴图或绿色发光向量。','',
        '## 原始 UV 使用','',
        '按原 UV 三角形与纹素方格的正面积交集统计；每原四边面两个三角形合并计一次，避免把对角线重复计数。另列纹素中心结果。黑色边界连通区仅标为 padding 候选，不当作已证实的材质语义。','',
        '| 类别 | 像素数 | 原件未覆盖 | 单原面覆盖 | 多原面共用 |','|---|---:|---:|---:|---:|']
    for k,c in coverage['classes'].items():lines.append(f'| {k} | {c["total"]} | {c["unused_positive_area"]} | {c["single_original_face_positive_area"]} | {c["multiple_original_faces_positive_area"]} |')
    lines += ['', '这些未用区和共用发生在原件本身，不是导入缺陷；忠实原件不能通过强行填满 atlas 或消除共用去改变原 UV。','',
        '## 核验范围','',
        '- 原始网格、UV、拓扑、刚性绑定和 PNG 保真；normals、tangents、UV1 逐值留在 sidecar，未声称 native importer 已消费。',
        '- 装配依据原玩家 binary bind、帽子 socket 和其余直接骨挂点，保留原 BP component TRS；未序列化字段采用明确标注的标准缺省值。native Paperdoll 骨架赋值与参考图运行时姿势仍未证实。',
        '- 本文件核验确认保存了白色 Emissive 参数、NaturalEmissive 和对应两张原纹理，及 native compiled 证明的 SpecularTexture=True。静态发光公式移植与主任务运行检查另有证据；本报告不凭 metadata 判定完整 Unreal 高光、粗糙度、Bloom、曝光或场景光照一致。',
        '- 本次不操作 Blockbench，不测游戏运行、动作或生命周期。','']
    (DEST/'verdant_original_validation.md').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps({'geometry_checks_pass':report['geometry_checks_pass'],'summary':summary,'coverage':coverage['classes']},ensure_ascii=False))


if __name__=='__main__':main()
