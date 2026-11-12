"""Reproduce Lucifer phase two's model, original animations and material data.

Usage: python _tools/convert_dungeons.py --phase 2
Only phase two is owned here. --static explicitly reproduces checkpoint A.
Dependencies: Python 3, NumPy, Pillow. No game files are modified.
"""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys,tempfile,uuid

def main():
    here=Path(__file__).resolve().parent
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--phase',choices=['2'],default='2')
    p.add_argument('--source-dir',type=Path,default=here/'lucifer_p2_ref')
    p.add_argument('--output-dir',type=Path)
    p.add_argument('--work-dir',type=Path)
    # Match P1 source units: armored/SageHat bbox is 44.47583139202386 BB.
    # Read-only 216-wedge audit: validation/scale_alignment/REPORT.md.
    p.add_argument('--blocks-per-cm',type=float,default=.008633902683354115)
    p.add_argument('--model-scale',type=float,default=7.194918902795097)
    p.add_argument('--authoring-model-scale',type=float,default=10.,help='Fixed authoring tolerance/atlas scale; must be >= runtime model scale')
    p.add_argument('--static',action='store_true',help='Explicitly generate only the checkpoint-A static model')
    args=p.parse_args()
    ref=args.source_dir.resolve();output=(args.output_dir or ref).resolve()
    if args.blocks_per_cm<=0 or args.model_scale<=0:p.error('Scale must be positive')
    if args.authoring_model_scale < args.model_scale:p.error('Authoring model scale must be >= runtime model scale')
    source_hash=hashlib.sha256((ref/'source/SK_Abomination_02.source.glb').read_bytes()).hexdigest()
    recovery=json.loads((ref/'validation/recovery_geometry.json').read_text(encoding='utf-8'))
    if recovery.get('source_mesh_sha256')!=source_hash:
        p.error('The recovered geometry map does not match this extracted source mesh')
    existing=output/'lucifer_p2.bbmodel'
    if args.static and existing.exists() and json.loads(existing.read_text(encoding='utf-8')).get('animations'):
        raise SystemExit('Refusing to replace an animated model with checkpoint-A static data.')
    work=(args.work_dir or Path(tempfile.gettempdir())/'tralancer-dungeons-p2'/str(uuid.uuid4())).resolve()
    if work==output or work.is_relative_to(output) or output.is_relative_to(work):
        p.error('Work and output directories must be separate and not nested')
    work.mkdir(parents=True,exist_ok=False)
    modules=here/'dungeons_conversion'
    stages=[
      ('phase2_static.py',['--source-dir',str(ref),'--out-dir',str(work/'planes'),
                          '--unit-scale',str(round(args.blocks_per_cm*16/args.model_scale,15)),'--model-scale',str(args.authoring_model_scale)]),
      ('merge_recovered_boxes.py',['--candidate',str(work/'planes'),'--recovery',str(ref/'validation/recovery_geometry.json'),'--output',str(work/'boxed')]),
      ('apply_glow_layers.py',['--candidate',str(work/'boxed'),'--mask',str(work/'planes/atlas_emission_support.png'),'--output',str(work/'complete')]),
    ]
    for script,arguments in stages:
        subprocess.run([sys.executable,'-B',str(modules/script),*arguments],check=True)
    animation_count=0
    if not args.static:
        from dungeons_conversion import animations,materials
        from mc_env import JAR
        complete=work/'complete'
        # Material preparation deliberately receives a fresh static atlas; the
        # canonical atlas may already contain its auxiliary quadrant on a rebuild.
        for relative in ('source/SK_Abomination_02.source.glb','source/skeleton.meta.json',
                         'T_Jungle_Abomination_M6.png','T_Jungle_Abomination_E_M6.png'):
            target=complete/relative;target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ref/relative,target)
        document=json.loads((complete/'lucifer_p2.bbmodel').read_text(encoding='utf-8'))
        document,data=animations.author_animations(document,ref)
        (complete/'lucifer_p2.bbmodel').write_text(json.dumps(document,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
        (complete/'validation/animation_conversion.json').write_text(json.dumps(data['validation'],ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
        material_dir=complete/'material'
        materials.prepare(complete,material_dir,JAR)
        material_document=json.loads((material_dir/'lucifer_p2_material_preview.bbmodel').read_text(encoding='utf-8'))
        material_document['display_dungeons']['checkpoint']='B_assets_generated'
        (complete/'lucifer_p2.bbmodel').write_text(json.dumps(material_document,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
        shutil.copyfile(material_dir/'atlas.png',complete/'atlas.png')
        animation_count=len(material_document['animations'])
    # Freeze geometry, UV baking and animation simplification at authoring scale.
    # Apply only the external runtime scale after the complete model is authored.
    final_path=work/'complete/lucifer_p2.bbmodel'
    final_document=json.loads(final_path.read_text(encoding='utf-8'))
    final_document['display_dungeons'].update(model_scale=args.model_scale,
        authoring_model_scale=args.authoring_model_scale,common_blocks_per_source_cm=args.blocks_per_cm)
    final_path.write_text(json.dumps(final_document,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    copied=[]
    for src in sorted((work/'complete').rglob('*')):
        if not src.is_file():continue
        relative=src.relative_to(work/'complete');target=output/relative
        target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,target)
        digest=hashlib.sha256(src.read_bytes()).hexdigest()
        if hashlib.sha256(target.read_bytes()).hexdigest()!=digest:raise RuntimeError(f'Copy verification failed: {target}')
        copied.append({'file':relative.as_posix(),'bytes':target.stat().st_size,'sha256':digest})
    manifest={'checkpoint':'A_static' if args.static else 'B_assets_generated','source_mesh_sha256':hashlib.sha256((ref/'source/SK_Abomination_02.source.glb').read_bytes()).hexdigest(),
              'blocks_per_cm':args.blocks_per_cm,'model_scale':args.model_scale,
              'authoring_model_scale':args.authoring_model_scale,'outputs':copied,
              'animations_authored':animation_count,'runtime_integrated':False,'work_directory':str(work)}
    (output/'conversion_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Phase-two model written to {output}; {animation_count} source animations. Runtime is generated separately.')

if __name__=='__main__':main()
