"""过渡动作的有标注关键姿态 + 原图屏幕轨迹约束；无缩放/隐藏。

单视图只确定投影，深度与关节角是重建方案，不称原作骨骼数据。
"""
import copy,math
import numpy as np
from scipy.spatial.transform import Rotation
from scipy.optimize import least_squares
from PIL import Image
import display_mob as dm
from pope_animate import REF,OUT,Rig,read,write,point,angles,matrix

def camera(yaw,pitch,px,origin,size):
    y,p=math.radians(yaw),math.radians(pitch)
    d=np.array([-math.sin(y)*math.cos(p),math.sin(p),-math.cos(y)*math.cos(p)])
    right=np.array([-math.cos(y),0,math.sin(y)]);up=np.cross(d,right)
    return dict(direction=d.tolist(),right=right.tolist(),up=up.tolist(),px=px,origin=origin,size=size)

CAMERAS={
    'appear':camera(45,30,7.3,[250,425],500),
    'teleport_in':camera(45,30,7.3,[250,425],500),
    'teleport_out':camera(45,30,7.3,[250,425],500),
    'whirlwind':camera(45,30,5.67,[400,735],800),
}

def unproject(cam,xy,depth=0):
    return (np.array(cam['right'])*(xy[0]-cam['origin'][0])/cam['px']-
            np.array(cam['up'])*(xy[1]-cam['origin'][1])/cam['px']+
            np.array(cam['direction'])*depth)

def fit_head(rig,pose,cam,xy,depth=0):
    world,_=rig.pose(pose)
    current=point(world['head'],[0,16,0])
    desired=unproject(cam,xy,depth)
    # Neutral depth of head remains close to rest instead of choosing the camera plane.
    desired+=np.array(cam['direction'])*float(np.dot(current,np.array(cam['direction'])))
    pose.setdefault('root',{})['position']=(desired-current).tolist()
    return pose

def fit_staff(rig,pose,cam,src):
    """Only visible full-size frames. Keep hand attached and solve projected rod endpoints."""
    if src['frame']<6 or src.get('staff_tray_px') is None or src.get('staff_bottom_px') is None:return pose
    base=copy.deepcopy(pose);body=rig.pose(base)[0]['body']
    project=np.array([cam['right'],-np.array(cam['up'])])*cam['px'];origin=np.array(cam['origin'])
    initial=np.array([*pose['left_arm']['rotation'][1:],*pose['left_hand'].get('world_rotation',[0,0,0]),pose['staff']['position'][1]],float)
    def predict(v):
        arm=body@np.array(dm.about(rig.bones['left_arm']['pivot'],[0,v[0],v[1]]))
        hp=point(arm,rig.bones['left_hand']['pivot']);hand=matrix(v[2:5].tolist())
        hand[:3,3]=hp-hand[:3,:3]@rig.bones['left_hand']['pivot']
        staff=hand@np.array(dm.translate(0,v[5],0))
        return [project@point(staff,p)+origin for p in ([-11,0,0],[-11,17.5,0])]
    def residual(v):
        points=predict(v)
        return np.r_[points[0]-src['staff_bottom_px'],points[1]-src['staff_tray_px'],(v-initial)*np.array([.015,.015,.003,.003,.003,.1])]
    fits=[]
    for dx in (0,80,-80):
        seed=initial.copy();seed[2]+=dx
        fits.append(least_squares(residual,seed,bounds=([-180,-110,-900,-900,-900,-2],[180,110,900,900,900,10]),max_nfev=220))
    v=min(fits,key=lambda f:np.linalg.norm(f.fun)).x
    pose['left_arm']['rotation']=[0,float(v[0]),float(v[1])]
    pose['left_hand']={'world_rotation':v[2:5].tolist()}
    pose['staff']['position']=[0,float(v[5]),0]
    return pose

def make_appear(rig,source,name):
    rows=[];cam=CAMERAS[name]
    # Source6/9/12 rise and turn,18 fall,27 compression,39..45 settling.
    key={0: (160, -25,20,-90,-50,40,10),
         3: (150,-25,20,-95,-40,40,10),
         6: (50,-12,15,-40,-65,45,7),
         9: (0,-8,10,0,-60,35,6),
         12:(-15,-12,15,-30,-60,45,6),
         15:(0,-15,20,-55,-60,50,5),
         18:(0,-20,25,-65,-45,50,4),
         24:(0,-40,35,-70,-25,55,3),
         27:(0,-35,30,-70,-22,45,3),
         30:(0,-20,20,-65,-20,30,2),
         39:(0,-8,7,-30,-10,10,1),
         45:(0,0,0,0,0,0,0)}
    for src in source:
        frame=src['frame'];t=src['clip_seconds']
        yaw,bx,hx,ly,lz,leg,slide=key[frame]
        head_z={6:-12,9:-25,12:-15}.get(frame,0)
        airborne=frame in (6,9,12,15,18)
        cape_angle=-10 if airborne else 0
        pose={'body':{'rotation':[bx,yaw,0]},'head':{'rotation':[hx,0,head_z]},
              'left_arm':{'rotation':[0,ly,lz]},'right_arm':{'rotation':[0,15,20]},
              'right_leg':{'rotation':[leg+(20 if airborne else 0),0,8]},'left_leg':{'rotation':[-8 if airborne else -leg*.7,0,-8]},
              'cape':{'rotation':[cape_angle,0,0]},'left_hand':{'world_rotation':[0,0,0]},
              'staff':{'position':[0,slide,0]},'staff_glow':{'rotation':[0,90*t,0]}}
        if frame==45:
            pose={}
        if src.get('head_gray'):
            pose=fit_head(rig,pose,cam,src['head_gray']['centroid'])
        else:
            pose['root']={'position':[0,-6,0]}
        if frame!=45:pose=fit_staff(rig,pose,cam,src)
        rows.append({'time':t,'source_frame':frame,'pose':pose})
    # The full-size first frame is intentional. Hiding/scaling is unsupported;
    # it is not silently emulated by taking the model off-screen or underground.
    if name=='appear':
        rows[-1]['pose']={}
    return rows

def make_out(rig,source):
    rows=[];cam=CAMERAS['teleport_out']
    turns={30:0,33:10,36:150,39:240,42:360,45:540,48:720,51:900,53:1080}
    for src in source:
        f=src['frame'];t=src['clip_seconds'];yaw=turns[f]
        amount=min(1,t/.6)
        pose={'body':{'rotation':[-15,yaw,0]},'head':{'rotation':[15,0,0]},
              'left_arm':{'rotation':[0,-65+50*amount,-15-35*amount]},
              'left_hand':{'rotation':[0,0,25*amount]},'staff':{'position':[0,2+4*amount,0]},
              'right_arm':{'rotation':[0,15,35]},'right_leg':{'rotation':[50*amount,0,8]},
              'left_leg':{'rotation':[-55*amount,0,-8]},'cape':{'rotation':[-40,0,0]},
              'staff_glow':{'rotation':[0,90*t,0]}}
        xy=src['head_gray']['centroid'] if src.get('head_gray') else [250,268]
        pose=fit_head(rig,pose,cam,xy)
        if f<=39:pose=fit_staff(rig,pose,cam,src)
        rows.append({'time':t,'source_frame':f,'pose':pose})
    return rows

def make_whirlwind(rig,source):
    # Source67 and68 both map to2.70s: use68 (first clear crown separation).
    source=list({s['clip_seconds']:s for s in source}.values())
    rows=[];cam=CAMERAS['whirlwind'];d=np.array(cam['direction'])
    raw=[s.get('screen_body_axis_degrees',0) for s in source]
    roll=np.degrees(np.unwrap(np.radians(raw)))
    # First .65s has one full clockwise tumble, supported by dense original frames.
    roll[:4]=[-19,23,182,336]
    for i in range(4,len(roll)):
        while roll[i]-roll[i-1]<-180:roll[i]+=360
        while roll[i]-roll[i-1]>180:roll[i]-=360
    for idx,src in enumerate(source):
        t=src['clip_seconds'];f=src['frame']
        # Roll is a screen observation; yaw/depth and individual limb angles are inferred.
        spin=Rotation.from_rotvec(d*math.radians(-roll[idx])).as_matrix()
        yaw_value=float(np.interp(t,[0,.3,.65,1.,1.35,1.7,2.05,2.35,2.7,3.05,3.35,3.7,4.05,4.35,4.7,5.05,5.4,5.7,6.1,6.4],
                                    [0,45,90,0,-90,-180,-300,-400,-360,-480,-540,-630,-720,-760,-810,-900,-990,-1080,-1170,-1260]))
        yaw=Rotation.from_euler('y',yaw_value,degrees=True).as_matrix()
        r=np.eye(4);r[:3,:3]=spin@yaw
        bodyrot=angles(r)
        pose={'body':{'world_rotation':bodyrot.tolist()},
              'head':{'rotation':[-45 if f==0 else 0,0,0]},
              'right_arm':{'rotation':[25*math.sin(t*8),20*math.sin(t*7),35]},
              'left_arm':{'rotation':[20*math.cos(t*7),-25*math.sin(t*5),-15]},
              'right_leg':{'rotation':[30+30*math.sin(t*8),0,15]},
              'left_leg':{'rotation':[-25-30*math.sin(t*8),0,-15]},
              'cape':{'rotation':[-30,0,0]},
              'staff_glow':{'rotation':[0,t*180,0]}}
        pose=fit_head(rig,pose,cam,src['head_gray']['centroid'],depth=4*math.sin(t*3))
        tray=src.get('staff_tray_px')
        if tray:
            pose['staff']={'world_rotation':[0,0,0],
                           'world_point':unproject(cam,tray).tolist(),'anchor':[-11,17.5,0]}
        else:
            attached=rig.pose(pose)[0]['staff']
            pose['staff']={'world_rotation':[0,0,0],
                           'world_point':point(attached,[-11,17.5,0]).tolist(),'anchor':[-11,17.5,0]}
        if t>=2.7:
            gold=src['crown_gold']['centroid'];head=src['head_gray']['centroid']
            vx,vy=gold[0]-head[0],gold[1]-head[1]
            # Crown long-axis from its original gold pixels. Head-to-crown vector
            # only chooses which end is outward; it does not invent the crown tilt.
            image=np.asarray(Image.open(REF/f'm1/motion/frames/whirlwind_game/{f:04}.png').convert('RGBA'))
            x0,y0,x1,y1=src['crown_gold']['bbox'];crop=image[y0:y1+1,x0:x1+1]
            mask=(crop[:,:,0]>120)&(crop[:,:,1]>80)&(crop[:,:,2]<crop[:,:,1]*.85)&(crop[:,:,3]>0)
            yy,xx=np.where(mask)
            if len(xx)>8:
                eig,vec=np.linalg.eigh(np.cov(np.array([xx,yy])))
                axis=vec[:,np.argmax(eig)]
                if np.dot(axis,[vx,vy])<0:axis=-axis
                vx,vy=axis
            direction=np.array(cam['right'])*vx-np.array(cam['up'])*vy
            direction/=np.linalg.norm(direction)
            rr=Rotation.align_vectors([direction],[[0,1,0]])[0].as_matrix()
            cr=np.eye(4);cr[:3,:3]=rr
            pose['crown']={'world_rotation':angles(cr).tolist(),
                           'world_point':unproject(cam,gold).tolist(),'anchor':[0,25,0]}
        else:
            attached=rig.pose(pose)[0]['crown']
            pose['crown']={'world_rotation':angles(attached).tolist(),
                           'world_point':point(attached,[0,25,0]).tolist(),'anchor':[0,25,0]}
        rows.append({'time':t,'source_frame':f,'pose':pose})
    # End convergence authored by pope_animate.py from the exact6.4s world poses.
    rows.append({'time':7.,'source_frame':None,'pose':copy.deepcopy(rows[-1]['pose'])})
    return rows

def main():
    rig=Rig();study=read(OUT/'motion_transition/transition_keyframes.json')['clips']
    clips={name:make_appear(rig,study[name]['keyframes'],name) for name in ('appear','teleport_in')}
    clips['teleport_out']=make_out(rig,study['teleport_out']['keyframes'])
    clips['whirlwind']=make_whirlwind(rig,study['whirlwind']['keyframes'])
    write(OUT/'transition_poses.json',{'evidence':'有动图；屏幕轨迹来自逐帧色块/人工标点；深度和欧拉为重建，起末透明缩放未制作','clips':clips})
    write(OUT/'transition_cameras.json',{'cameras':CAMERAS,'status':'单视角人工标定候选；不能当作原游戏相机参数'})
    print('过渡姿态已写；尚需Blockbench导出与并排审阅')

if __name__=='__main__':main()
