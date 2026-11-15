"""正式 HE/AV 数据包的隔离 1.21.11 运行验证，不操作玩家世界。

python _tools/heart_of_ender_final_test.py --datapack <已构建快照的数据包目录>
复用已接受 EULA 原字节；只在 heart_of_ender_ref/final_validation 下写测试证据。
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import io
import json
import math
import os
from pathlib import Path
import re
import shutil
import socket
import sys
import time
import traceback
import zipfile

import heart_of_ender_motion_probe_test as old_probe
from mc_env import JAVA, JAR, VJSON

HERE=Path(__file__).resolve().parent
OUT=HERE/'heart_of_ender_ref/final_validation'
OBJ='he_final_test'
old_probe.OBJ=OBJ  # only the imported task-local Server.step helper uses this.
Server=old_probe.Server

def read(p):return json.loads(Path(p).read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,data):Path(p).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

def transform(text):
    output={}
    for field in ['translation','left_rotation','scale','right_rotation']:
        match=re.search(r'\b'+field+r':\s*\[([^\]]+)\]',text)
        if not match:raise ValueError('缺少transform字段 '+field)
        output[field]=[float(x.strip().rstrip('fFdD')) for x in match.group(1).split(',')]
    return output

def native_semantics(left,right):
    """Explicit native serializer defaults, numeric strings and <=1e-5 rounding.

    Keep the strict equality fields in the report as well; this comparator must
    not turn actual schema omissions or animation changes into a pass.
    """
    defaults={'isOpen':False,'rotation_global':False,'quaternion_interpolation':False,
        'path':'','scope':0,'saved':True,'selected':False,'rotation':[0,0,0],
        'visibility':True,'inflate':0,'locked':False,'allow_mirror_modeling':True,'render_order':'default'}
    differences=[];accepted=[];maximum=[0.0];missing=object()
    def visit(a,b,path):
        if a==b:return
        if isinstance(a,dict)and isinstance(b,dict):
            for k in sorted(a.keys()|b.keys()):
                x,y=a.get(k,missing),b.get(k,missing)
                if x is missing or y is missing:
                    existing=y if x is missing else x
                    # Installed Blockbench 5.2.2 has ten editor marker colors;
                    # cube construction assigns a random index in 0..9.
                    editor_color=k=='color'and re.fullmatch(r'/(?:elements|groups)/\d+',path)and isinstance(existing,int)and 0<=existing<=9
                    if k in defaults and existing==defaults[k] or editor_color:
                        accepted.append({'path':path+'/'+k,'kind':'native default/editor field','value':existing});continue
                    differences.append({'path':path+'/'+k,'kind':'missing field','source_missing':x is missing,'export_missing':y is missing});continue
                visit(x,y,path+'/'+k)
        elif isinstance(a,list)and isinstance(b,list):
            if len(a)!=len(b):differences.append({'path':path,'kind':'list length','source':len(a),'export':len(b)})
            else:
                for i,(x,y)in enumerate(zip(a,b)):visit(x,y,path+'/'+str(i))
        else:
            x,y=a,b
            if '/data_points/'in path and path.rsplit('/',1)[-1]in ['x','y','z']:
                try:x,y=float(a),float(b)
                except (TypeError,ValueError):pass
            if isinstance(x,(int,float))and not isinstance(x,bool)and isinstance(y,(int,float))and not isinstance(y,bool):
                delta=abs(x-y);maximum[0]=max(maximum[0],delta)
                if delta<=1e-5:
                    accepted.append({'path':path,'kind':'number representation/rounding','delta':delta});return
            differences.append({'path':path,'kind':'value','source':a,'export':b})
    visit(left,right,'')
    return {'equal_with_native_normalization':not differences,'maximum_numeric_delta':maximum[0],
        'unexplained_differences':differences,'accepted_normalizations':accepted,'tolerance':1e-5}

def compare_native():
    from PIL import Image
    rows=[];directory=OUT/'native_validation'
    for source in sorted(directory.glob('*_input.bbmodel')):
        target=source.with_name(source.name.replace('_input.bbmodel','_roundtrip.bbmodel'))
        if not target.exists():continue
        a,b=read(source),read(target);deltas=[];maximum=0.0
        for x,y in zip(a['elements'],b['elements']):
            diff={k:{'before':x.get(k),'after':y.get(k)}for k in x.keys()|y.keys()if x.get(k)!=y.get(k)}
            if diff:deltas.append({'element':x['name'],'changes':diff})
            for k in ['from','to','origin','rotation']:
                xx,yy=x.get(k,[0,0,0]),y.get(k,[0,0,0])
                maximum=max(maximum,max((abs(u-v)for u,v in zip(xx,yy)),default=0.0))
        def rgba(doc):
            return Image.open(io.BytesIO(base64.b64decode(doc['textures'][0]['source'].split(',')[1]))).convert('RGBA').tobytes()
        uv=lambda d:[(e['uuid'],e['faces'])for e in d['elements']]
        model=source.name.removesuffix('_input.bbmodel')
        authoritative=HERE/(model+'_ref')/(model+'.bbmodel')
        row={'model':model,'source_sha256':sha(source),'native_export_sha256':sha(target),
            'authoritative_source':str(authoritative),'authoritative_sha256':sha(authoritative),
            'input_matches_current_authoritative_source':sha(source)==sha(authoritative),
            'native_application':'Blockbench 5.2.2 installed desktop; CUA File Open and Save Project As',
            'counts':{k:[len(a.get(k,[])),len(b.get(k,[]))]for k in ['elements','groups','animations','textures']},
            'animations_equal':a['animations']==b['animations'],'groups_equal':a['groups']==b['groups'],
            'outliner_equal':a['outliner']==b['outliner'],'face_uv_texture_tint_equal':uv(a)==uv(b),
            'atlas_rgba_equal':rgba(a)==rgba(b),'unhandled_root_fields_equal':a.get('unhandled_root_fields')==b.get('unhandled_root_fields'),
            'maximum_geometry_rounding_delta':maximum,'element_differences':deltas,
            'changed_top_level_keys':[k for k in a.keys()|b.keys()if a.get(k)!=b.get(k)],
            'source_name':a.get('name'),'export_name':b.get('name')}
        fields=['elements','groups','outliner','animations']
        row['semantic_comparison']=native_semantics({k:a[k]for k in fields},{k:b[k]for k in fields})
        # Blockbench's JSON encoder also rounds floating-point values inside
        # custom metadata. Keep strict equality above, permit only numeric
        # normalization here, and reject missing/default metadata fields.
        metadata=native_semantics(a.get('unhandled_root_fields'),b.get('unhandled_root_fields'))
        metadata['only_numeric_normalization']=all(c['kind']=='number representation/rounding' for c in metadata['accepted_normalizations'])
        row['metadata_semantic_comparison']=metadata
        row['keyframes_count']=[sum(len(animator.get('keyframes',[]))for animation in doc['animations']for animator in animation.get('animators',{}).values())for doc in [a,b]]
        row['passed']=row['input_matches_current_authoritative_source']and row['semantic_comparison']['equal_with_native_normalization']and row['atlas_rgba_equal']and metadata['equal_with_native_normalization']and metadata['only_numeric_normalization']and all(x==y for x,y in row['counts'].values())
        rows.append(row)
    report={'native_codec_verified':True,'tests':rows,'all_passed':{r['model']for r in rows}=={'heart_of_ender','arch_visage'}and all(r['passed']for r in rows),
        'limits':['Native Save As adds default editor fields and rounds floats, including custom metadata, to five decimals; strict equality fields remain reported and byte identity is not claimed','Original model files were not overwritten; this is a codec/schema roundtrip, not Minecraft client visual validation']}
    write(OUT/'native_report.json',report)
    print(json.dumps({'native_roundtrips':len(rows),'passed':report['all_passed']},ensure_ascii=False))
    if not report['all_passed']:raise SystemExit(1)

class Tests:
    def __init__(self,server,pack,report):self.s=server;self.pack=pack;self.report=report
    def check(self,condition,label,dimension='overworld'):
        self.s.seq+=1;token=f'HE_FINAL_ASSERT_{self.s.seq:04d}';start=len(self.s.lines)
        self.s.send(f'scoreboard players set #assert {OBJ} 0',
            f'execute in minecraft:{dimension} {condition} run scoreboard players set #assert {OBJ} 1',
            f'execute if score #assert {OBJ} matches 1 run say {token}_PASS',
            f'execute if score #assert {OBJ} matches 0 run say {token}_FAIL')
        line=self.s.wait(token,start,20);ok=token+'_PASS' in line
        self.report['checks'].append({'name':label,'passed':ok,'condition':condition,'dimension':dimension,'console':line})
        if not ok:print('FAIL '+label,flush=True)
        return ok
    def score(self,sel,obj,value,label,dim='overworld'):
        return self.check(f'if score {sel} {obj} matches {value}',label,dim)
    def count(self,selector,wanted,label,dim='overworld'):
        self.s.barrier(f'scoreboard players set #count {OBJ} 0',
            f'execute in minecraft:{dim} as {selector} run scoreboard players add #count {OBJ} 1')
        return self.score('#count',OBJ,wanted,label,dim)
    def cmd(self,m,entry,sel=None,dim='overworld',pos='8.5 80 8.5'):
        context=f'in minecraft:{dim} positioned {pos}'
        if sel:context+=f' as {sel} at @s'
        self.s.barrier(f'execute {context} run function rpg:{m["key"]}/debug/{entry}')
    def spawn(self,m,label,pos='8.5 80 8.5',dim='overworld'):
        self.cmd(m,'spawn',dim=dim,pos=pos)
        self.s.barrier(f'execute in minecraft:{dim} positioned {pos} run tag @e[type=armor_stand,tag={m["carrier_tag"]},distance=..1,sort=nearest,limit=1] add {label}')
        return f'@e[type=armor_stand,tag={label},distance=0..,limit=1]'
    def frame(self,m,clip,tick,carrier,dim='overworld'):
        expected={};tag=m['carrier_tag']
        for n in range(tick+1):
            path=self.pack/f'data/rpg/function/{m["key"]}/anim/{clip}/f{n}.mcfunction'
            for line in path.read_text(encoding='utf8').splitlines():
                name=re.search(r'tag='+re.escape(tag)+r'\.p\.([a-z0-9_]+)',line)
                if name and 'transformation:' in line:expected[name.group(1)]=transform(line.split('transformation:',1)[1])
        if len(expected)!=m['part_count']:raise ValueError('累计帧部件数量不匹配')
        commands=[]
        for part in expected:
            commands.append(f'execute in minecraft:{dim} as {carrier} on passengers if entity @s[tag={tag}.p.{part}] run data get entity @s transformation')
        start=len(self.s.lines);self.s.barrier(*commands)
        outputs=[line for line in self.s.lines[start:] if 'has the following entity data:' in line]
        if len(outputs)!=len(expected):raise ValueError(f'实际部件数据读取数量错误: {len(outputs)}/{len(expected)}')
        samples=[]
        for (part,target),line in zip(expected.items(),outputs):
            actual=transform(line);errors={}
            for field,wanted in target.items():
                if field.endswith('rotation'):
                    length=math.sqrt(sum(v*v for v in wanted));wanted=[v/length for v in wanted]
                    errors[field]=min(max(abs(a-b)for a,b in zip(actual[field],wanted)),max(abs(a+b)for a,b in zip(actual[field],wanted)))
                else:errors[field]=max(abs(a-b)for a,b in zip(actual[field],wanted))
            samples.append({'part':part,'target':target,'actual':actual,'errors':errors})
        error=max(v for row in samples for v in row['errors'].values());ok=error<=1e-6
        self.report['checks'].append({'name':f'{m["key"]}/{clip} f{tick} 实体目标变换','passed':ok,
            'maximum_error':error,'tolerance':1e-6,'samples':samples,'dimension':dim})
        if not ok:print(f'FAIL {m["key"]}/{clip} f{tick}: {error}',flush=True)
    def rig(self,m):
        key=m['key'];tag=m['carrier_tag'];sc=m['scoreboards'][0].removesuffix('_anim')
        self.cmd(m,'clear_all');a=self.spawn(m,'he_final_A')
        initial=m.get('runtime',{}).get('initial_clip','spawn_attack' if key=='arch_visage' else 'idle')
        self.score(a,sc+'_anim',m['clips'][initial]['id'],key+'/'+initial+'召唤初始片段')
        self.score(a,sc+'_t',0,key+'召唤第0帧')
        self.score(a,sc+'_run',1,key+'召唤播放状态');self.frame(m,initial,0,a)
        self.count(f'@e[tag={tag},type=armor_stand,distance=0..]',1,key+'单实例')
        self.count(f'@e[tag={tag}.part,type=item_display,distance=0..]',m['part_count'],key+'部件数量')
        self.s.barrier(f'execute store result score #passengers {OBJ} run data get entity {a} Passengers')
        self.score('#passengers',OBJ,m['part_count'],key+'真实Passengers数量')
        self.s.barrier(f'scoreboard players set #bad {OBJ} 0',
            f'execute as {a} on passengers unless score @s {sc}_id = {a} {sc}_id run scoreboard players add #bad {OBJ} 1')
        self.score('#bad',OBJ,0,key+'每个乘客owner id等于其载体')
        self.s.step(2)
        for axis in range(3):
            self.s.barrier(f'execute store result score #carrier_pos {OBJ} run data get entity {a} Pos[{axis}] 1000000',
                f'scoreboard players set #bad {OBJ} 0',
                f'execute as {a} on passengers store result score @s {OBJ} run data get entity @s Pos[{axis}] 1000000',
                f'execute as {a} on passengers unless score @s {OBJ} = #carrier_pos {OBJ} run scoreboard players add #bad {OBJ} 1')
            self.score('#bad',OBJ,0,key+f'乘客Pos[{axis}]与载体一致')
        for clip,info in m['clips'].items():
            self.cmd(m,'anim/'+clip,a)
            self.score(a,sc+'_anim',info['id'],key+'/'+clip+'编号')
            self.score(a,sc+'_t',0,key+'/'+clip+'初始帧');self.frame(m,clip,0,a)
            for end in sorted(set([min(5,info['ticks']//2),info['ticks']//2,info['last_tick']])):
                current=0 if end==min(5,info['ticks']//2) else previous
                if end>current:self.s.step(end-current)
                self.score(a,sc+'_t',end,key+'/'+clip+f'运行到{end}tick');self.frame(m,clip,end,a)
                previous=end
            if info['loop']:
                self.s.step(1);self.score(a,sc+'_t',0,key+'/'+clip+'循环回0')
                self.score(a,sc+'_run',1,key+'/'+clip+'循环仍播放');self.frame(m,clip,0,a)
            else:
                self.score(a,sc+'_run',2,key+'/'+clip+'单次结束')
                self.s.step(5);self.cmd(m,'resume',a);self.s.step(2)
                self.score(a,sc+'_t',info['ticks'],key+'/'+clip+'结束后保持末帧')
                self.score(a,sc+'_run',2,key+'/'+clip+'结束后resume不重启')
            print('已实测 '+key+'/'+clip,flush=True)
        for clip in ['walk',next(n for n,c in m['clips'].items()if not c['loop'])]:
            self.cmd(m,'anim/'+clip,a);self.s.step(7);self.cmd(m,'pause',a);self.s.step(9)
            self.score(a,sc+'_run',0,key+'/'+clip+'暂停状态');self.score(a,sc+'_t',7,key+'/'+clip+'暂停保持')
            self.frame(m,clip,7,a);self.cmd(m,'resume',a);self.s.step(3)
            self.score(a,sc+'_t',10,key+'/'+clip+'恢复继续');self.frame(m,clip,10,a)
            self.cmd(m,'stop',a);self.s.step(5)
            self.score(a,sc+'_anim',0,key+'/'+clip+'stop返回idle');self.score(a,sc+'_t',0,key+'/'+clip+'stop第0帧')
            self.score(a,sc+'_run',0,key+'/'+clip+'stop静态');self.frame(m,'idle',0,a)
        # Four instances cover nearest selection and every vanilla dimension.
        b=self.spawn(m,'he_final_B','24.5 80 8.5');c=self.spawn(m,'he_final_C',dim='the_nether')
        d=self.spawn(m,'he_final_D',dim='the_end')
        instances=[(a,'overworld','A'),(b,'overworld','B'),(c,'the_nether','C'),(d,'the_end','D')]
        for sel,dim,label in instances:
            self.s.barrier(f'execute in minecraft:{dim} run scoreboard players operation #id_{label} {OBJ} = {sel} {sc}_id',
                f'scoreboard players set #bad {OBJ} 0',
                f'execute in minecraft:{dim} as {sel} on passengers unless score @s {sc}_id = #id_{label} {OBJ} run scoreboard players add #bad {OBJ} 1')
            self.score('#bad',OBJ,0,key+'/'+label+'跨维实例乘客归属正确')
        for i,left in enumerate('ABCD'):
            for right in 'ABCD'[i+1:]:
                self.check(f'unless score #id_{left} {OBJ} = #id_{right} {OBJ}',key+f'/{left}与{right}实例id不同')
        self.cmd(m,'anim/walk',a);self.cmd(m,'anim/idle',b);self.cmd(m,'anim/walk',c,dim='the_nether')
        self.cmd(m,'anim/walk',d,dim='the_end')
        self.s.step(5)
        for sel,dim,label in instances:
            self.score(sel,sc+'_t',5,key+'/'+label+'每tick只推进一次',dim)
        self.cmd(m,'pause',pos='24.5 80 8.5');self.s.step(3)
        self.score(a,sc+'_t',8,key+'/A不被最近B控制影响')
        self.score(b,sc+'_t',5,key+'/最近B暂停')
        self.score(c,sc+'_t',8,key+'/异维C不被最近B控制影响','the_nether')
        self.score(d,sc+'_t',8,key+'/异维D不被最近B控制影响','the_end')
        self.frame(m,'walk',8,a);self.frame(m,'idle',5,b);self.frame(m,'walk',8,c,'the_nether')
        self.frame(m,'walk',8,d,'the_end')
        self.cmd(m,'clear',a);self.s.step(1)
        self.count(f'@e[type=armor_stand,tag={tag},distance=0..]',1,key+'/clear仅删除A')
        self.count(f'@e[type=item_display,tag={tag}.part,distance=0..]',m['part_count'],key+'/B乘客完整')
        self.s.barrier('kill '+b);self.s.step(2)
        self.count(f'@e[type=item_display,tag={tag}.part,distance=0..]',0,key+'/kill B后无残留')
        self.count(f'@e[type=item_display,tag={tag}.part,distance=0..]',m['part_count'],key+'/C异维乘客未误清','the_nether')
        self.count(f'@e[type=item_display,tag={tag}.part,distance=0..]',m['part_count'],key+'/D异维乘客未误清','the_end')
        self.s.barrier(f'execute in minecraft:the_end run kill {d}');self.s.step(2)
        self.count(f'@e[type=item_display,tag={tag}.part,distance=0..]',0,key+'/End kill D后无残留','the_end')
        self.count(f'@e[type=item_display,tag={tag}.part,distance=0..]',m['part_count'],key+'/End清理不影响Nether C','the_nether')
        self.cmd(m,'clear_all');self.s.step(1)
        for dim in ['overworld','the_nether','the_end']:
            self.count(f'@e[type=armor_stand,tag={tag},distance=0..]',0,key+'/clear_all载体 '+dim,dim)
            self.count(f'@e[type=item_display,tag={tag}.part,distance=0..]',0,key+'/clear_all部件 '+dim,dim)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--datapack',type=Path)
    parser.add_argument('--native-only',action='store_true')
    parser.add_argument('--port',type=int,default=25590)
    parser.add_argument('--eula-source',type=Path,default=Path(r'D:\minecraft\本地部署\eula.txt'))
    args=parser.parse_args()
    if args.native_only:compare_native();return
    if args.datapack is None:parser.error('--datapack is required for the server test')
    source=args.datapack.resolve()
    manifests=[]
    for key in ['heart_of_ender','arch_visage']:
        m=read(source/(key+'_debug_manifest.json'));m['key']=key;manifests.append(m)
    if not(source/'pack.mcmeta').is_file():raise RuntimeError('仅接受完成构建的完整数据包')
    eula=args.eula_source.read_bytes()
    if not re.search(rb'(?m)^\s*eula\s*=\s*true\s*$',eula):raise RuntimeError('未找到可复用的已接受EULA')
    with socket.socket() as sock:sock.bind(('127.0.0.1',args.port))
    OUT.mkdir(exist_ok=True);run=OUT/time.strftime('run_%Y%m%d_%H%M%S');run.mkdir()
    (run/'eula.txt').write_bytes(eula);pack=run/'world/datapacks/tralancer-rpg';pack.parent.mkdir(parents=True)
    shutil.copytree(source,pack)
    hashes={p.relative_to(source).as_posix():sha(p)for p in source.rglob('*')if p.is_file()}
    if hashes!={p.relative_to(pack).as_posix():sha(p)for p in pack.rglob('*')if p.is_file()}:raise RuntimeError('数据包副本不一致')
    write(run/'datapack_hashes.json',hashes)
    (run/'server.properties').write_text('\n'.join([
        'server-ip=127.0.0.1',f'server-port={args.port}','online-mode=false','enforce-secure-profile=false',
        'enable-rcon=false','enable-query=false','enable-status=false','enable-jmx-monitoring=false',
        'max-players=1','view-distance=2','simulation-distance=2','spawn-protection=0',
        'pause-when-empty-seconds=0','level-name=world','level-type=minecraft:flat','generate-structures=false',
        'difficulty=peaceful','gamemode=creative','max-tick-time=120000',
        'generator-settings={"layers":[{"block":"minecraft:bedrock","height":1},{"block":"minecraft:stone","height":2}],"biome":"minecraft:plains"}','']),encoding='utf8')
    argv=sys.argv[:]
    try:
        sys.argv=['server_test.py',str(run)];spec=importlib.util.spec_from_file_location('he_final_classpath',HERE/'server_test.py')
        helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
    finally:sys.argv=argv
    command=[JAVA,'-Xmx2G','-Dfile.encoding=UTF-8','-Djava.awt.headless=true','-cp',os.pathsep.join(helper.classpath(read(VJSON))),
        'net.minecraft.server.Main','--nogui','--universe',str(run),'--world','world']
    with zipfile.ZipFile(JAR)as z:version=json.loads(z.read('version.json'))
    report={'scope':'M5 full built pack, real dedicated server; no client or player world',
        'datapack_source':str(source),'run_directory':str(run),'bind':'127.0.0.1','port':args.port,
        'manifest_sha256':{m['key']:sha(source/(m['key']+'_debug_manifest.json'))for m in manifests},
        'manifests':manifests,'datapack_files':len(hashes),'datapack_copy_exact':True,
        'eula_source':str(args.eula_source),'eula_source_sha256':sha(args.eula_source),
        'java':JAVA,'jar':JAR,'jar_sha256':sha(JAR),'minecraft_version':version,'checks':[]}
    write(run/'launch.json',{'command':command,'evidence':report});srv=None
    try:
        print('启动隔离完整包服务端: '+str(run),flush=True)
        srv=Server(command,run);srv.wait('Done (',timeout=240);report['startup_done']=True
        srv.barrier('tick freeze','tick rate 100',f'scoreboard objectives add {OBJ} dummy','datapack list enabled')
        test=Tests(srv,pack,report)
        for dim in ['overworld','the_nether','the_end']:
            srv.barrier(f'execute in minecraft:{dim} run forceload add 0 0 31 15')
        srv.step(20)
        for dim in ['overworld','the_nether','the_end']:
            for attempt in range(20):
                start=len(srv.lines);token=f'HE_FINAL_LOADED_{dim}_{attempt}'
                srv.send(f'execute in minecraft:{dim} if loaded 8 80 8 run say {token}')
                try:srv.wait(token,start,.4);break
                except TimeoutError:srv.step(10)
            test.check('if loaded 8 80 8','测试区块已加载 '+dim,dim)
        for m in manifests:test.rig(m)
        he,av=manifests
        h=test.spawn(he,'he_final_HE');v=test.spawn(av,'he_final_AV','24.5 80 8.5')
        srv.step(3);test.cmd(he,'clear_all');srv.step(2)
        test.count(f'@e[type=item_display,tag={av["part_tag"]},distance=0..]',av['part_count'],'HE clear_all不误清AV')
        test.count(f'@e[type=armor_stand,tag={av["carrier_tag"]},distance=0..]',1,'HE clear_all不误清AV载体')
        test.cmd(av,'clear_all');srv.step(2)
        for m in manifests:
            test.count(f'@e[type=item_display,tag={m["part_tag"]},distance=0..]',0,m['key']+'最终零残留')
        report['tests_complete']=True
    except Exception as exc:
        report['failure']={'type':type(exc).__name__,'message':str(exc),'traceback':traceback.format_exc()}
        print('测试中断: '+str(exc),flush=True)
    finally:
        if srv:
            report['server_exit_code']=srv.stop();report['server_process_exited']=srv.proc.poll()is not None
            pattern=re.compile(r'Failed to load function|Failed to parse|Couldn.t load tag|Unknown function|Unknown or incomplete command|Whilst parsing|Parsing error|Exception executing command')
            report['function_or_command_errors']=[s for s in srv.lines if pattern.search(s)]
        report['eula_source_unchanged']=sha(args.eula_source)==report['eula_source_sha256']
        report['passed']=sum(c['passed']for c in report['checks']);report['failed']=[c for c in report['checks']if not c['passed']]
        report['success']=not report.get('failure')and not report['failed']and not report.get('function_or_command_errors')and report.get('server_exit_code')==0
        report['limits']=['没有启动客户端；不验证透明排序、视觉还原或实际听感','变换为实体保存的目标NBT；四元数正规化后比较，非客户端插值图','clear_all仅测试已加载实体，未声称卸载区块的实例也被清除']
        write(run/'report.json',report);write(OUT/'server_report.json',report)
        print(json.dumps({k:report.get(k)for k in ['success','passed','failed','failure','function_or_command_errors','server_exit_code']},ensure_ascii=False),flush=True)
    if not report['success']:raise SystemExit(1)

if __name__=='__main__':main()
