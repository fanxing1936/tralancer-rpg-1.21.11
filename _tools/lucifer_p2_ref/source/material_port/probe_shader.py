"""Read-only inline material/shader evidence extraction, using existing archive.
All emitted files are beside this script. No UE package/model modifications.
"""
from pathlib import Path
import ast, ctypes, hashlib, json, struct, zlib

OUT = Path(__file__).resolve().parent
OLD = Path(r'D:\agent\codex\TRA\work\lucifer_original')
ARCHIVE = OLD / 'shader/ShaderArchive-Dungeons-PCD3D_SM5.ushaderbytecode'
INDEX = json.loads((OLD / 'shader/archive_v1_index.json').read_text())

def disassemble(dxbc):
    lib = ctypes.WinDLL('d3dcompiler_47.dll')
    f = lib.D3DDisassemble
    f.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_uint, ctypes.c_char_p, ctypes.POINTER(ctypes.c_void_p)]
    f.restype = ctypes.c_long
    blob = ctypes.c_void_p()
    buf = ctypes.create_string_buffer(dxbc)
    hr = f(buf, len(dxbc), 0, None, ctypes.byref(blob))
    if hr: raise RuntimeError(f'D3DDisassemble HRESULT={hr:#x}')
    vtable = ctypes.cast(blob, ctypes.POINTER(ctypes.POINTER(ctypes.c_void_p))).contents
    pointer = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p)(vtable[3])(blob)
    size = ctypes.WINFUNCTYPE(ctypes.c_size_t, ctypes.c_void_p)(vtable[4])(blob)
    result = ctypes.string_at(pointer, size).rstrip(b'\0').decode('utf-8')
    ctypes.WINFUNCTYPE(ctypes.c_ulong, ctypes.c_void_p)(vtable[2])(blob)
    return result

def names_at(data, start):
    n, = struct.unpack_from('<i', data, start)
    p = start + 4
    names = []
    for _ in range(n):
        size, = struct.unpack_from('<i', data, p); p += 4
        assert 0 < size < 1000
        names.append(data[p:p+size-1].decode('utf-8')); p += size + 4
    return {'start': start, 'end': p, 'names': names}

def reader_env(data, names):
    # Reuse proven legacy expression implementation without executing its
    # hard-coded phase1 IO or main. Only class and pure function definitions.
    tree = ast.parse((OLD / 'parse_legacy_uniforms.py').read_text())
    nodes = [n for n in tree.body if isinstance(n, (ast.ClassDef, ast.FunctionDef)) and getattr(n, 'name', '') not in ('overrides',)]
    env = {'DATA': data, 'NAMES': names, 'struct': struct, 'math': __import__('math')}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), '<readonly legacy parser>', 'exec'), env)
    return env

def main():
    archive = ARCHIVE.read_bytes()
    materials = json.loads((OUT/'raw_material_offsets.json').read_text())['materials']
    for material in materials:
        name = material['object']
        dest = OUT/name; dest.mkdir(exist_ok=True)
        data = Path(material['raw_uexp']).read_bytes()
        names = names_at(data, material['post_tagged_native_start_uexp']+8)
        (dest/'inline_names.json').write_text(json.dumps(names, indent=2))
        env = reader_env(data, names['names'])
        # Locate valid serialized expression sets. Starts must be a positive
        # count followed by a registered uniform expression FName.
        type_ids = {i for i,s in enumerate(names['names']) if s.startswith('FMaterialUniformExpression')}
        candidates = []; errors = {}
        for pos in range(names['end'], len(data)-16):
            count, type_id, number = struct.unpack_from('<iii', data, pos)
            if 1 <= count <= 100 and type_id in type_ids and number == 0:
                try:
                    parsed = env['parse'](pos)
                    if parsed['Uniform2DTextureExpressions']['count'] > 0:
                        candidates.append(parsed)
                except (ValueError, struct.error, RecursionError) as e:
                    errors[str(pos)] = str(e)
        (dest/'uniform_candidates.json').write_text(json.dumps(candidates, indent=2))
        (dest/'uniform_parse_errors.json').write_text(json.dumps(errors, indent=2))
        matches = []
        for row in INDEX['rows']:
            binary_hash = bytes.fromhex(row['hash'])
            pos = data.find(binary_hash)
            if pos < 0: continue
            offsets=[]
            while pos >= 0:
                offsets.append(pos); pos=data.find(binary_hash, pos+1)
            match = dict(row, material_offsets=offsets)
            # Frequency 3 is pixel shader (as independently verified by DXBC).
            if row['frequency'] == 3:
                p = INDEX['data_offset']+row['offset']
                code = archive[p:p+row['size']]
                if len(code) != row['uncompressed']: code = zlib.decompress(code)
                assert len(code)==row['uncompressed']
                dxpos = code.index(b'DXBC')
                dxsize, = struct.unpack_from('<I', code, dxpos+24)
                dxbc = code[dxpos:dxpos+dxsize]
                asm = disassemble(dxbc)
                stem=dest/row['hash']
                stem.with_suffix('.bin').write_bytes(code)
                stem.with_suffix('.dxbc').write_bytes(dxbc)
                stem.with_suffix('.asm').write_text(asm)
                match.update(dxbc_offset=dxpos, dxbc_size=dxsize, asm_lines=len(asm.splitlines()), model=next((s for s in asm.splitlines() if s.startswith('ps_')), None))
            matches.append(match)
        result={'object':name,'raw_sha256':hashlib.sha256(data).hexdigest(),'name_count':len(names['names']), 'names_end':names['end'], 'uniform_candidates':len(candidates),'matches':matches}
        (dest/'matches.json').write_text(json.dumps(result, indent=2))
        print(json.dumps({k:v for k,v in result.items() if k!='matches'}), 'matched',len(matches),'pixel',sum(r['frequency']==3 for r in matches))
        print('uniforms',[(c['start'],c['end'],*[c[k]['count'] for k in ('UniformVectorExpressions','UniformScalarExpressions','Uniform2DTextureExpressions','UniformCubeTextureExpressions')]) for c in candidates])

if __name__ == '__main__': main()
