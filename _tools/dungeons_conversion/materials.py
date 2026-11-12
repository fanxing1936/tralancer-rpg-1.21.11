"""Opt-in Jungle Abomination material for Java 1.21.11 and Blockbench.

Original PNGs and geometry stay intact. Shader mode uses a derived single atlas
whose otherwise unused fourth quadrant holds nearest-sampled source auxiliary
B, with opaque RGB data guards. No pack/client files are written implicitly.
"""
from __future__ import annotations
import argparse, base64, contextlib, copy, hashlib, io, json, math, sys, tempfile, zipfile
from pathlib import Path
import numpy as np
from PIL import Image

SCHEMA = 'dungeons-jungle-emissive-v1'
HALF = 2048
AUXILIARY_MAGIC = (19, 237, 255)  # R, G, A; B is the exact original sample.
NONGLOW_RGB = (37, 211, 0)
GLOW_RGB = (38, 211, 0)
NONGLOW_MARKER = (37 << 16) | (211 << 8)
GLOW_MARKER = (38 << 16) | (211 << 8)
INITIAL_COLORS = [16777215, NONGLOW_MARKER, GLOW_MARKER]
COLOR = np.array([1.0, 0.13600000739097595, 0.9861199855804443])
NATURAL = 0.6000000238418579
POWER = 10.0
PERIOD_TICKS = 200
SHADER_NAME = 'rendertype_item_entity_translucent_cull'
VANILLA_SHADER_SHA256 = {
    'vsh':'1dd0553f4f42043e9d7603f108d2963a20081b77580c814e20fef0f1eefe48af',
    'fsh':'f7d2074126564aba5e1d5c4c3a509474e8b7191670ee15ea7dd67d140033272e',
}

VERTEX_DECL = '''
// BEGIN LUCIFER_P2_OPT_IN declarations
flat out int lrp2Mode;
flat out int lrp2Phase;
out vec4 lrp2WhiteLight;
// END LUCIFER_P2_OPT_IN declarations
'''
VERTEX_MAIN = '''
    // BEGIN LUCIFER_P2_OPT_IN vertex
    ivec3 lrp2Bytes = ivec3(floor(Color.rgb * 255.0 + 0.5));
    lrp2Mode = 0;
    lrp2Phase = 0;
    if (lrp2Bytes.g == 211 && lrp2Bytes.b >= 0 && lrp2Bytes.b < 200) {
        if (lrp2Bytes.r == 37) lrp2Mode = 1;
        if (lrp2Bytes.r == 38) lrp2Mode = 2;
        lrp2Phase = lrp2Bytes.b;
    }
    // Separate white input: no division by tinted colors or zero components.
    lrp2WhiteLight = minecraft_mix_light(Light0_Direction, Light1_Direction, Normal, vec4(1.0, 1.0, 1.0, Color.a)) * texelFetch(Sampler2, UV2 / 16, 0);
    // END LUCIFER_P2_OPT_IN vertex
'''
COLOR_FUNCTIONS = '''
vec3 lrp2Linear(vec3 s) {
    return mix(s / 12.92, pow((s + 0.055) / 1.055, vec3(2.4)), step(vec3(0.04045), s));
}
vec3 lrp2SRGB(vec3 s) {
    s = max(s, vec3(0.0));
    return mix(12.92 * s, 1.055 * pow(s, vec3(1.0 / 2.4)) - 0.055, step(vec3(0.0031308), s));
}
vec3 lrp2DisplayMap(vec3 x) {
    // Explicit bounded display transform, shared with the BB preview.
    // ACES fitted curve; this is not a claim about the game's original exposure.
    return clamp((x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14), 0.0, 1.0);
}
vec3 lrp2Emission(vec3 albedo, float auxiliaryB, float phase) {
    float pulse = max(sin(6.283185307179586 * phase) / 3.0 + 2.0, 0.0);
    vec3 c = vec3(1.0, 0.13600000739097595, 0.9861199855804443);
    return albedo * 0.6000000238418579 + auxiliaryB * 10.0 * pulse * c * c;
}
'''
FRAGMENT_DECL = '''
// BEGIN LUCIFER_P2_OPT_IN declarations
flat in int lrp2Mode;
flat in int lrp2Phase;
in vec4 lrp2WhiteLight;
''' + COLOR_FUNCTIONS + '''
// END LUCIFER_P2_OPT_IN declarations
'''
FRAGMENT_MAIN = '''
    // BEGIN LUCIFER_P2_OPT_IN fragment
    if (lrp2Mode != 0) {
        ivec2 lrp2Extent = textureSize(Sampler0, 0);
        ivec2 lrp2Pixel = ivec2(floor(texCoord0 * vec2(lrp2Extent)));
        ivec2 lrp2Aux = lrp2Pixel + (lrp2Mode == 1 ? ivec2(0, 2048) : ivec2(2048, 0));
        if (all(greaterThanEqual(lrp2Aux, ivec2(0))) && all(lessThan(lrp2Aux, lrp2Extent))) {
            vec4 lrp2Packed = texelFetch(Sampler0, lrp2Aux, 0);
            // Opaque data prevents browser Canvas premultiplication rounding B.
            ivec3 lrp2Magic = ivec3(floor(vec3(lrp2Packed.rg, lrp2Packed.a) * 255.0 + 0.5));
            if (all(equal(lrp2Magic, ivec3(19, 237, 255)))) {
                // LOD0 on both inputs prevents mips crossing cutout/data tiles.
                vec4 lrp2Base = texelFetch(Sampler0, lrp2Pixel, 0);
                float lrp2Alpha = lrp2Base.a * lrp2WhiteLight.a * ColorModulator.a;
                if (lrp2Alpha < 0.1) discard;
                vec3 lrp2A = lrp2Linear(lrp2Base.rgb);
                vec3 lrp2S = lrp2Linear(lrp2Packed.rgb);
                vec3 lrp2Lit = lrp2A * lrp2WhiteLight.rgb;
                vec3 lrp2E = lrp2Emission(lrp2A, lrp2S.b, float(lrp2Phase) / 200.0);
                vec4 lrp2Color = vec4(lrp2SRGB(lrp2DisplayMap(lrp2Lit + lrp2E)) * ColorModulator.rgb, lrp2Alpha);
                fragColor = apply_fog(lrp2Color, sphericalVertexDistance, cylindricalVertexDistance, FogEnvironmentalStart, FogEnvironmentalEnd, FogRenderDistanceStart, FogRenderDistanceEnd, FogColor);
                return;
            }
        }
    }
    // END LUCIFER_P2_OPT_IN fragment
'''


def read_json(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def write_json(path, value):
    path=Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def digest(data): return hashlib.sha256(data).hexdigest()


def srgb_to_linear(value):
    x=np.asarray(value,dtype=np.float64)
    return np.where(x<=0.04045,x/12.92,((x+0.055)/1.055)**2.4)


def emission(albedo_linear, auxiliary_blue_linear, seconds):
    pulse=max(math.sin(math.tau*seconds/10.0)/3.0+2.0,0.0)
    return np.asarray(albedo_linear)*NATURAL+np.asarray(auxiliary_blue_linear)[...,None]*POWER*pulse*COLOR**2


def marker_colors(phase=0):
    if not isinstance(phase,int) or not 0<=phase<PERIOD_TICKS: raise ValueError('phase must be integer 0..199')
    return [16777215,NONGLOW_MARKER,GLOW_MARKER+phase]


def shader_sources(client_jar):
    with zipfile.ZipFile(client_jar) as archive:
        version=read_json_from_bytes(archive.read('version.json'))
        if version['id']!='1.21.11': raise ValueError('Only locally verified 1.21.11 shader layout is supported')
        source={ext:archive.read(f'assets/minecraft/shaders/core/{SHADER_NAME}.{ext}').decode('utf-8') for ext in ('vsh','fsh')}
    if 'lrp2' in source['vsh']+source['fsh']: raise ValueError('Input jar must contain original vanilla shader')
    for ext in source:
        if digest(source[ext].encode())!=VANILLA_SHADER_SHA256[ext]: raise ValueError('Client shader bytes differ from the verified 1.21.11 originals')
        if source[ext].count('void main() {')!=1: raise ValueError('Unexpected vanilla shader structure')
    vertex=source['vsh'].replace('void main() {',VERTEX_DECL+'\nvoid main() {',1)
    close=vertex.rfind('}')
    vertex=vertex[:close]+VERTEX_MAIN+vertex[close:]
    fragment=source['fsh'].replace('void main() {',FRAGMENT_DECL+'\nvoid main() {\n'+FRAGMENT_MAIN,1)
    # Strict compatibility invariant: deleting only our insertions restores bytes.
    assert vertex.replace(VERTEX_DECL+'\n','',1).replace(VERTEX_MAIN,'',1)==source['vsh']
    assert fragment.replace(FRAGMENT_DECL+'\n','',1).replace('\n'+FRAGMENT_MAIN,'',1)==source['fsh']
    return {'vsh':vertex,'fsh':fragment},source,version


def read_json_from_bytes(data): return json.loads(data.decode('utf-8'))


def prepare_atlas(ref, output):
    """Re-run the source rasterizer for exact albedo/auxiliary tile alignment."""
    ref=Path(ref);output=Path(output);output.mkdir(parents=True,exist_ok=True)
    if str(Path(__file__).parent) not in sys.path: sys.path.insert(0,str(Path(__file__).parent))
    sys.dont_write_bytecode = True
    import phase2_static
    atlas=np.asarray(Image.open(ref/'atlas.png').convert('RGBA')).copy()
    reference=np.asarray(Image.open(ref/'atlas_reference.png').convert('RGBA'))
    scale_config=read_json(ref/'lucifer_p2.bbmodel').get('display_dungeons',{})
    unit_scale=float(scale_config.get('unit_scale_java_pixels_per_ue_cm',0.0192))
    model_scale=float(scale_config.get('model_scale',10.0))
    if not math.isfinite(unit_scale) or not math.isfinite(model_scale) or min(unit_scale,model_scale)<=0:
        raise ValueError('Invalid source/model scale')
    if atlas.shape!=(HALF*2,HALF*2,4) or reference.shape!=(HALF,HALF,4): raise ValueError('Expected current 4096 atlas / 2048 reference layout')
    if np.any(atlas[HALF:,HALF:]): raise ValueError('Auxiliary quadrant is no longer empty; refuse overwrite')
    with tempfile.TemporaryDirectory(prefix='material_bake_',dir=output) as temp:
        temp=Path(temp)
        with contextlib.redirect_stdout(io.StringIO()):
            phase2_static.convert(ref/'source/SK_Abomination_02.source.glb',ref/'source/skeleton.meta.json',ref/'T_Jungle_Abomination_M6.png',temp/'base',unit_scale=unit_scale,model_scale=model_scale)
        actual=np.asarray(Image.open(temp/'base/atlas.png').convert('RGBA'))
        if not np.array_equal(actual,reference): raise ValueError('Albedo rasterizer output differs from canonical reference; refuse guessed auxiliary UVs')
        with contextlib.redirect_stdout(io.StringIO()):
            phase2_static.convert(ref/'source/SK_Abomination_02.source.glb',ref/'source/skeleton.meta.json',ref/'T_Jungle_Abomination_E_M6.png',temp/'aux',unit_scale=unit_scale,model_scale=model_scale)
        aux=np.asarray(Image.open(temp/'aux/atlas.png').convert('RGBA')).copy()
        regions=read_json(temp/'base/atlas_regions.json')
        aux_regions=read_json(temp/'aux/atlas_regions.json')
        assert [(r['offset'],r['size']) for r in regions]==[(r['offset'],r['size']) for r in aux_regions]
    support=np.asarray(Image.open(ref/'atlas_emission_support.png').convert('L'))>0
    assert np.array_equal((aux[:,:,2]>0)&(reference[:,:,3]>0),support)
    # Only source B is needed by the verified default formula. R/G/A carry a
    # guard; opaque alpha avoids Canvas premultiply/unpremultiply byte changes.
    # Original packed _E RGBA stays byte-identical in its separate source PNG.
    aux[:,:,0]=AUXILIARY_MAGIC[0];aux[:,:,1]=AUXILIARY_MAGIC[1];aux[:,:,3]=AUXILIARY_MAGIC[2]
    atlas[HALF:,HALF:]=aux
    Image.fromarray(atlas).save(output/'atlas.png')
    Image.fromarray(aux).save(output/'auxiliary_atlas_data.png')
    assert np.array_equal(atlas[:HALF],np.asarray(Image.open(ref/'atlas.png'))[:HALF])
    assert np.array_equal(atlas[HALF:,:HALF],np.asarray(Image.open(ref/'atlas.png'))[HALF:,:HALF])
    return {'size':[4096,4096],'unit_scale_java_pixels_per_ue_cm':unit_scale,'model_scale':model_scale,'reference_and_render_quadrants_pixel_identical':True,
            'auxiliary_source_sha256':digest((ref/'T_Jungle_Abomination_E_M6.png').read_bytes()),
            'albedo_source_sha256':digest((ref/'T_Jungle_Abomination_M6.png').read_bytes()),
            'original_atlas_sha256':digest((ref/'atlas.png').read_bytes()),
            'shader_atlas_sha256':digest((output/'atlas.png').read_bytes()),
            'auxiliary_support_matches_existing_partition':True,'cutout_tiles':len(regions)-1,
            'auxiliary_encoding':{'r':19,'g':237,'b':'exact original _E.B','a':255},'reference_tile_bake_pixel_identical':True}


def configure_part_model(model):
    """Return a p2-only model copy with marker tint indices and ordinary light."""
    model=copy.deepcopy(model);counts={'nonglow':0,'glow':0,'elements':len(model['elements'])}
    for element in model['elements']:
        element['light_emission']=0;element['shade']=True
        for face in element['faces'].values():
            if not face.get('texture'): continue
            u0,v0,u1,v1=face['uv'];eps=1e-5
            if min(u0,u1)>=8-eps and max(u0,u1)<=16+eps and min(v0,v1)>=-eps and max(v0,v1)<=8+eps:
                face['tintindex']=1;counts['nonglow']+=1
            elif min(u0,u1)>=-eps and max(u0,u1)<=8+eps and min(v0,v1)>=8-eps and max(v0,v1)<=16+eps:
                face['tintindex']=2;counts['glow']+=1
            else: raise ValueError('Face is not in a p2 render quadrant; refusing global/post-hoc tint conversion')
    return model,counts


def configure_item_definition(item):
    item=copy.deepcopy(item)
    model=item['model']
    if model['type']!='minecraft:model': raise ValueError('Expected direct item model')
    tints=model.setdefault('tints',[])
    if len(tints)>1: raise ValueError('Tint slots 1/2 already assigned')
    if not tints:tints.append({'type':'minecraft:custom_model_data','index':0,'default':16777215})
    tints.extend([{'type':'minecraft:custom_model_data','index':1,'default':NONGLOW_MARKER},
                  {'type':'minecraft:custom_model_data','index':2,'default':GLOW_MARKER}])
    return item


def preview_config(texture_uuid):
    return {'schema':SCHEMA,'albedo_uuid':texture_uuid,'auxiliary_quadrant':[2048,2048,2048,2048],
            'parameters':{'EmissiveBColor':COLOR.tolist(),'EmissiveBPower':POWER,'NaturalEmissive':NATURAL,
                          'SinusTempo':0.10000000149011612,'SinusVariation':3.0,'SinusMin':2.0,'SinusMax':0.0},
            'preview':{'display_transform':'ACES fitted + linear-to-sRGB','exposure':1.0,'period_seconds':10.0}}


def prepare(ref, output, client_jar):
    ref=Path(ref);output=Path(output);output.mkdir(parents=True,exist_ok=True)
    if output.resolve()==ref.resolve():raise ValueError('Use an isolated output directory')
    atlas_info=prepare_atlas(ref,output)
    sources,original,version=shader_sources(client_jar)
    for ext,text in sources.items():
        path=output/'rp/assets/minecraft/shaders/core'/f'{SHADER_NAME}.{ext}'
        path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8',newline='')
        (output/f'vanilla_{SHADER_NAME}.{ext}').write_text(original[ext],encoding='utf-8',newline='')
    model=read_json(ref/'lucifer_p2.bbmodel')
    model['textures'][0]['source']='data:image/png;base64,'+base64.b64encode((output/'atlas.png').read_bytes()).decode('ascii')
    model['textures'][0]['path']='atlas.png'
    model['dungeons_material_source']=preview_config(model['textures'][0]['uuid'])
    write_json(output/'lucifer_p2_material_preview.bbmodel',model)
    parts=read_json(ref/'parts.json');pulse_parts=[p['name']for p in parts if p.get('glow_bones')]
    contract={'schema':SCHEMA,'shader_name':SHADER_NAME,'client_version':version['id'],
              'tint_slots':{'reserved':[1,2],'nonglow':{'index':1,'rgb':list(NONGLOW_RGB),'integer':NONGLOW_MARKER},
                            'glow':{'index':2,'rgb_base':list(GLOW_RGB),'integer_base':GLOW_MARKER}},
              'initial_custom_model_data_colors':INITIAL_COLORS,'phase_range':[0,199],'period_ticks':200,
              'pulse_parts':pulse_parts,'pulse_part_count':len(pulse_parts),
              'update':'colors[2] = glow integer_base + global phase; only pulse-tagged part item_displays',
              'other_color_writes':'Do not replace reserved colors slots for red hurt tint; use entity outline.',
              'max_pulse_absolute_error_one_tick':math.tau/(3*200),
              'max_pulse_relative_error_one_tick':math.tau/(3*200)/(5/3),
              'source_time_phase':'A shared server tick clock, not recovered UE runtime start phase',
              'texture_filter':'p2 only: nearest texelFetch LOD0 for both base and auxiliary',
              'hdr_display_mapping':'ACES fitted curve applied to linear lit base + verified HDR emission, then sRGB; no bloom',
              'color_space':'Standard source sRGB decode assumption; original property omitted SRGB, default parser true; not GPU-captured.',
              'compatibility':'Removing inserted shader declaration/main blocks reproduces original strings byte-for-byte; no Globals uniform added',
              'atlas':atlas_info,'vanilla_shader_sha256':{k:digest(v.encode()) for k,v in original.items()},
              'derived_shader_sha256':{k:digest(v.encode()) for k,v in sources.items()}}
    assert len(pulse_parts)==8
    write_json(output/'material_contract.json',contract)
    (output/'runtime_example.mcfunction').write_text(
        '# Integration template; root owns actual objective/storage and tick hooks.\n'
        '# Initial item component: minecraft:custom_model_data={colors:'+str(INITIAL_COLORS).replace(' ','')+'}\n'
        'scoreboard players add #phase rpg.lu2_mat 1\n'
        'execute if score #phase rpg.lu2_mat matches 200.. run scoreboard players set #phase rpg.lu2_mat 0\n'
        f'scoreboard players set #color rpg.lu2_mat {GLOW_MARKER}\n'
        'scoreboard players operation #color rpg.lu2_mat += #phase rpg.lu2_mat\n'
        'execute store result storage rpg:lucifer_p2 material.glow_color int 1 run scoreboard players get #color rpg.lu2_mat\n'
        'execute as @e[type=minecraft:item_display,tag=rpg.lu2.pulse] run data modify entity @s item.components."minecraft:custom_model_data".colors[2] set from storage rpg:lucifer_p2 material.glow_color\n',encoding='utf-8')
    return contract


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ref',type=Path,default=Path(__file__).resolve().parents[1]/'lucifer_p2_ref')
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--client-jar',type=Path,required=True)
    args=parser.parse_args();result=prepare(args.ref,args.out,args.client_jar)
    print(json.dumps({'output':str(args.out),'pulse_parts':result['pulse_part_count'],'colors':INITIAL_COLORS,'atlas_sha256':result['atlas']['shader_atlas_sha256']},ensure_ascii=False))


if __name__=='__main__': main()
