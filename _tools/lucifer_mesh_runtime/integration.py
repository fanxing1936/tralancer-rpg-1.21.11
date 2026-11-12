"""Append only guarded appearance calls to existing lord-one skill functions."""
from pathlib import Path
import hashlib
import json

MARK = b'# Lucifer mesh appearance (add_lucifer_model.py)'

def ensure_tick_order(datapack):
    root = Path(datapack).resolve()
    if not (root/'data/rpg/function/lucifer_lord/tick.mcfunction').is_file():
        return {'status': 'runtime_absent'}
    path = root/'data/minecraft/tags/function/tick.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    identity = lambda v: v if isinstance(v, str) else v.get('id')
    early, late, phase2 = 'rpg:lucifer_lord/tick', 'rpg:lucifer_lord/tick_late', 'rpg:lucifer_p2/tick'
    values = [v for v in data['values'] if identity(v) not in [early, late]]
    before = next((i for i,v in enumerate(values) if identity(v) == phase2), len(values))
    values.insert(before, early)
    values.append(late)
    data['values'] = values
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return {'status': 'ordered', 'phase1_before_phase2': True, 'late_is_final': True}

def integrate_hooks(datapack, skills):
    root = Path(datapack).resolve() / 'data/rpg/function'
    result = []
    for name, clip in skills.items():
        path = root / 'taint' / (name + '.mcfunction')
        if not path.is_file():
            result.append({'hook': name, 'status': 'source_function_absent'})
            continue
        raw = path.read_bytes()
        line = ('execute if entity @s[tag=rpg.lu,tag=!rpg.lu.phase2] '
                'run function rpg:lucifer_lord/skill/' + name).encode()
        if MARK in raw:
            if raw.count(MARK) != 1 or raw.count(line) != 1:
                raise ValueError('Unexpected existing Lucifer appearance hook: ' + str(path))
            result.append({'hook': name, 'clip': clip, 'status': 'already_present'})
            continue
        suffix = (b'' if raw.endswith(b'\n') else b'\n') + MARK + b'\n' + line + b'\n'
        path.write_bytes(raw + suffix)
        assert path.read_bytes()[:-len(suffix)] == raw
        result.append({'hook': name, 'clip': clip, 'status': 'appended',
                       'original_sha256': hashlib.sha256(raw).hexdigest(),
                       'existing_commands_byte_exact': True})
    return result
