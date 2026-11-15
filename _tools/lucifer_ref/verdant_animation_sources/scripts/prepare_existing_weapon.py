"""Read existing assets and the direct 1.21.11 client export; write scratch input only."""
from pathlib import Path
import base64
import hashlib
import json
import math
import zipfile
import numpy as np
from PIL import Image

WORK = Path(__file__).resolve().parent
REPO = Path(r'D:\agent\claude\github-create\tralancer-rpg-1.21.11')
ORIGINAL = Path(r'D:\agent\codex\TRA\work\lucifer_original')
MODEL = REPO / 'resourcepack/assets/rpg/models/item/lucifer_in_hand.json'
PNG = REPO / 'resourcepack/assets/rpg/textures/item/lucifer_in_hand.png'
BODY = REPO / '_tools/lucifer_ref/separate/mossy_skeleton_body_original.bbmodel'
GLTF = ORIGINAL / 'exported/Game/Actors/Characters/Enemies/Skeleton/SK_Skeleton.gltf'
JAR = Path(r'D:\minecraft\PCL启动器\.minecraft\versions\1.21.11-Fabric 0.19.3\1.21.11-Fabric 0.19.3.jar')

def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def T(v):
    m = np.eye(4); m[:3, 3] = v; return m
def S(v): return np.diag(list(v) + [1.0])
def R(axis, deg):
    a = math.radians(deg); c = math.cos(a); s = math.sin(a); m = np.eye(4)
    i,j = [(1,2),(2,0),(0,1)][axis]
    m[i,i]=m[j,j]=c; m[i,j]=-s; m[j,i]=s
    return m
def Q(q):
    x,y,z,w = np.array(q,dtype=float)/np.linalg.norm(q)
    return np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w),0],
                     [2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w),0],
                     [2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y),0],[0,0,0,1]])

generated = read(WORK/'weapon_existing_generated.json')
body_import = read(ORIGINAL/'body_for_blockbench.json')
gltf = read(GLTF)
parents={c:i for i,n in enumerate(gltf['nodes']) for c in n.get('children',[])}
source_world={}
def source_matrix(i):
    if i in source_world: return source_world[i]
    n=gltf['nodes'][i]
    m=T(n.get('translation',[0,0,0])) @ Q(n.get('rotation',[0,0,0,1])) @ S(n.get('scale',[1,1,1]))
    if i in parents: m=source_matrix(parents[i]) @ m
    source_world[i]=m;return m
C=S([-16,16,-16]);Ci=np.linalg.inv(C)
node_index={n.get('name'):i for i,n in enumerate(gltf['nodes'])}
source_java={name:C @ source_matrix(node_index[name]) @ Ci for name in ['J_R_Arm','J_R_Hand','J_R_Weapon']}

bb=read(BODY); elements={e['uuid']:e for e in bb['elements']}; native_world={}; native_by_name={}
def visit(nodes,parent=np.eye(4)):
    for entry in nodes:
        uid=entry if isinstance(entry,str) else entry['uuid']; e=elements.get(uid)
        if not e: continue
        m=np.eye(4)
        if e['type']=='armature_bone':
            x,y,z=e.get('rotation',[0,0,0]);m=T(e['origin']) @ R(2,z) @ R(1,y) @ R(0,x)
        world=parent @ m
        native_world[uid]=world;native_by_name[e['name']]=uid
        if isinstance(entry,dict):visit(entry.get('children',[]),world)
visit(bb['outliner'])
socket_world=native_world[native_by_name['J_R_Weapon']]
arm_world=native_world[native_by_name['J_R_Arm']]
bone=next(b for b in body_import['bones'] if b['name']=='J_R_Weapon')

# Exact client ItemTransform includes its final translate(-.5,-.5,-.5).
item_unit=np.array(generated['thirdperson_righthand_matrix_from_unit_model'])
item_pixels=item_unit @ S([1/16]*3)
VANILLA=S([-16,-16,16])
HOLD=R(0,-90) @ R(1,180) @ T([1/16,2/16,-10/16])
holder=VANILLA @ HOLD
legacy_world=T(arm_world[:3,3]) @ holder @ item_pixels
# Replace only the vanilla arm-to-grip translation with the evidenced source socket.
# Keep the existing Java held-item basis and existing item display transform.
holder_origin=holder[:3,3].copy()
socket_anchored_world=T(socket_world[:3,3]) @ T(-holder_origin) @ holder @ item_pixels
socket_local=np.linalg.inv(socket_world) @ socket_anchored_world
legacy_socket_local=np.linalg.inv(socket_world) @ legacy_world

vertices={};faces=[];weights={};raw_vertices={};raw_uvs={};face_provenance=[]
for ei,element in enumerate(generated['elements']):
    for fi,face in enumerate(element['faces']):
        keys=[];uv={}
        for ci,corner in enumerate(face['corners']):
            key=f'w{len(vertices)}';p=np.array(corner['position_model_pixels']+[1.0]); keys.append(key)
            vertices[key]=(socket_anchored_world @ p)[:3].tolist()
            raw_vertices[key]=p[:3].tolist()
            uv[key]=[float(corner['uv_normalized'][0]*32),float(corner['uv_normalized'][1]*32)]
            raw_uvs[key]=uv[key];weights[key]=[[bone['id'],1.0]]
        faces.append({'vertices':keys,'uv':uv})
        face_provenance.append({'native_face_index':len(faces)-1,'source_element':ei,'source_face':fi,'direction':face['direction']})

socket_asset=read(ORIGINAL/'Skeleton_Skeleton.parsed.json')
socket_record=next(e for e in socket_asset['exports'] if any(p.get('name')=='SocketName' and p.get('value')=='J_R_WeaponSocket' for p in e.get('properties',[])))
mesh_asset=read(ORIGINAL/'SK_Skeleton.parsed.json')
skeletal_refs=[p for e in mesh_asset['exports'] for p in e.get('properties',[]) if p.get('name')=='Skeleton']
source_files=[MODEL,PNG,BODY,GLTF,ORIGINAL/'Skeleton_Skeleton.parsed.json',REPO/'_tools/display_mob.py',REPO/'_tools/add_lucifer.py',REPO/'_tools/add_sunken_skeleton.py']
manifest={str(p):sha(p) for p in source_files}
source_manifest={'files_sha256':manifest,'minecraft_jar':str(JAR),'minecraft_jar_sha1':hashlib.sha1(JAR.read_bytes()).hexdigest(),
    'model':read(MODEL),'parent_model':read(WORK/'spear_in_hand.original.json'),
    'generated_export_sha256':sha(WORK/'weapon_existing_generated.json')}
dispatch_path=REPO/'resourcepack/assets/minecraft/items/netherite_spear.json'
dispatch=read(dispatch_path)
source_manifest['netherite_spear_dispatch']={'path':str(dispatch_path),'sha256':sha(dispatch_path),
    'lucifer_entries':[e for e in dispatch.get('model',{}).get('entries',[]) if e.get('threshold')==1110014]}
png_bytes=PNG.read_bytes()
input_data={'project_name':'lucifer_existing_spear_source_preview','armature_name':body_import['armature_name'],
    'texture_path':str(PNG),'resolution':[32,32],'bones':body_import['bones'],
    'parts':[{'name':'lucifer_existing_spear','vertices':vertices,'faces':faces,'weights':weights}],
    'source_manifest':source_manifest,
    'texture':{'path':str(PNG),'sha256':sha(PNG),'width':32,'height':32,'png_data_url':'data:image/png;base64,'+base64.b64encode(png_bytes).decode(),
               'already_mirrored_by_add_lucifer':True,'apply_additional_mirror':False},
    'coordinate_contract':{'axes':'Java rig: +y up, front -z; generated item pixels are Minecraft model coordinates',
        'matrix_convention':'row-major 4x4; column vectors; no additional transform after importing parts[].vertices',
        'weights':'Each wedge has weight 1 on original J_R_Weapon source skin joint id 16. Map by bone id/name into the existing rig.',
        'import_rule':'Append only parts[0] and the existing texture to the original body rig. bones[] is correspondence context, do not create duplicate bones.',
        'weapon_geometry':'Direct client ItemModelGenerator.processFrames + FaceInfo/BlockElementFace UV corners; no authored replacement model.',
        'attachment_scope':'Dungeons socket placement is source evidence; mapping the existing Java weapon holder basis to it is an explicit cross-game adapter.'},
    'binding':{'bone_name':'J_R_Weapon','bone_id':bone['id'],'parent_bone':'J_R_Hand',
        'source_gltf_node_index':node_index['J_R_Weapon'],'source_socket_record':socket_record,'source_mesh_skeleton_references':skeletal_refs,
        'socket_relative_transform_note':'Socket serializes only SocketName and BoneName; no nondefault relative translation/rotation/scale override. Identity socket-to-bone uses standard engine defaults.',
        'source_normalized_bind_world':{k:v.tolist() for k,v in source_java.items()},
        'native_bind_world':socket_world.tolist(),'socket_local_matrix_from_generated_pixels':socket_local.tolist(),
        'world_matrix_from_generated_pixels':socket_anchored_world.tolist(),
        'legacy_arm_pivot_world_matrix':legacy_world.tolist(),'legacy_arm_pivot_socket_local_matrix':legacy_socket_local.tolist(),
        'legacy_vanilla_hand_origin_relative_arm':holder_origin.tolist(),
        'translation_change_from_legacy_arm_pivot':(socket_anchored_world[:3,3]-legacy_world[:3,3]).tolist(),
        'adapter_choice':'Use actual J_R_Weapon origin instead of the old fixed vanilla arm-to-grip translation; keep the existing Java held basis and original item thirdperson transform.',
        'item_transform_unit_model':item_unit.tolist(),'item_transform_from_model_pixels':item_pixels.tolist(),'HOLD':HOLD.tolist(),'VANILLA':VANILLA.tolist()},
    'source_generated_vertices':raw_vertices,'source_generated_uv_pixels':raw_uvs,'face_provenance':face_provenance}
(WORK/'weapon_native_input.json').write_text(json.dumps(input_data,ensure_ascii=False,indent=2),encoding='utf-8')

rgba=np.array(Image.open(PNG).convert('RGBA'));gui=np.array(Image.open(PNG.with_name('lucifer.png')).convert('RGBA'))
mask=rgba[:,:,3]!=0
edges=sum(int(mask[y,x]) * sum(1 for dx,dy in [(0,-1),(0,1),(-1,0),(1,0)] if not (0<=x+dx<32 and 0<=y+dy<32 and mask[y+dy,x+dx])) for y in range(32) for x in range(32))
inv=np.linalg.inv(socket_anchored_world)
position_error=max(float(np.max(np.abs((inv@np.array(p+[1.0]))[:3]-raw_vertices[k]))) for k,p in vertices.items())
alignment_error=float(np.max(np.abs(socket_world @ socket_local-socket_anchored_world)))
saved=read(WORK/'weapon_native_input.json')
uv_error=0.0
for prov in saved['face_provenance']:
    face=saved['parts'][0]['faces'][prov['native_face_index']]
    src_face=generated['elements'][prov['source_element']]['faces'][prov['source_face']]
    for key,corner in zip(face['vertices'],src_face['corners']):
        uv_error=max(uv_error,float(np.max(np.abs(np.array(face['uv'][key])-np.array(corner['uv_normalized'])*32))))
v=np.array(list(vertices.values()))
validation={'generated_elements':len(generated['elements']),'generated_front_back_faces':2,'generated_side_faces':len(faces)-2,
    'independent_alpha_boundary_edges':edges,'side_faces_equal_alpha_boundary_edges':len(faces)-2==edges,
    'quad_faces':len(faces),'wedges':len(vertices),'triangles_if_split_each_quad':2*len(faces),
    'texture_alpha_values':sorted(np.unique(rgba[:,:,3]).tolist()),'opaque_texels':int(mask.sum()),
    'in_hand_rgba_equals_horizontal_mirror_of_gui':bool(np.array_equal(rgba,gui[:,::-1])),
    'additional_texture_mirror':False,'source_uv_max_abs_error':uv_error,
    'inverse_adapter_position_max_abs_error':position_error,'socket_local_world_composition_max_abs_error':alignment_error,
    'native_vs_source_normalized_socket_bind_matrix_max_abs_error':float(np.max(np.abs(socket_world-source_java['J_R_Weapon']))),
    'binding_bone_id':bone['id'],'binding_bone_name':bone['name'],
    'all_weights_one':all(ws==[[bone['id'],1.0]] for ws in saved['parts'][0]['weights'].values()),
    'model_space_bounds':[v.min(axis=0).tolist(),v.max(axis=0).tolist()],
    'input_sha256':sha(WORK/'weapon_native_input.json'),
    'limits':['No Blockbench import or runtime animation was performed in this task.','No Java game final render/atlas filtering or pose acceptability claim.','Bone bind TRS is normalized exported glTF/native Euler data, not raw UE full precision.','Cross-game grip orientation is an explicit adapter, not an original Mossy-with-Lucifer-spear asset.']}
(WORK/'weapon_native_validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(validation,ensure_ascii=False,indent=2))
