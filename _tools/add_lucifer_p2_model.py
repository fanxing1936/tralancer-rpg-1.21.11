"""Jungle Abomination phase-two appearance, source animations and original sounds."""
from pathlib import Path
import argparse,hashlib,json,os,shutil
from display_mob import Mob,build,wj,playsound
from dungeons_conversion import materials,runtime,sounds

HERE=Path(__file__).resolve().parent
REF=HERE/'lucifer_p2_ref'

# 材质模式（2026-11-08，用户在 Iris + Complementary 光影下看到只有外形、满身黑块）：
# hdr   = 原交付：面带标记色，靠自定义 core shader 解码出贴图、微光与十秒脉动；
#         光影包会替换 core shader，标记色就被当成普通染色乘上去。
# plain = 默认：不加标记色、不装 shader，发光象限的面用 light_emission 满亮度，
#         任何着色器下都按普通物品贴图显示；代价是没有脉动。
MATERIAL=os.environ.get('LUCIFER_P2_MATERIAL','plain')


def plain_part_model(model):
    """发光象限（左下）里的面所在元素满亮度；UV、几何不变。"""
    eps=1e-5
    for element in model['elements']:
        for face in element['faces'].values():
            u0,v0,u1,v1=face['uv']
            if min(u0,u1)>=-eps and max(u0,u1)<=8+eps and min(v0,v1)>=8-eps and max(v0,v1)<=16+eps:
                element['light_emission']=15
                break
    return model

def configured_mob(ref=REF):
    ref=Path(ref)
    document=json.loads((ref/'lucifer_p2.bbmodel').read_text(encoding='utf-8'))
    parts=json.loads((ref/'parts.json').read_text(encoding='utf-8'))
    if len(document.get('animations',[]))!=18:
        raise ValueError('Run convert_dungeons.py --phase 2 first: all 18 source animations are required.')
    clips=[(a['name'].removeprefix('animation.'),1,a['loop']=='loop') for a in document['animations']]
    if [n for n,_,_ in clips[:2]]!=['jungleabomination_idle','jungleabomination_walk']:
        raise ValueError('Original idle/walk must be the first two clips')
    # 二阶段载体被 add_lucifer_fight.py 放大到 2.5 倍；座位实测随之从 2.0 升到 5.0。
    mob=Mob(key='lucifer_p2',label='路西法·二阶段',generator=Path(__file__).name,
        bbmodel=str(ref/'lucifer_p2.bbmodel'),parts=[(p['name'],p['bones']) for p in parts],
        glow=json.loads((ref/'glow_bones.json').read_text(encoding='utf-8')),
        seat=2.*2.5,tag='rpg.lu2',score='rpg_lu2',clips=clips,model_scale=document['display_dungeons']['model_scale'],
        face_rotation=True,idle_clip=clips[0][0],walk_clip=clips[1][0],
        affine_parts=document['display_dungeons']['deforming_parts'],
        hold_clips=('jungleabomination_death',),pose_cache=True,bulk_pose=True,tick_rounding='ceil',
        **sounds.configuration(ref))
    mob.on_hurt.append(playsound(mob,sounds.HURT_FOLEY,1.))
    return mob

def generate(resourcepack,datapack,ref=REF):
    ref=Path(ref);rp=Path(resourcepack);dp=Path(datapack)
    mob=configured_mob(ref)
    baked,first=build(mob,str(rp),str(dp))
    counts={'nonglow':0,'glow':0,'elements':0}
    if MATERIAL=='plain':
        for part,_ in mob.parts:
            path=rp/'assets/rpg/models/lucifer_p2'/(part+'.json')
            wj(str(path),plain_part_model(json.loads(path.read_text(encoding='utf-8'))))
    for part,_ in (mob.parts if MATERIAL=='hdr' else ()):
        path=rp/'assets/rpg/models/lucifer_p2'/(part+'.json')
        model,stats=materials.configure_part_model(json.loads(path.read_text(encoding='utf-8')))
        wj(str(path),model)
        for key in counts:counts[key]+=stats[key]
        path=rp/'assets/rpg/items/lucifer_p2'/(part+'.json')
        wj(str(path),materials.configure_item_definition(json.loads(path.read_text(encoding='utf-8'))))
    contract=json.loads((ref/'material/material_contract.json').read_text(encoding='utf-8'))
    for ext in (('vsh','fsh') if MATERIAL=='hdr' else ()):
        source=ref/'material/rp/assets/minecraft/shaders/core'/(materials.SHADER_NAME+'.'+ext)
        target=rp/'assets/minecraft/shaders/core'/source.name
        if target.exists():
            actual=hashlib.sha256(target.read_bytes()).hexdigest()
            if actual not in (hashlib.sha256(source.read_bytes()).hexdigest(),contract['vanilla_shader_sha256'][ext]):
                raise ValueError('Existing unrelated shader override requires an explicit merge: '+str(target))
        target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
    result=runtime.write(mob,baked,first,ref)
    result.update(material_faces=counts,sounds=sounds.validate_sources(ref),
                  sound_runtime=sounds.finalize_runtime_sound_policies(mob),
                  sound_debug=sounds.write_debug_functions(dp),
                  phase1_guard=runtime.guard_phase1_entry(dp))
    return mob,baked,result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('resourcepack',nargs='?',type=Path,default=HERE.parent/'resourcepack')
    p.add_argument('datapack',nargs='?',type=Path,default=HERE.parent/'rpg')
    p.add_argument('--ref',type=Path,default=REF);p.add_argument('--report',type=Path)
    a=p.parse_args();mob,baked,result=generate(a.resourcepack,a.datapack,a.ref)
    if a.report:wj(str(a.report),result)
    print('lucifer_p2: %d parts, %d source clips, %d sound events; material=%s%s.'%(
        len(mob.parts),len(baked),len(mob.sounds),MATERIAL,' (microglow + 200-tick pulse)' if MATERIAL=='hdr' else ' (shader-free)'))

if __name__=='__main__':main()
