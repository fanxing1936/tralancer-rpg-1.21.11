"""Retarget source PSA motion; native Blockbench owns final animation serialization."""
from pathlib import Path
import json, sys, math, warnings
import numpy as np
from scipy.spatial.transform import Rotation as R, Slerp

HERE=Path(__file__).resolve().parent
REF=Path(r'D:\agent\claude\github-create\tralancer-rpg-1.21.11\_tools\lucifer_ref')
sys.path.insert(0,str(REF.parent))
from display_mob import track_value
SRC=json.loads((HERE/'necromancer_animation_source.json').read_text(encoding='utf-8'))
BODY=json.loads((HERE.parent/'lucifer_original/body_for_blockbench.json').read_text(encoding='utf-8'))
BONES=BODY['bones']; N=len(BONES)
NAMES={b['name']:i for i,b in enumerate(BONES)}
REST_P=np.array([b['translation'] for b in BONES])
REST_R=np.array([R.from_quat(b['quaternion']).as_matrix() for b in BONES])
SB=SRC['bones']; MAP=SRC['target_mapping']
SWB=np.array([b['psaReferenceWorldJava'] for b in SB])
TWB=np.array([m['target_restWorldJava'] for m in MAP])
NATIVE=json.loads((REF/'separate/lucifer_verdant.bbmodel').read_text(encoding='utf-8'))
NE={e['name']:e for e in NATIVE['elements'] if e['type']=='armature_bone'}
REST_E=np.array([NE[b['name']]['rotation'] for b in BONES])

def world(lr,lp):
    wr=np.zeros_like(lr); wp=np.zeros_like(lp)
    for i,b in enumerate(BONES):
        p=b['parent']
        if p is None:wr[i]=lr[i];wp[i]=lp[i]
        else:wr[i]=wr[p]@lr[i];wp[i]=wp[p]+wr[p]@lp[i]
    return wr,wp

def source_clip(name):
    a=next(x for x in SRC['animations'] if x['short_name']==name)
    times=np.array(a['sample_times_seconds']); count=len(times)
    lr=np.zeros((count,N,3,3));lp=np.zeros((count,N,3))
    source_local={t['bone_index']:t for t in a['tracks_java']}
    for f in range(count):
        sr=[]
        for i,s in enumerate(SB):
            tr=source_local[i]; rot=R.from_quat(tr['quaternion_java_xyzw_normalized_continuous'][f]).as_matrix()
            p=s['parent_index']; sr.append(rot if p is None else sr[p]@rot)
        tw=[]
        for i,m in enumerate(MAP):
            si=m['source_index'];p=BONES[i]['parent'];sp=SB[si]['parent_index']
            wr=sr[si]@SWB[si,:3,:3].T@TWB[i,:3,:3]
            lr[f,i]=wr if p is None else tw[p].T@wr;tw.append(wr)
            delta=np.array(source_local[si]['position_java_px'][f])-np.array(SB[si]['psaReferenceLocalJava']['translation'])
            basis=np.eye(3) if p is None else TWB[p,:3,:3].T@SWB[sp,:3,:3]
            lp[f,i]=REST_P[i]+basis@delta
    return {'source':name,'times':times,'duration':a['duration_seconds'],'lr':lr,'lp':lp,
            'notes':['World rotation delta from original USkeleton reference; target bind offsets preserved with source local translation deltas.']}

def sample(c,t):
    t=float(np.clip(t,c['times'][0],c['times'][-1]));j=int(np.searchsorted(c['times'],t))
    if j==0:return c['lr'][0].copy(),c['lp'][0].copy()
    lo=j-1;hi=min(j,len(c['times'])-1);f=(t-c['times'][lo])/(c['times'][hi]-c['times'][lo]) if hi!=lo else 0
    return blend_pose(c['lr'][lo],c['lp'][lo],c['lr'][hi],c['lp'][hi],f)

def blend_pose(ar,ap,br,bp,f):
    dr=R.from_matrix(np.swapaxes(ar,-1,-2)@br).as_rotvec()
    return ar@R.from_rotvec(dr*f).as_matrix(),ap*(1-f)+bp*f

def set_hand(lr,lp,side,desired_world_r):
    hand=NAMES['J_'+side+'_Hand'];arm=NAMES['J_'+side+'_Arm']
    wr,wp=world(lr,lp)
    delta=desired_world_r@TWB[hand,:3,:3].T
    desired_p=wp[arm]+delta@(TWB[hand,:3,3]-TWB[arm,:3,3])
    lr[hand]=wr[arm].T@desired_world_r;lp[hand]=wr[arm].T@(desired_p-wp[arm])

def adapt_walk():
    c=source_clip('Walk');duration=c['duration']
    # Preserve every source upper-body sample and close the loop exactly.
    c['times']=np.append(c['times'],duration)
    c['lr']=np.concatenate([c['lr'],c['lr'][:1]]);c['lp']=np.concatenate([c['lp'],c['lp'][:1]])
    leg_indices=[2,3,4,5,6,7]
    leg_parts=[p for p in BODY['parts'] if p['name'] in ['R_Leg','L_Leg']]
    for f,t in enumerate(c['times']):
        lr,lp=c['lr'][f],c['lp'][f]
        lr[0]=REST_R[0];lp[0]=REST_P[0];lr[1]=REST_R[1];lp[1]=REST_P[1]
        lr[leg_indices]=REST_R[leg_indices];lp[leg_indices]=REST_P[leg_indices]
        swing=math.radians(25)*math.sin(2*math.pi*t/duration)
        lr[2]=R.from_rotvec([swing,0,0]).as_matrix()@REST_R[2]
        lr[5]=R.from_rotvec([-swing,0,0]).as_matrix()@REST_R[5]
        wr,wp=world(lr,lp);lowest=100
        for part in leg_parts:
            bi=part['weights'][next(iter(part['weights']))][0][0]
            v=np.array(list(part['vertices'].values()));pos=(v-TWB[bi,:3,3])@TWB[bi,:3,:3]@wr[bi].T+wp[bi]
            lowest=min(lowest,float(pos[:,1].min()))
        # Foot contact is an explicit Minecraft walking adaptation.
        lp[1]+=wr[0].T@np.array([0,-lowest,0])
    c['notes']+=['Hover lower body replaced by opposite 25-degree leg steps; source upper-body motion retained. Lowest leg vertex grounded each sampled frame; loop endpoint closes exactly.']
    return c

def adapt_attack():
    source=source_clip('BasicAttack');idle=source_clip('Idle');ir,ip=sample(idle,0)
    grip=json.loads((HERE/'weapon_grip_alignment.json').read_text(encoding='utf-8'))['semantic_points_world_after']
    tip_direction=np.array(grip['tip'])-np.array(grip['grip']);tip_direction/=np.linalg.norm(tip_direction)
    aim=R.align_vectors([[0,0,-1]],[tip_direction])[0].as_matrix()
    ts=np.unique(np.r_[np.linspace(0,.9,28),.06,.16,.34,.62,.9]);rs=[];ps=[]
    for t in ts:
        sr,sp=sample(source,.35+min(t,.65));lr,lp=blend_pose(ir,ip,sr,sp,.22*(1-t/.9))
        # Restrained source recoil, with a rigid arm aimed forward at the immediate damage frame.
        wr,wp=world(lr,lp);torso=wr[9]@TWB[9,:3,:3].T
        angle=float(np.interp(t,[0,.06,.16,.34,.62,.9],[88,88,78,47,67,82]))
        hand_r=torso@R.from_euler('X',angle,degrees=True).as_matrix()@TWB[15,:3,:3]
        set_hand(lr,lp,'R',hand_r)
        wr,wp=world(lr,lp)
        pitch=float(np.interp(t,[0,.06,.16,.34,.62,.9],[0,0,8,45,76,82]))
        weapon_world=R.from_euler('X',pitch,degrees=True).as_matrix()@aim@TWB[16,:3,:3]
        lr[16]=wr[15].T@weapon_world;lp[16]=REST_P[16]
        if t>.62:lr,lp=blend_pose(lr,lp,ir,ip,(t-.62)/(.9-.62))
        rs.append(lr);ps.append(lp)
    return {'source':'BasicAttack + explicitly adapted spear thrust','times':ts,'duration':.9,'lr':np.array(rs),'lp':np.array(ps),
        'notes':['Original BasicAttack torso recoil reduced to 22%; right arm and socket solved for a forward spear point, not a staff swing.',
        'Damage/maximum thrust at 0 seconds to match existing immediate skills; contact holds 0.06 s then withdraws and returns to idle. No combat code or damage values changed.']}

def crop_source(c,start):
    old=c;times=np.r_[start,c['times'][c['times']>start],c['duration']]
    poses=[sample(old,t) for t in times]
    return dict(c,times=times-start,duration=c['duration']-start,lr=np.array([p[0] for p in poses]),lp=np.array([p[1] for p in poses]),
        notes=c['notes']+[f'Source begins at {start} s (visually selected release pose) so the existing immediate damage event is at output 0 s; source anticipation was omitted, not moved into combat logic.'])

def legacy_clip(name):
    path=REF.parent/'leviathan_ref/leviathan.bbmodel';src=json.loads(path.read_text(encoding='utf-8'))
    anim=next(a for a in src['animations'] if a['name']=='animation.'+name)
    groups={g['name']:g for g in src['groups']};tracks={t['name']:t for t in anim['animators'].values() if 'name' in t}
    def curve(n,channel,t):
        keys=[k for k in tracks.get(n,{}).get('keyframes',[]) if k['channel']==channel]
        if not keys:return np.zeros(3)
        parsed=[(k['time'],[float(k['data_points'][0][a]) for a in 'xyz'],k.get('interpolation','linear')) for k in keys]
        return np.array(track_value(parsed,t,False))
    start=.65 if name=='cast' else 0;end=anim['length']
    times=np.unique(np.r_[np.linspace(start,end,int((end-start)*30)+1),[k['time'] for tr in tracks.values() for k in tr.get('keyframes',[]) if start<=k['time']<=end]])
    idle=source_clip('Idle');ir,ip=sample(idle,0);rs=[];ps=[]
    for t in times:
        lr=REST_R.copy();lp=REST_P.copy();lp[0]+=curve('root','position',t)
        body_r=R.from_euler('ZYX',curve('body','rotation',t)[::-1],degrees=True).as_matrix()
        wr,wp=world(lr,lp);lr[8]=wr[1].T@body_r@TWB[8,:3,:3]
        wr,wp=world(lr,lp);head_r=R.from_euler('ZYX',curve('head','rotation',t)[::-1],degrees=True).as_matrix()
        lr[18]=wr[9].T@body_r@head_r@TWB[18,:3,:3]
        for side,group in [('R','right_arm'),('L','left_arm')]:
            angle=np.array(groups[group].get('rotation',[0,0,0]))+curve(group,'rotation',t)
            arm_r=body_r@R.from_euler('ZYX',angle[::-1],degrees=True).as_matrix()
            set_hand(lr,lp,side,arm_r@TWB[NAMES['J_'+side+'_Hand'],:3,:3])
        blend_start=end-.25
        if t>blend_start:lr,lp=blend_pose(lr,lp,ir,ip,(t-blend_start)/(end-blend_start))
        rs.append(lr);ps.append(lp)
    notes=['Copied existing Leviathan root/body/head/arm numeric motion, including its Catmull-Rom interpolation sampled with the existing display_mob.track_value; world-basis retarget to original Mossy skeleton, no cape/gem geometry invented. Last 0.25 s blends to source Idle.']
    if name=='cast':notes.append('Original cast release at 0.65 s becomes output 0 s to match immediate magic skill; original 0.65–1.2 s follow-through retained.')
    return {'source':'Existing leviathan.bbmodel animation.'+name,'times':times-start,'duration':end-start,'lr':np.array(rs),'lp':np.array(ps),'notes':notes}

def export(clips):
    output=[]
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        for name,c in clips:
            times=c['times'];lr=c['lr'];lp=c['lp'];tracks=[]
            for bi,b in enumerate(BONES):
                # Intrinsic ZYX matches THREE.Euler(order=ZYX); storage is x,y,z.
                e=R.from_matrix(lr[:,bi]).as_euler('ZYX')[:,::-1]
                e=np.unwrap(e,axis=0)*180/math.pi
                # Pick the equivalent first representation closest to native rest.
                e-=360*np.round((e[0]-REST_E[bi])/360)
                rot=e-REST_E[bi];pos=lp[:,bi]-REST_P[bi]
                frames=[]
                for channel,values in [('rotation',rot),('position',pos)]:
                    if np.max(np.abs(values))<1e-10:continue
                    indices=[0] if np.max(np.abs(values-values[0]))<1e-10 else range(len(times))
                    for f in indices:
                        frames.append({'channel':channel,'time':float(times[f]),'interpolation':'linear',
                            'data_points':[dict(zip('xyz',[float(x) for x in values[f]]))]})
                if frames:tracks.append({'bone':b['name'],'keyframes':frames})
            output.append({'name':'animation.'+name,'loop':'loop' if name in ['idle','walk'] else 'once',
                'length':float(c['duration']),'snapping':100,'tracks':tracks,'source':c['source'],'notes':c['notes']})
    (HERE/'animation_payload.json').write_text(json.dumps(output,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    np.savez_compressed(HERE/'animation_pose_reference.npz',**{name+'__'+k:c[k] for name,c in clips for k in ['times','lr','lp']})
    print([(a['name'],a['length'],sum(len(t['keyframes']) for t in a['tracks'])) for a in output])
    return output

def main():
    idle=source_clip('Idle')
    idle['times']=np.append(idle['times'],idle['duration']);idle['lr']=np.concatenate([idle['lr'],idle['lr'][:1]]);idle['lp']=np.concatenate([idle['lp'],idle['lp'][:1]])
    clips=[('idle',idle),('walk',adapt_walk()),('attack',adapt_attack()),('strong',crop_source(source_clip('StrongAttack'),.8)),('cast',legacy_clip('cast')),('laugh',source_clip('Novelty')),('stun',source_clip('Stun')),('rise',legacy_clip('rise'))]
    for name,c in clips:
        for bone in ['J_L_Weapon','J_R_Weapon']:
            i=NAMES[bone];c['lp'][:,i]=REST_P[i]
        c['notes'].append('Source staff socket translations removed for the existing serpent spear attached directly to the hand socket; source rotations retained.')
    export(clips)

if __name__=='__main__':main()
