"""Private offline server with local file inbox; never touches a user world."""
from pathlib import Path
import argparse, json, os, shutil, socket, subprocess, sys, threading, time

ROOT=Path(__file__).resolve().parent
SERVER=ROOT/'server'
INBOX=SERVER/'commands'
DP=Path(r'D:\agent\dungeons_extract\phase2_b\build_workspace\rpg')

def prepare():
    SERVER.mkdir(exist_ok=True)
    INBOX.mkdir(exist_ok=True)
    target=SERVER/'packtest'/'datapacks'/'rpg'
    if not target.exists():
        shutil.copytree(DP,target)
    with socket.socket() as sock:
        sock.bind(('127.0.0.1',0))
        port=sock.getsockname()[1]
    (SERVER/'eula.txt').write_text('eula=true\n',encoding='utf-8')
    props={'server-ip':'127.0.0.1','server-port':port,'online-mode':'false',
           'enforce-secure-profile':'false','spawn-protection':0,'max-players':2,
           'level-name':'packtest','level-type':'minecraft:flat','gamemode':'creative',
           'difficulty':'normal','view-distance':6,'simulation-distance':4,
           'max-tick-time':-1,'enable-rcon':'false','enable-query':'false',
           'motd':'Isolated Lucifer Phase 2 Validation'}
    (SERVER/'server.properties').write_text('\n'.join(str(k)+'='+str(v) for k,v in props.items())+'\n',encoding='utf-8')
    client=json.loads((ROOT/'launch_manifest.json').read_text(encoding='utf-8'))
    (SERVER/'ops.json').write_text(json.dumps([{'uuid':client['offline_uuid'],'name':client['username'],'level':4,'bypassesPlayerLimit':False}]),encoding='utf-8')
    cmd=[client['java'],'-Xms512M','-Xmx2G','-Dfile.encoding=UTF-8','-cp',
         os.pathsep.join(client['libraries']+[client['jar']]),'net.minecraft.server.Main',
         '--nogui','--universe',str(SERVER),'--world','packtest']
    (SERVER/'launch.json').write_text(json.dumps({'command':cmd,'port':port},indent=2),encoding='utf-8')
    return port

def worker():
    config=json.loads((SERVER/'launch.json').read_text(encoding='utf-8'))
    proc=subprocess.Popen(config['command'],cwd=SERVER,stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',bufsize=1,
                          creationflags=subprocess.CREATE_NO_WINDOW)
    status={'java_pid':proc.pid,'runner_pid':os.getpid(),'port':config['port'],'ready':False}
    status_path=SERVER/'status.json'
    status_path.write_text(json.dumps(status),encoding='utf-8')
    log=open(SERVER/'console.log','a',encoding='utf-8',buffering=1)
    def pump():
        for line in proc.stdout:
            log.write(line)
            if 'Done (' in line:
                status['ready']=True
                status_path.write_text(json.dumps(status),encoding='utf-8')
    threading.Thread(target=pump,daemon=True).start()
    while proc.poll() is None:
        for path in sorted(INBOX.glob('*.json')):
            commands=json.loads(path.read_text(encoding='utf-8'))
            for cmd in commands:
                log.write('>>> '+cmd+'\n')
                proc.stdin.write(cmd+'\n')
                proc.stdin.flush()
                time.sleep(.1)
            path.rename(path.with_suffix('.sent'))
        time.sleep(.1)
    status['exit_code']=proc.returncode
    status_path.write_text(json.dumps(status),encoding='utf-8')
    time.sleep(.3)
    log.close()

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('action',choices=['start','worker','send','status'])
    ap.add_argument('--file')
    ap.add_argument('commands',nargs='*')
    args=ap.parse_args()
    if args.action=='worker':
        worker()
    elif args.action=='start':
        assert not (SERVER/'status.json').exists(), 'Server already initialized; inspect status instead of restarting blindly.'
        port=prepare()
        proc=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'worker'],cwd=ROOT,
                              stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,
                              creationflags=subprocess.CREATE_NO_WINDOW|subprocess.CREATE_NEW_PROCESS_GROUP)
        print(json.dumps({'runner_pid':proc.pid,'port':port}))
    elif args.action=='send':
        commands=args.commands
        if args.file:
            commands += [x.strip() for x in Path(args.file).read_text(encoding='utf-8').splitlines() if x.strip() and not x.startswith('#')]
        assert commands
        p=INBOX/(str(time.time_ns())+'.tmp')
        p.write_text(json.dumps(commands),encoding='utf-8')
        p.rename(p.with_suffix('.json'))
        print('queued',len(commands))
    else:
        print((SERVER/'status.json').read_text(encoding='utf-8'))
