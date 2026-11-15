"""根据原帧人工点拟合持杖手与杖；保持M2几何、躯干/头旋转。
按头盒标点补整体位移，皇冠轴单独拟合。

屏幕约束最小二乘只是三维重建，不是官方骨骼数据；残差完整保留。
"""
import argparse,copy,math
import numpy as np
from scipy.optimize import least_squares
from scipy import ndimage
from PIL import Image
import display_mob as dm
from pope_animate import REF,OUT,Rig,read,write,point,matrix

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--clips',nargs='*');args=parser.parse_args()
    rig=Rig();study=OUT/'motion_attack_cast'
    rows=read(study/'action_poses_candidates.json')
    manual=read(study/'manual_landmarks.json')['clips']
    cameras=read(study/'camera_calibration.json')['cameras']
    source_meta=read(REF/'m1/motion/clips.json')['clips']
    reports=[]
    if args.clips and (OUT/'action_poses.json').exists():
        existing=read(OUT/'action_poses.json')['clips']
        for n in list(rows):
            if n not in args.clips:rows[n]=existing[n]
        reports=[r for r in read(OUT/'action_fit_report.json')['records'] if r['clip'] not in args.clips]
    for name,keys in rows.items():
        if args.clips and name not in args.clips:continue
        cam=cameras[name];yaw=math.radians(cam['camera_yaw_degrees']);pitch=math.radians(cam['camera_pitch_down_degrees'])
        project=np.array([[-math.cos(yaw),0,math.sin(yaw)],[-math.sin(pitch)*math.sin(yaw),-math.cos(pitch),-math.sin(pitch)*math.cos(yaw)]])*cam['pixels_per_model_unit']
        origin=np.array(cam['world_origin_pixel']);points={r['source_frame']:r for r in manual[name]}
        mapping=next(c for c in source_meta if c['name']==name)['key_poses']
        sf=[r['source_frame'] for r in mapping];ct=[r['proposed_clip_time_seconds'] for r in mapping]
        for row in keys:
            frame=row['source_frame'];row['time']=round(float(np.interp(frame,sf,ct)),5)
            if frame in (0,keys[-1]['source_frame']):continue
            target=points.get(frame)
            if not target:continue
            pose=row['pose'];base=copy.deepcopy(pose)
            # At the forward thrust the source feet fold behind the raised robe,
            # not down below the head. The body already pitches -65..-75deg;
            # do not cancel all that pitch again on the leg bones.
            if name=='attack' and frame in (11,13,18):
                pose['right_leg']['rotation']=[35 if frame==11 else 25,0,0]
                pose['left_leg']['rotation']=[20 if frame==11 else 10,0,0]
                base=copy.deepcopy(pose)
            if target.get('head_visible_box_center_proxy') is not None:
                current=project@point(rig.pose(base)[0]['head'],[0,16,0])+origin
                first=keys[0]['pose'];rest_center=project@point(rig.pose(first)[0]['head'],[0,16,0])+origin
                bias=rest_center-np.array(points[0]['head_visible_box_center_proxy'])
                delta=np.array(target['head_visible_box_center_proxy'])+bias-current
                offset=project.T@delta/cam['pixels_per_model_unit']**2
                pose['root']={'position':offset.tolist()};base=copy.deepcopy(pose)
            # Fit the independent crown's screen long-axis and gold center. The
            # original mask is retained by the study; no texture pixels are edited.
            im=np.asarray(Image.open(REF/f'm1/motion/frames/{name}/{frame:04}.png').convert('RGBA'))
            mask=(im[:,:,0]>110)&(im[:,:,1]>65)&(im[:,:,2]<im[:,:,1]*.68)&(im[:,:,0]>im[:,:,1]*1.08)&(im[:,:,3]>0)
            head_target=target.get('head_visible_box_center_proxy')
            if head_target:mask[round(head_target[1]):]=False
            labels,count=ndimage.label(mask);components=[]
            for index in range(1,count+1):
                yy,xx=np.where(labels==index)
                if len(xx)>80:components.append((len(xx),xx,yy))
            if components:
                _,xx,yy=max(components,key=lambda item:item[0]);gold=np.array([xx.mean(),yy.mean()])
                eigen,vectors=np.linalg.eigh(np.cov([xx,yy]));axis=vectors[:,np.argmax(eigen)]
                if head_target and np.dot(axis,gold-head_target)<0:axis=-axis
                original=np.array(pose['crown']['world_rotation']);headworld=rig.pose(pose)[0]['head']
                pivot=np.array(rig.bones['crown']['pivot']);worldpivot=point(headworld,pivot)
                def crown_residual(v):
                    m=matrix([v[0],original[1],v[1]]);m[:3,3]=worldpivot-m[:3,:3]@pivot
                    v2=project@m[:3,1];v2/=np.linalg.norm(v2)
                    center=project@point(m,[0,25,0])+origin
                    return np.r_[(v2-axis)*35,(center-gold)*.7,(v-original[[0,2]])*.02]
                cf=least_squares(crown_residual,original[[0,2]],max_nfev=150)
                pose['crown']['world_rotation']=[float(cf.x[0]),float(original[1]),float(cf.x[1])]
                base=copy.deepcopy(pose)
            body=rig.pose(base)[0]['body']
            initial=np.array([*pose['left_arm']['rotation'][1:],*pose['left_hand']['world_rotation'],pose['staff']['position'][1],pose['staff_glow']['position'][1]],float)
            anchors={'left_hand_grip':([-11,11,0],2.),'staff_rod_bottom':([-11,0,0],1.),
                     'staff_tray_center':([-11,17.5,0],1.5),'staff_core_visible_pixel_centroid':([-11,22.2645298841,0],.65)}
            selected={n:(np.array(p),w) for n,(p,w) in anchors.items() if target.get(n) is not None}
            if len(selected)<2:continue
            def predict(v,world_points=False):
                arm=body@np.array(dm.about(rig.bones['left_arm']['pivot'],[0,v[0],v[1]]))
                handpivot=point(arm,rig.bones['left_hand']['pivot'])
                hand=matrix(v[2:5].tolist());hand[:3,3]=handpivot-hand[:3,:3]@rig.bones['left_hand']['pivot']
                staff=hand@np.array(dm.translate(0,v[5],0))
                result={}
                for n,(p,w) in selected.items():
                    q=p.copy()
                    if n=='staff_core_visible_pixel_centroid':q[1]+=v[6]
                    world_point=point(hand if n=='left_hand_grip' else staff,q)
                    result[n]=world_point if world_points else project@world_point+origin
                return result
            def residual(v):
                predicted=predict(v)
                error=[(predicted[n]-np.array(target[n]))*w for n,(p,w) in selected.items()]
                error.append((v-initial)*np.array([.02,.02,.002,.002,.002,.2,.2]))
                if name=='attack' and 'staff_core_visible_pixel_centroid' in selected:
                    core_y=predict(v,True)['staff_core_visible_pixel_centroid'][1]
                    error.append(np.array([max(0,1.5-core_y)*20]))
                return np.concatenate(error)
            # Several wrist-depth seeds avoid selecting a local solution just because the
            # first guess points the staff along the view direction.
            seeds=[initial.copy()]
            for dx,dy in ((80,0),(-80,0),(0,90),(0,-90)):
                s=initial.copy();s[2]+=dx;s[3]+=dy;seeds.append(s)
            lower=np.array([-180,-110,-900,-900,-900,-2,0]);upper=np.array([180,110,900,900,900,10,13])
            fits=[least_squares(residual,np.clip(s,lower+1e-7,upper-1e-7),bounds=(lower,upper),max_nfev=250,ftol=1e-7) for s in seeds]
            fit=min(fits,key=lambda f:np.linalg.norm(f.fun));v=fit.x
            pose['left_arm']['rotation']=[0,float(v[0]),float(v[1])]
            pose['left_hand']['world_rotation']=v[2:5].tolist()
            pose['staff']['position']=[0,float(v[5]),0]
            pose['staff_glow']['position']=[0,float(v[6]),0]
            predicted=predict(v)
            errors={n:float(np.linalg.norm(predicted[n]-target[n])) for n in predicted}
            reports.append({'clip':name,'frame':frame,'clip_time':row['time'],'points':{n:{'target_px':target[n],'predicted_px':predicted[n].tolist(),'error_px':errors[n]} for n in predicted},
                            'max_pixel_error':max(errors.values()),'parameters':v.tolist(),'meaning':'几何锚点对原图人工点/可见色块质心；不是原生渲染轮廓误差'})
        print(name,'fit done',flush=True)
    write(OUT/'action_poses.json',{'method':'人工点约束的最小二乘重建；固定已确认几何/相机，保留各点残差','clips':rows})
    write(OUT/'action_fit_report.json',{'records':reports,'warning':'二维点不能唯一确定深度；每段仍须以原生并排图验收，不以数值误差冒充视觉复刻'})

if __name__=='__main__':main()
