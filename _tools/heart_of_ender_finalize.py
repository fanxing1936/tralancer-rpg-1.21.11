"""Promote the source-backed face UV and bind the unchanged raw glow mask.

Only owns final_material/ and, with --promote, the task's primary bbmodel.
The reviewed v3 and face candidate remain immutable reconstruction inputs.
"""
from __future__ import annotations
import argparse, base64, copy, hashlib, io, json, uuid
from pathlib import Path
from types import SimpleNamespace
import numpy as np
from PIL import Image
import display_mob as dm
from heart_of_ender_material_probe import assemble_parts
from heart_of_ender_emission import mask_records

REF = Path(__file__).resolve().parent/'heart_of_ender_ref'
OUT = REF/'final_material'
BASE = REF/'gallery_followup/pose_analysis/candidate.bbmodel'
BASE_SHA = '5a6f434080a8bae55fa6f26b073421d656d67c515b1058b575eee730dab8e75c'
V3_SHA = 'af9f3fead3a0a57784288359a38b34fcc03ee6c22e78b7aef08b88d00858328d'

def sha(data): return hashlib.sha256(data).hexdigest()
def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', 'utf8')
def node(nodes, uid):
    for n in nodes:
        if isinstance(n, str): continue
        if n['uuid'] == uid: return n
        match = node(n['children'], uid)
        if match: return match

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--promote',action='store_true')
    args=parser.parse_args()
    raw=BASE.read_bytes()
    if sha(raw)!=BASE_SHA: raise ValueError('Face candidate changed; review before promotion')
    before=json.loads(raw); doc=copy.deepcopy(before)
    groups={g['name']:g for g in doc['groups']}
    template=next(e for e in doc['elements'] if e['name']=='front_eyes_surface')
    records=[]
    for name,bone,y,face in [('upper_mouth_raw44','shell_eyes_glow',25.998,'down'),
                              ('lower_mouth_raw44','shell_teeth_front_glow',26.002,'up')]:
        e=copy.deepcopy(template)
        e.update(name=name,uuid=str(uuid.uuid5(uuid.NAMESPACE_URL,'tralancer/heart_of_ender/'+name)),
                 origin=groups[bone]['origin'],rotation=[0,0,0],
                 **{'from':[-6,y,-10.8],'to':[6,y,1.61051]})
        e['faces']={n:{'uv':[0,0,0,0],'texture':None} for n in template['faces']}
        e['faces'][face]={'uv':[432,90,465,132],'texture':0,'tint':1}
        doc['elements'].append(e);node(doc['outliner'],groups[bone]['uuid'])['children'].append(e['uuid'])
        records.append({'element_uuid':e['uuid'],'element_name':name,'face':face,
                        'source_texture':'MCD_Heart_of_Ender_(glow_effect_texture).png',
                        'source_rect':[0,2,33,44],'atlas_rect':[432,90,465,132],
                        'tint_rgb':[255,211,255],
                        'tint_source':{'file':'Heart_of_Ender_prepare_to_shoot_beams.png','pixel':[1105,267]},
                        'mode':'source RGB multiplied by constant item tint; original alpha source-over',
                        'status':'mouth mapping inferred; original raw RGBA unchanged; no bloom'})
    fields=doc.setdefault('unhandled_root_fields',{})
    fields['emissive_masks']=records
    fields['heart_of_ender_stage']='Final model and animation integration; R2 geometry with source-backed face UV and two mouth mask planes'
    fields['glow_mask']['binding']='two emissive mouth planes, raw source white field [0,2,33,44], item constant tint'
    fields['material_status'].update(version='Final material v4',
        raw44='RGBA unchanged; actually sampled by two mouth planes and tinted at runtime',
        runtime='pending final resource/datapack and native codec verification; client visual review separate',
        face='source-backed six-patch eyebrow/eye UV reconstruction, same v3 palette')
    target=OUT/'heart_of_ender_final.bbmodel';write(target,doc)
    mob=SimpleNamespace(bbmodel=str(target),anim_from=None,key='heart_of_ender',glow=set(groups),
                        model_scale=1.,seat=-4.66381/16,tex='rpg:item/heart_of_ender/atlas',held=None)
    bones,png,res=dm.load_bbmodel(mob);clips=dm.load_animations(mob)
    parts=assemble_parts(json.loads((REF/'m2_geometry/geometry_spec.json').read_text('utf8')),bones,clips)
    mob.parts=parts;mob.clips=[(name,1,name in ('idle','walk')) for name in clips]
    old_bones,_,_=dm.load_bbmodel(SimpleNamespace(bbmodel=str(BASE)))
    offsets={};offset_errors={}
    for part,members in parts:
        model,k=dm.part_model(mob,bones,part,members,res)
        _,old_k=dm.part_model(mob,old_bones,part,members,res)
        offsets[part]=k;offset_errors[part]=max(abs(x-y) for x,y in zip(k,old_k))
    baked=dm.bake(mob,bones,offsets,clips)
    atlas=np.array(Image.open(io.BytesIO(png)).convert('RGBA'))
    original_mask=np.array(Image.open(REF/'MCD_Heart_of_Ender_(glow_effect_texture).png').convert('RGBA'))
    tint_source=Image.open(REF/'Heart_of_Ender_prepare_to_shoot_beams.png').convert('RGBA').getpixel((1105,267))
    checks={
        'immutable_face_candidate':sha(BASE.read_bytes())==BASE_SHA,
        'all_original_49_elements_unchanged':doc['elements'][:49]==before['elements'],
        'exactly_two_registered_emissive_planes':len(doc['elements'])==51 and len(mask_records(doc))==2,
        'same_groups_and_animations':doc['groups']==before['groups'] and doc['animations']==before['animations'],
        'embedded_png_bytes_unchanged':doc['textures']==before['textures'],
        'raw44_rgba_exact':np.array_equal(atlas[88:132,432:476],original_mask),
        'sampled_white_field_original_rgb':bool(np.all(original_mask[2:44,0:33,:3]==255)),
        'source_tint_exact':tint_source[:3]==(255,211,255),
        'all_21_part_centers_unchanged':len(parts)==21 and max(offset_errors.values())<1e-12,
        'all_numeric_bakes_finite':all(np.isfinite(x).all() for c in baked.values() for _,f in c['frames'] for comp in f.values() for x in comp),
        'rotation_position_only':all(k['channel'] in ('rotation','position') for a in doc['animations'] for an in a['animators'].values() for k in an['keyframes']),
    }
    final_sha=sha(target.read_bytes());write(OUT/'validation.json',{'checks':checks,'success':all(checks.values()),
        'model_sha256':final_sha,'candidate_sha256':BASE_SHA,'elements':len(doc['elements']),'bones':len(groups),
        'parts':len(parts),'keyframes':sum(len(an['keyframes']) for a in doc['animations'] for an in a['animators'].values()),
        'offset_errors':offset_errors,'raw_mask_source_sha256':sha((REF/records[0]['source_texture']).read_bytes()),
        'runtime_bakes':{n:{'ticks':c['ticks'],'frames':len(c['frames'])} for n,c in baked.items()}})
    if not all(checks.values()): raise ValueError(checks)
    write(OUT/'material_changes.json',{'model_sha256':final_sha,'face_candidate_sha256':BASE_SHA,'mask_records':records,
        'original_mask_atlas_rect':[432,88,476,132], 'original_mask_rgba_preserved':True,
        'unmapped_mask_regions':'top two rows and right 11 columns contain dark/non-emitting RGB; not repainted or mapped to mouth',
        'geometry_change':'two coplanar-offset interior surfaces, no silhouette/rig/animation or part-center changes',
        'source_alpha_used_as_is':True,'visual_status':'offline/native/runtime checks separate; no claimed client view'})
    (OUT/'atlas.png').write_bytes(png)
    sockets=json.loads((REF/'m3_material_v3/sockets.json').read_text('utf8'));sockets['bbmodel_sha256']=final_sha
    sockets['model_scale']=1;sockets['carrier_seat']=-4.66381/16
    sockets['placement_note']='physical Marker armor_stand seat=0; pipeline seat parameter additionally compensates research ground_y/16'
    write(OUT/'sockets.json',sockets)
    if args.promote:
        main=REF/'heart_of_ender.bbmodel'
        if sha(main.read_bytes()) not in (V3_SHA,BASE_SHA,final_sha):raise ValueError('Main model contains unreviewed changes; not overwriting')
        main.write_bytes(target.read_bytes())
    print(json.dumps({'model_sha256':final_sha,'promoted':args.promote,'parts':21,'checks':checks},ensure_ascii=False))

if __name__=='__main__':main()
