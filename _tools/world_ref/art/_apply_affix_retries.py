from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
p=HERE/'affix_generation_manifest.json'
specs=json.loads(p.read_text(encoding='utf-8'))
for r in json.loads((HERE/'_affix_retry_results.json').read_text(encoding='utf-8')):
    s=next(s for s in specs if s['id']==r['id'])
    if not any(h['attempt']==r['attempt'] for h in s['generation_history']):
        s['generation_history'].append(dict(attempt=r['attempt'],original_generated_path=r['source'],prompt=r['prompt']))
    s['adopted_attempt']=r['attempt']
p.write_text(json.dumps(specs,ensure_ascii=False,indent=2),encoding='utf-8')
print('Recorded',len(json.loads((HERE/'_affix_retry_results.json').read_text(encoding='utf-8'))),'revisions')
