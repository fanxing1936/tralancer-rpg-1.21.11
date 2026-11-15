"""从可追溯源像素、测量与数字轨道生成 Arch-Visage Blockbench 工程。"""
from pathlib import Path
from types import SimpleNamespace
import base64, copy, hashlib, io, json, math, shutil, sys, uuid
import numpy as np
from PIL import Image
from scipy.ndimage import label
from scipy.optimize import least_squares
import display_mob as dm
from arch_visage_fit import project

HERE=Path(__file__).resolve().parent;REF=HERE/'heart_of_ender_ref';OUT=HERE/'arch_visage_ref'
BASE=REF/'m3_material_v3/heart_of_ender_material_v3.bbmodel'
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'tralancer:arch_visage:'+s))
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def png(im):
    b=io.BytesIO();im.save(b,format='PNG');return b.getvalue()
def sample_quad(src,quad,w=128,h=128):
    # Unit-square homography, integer texel-center nearest-neighbor sampling.
    A=[];b=[]
    for (u,v),(x,y) in zip([(0,0),(1,0),(1,1),(0,1)],quad):
        A.extend([[u,v,1,0,0,0,-u*x,-v*x],[0,0,0,u,v,1,-u*y,-v*y]]);b.extend([x,y])
    H=np.append(np.linalg.solve(np.array(A),b),1).reshape(3,3)
    y,x=np.mgrid[0:h,0:w];q=np.stack([(x+.5)/w,(y+.5)/h,np.ones_like(x)],-1)@H.T
    xx=np.floor(q[:,:,0]/q[:,:,2]+.5).astype(int);yy=np.floor(q[:,:,1]/q[:,:,2]+.5).astype(int)
    return src[yy,xx].copy(),H,xx,yy

def main():
    OUT.mkdir(exist_ok=True)
    current=OUT/'arch_visage.bbmodel'
    if current.exists() and json.loads(current.read_text(encoding='utf-8')).get('unhandled_root_fields',{}).get('head_match'):
        raise SystemExit('当前模型已按用户要求复用HE主头部；请使用 arch_visage_match_head.py，禁止旧厚颚生成器覆盖。')
    base=json.loads(BASE.read_text(encoding='utf-8'));cal=json.loads((OUT/'calibration.json').read_text());motion=json.loads((OUT/'refined_motion.json').read_text())
    D,H,J,JW,JD=cal['parameters'][:5]
    atlas=np.array(Image.open(io.BytesIO(base64.b64decode(base['textures'][0]['source'].split(',')[1]))).convert('RGBA'))
    original=atlas.copy();source=np.array(Image.open(REF/'MCD_Arch-Visage.png').convert('RGBA'))
    materials=[]
    for name,quad,rect in [('upper_mouth',[[185,319],[406,451],[491,576],[273,449]],[600,800,728,928]),('lower_mouth',[[339,626],[120,500],[273,449],[491,576]],[740,800,868,928])]:
        x0,y0,x1,y1=rect;assert not atlas[y0:y1,x0:x1].any()
        a,m,x,y=sample_quad(source,quad)
        atlas[y0:y1,x0:x1]=a
        materials.append({'name':name,'source_file':'../heart_of_ender_ref/MCD_Arch-Visage.png','source_sha256':sha((REF/'MCD_Arch-Visage.png').read_bytes()),'source_quad':quad,'atlas_rect':rect,'sampling':'homography output pixel centers (x+.5)/128, (y+.5)/128; floor(source+.5); original RGBA untouched','matrix':m.tolist(),'output_rgba_sha256':sha(a.tobytes()),'geometry_mapping':'visible cavity-face projection inferred from the static open-mouth render; source pixel colors and irregular bright boundaries copied, no invented pattern'})
    atlas_bytes=png(Image.fromarray(atlas));(OUT/'atlas.png').write_bytes(atlas_bytes)
    template_e=copy.deepcopy(base['elements'][0]);template_g=copy.deepcopy(base['groups'][0]);elements=[];groups=[];nodes={}
    parents={'root':None,'head':'root','jaw':'root','head_light':'head','jaw_light':'jaw','eyes':'head'}
    pivots={'root':[0,0,0],'head':[0,J,D/2],'jaw':[0,J,JD/2],'head_light':[0,J,D/2],'jaw_light':[0,J,JD/2],'eyes':[0,J,D/2]}
    for name in parents:
        g=copy.deepcopy(template_g);g.update(name=name,uuid=uid(name),origin=pivots[name],rotation=[0,0,0],children=[]);groups.append(g);nodes[name]={'uuid':g['uuid'],'children':[]}
    for name,parent in parents.items():
        if parent:nodes[parent]['children'].append(nodes[name])
    null=lambda:{n:{'uv':[0,0,0,0],'texture':None}for n in ['north','east','south','west','up','down']}
    def cube(name,bone,lo,hi,faces):
        e=copy.deepcopy(template_e);e.update(name=name,uuid=uid(name),type='cube',origin=pivots[bone],rotation=[0,0,0],inflate=0,from_=lo)
        e.pop('from_',None);e['from']=list(lo);e['to']=list(hi);e['faces']=null();e['shade']=False;e['visibility']=True
        for face,uv in faces.items():e['faces'][face]={'uv':list(uv),'texture':0}
        elements.append(e);nodes[bone]['children'].append(e['uuid']);return e
    face_names=['north','east','south','west','up','down'];windows=[(8,8),(144,8),(280,8),(8,144),(144,144),(280,144)]
    def star_faces(width,height,depth,density,offset=0):
        dims=[(width,height),(depth,height),(width,height),(depth,height),(width,depth),(width,depth)];result={}
        for k,(face,(w,h))in enumerate(zip(face_names,dims)):
            x,y=windows[(k+offset)%6];ww=min(124,w*density);hh=min(124,h*density);result[face]=[x+2,y+2,x+2+ww,y+2+hh]
        return result
    skull=cube('upper_skull','head',[-6,J,-D/2],[6,J+H,D/2],star_faces(12,H,D,4.5))
    jaw=cube('lower_jaw','jaw',[-JW/2,0,-JD/2],[JW/2,J,JD/2],star_faces(JW,J,JD,9,3))
    # Source-derived teeth stay attached to their respective lip; image-space
    # source masks are reused from accepted HE atlas, with no new tooth drawing.
    cube('upper_front_teeth','head',[-6,J,-D/2-.012],[5.25,J+1.2,-D/2-.012],{'north':[159,408,272,420]})
    cube('lower_front_teeth','jaw',[-JW/2,J-1.2,-JD/2-.012],[JW/2,J,-JD/2-.012],{'north':[159,420,272,432]})
    cube('upper_side_teeth','head',[-6.012,J,-D/2],[-6.012,J+1.2,-D/2+4.3],{'west':[280,408,324,418]})
    cube('lower_side_teeth','jaw',[-JW/2-.012,J-1.2,-JD/2],[-JW/2-.012,J,-JD/2+4.3],{'west':[280,418,324,426]})
    # Fit actual white-core centroids, not a guessed fraction of skull height.
    eye_pixels=atlas[362:379,20:123];eye_mask=(eye_pixels[:,:,0]>230)&(eye_pixels[:,:,1]>180)&(eye_pixels[:,:,2]>230)&(eye_pixels[:,:,3]>25)
    labs,n=label(eye_mask);uv_centers=[]
    for i in range(1,n+1):
        yy,xx=np.where(labs==i)
        if len(xx)>50:uv_centers.append([float((xx+.5).mean()/103),float((yy+.5).mean()/17)])
    uv_centers.sort();assert len(uv_centers)==2
    source5=np.array(Image.open(REF/'frames/MCD_Arch-Visage_Spawn_Attack_in_game/frame_0005.png').convert('RGBA'))
    source_centers=[]
    for x0,y0,x1,y1 in [(140,155,190,200),(200,185,245,225)]:
        a=source5[y0:y1,x0:x1];m=(a[:,:,0]>230)&(a[:,:,1]>180)&(a[:,:,2]>230)&(a[:,:,3]>25);yy,xx=np.where(m);source_centers.append([float(xx.mean()+x0),float(yy.mean()+y0)])
    target=np.array(source_centers)
    def predicted_eye(p):
        cx,cy,w=p;pts=np.array([[cx+w/2-u*w,cy+.8-v*1.6,-D/2-.018]for u,v in uv_centers]);return project(cal,pts)
    ef=least_squares(lambda p:(predicted_eye(p)-target).ravel(),[0,J+4.4,9.6]);cx,cy,ew=ef.x
    cube('source_eye_cores','eyes',[cx-ew/2,cy-.8,-D/2-.018],[cx+ew/2,cy+.8,-D/2-.018],{'north':[20,362,123,379]})
    write(OUT/'eyes_fit.json',{'source_frame':5,'source_time':.2,'threshold':'RGBA alpha>25,R>230,G>180,B>230','source_core_centers':source_centers,'atlas_core_normalized_centers':uv_centers,'fitted_plane_center':[float(cx),float(cy),-D/2-.018],'width':float(ew),'height':1.6,'projected_centers':predicted_eye(ef.x).tolist(),'center_rms_px':float(np.sqrt(np.mean((predicted_eye(ef.x)-target)**2))),'source005_closed_calibration_pose':True,'early_visibility':'s002/s003 source no eye cores; eyes hidden inside skull until s004'})
    cube('upper_cavity','head_light',[-6,J-.018,-D/2],[6,J-.018,D/2],{'down':[600,800,728,928]})
    cube('lower_cavity','jaw_light',[-JW/2,J+.018,-JD/2],[JW/2,J+.018,JD/2],{'up':[740,800,868,928]})
    masks=[]
    for name,bone,lo,hi,face in [('upper_raw44','head_light',[-6,J-.025,-D/2],[6,J-.025,D/2],'down'),('lower_raw44','jaw_light',[-JW/2,J+.025,-JD/2],[JW/2,J+.025,JD/2],'up')]:
        e=cube(name,bone,lo,hi,{face:[432,90,465,132]})
        masks.append({'element_uuid':e['uuid'],'face':face,'tint_rgb':[255,211,255],'source_texture':'MCD_Heart_of_Ender_(glow_effect_texture).png','source_rect':[0,2,33,44],'atlas_rect':[432,90,465,132]})
    animations=[]
    def anim(name,length,loop,tracks):
        animators={}
        for (bone,channel),values in tracks.items():
            a=animators.setdefault(uid(bone),{'name':bone,'type':'bone','keyframes':[]})
            for time,val in values:
                a['keyframes'].append({'channel':channel,'data_points':[dict(zip('xyz',[float(v)for v in val]))],'uuid':uid(f'{name}/{bone}/{channel}/{time}'),'time':float(time),'color':-1,'interpolation':'linear'})
        animations.append({'uuid':uid('animation.'+name),'name':'animation.'+name,'loop':'loop'if loop else'once','override':False,'length':length,'snapping':25,'anim_time_update':'','blend_weight':'','start_delay':'','loop_delay':'','animators':animators})
    for name in ['idle','walk']:anim(name,1.0,True,{('root','position'):[(0,[0,-40,0]),(1,[0,-40,0])]})
    tracks={}
    def key(bone,channel,t,v):tracks.setdefault((bone,channel),[]).append((t,v))
    for r in motion['records']:
        i=r['frame'];t=i/25;a,b,ry,rz,x,y,hy=r['pose']
        shift=np.array(r.get('depth_lift_translation',[0,0,0]));position=np.array([x,y,0])+shift
        key('root','rotation',t,[0,ry,rz]);key('root','position',t,position.tolist());key('head','rotation',t,[a,0,0]);key('head','position',t,[0,hy,0]);key('jaw','rotation',t,[b,0,0])
        light_on=(6<=i<=9)or(17<=i<=80)
        key('head_light','position',t,[0,0 if light_on else .4,0]);key('jaw_light','position',t,[0,0 if light_on else -.4,0]);key('eyes','position',t,[0,0,0 if 4<=i<=16 else 1])
    for track in tracks.values():track.append((4.88,track[-1][1]))
    anim('spawn_attack',4.88,False,tracks)
    texture=copy.deepcopy(base['textures'][0]);texture.update(name='arch_visage_atlas.png',path='',source='data:image/png;base64,'+base64.b64encode(atlas_bytes).decode())
    doc={k:copy.deepcopy(v)for k,v in base.items()if k not in ['elements','groups','outliner','textures','animations','unhandled_root_fields']}
    doc.update(name='arch_visage',model_identifier='geometry.arch_visage',elements=elements,groups=groups,outliner=[nodes['root']],textures=[texture],animations=animations,
        unhandled_root_fields={'arch_visage_stage':'M4; in-game GIF reference; geometric/hidden-depth fitting is inference','emissive_masks':masks,'source_raw44':{'atlas_rect':[432,88,476,132],'rgba':'unchanged','usage':'effective white subset [0,2,33,44) is sampled by two mouth layers and multiplied by constant source tint in item definition; no screen bloom'},'animation_note':'idle and walk are hidden static compatibility clips, not original movement; spawn_attack source 4.88s, 20Hz bake rounds to4.90s'})
    path=OUT/'arch_visage.bbmodel';write(path,doc)
    sounds={};(OUT/'sounds').mkdir(exist_ok=True)
    for p in (REF/'sounds').glob('*Archvisage*.ogg'):shutil.copyfile(p,OUT/'sounds'/p.name)
    for event,stem,zh,en in [('tele_in','TeleIn','现身','appears'),('tele_out','TeleOut','沉入地面','sinks'),('beam_attack','BeamAttack','张嘴蓄光','charges its mouth'),('beam_loop','BeamLoop','口内鸣响','mouth hums'),('mortar','MortarShoot','投射音效存档','archived mortar sound')]:
        files=sorted(p.name for p in (OUT/'sounds').glob('Sfx_boss_Archvisage'+stem+'*.ogg'))
        sounds[event]=[[f'Arch-Visage：{zh}',f'Arch-Visage {en}'],files,None]
    config={'key':'arch_visage','label':'Arch-Visage','bbmodel':'arch_visage.bbmodel','tag':'rpg.av','score':'rpg_av','carrier':'minecraft:armor_stand','model_scale':1.0,'seat':0.0,'research_ground_y':0.0,'parts':[{'name':b,'bones':[b]}for b in ['head','jaw','eyes','head_light','jaw_light']],'glow':['head','jaw','eyes','head_light','jaw_light'],'clips':[['idle',1,True],['walk',1,True],['spawn_attack',1,False]],'sounds':sounds,'sound_dir':'sounds','cues':{'spawn_attack':[[.72,'beam_attack',1,1],[.80,'beam_loop',.6,1],[3.28,'tele_out',1,1]]},'enter_cues':{'spawn_attack':[['tele_in',1,1]]},'material':{'atlas':'atlas.png','accepted_HE_source_sha256':sha(BASE.read_bytes()),'fullbright':True,'raw44_rgba_preserved':True,'actual_mask_consumption':'emissive_masks metadata, dedicated generated-item constant tint postprocess','no_bloom':True},'emissive':{'metadata':'unhandled_root_fields.emissive_masks','mask_bones':['head_light','jaw_light']},'placeholder_clips':['idle','walk'],'debug_recommended_clip':'spawn_attack','sound_timing_status':'timings attached to observed visual stages; original GIF has no audio, not verified original audiovisual sync','part_count_reason':'5 independent display parts: head, jaw, eye on/off, upper-cavity on/off, lower-cavity on/off. Visibility uses position into opaque parent, never scale.'}
    face_uvs=[{'element':e['name'],'bone':next(b for b,n in nodes.items()if e['uuid']in n['children']),'face':f,'atlas_uv':d['uv'],'source_type':'original44_white_subset_with_constant_tint'if'raw44'in e['name']else'Arch-Visage render projected cavity'if'cavity'in e['name']else'accepted_HE_v3_exact_atlas_pixels'}for e in elements for f,d in e['faces'].items()if d.get('texture')is not None]
    write(OUT/'config.json',config);write(OUT/'atlas_regions.json',{'atlas_png_sha256':sha(atlas_bytes),'base_HE_v3_atlas':'../heart_of_ender_ref/m3_material_v3/atlas.png','base_HE_bbmodel_sha256':sha(BASE.read_bytes()),'regions':materials,'face_uvs':face_uvs,'inherited_regions':'remaining atlas bytes are from accepted HE v3; exact stars/teeth/eye provenance is in HE m2_atlas and m3_material material manifests','inherited_provenance_files':['../heart_of_ender_ref/m2_atlas/atlas_regions.json','../heart_of_ender_ref/m3_material/material_transform.json','../heart_of_ender_ref/m3_material_v3/material_changes.json'],'raw44_atlas_rect':[432,88,476,132],'new_tiles_only':True})
    mob=dm.Mob(key='arch_visage',label='Arch-Visage',generator='arch_visage_author.py',bbmodel=str(path),parts=[(p['name'],p['bones'])for p in config['parts']],glow=config['glow'],seat=0,tag='rpg.av',score='rpg_av',clips=config['clips'])
    bones,_,res=dm.load_bbmodel(mob);clips=dm.load_animations(mob);offsets={};bounds=[]
    for part,members in mob.parts:
        model,k=dm.part_model(mob,bones,part,members,res);offsets[part]=k;bounds.append({'part':part,'element_count':len(model['elements']),'K':k})
    baked=dm.bake(mob,bones,offsets,clips)
    raw44=np.array(Image.open(REF/'MCD_Heart_of_Ender_(glow_effect_texture).png').convert('RGBA'))
    assert np.array_equal(atlas[88:132,432:476],raw44)
    assert all(k['channel']in['position','rotation']for a in animations for an in a['animators'].values()for k in an['keyframes'])
    sockets=[]
    for t in [0,.20,.32,.48,.64,.80,2,3.04,3.20,3.68,4.88]:
        points=[]
        for bone,p in [('head',[0,J,-D/2]),('jaw',[0,J,-JD/2])]:
            m=np.array(dm.posed_matrix(bones,bone,clips['spawn_attack'],t));points.append((m@[*p,1])[:3])
        center=(points[0]+points[1])/2
        sockets.append({'time':t,'mouth_center_model':center.tolist(),'upper_lip_model':points[0].tolist(),'lower_lip_model':points[1].tolist(),'suggested_forward_minus_z':'root/head orientation required at runtime; actual original beam emitter depth not recovered'})
    write(OUT/'sockets.json',{'bbmodel_sha256':sha(path.read_bytes()),'coordinate_system':'+Y up, front -Z; unscaled model units; divide by16 and multiply model_scale for blocks','status':'dynamic midpoint of modeled front lips, candidate FX attachment only; no beam created','samples':sockets})
    write(OUT/'validation.json',{'bbmodel_sha256':sha(path.read_bytes()),'element_count':len(elements),'bone_count':len(groups),'part_count':len(mob.parts),'clips':{n:{'source_length':clips[n]['length'],'baked_ticks':b['ticks'],'baked_frames':len(b['frames'])}for n,b in baked.items()},'keyframe_count':sum(len(an['keyframes'])for a in animations for an in a['animators'].values()),'checks':{'single_atlas':True,'raw44_rgba_exact':True,'part_bounds_inside_minus16_32':True,'numeric_rotation_position_only':True,'idle_walk_first':True,'all_three_clips_memory_baked':True,'no_shared_file_written':True},'parts':bounds,'errors':0,'real_game_seen':False,'native_blockbench_export_verified':False})
    print(json.dumps({'bbmodel':str(path),'sha256':sha(path.read_bytes()),'parts':len(mob.parts),'elements':len(elements),'clips':list(clips)},ensure_ascii=False))

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8');main()
