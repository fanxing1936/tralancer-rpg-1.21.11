"""M3 保存工程的兼容性审计；只读公共管线，在内存中烘焙，不构建/同步游戏。"""
from __future__ import annotations
import argparse
import base64
import copy
import hashlib
import io
import json
import math
import re
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from PIL import Image
import display_mob as dm
from heart_of_ender_audio import validate as audio_validate, CUES, ENTER_CUES
from heart_of_ender_blockbench import REF

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def shell_face(element, face):
    name=element['name']
    return (name.startswith('limb_') or name.startswith('shell_body_') or
            name=='shell_skull' and face!='down' or
            name=='shell_lower_jaw' and face!='up')

def material_v3_checks(doc, base, embedded, check):
    old=Image.open(io.BytesIO(base64.b64decode(base['textures'][0]['source'].split(',',1)[1]))).convert('RGBA')
    before=np.array(old)
    after=np.array(embedded)
    check(embedded.size==old.size==(1024,1024),'v3与已接受v2保持1024图集尺寸')
    if after.shape!=before.shape:
        return {'dimensions_match':False}
    check(np.array_equal(after[:,:,3],before[:,:,3]),'全图alpha逐byte等于已接受v2')
    allowed=np.zeros(before.shape[:2],bool)
    regions=[(r['atlas_rect'],0) for r in read(REF/'m3_material/atlas_regions.json')['regions']
             if r['name'].startswith('stars_')]
    original_window_count=len(regions)
    regions += [(r['atlas_rect'],1) for r in read(REF/'m3_material_v2/atlas_regions.json')['regions']
                if r['kind']=='independent_uv_alpha_profile']
    for (x0,y0,x1,y1),pad in regions:
        allowed[max(0,y0-pad):min(before.shape[0],y1+pad),
                max(0,x0-pad):min(before.shape[1],x1+pad)]=True
    check(original_window_count==6 and len(regions)==60,'仅6星窗及54渐隐副本为可改区域',
          {'original_window_padding':0,'fade_copy_padding':1})
    shell=np.zeros_like(allowed)
    protected=np.zeros_like(allowed)
    shell_count=protected_count=0
    for element in base['elements']:
        for face,data in element['faces'].items():
            if data.get('texture') is None:continue
            u0,v0,u1,v1=data['uv']
            x0,y0=math.floor(min(u0,u1)),math.floor(min(v0,v1))
            x1,y1=math.ceil(max(u0,u1)),math.ceil(max(v0,v1))
            if shell_face(element,face):
                shell[y0:y1,x0:x1]=True
                shell_count+=1
            else:
                protected[y0:y1,x0:x1]=True
                protected_count+=1
    delta=np.any(after[:,:,:3]!=before[:,:,:3],axis=2)
    bright=before[:,:,:3].max(axis=2)>=24
    check(not np.any(allowed&protected),'可改区域不与眼牙嘴腔小人采样UV重叠')
    check(not np.any(shell&~allowed),'全部196外壳face采样区域被注册覆盖',shell_count)
    check(np.array_equal(after[protected,:3],before[protected,:3]),'全部非外壳face采样RGB逐byte不变',protected_count)
    check(not np.any(delta&~allowed),'60注册区域之外的RGB逐byte不变')
    check(np.array_equal(after[bright,:3],before[bright,:3]),'原maxRGB>=24星点RGB逐byte不变')
    return {'dimensions_match':True,'shell_faces':shell_count,'protected_faces':protected_count,
            'allowed_region_count':len(regions),'allowed_pixels':int(allowed.sum()),
            'changed_rgb_pixels':int(delta.sum()),'changed_outside_allowed':int((delta&~allowed).sum()),
            'changed_protected_pixels':int((delta&protected).sum()),
            'alpha_changed_pixels':int(np.count_nonzero(after[:,:,3]!=before[:,:,3]))}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model',type=Path,default=REF/'heart_of_ender.bbmodel')
    args=parser.parse_args()
    target=args.model.resolve()
    doc=read(target)
    version=doc.get('unhandled_root_fields',{}).get('material_status',{}).get('version')
    material_v2=version=='M3 material v2'
    material_v3=version=='M3 material v3'
    output_dir=REF/('m3_material_v3' if material_v3 else 'm3_material_v2' if material_v2 else 'm3_motion')
    base_path=REF/('m3_material_v2/heart_of_ender_material_v2.bbmodel' if material_v3 else
                  'm3_material_v2/baseline.bbmodel' if material_v2 else 'm3_motion/accepted_R2.bbmodel')
    base=read(base_path)
    spec=read(REF/"m2_geometry/geometry_spec.json")
    checks=[]
    def check(ok, name, detail=None):
        checks.append({"name":name,"passed":bool(ok),"detail":detail})
    if material_v3:
        check(hashlib.sha256(base_path.read_bytes()).hexdigest()=='88d22edc9b13f96a0ca56a57c605894d94b64c101279bd1e69c237affdcb0f39',
              'v3基线为用户已接受88d22模型')
        check(doc['elements']==base['elements'],'49元素及全部UV逐值等于已接受v2')
        check(len(doc['elements'])==49,'v3仍为49元素')
        check(doc['animations']==base['animations'],'七段动作逐值等于已接受v2')
        check(doc['resolution']==base['resolution']=={'width':1024,'height':1024},'v3模型UV分辨率保持1024')
        check(doc['outliner']==base['outliner'],'v3完整outliner逐值等于已接受v2')
    elif material_v2:
        changes=read(REF/'m3_material_v2/material_changes.json')
        expected=copy.deepcopy(base['elements'])
        by_name={e['name']:e for e in expected}
        for change in changes['uv_changes']:
            by_name[change['element']]['faces'][change['face']]['uv']=change['new_uv']
        actual={e['uuid']:e for e in doc['elements']}
        check(all(actual[e['uuid']]==e for e in expected),'原46元素仅包含登记的材质UV变化')
        check(set(actual)-{e['uuid'] for e in expected}==set(changes['added_overlay_uuids']),'仅新增3张登记的光晕面')
        check(doc['animations']==base['animations'],'七段动作逐值不变')
    else:
        check(doc["elements"]==base["elements"],"已验收几何/UV/元素未改变")
    check(doc["groups"]==base["groups"],"已接受v2骨骼逐值不变" if material_v3 else "R2骨骼rest/连接未改变")
    def hierarchy(nodes):
        return [(n if isinstance(n,str) else [n['uuid'],hierarchy(n['children'])]) for n in nodes]
    filtered=copy.deepcopy(doc['outliner'])
    if material_v2:
        def strip(nodes):
            nodes[:]=[n for n in nodes if not isinstance(n,str) or n not in changes['added_overlay_uuids']]
            for n in nodes:
                if isinstance(n,dict):strip(n['children'])
        strip(filtered)
    check(hierarchy(filtered)==hierarchy(base["outliner"]),"原R2父子连接未改变")
    check(len(doc["textures"])==1,"单张内嵌图集")
    embedded=Image.open(io.BytesIO(base64.b64decode(doc["textures"][0]["source"].split(',')[1]))).convert('RGBA')
    atlas=Image.open((output_dir/'atlas.png') if material_v2 or material_v3 else (REF/'m3_material/atlas.png')).convert('RGBA')
    size=(1024,1024) if material_v2 or material_v3 else (512,512)
    check(embedded.size==size and embedded.tobytes()==atlas.tobytes(),"内嵌M3图集与磁盘RGBA一致")
    material_pixel_checks=material_v3_checks(doc,base,embedded,check) if material_v3 else None
    if material_v2:
        old=Image.open(REF/'m3_material/atlas.png').convert('RGBA')
        check(embedded.crop((0,0,512,512)).tobytes()==old.tobytes(),'原512图集RGBA全部保留')
    mask=Image.open(REF/"MCD_Heart_of_Ender_(glow_effect_texture).png").convert('RGBA')
    check(embedded.crop((432,88,476,132)).tobytes()==mask.tobytes(),"44遮罩RGBA原样保留")
    names=[a["name"] for a in doc["animations"]]
    check(names==["animation."+x for x in ("idle","walk","mortar","cross_beam","sink","rise","death")],"七段动作且idle/walk在前")
    group_names={g['uuid']:g['name'] for g in doc['groups']}
    total=0
    for a in doc['animations']:
        valid=True
        for uuid, anim in a['animators'].items():
            valid=valid and uuid in group_names
            keys=set()
            for k in anim['keyframes']:
                total+=1
                vals=list(k['data_points'][0][axis] for axis in 'xyz')
                valid=valid and k['channel'] in ('position','rotation') and k['interpolation'] in ('linear','catmullrom','step')
                # Blockbench 原生保存时可将数值序列化成数字字符串；禁止表达式/Molang。
                valid=valid and all((isinstance(v,(int,float)) or isinstance(v,str) and re.fullmatch(r'[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?',v)) and math.isfinite(float(v)) for v in vals)
                valid=valid and 0<=k['time']<=a['length']+1e-6 and (k['channel'],k['time']) not in keys
                keys.add((k['channel'],k['time']))
        check(valid,a['name']+' 纯数字合法关键帧')
    mob=dm.Mob(key='heart_of_ender',label='末影之心',generator=__file__,bbmodel=target,
        parts=[(p['name'],p['bones']) for p in spec['parts']],glow=list(group_names.values()),seat=0,model_scale=1,
        tag='rpg.he',score='rpg_he',clips=[(a['name'].split('.')[-1],1,a['loop']=='loop') for a in doc['animations']])
    check(len(mob.parts)==21,'21个展示部件，静态验收数量不增加')
    bones,png,res=dm.load_bbmodel(mob)
    offsets={}
    for part,members in mob.parts:
        model,K=dm.part_model(mob,bones,part,members,res)
        offsets[part]=K
        check(all(-16<=v<=32 for el in model['elements'] for v in el['from']+el['to']),part+' 居中坐标合法')
        check(all(el.get('light_emission')==15 and el.get('shade') is False for el in model['elements']),part+' 自发光标记')
    clips=dm.load_animations(mob)
    ground=read(REF/'m3_motion/shell_motion.json')['ground_y']
    def y_range(clip,time,names):
        values=[]
        for name in names:
            W=dm.posed_matrix(bones,name,clips[clip],time)
            for cube in bones[name]['cubes']:
                for corner in range(8):
                    p=[cube['to'][k] if corner>>k&1 else cube['from'][k] for k in range(3)]
                    values.append(sum(W[1][k]*p[k] for k in range(3))+W[1][3])
        return [min(values),max(values)]
    inner_bones=[n for n in bones if n.startswith('inner_')]
    spatial={
        'ground_y':ground,'sink_1_7s_y_range':y_range('sink',1.7,bones),
        'rise_0s_y_range':y_range('rise',0,bones),
        'death_inner_3_2s_y_range':y_range('death',3.2,inner_bones),
        'death_inner_3_8s_y_range':y_range('death',3.8,inner_bones)}
    check(spatial['sink_1_7s_y_range'][1]<ground,'sink全模型实际低于地面')
    check(spatial['rise_0s_y_range'][1]<ground,'rise从地面以下开始')
    check(spatial['death_inner_3_2s_y_range'][1]>ground and spatial['death_inner_3_8s_y_range'][1]<ground,'death末段小人经position沉地消失')
    lowest=min((y_range('walk',i*.05,[n])[0]-ground,i*.05,n) for i in range(161) for n in bones if n.startswith('limb_') and n.endswith('_distal'))
    spatial['walk_min_distal_ground_gap_at_20Hz']={'gap':lowest[0],'time':lowest[1],'bone':lowest[2]}
    check(lowest[0]>-.05,'walk远段20Hz地面穿入小于0.05归一化单位',lowest)
    loop_seams=[]
    for name,clip in clips.items():
        if clip['loop']:
            error=max(abs(dm.posed_matrix(bones,b,clip,0)[i][j]-dm.posed_matrix(bones,b,clip,clip['length'])[i][j]) for b in bones for i in range(4) for j in range(4))
            loop_seams.append({'clip':name,'matrix_error':error})
            check(error<0.0001,name+' 循环姿态闭合',error)
    baked=dm.bake(mob,bones,offsets,clips)
    baked_info={}
    for name,clip in baked.items():
        flat=[v for _,f in clip['frames'] for values in f.values() for array in values for v in array]
        check(all(math.isfinite(x) for x in flat),name+' 20Hz内存烘焙数值有效')
        baked_info[name]={'ticks':clip['ticks'],'frames':len(clip['frames']),'parts':len(mob.parts)}
        cue_ok=all(0<=t and (t<clips[name]['length'] if clip['loop'] else t<=clips[name]['length']) and abs(t/.05-round(t/.05))<1e-5 for t,_,_,_ in CUES.get(name,[]))
        check(cue_ok,name+' 声音时点在片段范围并对齐20Hz')
    check(audio_validate()['files']==47,'47个HE音效文件可读取')
    model_sha=hashlib.sha256(target.read_bytes()).hexdigest()
    runtime_status='M3 structural audit only; M5 RPG pack integration/build/server test not performed'
    runtime_evidence={'visual_acceptance':'not assessed by this structural validator',
        'm5_integrated':False,'independent_probe_sync_receipt':None}
    if material_v2 or material_v3:
        receipt_path=output_dir/'sync_receipt.json'
        if receipt_path.exists():
            receipt=read(receipt_path)
            matches=receipt.get('model_sha256')==model_sha and receipt.get('user_authorized') is True
            runtime_evidence['independent_probe_sync_receipt']={
                'path':str(receipt_path.relative_to(REF)).replace('\\','/'),
                'sha256':hashlib.sha256(receipt_path.read_bytes()).hexdigest(),
                'model_sha256':receipt.get('model_sha256'),'matches_current_model':matches,
                'files':len(receipt.get('files',[])),'scope':receipt.get('scope')}
            if matches:
                runtime_status=('Independent he_material_probe synchronized under user authorization '
                    '(receipt matches this model); M5 RPG pack integration/build/server test not performed. '
                    'Client launch/resource-pack enablement and visual acceptance are separate from this structural audit.')
    report={'bbmodel_sha256':model_sha,
        'checks':checks,'passed':sum(x['passed'] for x in checks),'errors':[x for x in checks if not x['passed']],
        'keyframes':total,'parts':len(mob.parts),'baked_in_memory':baked_info,'loop_seams':loop_seams,
        'spatial_checks':spatial,
        'game_scale':'not decided; normalized model_scale=1, seat=0 only for mathematical checks',
        'runtime_status':runtime_status,'runtime_evidence':runtime_evidence,
        'audio_binding':{'cues':CUES,'enter_cues':ENTER_CUES,'timing_status':'author inference; source GIFs are silent'}}
    if material_v3:
        report['material_version']=version
        report['accepted_baseline']={'path':str(base_path.relative_to(REF)).replace('\\','/'),
            'sha256':hashlib.sha256(base_path.read_bytes()).hexdigest()}
        report['material_pixel_checks']=material_pixel_checks
    out=output_dir/'validation.json'
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('passed','errors','keyframes','parts','baked_in_memory')},ensure_ascii=False))
    if report['errors']:raise SystemExit(1)

if __name__=='__main__':main()
