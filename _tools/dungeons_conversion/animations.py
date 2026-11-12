"""Author source-timed UE4.22 animations and explicit mixed-skin eye matrices.

author_animations(document, ref) -> (updated_document, data)
Only the returned copy is changed. This module never writes the reference model.
Ordinary bones retain decoded source keys, with adaptive Euler refinement only
where the measured world error requires it. Four eye surfaces use derived 4x4
absolute BB-world matrices, sampled at source frames and every runtime tick.
"""
from __future__ import annotations

import argparse
from bisect import bisect_right
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
import uuid
import numpy as np

try:
    from .source_math import C, quat_matrix, matrix_to_euler_zyx, euler_zyx_matrix, about, load_source, transform_points, ue_to_java
except ImportError:
    from source_math import C, quat_matrix, matrix_to_euler_zyx, euler_zyx_matrix, about, load_source, transform_points, ue_to_java

NS=uuid.UUID('974ec85b-de4d-5fea-ae53-3a23cdb4ee72')
UE_COMMIT='99a530d4ccbe6bea1e8f49df20acfeb294006962'
CUE_COMMIT='920dc1682278d70ee738383b6fbd3a1e9b7523ea'
UE_URL=f'https://github.com/folgerwang/UnrealEngine/blob/{UE_COMMIT}/Engine/'
CUE_URL=f'https://github.com/FabianFG/CUE4Parse/blob/{CUE_COMMIT}/CUE4Parse-Conversion/'
TIMING_EVIDENCE={
    'contract':'UE4.22 ConstantKeyLerp endpoint time and shortest-path normalized linear quaternion interpolation; CUE FPS is diagnostic only.',
    'no_time_keys':'K>1: key_time[i]=i*SequenceLength/(K-1); K=1 is constant; K=0 keeps rest.',
    'explicit_frame_keys':'key_time[i]=source_frame_index[i]*SequenceLength/(NumFrames-1)',
    'rotation':'UE FastLerp followed by Normalize (shortest-path NLERP), not CUE SLERP',
    'sources':[
        UE_URL+'Build/Build.version',
        UE_URL+'Source/Runtime/Engine/Public/Animation/AnimSequenceDecompressionContext.h#L54',
        UE_URL+'Source/Runtime/Engine/Public/AnimEncoding.h#L587',
        UE_URL+'Source/Runtime/Engine/Public/AnimEncoding.h#L702',
        UE_URL+'Source/Runtime/Engine/Public/AnimEncoding_ConstantKeyLerp.h#L264',
        UE_URL+'Source/Runtime/Core/Public/Math/Quat.h#L1114',
        UE_URL+'Source/Runtime/Engine/Private/Animation/AnimCompositeBase.cpp#L53',
        CUE_URL+'Animations/PSA/CAnimSequence.cs#L37',
        CUE_URL+'Animations/PSA/CAnimTrack.cs#L78',
        CUE_URL+'Animations/AnimConverter.cs#L27'],
    'provenance':'Pinned public mirror of original UE4.22.3 source, not an Epic-hosted URL or runtime capture. CUE commit is the repository commit in installed NuGet 1.2.1 nuspec.',
    'previous_probe_scope':'Earlier source_idle_validation used the CUE FPS/SLERP reference. Its geometry agreement remains a CUE-reference result, not evidence of original UE playback timing.'}

def uid(text):return str(uuid.uuid5(NS,text))
def read(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def unique_times(values):return sorted({round(float(v),12) for v in values})
def numeric_string(value):
    # Blockbench treats exponent notation in strings as a Molang expression.
    text=format(float(value),'.12f').rstrip('0').rstrip('.')
    return '0' if text in ('','-0') else text

def nlerp(a,b,alpha):
    a=np.asarray(a,dtype=float);b=np.asarray(b,dtype=float)
    a=a/np.linalg.norm(a);b=b/np.linalg.norm(b)
    if np.dot(a,b)<0:b=-b
    value=a+(b-a)*alpha
    return value/np.linalg.norm(value)

def source_key_times(track,channel,length,num_frames):
    """Decode the UE runtime time contract, intentionally ignoring CUE FPS."""
    count=len(track.get(channel,[]))
    if count<=1:return np.zeros(count)
    frame_times=track.get(channel+'Time') or track.get('time') or []
    if frame_times:
        if len(frame_times)!=count or num_frames<2:raise ValueError('Invalid explicit key times')
        values=np.asarray(frame_times,dtype=float)*length/(num_frames-1)
    else:values=np.linspace(0.,length,count)
    if not np.isfinite(values).all() or np.any(np.diff(values)<=0):raise ValueError('Key times must strictly increase')
    return values

def sample_channel(times,values,time,rest,rotation=False):
    if len(values)==0:return np.asarray(rest,dtype=float)
    if len(values)==1 or time<=times[0]:return np.asarray(values[0],dtype=float)
    if time>=times[-1]:return np.asarray(values[-1],dtype=float)
    i=bisect_right(times,time)-1
    alpha=(time-times[i])/(times[i+1]-times[i])
    return nlerp(values[i],values[i+1],alpha) if rotation else np.asarray(values[i])+(np.asarray(values[i+1])-values[i])*alpha

def _hierarchy(document):
    groups={g['uuid']:g for g in document['groups']};by_name={g['name']:g for g in document['groups']}
    if len(by_name)!=len(groups):raise ValueError('Duplicate group names')
    parents={};order=[]
    def walk(node,parent):
        group=groups[node['uuid']];name=group['name'];parents[name]=parent;order.append(name)
        for child in node.get('children',[]):
            if isinstance(child,dict):walk(child,name)
    for node in document['outliner']:walk(node,None)
    world={}
    for name in order:
        group=by_name[name];local=about(group['origin'],euler_zyx_matrix(group.get('rotation',[0,0,0])))
        world[name]=world[parents[name]]@local if parents[name] else local
    return by_name,parents,world

class SourceClip:
    def __init__(self, path, bones, documents):
        self.path=Path(path);self.payload=read(path);self.obj=documents[self.path.name.replace('.tracks.json','')]
        self.original_name=self.obj['Name'];self.name=self.original_name.lower()
        self.length=float(self.obj['Properties']['SequenceLength']);self.kind=self.obj['Type']
        self.bones=bones;self.by_name={b['name']:b['index'] for b in bones}
        self.sequence=self.payload['sequences'][0]
        if len(self.payload['sequences'])!=1 or self.sequence.get('IsAdditive'):raise ValueError('This conversion requires one non-additive decoded sequence per asset')
        self.num_frames=int(self.sequence['NumFrames']);self.start=0.;self.end=self.length;self.rate=1.;self.start_pos=0.
        sequence_obj=documents[self.sequence['Name']]
        self.sequence_length=float(sequence_obj['Properties']['SequenceLength'])
        codec=sequence_obj.get('CompressedDataStructure',{})
        if codec.get('KeyEncodingFormat') not in (None,'AKF_ConstantKeyLerp'):raise ValueError('Unreviewed source codec')
        if sequence_obj['Properties'].get('RateScale',1)!=1:raise ValueError('Non-unit RateScale needs an explicit playback policy')
        if self.kind=='AnimComposite':
            segments=self.obj['Properties']['AnimationTrack']['AnimSegments']
            if len(segments)!=1:raise ValueError('Multiple composite segments require explicit support')
            segment=segments[0]
            self.start=float(segment['AnimStartTime']);self.end=float(segment['AnimEndTime'])
            self.rate=float(segment.get('AnimPlayRate',1));self.start_pos=float(segment.get('StartPos',0))
            if self.rate<=0 or segment.get('LoopingCount',1)!=1 or self.start_pos!=0:raise ValueError('Unreviewed composite rate/loop/start position')
            if abs((self.end-self.start)/self.rate-self.length)>2e-6:raise ValueError('Composite segment length mismatch')
        if self.num_frames!=sequence_obj['Properties']['NumFrames']:raise ValueError('Source frame count mismatch')
        tracks={t['boneName']:t for t in self.sequence['tracks']};self.channels=[]
        for b in bones:
            t=tracks.get(b['name'],{});row={}
            if t.get('scale') and np.max(np.abs(np.asarray(t['scale'])-1.))>1e-6:raise ValueError('Animated source scale requires a separately reviewed implementation')
            for channel,rest in (('position',b['translation']),('rotation',b['rotation'])):
                row[channel]=(source_key_times(t,channel,self.sequence_length,self.num_frames),np.asarray(t.get(channel,[]),dtype=float),np.asarray(rest,dtype=float))
            self.channels.append(row)
        self.pose_cache={}
    def source_time(self,time):return min(self.end,max(self.start,self.start+min(self.length,max(0.,time))*self.rate))
    def sample(self,index,channel,time):
        times,values,rest=self.channels[index][channel]
        return sample_channel(times,values,self.source_time(time),rest,channel=='rotation')
    def times(self,index,channel):
        times,values,_=self.channels[index][channel]
        if len(values)<=1:return [0.]
        return unique_times([0.,self.length]+[(t-self.start)/self.rate for t in times if self.start<t<self.end])
    def sample_times(self):
        frames=np.linspace(0.,self.sequence_length,self.num_frames)
        return unique_times([0.,self.length]+[(t-self.start)/self.rate for t in frames if self.start<t<self.end]+[i/20 for i in range(int(math.ceil(self.length*20))+1)])
    def world(self,time):
        key=round(min(self.length,max(0.,time)),12)
        if key not in self.pose_cache:
            result=[]
            for i,b in enumerate(self.bones):
                local=np.eye(4);local[:3,:3]=quat_matrix(self.sample(i,'rotation',key));local[:3,3]=self.sample(i,'position',key)
                result.append(result[b['parent']]@local if b['parent']>=0 else local)
            self.pose_cache[key]=np.asarray(result)
        return self.pose_cache[key]

def continuous_eulers(rotations,reference):
    """Choose both equivalent ZYX branches, then unwrap to the preceding key."""
    previous=np.asarray(reference,dtype=float);out=[]
    for rotation in rotations:
        base=matrix_to_euler_zyx(rotation)
        candidates=[base,np.array([base[0]+180,180-base[1],base[2]+180])]
        candidates=[v+360*np.round((previous-v)/360) for v in candidates]
        choice=min(candidates,key=lambda v:np.linalg.norm(v-previous))
        if np.max(abs(euler_zyx_matrix(choice)-rotation))>2e-7:raise ValueError('Euler branch reconstruction failed')
        out.append(choice);previous=choice
    return np.asarray(out)

def _make_channels(clip,bones,groups,unit_scale,extra_times=None):
    authored={};counts={'source_position_keys':0,'source_rotation_keys':0,'adaptive_rotation_keys':0}
    extra_times=extra_times or {}
    for i,b in enumerate(bones):
        name=b['name'];rest_euler=np.asarray(groups[name].get('rotation',[0,0,0]),dtype=float)
        rt=clip.times(i,'rotation');pt=clip.times(i,'position')
        counts['source_rotation_keys']+=len(rt);counts['source_position_keys']+=len(pt)
        refined=unique_times(rt+list(extra_times.get(i,[])));counts['adaptive_rotation_keys']+=len(refined)-len(rt)
        rotations=[C@quat_matrix(clip.sample(i,'rotation',t))@C.T for t in refined]
        eulers=continuous_eulers(rotations,rest_euler)-rest_euler
        positions=[C@(clip.sample(i,'position',t)-np.asarray(b['translation']))*unit_scale for t in pt]
        # Keep genuine source keys. Collapse only channels constant to numerical precision.
        if np.max(abs(eulers-eulers[0]))<1e-10:refined=refined[:1];eulers=eulers[:1]
        if np.max(abs(np.asarray(positions)-positions[0]))<1e-10:pt=pt[:1];positions=positions[:1]
        authored[name]={'rotation':(np.asarray(refined),np.asarray(eulers)), 'position':(np.asarray(pt),np.asarray(positions))}
    return authored,counts

def authored_world(authored,time,bones,groups):
    world=[]
    for b in bones:
        name=b['name'];rtime,rvalues=authored[name]['rotation'];ptime,pvalues=authored[name]['position']
        rotation=sample_channel(rtime,rvalues,time,[0,0,0])+groups[name].get('rotation',[0,0,0])
        offset=sample_channel(ptime,pvalues,time,[0,0,0])
        local=about(groups[name]['origin'],euler_zyx_matrix(rotation));local[:3,3]+=offset
        world.append(world[b['parent']]@local if b['parent']>=0 else local)
    return np.asarray(world)

def _reference(clip,time,S,Sinv):return S@clip.world(time)@Sinv

def _skin(matrices,source,rest_vertices):
    result=np.zeros_like(rest_vertices)
    hom=np.c_[rest_vertices,np.ones(len(rest_vertices))]
    for j in range(source['weights'].shape[1]):
        values=np.einsum('nij,nj->ni',matrices[source['joint_source_indices'][:,j]],hom)[:,:3]
        result+=values*source['weights'][:,j,None]
    return result

def _validate(authored,clip,source,groups,rest_bb,rest_h_inv,S,Sinv,unit_scale,model_scale):
    rows=[];pivots=np.asarray([groups[b['name']]['origin'] for b in source['bones']]);hom=np.c_[pivots,np.ones(len(pivots))]
    vertex_java=ue_to_java(source['vertices_ue_cm'],unit_scale)
    for time in clip.sample_times():
        current=authored_world(authored,time,source['bones'],groups)
        desired_h=_reference(clip,time,S,Sinv)
        expected_pivots=desired_h[:,:3,3]
        actual_pivots=np.einsum('nij,nj->ni',current,hom)[:,:3]
        bone_error=float(np.linalg.norm(actual_pivots-expected_pivots,axis=1).max()*model_scale)
        desired=_skin(desired_h@rest_h_inv,source,vertex_java)
        actual=_skin(current@np.linalg.inv(rest_bb),source,vertex_java)
        vertex_error=float(np.linalg.norm(actual-desired,axis=1).max()*model_scale)
        rows.append({'time':time,'bone_error_visual_pixels':bone_error,'vertex_error_visual_pixels':vertex_error})
    return rows

def _affine_tracks(clip,records,source,groups,rest_world,rest_h_inv,S,Sinv,unit_scale,model_scale):
    vertex_java=ue_to_java(source['vertices_ue_cm'],unit_scale);out={};errors=[];degenerate=0
    times=unique_times(clip.sample_times()+[i/20 for i in range(int(math.ceil(clip.length*20))+1)])
    # Native source frames and 20 Hz ticks are both retained; times after length
    # carry the clamped endpoint; phase 2 opts into ceil-rounded tick counts.
    posed={t:_skin(_reference(clip,t,S,Sinv)@rest_h_inv,source,vertex_java) for t in times}
    for record in records:
        name=record['part'];indices=record['source_vertex_indices'];p=vertex_java[indices]
        n=np.cross(p[1]-p[0],p[2]-p[0]);n/=np.linalg.norm(n)
        basis=np.column_stack([p[1]-p[0],p[2]-p[0],n]);inv_basis=np.linalg.inv(basis)
        owner=source['bones'][source['joint_source_indices'][indices[0],int(np.argmax(source['weights'][indices[0]]))]]['index']
        frames=[]
        for time in times:
            target=posed[time][indices]
            # The triangle constrains only its plane. Transport a rest unit
            # normal by its first vertex's source owner; this stays finite at
            # complete eyelid collapse, when the in-plane matrix may be rank 1.
            transport=(_reference(clip,time,S,Sinv)@rest_h_inv)[owner,:3,:3]
            normal=transport@n;normal/=np.linalg.norm(normal)
            target_basis=np.column_stack([target[1]-target[0],target[2]-target[0],normal])
            linear=target_basis@inv_basis
            affine=np.eye(4);affine[:3,:3]=linear;affine[:3,3]=target[0]-linear@p[0]
            world=affine@rest_world[name]
            if not np.isfinite(world).all():raise ValueError('Non-finite derived eye affine')
            degenerate+=int(np.linalg.matrix_rank(linear,tol=1e-10)<3)
            local=transform_points(np.linalg.inv(rest_world[name]),p)
            error=float(np.linalg.norm(transform_points(world,local)-target,axis=1).max()*model_scale)
            errors.append(error);frames.append([float(time),world.tolist()])
        out[name]=frames
    return out,{'parts':len(records),'samples_per_part':len(times),'max_source_triangle_error_visual_pixels':max(errors,default=0.),'rank_deficient_samples':degenerate,
                'normal_policy':'Transport rest unit normal by first source vertex owner. Third dimension is unconstrained by triangle; no cross-product division at collapse.',
                'interpolation':'Linear 4x4 matrix interpolation; exact source/tick samples; outside interval clamp.'}

def _bb_animation(clip,channels,groups,loop,affine):
    animators={}
    for name,channel_map in channels.items():
        keys=[]
        for channel,(times,values) in channel_map.items():
            for i,(time,value) in enumerate(zip(times,values)):
                keys.append({'channel':channel,'data_points':[{axis:numeric_string(v) for axis,v in zip('xyz',value)}],
                             'uuid':uid(f'{clip.name}/{name}/{channel}/{i}/{time:.12f}'),'time':float(time),'color':-1,'interpolation':'linear'})
        animators[groups[name]['uuid']]={'name':name,'type':'bone','rotation_global':False,'quaternion_interpolation':False,'keyframes':keys}
    return {'uuid':uid(clip.name),'name':'animation.'+clip.name,'loop':'loop' if loop else 'once','override':False,
            'length':clip.length,'snapping':24,'selected':False,'saved':True,'path':'','scope':0,'anim_time_update':'','blend_weight':'','start_delay':'','loop_delay':'',
            'animators':animators,'dungeons_affine_tracks':affine}

def author_animations(document,ref,*,max_error_visual_pixels=.1):
    """Return a new document and JSON-serializable validation/derived-track data."""
    ref=Path(ref);doc=deepcopy(document);groups,parents,rest_world=_hierarchy(doc)
    settings=doc['display_dungeons'];unit_scale=float(settings['unit_scale_java_pixels_per_ue_cm']);model_scale=float(settings['model_scale'])
    source=load_source(ref/'source/SK_Abomination_02.source.glb',ref/'source/skeleton.meta.json');bones=source['bones']
    if len(bones)!=40 or any(b['name'] not in groups for b in bones):raise ValueError('Expected all 40 source bones')
    if max(np.max(abs(np.asarray(b['scale'])-1)) for b in bones)>1e-6:raise ValueError('Non-unit rest scale unsupported')
    for b in bones:
        expected=bones[b['parent']]['name'] if b['parent']>=0 else None
        if parents[b['name']]!=expected:raise ValueError('Original source bone hierarchy changed')
    S=np.eye(4);S[:3,:3]=C*unit_scale;Sinv=np.linalg.inv(S)
    # Canonicalize only the original exporter float noise in near-unit rest scale.
    rest_ue=[]
    for b in bones:
        local=np.eye(4);local[:3,:3]=quat_matrix(b['rotation']);local[:3,3]=b['translation']
        rest_ue.append(rest_ue[b['parent']]@local if b['parent']>=0 else local)
    rest_h=S@np.asarray(rest_ue)@Sinv;rest_h_inv=np.linalg.inv(rest_h)
    rest_bb=np.asarray([rest_world[b['name']] for b in bones])
    records=settings.get('deforming_source_triangles',[])
    if len(records)!=4:raise ValueError('Expected four separately traced mixed-skin eye triangles')
    settings['deforming_parts']={r['part']:{'source_vertex_indices':r['source_vertex_indices'],'source_vertex_bones':r['vertex_source_bones'],
        'source_rest_vertices_java_internal':r['rest_vertices_java_internal'],'matrix_space':'absolute_BB_world_internal_pixels','derived':True} for r in records}
    animation_dir=ref/'source/animations';documents={p.name.removesuffix('.uobject.json'):read(p) for p in animation_dir.glob('*.uobject.json')}
    inventory=read(ref/'source/inventory_phase2.json')
    provider_names=[row['name'] for row in inventory['animations_provider_order']]
    first=['jungleAbomination_idle','jungleAbomination_walk']
    clip_order=first+[name for name in provider_names if name not in first]
    if clip_order!=inventory['suggested_clip_order_original_names']:raise ValueError('Inventory clip order differs from captured provider order')
    paths=[animation_dir/(name+'.tracks.json') for name in clip_order]
    if set(paths)!=set(animation_dir.glob('*.tracks.json')):raise ValueError('Inventory/source clip list mismatch')
    if len(paths)!=18:raise ValueError('Expected all 18 original animation assets')
    loops={'jungleabomination_idle','jungleabomination_walk','jungleabomination_projectileattack_loop','jungleabomination_vineattackidle','jungleabomination_vulnerablestuncycle'}
    reports=[];animations=[];all_affine={}
    for path in paths:
        clip=SourceClip(path,bones,documents);extra={};iterations=0
        for iterations in range(12):
            channels,counts=_make_channels(clip,bones,groups,unit_scale,extra)
            checks=_validate(channels,clip,source,groups,rest_bb,rest_h_inv,S,Sinv,unit_scale,model_scale)
            bad=[v for v in checks if max(v['bone_error_visual_pixels'],v['vertex_error_visual_pixels'])>max_error_visual_pixels*.8]
            if not bad:break
            added=0
            for row in bad:
                time=row['time']
                for i,b in enumerate(bones):
                    times,values=channels[b['name']]['rotation']
                    value=sample_channel(times,values,time,[0,0,0])+groups[b['name']].get('rotation',[0,0,0])
                    true=C@quat_matrix(clip.sample(i,'rotation',time))@C.T
                    if np.max(abs(euler_zyx_matrix(value)-true))>1e-10 and time not in extra.setdefault(i,set()):extra[i].add(time);added+=1
            if not added:raise ValueError(f'{clip.name}: world error cannot be corrected by Euler refinement: {max(bad,key=lambda x:x["vertex_error_visual_pixels"])}')
        else:raise ValueError(clip.name+': adaptive rotation refinement did not converge')
        affine,affine_report=_affine_tracks(clip,records,source,groups,rest_world,rest_h_inv,S,Sinv,unit_scale,model_scale)
        all_affine[clip.name]=affine
        animation=_bb_animation(clip,channels,groups,clip.name in loops,affine)
        animations.append(animation)
        endpoint_source=_skin(_reference(clip,0,S,Sinv)@rest_h_inv,source,ue_to_java(source['vertices_ue_cm'],unit_scale))
        endpoint_end=_skin(_reference(clip,clip.length,S,Sinv)@rest_h_inv,source,ue_to_java(source['vertices_ue_cm'],unit_scale))
        report={'name':clip.name,'source_name':clip.original_name,'type':clip.kind,'length_seconds':clip.length,
            'sequence_length_seconds':clip.sequence_length,'source_frame_count':clip.num_frames,'ue_effective_fps':(clip.num_frames-1)/clip.sequence_length,
            'cue_reported_fps':clip.sequence['FramesPerSecond'],'source_segment_seconds':[clip.start,clip.end],
            'loop':clip.name in loops,'loop_reason':'Original idle/walk or explicitly named held-cycle/composite Loop; original endpoints retained, not forced equal.' if clip.name in loops else 'One-shot action; hold original final pose.',
            'endpoint_mesh_max_distance_visual_pixels':float(np.linalg.norm(endpoint_end-endpoint_source,axis=1).max()*model_scale),
            'source_keys_and_refinement':counts,'adaptive_passes':iterations,'authored_key_count':sum(len(a['keyframes']) for a in animation['animators'].values()),
            'check_sample_count':len(checks),'max_bone_error_visual_pixels':max(x['bone_error_visual_pixels'] for x in checks),
            'max_vertex_error_visual_pixels':max(x['vertex_error_visual_pixels'] for x in checks),'affine':affine_report,
            'runtime_tick_rounding':'ceil','runtime_tick_count':int(math.ceil(clip.length*20)),
            'runtime_last_sample_seconds':math.ceil(clip.length*20)/20,
            'runtime_period_extension_seconds':math.ceil(clip.length*20)/20-clip.length,
            'samples':checks,'source_tracks_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'source_uobject_sha256':hashlib.sha256(path.with_name(path.name.replace('.tracks.json','.uobject.json')).read_bytes()).hexdigest()}
        reports.append(report)
    doc['animations']=animations;settings['checkpoint']='B_animations_authored'
    settings['animation_timing_contract']=deepcopy(TIMING_EVIDENCE)
    settings['affine_track_contract']={'space':'absolute_BB_world_internal_pixels','storage':'animation.dungeons_affine_tracks[bone_name] = [[time_seconds, row_major_4x4], ...]',
        'application':'Replace accumulated matrix when chain reaches named bone; compose descendants afterward. Clamp outside keys, linearly interpolate 16 matrix components.',
        'normal_policy':'Transported rest normal; full eyelid collapse may have a singular in-plane affine. SVD must support zero scale.',
        'derived':True,'source_bone_tracks':'Only original 40 bones have ordinary position/rotation keyframes; all helper/glow hierarchy unchanged.'}
    if doc['groups']!=document['groups'] or doc['outliner']!=document['outliner'] or doc['elements']!=document['elements'] or doc['textures']!=document['textures']:raise AssertionError('Animation authoring changed static content')
    validation={'status':'pass','clip_count':len(animations),'source_bones':len(bones),'groups_preserved':len(groups),'elements_preserved':len(doc['elements']),
        'clip_order':clip_order,'clip_order_source':'Captured provider_index_ordinal order from source/inventory_phase2.json, with idle/walk first; not authored playback order.',
        'original_lengths_preserved':True,'original_names_lowercased':True,'loop_names':sorted(loops),'error_limit_visual_pixels':max_error_visual_pixels,
        'max_bone_error_visual_pixels':max(r['max_bone_error_visual_pixels'] for r in reports),
        'max_vertex_error_visual_pixels':max(r['max_vertex_error_visual_pixels'] for r in reports),
        'max_affine_triangle_error_visual_pixels':max(r['affine']['max_source_triangle_error_visual_pixels'] for r in reports),
        'sample_scope':'All original source frame times within each exact segment plus every 20 Hz runtime sample and exact endpoints; not a proof over all continuous time.',
        'timing_evidence':TIMING_EVIDENCE,'clips':reports,'rest_scale_canonicalization_tolerance':1e-6,
        'limitations':['Ordinary Euler curves approximate source NLERP only within reported measured error.','Derived eye matrices are required for correct mixed-skin deformation; stock Blockbench does not execute this extension.','Phase 2 opts into ceil-rounded runtime durations, extending the period by less than 50ms. Original document lengths remain exact; source and authored overshoot samples clamp to the endpoint.']}
    return doc,{'validation':validation,'affine_tracks':all_affine,'timing_evidence':deepcopy(TIMING_EVIDENCE)}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--ref',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    args=p.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    document,data=author_animations(read(args.ref/'lucifer_p2.bbmodel'),args.ref)
    for name,value in [('lucifer_p2.animated.bbmodel',document),('animation_validation.json',data['validation']),('affine_tracks.json',data['affine_tracks'])]:
        (args.out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in data['validation'].items() if k not in ('clips','timing_evidence')},indent=2))

if __name__=='__main__':main()
