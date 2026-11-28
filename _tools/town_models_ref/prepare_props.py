"""从只读原作导出指定道具，并保留蓝图尺寸与骨架来源。"""
import json
import pathlib
import subprocess
import sys
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from dungeons_conversion import generic as G
from dungeons_conversion import blueprint as BP
NAMES = dict(pyre='SM_Bonfire', cage='SK_HangingVillagerCage', grave_a='SM_Gravestone0', grave_b='SM_Gravestone1', candles_a='SM_EvilCandles_01', candles_b='SM_EvilCandles_02', cauldron='SM_Cauldron_Witch', bell='SM_Bell', barrel='SM_Barrel', crate='SM_Crate', crate_pile='SM_CratePile', cart='SM_CartBroken')


def main():
    paths = [line.split('\t')[0] for line in pathlib.Path('D:/agent/dungeons_extract/index/pak_files.tsv').read_text().splitlines()]
    selected = {name: next(p[:-7] for p in paths if p.endswith('/' + mesh + '.uasset')) for name, mesh in NAMES.items()}
    work = HERE / '_work'
    work.mkdir(exist_ok=True)
    export = work / 'prop_sources'
    export.mkdir(parents=True, exist_ok=True)
    packages = [p + '.uasset' for p in selected.values()] + ['Dungeons/Content/Decor/Prefabs/Barrel/BP_Barrel.uasset', 'Dungeons/Content/Decor/Prefabs/Gravestone/BP_Gravestone0.uasset']
    packages += [p for p in paths if p.endswith('.uasset') and any('/'+folder+'/' in p for folder in ('Bonfire','Candle','CartBroken','Bell','Cauldron','Crate')) and '/BP_' in p]
    listing = work / 'prop_paths.json'
    listing.write_text(json.dumps(packages))
    key = pathlib.Path('D:/agent/dungeons_extract/phase2_b/public_aes.txt').read_text().strip()
    with (work / 'prop_export.log').open('w') as log:
        result = subprocess.run(['D:/agent/dungeons_extract/exporter/bin/Debug/net8.0/exporter.exe', 'export', 'D:/XboxGames/Minecraft Dungeons/Content/Dungeons/Content/Paks', str(export), key, '4.22', '@' + str(listing)], stdout=log, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError('道具导出失败，参见 prop_export.log')
    report = {}
    original_loader = G.load_any
    for name, path in selected.items():
        mesh = export / 'assets' / (path + '.glb')
        meta = export / 'metadata' / path / (NAMES[name] + '.meta.json')
        metadata = json.loads(meta.read_text())
        skeletal_meta = meta if metadata.get('type') == 'SkeletalMesh' else None
        source, skeleton = original_loader(mesh, skeletal_meta)
        blueprint_source = None
        component = None
        for candidate in sorted((export / 'metadata').rglob('*GEN_VARIABLE.uobject.json')):
            document = json.loads(candidate.read_text())
            props = document.get('Properties', {})
            if document.get('Type') == 'StaticMeshComponent' and props.get('StaticMesh', {}).get('ObjectName') == "StaticMesh'" + NAMES[name] + "'":
                component, blueprint_source = props, candidate
                break
        if name == 'grave_b':
            blueprint_source = export / 'metadata/Dungeons/Content/Decor/Prefabs/Gravestone/BP_Gravestone0/StaticMesh_GEN_VARIABLE.uobject.json'
            component = json.loads(blueprint_source.read_text())['Properties']
        if name in ('bell', 'cauldron'):
            component = {'RelativeRotation': {'Roll': 90}}
        if component is not None:
            transform = BP.relative(component)
            source['vertices_ue_cm'] = source['vertices_ue_cm'] @ transform[:3, :3].T + transform[:3, 3]
        points = source['vertices_ue_cm']
        grounding_cm = 0 if name == 'cage' else -float(points[:, 2].min())
        if skeletal_meta is None:
            points[:, 2] += grounding_cm
        def prepared_loader(mesh_path, meta_path):
            return source, skeleton
        G.load_any = prepared_loader
        out = HERE.parent / (name + '_dungeons_ref')
        overrides = {}
        for material in {r['material'] for r in source['primitive_ranges']}:
            albedo, emissive = G.material_textures(export, material)
            if emissive and emissive.parent != albedo.parent:
                overrides[material] = (albedo, None)
        try:
            G.convert(mesh, skeletal_meta, export, out, name=name, unit_scale=.0192, material_textures_override=overrides)
        finally:
            G.load_any = original_loader
        info = {'package': path, 'albedo_only_materials': list(overrides), 'mesh': str(mesh.relative_to(HERE.parent)), 'metadata': str(meta.relative_to(HERE.parent)), 'blueprint_component': str(blueprint_source.relative_to(HERE.parent)) if blueprint_source else None, 'unit_scale': .0192, 'display_scale': .16 / .0192, 'placement_component_transform': component, 'grounding_cm': grounding_cm, 'placement': 'original_hanging_pivot' if name == 'cage' else 'lowest_vertex_at_execution_y', 'grave_b_scale_note': '与同目录同尺寸规范的 Gravestone0 蓝图统一使用 200 倍和 Roll90' if name == 'grave_b' else None}
        (out / 'source.json').write_text(json.dumps(info, indent=2, ensure_ascii=False))
        row = json.loads((out / 'conversion.json').read_text())
        row['dimensions_blocks'] = [round(float(v) / 100, 4) for v in (points.max(axis=0) - points.min(axis=0))[[0, 2, 1]]]
        row['dimensions_axes'] = 'Java X width, Y height, Z depth'
        row['source_package'] = path
        row['grounding_cm'] = grounding_cm
        row['placement'] = info['placement']
        report[name] = row
    (HERE / 'prop_report.json').write_text(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
