"""独立1.21.11 headless探针测试；不触碰玩家世界或公共server_test.py。"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import shutil
import socket
import subprocess
import sys
import threading
import time
import traceback
import zipfile

from heart_of_ender_blockbench import REF
from mc_env import JAVA, JAR, VJSON

OUT=REF/'m3_material_v3/motion_probe_test'
PACK=REF/'m3_material_v3/motion_probe'
C_ALL='@e[type=minecraft:armor_stand,tag=he_material_probe.carrier,distance=0..]'
C='@e[type=minecraft:armor_stand,tag=he_material_probe.carrier,distance=0..,limit=1]'
D='@e[type=minecraft:item_display,tag=he_material_probe.part,distance=0..]'
OBJ='he_test'

def read(p):return json.loads(p.read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

class Server:
    def __init__(self,command,run):
        self.lines=[];self.cv=threading.Condition();self.seq=0
        self.log=(run/'console.log').open('w',encoding='utf8',buffering=1)
        self.proc=subprocess.Popen(command,cwd=run,stdin=subprocess.PIPE,stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,text=True,encoding='utf8',errors='replace',bufsize=1,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
        def pump():
            for line in self.proc.stdout:
                with self.cv:
                    self.lines.append(line.rstrip());self.log.write(line);self.cv.notify_all()
        self.reader=threading.Thread(target=pump,daemon=True);self.reader.start()

    def send(self,*commands):
        for c in commands:
            self.log.write('>>> '+c+'\n');self.proc.stdin.write(c+'\n')
        self.proc.stdin.flush()

    def wait(self,needle,start=0,timeout=60):
        end=time.monotonic()+timeout
        with self.cv:
            while time.monotonic()<end:
                found=next((x for x in self.lines[start:] if needle in x),None)
                if found:return found
                if self.proc.poll() is not None:raise RuntimeError('服务端提前退出: '+str(self.proc.returncode))
                self.cv.wait(min(.25,max(0,end-time.monotonic())))
        raise TimeoutError('等待服务端输出超时: '+needle)

    def barrier(self,*commands):
        self.seq+=1;token=f'HE_TEST_BARRIER_{self.seq:04d}'
        start=len(self.lines);self.send(*commands,'say '+token);self.wait(token,start,20)

    def step(self,n):
        self.barrier(f'execute store result score #before {OBJ} run time query gametime',
            f'scoreboard players operation #target {OBJ} = #before {OBJ}',
            f'scoreboard players add #target {OBJ} {n}',f'tick step {n}')
        self.seq+=1;token=f'HE_TEST_STEP_{self.seq:04d}';start=len(self.lines)
        end=time.monotonic()+max(20,n/10)
        while time.monotonic()<end:
            self.send(f'execute store result score #now {OBJ} run time query gametime',
                f'execute if score #now {OBJ} >= #target {OBJ} run say {token}')
            try:self.wait(token,start,.4);return
            except TimeoutError:pass
        raise TimeoutError(f'无法推进{n}个服务器刻')

    def stop(self):
        if self.proc.poll() is None:
            try:self.send('stop');self.proc.wait(timeout=45)
            except (OSError,subprocess.TimeoutExpired):
                self.proc.kill();self.proc.wait(timeout=10)
        self.reader.join(5);self.log.close()
        return self.proc.returncode

def main():
    global C,C_ALL
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--smoke',action='store_true')
    parser.add_argument('--port',type=int,default=25589)
    parser.add_argument('--eula-source',type=Path,default=Path(r'D:\minecraft\本地部署\eula.txt'))
    args=parser.parse_args()
    accepted=args.eula_source.read_bytes()
    if not re.search(rb'(?m)^\s*eula\s*=\s*true\s*$',accepted):
        raise RuntimeError('没有可复用的已接受EULA；不会自动新接受条款')
    with socket.socket() as sock:sock.bind(('127.0.0.1',args.port))
    manifest=read(PACK/'motion_probe_manifest.json')
    carrier_type=manifest['carrier']['type']
    C_ALL=f'@e[type={carrier_type},tag=he_material_probe.carrier,distance=0..]'
    C=f'@e[type={carrier_type},tag=he_material_probe.carrier,distance=0..,limit=1]'
    OUT.mkdir(exist_ok=True)
    run=OUT/(time.strftime('run_%Y%m%d_%H%M%S')+('_smoke' if args.smoke else '_full'))
    run.mkdir();(run/'eula.txt').write_bytes(accepted)
    world=run/'world';target=world/'datapacks/he_material_probe'
    target.parent.mkdir(parents=True);shutil.copytree(PACK/'datapack',target)
    copied={p.relative_to(target).as_posix():sha(p) for p in target.rglob('*') if p.is_file()}
    source={p.relative_to(PACK/'datapack').as_posix():sha(p) for p in (PACK/'datapack').rglob('*') if p.is_file()}
    if copied!=source:raise RuntimeError('隔离数据包副本与生成目录不一致')
    (run/'server.properties').write_text('\n'.join([
        'server-ip=127.0.0.1',f'server-port={args.port}','online-mode=false','enforce-secure-profile=false',
        'enable-rcon=false','enable-query=false','enable-status=false','enable-jmx-monitoring=false',
        'max-players=1','view-distance=2','simulation-distance=2','spawn-protection=0',
        'pause-when-empty-seconds=0','level-name=world','level-type=minecraft:flat','generate-structures=false',
        'difficulty=peaceful','gamemode=creative','sync-chunk-writes=false','max-tick-time=120000',
        'generator-settings={"layers":[{"block":"minecraft:bedrock","height":1},{"block":"minecraft:stone","height":2}],"biome":"minecraft:plains"}',
        'motd=Local isolated Heart of Ender test','']) ,encoding='utf8')
    # Import the existing classpath helper without invoking its RPG-specific probes.
    saved=sys.argv[:]
    try:
        sys.argv=['server_test.py',str(run)]
        spec=importlib.util.spec_from_file_location('he_server_test_helpers',Path(__file__).with_name('server_test.py'))
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    finally:sys.argv=saved
    cp=module.classpath(read(Path(VJSON)))
    command=[JAVA,'-Xmx2G','-Dfile.encoding=UTF-8','-Djava.awt.headless=true','-cp',os.pathsep.join(cp),
             'net.minecraft.server.Main','--nogui','--universe',str(run),'--world','world']
    with zipfile.ZipFile(JAR) as z:version=json.loads(z.read('version.json'))
    report={'scope':'M3 isolated real 1.21.11 dedicated-server test; no main RPG pack, no client visual claim',
        'mode':'smoke' if args.smoke else 'full','run_directory':str(run),'bind':'127.0.0.1','port':args.port,
        'model_sha256':manifest['model_sha256'],'probe_manifest_sha256':sha(PACK/'motion_probe_manifest.json'),
        'java':JAVA,'jar':JAR,'jar_sha256':sha(Path(JAR)),'minecraft_version':version,
        'eula':{'source':str(args.eula_source),'source_sha256':hashlib.sha256(accepted).hexdigest(),
                'copied_sha256':sha(run/'eula.txt'),'action':'reused existing accepted bytes; no new agreement submitted'},
        'datapack_files':len(copied),'datapack_copy_exact':True,'checks':[],'visual_client_test':False}
    (run/'launch.json').write_text(json.dumps({'command':command,'evidence':report},ensure_ascii=False,indent=2),encoding='utf8')
    srv=None
    def check(condition,label):
        srv.seq+=1;token=f'HE_TEST_ASSERT_{srv.seq:04d}';start=len(srv.lines)
        # Missing entity selectors abort both `if score` and `unless score`;
        # use an explicit default-failure sentinel instead of waiting forever.
        srv.send(f'scoreboard players set #assert {OBJ} 0',
            f'execute {condition} run scoreboard players set #assert {OBJ} 1',
            f'execute if score #assert {OBJ} matches 1 run say {token}_PASS',
            f'execute if score #assert {OBJ} matches 0 run say {token}_FAIL')
        line=srv.wait(token,start,20);ok=token+'_PASS' in line
        report['checks'].append({'name':label,'passed':ok,'condition':condition,'console':line})
        if not ok:print('FAIL '+label,flush=True)
        return ok
    def score(holder,obj,value,label):return check(f'if score {holder} {obj} matches {value}',label)
    def counts(ncarrier,nparts,label):
        srv.barrier(f'scoreboard players set #carriers {OBJ} 0',f'scoreboard players set #parts {OBJ} 0',
            f'execute as {C_ALL} run scoreboard players add #carriers {OBJ} 1',
            f'execute as {D} run scoreboard players add #parts {OBJ} 1')
        score('#carriers',OBJ,ncarrier,label+' carrier数量');score('#parts',OBJ,nparts,label+' display数量')
    def play(clip):srv.barrier(f'execute in minecraft:overworld positioned 8 80 8 run function he_material_probe:play/{clip}')
    def transform(snbt):
        result={}
        for key in ['translation','left_rotation','scale','right_rotation']:
            match=re.search(r'\b'+key+r':\s*\[([^\]]+)\]',snbt)
            if not match:raise ValueError('缺少transform字段 '+key)
            result[key]=[float(x.strip().rstrip('fFdD')) for x in match.group(1).split(',')]
        return result
    def frame(clip,tick):
        # dm.bake omits unchanged parts; replay targets through this frame.
        expected={}
        for n in range(tick+1):
            source=PACK/f'datapack/data/he_material_probe/function/anim/{clip}/f{n}.mcfunction'
            for line in source.read_text(encoding='utf8').splitlines():
                part=re.search(r'tag=he_material_probe\.p\.([a-z_]+)',line)
                if part and 'transformation:'in line:
                    expected[part.group(1)]=transform(line.split('transformation:',1)[1])
        if set(expected)!=set(manifest['parts']):raise ValueError('累计帧未覆盖21部件')
        start=len(srv.lines)
        srv.barrier(*[f'data get entity @e[type=minecraft:item_display,tag=he_material_probe.p.{part},distance=0..,limit=1] transformation' for part in expected])
        outputs=[line for line in srv.lines[start:] if 'has the following entity data:'in line]
        if len(outputs)!=21:raise ValueError('无法读取21部件实际transform: '+str(len(outputs)))
        samples=[]
        for (part,target),line in zip(expected.items(),outputs):
            actual=transform(line);errors={}
            for key,wanted in target.items():
                # Minecraft normalizes rotations on load; compare that result,
                # not the unnormalized decimal SNBT source or list order tests.
                if key.endswith('rotation'):
                    length=math.sqrt(sum(x*x for x in wanted));wanted=[x/length for x in wanted]
                    errors[key]=min(max(abs(a-b) for a,b in zip(actual[key],wanted)),
                        max(abs(a+b) for a,b in zip(actual[key],wanted)))
                else:errors[key]=max(abs(a-b) for a,b in zip(actual[key],wanted))
            samples.append({'part':part,'target':target,'actual':actual,'errors':errors})
        maximum=max(x for item in samples for x in item['errors'].values())
        ok=maximum<=1e-6
        report['checks'].append({'name':f'{clip} f{tick}: 实际21部件transform数值匹配累计烘焙目标',
            'passed':ok,'maximum_error':maximum,'tolerance':1e-6,
            'comparison':'quaternion normalized, q and -q equivalent; other fields direct',
            'samples':samples})
        if not ok:print(f'FAIL {clip} f{tick} transform误差 {maximum}',flush=True)
    try:
        print('开始隔离1.21.11服务端: '+str(run),flush=True)
        srv=Server(command,run);srv.wait('Done (',timeout=240)
        report['startup_done']=True
        print('服务端已加载，开始最小召唤/推进/清理检查',flush=True)
        srv.barrier('tick freeze','tick rate 100',f'scoreboard objectives add {OBJ} dummy',
                    'execute in minecraft:overworld run forceload add 0 0 15 15','datapack list enabled')
        srv.step(5)
        for attempt in range(20):
            token=f'HE_TEST_CHUNK_READY_{attempt}';start=len(srv.lines)
            srv.send('execute if loaded 8 80 8 run say '+token)
            try:srv.wait(token,start,.3);break
            except TimeoutError:srv.step(10)
        check('if loaded 8 80 8','测试坐标区块已加载')
        srv.barrier('forceload query 8 8')
        play('idle');counts(1,21,'idle召唤')
        srv.barrier('data get entity '+C, f'execute as {D} run data get entity @s Pos',
                    'scoreboard players get #generation he_probe_id',f'scoreboard players get {C} he_probe_id')
        score(C,'he_probe_clip',0,'idle片段编号');score(C,'he_probe_t',0,'idle初始帧');score(C,'he_probe_run',1,'idle播放状态')
        srv.step(5);score(C,'he_probe_t',5,'idle实际推进5tick')
        srv.barrier('data get entity '+C, f'execute as {D} run data get entity @s Pos',
                    f'scoreboard players set #passengers {OBJ} 0',
                    f'execute store result score #passengers {OBJ} run data get entity {C} Passengers')
        score('#passengers',OBJ,21,'载体NBT实际有21乘客')
        for axis in range(3):
            srv.barrier(f'execute as {C} store result score @s {OBJ} run data get entity @s Pos[{axis}] 1000000',
                f'execute as {D} store result score @s {OBJ} run data get entity @s Pos[{axis}] 1000000',
                f'scoreboard players set #bad {OBJ} 0',
                f'execute as {D} unless score @s {OBJ} = {C} {OBJ} run scoreboard players add #bad {OBJ} 1')
            score('#bad',OBJ,0,f'全部21乘客Pos[{axis}]与载体相同，精度1e-6')
        srv.barrier('function he_material_probe:clear');counts(0,0,'clear后')
        play('idle');srv.step(2);srv.barrier('kill '+C);srv.step(2);counts(0,0,'直接kill载体后2tick')
        report['smoke_complete']=True
        if not args.smoke:
            if any(not item['passed'] for item in report['checks']):
                raise RuntimeError('最小测试失败，不继续完整动作检查')
            print('最小检查通过；开始7段动作、循环/单次及控制测试',flush=True)
            for clip,info in manifest['clips'].items():
                play(clip);counts(1,21,clip+'重建唯一模型')
                score(C,'he_probe_clip',info['clip_id'],clip+' clip编号')
                score(C,'he_probe_t',0,clip+' 初始帧')
                score(C,'he_probe_run',1,clip+' 开始播放')
                frame(clip,0)
                srv.step(5);score(C,'he_probe_t',5,clip+' 推进5tick');frame(clip,5)
                srv.step(info['duration_ticks']-5)
                if info['loop']:
                    score(C,'he_probe_t',0,clip+' 整周期回到0帧')
                    score(C,'he_probe_run',1,clip+' 循环继续运行');frame(clip,0)
                    srv.step(3);score(C,'he_probe_t',3,clip+' 第二周期推进');frame(clip,3)
                else:
                    final=info['duration_ticks']
                    score(C,'he_probe_t',final,clip+' 到达末帧')
                    score(C,'he_probe_run',2,clip+' 单次结束状态');frame(clip,final)
                    srv.step(7);score(C,'he_probe_t',final,clip+' 结束后末帧保持')
                    srv.barrier('function he_material_probe:resume');srv.step(2)
                    score(C,'he_probe_run',2,clip+' 完成后resume不误重启')
                    score(C,'he_probe_t',final,clip+' 完成后resume仍保留末帧')
                print('已检查 '+clip,flush=True)
            for clip in ['walk','mortar']:
                play(clip);srv.step(13)
                srv.barrier('function he_material_probe:pause')
                score(C,'he_probe_run',0,clip+' pause状态')
                srv.step(17);score(C,'he_probe_t',13,clip+' pause期间帧不前进');frame(clip,13)
                srv.barrier('function he_material_probe:resume');srv.step(7)
                score(C,'he_probe_run',1,clip+' resume状态')
                score(C,'he_probe_t',20,clip+' resume从暂停帧继续');frame(clip,20)
                srv.barrier('function he_material_probe:stop');srv.step(9)
                score(C,'he_probe_clip',0,clip+' stop回idle')
                score(C,'he_probe_t',0,clip+' stop保持第0帧')
                score(C,'he_probe_run',0,clip+' stop为静态状态');frame('idle',0)
            for entry in ['spawn_idle','spawn_cross','spawn_mortar']:
                srv.barrier(f'execute positioned 8 80 8 run function he_material_probe:{entry}')
                counts(1,21,entry+'静态入口')
                score(C,'he_probe_run',0,entry+'不自动播放')
                srv.barrier(f'scoreboard players operation #saved_t {OBJ} = {C} he_probe_t')
                srv.step(5)
                check(f'if score {C} he_probe_t = #saved_t {OBJ}',entry+'静态帧保持')
            play('idle')
            srv.barrier('scoreboard players add #generation he_probe_id 1');srv.step(1)
            counts(0,0,'旧generation载体下一tick退休')
            play('cross_beam');srv.step(3)
            srv.barrier('function he_material_probe:clear');counts(0,0,'全量结束clear')
            play('walk');srv.step(3);srv.barrier('kill '+C);srv.step(2)
            counts(0,0,'全量结束直接kill载体后零残留')
            report['full_complete']=True
    except Exception as exc:
        report['failure']={'type':type(exc).__name__,'message':str(exc),'traceback':traceback.format_exc()}
        print('测试中断: '+str(exc),flush=True)
    finally:
        if srv:
            report['server_exit_code']=srv.stop()
            report['server_process_exited']=srv.proc.poll() is not None
            report['console_lines']=len(srv.lines)
            pattern=re.compile(r'Failed to load function|Failed to parse|Couldn.t load tag|Unknown function|Unknown or incomplete command|Whilst parsing|Parsing error|Exception executing command')
            report['function_or_command_errors']=[s for s in srv.lines if pattern.search(s)]
        report['eula_source_unchanged']=sha(args.eula_source)==report['eula']['source_sha256']
        report['passed']=sum(c['passed']for c in report['checks'])
        report['failed']=[c for c in report['checks']if not c['passed']]
        report['success']=not report.get('failure') and not report['failed'] and not report.get('function_or_command_errors') and report.get('server_exit_code')==0
        report['limits']=['真实专用服务端已执行命令；未运行游戏客户端，不证明视觉/半透明排序/音效听感',
            'transform检查比较实体保存的目标NBT，不是客户端插值后的渲染图',
            'generation检查直接使代号过期，未声称实测卸载区块再加载',
            '只加载独立he_material_probe数据包；未构建、同步或测试主RPG包']
        text=json.dumps(report,ensure_ascii=False,indent=2)+'\n'
        (run/'report.json').write_text(text,encoding='utf8')
        (OUT/('smoke_report.json'if args.smoke else'report.json')).write_text(text,encoding='utf8')
        print(json.dumps({k:report.get(k)for k in ['success','passed','failed','failure','server_exit_code','function_or_command_errors']},ensure_ascii=False),flush=True)
    if not report['success']:raise SystemExit(1)

if __name__=='__main__':main()
