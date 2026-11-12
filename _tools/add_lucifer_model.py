"""Lucifer phase-one original mesh appearance adapter; no combat value changes."""
from pathlib import Path
import argparse,json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'lucifer_mesh_runtime'))
from mesh_runtime import REPO,NativeRig,build,export_shaders,set_output_roots,sha
from mesh_runtime import SKILLS
from integration import integrate_hooks,ensure_tick_order

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('resourcepack',nargs='?',type=Path,default=REPO/'resourcepack')
    parser.add_argument('datapack',nargs='?',type=Path,default=REPO/'rpg')
    mode=parser.add_mutually_exclusive_group();mode.add_argument('--defer-shaders',action='store_true');mode.add_argument('--finalize-shaders',action='store_true')
    parser.add_argument('--model',type=Path,default=REPO/'_tools/lucifer_ref/lucifer.bbmodel')
    parser.add_argument('--model-scale',type=float)
    args=parser.parse_args()
    if args.finalize_shaders:
        set_output_roots(args.resourcepack,args.datapack);rig=NativeRig(args.model);result=export_shaders(rig,args.resourcepack.resolve(),None)
        if sha(args.model)!=rig.sha:raise ValueError('Native changed during shader finalization')
        for entry in result['fallback']:
            h=entry.get('phase2_material_module_sha256')
            if h and sha(REPO/'_tools/dungeons_conversion/materials.py')!=h:raise ValueError('Phase2 owning source changed during finalization')
        result={'mode':'finalize-shaders','model_sha256':rig.sha,'material':result}
    else:
        result=build(args.model,args.resourcepack,args.datapack,model_scale=args.model_scale,defer_shaders=args.defer_shaders)
        result['appearance_hooks']=integrate_hooks(args.datapack,SKILLS)
    result['tick_order']=ensure_tick_order(args.datapack)
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
