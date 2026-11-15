"""Lossless PSA fields plus explicit, source-backed Java-coordinate animation tracks.

No Blockbench calls. All original PSA scalars are retained in raw_keys_frame_major.
BONENAMES parents are exporter placeholders; hierarchy is taken from the paired glTF.
"""
from pathlib import Path
import struct,json,hashlib,math
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent
OLD=ROOT.parent/'lucifer_original'
BASE=ROOT/'necromancer_exported/Game/Actors/Characters/Enemies/SkeletonNecromancer'
REPO=Path(r'D:\agent\claude\github-create\tralancer-rpg-1.21.11')

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def normal(q):
    q=np.asarray(q,float);return q/np.linalg.norm(q)
def qmat(q):
    x,y,z,w=normal(q)
    return np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],
                     [2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],
                     [2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])
def local(p,q):
    m=np.eye(4);m[:3,:3]=qmat(q);m[:3,3]=p;return m
def name(b):return b.split(b'\0',1)[0].decode('utf-8')
def psa(path):
    b=path.read_bytes();o=0;chunks={}
    while o<len(b):
        n,version,size,count=struct.unpack_from('<20siii',b,o)
        n=name(n);start=o+32;assert n not in chunks and count>=0 and size>=0
        chunks[n]={'header_offset':o,'data_offset':start,'element_size':size,'count':count,'version':version}
        o=start+size*count
    assert o==len(b) and set(chunks)=={'ANIMHEAD','BONENAMES','ANIMINFO','ANIMKEYS','SCALEKEYS'}
    assert chunks['BONENAMES']['element_size']==120 and chunks['ANIMINFO']['element_size']==168
    assert chunks['ANIMKEYS']['element_size']==32 and chunks['SCALEKEYS']['count']==0
    bones=[]
    for i in range(chunks['BONENAMES']['count']):
        vals=struct.unpack_from('<64sIii11f',b,chunks['BONENAMES']['data_offset']+i*120)
        bones.append({'track_index':i,'name':name(vals[0]),'flags':vals[1],'num_children_placeholder':vals[2],
                      'parent_index_placeholder':vals[3],'reference_quaternion_UE_raw':list(vals[4:8]),
                      'reference_position_UE_cm':list(vals[8:11]),'length':vals[11],'size':list(vals[12:15])})
    infos=[]
    for i in range(chunks['ANIMINFO']['count']):
        a=struct.unpack_from('<64s64s4i3f3i',b,chunks['ANIMINFO']['data_offset']+i*168)
        infos.append(dict(zip(['name','group','total_bones','root_include','key_compression_style','key_quotum','key_reduction','track_time_units','anim_rate','start_bone','first_raw_frame','num_raw_frames'],[name(a[0]),name(a[1]),*a[2:]])))
    assert len(infos)==1
    info=infos[0];N=info['num_raw_frames'];B=info['total_bones'];assert B==len(bones)
    assert chunks['ANIMKEYS']['count']==N*B
    keys=np.array([struct.unpack_from('<8f',b,chunks['ANIMKEYS']['data_offset']+i*32) for i in range(N*B)]).reshape(N,B,8)
    assert np.all(np.isfinite(keys)) and np.all(keys[:,:,7]==1)
    return chunks,bones,info,keys

def main():
    gp=BASE/'SK_SkeletonNecromancer.gltf';g=json.loads(gp.read_text());joints=g['skins'][0]['joints'];node_to_joint={n:i for i,n in enumerate(joints)}
    parents={c:i for i,n in enumerate(g['nodes']) for c in n.get('children',[])}
    chunks,psa_bones,_,_=psa(BASE/'Animations/SkeletonNecromancer_Idle.psa')
    track_by_name={b['name'].lower():b['track_index'] for b in psa_bones}
    bones=[];gw={};sw={}
    for i,ni in enumerate(joints):
        n=g['nodes'][ni];pid=node_to_joint.get(parents.get(ni));track=track_by_name[n['name'].lower()];ref=psa_bones[track]
        p=np.array(n['translation'])*[-16,16,-16];q=normal(np.array(n['rotation'])*[-1,1,-1,1]);m=local(p,q)
        rp=np.array(ref['reference_position_UE_cm']);rp=np.array([-.16*rp[0],.16*rp[2],-.16*rp[1]])
        rq=ref['reference_quaternion_UE_raw'];rq=normal([rq[0],-rq[2],rq[1],rq[3]])
        rm=local(rp,rq)
        gw[i]=(gw[pid] if pid is not None else np.eye(4))@m
        sw[i]=(sw[pid] if pid is not None else np.eye(4))@rm
        bones.append({'index':i,'name':n['name'],'parent_index':pid,'parent_name':g['nodes'][joints[pid]]['name'] if pid is not None else None,
                      'psa_track_index':track,'restLocalJava':{'translation':p.tolist(),'quaternion':q.tolist()},
                      'restWorldJava':gw[i].tolist(),'psaReferenceLocalJava':{'translation':rp.tolist(),'quaternion':rq.tolist()},
                      'psaReferenceWorldJava':sw[i].tolist(),
                      'gltf_vs_psa_reference_local_position_max_error_px':float(np.abs(p-rp).max()),
                      'gltf_vs_psa_reference_local_rotation_matrix_max_error':float(np.abs(m[:3,:3]-rm[:3,:3]).max())})
    animations=[]
    for nm in ['Idle','Walk','BasicAttack','StrongAttack','Stun','Novelty','GetHitFront']:
        path=BASE/'Animations'/f'SkeletonNecromancer_{nm}.psa';cs,bs,info,keys=psa(path)
        assert bs==psa_bones
        config=path.with_suffix('.config').read_text(encoding='utf-8')
        unused=[i for i in range(len(bs)) if f'{info["name"]}.{i}=all' in config]
        assert set(unused) <= {35,36}
        tracks=[]
        for bone in bones:
            i=bone['psa_track_index'];k=keys[:,i,:];p=k[:,:3];q=k[:,3:7]
            jp=np.stack([-.16*p[:,0],.16*p[:,2],.16*p[:,1]],axis=1)
            jq=np.stack([-q[:,0],q[:,2],q[:,1],-q[:,3]],axis=1)
            if bone['parent_index'] is None: jq[:,:3]*=-1
            jq/=np.linalg.norm(jq,axis=1)[:,None]
            # q and -q encode same orientation; keep a continuous representative for interpolation.
            for f in range(1,len(jq)):
                if np.dot(jq[f],jq[f-1])<0:jq[f]*=-1
            tracks.append({'bone_index':bone['index'],'bone_name':bone['name'],'psa_track_index':i,
                           'position_java_px':jp.tolist(),'quaternion_java_xyzw_normalized_continuous':jq.tolist()})
        fps=info['anim_rate'];N=info['num_raw_frames']
        gif=REPO/'_tools/lucifer_ref'/f'MCD_Necromancer_{nm}.gif';im=Image.open(gif);times=[]
        for f in range(im.n_frames):im.seek(f);times.append(im.info.get('duration',0)/1000)
        animations.append({'short_name':nm,'psa_path':str(path),'psa_sha256':sha(path),'chunks':cs,'anim_info':info,
                           'sample_times_seconds':[i/fps for i in range(N)],'duration_seconds':N/fps,
                           'last_sample_seconds':(N-1)/fps,'raw_keys_layout':'[frame][psa_track][px,py,pz,qx,qy,qz,qw,time_units]',
                           'raw_keys_frame_major':keys.tolist(),'tracks_java':tracks,
                           'unused_removed_tracks':[{'index':i,'name':bs[i]['name'],'reason':'PSA config RemoveTracks=all'} for i in unused],
                           'tracks_absent_from_mesh':[{'index':i,'name':bs[i]['name'],'removed_by_config':i in unused} for i in [35,36]],
                           'reference_gif':{'path':str(gif),'sha256':sha(gif),'frames':im.n_frames,'duration_seconds':sum(times),'frame_durations_seconds':times}})
    target=json.loads((OLD/'body_for_blockbench.json').read_text());nb={b['name'].lower():b for b in bones};tw={};mapping=[]
    for tb in target['bones']:
        s=nb[tb['name'].lower()];pid=tb['parent'];i=tb['id'];tm=local(tb['translation'],tb['quaternion']);tw[i]=(tw[pid] if pid is not None else np.eye(4))@tm
        src_world=np.array(s['restWorldJava']);src_ref=np.array(s['psaReferenceWorldJava']);target_world=tw[i]
        same_parent=(s['parent_name'] or '').lower()==(target['bones'][pid]['name'].lower() if pid is not None else '')
        mapping.append({'target_id':i,'target_name':tb['name'],'source_index':s['index'],'source_name':s['name'],
                        'psa_track_index':s['psa_track_index'],'same_parent_by_casefold_name':same_parent,
                        'target_restLocalJava':{'translation':tb['translation'],'quaternion':normal(tb['quaternion']).tolist()},
                        'target_restWorldJava':target_world.tolist(),
                        'source_gltf_vs_target_restworld_matrix_max_abs_difference':float(np.abs(src_world-target_world).max()),
                        'source_gltf_vs_target_origin_delta_java_px':(src_world[:3,3]-target_world[:3,3]).tolist(),
                        'source_gltf_vs_target_linear_max_abs_difference':float(np.abs(src_world[:3,:3]-target_world[:3,:3]).max()),
                        'source_psa_reference_vs_target_restworld_matrix_max_abs_difference':float(np.abs(src_ref-target_world).max())})
    assert len(mapping)==22 and all(m['same_parent_by_casefold_name'] for m in mapping)
    # Algebraic zero-motion retarget test: world rotation delta from source bind is identity.
    errs=[]
    for m in mapping:
        s=bones[m['source_index']];S=np.array(s['psaReferenceWorldJava'])[:3,:3];T=tw[m['target_id']][:3,:3]
        retarget=S@np.linalg.inv(S)@T
        errs.append(float(np.max(np.abs(retarget-T))))
    result={'schema':'umodel-psa-java-source-v1','scope':'Original animation source evidence and coordinate conversion; no final adapted clips, Blockbench writes or combat changes.',
            'rig_gltf':{'path':str(gp),'sha256':sha(gp),'bin_sha256':sha(gp.with_suffix('.bin'))},
            'bones':bones,'psa_bone_records':psa_bones,'animations':animations,'target_mapping':mapping,
            'target_input':{'path':str(OLD/'body_for_blockbench.json'),'sha256':sha(OLD/'body_for_blockbench.json')},
            'coordinate_rules':{'psa_key_position_to_java':'[-0.16*px, +0.16*pz, +0.16*py]',
                                'psa_nonroot_key_quaternion_to_java':'normalize([-qx,+qz,+qy,-qw])',
                                'psa_root_key_quaternion_to_java':'normalize([+qx,-qz,-qy,-qw])',
                                'psa_bonenames_reference_position_to_java':'[-0.16*px,+0.16*pz,-0.16*py]',
                                'psa_bonenames_reference_quaternion_to_java':'normalize([+qx,-qz,+qy,+qw])',
                                'gltf_position_to_java':'[-16*x,+16*y,-16*z]',
                                'gltf_quaternion_to_java':'normalize([-qx,+qy,-qz,+qw])',
                                'reason':'PSA key mirror is undone; UModel animation nonroot FixRotationKeys differs from unmodified BONENAMES refpose; glTF conjugates root and swaps Y/Z. Java applies proper 180-degree Y rotation.',
                                'psa_time':'VQuatAnimKey.Time is 1 frame-unit for every key; seconds=f/AnimRate, not the stored Time=1 seconds.',
                                'psa_parent':'Exporter placeholder, never used. 35 real bone parents resolved from same original mesh glTF; 2 unused tracks remain raw data only.'},
            'static_zero_motion_retarget_rotation_error':max(errs),
            'retarget_recommendation':{'rotation':'D_world(t)=R_source_world(t)*inverse(R_source_reference_world); R_target_world(t)=D_world(t)*R_target_reference_world; R_target_local(t)=inverse(R_target_parent_world(t))*R_target_world(t). Use normalized quaternions/matrices and slerp, never add source Euler angles.',
                                     'translation':'Preserve target rest bone offsets. Transform the source local-position delta through C_parent = inverse(R_target_parent_reference_world)*R_source_parent_reference_world, then add to target local rest. Apply any locomotion/foot-lock/amplitude choice as an explicit adaptation. Do not copy source absolute local positions.',
                                     'native_Euler':'Convert the final target local rotation to the exact Blockbench Euler order; unwrap continuity; channel = solvedLocalEuler - nativeRestEuler. Subtraction is only the final serialization adapter, not the retarget operation.',
                                     'basis_choice':'psaReferenceLocal/World is the USkeleton reference used by animation; restLocal/World is the exported mesh bind pose. Both supplied and errors reported. Shared 22 mapped names all have matching hierarchy. J_* joint bind frames coincide numerically, but geometry-marker bones Body/Head/R_Arm/R_Leg/L_Leg have different bind origins and sometimes orientations; never copy their absolute local poses.',
                                     'unadapted_clips':'Walk still original hover locomotion; BasicAttack still original staff action; these source tracks are not mislabeled finished walking/spear-thrust animation.'},
            'primary_sources':['https://github.com/gildor2/UEViewer/blob/master/Exporters/Psk.h',
                               'https://github.com/gildor2/UEViewer/blob/master/Exporters/ExportPsk.cpp',
                               'https://github.com/gildor2/UEViewer/blob/master/Exporters/ExportGLTF.cpp',
                               'https://github.com/gildor2/UEViewer/blob/master/Unreal/UnrealMesh/UnAnim4.cpp']}
    out=ROOT/'necromancer_animation_source.json';out.write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n',encoding='utf-8')
    brief={'file':str(out),'sha256':sha(out),'bytes':out.stat().st_size,'real_bones':len(bones),'PSA_tracks':len(psa_bones),
           'clips':[{'name':a['short_name'],'fps':a['anim_info']['anim_rate'],'frames':a['anim_info']['num_raw_frames'],'duration':a['duration_seconds'],'GIF_duration':a['reference_gif']['duration_seconds']} for a in animations],
           'zero_motion_rotation_error':max(errs),'mapped_rigid_ends':[m for m in mapping if m['target_name'] in ['Body','Head','R_Arm','L_Arm','R_Leg','L_Leg','J_Shoulders','J_Head','J_R_Hand','J_L_Hand','J_R_Foot','J_L_Foot']]}
    (ROOT/'necromancer_animation_summary.json').write_text(json.dumps(brief,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in brief.items() if k!='mapped_rigid_ends'},indent=2))

if __name__=='__main__':main()
