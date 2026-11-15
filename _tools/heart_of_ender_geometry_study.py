#!/usr/bin/env python3
"""M2: reproducible, untextured static geometry/camera study. NOT a bbmodel.

Source pixels and 3D inferences are kept separate. Java +Y up, faces -Z.
This writes only heart_of_ender_ref/m2_geometry, never pipeline/build files.
"""
from pathlib import Path
import json
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.spatial.transform import Rotation

HERE=Path(__file__).resolve().parent
REF=HERE/'heart_of_ender_ref'
OUT=REF/'m2_geometry'
OUT.mkdir(parents=True,exist_ok=True)
BG=(55,60,70)


def rxyz(values):
    return Rotation.from_euler('ZYX',list(reversed(values)),degrees=True).as_matrix()


def angles(matrix):
    return Rotation.from_matrix(matrix).as_euler('ZYX',degrees=True)[::-1].tolist()


def camera(yaw,elevation):
    a,b=np.radians([yaw,elevation])
    # A real right-handed viewer: right x up = direction towards viewer.
    # Front is -Z, so a camera at -Z sees model +X on image LEFT.
    u=np.array([-math.cos(a),0,-math.sin(a)])
    v=np.array([math.sin(a)*math.sin(b),-math.cos(b),-math.cos(a)*math.sin(b)])
    return np.stack([u,v,-np.cross(u,v)])


def orient_minus_y(direction,roll=0):
    y=-direction/np.linalg.norm(direction)
    reference=np.array([0.,0.,1.])
    if abs(np.dot(reference,y))>.96:reference=np.array([1.,0.,0.])
    x=np.cross(y,reference);x/=np.linalg.norm(x);z=np.cross(x,y)
    return np.column_stack([x,y,z])@rxyz([0,roll,0])


def font(n=22):
    return ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',n)


def add_label(draw,p,text,size=22,color=(245,245,245)):
    f=font(size);bb=draw.textbbox(p,text,font=f)
    draw.rectangle((bb[0]-3,bb[1]-2,bb[2]+3,bb[3]+2),fill=(15,20,28))
    draw.text(p,text,font=f,fill=color)


def rounded(value):
    if isinstance(value,np.ndarray):return rounded(value.tolist())
    if isinstance(value,(list,tuple)):return [rounded(v) for v in value]
    if isinstance(value,dict):return {k:rounded(v) for k,v in value.items()}
    if isinstance(value,(float,np.floating)):return round(float(value),6)
    if isinstance(value,np.integer):return int(value)
    return value


def build_spec():
    # Three projected axes of the head including its closed lower jaw.
    A=np.array([130.,51.]); B=np.array([-54.,-177.]); C=np.array([128.,-108.])
    width=12.
    M=np.array([[B[0]*B[1],C[0]*C[1]], [B[0]**2-B[1]**2,C[0]**2-C[1]**2]])
    rhs=-np.array([A[0]*A[1],A[0]**2-A[1]**2])/width**2
    inv_sq=np.linalg.solve(M,rhs)
    height,depth=1/np.sqrt(inv_sq)
    rows=np.column_stack([-A/width,B/height,C/depth])
    px_per_unit=float(np.linalg.norm(rows[0]))
    rows/=px_per_unit
    head_projected=np.vstack([rows,-np.cross(rows[0],rows[1])])
    P=camera(-45,25)
    shell_rest=rxyz([0,0,-12])
    head_world=P.T@head_projected
    head_relative=shell_rest.T@head_world
    head_pivot=np.array([0.,25.,0.])
    skull_top=38.
    head_front=-10.8
    head_back=head_front+float(depth)
    closed_bottom=skull_top-float(height)
    split_y=26.
    bones=[];cubes=[];parts=[]

    def bone(name,parent,pivot,rest=(0,0,0),evidence='inferred'):
        bones.append(dict(name=name,parent=parent,pivot=list(pivot),rest_rotation=list(rest),evidence=evidence))

    def cube(name,bone_name,lo,hi,purpose,inferred=True):
        cubes.append(dict(name=name,bone=bone_name,**{'from':list(lo),'to':list(hi)},purpose=purpose,inferred=inferred))

    def part(name):parts.append(dict(name=name,bones=[name]))

    bone('shell_root',None,[0,0,0],[0,0,-12],'推断：壳整体静态倾斜，使躯干投影匹配；不是动画')
    bone('shell_body','shell_root',[0,17,4.5])
    cube('shell_body_upper','shell_body',[-4.5,10.0,0.0],[4.5,30.0,8.0],'紧凑纵长中央上躯干；下方留前开口，以不透明几何显示体内小人')
    cube('shell_body_lower_back','shell_body',[-4.5,-1.5,6.5],[4.5,10.0,8.0],'下躯干后壁；为代替原作半透明的明确适配推断，非原作实证拓扑')
    cube('shell_body_lower_left_rim','shell_body',[3.4,3.0,0.0],[4.5,10.0,8.0],'下躯干窄侧缘；前方不做实心封板，不依赖半透明')
    cube('shell_body_lower_right_rim','shell_body',[-4.5,3.0,0.0],[-3.4,10.0,8.0],'下躯干窄侧缘；前方不做实心封板，不依赖半透明')
    part('shell_body')
    bone('shell_head','shell_root',head_pivot,angles(head_relative),'上颅+闭颚总轮廓的三轴正交投影拟合；黑色边界±8–12px')
    cube('shell_skull','shell_head',[-6,split_y,head_front],[6,skull_top,head_back],'上颅主方块；宽12、高12；深由2D拟合推断')
    part('shell_head')
    bone('shell_jaw','shell_head',[0,split_y,head_back],[0,0,0],'闭口静态；铰点在后上缘，为张口结构推断，未制作动作')
    cube('shell_lower_jaw','shell_jaw',[-6,closed_bottom,head_front],[6,split_y,head_back],'闭口下颚；厚度来自总头轮廓减上颅高12')
    part('shell_jaw')

    # Fit the screen translation to the most readable front top-left contour.
    tl=np.array([6,skull_top,head_front])
    world_tl=shell_rest@head_pivot+head_world@(tl-head_pivot)
    offset=np.array([218.,211.])-px_per_unit*(P@world_tl)[:2]

    def project(world):return px_per_unit*(P@world)[:2]+offset

    def point_on_screen(xy,depth_value):
        q=np.array([(xy[0]-offset[0])/px_per_unit,(xy[1]-offset[1])/px_per_unit,depth_value])
        return P.T@q

    # Root rows are symmetrical in model coordinates. Mapping A-F to these
    # rows is explicitly a hypothesis; only projected endpoint IDs are known.
    limb_fit=[
        ('left_upper','A',[4.5,28,4], [229,182],[86,54],-1,-1),
        ('left_middle','B',[4.5,18.5,4], [207,405],[49,452],-1,-1),
        ('left_lower','C',[4.5,9,4], [250,574],[47,674],+1,+1),
        ('right_upper','F',[-4.5,28,4], [626,501],[668,627],-1,-1),
        ('right_middle','E',[-4.5,18.5,4], [585,655],[626,778],+1,+1),
        ('right_lower','D',[-4.5,9,4], [735,525],[966,487],+1,+1),
    ]
    limb_records=[]
    for limb,label,root,elbow_xy,tip_xy,sgn1,sgn2 in limb_fit:
        root=np.array(root,dtype=float)
        root_world=shell_rest@root
        rcam=P@root_world
        q=(np.array(elbow_xy)-offset)/px_per_unit
        lproj=float(np.linalg.norm(q-rcam[:2]))
        L1=max(14.,lproj*1.005)
        elbow_depth=rcam[2]+sgn1*math.sqrt(max(0,L1*L1-lproj*lproj))
        elbow_world=point_on_screen(elbow_xy,elbow_depth)
        tip_q=(np.array(tip_xy)-offset)/px_per_unit
        dist_proj=float(np.linalg.norm(tip_q-q))
        L2=max(16.,dist_proj*1.005)
        tip_depth=elbow_depth+sgn2*math.sqrt(max(0,L2*L2-dist_proj*dist_proj))
        tip_world=point_on_screen(tip_xy,tip_depth)
        d1=shell_rest.T@(elbow_world-root_world)
        d2=shell_rest.T@(tip_world-elbow_world)
        R1=orient_minus_y(d1)
        R2=orient_minus_y(d2)
        b1='limb_'+limb+'_proximal';b2='limb_'+limb+'_distal'
        distal_pivot=root+np.array([0,-L1,0])
        bone(b1,'shell_root',root,angles(R1),'根点层级/深度推断；拟合'+label+'屏幕折点')
        bone(b2,b1,distal_pivot,angles(R1.T@R2),'两段方向静态拟合；'+label+'实际原始骨骼/深度未知')
        thick=4.0
        cube(b1+'_cube',b1,[root[0]-thick/2,root[1]-L1,root[2]-thick/2],[root[0]+thick/2,root[1],root[2]+thick/2],'近端直方柱，无额外肩块/手掌')
        cube(b2+'_cube',b2,[root[0]-thick/2,root[1]-L1-L2,root[2]-thick/2],[root[0]+thick/2,root[1]-L1,root[2]+thick/2],'远端方柱平端，无手指/脚掌')
        part(b1);part(b2)
        limb_records.append(dict(bone_prefix='limb_'+limb,source_id=label,root_model=root,root_projected=project(root_world),elbow_projected=elbow_xy,tip_projected=tip_xy,root_world=root_world,elbow_world=elbow_world,tip_world=tip_world,segment_lengths=[L1,L2],thickness=thick,depth_signs=[sgn1,sgn2],mapping_status='推断：模型左右/层级不是已知原骨架；端点投影拟合不验证深度'))

    # Placeholder geometry of the inner figure follows its observed silhouette,
    # especially the long upper strip. It is not a conventional villager rig.
    bone('inner_root','shell_root',[0,0,-4.5],[0,0,4],'独立整体骨；静态漂浮位置为投影拟合，未作动画')
    bone('inner_body','inner_root',[0,3,-4.5])
    cube('inner_torso','inner_body',[-1.4,1.5,-5.375],[1.4,4.6,-3.625],'小人躯干；Docile轮廓为主，兼容UV候选8/9宽×9高×4/5深的区间，非精确展开图反推')
    part('inner_body')
    bone('inner_head','inner_root',[0,4.5,-4.5],[0,0,-4])
    cube('inner_head_core','inner_head',[-2.1,4.5,-5.55],[2.1,6.95,-3.45],'小人大头；按64px原贴图UV候选12×7×6乘0.35，UV反推仍非原geo')
    cube('inner_head_upper_strip','inner_head',[-.7,6.95,-5.2],[.7,10.8,-3.8],'可见头顶高条；与原贴图金色4×11×4冠岛比例吻合，0.35倍')
    cube('inner_nose','inner_head',[-.35,4.85,-6.25],[.35,6.25,-5.55],'小人鼻候选2×4×2乘0.35；UV反推，非原geo')
    part('inner_head')
    for side,s in [('left',-1),('right',1)]:
        name='inner_arm_'+side;px=-s*1.55
        bone(name,'inner_root',[px,4.1,-4.5],[8,0,s*14])
        cube(name+'_cube',name,[px-.28,1.7,-4.82],[px+.28,4.1,-4.18],'细臂，仅一段，手随臂刚性')
        part(name)
        name='inner_leg_'+side;px=-s*.72
        bone(name,'inner_root',[px,1.7,-4.5],[-10,0,-s*7])
        cube(name+'_shin',name,[px-.30,0,-4.85],[px+.30,1.7,-4.15],'小人独立腿')
        cube(name+'_foot',name,[px-.30,-.2,-5.45],[px+.30,.22,-4.15],'原轮廓中的前伸短足，合并到腿骨')
        part(name)

    # Fit the tiny figure to the observed lower central glow silhouette while
    # keeping it physically inside the lower shell. This is a static offset,
    # not an animation position channel or a hidden scale track.
    inner_shift=np.array([0.,-4.3,7.4])
    for b in bones:
        if b['name'].startswith('inner_'):
            b['pivot']=(np.array(b['pivot'])+inner_shift).tolist()
    for c in cubes:
        if c['bone'].startswith('inner_'):
            c['from']=(np.array(c['from'])+inner_shift).tolist()
            c['to']=(np.array(c['to'])+inner_shift).tolist()

    glow_names=['shell_eyes_glow','shell_teeth_front_glow','shell_teeth_side_glow']
    bone('shell_eyes_glow','shell_head',head_pivot,[0,0,0],'空骨占位；root按原渲染采样生成眼形，刚性合入头部')
    for name in glow_names[1:]:
        bone(name,'shell_jaw',[0,split_y,head_back],[0,0,0],'空骨占位；root按原渲染采样生成牙形，刚性合入下颚')
    for p in parts:
        if p['name']=='shell_head':p['bones'].append('shell_eyes_glow')
        if p['name']=='shell_jaw':p['bones'].extend(glow_names[1:])

    target_cam=(np.array([500.,420.])-offset)/px_per_unit
    target_world=P.T@np.r_[target_cam,0.]

    spec=dict(stage='M2 static geometry study; not an accepted final model',expected_part_count=21,
        coordinate_system='Java model space: +y up, facing -z; cube coordinates are absolute unposed rig coordinates; rotations are degrees XYZ applied as Rz*Ry*Rx around pivot',
        model_scale=None,seat=0,scale_note='head width = 12 model units; seat=0 only for normalized geometry study; game visual size not chosen',
        camera=dict(projection='orthographic',yaw_deg=-45,elevation_deg=25,roll_deg=0,pixels_per_unit=px_per_unit,offset_px=offset,screen_basis_rows=P,canvas=[1000,840],depth_rule='larger camera depth is nearer viewer',handedness='screen_right cross screen_up = viewer; P rows are right, down, viewer (det=-1)',orthographic_height=840/px_per_unit,target=target_world,position_at_distance_80=target_world+P[2]*80),
        head_fit=dict(width=width,total_closed_height=height,depth=depth,upper_skull_height=12.,closed_jaw_height=height-12.,front_face='north',side_face='west',front_quad_px=[[218,211],[348,262],[402,439],[272,388]],top_quad_px=[[218,211],[346,103],[476,154],[348,262]],side_quad_px=[[348,262],[476,154],[530,331],[402,439]],front_model_quad=[[6,skull_top,head_front],[-6,skull_top,head_front],[-6,closed_bottom,head_front],[6,closed_bottom,head_front]],side_model_quad=[[-6,skull_top,head_front],[-6,skull_top,head_back],[-6,closed_bottom,head_back],[-6,closed_bottom,head_front]],inferred='2D black boundaries ±8–12px; complete head includes closed lower jaw; not original UV or bone data',world_rotation=angles(head_world),relative_rotation=angles(head_relative)),
        bones=bones,cubes=cubes,parts=parts,glow_bones=glow_names,limb_fit=limb_records,inner_static_translation=inner_shift,
        uncertainty=['All hidden depth and root positions inferred; one image cannot recover unique 3D rig.','A-F to side/row assignment is a hypothesis only.','No original clean back/side view; side and back study views expose inferred geometry.','The lower-body front opening is an opaque-rendering adaptation, not proven source topology.','Inner upper strip aspect agrees with a 4x11x4 gold UV island; source geometry is still unavailable.','No textures, eye/mouth drawing, particles, gameplay, animation or runtime hooks included.','Root origin is a normalized study origin, not a verified in-game ground or passenger seat position.'])
    return spec


def world_matrices(spec):
    result={}
    for b in spec['bones']:
        R=rxyz(b['rest_rotation']);p=np.array(b['pivot'],float)
        T=np.eye(4);T[:3,:3]=R;T[:3,3]=p-R@p
        if b['parent']:T=result[b['parent']]@T
        result[b['name']]=T
    return result


def vertices(cube,T):
    lo,hi=np.array(cube['from']),np.array(cube['to'])
    return np.array([(T@np.r_[[(hi if (i>>k)&1 else lo)[k] for k in range(3)],1])[:3] for i in range(8)])


FACES=[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)]


def render(spec,yaw=None,elevation=None,canvas=(1000,840),auto=False,wire=False):
    P=np.array(spec['camera']['screen_basis_rows']) if yaw is None else camera(yaw,elevation)
    scale=spec['camera']['pixels_per_unit'];offset=np.array(spec['camera']['offset_px'])
    wm=world_matrices(spec)
    polys=[];allverts=[]
    for index,c in enumerate(spec['cubes']):
        world=vertices(c,wm[c['bone']]);cam=world@P.T;allverts.append(cam)
        for fi,face in enumerate(FACES):
            polys.append([float(cam[list(face),2].mean()),cam[list(face),:2],c['bone'],fi])
    if auto:
        vv=np.vstack(allverts);lo=vv[:,:2].min(0);hi=vv[:,:2].max(0)
        scale=min((canvas[0]-80)/(hi[0]-lo[0]),(canvas[1]-110)/(hi[1]-lo[1]));offset=np.array(canvas)/2-scale*(lo+hi)/2+np.array([0,25])
    im=Image.new('RGB',canvas,BG);d=ImageDraw.Draw(im)
    for depth,xy,name,fi in sorted(polys,key=lambda p:p[0]):
        xy=xy*scale+offset
        if name.startswith('inner'):base=(220,156,222)
        elif name=='shell_head':base=(114,139,163)
        elif name=='shell_jaw':base=(94,122,146)
        elif name=='shell_body':base=(81,100,111)
        elif name.startswith('limb_left'):base=(98,132,125)
        else:base=(136,111,130)
        shade=[.68,.81,.9,1.06,.75,.99][fi]
        color=tuple(int(v*shade) for v in base)
        d.polygon([tuple(v) for v in xy],fill=color if not wire else BG,outline=(190,202,214))
    return im


def main():
    spec=build_spec()
    bounds=[]
    for part in spec['parts']:
        members=[c for c in spec['cubes'] if c['bone'] in part['bones']]
        lo=np.min([c['from'] for c in members],axis=0);hi=np.max([c['to'] for c in members],axis=0)
        span=hi-lo
        bounds.append(dict(part=part['name'],span=span,centered_from=8-span/2,centered_to=8+span/2,within_minus16_plus32=bool(np.all(span<=48))))
    if len(spec['parts'])!=21 or not all(x['within_minus16_plus32'] for x in bounds):
        raise ValueError('Static geometry part budget / local span check failed')
    (OUT/'part_bounds.json').write_text(json.dumps(rounded(dict(expected_parts=21,actual_parts=len(spec['parts']),largest_span=max(max(x['span']) for x in bounds),all_within_limits=True,parts=bounds)),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (OUT/'geometry_spec.json').write_text(json.dumps(rounded(spec),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    P=np.array(spec['camera']['screen_basis_rows']);head_wm=world_matrices(spec)['shell_head']
    q=np.array(spec['head_fit']['front_model_quad']);world=(np.c_[q,np.ones(4)]@head_wm.T)[:,:3]
    px=(world@P.T)[:,:2]*spec['camera']['pixels_per_unit']+spec['camera']['offset_px']
    cam_check=dict(utf8_chinese_ok='推断' in (OUT/'geometry_spec.json').read_text(encoding='utf-8'),replacement_characters=(OUT/'geometry_spec.json').read_text(encoding='utf-8').count('\ufffd'),screen_right_cross_up_equals_viewer=bool(np.allclose(np.cross(P[0],-P[1]),P[2],atol=1e-8)),head_rotation_det=float(np.linalg.det(head_wm[:3,:3])),front_corner_max_error_px=float(np.max(np.linalg.norm(px-np.array(spec['head_fit']['front_quad_px']),axis=1))),camera_position=spec['camera']['position_at_distance_80'],camera_target=spec['camera']['target'],side_face=spec['head_fit']['side_face'])
    if not cam_check['screen_right_cross_up_equals_viewer'] or cam_check['front_corner_max_error_px']>1e-5:
        raise ValueError('Camera handedness / corner reprojection check failed')
    (OUT/'camera_validation.json').write_text(json.dumps(rounded(cam_check),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    source=Image.open(REF/'MCD_Heart_of_Ender.png').convert('RGBA');flat=Image.new('RGBA',source.size,BG+(255,));flat.alpha_composite(source);source=flat.convert('RGB')
    fitted=render(spec)
    combined=Image.new('RGB',(2000,910),BG);combined.paste(source,(0,70));combined.paste(fitted,(1000,70));d=ImageDraw.Draw(combined)
    add_label(d,(20,12),'原始渲染（仅灰底合成）',25)
    add_label(d,(1020,12),'几何投影研究：无材质；深度和根点含推断',24)
    combined.save(OUT/'reference_fit.png')
    fitted.save(OUT/'geometry_reference_view.png')
    views=[('front',0,0),('right_side',90,0),('back',180,0),('three_quarter',-45,25)]
    sheet=Image.new('RGB',(1600,1300),BG);d=ImageDraw.Draw(sheet)
    for n,(name,yaw,elev) in enumerate(views):
        im=render(spec,yaw,elev,(800,650),auto=True);sheet.paste(im,(n%2*800,n//2*650));add_label(d,(n%2*800+20,n//2*650+10),name+'（深度/背侧含推断）',22)
        im.save(OUT/(name+'.png'))
    sheet.save(OUT/'geometry_four_views.png')
    wm=world_matrices(spec)
    print(json.dumps(rounded({'parts':len(spec['parts']),'head':spec['head_fit'],'camera':spec['camera'],'body_bbox':(vertices(spec['cubes'][0],wm['shell_body'])@np.array(spec['camera']['screen_basis_rows']).T)[:,:2].tolist(),'limb_root_projection':[{k:v for k,v in r.items() if k in ['source_id','root_projected','segment_lengths']} for r in spec['limb_fit']]}),ensure_ascii=False))


def study_endcaps():
    """Read saved spec, vary only distal axial roll; never write the spec/bbmodel."""
    import copy
    import itertools
    from scipy.optimize import minimize_scalar
    spec=json.loads((OUT/'geometry_spec.json').read_text(encoding='utf-8'))
    P=np.array(spec['camera']['screen_basis_rows'])
    scale=spec['camera']['pixels_per_unit'];offset=np.array(spec['camera']['offset_px'])
    measured={
        'A':dict(corners=[[66,44],[107,20],[64,87]],uncertainty_px=3,
                 note='Three outer silhouette vertices only; fourth cap corner not independently measured.'),
        'B':dict(corners=[[49,416],[31,451],[61,492]],uncertainty_px=3,
                 note='Three outer silhouette vertices; interior cap border is low contrast.'),
        'E':dict(edge=[[602,800],[657,787]],uncertainty_px=2,
                 note='Visible bottom edge only; do not invent the hidden cap corners.')}

    def sample(label,roll):
        s=copy.deepcopy(spec)
        row=next(r for r in s['limb_fit'] if r['source_id']==label)
        name=row['bone_prefix']+'_distal'
        b=next(b for b in s['bones'] if b['name']==name)
        old_rotation=list(b['rest_rotation'])
        b['rest_rotation']=angles(rxyz(old_rotation)@rxyz([0,roll,0]))
        c=next(c for c in s['cubes'] if c['bone']==name)
        T=world_matrices(s)[name];T0=world_matrices(spec)[name]
        points=[]
        for x,z in itertools.product([c['from'][0],c['to'][0]],[c['from'][2],c['to'][2]]):
            world=(T@np.array([x,c['from'][1],z,1]))[:3]
            points.append(scale*(P@world)[:2]+offset)
        center=np.array([(c['from'][0]+c['to'][0])/2,c['from'][1],(c['from'][2]+c['to'][2])/2,1])
        center_error=float(np.linalg.norm((T@center-T0@center)[:3]))
        if center_error>1e-10:raise ValueError('Axial roll moved the centerline')
        return dict(source_id=label,bone=name,axial_roll_delta_degrees=roll,
                    old_rest_rotation=old_rotation,rest_rotation=b['rest_rotation'],
                    projected_cap_corners_xz_order=points,tip_center_3d_delta=center_error)

    fits={}
    for label in ['A','B']:
        targets=np.array(measured[label]['corners'])
        def loss(roll):
            corners=np.array(sample(label,roll)['projected_cap_corners_xz_order'])
            return min(np.mean(np.linalg.norm(corners[list(p)]-targets,axis=1)**2)
                       for p in itertools.permutations(range(4),3))
        grid=np.arange(-45,45,.5);approx=grid[np.argmin([loss(v) for v in grid])]
        fit=minimize_scalar(loss,bounds=(approx-1,approx+1),method='bounded')
        fits[label]=dict(roll_degrees=float(fit.x),three_corner_rms_px=float(np.sqrt(fit.fun)),
                         note='This error is to supplied fitted silhouette vertices, not an independent accuracy score.')
    options=[]
    for ident,caption,rolls in [
        ('R0','现状；保留当前中心线、截面和滚转',{'A':0,'B':0,'E':0}),
        ('R1','中间角度：A轮廓拟合，B/E取折中滚转',{'A':fits['A']['roll_degrees'],'B':15,'E':-7}),
        ('R2','边线方向优先：A/B三角点拟合，E底边斜率拟合',{'A':fits['A']['roll_degrees'],'B':fits['B']['roll_degrees'],'E':-14})]:
        details=[sample(label,roll) for label,roll in rolls.items()]
        options.append(dict(id=ident,label=caption,
                            bone_rest_replacements={r['bone']:r['rest_rotation'] for r in details},
                            details=details))
    result=dict(stage='M2 unselected endcap roll options; no fact-source edit',
        source_file='MCD_Heart_of_Ender.png',source_canvas=[1000,840],
        source_points=measured,fit_results=fits,
        convention='Replacement Euler XYZ, Rz*Ry*Rx. New local matrix = old local matrix @ Ry(delta). All cubes/pivots/centerlines unchanged.',
        limitations=['A/B cap hidden edge is not independently observed.',
            'E roll-only cannot simultaneously match bottom edge slope and position at the fixed centerline/depth/4x4 section.',
            'R2 E visible bottom-edge direction is closer, but its lower edge is about 10 pixels too low.',
            'B best three-corner residual remains about 10.8 pixels; source cap center and section/depth remain uncertain.',
            'No option is automatically accepted. Native Blockbench comparisons should be offered to the user.'],
        options=options)
    (OUT/'endcap_options.json').write_text(json.dumps(rounded(result),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    source=Image.open(REF/'MCD_Heart_of_Ender.png').convert('RGBA')
    flat=Image.new('RGBA',source.size,BG+(255,));flat.alpha_composite(source)
    d=ImageDraw.Draw(flat)
    for label,data in measured.items():
        points=data.get('corners',data.get('edge'))
        if 'edge' in data:d.line([tuple(p) for p in points],fill=(255,214,74),width=2)
        for index,(x,y) in enumerate(points):
            d.ellipse((x-4,y-4,x+4,y+4),outline=(255,214,74),width=2)
            text_xy=(465,811) if label=='E' and index==0 else (x+7,y+3)
            add_label(d,text_xy,f'{label}{index+1} ({x},{y})',15,(255,235,140))
    flat.convert('RGB').save(OUT/'endcap_source_measurements.png')
    print(json.dumps(rounded(dict(file=str(OUT/'endcap_options.json'),fits=fits,options=options)),ensure_ascii=False))


if __name__=='__main__':
    import sys
    study_endcaps() if '--endcaps' in sys.argv else main()
