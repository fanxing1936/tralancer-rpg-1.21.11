"""Read-only UE4.22 inline uniform-expression evidence parser for MI_NatureArmor.

The legacy serializer structure is independently documented by
https://github.com/DarkStarSword/3d-fixes/blob/master/extract_unreal_shaders.py
UE4.22 FMaterialParameterInfo and later fields are verified against this asset's
type boundaries and the duplicate SM4 resource, rather than presumed UE5 layout.
Does not write game data or Blockbench models.
"""
from pathlib import Path
import json, struct, hashlib, math

ROOT = Path(__file__).resolve().parent
RAW = ROOT / 'raw/Game/Content_Season2/Actors/Equipment/Armor/NatureArmor/MI_NatureArmor.uexp'
DATA = RAW.read_bytes()
NAMES = json.loads((ROOT / 'shader/MI_NatureArmor_inline_names.json').read_text())['names']

class Reader:
    def __init__(self, pos): self.pos = pos
    def read(self, fmt):
        values = struct.unpack_from('<' + fmt, DATA, self.pos)
        self.pos += struct.calcsize('<' + fmt)
        return values[0] if len(values) == 1 else list(values)
    def name(self):
        off = self.pos
        i, n = self.read('ii')
        if not 0 <= i < len(NAMES) or not 0 <= n < 100000:
            raise ValueError(f'invalid FName at {off}: {i}, {n}')
        return NAMES[i] if n == 0 else NAMES[i] + '_' + str(n - 1)
    def parameter(self):
        return {'name': self.name(), 'association': self.read('B'), 'index': self.read('i')}
    def expr(self):
        start = self.pos
        name = self.name()
        t = name.removeprefix('FMaterialUniformExpression')
        out = {'start': start, 'type': t}
        if t in ('VectorParameter', 'ScalarParameter'):
            out['parameter'] = self.parameter()
            out['default'] = self.read('4f' if t == 'VectorParameter' else 'f')
        elif t == 'ComponentSwizzle':
            out['x'] = self.expr()
            out['indices'] = self.read('4b')
            out['num_elements'] = self.read('b')
        elif t == 'Constant':
            out['value'] = self.read('4f')
            out['value_type'] = self.read('B')
        elif t == 'FoldedMath':
            out['a'] = self.expr()
            out['b'] = self.expr()
            out['operation'] = self.read('B')
            out['value_type'] = self.read('I')
        elif t == 'Floor':
            out['x'] = self.expr()
        elif t == 'Min':
            out['a'] = self.expr()
            out['b'] = self.expr()
        elif t == 'TextureParameter':
            out['parameter'] = self.parameter()
            out['texture_index'] = self.read('i')
            out['sampler_source'] = self.read('i')
        elif t == 'Texture':
            out['texture_index'] = self.read('i')
            out['sampler_source'] = self.read('i')
        else:
            raise ValueError(f'unhandled {name} at {start}')
        out['end'] = self.pos
        return out
    def array(self, label):
        start = self.pos
        count = self.read('i')
        if not 0 <= count <= 200: raise ValueError(f'{label} invalid count {count} at {start}')
        result = {'start': start, 'count': count, 'expressions': []}
        for i in range(count):
            try: result['expressions'].append(self.expr())
            except Exception as e: raise ValueError(f'{label}[{i}] {e}') from e
        result['end'] = self.pos
        return result

def parse(pos):
    r = Reader(pos)
    result = {'start': pos}
    for field in ('UniformVectorExpressions', 'UniformScalarExpressions', 'Uniform2DTextureExpressions', 'UniformCubeTextureExpressions'):
        result[field] = r.array(field)
    result['end'] = r.pos
    return result

def summary_expr(e):
    t = e['type']
    if t in ('ScalarParameter', 'VectorParameter'): return e['parameter']['name']
    if t == 'ComponentSwizzle': return f"{summary_expr(e['x'])}.swizzle{e['indices'][:e['num_elements']]}"
    if t == 'Constant': return str(e['value'])
    if t == 'Floor': return f"Floor({summary_expr(e['x'])})"
    if t in ('FoldedMath', 'Min'): return f"{t}[{e.get('operation', '')}]({summary_expr(e['a'])},{summary_expr(e['b'])})"
    if t == 'TextureParameter': return e['parameter']['name'] + f"(texture={e['texture_index']}, sampler={e['sampler_source']})"
    return t

def evaluate(e, overrides):
    """Evaluate this asset's CPU-side scalar/vector uniform tree, not a shader."""
    t = e['type']
    if t in ('ScalarParameter', 'VectorParameter'):
        value = overrides.get(e['parameter']['name'], e['default'])
        return value if isinstance(value, list) else [value] * 4
    if t == 'Constant': return e['value']
    if t == 'ComponentSwizzle':
        x = evaluate(e['x'], overrides)
        return [x[i] if i >= 0 else 0.0 for i in e['indices']]
    if t == 'Floor': return [math.floor(v) for v in evaluate(e['x'], overrides)]
    a, b = evaluate(e['a'], overrides), evaluate(e['b'], overrides)
    if t == 'Min': return [min(x, y) for x, y in zip(a, b)]
    if t == 'FoldedMath':
        op = e['operation']
        if op == 0: return [x + y for x, y in zip(a, b)]
        if op == 1: return [x - y for x, y in zip(a, b)]
        if op == 2: return [x * y for x, y in zip(a, b)]
        if op == 3: return [x / y for x, y in zip(a, b)]
    raise ValueError(t)

def propdict(obj): return {p['name']: p['value'] for p in obj['properties']}

def overrides():
    parsed = json.loads((ROOT / 'MI_NatureArmor.parsed.json').read_text())
    props = propdict(parsed['exports'][0])
    result = {}
    for field in ('ScalarParameterValues', 'VectorParameterValues', 'TextureParameterValues'):
        for item in props[field]['items']:
            item = propdict(item)
            name = propdict(item['ParameterInfo'])['Name']
            result[name] = item['ParameterValue']
    return result

def resource_table(code):
    pos = 0
    def read():
        nonlocal pos
        v, = struct.unpack_from('<I', code, pos); pos += 4
        return v
    result = {'ResourceTableBits': read()}
    for field in ('ShaderResourceViewMap', 'SamplerMap', 'UnorderedAccessViewMap', 'ResourceTableLayoutHashes', 'TextureMap'):
        start = pos
        count = read()
        entries = [read() for _ in range(count)]
        result[field] = {'start': start, 'count': count, 'raw_u32': entries}
        if field in ('TextureMap', 'SamplerMap'):
            result[field]['decoded_material_entries'] = [
                {'token': f'0x{v:08x}', 'uniform_buffer_index': v >> 24,
                 'resource_index': (v >> 8) & 0xffff, 'bind_index': v & 0xff}
                for v in entries if v != 0xffffffff and v >> 24 == 3]
    assert code[pos:pos + 4] == b'DXBC', (pos, code[pos:pos + 4])
    result['dxbc_offset'] = pos
    return result

if __name__ == '__main__':
    result = parse(8734)
    second = parse(85458)
    assert DATA[result['start']:result['end']] == DATA[second['start']:second['end']]
    override = overrides()
    vector = result['UniformVectorExpressions']['expressions']
    scalar = result['UniformScalarExpressions']['expressions']
    slots = [{'source_kind': 'vector', 'index': i, 'buffer': f'cb3[{i}]',
              'expression': summary_expr(e), 'static_value': evaluate(e, override),
              'uexp_start': e['start'], 'uexp_end': e['end']} for i,e in enumerate(vector)]
    slots += [{'source_kind': 'scalar', 'index': i, 'buffer': f'cb3[{len(vector) + i // 4}].{"xyzw"[i % 4]}',
               'expression': summary_expr(e), 'static_value': evaluate(e, override)[0],
               'uexp_start': e['start'], 'uexp_end': e['end']} for i,e in enumerate(scalar)]
    shader = ROOT / 'shader/MI_NatureArmor/762fe3b6f361f38e14e6ec6c1b4e1f6f8a25d76c.bin'
    shader_data = shader.read_bytes()
    table = resource_table(shader_data)
    tex_entries = table['TextureMap']['decoded_material_entries']
    sampler_entries = table['SamplerMap']['decoded_material_entries']
    assert [(e['resource_index'],e['bind_index']) for e in tex_entries] == [(0,3),(2,4),(4,5),(6,6),(8,7)]
    assert [(e['resource_index'],e['bind_index']) for e in sampler_entries] == [(1,1),(3,2),(5,3),(7,4),(9,5)]
    assert slots[13+14]['static_value'] == 0.0
    assert slots[13+13]['static_value'] == 0.0
    mpc = json.loads((ROOT / 'MPC_Dungeons.parsed.json').read_text())
    mpc_props = propdict(mpc['exports'][0])
    death = propdict(mpc_props['ScalarParameters']['items'][0])
    assert death['ParameterName'] == 'DeathEmissive' and death['DefaultValue'] == 1.0
    assert DATA[11545:11561].hex() == mpc_props['StateId']
    result['_evidence'] = {
        'raw_path': str(RAW), 'raw_sha256': hashlib.sha256(DATA).hexdigest(),
        'SM4_start': second['start'], 'SM4_end': second['end'],
        'SM5_SM4_expression_bytes_identical': True,
        'matched_bytes': result['end'] - result['start'],
        'material_overrides': override,
        'buffer_float4_count': len(vector) + math.ceil(len(scalar) / 4),
        'slots': slots,
        'buffer_layout_basis': 'Legacy vector float4 array followed by scalar expressions packed 4-per-float4; exact 19 float4 slots and all shader uses agree. Inferred from legacy format + compiled shader, not a live GPU buffer capture.',
        'shader_path': str(shader), 'shader_code_sha256': hashlib.sha256(shader_data).hexdigest(),
        'shader_resource_table': table,
        'collection_state_id_offset': 11545, 'collection_state_id': mpc_props['StateId'],
        'death_emissive': death,
        'unparsed_uniform_set_tail': {'start': 11529, 'debug_description_length_offset': 11611,
                                     'note': 'Extra arrays/flags in this later UE4 version are not fully assigned semantic names. The collection state GUID is exact-matched, and subsequent DebugDescription FString is independently validated.'},
        'debug_description': DATA[11615:12150].rstrip(b'\0').decode('ascii'),
        'static_emissive_formula': 'linear(T_NatureArmor_S).B * [0.693310022354126,8,0] + linear(T_NatureArmor).RGB * 0.699999988079071',
        'static_conditions': 'Original cooked defaults + MI overrides; Time >= 0, Power=0, EnchantmentAdd=0, Flash Timestamp=-100, SelectionColor.rgb=0, DeathEmissive=1. Runtime overrides and scene exposure are outside this snapshot.',
        'srgb': {'resolved_value': True, 'serialized_on_assets': False,
                 'basis': 'CUE4Parse UTexture.Deserialize GetOrDefault(SRGB,true), standard UE interpretation; direct game-native constructor not inspected',
                 'primary_source': 'https://github.com/FabianFG/CUE4Parse/blob/master/CUE4Parse/UE4/Assets/Exports/Texture/UTexture.cs'},
    }
    out = ROOT / 'shader/MI_NatureArmor_uniforms.json'
    out.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({'output': str(out), 'arrays': {k:v['count'] for k,v in result.items() if isinstance(v,dict) and 'count' in v},
                      'duplicate_SM4_identical': True, 'slots': len(vector) + math.ceil(len(scalar)/4),
                      'texture_binding': tex_entries[:2], 'status':'parsed and cross-checked'}, indent=2))
