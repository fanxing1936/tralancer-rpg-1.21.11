from pathlib import Path
import json
import shutil
HERE=Path(__file__).resolve().parent
manifest=HERE/'generation_manifest.json'
specs=json.loads(manifest.read_text(encoding='utf-8'))
retries={r['id']:r for r in json.loads((HERE/'_retry_results.json').read_text(encoding='utf-8'))}
(HERE/'_generation').mkdir(exist_ok=True)
for spec in specs:
    history=spec.get('generation_history') or [dict(attempt=1,original_generated_path=spec['source'],prompt=spec['prompt'])]
    if spec['id'] in retries and len(history)==1:
        r=retries[spec['id']]
        history.append(dict(attempt=2,original_generated_path=r['source'],prompt=r['prompt']))
    for h in history:
        dst=HERE/'_generation'/f"{spec['id']}_attempt_{h['attempt']}.png"
        shutil.copy2(h['original_generated_path'],dst)
        h['source']=dst.relative_to(HERE).as_posix()
    chosen=history[-1]
    spec.update(source=chosen['source'],prompt=chosen['prompt'],attempts=len(history),adopted_attempt=chosen['attempt'],generation_history=history)
    if spec['id']=='title_ledger':
        spec['palette']=['#211D26','#4C4550','#DCCBAA']
    if spec['id']=='title_waverer':
        spec['sampling_phase']=[0.0,0.4]
manifest.write_text(json.dumps(specs,ensure_ascii=False,indent=2),encoding='utf-8')
print('Archived',sum(len(s['generation_history']) for s in specs),'generation attempts for',len(specs),'sprites.')
