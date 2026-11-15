"""Read-only native assembly audit against independently saved component sources."""
import base64
import hashlib
import io
import json
from pathlib import Path
import numpy as np
from PIL import Image

WORK=Path(__file__).parent
REF=Path(r'D:\agent\claude\github-create\tralancer-rpg-1.21.11\_tools\lucifer_ref')
DEST=REF/'separate'
MODEL=DEST/'lucifer_verdant.bbmodel'
BODY=DEST/'mossy_skeleton_body_original.bbmodel'
ARMOR=DEST/'verdant_robe_original.bbmodel'
WEAPON=WORK/'weapon_native_input.json'

def digest(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def core(b):return {k:b.get(k) for k in ['resolution','elements','groups','outliner','textures','dungeons_material_source']}
def meshes(b):return {e['name']:e for e in b['elements'] if e['type']=='mesh'}
def bones(b):return {e['name']:e for e in b['elements'] if e['type']=='armature_bone'}
def arm(b):return next(e for e in b['elements'] if e['type']=='armature')
def parents(b):
    byid={e['uuid']:e for e in b['elements']};p={}
    def walk(n,parent=None):
        uid=n if isinstance(n,str) else n['uuid'];p[uid]=parent
        if isinstance(n,dict):
            for c in n.get('children',[]):walk(c,uid)
    for n in b['outliner']:walk(n)
    return {uid:byid.get(parent,{}).get('name') for uid,parent in p.items()}
def weights(b,m,k):
    token=m['uuid'][:6]+':'+k
    return {name:bone['vertex_weights'][token] for name,bone in bones(b).items() if isinstance(bone.get('vertex_weights'),dict) and bone['vertex_weights'].get(token,0)!=0}
def texture_bytes(t):return base64.b64decode(t['source'].split(',',1)[1])
def maximum(a,b):return float(np.max(np.abs(np.asarray(a,float)-np.asarray(b,float))))
def mapped_bone(n):return 'J_L_Spine' if n=='J_Spine' else n

def compare_mesh(name,actual,expected_vertices,expected_faces,expected_weights,texture_index,parent_name,par):
    keys=set(expected_vertices);actual_keys=set(actual['vertices']);positions=[]
    for k in sorted(keys&actual_keys):
        error=maximum(actual['vertices'][k],expected_vertices[k])
        if error:positions.append({'vertex':k,'error':error,'source':expected_vertices[k],'saved':actual['vertices'][k]})
    fs=list(actual['faces'].items());face_rows=[];topology=[];uv=[];textures=[]
    for i,(expected,(fid,f)) in enumerate(zip(expected_faces,fs)):
        if f['vertices']!=expected['vertices']:topology.append({'face':i,'expected':expected['vertices'],'actual':f['vertices']})
        if set(f['uv'])!=set(expected['uv']):uv.append({'face':i,'uv_vertex_keys_differ':True})
        for k in set(f['uv'])&set(expected['uv']):
            d=maximum(f['uv'][k],expected['uv'][k])
            if d:uv.append({'face':i,'vertex':k,'error':d,'source':expected['uv'][k],'saved':f['uv'][k]})
        if f.get('texture')!=texture_index:textures.append({'face':i,'expected':texture_index,'saved':f.get('texture')})
        face_rows.append({'source_face_index':i,'saved_face_uuid':fid,'source_vertices':expected['vertices'],
            'saved_vertices':f['vertices'],'source_uv':expected['uv'],'saved_uv':f['uv'],'saved_texture_index':f.get('texture')})
    weightdiff=[]
    for k in sorted(keys&actual_keys):
        got=weights(CURRENT,actual,k);expected=expected_weights[k]
        if got!=expected:weightdiff.append({'vertex':k,'source_remapped':expected,'saved':got})
    transforms={k:actual.get(k,default) for k,default in [('origin',[0,0,0]),('rotation',[0,0,0]),('scale',[1,1,1])]}
    neutral=transforms=={'origin':[0,0,0],'rotation':[0,0,0],'scale':[1,1,1]}
    result={'name':name,'vertices':len(actual_keys),'faces':len(fs),'triangles_if_convex_faces_split':sum(len(f['vertices'])-2 for fid,f in fs),
        'source_vertex_keys_exact':keys==actual_keys,'source_faces_count':len(expected_faces),'face_count_equal':len(expected_faces)==len(fs),
        'position_max_abs_difference_java_pixels':max([r['error'] for r in positions],default=0),'position_differences':positions,
        'topology_order_differences':topology,'uv_differences':uv,'texture_index_differences':textures,'weight_differences':weightdiff,
        'neutral_mesh_transform':neutral,'mesh_transform':transforms,'parent':par.get(actual['uuid']),'expected_parent':parent_name,
        'parent_matches':par.get(actual['uuid'])==parent_name,'source_to_native_face_mapping':face_rows}
    result['pass']=all([keys==actual_keys,len(expected_faces)==len(fs),not positions,not topology,not uv,not textures,not weightdiff,neutral,result['parent_matches']])
    return result

def main():
    global CURRENT
    sourcebytes={str(p):p.read_bytes() for p in [MODEL,BODY,ARMOR,WEAPON]}
    CURRENT=json.loads(sourcebytes[str(MODEL)]);body=json.loads(sourcebytes[str(BODY)]);armor=json.loads(sourcebytes[str(ARMOR)]);weapon=json.loads(sourcebytes[str(WEAPON)])
    actual_mesh=meshes(CURRENT);actual_bones=bones(CURRENT);ap=parents(CURRENT);bp=parents(body);ar=arm(CURRENT);rows=[]
    expected_names=set()
    for source,prefix,ti in [(body,'body__',0),(armor,'armor__',1)]:
        for name,sm in meshes(source).items():
            target=prefix+name;expected_names.add(target)
            ew={k:{(mapped_bone(n) if prefix=='armor__' else n):v for n,v in weights(source,sm,k).items()} for k in sm['vertices']}
            rows.append(compare_mesh(target,actual_mesh[target],sm['vertices'],list(sm['faces'].values()),ew,ti,ar['name'],ap))
    wm=weapon['parts'][0];wn={b['id']:b['name'] for b in weapon['bones']};target='weapon__LuciferSerpentSpear';expected_names.add(target)
    alignment=load(WORK/'weapon_grip_alignment.json');translation=np.array(alignment['translation_global_bind'],float)
    assert digest(sourcebytes[str(WEAPON)])==alignment['immutable_adapter_sha256']
    shifted_vertices={k:(np.array(v,float)+translation).tolist() for k,v in wm['vertices'].items()}
    ew={k:{wn[i]:v for i,v in w} for k,w in wm['weights'].items()}
    rows.append(compare_mesh(target,actual_mesh[target],shifted_vertices,wm['faces'],ew,3,ar['name'],ap))
    vk=list(wm['vertices']);original_v=np.array([wm['vertices'][k] for k in vk]);saved_v=np.array([actual_mesh[target]['vertices'][k] for k in vk])
    original_dist=np.linalg.norm(original_v[:,None,:]-original_v[None,:,:],axis=2)
    saved_dist=np.linalg.norm(saved_v[:,None,:]-saved_v[None,:,:],axis=2)
    weapon_translation_check={'authorized_delta_java_pixels':translation.tolist(),'source_input_sha256':alignment['immutable_adapter_sha256'],
        'absolute_difference_vs_unshifted_source_max':maximum(saved_v,original_v),
        'max_difference_after_authorized_translation':maximum(saved_v,original_v+translation),
        'all_pairs_distance_max_numeric_difference':maximum(original_dist,saved_dist),
        'all_pairs_checked':int(len(vk)*(len(vk)-1)//2),
        'world_linear_matrix_difference':maximum(np.array(alignment['world_matrix_before'])[:3,:3],np.array(alignment['world_matrix_after'])[:3,:3]),
        'mathematical_invariance':'A common translation preserves shape, scale, orientation and pairwise distances; floating-point distance recomputation residuals are reported separately.',
        'provenance':str(WORK/'weapon_grip_alignment.json'),'provenance_sha256':digest((WORK/'weapon_grip_alignment.json').read_bytes())}
    bone_rows=[]
    for name,old in bones(body).items():
        new=actual_bones[name];expected_parent=ar['name'] if bp[old['uuid']]==arm(body)['name'] else bp[old['uuid']]
        o=maximum(old['origin'],new['origin']);r=maximum(old['rotation'],new['rotation'])
        bone_rows.append({'name':name,'local_origin_difference':o,'local_euler_difference':r,'parent':ap[new['uuid']],
            'expected_parent':expected_parent,'pass':o==0 and r==0 and ap[new['uuid']]==expected_parent})
    valid_weight_tokens={m['uuid'][:6]+':'+k for m in actual_mesh.values() for k in m['vertices']}
    unexpected_weights=[{'bone':n,'key':k,'value':v} for n,b in actual_bones.items() if isinstance(b.get('vertex_weights'),dict) for k,v in b['vertex_weights'].items() if k not in valid_weight_tokens]
    texture_sources=[texture_bytes(body['textures'][0]),texture_bytes(armor['textures'][0]),texture_bytes(armor['textures'][1]),Path(weapon['texture_path']).read_bytes()]
    texture_sizes=[(64,32),(64,64),(64,64),(32,32)];texture_rows=[]
    for i,(t,src,size) in enumerate(zip(CURRENT['textures'],texture_sources,texture_sizes)):
        raw=texture_bytes(t);srgba=np.asarray(Image.open(io.BytesIO(src)).convert('RGBA'));rgba=np.asarray(Image.open(io.BytesIO(raw)).convert('RGBA'))
        texture_rows.append({'index':i,'name':t['name'],'uuid':t['uuid'],'source_sha256':digest(src),'saved_sha256':digest(raw),
            'bytes_equal':src==raw,'rgba_differing_pixels':int(np.any(srgba!=rgba,axis=2).sum()),
            'expected_resolution':size,'saved_uv_resolution':[t.get('uv_width'),t.get('uv_height')],
            'resolution_matches':(t.get('uv_width'),t.get('uv_height'))==size})
    mat=CURRENT.get('dungeons_material_source',{});oldmat=armor.get('dungeons_material_source',{})
    # UUIDs must change to the assembly's own texture objects; all other material settings remain exactly source.
    material={
        'source_metadata_equal_excluding_project_texture_uuids_and_authorized_tint':{k:v for k,v in mat.items() if k not in ['albedo_uuid','auxiliary_uuid','palette_tint_linear']}=={k:v for k,v in oldmat.items() if k not in ['albedo_uuid','auxiliary_uuid','palette_tint_linear']},
        'authorized_palette_tint_linear':mat.get('palette_tint_linear'),
        'authorized_palette_tint_matches':mat.get('palette_tint_linear')==[.4,.4,.4],
        'albedo_targets_robe_texture_index1':mat.get('albedo_uuid')==CURRENT['textures'][1]['uuid'],
        'auxiliary_targets_texture_index2':mat.get('auxiliary_uuid')==CURRENT['textures'][2]['uuid'],
        'white_emissive':mat.get('parameters',{}).get('Emissive')==[1,1,1],
        'natural_emissive_original':mat.get('parameters',{}).get('NaturalEmissive')==0.699999988079071,
        'source_pixel_shader_hash':mat.get('source_pixel_shader_hash'),'formula':mat.get('formula'),
        'effective_switches':mat.get('original_effective_switches'),
        'preview_scope':mat.get('preview'),
        'execution_limit':'This file audit verifies metadata and texture association, not the running shader or full original game render.'}
    attachment_bones={mapped_bone(p['bone']) for p in load(WORK/'verdant_assembly.json')['parts']}
    screenshot=REF/'native/lucifer_verdant_darkpalette_040_idle_0.000.png'
    visual={'screenshot':str(screenshot),'sha256':digest(screenshot.read_bytes()),'view':'Actual native animation.idle time 0 preview, with user-authorized dark palette 0.40.',
        'observed':['Hat brim sits above the skeleton head; green hat, silver buckle, robe sleeves and body have the expected orientation.',
            'The spear is held upright in front of the body in the idle pose and partially occludes the face/torso.',
            'No definite silhouette-breaking body/armor penetration was identified in this one visible view.'],
        'not_verified':['The spear overlap in this single projection cannot prove or exclude actual 3D intersection.',
            'Occluded back/side surfaces, movement poses and full-range collision clearance were not shown; no all-angle no-clipping acceptance.']}
    endbytes=MODEL.read_bytes();endmodel=json.loads(endbytes)
    report={'scope':'Native integrated file audit against actual native body/armor component saves and existing-weapon source input. No Blockbench or model changes.',
        'model':str(MODEL),'model_sha256_at_start':digest(sourcebytes[str(MODEL)]),'model_sha256_at_end':digest(endbytes),
        'frozen_core_sha256':digest(canonical(core(CURRENT))),'core_unchanged_during_audit':core(CURRENT)==core(endmodel),
        'core_hash_fields':['resolution','elements','groups','outliner','textures','dungeons_material_source'],
        'animation_scope':'Animations may be added separately. This audit excludes animations and does not certify any motion.',
        'animations_in_snapshot':[{'name':a.get('name'),'length':a.get('length')} for a in CURRENT.get('animations',[])],
        'source_files':[{'path':str(p),'sha256':digest(sourcebytes[str(p)])} for p in [BODY,ARMOR,WEAPON]],
        'counts':{'meshes':len(actual_mesh),'bones':len(actual_bones),'armatures':sum(e['type']=='armature' for e in CURRENT['elements']),
            'vertices':sum(len(m['vertices']) for m in actual_mesh.values()),'faces':sum(len(m['faces']) for m in actual_mesh.values()),
            'triangle_faces':sum(len(f['vertices'])==3 for m in actual_mesh.values() for f in m['faces'].values()),
            'quad_faces':sum(len(f['vertices'])==4 for m in actual_mesh.values() for f in m['faces'].values()),
            'triangles_if_quads_split':sum(len(f['vertices'])-2 for m in actual_mesh.values() for f in m['faces'].values()),'textures':len(CURRENT['textures'])},
        'part_checks':rows,'bone_checks':bone_rows,'texture_checks':texture_rows,'material_checks':material,
        'mesh_name_set_exact':set(actual_mesh)==expected_names,'bone_name_set_exact_to_body':set(actual_bones)==set(bones(body)),
        'no_extra_weight_references':not unexpected_weights,'unexpected_weights':unexpected_weights,
        'armor_attachment_bones':sorted(attachment_bones),'armor_remapping':{'J_Spine':'J_L_Spine','all_other_bones':'unchanged by name'},
        'weapon_attachment':{'bone':'J_R_Weapon','all_vertices_rigid_weight_one':all(w=={'J_R_Weapon':1.0} for w in ew.values()),
            'scope':'Original existing Java weapon geometry and texture; cross-game hand/socket basis is an explicit adapter, not original Dungeons armor geometry.'},
        'authorized_weapon_rigid_translation':weapon_translation_check,
        'visual_review':visual,
        'limits':['Component native source models already carry their own original-asset verification; this check verifies faithful assembly of those sources.',
            'Original player versus Mossy attachment-world comparison is recorded separately; this report does not assert full animation retargeting acceptance.',
            'File-only metadata audit does not execute the material plugin, validate game rendering, or measure motion clipping.']}
    report['assembly_data_checks_pass']=all([all(r['pass'] for r in rows),all(r['pass'] for r in bone_rows),len(actual_bones)==22,
        report['counts']['armatures']==1,len(CURRENT['textures'])==4,all(t['bytes_equal'] and t['resolution_matches'] for t in texture_rows),
        report['mesh_name_set_exact'],report['bone_name_set_exact_to_body'],not unexpected_weights,report['core_unchanged_during_audit'],
        weapon_translation_check['max_difference_after_authorized_translation']==0,weapon_translation_check['all_pairs_distance_max_numeric_difference']<1e-12,
        all(material[k] for k in ['source_metadata_equal_excluding_project_texture_uuids_and_authorized_tint','authorized_palette_tint_matches','albedo_targets_robe_texture_index1','auxiliary_targets_texture_index2','white_emissive','natural_emissive_original'])])
    (DEST/'verdant_assembly_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    c=report['counts'];lines=['# Lucifer Verdant 整合工程独立回读核验','',
        f'文件：`{MODEL.name}`',f'快照 SHA-256：`{report["model_sha256_at_start"]}`',f'网格/骨/纹理/材质配置范围指纹：`{report["frozen_core_sha256"]}`','',
        f'装配数据检查通过：**{report["assembly_data_checks_pass"]}**。直接回读已保存的本体、原 Verdant 盔甲与武器输入，对比实际整合 bbmodel；未操作 Blockbench、未改模型。',
        f'实际含 {c["meshes"]} Mesh、{c["vertices"]} 顶点、{c["triangle_faces"]} 三角面、{c["quad_faces"]} 四边面（拆分后 {c["triangles_if_quads_split"]} 三角）、{c["bones"]} 本体骨、{c["textures"]} 纹理。','',
        '| 部件 | 顶点/面 | 坐标差（Java像素） | UV差项 | 顺序差项 | 权重差项 |','|---|---:|---:|---:|---:|---:|']
    for r in rows:lines.append(f'| {r["name"]} | {r["vertices"]}/{r["faces"]} | {r["position_max_abs_difference_java_pixels"]:.16g} | {len(r["uv_differences"])} | {len(r["topology_order_differences"])} | {len(r["weight_differences"])} |')
    lines+=['','本体与盔甲原 world 顶点没有二次缩放或移动。武器全部顶点采用经授权的同一刚体平移，表中坐标差针对平移后的明确期望值，不冒称相对未移动源坐标差为 0。各 Mesh 变换为中性，均直属保留的本体 Armature；骨架只保留本体 22 骨，局部原点、Euler 和父级与本体源一致。盔甲仅将 `J_Spine` 权重改绑到 `J_L_Spine`，其余按同名骨；武器刚性绑定 `J_R_Weapon`。JSON 给出全部源面到整合 native 面的映射。',
        f'武器授权平移 Δ=`{translation.tolist()}` Java 像素；相对原未平移顶点的最大绝对差 `{weapon_translation_check["absolute_difference_vs_unshifted_source_max"]:.16g}`，施加同一 Δ 后差 `{weapon_translation_check["max_difference_after_authorized_translation"]:.16g}`。检查全部 {weapon_translation_check["all_pairs_checked"]} 对顶点，距离重算最大浮点残差 `{weapon_translation_check["all_pairs_distance_max_numeric_difference"]:.16g}`；线性矩阵未变，形状、尺度和朝向保持。','',
        '## 纹理与材质','',
        '四纹理顺序是 body=0、robe=1、aux=2、weapon=3。每个面的纹理编号和各纹理独立 UV 分辨率均已检查；四张 PNG 内嵌字节与对应源完全相等，没有重新采样或叠加发光颜色。',
        '材质 metadata 除项目纹理 UUID 和用户授权的 palette_tint_linear=[0.40,0.40,0.40] 外与独立 Verdant 工程相等；Albedo UUID 指向 1，辅助 S UUID 指向 2。表面与 NaturalEmissive 项共用深色 Albedo；辅助 S.B 控制的主发光不乘 tint，Emissive 仍是原白色 [1,1,1]。NaturalEmissive=0.699999988079071 和有效 SpecularTexture=True 保留。这是用户授权的视觉风格变更，不再声称整合版法袍配色与原作完全相同。此文件检查不替代真实 shader 执行和完整 Unreal 高光、粗糙度、曝光、Bloom/场景光照核验。','',
        '## 截图检查与范围','',
        '检查了 `native/lucifer_verdant_darkpalette_040_idle_0.000.png`：帽檐位于头顶，暗绿帽、银扣、袖袍与本体方向一致。在该可见视角未发现可明确判定的轮廓穿出问题。idle 中武器竖持在身前并部分遮挡头/身体；单张投影不能将遮挡直接判为三维穿模，也不能据此判定无穿模。',
        '未显示的背面/侧面、动作姿态及全程碰撞间隙均未验收；需主任务其他视角及动画预览继续核查。','',
        f'本次快照中的动画数为 {len(CURRENT.get("animations",[]))}。本报告只验证稳定的网格、骨、纹理和材质配置，不验证动画；后续仅添加动画会改变整文件哈希，但不改变上述范围指纹。核验过程中该范围保持不变：{report["core_unchanged_during_audit"]}。','']
    (DEST/'verdant_assembly_validation.md').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps({'pass':report['assembly_data_checks_pass'],'counts':c,'model_sha256':report['model_sha256_at_start'],
        'frozen_core_sha256':report['frozen_core_sha256'],'material_checks':material,'source_files':report['source_files']},ensure_ascii=False))

if __name__=='__main__':main()
