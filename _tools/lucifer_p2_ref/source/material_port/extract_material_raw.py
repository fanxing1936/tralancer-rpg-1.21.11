"""Reuse the existing exact PAK reader; all new files stay in material_port."""
import hashlib
import json
import os
from pathlib import Path
import sys
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent
EXISTING=Path(r'D:\agent\codex\TRA\work\lucifer_original')
sys.path.insert(0,str(EXISTING))

def audit(event,args):
    targets=[]
    if event=='open':
        path,mode,flags=args
        if isinstance(path,(str,bytes,os.PathLike)) and flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND):targets=[path]
    elif event in ('os.mkdir','os.remove','os.rmdir','os.unlink','os.chmod'):targets=[args[0]]
    elif event in ('os.rename','os.replace'):targets=list(args[:2])
    elif event=='subprocess.Popen':raise RuntimeError('No external processes needed for exact raw extraction')
    for target in targets:
        if not Path(os.fsdecode(target)).resolve().is_relative_to(OUT):raise RuntimeError('Write outside material_port refused')
sys.addaudithook(audit)
import pak_index
catalog=json.loads((EXISTING/'list.json').read_text(encoding='utf-8'))
pak_index.ROOT=OUT  # KEY_FILE retains the existing private local key path; never serialized.
requested=['/Game/Actors/Characters/Enemies/JungleAbomination/M_JungleAbomination','/Game/Models/Master_ModelMaterial']
selected=[row for row in catalog['files'] if Path(row['path']).stem in ('M_JungleAbomination','Master_ModelMaterial')]
source_paths=sorted({pak_index.PAKS/row['pak'] for row in selected})
before={str(path):[path.stat().st_size,path.stat().st_mtime_ns] for path in source_paths}
manifest=pak_index.extract_exact(catalog,requested)
import ue4_bp
results=[]
for stem in requested:
    path=OUT/'raw'/Path(stem.lstrip('/')+'.uasset')
    package=ue4_bp.Package(path)
    parsed=package.dump()
    output=OUT/(path.stem+'.parsed.json')
    output.write_text(json.dumps(parsed,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for obj in parsed['exports']:
        if obj['name'] not in ('M_JungleAbomination','Master_ModelMaterial'):continue
        tagged=obj.get('tagged_property_bytes')
        start=obj['uexp_offset']+tagged if tagged is not None else None
        results.append({'package':stem,'object':obj['name'],'class':obj['class_path'],
            'header_bytes':len(package.header),'uexp_bytes':len(package.payload),
            'export_serial_offset':obj['serial_offset'],'export_uexp_offset':obj['uexp_offset'],
            'export_serial_bytes':obj['serial_bytes'],'tagged_property_bytes':tagged,
            'post_tagged_native_start_uexp':start,'remaining_native_bytes':obj.get('remaining_native_bytes'),
            'note':'Post-tagged native offset is an evidence boundary, not a claimed material-resource start. Guid/cooked/resource headers must still be parsed.',
            'native_prefix_hex':package.payload[start:start+96].hex() if start is not None else None,
            'parsed_file':str(output),'raw_uasset':str(path),'raw_uexp':str(path.with_suffix('.uexp'))})
after={str(path):[path.stat().st_size,path.stat().st_mtime_ns] for path in source_paths}
if before!=after:raise RuntimeError('PAK source stat changed during read')
report={'scope':'Exact two material packages only; existing reader/key/index reused read-only; all new files confined to material_port.',
        'pak_lengths_and_mtime_unchanged':True,'source_paks':before,'materials':results,
        'tool_sources':{name:hashlib.sha256((EXISTING/name).read_bytes()).hexdigest() for name in ('pak_index.py','ue4_bp.py')},
        'raw_manifest':str(OUT/'raw_manifest.json')}
(OUT/'raw_material_offsets.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=True,indent=2))
