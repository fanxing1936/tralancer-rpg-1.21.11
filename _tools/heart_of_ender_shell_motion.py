#!/usr/bin/env python3
"""M3 shell motion evidence/fit. Writes only m3_motion/shell_*; never bbmodel.

Digitized 2-D limb axes are constraints, not recovered original 3-D geometry.
All rotations are numeric deltas to accepted_R2.bbmodel Euler rest angles.
"""
from pathlib import Path
import copy
import hashlib
import json
import math
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import label, find_objects
from scipy.optimize import least_squares, minimize_scalar, minimize
from scipy.spatial.transform import Rotation

HERE=Path(__file__).resolve().parent
REF=HERE/'heart_of_ender_ref'
OUT=REF/'m3_motion'
OUT.mkdir(exist_ok=True)
sys.path.insert(0,str(HERE))
import heart_of_ender_geometry_study as geom

# Rows: f at 25 Hz; each limb has endpoint x,y and distal/proximal junction x,y.
# Endpoint labels follow the M1 screen IDs, never an asserted anatomical name.
# Junctions are mostly obscured by smoke: these are explicitly inferred axes.
# Entries -1 visibility mean endpoint itself is occluded / not separately resolved.
MANUAL={
 0: [[50,80,117,146],[26,282,106,257],[30,390,128,342],[481,300,370,319],[317,446,295,383],[334,371,315,306]],
 5: [[51,68,122,139],[22,269,100,246],[18,369,119,330],[481,329,370,325],[311,442,293,383],[338,376,317,310]],
10: [[114,65,156,129],[38,250,80,235],[30,329,95,306],[443,393,357,356],[321,442,299,379],[322,313,309,286]],
15: [[170,60,192,121],[55,262,45,225],[110,250,165,264],[402,451,345,391],[322,446,298,381],[321,275,308,273]],
20: [[198,64,210,123],[137,224,158,242],[39,188,145,222],[354,477,337,437],[327,443,305,385],[322,264,309,272]],
25: [[200,81,213,139],[44,158,102,205],[118,164,161,226],[326,475,335,405],[335,431,306,380],[323,281,310,283]],
30: [[188,97,211,136],[53,161,89,207],[161,245,176,259],[358,457,349,422],[326,441,303,382],[331,302,315,285]],
35: [[166,78,206,129],[38,192,45,204],[91,215,139,278],[418,425,357,361],[324,424,302,369],[336,310,319,296]],
40: [[153,28,184,122],[64,228,127,240],[31,288,122,317],[461,367,362,337],[294,356,288,337],[318,370,310,310]],
45: [[133,28,174,121],[65,215,119,208],[19,345,132,316],[483,323,371,324],[289,352,283,336],[335,365,314,310]],
50: [[108,44,164,128],[67,207,118,211],[30,388,142,327],[481,297,370,317],[285,354,281,339],[339,372,316,312]],
55: [[93,69,155,132],[30,182,108,210],[32,365,140,314],[466,294,373,332],[287,354,282,338],[323,297,311,287]],
60: [[77,98,154,125],[27,180,58,195],[29,294,100,282],[445,329,364,357],[290,355,285,338],[308,250,303,269]],
65: [[64,104,146,127],[30,185,49,198],[41,255,81,259],[440,392,361,372],[292,354,286,340],[311,260,305,278]],
70: [[58,80,149,136],[33,219,52,231],[166,251,185,273],[438,430,355,372],[301,376,290,344],[318,288,309,286]],
75: [[86,91,156,142],[73,180,129,204],[67,191,126,258],[425,439,354,371],[323,400,300,357],[321,298,310,288]],
80: [[106,127,146,157],[38,114,57,136],[43,220,121,282],[425,431,354,361],[324,423,302,367],[325,264,311,276]],
85: [[125,157,157,178],[40,128,105,180],[22,250,134,294],[442,407,357,352],[324,439,301,374],[326,276,312,284]],
90: [[124,149,161,170],[34,124,54,146],[13,314,140,313],[472,362,367,337],[321,451,297,384],[331,285,314,290]],
95: [[53,86,126,145],[26,242,101,257],[20,372,135,330],[480,322,369,322],[321,449,297,384],[337,371,316,308]],
100:[[50,80,117,146],[26,282,106,257],[30,390,128,342],[481,300,370,319],[317,446,295,383],[334,371,315,306]],
}
IDS=['A','B','C','D','E','F']
HIDDEN={'A':{75,80,85,90}, 'B':{20,35,40,50,55,75}, 'C':{30},
        'D':set(), 'E':{40,45,50,55,60,65,70},
        'F':{10,15,20,25,30,35,55,60,65,70,75,80,85,90}}
# Back edge intersection at screen y=300: source-image manual guide only.
BODY_EDGE_X=[307,309,316,321,324,328,327,325,320,315,311,310,312,315,317,323,323,320,315,311,307]
BG=(55,60,70)


def rounded(v): return geom.rounded(v)
def write_json(name,data):
    (OUT/name).write_text(json.dumps(rounded(data),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def font(n=16):return ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',n)


def load_base():
    spec=json.loads((REF/'m2_geometry/geometry_spec.json').read_text(encoding='utf-8'))
    bb=OUT/'accepted_R2.bbmodel'
    doc=json.loads(bb.read_text(encoding='utf-8'))
    groups={g['name']:g for g in doc['groups']}
    for b in spec['bones']:
        b['rest_rotation']=groups[b['name']].get('rotation',[0,0,0])
        b['pivot']=groups[b['name']]['origin']
    # Geometry fits use the already accepted primitive dimensions, not newly edited cubes.
    return spec,doc,hashlib.sha256(bb.read_bytes()).hexdigest()


def world(spec,pose=None):
    pose=pose or {};result={}
    for b in spec['bones']:
        p=np.array(b['pivot'],float);state=pose.get(b['name'],{})
        R=geom.rxyz(np.array(b['rest_rotation'])+state.get('rotation',np.zeros(3)))
        T=np.eye(4);T[:3,:3]=R;T[:3,3]=p-R@p+state.get('position',np.zeros(3))
        result[b['name']]=result[b['parent']]@T if b['parent'] else T
    return result


def matrix_delta(spec,bone,world_rotation,parent_world):
    b=next(b for b in spec['bones'] if b['name']==bone)
    relative=parent_world[:3,:3].T@world_rotation
    value=np.array(geom.angles(relative))-np.array(b['rest_rotation'])
    return (value+180)%360-180


def minimal_alignment(old,new):
    a=np.array(old)/np.linalg.norm(old);b=np.array(new)/np.linalg.norm(new)
    v=np.cross(a,b);sn=np.linalg.norm(v);cs=np.clip(a@b,-1,1)
    if sn<1e-9:
        if cs>0:return np.eye(3)
        axis=np.cross(a,[1,0,0])
        if np.linalg.norm(axis)<1e-6:axis=np.cross(a,[0,0,1])
        return Rotation.from_rotvec(axis/np.linalg.norm(axis)*math.pi).as_matrix()
    return Rotation.from_rotvec(v/sn*math.atan2(sn,cs)).as_matrix()


def source_array(f):
    return np.array(Image.open(REF/'frames/MCD_Heart_of_Ender_Idle'/f'frame_{f:04d}.png').convert('RGBA'))


def bright_measure(a):
    mask=(a[:,:,3]>128)&(a[:,:,1]>170);mask[300:]=False;mask[:100]=False
    labs,_=label(mask);components=[]
    for i,sl in enumerate(find_objects(labs)):
        if sl is None:continue
        yy,xx=np.where(labs[sl]==i+1)
        if len(xx)>18:
            components.append(dict(area=len(xx),center=[float(xx.mean()+sl[1].start),float(yy.mean()+sl[0].start)],
                                   bbox=[sl[1].start,sl[0].start,sl[1].stop,sl[0].stop]))
    components.sort(key=lambda p:p['center'][1])
    eyes=components[:2]
    if len(eyes)!=2 or min(c['area'] for c in eyes)<80:raise ValueError('Eye extraction lost source frame')
    eyes.sort(key=lambda p:p['center'][0])
    yy,xx=np.where(mask)
    lower=yy>max(c['bbox'][3] for c in eyes)+4
    mouth=np.array([xx[lower].mean(),yy[lower].mean()])
    return dict(eyes=[c['center'] for c in eyes],eye_areas=[c['area'] for c in eyes],mouth_center=mouth.tolist())


def camera_fit(spec):
    rows={r['source_id']:r for r in spec['limb_fit']}
    render=np.array([rows[x]['tip_projected'] for x in IDS]);gif=np.array([MANUAL[0][i][:2] for i in range(6)])
    A=[];rhs=[]
    for a,b in zip(render,gif):
        A.extend([[a[0],1,0],[a[1],0,1]]);rhs.extend(b)
    s,ox,oy=np.linalg.lstsq(A,rhs,rcond=None)[0]
    P=np.array(spec['camera']['screen_basis_rows']);scale=spec['camera']['pixels_per_unit']*s
    offset=np.array(spec['camera']['offset_px'])*s+[ox,oy]
    target=P.T@np.r_[(np.array([250,250])-offset)/scale,0.]
    fitted=render*s+[ox,oy]
    return dict(projection='orthographic',canvas=[500,500],pixels_per_unit=scale,offset_px=offset,
                screen_basis_rows=P,position=(target+P[2]*80),target=target,orthographic_height=500/scale,
                render_to_gif_uniform_scale=s,render_to_gif_offset=[ox,oy],
                baseline_tip_rms_px=float(np.sqrt(np.mean(np.sum((fitted-gif)**2,axis=1)))),
                note='Fixed GIF camera fit from all six M1 endpoint correspondences; not animated camera.')


def project(point,cam):
    return (np.array(cam['screen_basis_rows'])@point)[:2]*cam['pixels_per_unit']+cam['offset_px']


def phase_guide(phase):
    lo=int(phase//5)*5;hi=min(lo+5,100);u=(phase-lo)/(hi-lo) if hi!=lo else 0
    return (1-u)*np.array(MANUAL[lo],float)+u*np.array(MANUAL[hi],float)


def repeated_frame_shift(reference,current,center):
    # Independent local alpha check at the same phase of every original cycle.
    # ±2 px allows raster changes without inventing new limb trajectories.
    x,y=np.rint(center).astype(int);rad=17
    x=max(rad+2,min(499-rad-2,x));y=max(rad+2,min(499-rad-2,y))
    src=(reference[y-rad:y+rad+1,x-rad:x+rad+1,3]>128).astype(float)
    candidates=[]
    for dy in range(-2,3):
        for dx in range(-2,3):
            patch=(current[y-rad+dy:y+rad+1+dy,x-rad+dx:x+rad+1+dx,3]>128).astype(float)
            loss=float(np.mean((patch-src)**2))+.00001*(dx*dx+dy*dy)
            candidates.append((loss,dx,dy,int(np.count_nonzero(patch!=src))))
    _,dx,dy,diff=min(candidates)
    return np.array([dx,dy]),diff


def face_local_point(spec,wm,cam,pixel,bone='shell_head',z=-10.8):
    # Solve exact point on the existing front plane, not a newly drawn UV.
    T=wm[bone];P=np.array(cam['screen_basis_rows']);scale=cam['pixels_per_unit']
    constant=project((T@np.array([0,0,z,1]))[:3],cam)
    M=scale*(P@T[:3,:3])[:2,:2]
    x,y=np.linalg.solve(M,np.array(pixel)-constant)
    return np.array([x,y,z])


def solve_projected_segment(root,target_xy,length,depth_sign,cam):
    P=np.array(cam['screen_basis_rows']);root_cam=P@root
    requested=(target_xy-np.array(cam['offset_px']))/cam['pixels_per_unit']
    v=requested-root_cam[:2];length2=np.linalg.norm(v);clamped=False
    if length2>length*.999:
        v*=length*.999/length2;clamped=True
    point=np.r_[root_cam[:2]+v,root_cam[2]+depth_sign*math.sqrt(max(0,length*length-v@v))]
    world_point=P.T@point
    return world_point,float(np.linalg.norm(project(world_point,cam)-target_xy)),clamped


def feasible_elbow(root_xy,tip_xy,guide_xy,lengths,cam):
    """Extend a visible distal-axis guide into the smoke, within both limb lengths.

    A short dark sliver is not the whole distal cuboid. Its inner end cannot be
    asserted to be the elbow. Keep its observed axis where the two circles allow.
    """
    R=np.array(root_xy);T=np.array(tip_xy);G=np.array(guide_xy)
    r1,r2=np.array(lengths)*cam['pixels_per_unit']*.999
    total=np.linalg.norm(T-R);tip_adjustment=0.
    if total>r1+r2-.01:
        newT=R+(T-R)*(r1+r2-.01)/total;tip_adjustment=float(np.linalg.norm(newT-T));T=newT
    ray=G-T;initial=np.linalg.norm(ray)
    if initial<1e-6:ray=R-T;initial=np.linalg.norm(ray)
    ray/=initial
    a=float((T-R)@ray);b=float(np.sum((T-R)**2)-r1*r1);disc=a*a-b
    ray_possible=False
    if disc>=0:
        lo=max(0.,-a-math.sqrt(disc));hi=min(r2,-a+math.sqrt(disc))
        if lo<=hi:
            E=T+ray*np.clip(initial,lo,hi);ray_possible=True
    if not ray_possible:
        init=R+(T-R)*r1/(r1+r2)
        constraints=[{'type':'ineq','fun':lambda e:r1*r1-np.sum((e-R)**2)},
                     {'type':'ineq','fun':lambda e:r2*r2-np.sum((e-T)**2)}]
        fit=minimize(lambda e:np.sum((e-G)**2),init,method='SLSQP',constraints=constraints,
                     options={'maxiter':100,'ftol':1e-8})
        E=fit.x
    axis=E-T
    axis_error=math.degrees(math.acos(np.clip((axis@ray)/max(1e-9,np.linalg.norm(axis)),-1,1)))
    return E,T,dict(junction_guide_extension_px=float(np.linalg.norm(E-G)),
                    distal_axis_residual_degrees=axis_error,axis_preserved=ray_possible,
                    total_reach_tip_adjustment_px=tip_adjustment)


def idle_fit(spec,cam):
    base=world(spec);bones={b['name']:b for b in spec['bones']}
    rows={r['source_id']:r for r in spec['limb_fit']}
    source=[source_array(f) for f in range(400)]
    light=[bright_measure(a) for a in source]
    eye_local=[face_local_point(spec,base,cam,p) for p in light[0]['eyes']]
    mouth_local=face_local_point(spec,base,cam,light[0]['mouth_center'],'shell_jaw')
    source0=np.array(MANUAL[0],float)
    frames=list(range(0,400,5))+[399]
    poses=[];evidence=[];prev_head=np.zeros(3)
    for f in frames:
        phase=f%100;guide=phase_guide(phase);pose={}
        # Torso-edge intersection is a low-confidence 2-D cue, not original root animation.
        edge_x=float(np.interp(phase,np.arange(0,101,5),BODY_EDGE_X))
        marker=np.array([-4.5,15,8,1.]);baseline_x=project((base['shell_root']@marker)[:3],cam)[0]
        target_x=baseline_x+edge_x-BODY_EDGE_X[0]
        def root_loss(z):
            w=world(spec,{'shell_root':{'rotation':[0,0,z]}})
            return (project((w['shell_root']@marker)[:3],cam)[0]-target_x)**2+.015*z*z
        root_z=minimize_scalar(root_loss,bounds=(-18,18),method='bounded').x
        if f==0:root_z=0.
        pose['shell_root']={'rotation':np.array([0.,0.,root_z]),'position':np.zeros(3)}
        target_eyes=np.array(light[f]['eyes'])
        def head_residual(delta):
            trial=copy.deepcopy(pose);trial['shell_head']={'rotation':delta};w=world(spec,trial)
            p=np.array([project((w['shell_head']@np.r_[v,1])[:3],cam) for v in eye_local])
            return np.r_[(p-target_eyes).ravel(),.018*delta,.007*(delta-prev_head)]
        head=least_squares(head_residual,prev_head,bounds=(-45,45),max_nfev=100).x
        if f==0:head=np.zeros(3)
        pose['shell_head']={'rotation':head};prev_head=head
        def jaw_loss(angle):
            trial=copy.deepcopy(pose);trial['shell_jaw']={'rotation':[angle,0,0]};w=world(spec,trial)
            p=project((w['shell_jaw']@np.r_[mouth_local,1])[:3],cam)
            target=np.array(light[f]['mouth_center'])
            return float(np.sum((p-target)**2)+.12*angle*angle)
        jaw=minimize_scalar(jaw_loss,bounds=(-24,3),method='bounded').x
        if f==0:jaw=0.
        pose['shell_jaw']={'rotation':np.array([jaw,0.,0.])}
        pose['shell_body']={'rotation':np.zeros(3)}
        wroot=world(spec,pose)['shell_root'];records=[]
        for i,ident in enumerate(IDS):
            row=rows[ident];prox=row['bone_prefix']+'_proximal';dist=row['bone_prefix']+'_distal'
            bprox=bones[prox];bdist=bones[dist]
            old_root=(base['shell_root']@np.r_[bprox['pivot'],1])[:3]
            old_elbow=(base[prox]@np.r_[bdist['pivot'],1])[:3]
            c=next(c for c in spec['cubes'] if c['bone']==dist)
            endpoint=np.array([(c['from'][0]+c['to'][0])/2,c['from'][1],(c['from'][2]+c['to'][2])/2,1])
            old_tip=(base[dist]@endpoint)[:3]
            visibility='occluded_inferred' if int(round(phase/5)*5)%100 in HIDDEN[ident] else 'visible_tip'
            shift,differing=repeated_frame_shift(source[phase],source[f],guide[i,:2])
            target_tip=project(old_tip,cam)+(guide[i,:2]-source0[i,:2])+shift
            target_elbow=project(old_elbow,cam)+(guide[i,2:]-source0[i,2:])+shift
            root=(wroot@np.r_[bprox['pivot'],1])[:3]
            feasible_joint,feasible_tip,axis_info=feasible_elbow(project(root,cam),target_tip,target_elbow,row['segment_lengths'],cam)
            elbow,err1,clamp1=solve_projected_segment(root,feasible_joint,row['segment_lengths'][0],row['depth_signs'][0],cam)
            tip,err2,clamp2=solve_projected_segment(elbow,feasible_tip,row['segment_lengths'][1],row['depth_signs'][1],cam)
            err1=float(np.linalg.norm(project(elbow,cam)-feasible_joint))
            err2=float(np.linalg.norm(project(tip,cam)-target_tip))
            Rp=minimal_alignment(old_elbow-old_root,elbow-root)@base[prox][:3,:3]
            dp=matrix_delta(spec,prox,Rp,wroot);pose[prox]={'rotation':dp}
            wp=world(spec,pose)[prox]
            Rd=minimal_alignment(old_tip-old_elbow,tip-elbow)@base[dist][:3,:3]
            dd=matrix_delta(spec,dist,Rd,wp);pose[dist]={'rotation':dd}
            if f==0:pose[prox]['rotation']=np.zeros(3);pose[dist]['rotation']=np.zeros(3)
            records.append(dict(id=ident,visibility=visibility,source_endpoint=guide[i,:2]+shift,
                source_axis_inner_guide=guide[i,2:]+shift,junction_evidence='axis direction guide, NOT a measured elbow; extend into smoke within fixed lengths',
                endpoint_uncertainty_px=6 if visibility=='visible_tip' else None,
                requested_model_tip_px=target_tip,requested_model_junction_px=target_elbow,
                feasible_junction_px=feasible_joint,fitted_tip_px=project(tip,cam),fitted_junction_px=project(elbow,cam),
                tip_constraint_residual_px=err2,junction_constraint_residual_px=err1,
                fixed_length_clamped=clamp1 or clamp2,axis_fit=axis_info,same_phase_alpha_patch_difference_pixels=differing,
                independent_cycle_patch_shift_px=shift,depth_status='inferred; static depth branch retained'))
        w=world(spec,pose)
        actual_eyes=np.array([project((w['shell_head']@np.r_[p,1])[:3],cam) for p in eye_local])
        evidence.append(dict(id=f'idle_f{f:03d}',time=f/25,source_frame=f,
            source_path=f'frames/MCD_Heart_of_Ender_Idle/frame_{f:04d}.png',
            eyes=light[f]['eyes'],mouth_center=light[f]['mouth_center'],
            eye_rms_px=float(np.sqrt(np.mean(np.sum((actual_eyes-target_eyes)**2,axis=1)))),
            torso_edge_screen_y=300,torso_edge_x_guide=edge_x,
            torso_rotation_status='inferred fit to hand-digitized back-edge intersection; depth unresolved',
            jaw_status='inferred pitch from bright-mouth centroid; glow cannot prove exact jaw geometry',limbs=records))
        poses.append((f/25,pose,f'idle_f{f:03d}'))
    poses.append((16.,copy.deepcopy(poses[0][1]),'idle_loop_boundary'))
    return poses,evidence,light


def pose_tracks(poses):
    channels=sorted({(bone,ch) for _,p,_ in poses for bone,v in p.items() for ch in v})
    tracks=[]
    for bone,ch in channels:
        values=np.array([p.get(bone,{}).get(ch,[0,0,0]) for _,p,_ in poses],float)
        if ch=='rotation':
            values=np.degrees(np.unwrap(np.radians(values),axis=0))
            # Do not silently erase an actual winding; final loop checks inspect matrices.
        keys=[dict(time=t,value=v,interpolation='linear',evidence_id=eid) for (t,_,eid),v in zip(poses,values)]
        tracks.append(dict(bone=bone,channel=ch,keyframes=keys))
    return tracks


def make_clip(name,length,loop,evidence,poses,references,notes):
    return dict(name=name,length=length,loop=loop,evidence=evidence,tracks=pose_tracks(poses),
                key_poses=[dict(time=t,evidence_id=eid) for t,_,eid in poses],source_references=references,notes=notes)


def keypose(spec,root=(0,0,0),head=(0,0,0),jaw=0,root_y=0,limb_flex=0):
    pose={'shell_root':{'rotation':np.array(root,float),'position':np.array([0,root_y,0],float)},
          'shell_body':{'rotation':np.zeros(3)},'shell_head':{'rotation':np.array(head,float)},
          'shell_jaw':{'rotation':np.array([jaw,0,0],float)}}
    for r in spec['limb_fit']:
        sign=1 if r['source_id'] in ['A','B','C'] else -1
        pose[r['bone_prefix']+'_proximal']={'rotation':np.array([limb_flex*.12,0,sign*limb_flex])}
        pose[r['bone_prefix']+'_distal']={'rotation':np.array([-limb_flex*.3,0,-sign*limb_flex*.5])}
    return pose


def two_bone_target(spec,pose,row,target,base,pole):
    bones={b['name']:b for b in spec['bones']};prox=row['bone_prefix']+'_proximal';dist=row['bone_prefix']+'_distal'
    bprox=bones[prox];bdist=bones[dist];wr=world(spec,pose)['shell_root']
    root=(wr@np.r_[bprox['pivot'],1])[:3];v=np.array(target)-root;distance=np.linalg.norm(v)
    L1,L2=row['segment_lengths'];distance=min(distance,L1+L2-.01);direction=v/np.linalg.norm(v)
    end=root+direction*distance;a=(L1*L1-L2*L2+distance*distance)/(2*distance)
    bend=np.array(pole)-direction*(np.array(pole)@direction);bend/=np.linalg.norm(bend)
    elbow=root+direction*a+bend*math.sqrt(max(0,L1*L1-a*a))
    old_root=(base['shell_root']@np.r_[bprox['pivot'],1])[:3]
    old_elbow=(base[prox]@np.r_[bdist['pivot'],1])[:3]
    c=next(c for c in spec['cubes'] if c['bone']==dist)
    end_local=np.array([(c['from'][0]+c['to'][0])/2,c['from'][1],(c['from'][2]+c['to'][2])/2,1])
    old_end=(base[dist]@end_local)[:3]
    Rp=minimal_alignment(old_elbow-old_root,elbow-root)@base[prox][:3,:3]
    pose[prox]={'rotation':matrix_delta(spec,prox,Rp,wr)}
    wp=world(spec,pose)[prox]
    Rd=minimal_alignment(old_end-old_elbow,end-elbow)@base[dist][:3,:3]
    pose[dist]={'rotation':matrix_delta(spec,dist,Rd,wp)}
    w=world(spec,pose)[dist]
    cap=[(w@np.array([x,c['from'][1],z,1]))[:3] for x in [c['from'][0],c['to'][0]] for z in [c['from'][2],c['to'][2]]]
    return min(p[1] for p in cap),float(np.linalg.norm(end-target))


def inferred_clips(spec,ground,buried):
    base=world(spec);clips=[];walk_poses=[];contact=[]
    for tick in range(33):
        t=tick*.25;p=keypose(spec,root=(-55,0,12),head=(62,0,-6))
        wr=world(spec,p)['shell_root']
        for row in spec['limb_fit']:
            ident=row['source_id'];group=0 if ident in ['A','C','E'] else 1
            u=(t-group)%2
            # Digitally designed six-contact crawl, not source motion capture.
            if u<=1.2:fore=5-10*u/1.2;lift=0
            elif u<=1.6:fore=-5+5*(u-1.2)/.4;lift=6*(u-1.2)/.4
            else:fore=5*(u-1.6)/.4;lift=6*(2-u)/.4
            b=next(b for b in spec['bones'] if b['name']==row['bone_prefix']+'_proximal')
            root=(wr@np.r_[b['pivot'],1])[:3];sign=1 if b['pivot'][0]>0 else -1
            target=np.array([root[0]+sign*12,ground+2.5+lift,root[2]-fore])
            err=0;low=ground
            for _ in range(5):
                low,err=two_bone_target(spec,p,row,target,base,[sign,.45,0])
                target[1]+=ground+lift-low
            if abs(u)<1e-9:
                contact.append(dict(time=t,limb=ident,lowest_cap_y=low,ground_y=ground,gap=low-ground,target_clamp_error=err))
        walk_poses.append((t,p,f'walk_inferred_{t:.2f}'))
    clips.append(make_clip('walk',8,True,'推断',walk_poses,['Heart_of_ender_crawling_with_decal_trail.png','Wiki: Crawl'],
        ['No original walking animation used. Alternating A/C/E and B/D/F tripod gait is an explicit design inference.',
         'Contact events at integers 0..7 seconds; actual cap minima checked against fixed ground.',
         'Anxious inner clip belongs in this same 8-second animation; shell alone here.']))
    sequence=[
      ('mortar',4,[(0,{}),(.4,dict(root=(4,0,0),head=(5,0,0),limb_flex=7)),(.8,dict(root=(8,0,0),head=(24,0,0),limb_flex=14)),
        (1.2,dict(root=(9,0,0),head=(32,0,0),jaw=-26,limb_flex=12)),(2.0,dict(root=(9,0,0),head=(30,0,0),jaw=-23,limb_flex=12)),
        (2.8,dict(root=(8,0,0),head=(28,0,0),jaw=-24,limb_flex=10)),(3.2,dict(root=(4,0,0),head=(12,0,0),jaw=-7,limb_flex=5)),(4,{})],
        ['Wiki: Mortar barrage','Minecraft-dungeons-heart-of-ender.jpg'],
        ['4-second timing inferred. Open emission hold 1.2..2.8s; thirteen projectiles are page text, not thirteen invented jaw pulses.']),
      ('cross_beam',4,[(0,{}),(.5,dict(root=(0,0,6),root_y=3,limb_flex=-10)),(1,dict(root=(0,0,12),root_y=7,head=(6,0,-6),limb_flex=-18)),
        (2,dict(root=(0,0,12),root_y=7,head=(6,0,-6),limb_flex=-18)),(3,dict(root=(0,0,12),root_y=7,head=(6,0,-6),limb_flex=-18)),
        (3.5,dict(root=(0,0,6),root_y=3,limb_flex=-8)),(4,{})],
        ['Heart_of_Ender_prepare_to_shoot_beams.png','Heart_Of_Ender_laser.jpg','Wiki: Cross beam'],
        ['Shell is inferred; Fourside 2-second source maps to t1..3.',
         'Page clockwise rotation describes beams; no unsupported full-shell spin is invented. Beam effects are outside scope.']),
      ('sink',2,[(0,{}),(.4,dict(limb_flex=16)),(.8,dict(root_y=buried*.2,limb_flex=20)),(1.3,dict(root_y=buried*.7,limb_flex=20)),
        (1.7,dict(root_y=buried,limb_flex=12)),(2,dict(root_y=buried,limb_flex=12))],
        ['Wiki: Arch-Visages','Heart_of_Ender_in_game.png'],['2-second timing inferred; only root position descends. Fixed world ground is actual rest minimum, never image cropping.']),
      ('rise',2.4,[(0,dict(root_y=buried,limb_flex=12)),(.2,dict(root_y=buried,limb_flex=12)),(.8,dict(root_y=buried*.6,limb_flex=18)),
        (1.4,dict(root_y=buried*.18,limb_flex=12)),(1.9,dict(limb_flex=5)),(2.4,{})],
        ['Wiki: Arch-Visages','Heart_of_Ender_in_game.png'],['2.4-second rise is inferred and intentionally not claimed to be an original reverse-sink animation.']),
      ('death',4,[(0,{}),(.6,dict(head=(-7,0,4),jaw=-5,limb_flex=8)),(1.2,dict(head=(-16,0,7),jaw=-9,limb_flex=16)),
        (2.2,dict(head=(-23,0,10),jaw=-13,limb_flex=23)),(3.2,dict(head=(-28,0,12),jaw=-15,limb_flex=27)),
        (3.8,dict(head=(-28,0,12),jaw=-15,limb_flex=27)),(4,dict(head=(-28,0,12),jaw=-15,limb_flex=27))],
        ['Hero_kills_Heart_of_Ender_Arch-Illager_disappear.jpg','Wiki: death caption'],
        ['Entire shell sequence inferred from final-state evidence; no captured death motion exists.',
         'Root stays in place, so the inner model can disappear last by its own downward position at3.2..3.8s. No scale, breakup or particles.'])]
    for name,duration,keys,refs,notes in sequence:
        poses=[(t,keypose(spec,**kw),f'{name}_inferred_{t:.2f}') for t,kw in keys]
        clips.append(make_clip(name,duration,False,'推断',poses,refs,notes))
    return clips,contact


def render_pose(spec,pose,cam):
    w=world(spec,pose);P=np.array(cam['screen_basis_rows']);polys=[]
    for c in spec['cubes']:
        if c['bone'].startswith('inner'):continue
        pts=geom.vertices(c,w[c['bone']]);q=pts@P.T
        for fi,face in enumerate(geom.FACES):
            poly=q[list(face)];polys.append((poly[:,2].mean(),poly[:,:2],c['bone'],fi))
    im=Image.new('RGB',(500,500),BG);d=ImageDraw.Draw(im)
    for depth,xy,name,fi in sorted(polys,key=lambda x:x[0]):
        color=(105,127,149) if name=='shell_head' else (77,105,127) if name=='shell_jaw' else (73,94,105) if name=='shell_body' else (92,130,120) if 'left' in name else (130,102,121)
        shade=[.7,.85,.9,1,.75,.98][fi];color=tuple(int(v*shade) for v in color)
        d.polygon([tuple(p) for p in xy*cam['pixels_per_unit']+cam['offset_px']],fill=color,outline=(175,183,195))
    return im


def preview(spec,cam,poses,evidence):
    selected=[0,20,45,65,80,100,165,265,365,399]
    table={round(t*25):(t,p,e) for t,p,e in poses}
    for page in range(2):
        board=Image.new('RGB',(2000,1590),BG);d=ImageDraw.Draw(board)
        for n,f in enumerate(selected[page*5:page*5+5]):
            t,p,eid=table[f];a=Image.fromarray(source_array(f));src=Image.new('RGBA',(500,500),BG+(255,));src.alpha_composite(a)
            x=n%2*1000;y=n//2*530
            board.paste(src.convert('RGB'),(x,y+30));board.paste(render_pose(spec,p,cam),(x+500,y+30))
            d.text((x+8,y+4),f'idle f{f:03d} / {t:.2f}s | source / numeric shell fit',font=font(16),fill='white')
        board.save(OUT/f'shell_idle_fit_{page+1:02d}.png')


def main():
    spec,doc,sha=load_base();cam=camera_fit(spec);base=world(spec)
    verts=np.vstack([geom.vertices(c,base[c['bone']]) for c in spec['cubes']])
    ground=float(verts[:,1].min());max_y=float(verts[:,1].max());buried=ground-max_y-4
    poses,evidence,all_light=idle_fit(spec,cam)
    idle=make_clip('idle',16,True,'有动图',poses,['MCD_Heart_of_Ender_Idle.gif'],
        ['81 samples from the actual 16-second source plus a 16.0s closing key, 82 key times total. Linear interpolation only; no sinusoid.',
         'Visible 2D endpoints and eyes constrain motion. Hidden depth, smoked-out junctions, torso rotation and jaw extraction remain inference.',
         'Some E/F endpoints are occluded. Those samples are continuity guides, not measured recovered joints.',
         'Independent same-phase source alpha patches are checked in all four cycles; this does not make depth observable.',
         'Inner Docile is supplied separately, three 5.333333s cycles at 90% source speed.'])
    others,contact=inferred_clips(spec,ground,buried)
    data=dict(stage='M3 draft numeric motion awaiting native Blockbench comparison',base_bbmodel_sha256=sha,
        base_bbmodel='m3_motion/accepted_R2.bbmodel',
        rotation_semantics='Numeric XYZ Euler deltas added to accepted R2 rest; position added before local pivot rotation; no scale',
        expected_part_count=21,camera=cam,ground_y=ground,rest_max_y=max_y,fully_buried_root_position=[0,buried,0],
        clips=[idle,others[0]]+others[1:],measurements_file='shell_measurements.json',
        cue_timing=dict(walk_steps=list(range(8)),mortar_open=[1.2,2.8],cross_fourside=[1,3],sink_invisible_from=1.7,rise_recovered=1.9,death_inner_disappear=[3.2,3.8]),
        limitations=['No original geometry or skeleton has been extracted.',
            'Motion is constrained from 2D references; endpoint-fit errors do not measure full visual fidelity.',
            'Limb ID correspondence through complete occlusion is uncertain and explicitly labeled.',
            'No Minecraft in-game animation/render validation, build, runtime integration or gameplay is included.'])
    write_json('shell_motion.json',data)
    write_json('shell_measurements.json',dict(source_fps=25,manual_phase_guides=MANUAL,visibility_occlusions={k:sorted(v) for k,v in HIDDEN.items()},
        records=evidence,all_400_frame_light_measurements=all_light,contact_checks=contact))
    preview(spec,cam,poses,evidence)
    stats=dict(samples=len(poses),eye_max_rms=max(e['eye_rms_px'] for e in evidence),
        limb_tip_max_residual=max(r['tip_constraint_residual_px'] for e in evidence for r in e['limbs']),
        limb_clamped_samples=sum(r['fixed_length_clamped'] for e in evidence for r in e['limbs']),
        max_contact_gap=max(abs(r['gap']) for r in contact),ground_y=ground,camera=cam)
    write_json('shell_fit_stats.json',stats)
    print(json.dumps(rounded(stats),ensure_ascii=False))


def key_pose_from_clip(clip,time):
    p={}
    for tr in clip['tracks']:
        keys=tr['keyframes'];times=[k['time'] for k in keys]
        v=[float(np.interp(time,times,[k['value'][i] for k in keys])) for i in range(3)]
        p.setdefault(tr['bone'],{})[tr['channel']]=v
    return p


def b_options():
    """One unaccepted frame alternative; does not regenerate any frozen tracks."""
    spec,_,sha=load_base();base=world(spec)
    data=json.loads((OUT/'shell_motion.json').read_text(encoding='utf-8'))
    measurements=json.loads((OUT/'shell_measurements.json').read_text(encoding='utf-8'))
    cam=data['camera'];time=.6;pose=key_pose_from_clip(data['clips'][0],time)
    record=next(e for e in measurements['records'] if e['source_frame']==15)
    measured=next(r for r in record['limbs'] if r['id']=='B')
    row=next(r for r in spec['limb_fit'] if r['source_id']=='B')
    prox=row['bone_prefix']+'_proximal';dist=row['bone_prefix']+'_distal'
    bprox=next(b for b in spec['bones'] if b['name']==prox)
    bdist=next(b for b in spec['bones'] if b['name']==dist)
    c=next(c for c in spec['cubes'] if c['bone']==dist)
    endpoint=np.array([(c['from'][0]+c['to'][0])/2,c['from'][1],(c['from'][2]+c['to'][2])/2,1])
    w=world(spec,pose);root=(w['shell_root']@np.r_[bprox['pivot'],1])[:3]
    requested_tip=np.array(measured['requested_model_tip_px'])
    guide=np.array(measured['requested_model_junction_px'])
    projected_axis=requested_tip-guide
    elbow,_,_=solve_projected_segment(root,guide,row['segment_lengths'][0],row['depth_signs'][0],cam)
    # Hold the visible short distal-axis projection exactly. The unattainable
    # source elbow is moved to the nearest possible proximal reach instead.
    direction_tip=project(elbow,cam)+projected_axis
    tip,_,_=solve_projected_segment(elbow,direction_tip,row['segment_lengths'][1],row['depth_signs'][1],cam)
    old_root=(base['shell_root']@np.r_[bprox['pivot'],1])[:3]
    old_elbow=(base[prox]@np.r_[bdist['pivot'],1])[:3]
    old_tip=(base[dist]@endpoint)[:3]
    candidate=copy.deepcopy(pose)
    Rp=minimal_alignment(old_elbow-old_root,elbow-root)@base[prox][:3,:3]
    candidate[prox]['rotation']=matrix_delta(spec,prox,Rp,w['shell_root'])
    wp=world(spec,candidate)[prox]
    Rd=minimal_alignment(old_tip-old_elbow,tip-elbow)@base[dist][:3,:3]
    candidate[dist]['rotation']=matrix_delta(spec,dist,Rd,wp)
    options=[]
    for ident,label_,p in [('endpoint_priority','当前：端点优先，短竖轴无法同时匹配',pose),
                          ('visible_axis_priority','候选：可见短竖轴优先，端点会向身体移动',candidate)]:
        wm=world(spec,p);actual_tip=project((wm[dist]@endpoint)[:3],cam)
        actual_elbow=project((wm[prox]@np.r_[bdist['pivot'],1])[:3],cam)
        a=actual_tip-actual_elbow;b=requested_tip-guide
        error=math.degrees(math.acos(np.clip((a@b)/(np.linalg.norm(a)*np.linalg.norm(b)),-1,1)))
        options.append(dict(id=ident,label=label_,animation_rotation_replacements={prox:p[prox]['rotation'],dist:p[dist]['rotation']},
            projected_tip_px=actual_tip,projected_elbow_px=actual_elbow,
            calibrated_tip_error_px=float(np.linalg.norm(actual_tip-requested_tip)),
            raw_source_tip_error_px=float(np.linalg.norm(actual_tip-np.array(measured['source_endpoint']))),
            distal_axis_error_degrees=error))
    result=dict(stage='Unaccepted single-frame B-axis comparison; NOT added to the seven clips',
        base_bbmodel_sha256=sha,clip='idle',time=time,source_frame=15,
        source_path='frames/MCD_Heart_of_Ender_Idle/frame_0015.png',
        convention='Replace only the two animation rotation delta values at this pose; rest/root/cubes/other tracks stay unchanged.',
        camera=cam,source_endpoint=measured['source_endpoint'],source_axis_inner_guide=measured['source_axis_inner_guide'],
        source_ambiguity='The L-shaped isolated black fragment is visible, but its short vertical arm and connection through smoke do not establish original joint ownership.',
        options=options,
        conclusion='The fixed accepted root and bone lengths cannot reproduce this interpreted short vertical axis and the distant endpoint together. User review is required before changing any geometry hypothesis.')
    write_json('shell_b_f015_options.json',result)
    source=Image.new('RGBA',(500,500),BG+(255,));source.alpha_composite(Image.fromarray(source_array(15)))
    board=Image.new('RGB',(1500,540),BG);board.paste(source.convert('RGB'),(0,40))
    board.paste(render_pose(spec,pose,cam),(500,40));board.paste(render_pose(spec,candidate,cam),(1000,40))
    draw=ImageDraw.Draw(board)
    for x,label_ in [(10,'原图 f015 / 0.60 秒'),(510,'当前：端点优先'),(1010,'候选：可见短竖轴优先')]:
        draw.text((x,8),label_,font=font(19),fill='white')
    board.save(OUT/'shell_b_f015_options.png')
    print(json.dumps(rounded(result),ensure_ascii=False))


def review_frozen():
    """Visual/20 Hz checks of frozen numeric tracks; no animation JSON mutation."""
    spec,_,sha=load_base();data=json.loads((OUT/'shell_motion.json').read_text(encoding='utf-8'))
    checks=[]
    for clip in data['clips']:
        start=world(spec,key_pose_from_clip(clip,0));end=world(spec,key_pose_from_clip(clip,clip['length']))
        loop_error=max(float(np.max(np.abs(start[b]-end[b]))) for b in start)
        lowest=(1e9,None,None);highest=(-1e9,None,None)
        for t in np.arange(0,clip['length']+.0001,.05):
            w=world(spec,key_pose_from_clip(clip,float(t)))
            for c in spec['cubes']:
                if c['bone'].startswith('inner'):continue
                y=geom.vertices(c,w[c['bone']])[:,1]
                if y.min()<lowest[0]:lowest=(float(y.min()),float(t),c['bone'])
                if y.max()>highest[0]:highest=(float(y.max()),float(t),c['bone'])
        checks.append(dict(clip=clip['name'],loop=clip['loop'],start_end_matrix_max_abs=loop_error,
                           lowest_shell_vertex_y=lowest[0],lowest_at=lowest[1],lowest_bone=lowest[2],
                           highest_shell_vertex_y=highest[0],ground_y=data['ground_y']))
    idle=data['clips'][0];keys=[0,.8,2.6,3.2]
    poses=[key_pose_from_clip(idle,t) for t in keys]
    sheet=Image.new('RGB',(2000,2160),BG);d=ImageDraw.Draw(sheet)
    for col,(name,yaw,elev) in enumerate([('front',0,0),('right',90,0),('back',180,0),('reference',-45,25)]):
        P=geom.camera(yaw,elev)
        allpts=[]
        for p in poses:
            w=world(spec,p)
            allpts.extend(geom.vertices(c,w[c['bone']])@P.T for c in spec['cubes'] if not c['bone'].startswith('inner'))
        q=np.vstack(allpts);lo=q[:,:2].min(0);hi=q[:,:2].max(0)
        scale=min(450/(hi[0]-lo[0]),450/(hi[1]-lo[1]));offset=np.array([250,250])-(lo+hi)/2*scale
        cam=dict(screen_basis_rows=P,pixels_per_unit=scale,offset_px=offset)
        for row,(t,p) in enumerate(zip(keys,poses)):
            sheet.paste(render_pose(spec,p,cam),(col*500,row*540+40))
            d.text((col*500+8,row*540+10),f'idle {t:.2f}s / {name} / geometry only',font=font(15),fill='white')
    sheet.save(OUT/'shell_four_view_study.png')
    write_json('shell_checks.json',dict(base_bbmodel_sha256=sha,sample_hz=20,
        note='Numeric geometry checks only; native BB/model-vs-source visual validation remains separate. Inner tracks are not included here.',
        clips=checks))
    print(json.dumps(rounded(checks),ensure_ascii=False))


def cross_candidates():
    """Independent source-constrained raised-arm proposals; never touch main clips."""
    spec,_,sha=load_base();base=world(spec)
    # Source screen roots are fade-out zones, not asserted real joint centers.
    axes={
      'A':[[1045,340],[898,194],[805,65]],
      'F':[[1141,344],[1282,213],[1384,90]],
      'B':[[1050,432],[905,346],[786,272]],
      'E':[[1162,407],[1298,296],[1392,208]],
      'C':[[1045,511],[929,450],[787,363]],
      'D':[[1156,539],[1317,431],[1452,374]],
    }
    # Nearly frontal source camera. All depth branches remain inferred.
    P=geom.camera(0,25);ppu=17.25
    candidate=keypose(spec,root=(0,0,12),head=(0,0,0),jaw=-18,root_y=7)
    records=[]
    for row in spec['limb_fit']:
        ident=row['source_id'];points=np.array(axes[ident],float)
        vectors=[points[1]-points[0],points[2]-points[1]]
        dirs=[]
        for index,(v,L,sign) in enumerate(zip(vectors,row['segment_lengths'],[-1,1])):
            screen=v/(ppu*L);p2=float(screen@screen)
            if p2>=.98:screen*=math.sqrt(.98/p2)
            dirs.append(P.T@np.r_[screen,sign*math.sqrt(max(0,1-screen@screen))])
        prox=row['bone_prefix']+'_proximal';dist=row['bone_prefix']+'_distal'
        bp=next(b for b in spec['bones'] if b['name']==prox);bd=next(b for b in spec['bones'] if b['name']==dist)
        c=next(c for c in spec['cubes'] if c['bone']==dist)
        end=np.array([(c['from'][0]+c['to'][0])/2,c['from'][1],(c['from'][2]+c['to'][2])/2,1])
        oldroot=(base['shell_root']@np.r_[bp['pivot'],1])[:3];oldjoint=(base[prox]@np.r_[bd['pivot'],1])[:3]
        oldend=(base[dist]@end)[:3]
        Rprox=minimal_alignment(oldjoint-oldroot,dirs[0])@base[prox][:3,:3]
        wr=world(spec,candidate)['shell_root'];candidate[prox]['rotation']=matrix_delta(spec,prox,Rprox,wr)
        Rdist=minimal_alignment(oldend-oldjoint,dirs[1])@base[dist][:3,:3]
        candidate[dist]['rotation']=matrix_delta(spec,dist,Rdist,world(spec,candidate)[prox])
        records.append(dict(id=ident,source_root_zone=points[0],source_bend=points[1],source_tip=points[2],
            source_axis_angles_above_horizontal=[math.degrees(math.atan2(-v[1],abs(v[0]))) for v in vectors],
            source_axis_vectors=vectors,world_direction_hypothesis=dirs,
            root_uncertainty_px=25,bend_uncertainty_px=15,tip_uncertainty_px=10,
            depth_status='Inferred away-from-viewer proximal branch and toward-viewer distal branch; not recovered source depth.'))
    options=[]
    for ident,title,shift_roots in [('C1','原根固定：六肢向上张开、口打开',False),('C2','根区内聚候选：另加上/中层近段下移',True)]:
        hold=copy.deepcopy(candidate)
        if shift_roots:
            for row in spec['limb_fit']:
                delta=-9 if '_upper' in row['bone_prefix'] else -4 if '_middle' in row['bone_prefix'] else 0
                if delta:hold[row['bone_prefix']+'_proximal']['position']=np.array([0.,delta,0.])
        poses=[]
        for t,weight in [(0,0),(.5,.5),(1,1),(2,1),(3,1),(3.5,.5),(4,0)]:
            pose={b:{ch:np.array(value)*weight for ch,value in state.items()} for b,state in hold.items()}
            poses.append((t,pose,f'cross_{ident}_inferred_{t:.2f}'))
        clip=make_clip('cross_beam',4,False,'推断',poses,['Heart_of_Ender_prepare_to_shoot_beams.png','Wiki: Cross beam'],
            ['Keep 0..1s preparation,1..3s Fourside window,3..4s recovery.',
             'Source near-frontal axis directions constrain the pose; unknown 3D depth branches are explicit.',
             'All six limbs open above the lower torso instead of covering the inner emitter.',
             'C2 root translation is an unaccepted hypothesis inside the same body surface; not source-proven root motion.' if shift_roots else 'All limb roots stay at accepted rest positions; only rotations and global rise are used.'])
        options.append(dict(id=ident,label=title,clip=clip,hold_pose=hold))
    w=world(spec,candidate)
    top=(w['shell_head']@np.array([0,38,-10.8,1]))[:3]
    offset=np.array([1104.,72.])-ppu*(P@top)[:2]
    target=P.T@np.r_[(np.array([811.,408.5])-offset)/ppu,0.]
    cam=dict(projection='orthographic',canvas=[1622,817],screen_basis_rows=P,pixels_per_unit=ppu,offset_px=offset,
        position=target+P[2]*100,target=target,orthographic_height=817/ppu,
        yaw_degrees=0,elevation_degrees=25,
        note='Near-frontal source-camera hypothesis, matched head upper-front midpoint; camera is fixed for both candidates. Not a claim of original camera recovery.')
    q=np.vstack([geom.vertices(c,w[c['bone']])@P.T for c in spec['cubes']])
    qlo=q[:,:2].min(0);qhi=q[:,:2].max(0)
    centered_target=P.T@np.r_[(qlo+qhi)/2,0.]
    centered_camera=dict(projection='orthographic',canvas=[500,500],
        position=centered_target+P[2]*100,target=centered_target,
        orthographic_height=float(max(qhi-qlo)*1.12),yaw_degrees=0,elevation_degrees=25,
        note='C1 fully framed for native review; reframing is not a source-match claim.')
    result=dict(stage='Unaccepted cross-beam shell candidates; main frozen tracks untouched',base_bbmodel_sha256=sha,
        source='Heart_of_Ender_prepare_to_shoot_beams.png',source_canvas=[1622,817],
        source_camera_hypothesis=cam,centered_C1_review_camera=centered_camera,
        C1_source_canvas_projected_bounds=[qlo*ppu+offset,qhi*ppu+offset],
        display_camera=json.loads((OUT/'shell_motion.json').read_text(encoding='utf-8'))['camera'],
        observations=records,options=options,
        limitations=['Image-space axis angles are not world Euler angles.',
            'C1 keeps roots fixed; C2 uses low-confidence source root-zone spacing and must be reviewed separately.',
            'With fixed accepted upper roots, the C1 upper tips extend above the source canvas. The centered review camera must not hide this silhouette difference.',
            'Source smoke/transparent back wall cannot be recreated by this opaque material adaptation.',
            'No scale, mesh/rest edit, camera animation or shell visibility switch is used.'])
    write_json('shell_cross_open_options.json',result)
    # Four study views expose the depth choice; these are not the native BB review.
    sheet=Image.new('RGB',(2000,1080),BG);d=ImageDraw.Draw(sheet)
    for col,(name,yaw,elev) in enumerate([('source front',0,25),('reference',-45,25),('right',90,0),('back',180,0)]):
        pv=geom.camera(yaw,elev);vv=[]
        for opt in options:
            wm=world(spec,opt['hold_pose']);vv.extend(geom.vertices(c,wm[c['bone']])@pv.T for c in spec['cubes'])
        q=np.vstack(vv);lo=q[:,:2].min(0);hi=q[:,:2].max(0)
        sc=min(450/(hi[0]-lo[0]),450/(hi[1]-lo[1]));off=np.array([250,250])-sc*(lo+hi)/2
        for row,opt in enumerate(options):
            sheet.paste(render_pose(spec,opt['hold_pose'],dict(screen_basis_rows=pv,pixels_per_unit=sc,offset_px=off)),(500*col,540*row+40))
            d.text((500*col+8,540*row+10),f'{opt["id"]} / {name} / shell geometry only',font=font(15),fill='white')
    sheet.save(OUT/'shell_cross_open_study.png')
    source=Image.open(REF/'Heart_of_Ender_prepare_to_shoot_beams.png').convert('RGB')
    dd=ImageDraw.Draw(source)
    colors={'A':'#ffdf70','B':'#63dfbb','C':'#7db2ff','D':'#d799ff','E':'#ff9d70','F':'#ff819d'}
    for r in records:
        pts=[tuple(v) for v in [r['source_root_zone'],r['source_bend'],r['source_tip']]]
        color=colors[r['id']];dd.line(pts,fill=color,width=3)
        for k,point in enumerate(pts):
            x,y=point;dd.ellipse((x-6,y-6,x+6,y+6),outline=color,width=2)
            dd.text((x+8,y+5),f'{r["id"]}:{k}',font=font(16),fill=color,stroke_width=1,stroke_fill='black')
    dd.rectangle((12,12,670,96),fill='#20232c')
    dd.text((24,20),'Source pixels unchanged except evidence overlay',font=font(19),fill='white')
    dd.text((24,47),'0: fade-out root zone / 1: visible bend / 2: tip',font=font(17),fill='white')
    dd.text((24,70),'A-F pairing and all depth branches remain inferred',font=font(17),fill='white')
    source.save(OUT/'shell_cross_source_axes.png')
    print(json.dumps(dict(file=str(OUT/'shell_cross_open_options.json'),options=[o['id'] for o in options]),ensure_ascii=False))


def review_cross_native():
    """Read native evidence with correct alpha; never modify native output files."""
    src=REF/'m3_preview/cross_options/C1'
    names=['near_front','overview','front','side','back']+[f'transition_{i}' for i in range(11)]
    sheet=Image.new('RGB',(2000,2160),BG);d=ImageDraw.Draw(sheet)
    records=[]
    for i,name in enumerate(names):
        path=src/(name+'.png');im=Image.open(path).convert('RGBA')
        bg=Image.new('RGBA',im.size,BG+(255,));bg.alpha_composite(im)
        x=(i%4)*500;y=(i//4)*540
        sheet.paste(bg.convert('RGB'),(x,y+40));d.text((x+8,y+10),name,font=font(17),fill='white')
        records.append(dict(path=str(path.relative_to(REF)),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    sheet.save(OUT/'shell_cross_C1_native_review.png')
    write_json('shell_cross_C1_review_inputs.json',dict(note='Correct alpha composite only; native pixels are not repainted.',files=records))
    continuous=sorted((REF/'m3_preview/continuous/movies/cross_beam').glob('frame_*.png'))
    if continuous:
        board=Image.new('RGB',(2000,math.ceil(len(continuous)/8)*280),BG);bd=ImageDraw.Draw(board)
        review=[]
        for i,path in enumerate(continuous):
            im=Image.open(path).convert('RGBA');bg=Image.new('RGBA',im.size,BG+(255,));bg.alpha_composite(im)
            x=(i%8)*250;y=(i//8)*280
            board.paste(bg.convert('RGB').resize((250,250),Image.Resampling.NEAREST),(x,y+30))
            bd.text((x+7,y+6),f'f{i:03d} / {i/12.5:.2f}s',font=font(15),fill='white')
            a=np.array(im);mask=(a[:,:,3]>128)&(np.max(abs(a[:,:,:3].astype(int)-np.array(BG)),axis=2)>10)
            yy,xx=np.where(mask)
            bounds=[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())] if len(xx) else None
            margin=min(bounds[0],bounds[1],im.width-1-bounds[2],im.height-1-bounds[3]) if bounds else None
            review.append(dict(path=str(path.relative_to(REF)),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                foreground_bbox=bounds,minimum_canvas_margin_px=margin,touches_canvas_edge=(margin==0)))
        board.save(OUT/'shell_cross_C1_continuous_review.png')
        write_json('shell_cross_C1_continuous_inputs.json',dict(sample_hz=12.5,native_size=[500,500],thumbnail_size=[250,250],
            edge_touch_frame_count=sum(r['touches_canvas_edge'] for r in review),
            minimum_canvas_margin_px=min(r['minimum_canvas_margin_px'] for r in review if r['minimum_canvas_margin_px'] is not None),
            note='Nearest-neighbor thumbnails and correct alpha composite only; no change to source files. Bounding mask: alpha>128 and RGB differs from gray background by >10.',files=review))


if __name__=='__main__':
    if '--b-options' in sys.argv:b_options()
    elif '--review' in sys.argv:review_frozen()
    elif '--cross-options' in sys.argv:cross_candidates()
    elif '--cross-review' in sys.argv:review_cross_native()
    else:main()
