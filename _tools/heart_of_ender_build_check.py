"""Run the unmodified project build entrypoints in a task-owned file snapshot.

The real entrypoints rebuild whole rpg/resourcepack trees. This avoids deleting
or replacing files being authored by other sessions in the original workspace.
No built tree is automatically copied back or synchronized to Minecraft.
"""
from __future__ import annotations
import argparse, hashlib, json, os, shutil, subprocess, sys, time
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'_tools/heart_of_ender_ref/build_validation'
WORK=Path(r'D:\agent\codex\TRA\work')
BASH=Path(r'C:\Program Files\Git\bin\bash.exe')

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n','utf8')
def safe_snapshot(path):
    path=path.resolve();base=WORK.resolve()
    if path.parent!=base or not path.name.startswith('ender_final_build_') or ROOT==path or ROOT in path.parents:
        raise ValueError('Not a dedicated build workspace: '+str(path))
    for name in ('rpg','resourcepack'):
        target=(path/name).resolve()
        if path not in target.parents or target.is_symlink():raise ValueError('Unsafe rebuild target')
    return path

def prepare():
    if not (ROOT/'_tools/arch_visage_ref/config.json').is_file():raise ValueError('Arch-Visage not ready')
    stamp=str(time.time_ns())
    dest=safe_snapshot(WORK/('ender_final_build_'+stamp))
    dest.mkdir(parents=True,exist_ok=False)
    for item in ROOT.iterdir():
        if item.is_file() and item.suffix.lower()!='.zip':shutil.copy2(item,dest/item.name)
    for name in ('_orig','_orig_rp','resourcepack','rpg','docs','_art_audit','_art_crops'):
        if (ROOT/name).is_dir():shutil.copytree(ROOT/name,dest/name)
    def ignore(directory,names):
        skipped={'__pycache__','.pytest_cache'}
        if Path(directory).resolve()==(ROOT/'_tools').resolve():
            skipped|={'heart_of_ender_ref','arch_visage_ref'}
        return [n for n in names if n in skipped]
    shutil.copytree(ROOT/'_tools',dest/'_tools',ignore=ignore)
    # Both final model files embed their atlas; copy their exact build inputs.
    he=dest/'_tools/heart_of_ender_ref';he.mkdir()
    shutil.copy2(ROOT/'_tools/heart_of_ender_ref/heart_of_ender.bbmodel',he/'heart_of_ender.bbmodel')
    shutil.copytree(ROOT/'_tools/heart_of_ender_ref/sounds',he/'sounds')
    (he/'m2_geometry').mkdir()
    shutil.copy2(ROOT/'_tools/heart_of_ender_ref/m2_geometry/geometry_spec.json',he/'m2_geometry/geometry_spec.json')
    av=dest/'_tools/arch_visage_ref';av.mkdir()
    for name in ('arch_visage.bbmodel','config.json'):
        shutil.copy2(ROOT/'_tools/arch_visage_ref'/name,av/name)
    if (ROOT/'_tools/arch_visage_ref/sounds').is_dir():
        shutil.copytree(ROOT/'_tools/arch_visage_ref/sounds',av/'sounds')
    inventory={}
    for prefix in ('_tools','_orig','_orig_rp'):
        for path in (dest/prefix).rglob('*'):
            if path.is_file():inventory[path.relative_to(dest).as_posix()]=sha(path)
    record={'snapshot':str(dest),'source_root':str(ROOT),'build_inputs':inventory,
            'purpose':'isolated original build.sh and rp_build.sh; no source/output sync back',
            'excluded':'HE/AV research images and temporary servers; exact bbmodels/config/sounds retained'}
    write(OUT/'snapshot.json',record)
    print('Prepared '+str(dest),flush=True)
    return dest

def run(snapshot):
    snapshot=safe_snapshot(snapshot)
    if not BASH.is_file():raise FileNotFoundError(BASH)
    marker=json.loads((OUT/'snapshot.json').read_text('utf8'))
    if snapshot!=Path(marker['snapshot']).resolve():raise ValueError('Unknown snapshot')
    # Recheck all potentially destructive destinations immediately before entrypoints.
    for name in ('rpg','resourcepack'):
        target=(snapshot/name).resolve()
        assert snapshot in target.parents and target!=ROOT/name
    env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
    env['PATH']=str(Path(sys.executable).parent)+os.pathsep+env.get('PATH','')
    results=[]
    commands=[('rp_build',[str(BASH),'_tools/rp_build.sh']),
              ('build',[str(BASH),'_tools/build.sh']),
              ('rp_validate',[sys.executable,'-X','utf8','_tools/rp_validate.py','resourcepack'])]
    for label,command in commands:
        log=OUT/(label+'.log');start=time.time()
        print('Starting '+label+' in isolated snapshot',flush=True)
        with log.open('w',encoding='utf8',newline='\n') as stream:
            proc=subprocess.run(command,cwd=snapshot,env=env,stdout=stream,stderr=subprocess.STDOUT,
                                creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0),timeout=900)
        entry={'name':label,'command':command,'cwd':str(snapshot),'exit_code':proc.returncode,
               'seconds':round(time.time()-start,2),'log':str(log),'log_sha256':sha(log)}
        results.append(entry);write(OUT/'build_results.json',{'snapshot':str(snapshot),'steps':results,'all_passed':all(x['exit_code']==0 for x in results) and len(results)==3})
        print(json.dumps(entry,ensure_ascii=False),flush=True)
        if proc.returncode:
            print('\n'.join(log.read_text('utf8').splitlines()[-25:]),flush=True)
            raise SystemExit(proc.returncode)
    print('All original build/validate entrypoints passed',flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--run',action='store_true');ap.add_argument('--existing',action='store_true')
    args=ap.parse_args()
    snapshot=Path(json.loads((OUT/'snapshot.json').read_text('utf8'))['snapshot']) if args.existing else prepare()
    if args.run:run(snapshot)
