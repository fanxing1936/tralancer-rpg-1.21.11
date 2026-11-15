"""Use the current HE head's exact geometry/UV/atlas in the AV animation rig.

The pre-edit AV model remains the timing/rotation source. New head/jaw geometry
is translated, never stretched. One common rear hinge replaces the old separated
hinges. Vertical placement is retargeted to the former visible body boundary.
"""
from __future__ import annotations
import base64,copy,hashlib,json,sys,uuid
from pathlib import Path
import numpy as np
from PIL import Image
import io
import display_mob as dm

HERE=Path(__file__).resolve().parent
HE=HERE/'heart_of_ender_ref'
AV=HERE/'arch_visage_ref'
OUT=AV/'head_match_v1'
BASE_SHA='268d11878897ac78e6b527dfd970769c8711724614c790c3c82c9f4acf6f412f'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n','utf8')
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'tralancer:arch_visage:he_head:'+s))
def read(p):return json.loads(p.read_text('utf8'))

def main():
    OUT.mkdir(exist_ok=True)
    baseline=OUT/'previous_arch_visage.bbmodel'
    if not baseline.exists():
        current=AV/'arch_visage.bbmodel'
        if sha(current)!=BASE_SHA:raise ValueError('Unexpected pre-edit AV source; refusing to overwrite')
        baseline.write_bytes(current.read_bytes())
        (OUT/'previous_config.json').write_bytes((AV/'config.json').read_bytes())
    if sha(baseline)!=BASE_SHA:raise ValueError('Frozen AV motion source changed')
    source_path=HE/'heart_of_ender.bbmodel';source=read(source_path);old=read(baseline)
    config=read(OUT/'previous_config.json');doc=copy.deepcopy(old)
    groups={g['name']:g for g in doc['groups']}
    seam=np.array(groups['head']['origin'],dtype=float)
    delta=seam-np.array([0,26,1.61051])
    for name,g in groups.items():
        if name!='root':g['origin']=seam.tolist()
    src={e['name']:e for e in source['elements']}
    mapping={
        'shell_skull':'head','shell_lower_jaw':'jaw',
        'front_eyes_surface':'eyes','eyes_source_wrapped_purple_halo':'head',
        'front_teeth_surface':'jaw','front_teeth_purple_halo_surface':'jaw',
        'side_teeth_surface':'jaw','side_teeth_purple_halo_surface':'jaw',
        'upper_mouth_raw44':'head_light','lower_mouth_raw44':'jaw_light'}
    elements=[];records=[];owners={name:[]for name in groups}
    source_uuid={}
    for name,bone in mapping.items():
        e=copy.deepcopy(src[name]);source_uuid[e['uuid']]=uid(name)
        e.update(uuid=uid(name),origin=seam.tolist(),rotation=[0,0,0])
        for key in ('from','to'):e[key]=(np.array(e[key])+delta).tolist()
        if name in ('upper_mouth_raw44','lower_mouth_raw44'):
            # A tiny external separation lets the unchanged mask blend over
            # the detachable source cavity face without coplanar flicker.
            separation=-.004 if name.startswith('upper') else .004
            for key in ('from','to'):e[key][1]+=separation
        elements.append(e);owners[bone].append(e['uuid'])
        records.append({'element':name,'source_element_uuid':src[name]['uuid'],'target_element_uuid':e['uuid'],'bone':bone,'translation':delta.tolist(),'source_from':src[name]['from'],'source_to':src[name]['to'],'source_faces':src[name]['faces'],'mask_surface_separation':(-.004 if name.startswith('upper') else .004) if name in ('upper_mouth_raw44','lower_mouth_raw44') else 0})
    # Keep source mouth face colours/UV while retaining the AV cavity on/off bones.
    for name,face,bone in [('shell_skull','down','head_light'),('shell_lower_jaw','up','jaw_light')]:
        original=next(e for e in elements if e['name']==name)
        p=copy.deepcopy(original);p['name']=name+'_'+face+'_light';p['uuid']=uid(p['name'])
        y=original['from'][1] if face=='down' else original['to'][1]
        p['from'][1]=p['to'][1]=y+(-.002 if face=='down' else .002)
        p['faces']={f:copy.deepcopy(v) if f==face else {'uv':[0,0,0,0],'texture':None}for f,v in original['faces'].items()}
        # An opaque source-star face occludes the light after it moves inward.
        # Removing this face leaves a hole through which the hidden light shows.
        backing='up' if face=='down' else 'down'
        original['faces'][face]=copy.deepcopy(src[name]['faces'][backing])
        elements.append(p);owners[bone].append(p['uuid'])
        records.append({'element':p['name'],'source_element_uuid':src[name]['uuid'],'source_face':face,'bone':bone,'translation':delta.tolist(),'separated_without_uv_change':True,'surface_separation':-.002 if face=='down' else .002,'hidden_state_backing_source_face':backing})
    nodes={g['name']:{'uuid':g['uuid'],'children':owners[g['name']][:]}for g in doc['groups']}
    nodes['root']['children']=[nodes['head'],nodes['jaw']]
    nodes['head']['children'] += [nodes['eyes'],nodes['head_light']]
    nodes['jaw']['children'] += [nodes['jaw_light']]
    doc['elements']=elements;doc['outliner']=[nodes['root']]
    doc['textures']=copy.deepcopy(source['textures'])
    doc['textures'][0]['name']='arch_visage_atlas.png';doc['textures'][0]['path']=''
    masks=copy.deepcopy(source['unhandled_root_fields']['emissive_masks'])
    for m in masks:m['element_uuid']=source_uuid[m['element_uuid']]
    doc.setdefault('unhandled_root_fields',{}).update(
        head_match={'source_sha256':sha(source_path),'source_model':'heart_of_ender.bbmodel','previous_av_sha256':BASE_SHA,'translation':delta.tolist(),'common_hinge':seam.tolist(),'geometry_scale':1,'atlas_png_bytes':'identical to current HE','eye_halo':'static wrapped HE glow on head; white eye core retains AV on/off'},
        emissive_masks=masks)
    anim=next(a for a in doc['animations'] if a['name']=='animation.spawn_attack')
    for a in anim['animators'].values():
        if a['name']=='head':
            for k in a['keyframes']:
                if k['channel']=='position':k['data_points']=[{'x':0.,'y':0.,'z':0.}]
    draft=OUT/'draft.bbmodel';write(draft,doc)
    def load(path):
        m=dm.Mob(key='arch_visage',label='Arch-Visage',generator=Path(__file__).name,bbmodel=str(path),parts=[(p['name'],p['bones'])for p in config['parts']],clips=config['clips'],glow=config['glow'],seat=0,tag='rpg.av',score='rpg_av')
        b,_,res=dm.load_bbmodel(m);return m,b,dm.load_animations(m),res
    oldmob,oldbones,oldclips,_=load(baseline)
    mob,bones,clips,res=load(draft)
    def bounds(bs,cs,t):
        pts=[]
        for name in ('head','jaw'):
            matrix=np.array(dm.posed_matrix(bs,name,cs['spawn_attack'],t))
            cube=bs[name]['cubes'][0]
            for x in (cube['from'][0],cube['to'][0]):
                for y in (cube['from'][1],cube['to'][1]):
                    for z in (cube['from'][2],cube['to'][2]):pts.append((matrix@[x,y,z,1])[1])
        return min(pts),max(pts)
    root=next(a for a in anim['animators'].values() if a['name']=='root');adjustments=[]
    for k in root['keyframes']:
        if k['channel']!='position':continue
        t=k['time'];frame=round(t*25)
        omin,omax=bounds(oldbones,oldclips,t);nmin,nmax=bounds(bones,clips,t)
        weight=(max(0.,min(1.,(5-frame)/3)) if frame<5 else max(0.,min(1.,(frame-76)/16)))
        dy=(1-weight)*(omin-nmin)+weight*(omax-nmax)
        # Both deliberately blank end states remain safely underground.
        if frame<2 or frame>=92:dy=0.
        k['data_points'][0]['y']+=dy
        adjustments.append({'frame':frame,'time':t,'old_bounds_y':[omin,omax],'new_unadjusted_bounds_y':[nmin,nmax],'top_anchor_weight':weight,'root_y_correction':dy})
    doc['unhandled_root_fields']['head_match']['placement']='root Y retargeted to old shell boundary: emerging top to bottom, body bottom, sinking bottom to top; head translation zero for connected hinge'
    target=AV/'arch_visage.bbmodel';write(target,doc)
    atlas=base64.b64decode(doc['textures'][0]['source'].split(',')[1]);(AV/'atlas.png').write_bytes(atlas)
    config['material'].update(accepted_HE_source_sha256=sha(source_path),head_match='exact source geometry/UV/PNG; only translated, no stretch')
    write(AV/'config.json',config)
    provenance={'model_sha256':sha(target),'HE_model_sha256':sha(source_path),'atlas_png_sha256':hashlib.sha256(atlas).hexdigest(),'atlas_png_identical_to_HE':True,'elements':records,'source_provenance':'../heart_of_ender_ref/final_material/MATERIAL_REPORT.md','note':'replaces previous AV-specific mouth projection; all current visible texels come from the HE main atlas'}
    write(AV/'atlas_regions.json',provenance);write(OUT/'geometry_transfer.json',provenance);write(OUT/'placement_adjustments.json',adjustments)
    mob,bones,clips,res=load(target);offsets={}
    for part,members in mob.parts:
        _,offsets[part]=dm.part_model(mob,bones,part,members,res)
    baked=dm.bake(mob,bones,offsets,clips)
    unchanged=[]
    for newa,olda in zip(doc['animations'],old['animations']):
        for aid,newtrack in newa['animators'].items():
            oldtrack=olda['animators'][aid]
            for nk,ok in zip(newtrack['keyframes'],oldtrack['keyframes']):
                assert nk['time']==ok['time'] and nk['channel']==ok['channel']
                if (newtrack['name'],nk['channel']) not in [('root','position'),('head','position')]:unchanged.append(nk==ok)
    sockets=[]
    point=[0,seam[1],-10.8+delta[2]]
    for t in [0,.2,.32,.48,.64,.8,2,3.04,3.20,3.68,4.88]:
        lips=[(np.array(dm.posed_matrix(bones,b,clips['spawn_attack'],t))@[*point,1])[:3]for b in ['head','jaw']]
        sockets.append({'time':t,'mouth_center_model':((lips[0]+lips[1])/2).tolist(),'upper_lip_model':lips[0].tolist(),'lower_lip_model':lips[1].tolist()})
    write(AV/'sockets.json',{'bbmodel_sha256':sha(target),'coordinate_system':'+Y up, front -Z; unscaled model units; divide by16 for blocks','status':'dynamic front lip midpoint; not official emitter; no beam created','samples':sockets})
    checks={'HE_source_unchanged':sha(source_path)==provenance['HE_model_sha256'],'exact_source_atlas_png':atlas==base64.b64decode(source['textures'][0]['source'].split(',')[1]),'unchanged_other_keyframes':all(unchanged),'all_parts_bake':len(offsets)==5,'single_atlas':len(doc['textures'])==1,'no_scale_channels':all(k['channel']in('position','rotation')for a in doc['animations']for v in a['animators'].values()for k in v['keyframes'])}
    result={'bbmodel_sha256':sha(target),'HE_model_sha256':sha(source_path),'element_count':len(elements),'bone_count':len(doc['groups']),'part_count':5,'keyframe_count':sum(len(a['keyframes'])for c in doc['animations']for a in c['animators'].values()),'checks':checks,'success':all(checks.values()),'clips':{n:{'source_length':clips[n]['length'],'baked_ticks':b['ticks'],'baked_frames':len(b['frames'])}for n,b in baked.items()},'real_game_seen':False,'native_blockbench_export_verified':False}
    write(OUT/'validation.json',result);write(AV/'validation.json',result)
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
