"""M3 嘴/十字光束接口坐标，只记录模型空间，不生成特效或玩法。"""
import argparse
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
import display_mob as dm
from heart_of_ender_blockbench import REF

def point(matrix, p):
    return [round(sum(matrix[i][j]*p[j] for j in range(3))+matrix[i][3],6) for i in range(3)]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model',type=Path,default=REF/'heart_of_ender.bbmodel')
    args=parser.parse_args()
    path=args.model.resolve()
    document=json.loads(path.read_text(encoding='utf8'))
    version=document.get('unhandled_root_fields',{}).get('material_status',{}).get('version')
    output_dir=REF/('m3_material_v3' if version=='M3 material v3' else
                   'm3_material_v2' if version=='M3 material v2' else 'm3_motion')
    mob=SimpleNamespace(bbmodel=path,anim_from=None,key='heart_of_ender')
    bones,_,_=dm.load_bbmodel(mob)
    clips=dm.load_animations(mob)
    base=json.loads((REF/'m2_sockets.json').read_text('utf8'))
    samples=[]
    for clip,time in [('idle',0),('mortar',1.2),('mortar',2.0),('cross_beam',1.0),('cross_beam',2.0),('cross_beam',3.0)]:
        sockets=[]
        for s in base['sockets']:
            if s['name'].startswith('cross_') and clip not in ('idle','cross_beam'):continue
            if s['name']=='mouth_center' and clip not in ('idle','mortar'):continue
            W=dm.posed_matrix(bones,s['bone'],clips[clip],time)
            forward=[round(-W[i][2],6) for i in range(3)]
            sockets.append({'name':s['name'],'bone':s['bone'],'local_unposed_point':s['bbmodel_unrotated_point'],
                'posed_model_point':point(W,s['bbmodel_unrotated_point']),
                'bone_forward_minus_z':forward,
                'status':'模型表面预留锚点；原作准确发射骨与特效方向未知'})
        samples.append({'clip':clip,'time':time,'sockets':sockets})
    report={'bbmodel_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'coordinate_system':'+Y up, facing -Z; unscaled model units, not Minecraft blocks',
        'model_scale':None,'carrier_seat':None,
        'mouth_note':'mouth_center跟随上颅的闭嘴缝参考点；张口后仍是上唇出口候选，不谎称上下颚动态中点',
        'cross_note':'cross_north/east/south/west是小人躯干四面候选；顺时针光束扫描属于未来特效，未生成光束',
        'samples':samples}
    output=output_dir/'sockets.json'
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('已按保存模型记录6个动作时点的接口坐标：'+str(output))

if __name__=='__main__':main()
