"""Run the original server_test.py against the complete isolated final build.

Uses a fresh private test world and an already accepted local EULA file. Does
not open or modify the player's world. Console complaints are checked explicitly
because the original script does not use its exit code to report parse errors.
"""
from __future__ import annotations
import argparse,hashlib,json,os,re,shutil,subprocess,sys,time
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'_tools/heart_of_ender_ref/build_validation'
WORK=Path(r'D:\agent\codex\TRA\work')
EULA=Path(r'D:\minecraft\本地部署\eula.txt')

def classify(record, output):
    # The original tool's generic WARN matcher includes the four standard
    # localhost offline-mode notices. Preserve every notice and exempt only
    # these exact messages, never a broad ERROR/WARN substring.
    expected={
        '**** SERVER IS RUNNING IN OFFLINE/INSECURE MODE!',
        'The server will make no attempt to authenticate usernames. Beware.',
        'While this makes the game possible to play without internet access, it also opens up the ability for hackers to connect with any username they choose.',
        'To change this, set "online-mode" to "true" in the server.properties file.'}
    block=output.split('--- server complaints (',1)[-1].split('--- full console ---',1)[0]
    lines=[line.strip() for line in block.splitlines() if re.match(r'\s*\[\d\d:\d\d:\d\d\]',line)]
    known=[line for line in lines if re.sub(r'^.*?/WARN\]:\s*','',line) in expected]
    unexpected=[line for line in lines if line not in known]
    record['known_environment_warnings']=known
    record['unexpected_complaints']=unexpected
    record['datapack_enabled']='[file/tralancer-rpg (world)]' in output
    record['success']=(record['exit_code']==0 and record['reached_done']
        and record['datapack_enabled'] and record['complaints'] is not None
        and len(lines)==record['complaints'] and not unexpected)
    return record

def finish(record,output):
    record=classify(record,output)
    (OUT/'server_test_result.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n','utf8')
    print(json.dumps(record,ensure_ascii=False),flush=True)
    if not record['success']:
        print('\n'.join(output.splitlines()[:100]))
        raise SystemExit('Original full-pack server_test.py did not pass')

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--review-existing',action='store_true',help='Reclassify the preserved console without rerunning the server')
    args=ap.parse_args()
    if args.review_existing:
        record=json.loads((OUT/'server_test_result.json').read_text('utf8'))
        raw=Path(record['log']).read_bytes()
        if hashlib.sha256(raw).hexdigest()!=record['log_sha256']:
            raise ValueError('Preserved log bytes changed')
        finish(record,raw.decode('utf8'))
        return
    source=Path(json.loads((OUT/'snapshot.json').read_text('utf8'))['snapshot'])
    build=json.loads((OUT/'build_results.json').read_text('utf8'))
    if not build['all_passed'] or build['snapshot']!=str(source):
        raise ValueError('Complete isolated build has not passed')
    eula=EULA.read_bytes()
    if not re.search(rb'(?im)^\s*eula\s*=\s*true\s*$',eula):
        raise ValueError('Existing EULA is not accepted; refusing to change it')
    run=WORK/('ender_final_server_'+str(time.time_ns()))
    if run.resolve().parent!=WORK.resolve() or run.exists():
        raise ValueError('Test world must be a fresh dedicated directory')
    run.mkdir(parents=True)
    (run/'eula.txt').write_bytes(eula)
    (run/'server.properties').write_text('\n'.join([
        'server-ip=127.0.0.1','server-port=25591','online-mode=false',
        'enable-rcon=false','enable-query=false','enforce-secure-profile=false',
        'pause-when-empty-seconds=0','max-tick-time=120000','view-distance=2',
        'simulation-distance=2','spawn-protection=0','level-type=minecraft:flat',
        'generator-settings={"layers":[{"block":"minecraft:bedrock","height":1},{"block":"minecraft:stone","height":2}],"biome":"minecraft:plains"}',
        'generate-structures=false','motd=HE AV isolated complete pack validation','']), 'utf8')
    destination=run/'packtest/datapacks/tralancer-rpg'
    shutil.copytree(source/'rpg',destination)
    log=OUT/'server_test.log'
    command=[sys.executable,'-X','utf8',str(source/'_tools/server_test.py'),str(run),'240']
    env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
    env.pop('MC_PROBE_FILE',None)
    start=time.time()
    with log.open('w',encoding='utf8',newline='\n') as stream:
        proc=subprocess.run(command,cwd=source,env=env,stdout=stream,stderr=subprocess.STDOUT,
                            timeout=540,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    output=log.read_text('utf8')
    complaints=re.search(r'--- server complaints \((\d+)\) ---',output)
    record={'command':command,'snapshot':str(source),'run_directory':str(run),
            'exit_code':proc.returncode,'seconds':round(time.time()-start,2),
            'reached_done':"server reached 'Done': True" in output,
            'complaints':int(complaints.group(1)) if complaints else None,
            'eula_source':str(EULA),'eula_sha256':hashlib.sha256(eula).hexdigest(),
            'log':str(log),'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest(),
            'server_test_script_unchanged':(source/'_tools/server_test.py').read_bytes()==(ROOT/'_tools/server_test.py').read_bytes(),
            'visual_validation':False}
    finish(record,output)

if __name__=='__main__':main()
