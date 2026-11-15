"""Generate only HE/AV into the shared repo; audit every unrelated RP/DP byte.

Run after isolated builds pass. Never restores or reformats another session's
files. Shared JSON is permitted to change only by inserting this task's keys.
"""
from __future__ import annotations
import hashlib,json,subprocess,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'_tools/heart_of_ender_ref/build_validation'
KEYS=('heart_of_ender','arch_visage')
SHARED={'rpg/data/minecraft/tags/function/load.json','rpg/data/minecraft/tags/function/tick.json',
        'resourcepack/assets/rpg/sounds.json','resourcepack/assets/rpg/lang/zh_cn.json',
        'resourcepack/assets/rpg/lang/en_us.json'}

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def own(path):
    for key in KEYS:
        for prefix in (f'rpg/data/rpg/function/{key}/',f'rpg/data/rpg/predicate/{key}/',
                       f'resourcepack/assets/rpg/models/{key}/',f'resourcepack/assets/rpg/items/{key}/',
                       f'resourcepack/assets/rpg/textures/item/{key}/',f'resourcepack/assets/rpg/sounds/{key}/'):
            if path.startswith(prefix):return True
        if path==f'rpg/{key}_debug_manifest.json':return True
    return False
def snapshot():
    hashes={};shared={}
    for folder in ('rpg','resourcepack'):
        for path in (ROOT/folder).rglob('*'):
            if not path.is_file():continue
            rel=path.relative_to(ROOT).as_posix()
            if own(rel):continue
            if rel in SHARED:shared[rel]=json.loads(path.read_text('utf8'))
            else:hashes[rel]=sha(path)
    return hashes,shared
def strip_own(path,doc):
    if '/tags/function/' in path:
        result=dict(doc)
        result['values']=[v for v in doc['values'] if not any((v if isinstance(v,str) else v.get('id','')).startswith('rpg:'+k+'/') for k in KEYS)]
        return result
    return {k:v for k,v in doc.items() if not any(k.startswith(p) for key in KEYS for p in (key+'.','subtitles.rpg.'+key+'.'))}

def main():
    isolated=Path(json.loads((OUT/'snapshot.json').read_text('utf8'))['snapshot'])
    build=json.loads((OUT/'build_results.json').read_text('utf8'))
    if not build['all_passed'] or build['snapshot']!=str(isolated):
        raise ValueError('Full isolated build has not passed')
    before,shared=snapshot()
    protected={n:sha(ROOT/n) for n in ('_tools/display_mob.py','_tools/opt_runtime_hotpaths.py','_data_loot.json','_guide_sections.json') if (ROOT/n).is_file()}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'workspace_before.json').write_text(json.dumps({'unrelated_hashes':before,'shared':shared,'protected':protected},ensure_ascii=False,indent=2)+'\n','utf8')
    for key in KEYS:
        proc=subprocess.run([sys.executable,'-X','utf8',str(ROOT/'_tools'/('add_'+key+'.py')),str(ROOT/'resourcepack'),str(ROOT/'rpg')],cwd=ROOT,check=True)
    after,after_shared=snapshot()
    drift=[p for p in sorted(set(before)|set(after)) if before.get(p)!=after.get(p)]
    shared_drift=[p for p in SHARED if strip_own(p,shared.get(p,{}))!=strip_own(p,after_shared.get(p,{}))]
    protected_drift=[p for p,h in protected.items() if sha(ROOT/p)!=h]
    def task_hashes(base):
        return {p.relative_to(base).as_posix():sha(p) for folder in ('rpg','resourcepack')
                for p in (base/folder).rglob('*') if p.is_file() and own(p.relative_to(base).as_posix())}
    built_task=task_hashes(isolated);live_task=task_hashes(ROOT)
    build_mismatch=[p for p in sorted(set(built_task)|set(live_task)) if built_task.get(p)!=live_task.get(p)]
    report={'success':not(drift or shared_drift or protected_drift or build_mismatch),'unrelated_files_checked':len(before),
            'unrelated_changed':drift,'shared_unrelated_entries_changed':shared_drift,'protected_changed':protected_drift,
            'isolated_build':str(isolated),'own_files_compared_to_full_build':len(built_task),
            'own_files_different_from_full_build':build_mismatch,
            'models':{k:json.loads((ROOT/'rpg'/(k+'_debug_manifest.json')).read_text('utf8')) for k in KEYS},
            'policy':'on drift, stop and report; never roll back another session'}
    (OUT/'workspace_integration.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf8')
    print(json.dumps({k:report[k] for k in ('success','unrelated_files_checked','unrelated_changed','shared_unrelated_entries_changed','protected_changed')},ensure_ascii=False))
    if not report['success']:raise SystemExit('Concurrent or unexpected differences detected; inspect report without rollback')

if __name__=='__main__':main()
