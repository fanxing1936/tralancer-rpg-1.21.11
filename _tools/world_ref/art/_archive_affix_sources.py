from pathlib import Path
import json
import shutil
HERE=Path(__file__).resolve().parent
path=HERE/'affix_generation_manifest.json'
specs=json.loads(path.read_text(encoding='utf-8'))
(HERE/'_generation_affix').mkdir(exist_ok=True)
for s in specs:
    history=s.get('generation_history') or [dict(attempt=1,original_generated_path=s['source'],prompt=s['prompt'])]
    for h in history:
        dst=HERE/'_generation_affix'/f"{s['id']}_attempt_{h['attempt']}.png"
        shutil.copy2(h['original_generated_path'],dst)
        h['source']=dst.relative_to(HERE).as_posix()
    adopted=next(h for h in history if h['attempt']==s.get('adopted_attempt',1))
    s.update(source=adopted['source'],prompt=adopted['prompt'],generation_history=history,attempts=len(history),adopted_attempt=adopted['attempt'])
path.write_text(json.dumps(specs,ensure_ascii=False,indent=2),encoding='utf-8')
print('Saved',sum(s['attempts'] for s in specs),'affix source images.')
