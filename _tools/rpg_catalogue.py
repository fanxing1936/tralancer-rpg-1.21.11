"""Resolve rewards from the pack's canonical give catalogue without rebuilding components."""
from pathlib import Path
from make_boxes import LEGACY, EXORCISM_GLOBS, parse_give, component_blob, max_stack
from extract_items import node_to_py, flatten


def catalogue(dp):
    found = {}
    base=Path(dp)/'data/rpg/function'
    sources=list(LEGACY)
    for pattern in EXORCISM_GLOBS:
        sources.extend(str(p.relative_to(base)).replace('\\','/') for p in sorted(base.glob(pattern)))
    for rel in dict.fromkeys(sources):
        for line in (Path(dp) / 'data/rpg/function' / rel).read_text(encoding='utf-8').splitlines():
            item = parse_give(line)
            if not item or item[1] is None:
                continue
            ident, block, _ = item
            components = {key.split(':')[-1]: node_to_py(value)
                          for key, value, neg, _sep in block.entries if value is not None and not neg}
            full_name = flatten(components.get('custom_name'))[0]
            name = full_name.split(']', 1)[-1].strip() if full_name.startswith('[') else full_name
            if not name:
                continue
            record = {'id': ident, 'block': block, 'name': name, 'full_name': full_name,
                      'components': components, 'source': rel,
                      'item': ident + '[' + component_blob(block) + ']'}
            found.setdefault(name, []).append(record)
    return found


def resolve(items, name):
    matches = items.get(name, [])
    if len(matches) != 1:
        raise ValueError(f'Expected one canonical reward {name!r}, found {len(matches)}')
    return matches[0]


def give(items, name, count=1):
    if count < 1:
        raise ValueError('Reward count must be positive')
    return f'give @s {resolve(items, name)["item"]} {count}'
