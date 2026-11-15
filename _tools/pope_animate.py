"""教皇 M3 制作脚本：原生 Blockbench 导入、导出；不接入构建。

从用户确认的 B 眼神 M2 快照和有证据标记的数值姿态生成动画。
保存后 pope.bbmodel 是事实来源；重建必须显式 --replace-authored。
只有 rotation/position，世界空间约束在制作时求解为普通数字轨道。
"""
from __future__ import annotations
import argparse, copy, hashlib, json, math, uuid, warnings
from pathlib import Path
from types import SimpleNamespace
import numpy as np
from scipy.spatial.transform import Rotation
import display_mob as dm
from pope_blockbench import BlockbenchMCP

REF = Path(__file__).resolve().parent / 'pope_ref'
OUT = REF / 'm3'
ORDER = ['idle','walk','attack','summon','cast','appear','teleport_in','teleport_out','whirlwind']
LENGTHS = [4,1.8,1.25,2,2.5,1.8,.9,.9,7]
BASE_SHA = '4f2d24f9c5da774cbf0be44d7895c7a449bd7a1f8f1442dcbd1f2eed83c575aa'
END_CENTER = np.array([0.,12.,0.])

def read(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def write(path, obj):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def uid(label): return str(uuid.uuid5(uuid.NAMESPACE_URL, 'tralancer/pope/m3/'+label))
def point(m,p): return (m @ np.r_[p,1])[:3]
def matrix(rot): return np.array(dm.euler(rot),float)
def angles(rot,previous=None):
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        a=Rotation.from_matrix(rot[:3,:3]).as_euler('xyz',degrees=True)
    if previous is not None:
        candidates=[a,a+np.array([180,180-2*a[1],180])]
        candidates=[v+360*np.round((previous-v)/360) for v in candidates]
        a=min(candidates,key=lambda v:float(np.linalg.norm(v-previous)))
    return a

class Rig:
    def __init__(self):
        self.base=OUT/'accepted_m2.bbmodel'
        if sha(self.base)!=BASE_SHA: raise ValueError('M2快照已变化')
        self.doc=read(self.base); self.spec=read(REF/'m2/model_spec.json')
        self.bones,_,self.res=dm.load_bbmodel(SimpleNamespace(bbmodel=self.base))
        self.centers={}
        mob=SimpleNamespace(key='pope',tex='rpg:item/pope/atlas',glow=set(self.spec['glow']))
        for part,members in self.spec['parts']:
            _,k=dm.part_model(mob,self.bones,part,members,self.res)
            self.centers[part]=np.array(k)+8
        self.names=list(self.bones)
        self.animated=[n for n in self.names if n=='root' or n in self.centers]

    def pose(self,values,previous=None):
        """Evaluate parent-first; globals are authored constraints, never runtime channels."""
        world,local={},{}
        for name,b in self.bones.items():
            val=values.get(name,{})
            parent=world[b['parent']] if b['parent'] else np.eye(4)
            pivot=np.array(b['pivot']); rest=np.array(b['rotation'])
            rot=np.array(val.get('rotation',[0,0,0]),float)
            pos=np.array(val.get('position',[0,0,0]),float)
            if 'world_rotation' in val:
                desired=matrix(val['world_rotation'])
                lr=np.linalg.inv(parent)@desired
                rot=angles(lr,None if previous is None else previous[name]['rotation']+rest)-rest
            w=parent@np.array(dm.translate(*pos))@np.array(dm.about(pivot,(rest+rot).tolist()))
            if 'world_matrix' in val:
                w=np.array(val['world_matrix'],float)
                lm=np.linalg.inv(parent)@w
                absolute=angles(lm,None if previous is None else previous[name]['rotation']+rest)
                rot=absolute-rest
                pos=lm[:3,3]-pivot+lm[:3,:3]@pivot
            elif 'world_point' in val:
                anchor=np.array(val.get('anchor',pivot))
                delta=np.array(val['world_point'])-point(w,anchor)
                pos+=parent[:3,:3].T@delta
                w=parent@np.array(dm.translate(*pos))@np.array(dm.about(pivot,(rest+rot).tolist()))
            world[name]=w
            local[name]={'rotation':rot,'position':pos}
        return world,local

def interpolate(rows,time):
    """Keyed authoring curves. Values are bone=>rotation/position/world constraints."""
    if time<=rows[0]['time']:return copy.deepcopy(rows[0]['pose'])
    if time>=rows[-1]['time']:return copy.deepcopy(rows[-1]['pose'])
    a,b=next((a,b) for a,b in zip(rows,rows[1:]) if a['time']<=time<=b['time'])
    u=(time-a['time'])/(b['time']-a['time'])
    result={}
    for bone in a['pose'].keys()|b['pose'].keys():
        av,bv=a['pose'].get(bone,{}),b['pose'].get(bone,{})
        result[bone]={}
        for ch in av.keys()|bv.keys():
            if ch in ('anchor',):result[bone][ch]=av.get(ch,bv.get(ch));continue
            x=np.array(av.get(ch,bv.get(ch) if ch.startswith('world') else [0,0,0]))
            y=np.array(bv.get(ch,av.get(ch) if ch.startswith('world') else [0,0,0]))
            result[bone][ch]=(x*(1-u)+y*u).tolist()
    return result

def base_rows():
    """Idle measured as near-still; walk source gait repeats four times in 1.8s.
    Amplitudes/depth are reconstructed, not extracted original bone curves.
    """
    result={}
    idle=[]
    for t in np.arange(0,4.001,.25):
        wave=math.sin(t*math.pi/2)
        idle.append({'time':round(float(t),4),'pose':{
            'body':{'rotation':[0,0,.45*wave],'position':[0,.10*wave,0]},
            'head':{'rotation':[.35*wave,0,-.35*wave]},
            'left_arm':{'rotation':[0,0,.25*wave]},
            'right_arm':{'rotation':[0,0,-.3*wave]},
            'left_hand':{'world_rotation':[0,0,0]},
            'staff_glow':{'rotation':[0,90*t,0]}}})
    result['idle']=idle
    walk=[]
    # The first cycle is traced with a forward kick at source f5/f6=.15/.18s,
    # passing below hip at f10=.30s, and recovered at f15=.45s.
    for t in np.arange(0,1.8001,.05):
        phase=2*math.pi*t/.45
        kick=float(np.interp(t%.45,[0,.05,.10,.15,.20,.25,.30,.35,.40,.45],[-15,15,45,65,65,50,0,-35,-45,-15]))
        bounce=(1-math.cos(2*phase))*.45
        walk.append({'time':round(float(t),4),'pose':{
            'body':{'rotation':[-25,0,2*math.sin(phase)],'position':[0,.4+bounce,0]},
            'head':{'rotation':[33,0,-math.sin(phase)]},
            'left_arm':{'rotation':[0,-72,-20]},
            'left_hand':{'world_rotation':[0,-8,4]},
            'staff':{'position':[0,5,0]},
            'right_arm':{'rotation':[10*math.cos(phase),22*math.sin(phase),35+10*math.sin(phase)]},
            'right_leg':{'rotation':[kick+20,0,0]},
            'left_leg':{'rotation':[-kick-10,0,0]},
            'cape':{'rotation':[-15-8*math.sin(phase-.5),0,0]},
            'staff_glow':{'rotation':[0,200*t,0]}}})
    result['walk']=walk
    return result

def metadata(rows):
    source=read(REF/'m1/motion/clips.json')
    data={'stage':'M3 review; no runtime integration','source_of_truth':'../pope.bbmodel',
          'model_scale':read(REF/'m2/model_spec.json')['model_scale'],
          'whirlwind_end_center_model':END_CENTER.tolist(),'whirlwind_handoff_time':7.0,
          'carrier_seat':2.0,'clips':[]}
    for i,(name,length) in enumerate(zip(ORDER,LENGTHS)):
        ref=source['clips'][i]
        if name=='whirlwind':
            for k in ref['key_poses']:
                if k['source_frame']==67:k.update(source_frame=68,source_time_seconds=2.72)
        data['clips'].append({'id':i,'name':name,'length':length,'loop':i<2,
            'release_times':{'attack':[.5],'summon':[.65],'cast':[.9]}.get(name,[]),
            'sample_times':sorted({0.,length}|{k['proposed_clip_time_seconds'] for k in ref['key_poses']}),
            'evidence':ref['evidence'],'source_key':ref['source_key'],
            'source_range_seconds':ref['source_range_seconds'],'key_poses':ref['key_poses'],
            'adaptation':ref['note']})
    return data

def compile_motion(rig,rows):
    doc=copy.deepcopy(rig.doc);doc['animations']=[]
    audits=[]
    for name,length in zip(ORDER,LENGTHS):
        if name not in rows: continue
        previous_world={}
        for row in rows[name]:
            for bone,v in row['pose'].items():
                if 'world_rotation' in v:
                    a=angles(matrix(v['world_rotation']),previous_world.get(bone))
                    v['world_rotation']=a.tolist();previous_world[bone]=a
        times={round(i/20,5) for i in range(round(length*20)+1)}|{r['time'] for r in rows[name]}
        if name=='attack':
            # Rapid parent/hand compensation needs more than one Euler interval
            # per game tick. These are ordinary numeric authoring keys; the
            # common pipeline still bakes at its own normal20TPS.
            times.update(round(float(t),5) for t in np.arange(.4,.75001,.005))
        times=sorted(times)
        tracks={n:{'rotation':[],'position':[]} for n in rig.animated}
        prev=None;end_start=None
        for time in times:
            values=interpolate(rows[name],min(time,6.4) if name=='whirlwind' else time)
            if name=='attack':
                posed=rig.pose(values)[0]
                core=point(posed['staff_glow'],rig.bones['staff_glow']['pivot'])
                if core[1]<1:
                    hand_pivot=point(posed['left_hand'],rig.bones['left_hand']['pivot'])
                    v=core-hand_pivot;radius=np.linalg.norm(v);desired=v.copy()
                    desired[1]=1-hand_pivot[1]
                    if abs(desired[1])>=radius:raise ValueError('无法仅用手腕转动保持杖顶离地')
                    horizontal=np.linalg.norm(v[[0,2]])
                    desired[[0,2]]*=math.sqrt(radius**2-desired[1]**2)/horizontal
                    turn=Rotation.align_vectors([desired/radius],[v/radius])[0].as_matrix()
                    fixed=posed['left_hand'].copy();fixed[:3,:3]=turn@fixed[:3,:3]
                    values.setdefault('left_hand',{})['world_rotation']=angles(fixed).tolist()
            if name=='whirlwind' and time>6.4:
                if end_start is None:end_start=rig.pose(interpolate(rows[name],6.4))[0]
                alpha=(time-6.4)/.6
                values=copy.deepcopy(values)
                for bone,center in rig.centers.items():
                    w=end_start[bone].copy()
                    w[:3,3]+=alpha*(END_CENTER-point(w,center))
                    values[bone]={'world_matrix':w.tolist()}
            world,local=rig.pose(values,prev)
            prev=local
            for bone in tracks:
                for channel in tracks[bone]: tracks[bone][channel].append((time,local[bone][channel].tolist()))
        animators={}
        for bone,channels in tracks.items():
            keys=[]
            for channel,values in channels.items():
                if max(abs(v) for _,value in values for v in value)<1e-8:continue
                for i,(time,value) in enumerate(values):
                    # BB stores numbers as strings; below1e-6 JS emits exponent
                    # notation (e.g.1e-7), which its Molang parser misreads.
                    # Six decimal places avoid that parser path and retain <1e-4
                    # model-unit endpoint precision. These are not expressions.
                    safe=[round(float(v),6) for v in value]
                    safe=[0 if abs(v)<1e-6 else v for v in safe]
                    keys.append({'uuid':uid(f'{name}/{bone}/{channel}/{i}'),'channel':channel,'time':time,
                        'color':-1,'interpolation':'linear','data_points':[dict(zip('xyz',safe))]})
            if keys:
                group=next(g for g in doc['groups'] if g['name']==bone)
                animators[group['uuid']]={'name':bone,'type':'bone','keyframes':keys}
        doc['animations'].append({'uuid':uid('animation/'+name),'name':'animation.'+name,
            'loop':'loop' if name in ('idle','walk') else 'once','override':False,'length':length,
            'snapping':20,'selected':False,'anim_time_update':'','blend_weight':'','start_delay':'','loop_delay':'','animators':animators})
        audits.append({'clip':name,'samples':len(times),'keyframes':sum(len(a['keyframes']) for a in animators.values())})
    return doc,audits

def native_export(doc):
    client=BlockbenchMCP()
    state_path=OUT/'blockbench_project.json'
    prior=read(state_path) if state_path.exists() else {}
    projects=client.evaluate('(function(){return ModelProject.all.map(p=>({uuid:p.uuid,name:p.name}));})()')
    old=next((p for p in projects if p['uuid']==prior.get('uuid') and p['name']=='pope_m3_motion'),None)
    if old:
        client.evaluate("(async function(){const p=ModelProject.all.find(p=>p.uuid==="+json.dumps(old['uuid'])+");if(!p||p.name!=='pope_m3_motion')throw Error('项目隔离');p.select();p.saved=true;await p.close();return true;})()")
    client.tool('create_project',{'name':'pope_m3_motion','format':'bedrock'})
    static=copy.deepcopy(doc);static['animations']=[]
    serialized=json.dumps(static,ensure_ascii=False).replace('/',r'\u002f')
    info=client.evaluate("(function(){if(Project.name!=='pope_m3_motion')throw Error('项目隔离');Codecs.project.parse("+serialized+");Project.name='pope_m3_motion';return {uuid:Project.uuid,name:Project.name,animations:Animation.all.length};})()")
    prefix="const p=ModelProject.all.find(p=>p.uuid==="+json.dumps(info['uuid'])+");if(!p||p.name!=='pope_m3_motion')throw Error('项目隔离');p.select();"
    # Avoid a multi-megabyte risky_eval source, which can crash the renderer.
    # Native Animation constructor, one clip at a time; all tracks remain ordinary numeric BB keys.
    for animation in doc['animations']:
        serialized=json.dumps(animation,ensure_ascii=False).replace('/',r'\u002f')
        client.evaluate('(function(){'+prefix+'new Animation('+serialized+').add();return Animation.all.length;})()')
    info['animations']=len(doc['animations'])
    actual=client.evaluate('(function(){'+prefix+'return Codecs.project.compile({raw:true});})()')
    # Compare authored numeric keyframes with native export before saving.
    for before,after in zip(doc['animations'],actual['animations']):
        for prop in ('name','length','loop'):assert before[prop]==after[prop],prop
        for bone,anim in before['animators'].items():
            b={(k['channel'],k['uuid']):k for k in anim['keyframes']}
            a={(k['channel'],k['uuid']):k for k in after['animators'][bone]['keyframes']}
            assert a.keys()==b.keys()
            for key,k in b.items():
                assert abs(k['time']-a[key]['time'])<.000006
                for axis in 'xyz':assert abs(float(k['data_points'][0][axis])-float(a[key]['data_points'][0][axis]))<.000006
    from pope_validate_motion import semantic_static,canonical_hash
    spec=read(REF/'m2/model_spec.json')
    assert canonical_hash(semantic_static(actual,spec))==canonical_hash(semantic_static(doc,spec))
    write(REF/'pope.bbmodel',actual)
    write(state_path,info)
    client.evaluate('(function(){'+prefix+'Project.save_path='+json.dumps(str(REF/'pope.bbmodel'))+';Project.saved=true;return true;})()')
    return info

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--replace-authored',action='store_true');ap.add_argument('--loops-only',action='store_true');args=ap.parse_args()
    if read(REF/'pope.bbmodel').get('animations') and not args.replace_authored:raise ValueError('已有动作，须核对无手改并显式 --replace-authored')
    rig=Rig();rows=base_rows()
    if not args.loops_only:
        rows.update(read(OUT/'action_poses.json')['clips'])
        rows.update(read(OUT/'transition_poses.json')['clips'])
        assert set(rows)==set(ORDER)
    write(OUT/'loop_poses.json',{'evidence':'有动图；姿态幅度/深度与骨骼曲线为人工重建','clips':base_rows()})
    doc,audit=compile_motion(rig,rows)
    info=native_export(doc)
    write(OUT/'clipmeta.json',metadata(rows))
    write(OUT/'authoring_audit.json',{'model_sha256':sha(REF/'pope.bbmodel'),'accepted_m2_sha256':BASE_SHA,'native_project':info,
        'unrecorded_manual_edits':False,'native_roundtrip_numeric_tracks':True,'clips':audit})
    print(json.dumps({'sha256':sha(REF/'pope.bbmodel'),'native_project':info,'clips':audit},ensure_ascii=False))

if __name__=='__main__':main()
