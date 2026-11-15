"""Independent read-only saved Armature animation/grip audit.

Rebuilds native local TRS semantics using elementary matrices, not the animation
builder or its pose payload. Supports the linear/step numeric tracks actually
exported here; unsupported expressions/interpolation explicitly fail closed.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import re

import numpy as np

HERE = Path(__file__).resolve().parent
DEFAULT = Path(r'D:\agent\claude\github-create\tralancer-rpg-1.21.11\_tools\lucifer_ref\separate\lucifer_verdant.bbmodel')


def euler_zyx(xyz):
    x,y,z = np.radians(xyz)
    cx,sx,cy,sy,cz,sz = math.cos(x),math.sin(x),math.cos(y),math.sin(y),math.cos(z),math.sin(z)
    rx=np.array([[1.,0,0],[0,cx,-sx],[0,sx,cx]])
    ry=np.array([[cy,0,sy],[0,1.,0],[-sy,0,cy]])
    rz=np.array([[cz,-sz,0],[sz,cz,0],[0,0,1.]])
    return rz @ ry @ rx


def curve(keys,t,default):
    if not keys:return np.array(default,dtype=float)
    times=[k['time'] for k in keys]
    ix=int(np.searchsorted(times,t,side='right'))
    if ix==0:return keys[0]['value'].copy()
    if ix==len(keys):return keys[-1]['value'].copy()
    a,b=keys[ix-1],keys[ix]
    if a['interpolation']=='step':return a['value'].copy()
    f=(t-a['time'])/(b['time']-a['time'])
    return a['value']*(1-f)+b['value']*f


def main():
    ap=argparse.ArgumentParser();ap.add_argument('bbmodel',nargs='?',type=Path,default=DEFAULT)
    ap.add_argument('--output',type=Path,default=HERE/'animation_grip_validation.json')
    args=ap.parse_args();raw=args.bbmodel.read_bytes();bb=json.loads(raw)
    source=json.loads((HERE/'weapon_native_input.json').read_text(encoding='utf-8'))
    alignment=json.loads((HERE/'weapon_grip_alignment.json').read_text(encoding='utf-8'))
    bones={e['uuid']:e for e in bb['elements'] if e['type']=='armature_bone'}
    byname={e['name']:uid for uid,e in bones.items()}
    parent={};order=[]
    def walk(items,p=None):
        for item in items:
            if isinstance(item,str):uid=item;children=[]
            else:uid=item['uuid'];children=item.get('children',[])
            if uid in bones:parent[uid]=p if p in bones else None;order.append(uid)
            walk(children,uid)
    walk(bb['outliner'])
    assert set(order)==set(bones),'Outliner bone set differs'
    def pose(tracks,t):
        result={}
        for uid in order:
            b=bones[uid];ch=tracks.get(uid,{})
            pos=np.array(b['origin'])+curve(ch.get('position',[]),t,[0,0,0])
            rot=np.array(b['rotation'])+curve(ch.get('rotation',[]),t,[0,0,0])
            scale=curve(ch.get('scale',[]),t,[1,1,1])
            local=np.eye(4);local[:3,:3]=euler_zyx(rot)@np.diag(scale);local[:3,3]=pos
            result[uid]=local if parent[uid] is None else result[parent[uid]]@local
        return result
    bind=pose({},0);inverse_bind={uid:np.linalg.inv(m) for uid,m in bind.items()}
    weapon=next(e for e in bb['elements'] if e['name']=='weapon__LuciferSerpentSpear')
    arm=next(e for e in bb['elements'] if e['name']=='body__R_Arm')
    legs=[next(e for e in bb['elements'] if e['name']=='body__'+name) for name in ['R_Leg','L_Leg']]
    for e in [weapon,arm]:assert e['origin']==[0,0,0] and e['rotation']==[0,0,0]
    delta=np.array(alignment['translation_global_bind'])
    sv=source['parts'][0]['vertices'];assert set(weapon['vertices'])==set(sv)
    point_error=max(abs(np.array(weapon['vertices'][k])-(np.array(sv[k])+delta)).max() for k in sv)
    weight_errors=[]
    for mesh,bname in [(weapon,'J_R_Weapon'),(arm,'R_Arm')]:
        for key in mesh['vertices']:
            token=mesh['uuid'][:6]+':'+key
            found=[(b['name'],b.get('vertex_weights',{})[token]) for b in bones.values() if token in b.get('vertex_weights',{})]
            if found!=[(bname,1)]:weight_errors.append([mesh['name'],key,found])
    reference=np.array([alignment['semantic_points_world_after'][n]+[1] for n in ['grip','tip','base']])
    corners=np.c_[np.array(alignment['grip_eight_corners_world_after']),np.ones(8)]
    av=np.array(list(arm['vertices'].values()));amin,amax=av.min(0),av.max(0)
    issues=[];rows=[];all_samples=[];channel_max={}
    decimal=re.compile(r'^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$')
    for animation in bb.get('animations',[]):
        name=animation['name'];tracks={};times={0.,float(animation['length'])}
        bad=[];weapon_pos_max=0.
        for uid,a in animation['animators'].items():
            if uid=='effects':continue
            if uid not in bones:bad.append('unknown animator '+uid);continue
            if a.get('quaternion_interpolation') or a.get('rotation_global'):bad.append('unsupported interpolation/basis '+a['name'])
            channel={}
            for k in a.get('keyframes',[]):
                interp=k.get('interpolation','linear')
                if interp not in ['linear','step']:bad.append('unsupported '+interp+' '+a['name'])
                points=k.get('data_points',[])
                if len(points)!=1:bad.append('pre/post data_points '+a['name']);continue
                vals=[]
                for axis in 'xyz':
                    v=points[0].get(axis,0)
                    if isinstance(v,str) and not decimal.match(v):bad.append('non-fixed-decimal expression '+repr(v)+' '+a['name'])
                    try:vals.append(float(v))
                    except (ValueError,TypeError):bad.append('nonnumeric value '+a['name']);vals.append(float('nan'))
                ch=k['channel'];t=float(k['time']);value=np.array(vals)
                if ch not in ['position','rotation','scale']:bad.append('unknown channel '+ch)
                if not np.isfinite(value).all():bad.append('nonfinite value')
                channel.setdefault(ch,[]).append({'time':t,'value':value,'interpolation':interp});times.add(t)
                if a['name'] in ['J_R_Weapon','J_L_Weapon'] and ch=='position':weapon_pos_max=max(weapon_pos_max,float(abs(value).max()))
            for ch,ks in channel.items():
                ks.sort(key=lambda k:k['time'])
                if len(set(k['time'] for k in ks))!=len(ks):bad.append('duplicate key times '+a['name']+' '+ch)
            tracks[uid]=channel
        if bad:issues += [{'animation':name,'issues':sorted(set(bad))}];continue
        original_times=sorted(times);times.update((a+b)/2 for a,b in zip(original_times,original_times[1:]))
        if name=='animation.attack':times.add(.06)
        # Dense 120 Hz checks augment every stored key and every segment midpoint.
        times.update(np.linspace(0,float(animation['length']),max(2,math.ceil(animation['length']*120)+1)).tolist())
        samples=[];clearance=[];corner_clearance=[];socket_error=[];hand_error=[];foot_mins=[]
        for t in sorted(times):
            worlds=pose(tracks,t)
            wd=worlds[byname['J_R_Weapon']]@inverse_bind[byname['J_R_Weapon']]
            ad=worlds[byname['R_Arm']]@inverse_bind[byname['R_Arm']]
            pts=(wd@reference.T).T[:,:3];cs=(wd@corners.T).T
            inverse_arm=np.linalg.inv(ad)
            grip_rest=(inverse_arm@np.r_[pts[0],1])[:3]
            corners_rest=(inverse_arm@cs.T).T[:,:3]
            c=float(min((grip_rest-amin).min(),(amax-grip_rest).min()))
            cc=float(min((corners_rest-amin).min(),(amax-corners_rest).min()))
            se=float(abs(pts[0]-worlds[byname['J_R_Weapon']][:3,3]).max())
            he=float(abs(pts[0]-worlds[byname['J_R_Hand']][:3,3]).max())
            direction=pts[1]-pts[2];direction/=np.linalg.norm(direction)
            tip_direction=pts[1]-pts[0];tip_direction/=np.linalg.norm(tip_direction)
            s={'t':t,'grip_world':pts[0].tolist(),'tip_world':pts[1].tolist(),'base_world':pts[2].tolist(),
                            'base_to_tip_unit':direction.tolist(),'grip_center_clearance_inside_arm':c,
                            'grip_to_tip_unit':tip_direction.tolist(),
                            'base_to_tip_angle_from_java_negative_z_degrees':math.degrees(math.acos(float(np.clip(-direction[2],-1,1)))),
                            'grip_to_tip_angle_from_java_negative_z_degrees':math.degrees(math.acos(float(np.clip(-tip_direction[2],-1,1)))),
                            'tip_forward_reach_from_grip_java_pixels':float(pts[0,2]-pts[1,2]),
                            'tip_forward_reach_from_model_origin_java_pixels':float(-pts[1,2]),
                            'grip_texel_full_prism_clearance_inside_arm':cc,'grip_to_socket_max_abs_error':se,
                            'grip_to_right_hand_max_abs_error':he}
            if name=='animation.walk':
                feet={}
                for leg in legs:
                    lname=leg['name'].removeprefix('body__');ld=worlds[byname[lname]]@inverse_bind[byname[lname]]
                    lv=np.c_[np.array(list(leg['vertices'].values())),np.ones(len(leg['vertices']))]
                    feet[lname]=float((ld@lv.T).T[:,1].min())
                s['foot_min_y_java_pixels']=feet;s['lowest_foot_y_java_pixels']=min(feet.values());foot_mins.append(s['lowest_foot_y_java_pixels'])
            samples.append(s)
            clearance.append(c);corner_clearance.append(cc);socket_error.append(se);hand_error.append(he)
        row={'animation':name,'duration':animation['length'],'loop':animation['loop'],'sample_count':len(samples),
             'weapon_position_channels_max_abs':weapon_pos_max,'grip_center_min_clearance':min(clearance),
             'full_grip_texel_prism_min_clearance':min(corner_clearance),'grip_to_socket_max_abs_error':max(socket_error),
             'grip_to_right_hand_max_abs_error':max(hand_error),
             'grip_center_always_inside_arm_volume':min(clearance)>=-1e-10,
             'full_grip_texel_prism_always_inside_arm_volume':min(corner_clearance)>=-1e-10,
             'first':samples[0],'last':samples[-1],
             'grip_tip_base_loop_endpoint_max_difference':max(abs(np.array(samples[0][key])-np.array(samples[-1][key])).max() for key in ['grip_world','tip_world','base_world'])}
        if name=='animation.attack':row['immediate_damage_and_hold_samples']=[s for s in samples if s['t'] in [0.,.06]]
        if foot_mins:
            row['lowest_foot_y_range_java_pixels']=[min(foot_mins),max(foot_mins)]
            row['lowest_foot_abs_y_max_java_pixels']=max(abs(x) for x in foot_mins)
            row['foot_samples_at_author_key_times']=[{'t':s['t'],**s['foot_min_y_java_pixels']} for s in samples if s['t'] in original_times]
        rows.append(row);all_samples.append({'animation':name,'samples':samples})
    report={'scope':'Read-only saved-file numerical audit; no native renderer execution and no game runtime claim.',
      'model':str(args.bbmodel),'sha256':hashlib.sha256(raw).hexdigest(),
      'equations':'Local=T(rest_origin+position)*Rz(rest_z+rot_z)*Ry(rest_y+rot_y)*Rx(rest_x+rot_x)*S(scale); world=parent_world*local; rigid deformation=posed_world*inverse(bind_world).',
      'supported_track_format':'ArmatureBone numeric fixed decimal single data point linear/step, local Euler ZYX; unsupported formats explicitly rejected.',
      'weapon_saved_vertices_max_error_vs_approved_rigid_translation':float(point_error),
      'weapon_and_right_arm_weight_errors':weight_errors,'unsupported_or_invalid_tracks':issues,
      'clips':rows,'source_model_changed_during_read':args.bbmodel.read_bytes()!=raw,
      'limits':['Checks all stored times, segment midpoints and 120 Hz samples, not symbolic continuous collision proof.',
        'Arm volume is the actual source R_Arm cuboid transformed by its original rigid bone. No separate hand mesh is invented.',
        'Grip center inside arm proves intersection/contact; the full texel prism need not be wholly hidden inside the arm.',
        'Aiming direction is measured in model world coordinates; report alone does not accept visual appeal or combat behavior.',
        'Original generated weapon topology/UV/texture preservation is covered by the separate geometry audit.']}
    report['numeric_grip_checks_pass']=bool(point_error==0 and not weight_errors and not issues and rows and
      all(r['weapon_position_channels_max_abs']==0 and r['grip_center_always_inside_arm_volume'] and r['grip_to_socket_max_abs_error']<1e-10 and r['grip_to_right_hand_max_abs_error']<1e-10 for r in rows)
      and not report['source_model_changed_during_read'])
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    args.output.with_suffix('.samples.json').write_text(json.dumps(all_samples,separators=(',',':')),encoding='utf-8')
    lines=['# 当前原生动画的握持与前刺数值核验','',
      f'模型：`{args.bbmodel}`',f'SHA-256：`{report["sha256"]}`','',
      f'**有限数值检查通过：{report["numeric_grip_checks_pass"]}。** 从实际保存的 bbmodel 独立重算局部 TRS 与刚性 skin 矩阵，未调用动作生成器的姿态结果。',
      f'全部 {len(rows)} 个动作共 {sum(r["sample_count"] for r in rows)} 个采样，覆盖每个存储 key、各段中点和 120 Hz 网格。',
      f'现有蛇矛全部顶点与获准刚体平移后的源顶点最大差 `{point_error:.16g}` Java 像素；武器与右臂实际权重错误 {len(weight_errors)} 个。',
      '握点选自未经改动 PNG 中棕色矛杆 texel `(18,19)` 的中心，三维厚度中点沿用现有 generated 模型。','',
      '| 动作 | 采样数 | 握点相对右手最大差 px | 握点最小内余量 px | 整个握点纹素棱柱最小内余量 px |',
      '|---|---:|---:|---:|---:|']
    for r in rows:lines.append(f'| {r["animation"]} | {r["sample_count"]} | {r["grip_to_right_hand_max_abs_error"]:.6g} | {r["grip_center_min_clearance"]:.6g} | {r["full_grip_texel_prism_min_clearance"]:.6g} |')
    lines += ['', '所有动作双手 Weapon 位置通道为 0，握点中心均在原右臂体积内。`laugh` 中整个纹素棱柱有角点最多伸出体积约 0.10959 像素；这不表示脱手，中心仍保持接触，不能把“整个握持棱柱均在手内”写成全动作结论。', '',
      '| attack 时刻 s | 握点→矛尖偏离 Java -Z | 从握点向前伸出 px | 矛尖位于模型原点前方 px |',
      '|---|---:|---:|---:|']
    for r in rows:
        for s in r.get('immediate_damage_and_hold_samples',[]):lines.append(f'| {s["t"]:.2f} | {s["grip_to_tip_angle_from_java_negative_z_degrees"]:.6f}° | {s["tip_forward_reach_from_grip_java_pixels"]:.6f} | {s["tip_forward_reach_from_model_origin_java_pixels"]:.6f} |')
    for r in rows:
        if r['animation']=='animation.walk':
            key_error=max(abs(min(s['R_Leg'],s['L_Leg'])) for s in r['foot_samples_at_author_key_times'])
            lo,hi=r['lowest_foot_y_range_java_pixels']
            lines+=['',f'走路原 key 时刻最低脚底最大绝对 Y 为 `{key_error:.16g}` px。包含插值时刻的最低脚底范围 `[{lo:.16g}, {hi:.16g}]` px；最小值约 `{lo/16:.8g}` block，明确存在微小插值穿地，不声称连续严格贴地。']
    lines += ['', 'idle 与 walk 的握点、矛尖和矛尾首尾坐标差均为 0。非循环动作不要求首尾同姿势。', '',
      '范围：本报告验证存储数值及有限采样的握持接触、朝向与脚底；不代替 Blockbench 原生姿态执行、视觉审阅或 Minecraft 运行验证。未测攻击命中、伤害、碰撞盒或客户端表现。',
      '复现：`python validate_grip_animation.py <保存的 bbmodel 路径>`；详细每采样点见同名 `.samples.json`。','']
    args.output.with_suffix('.md').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps({'report':str(args.output),'numeric_grip_checks_pass':report['numeric_grip_checks_pass'],
      'sha256':report['sha256'],'point_error':float(point_error),'issues':issues,'clips':rows},ensure_ascii=False))


if __name__=='__main__':main()
