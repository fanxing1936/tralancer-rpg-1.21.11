"""用户验收 v2 后追加全身淡紫微光；仅修改星空暗区 RGB，保留全部 alpha/UV/动作。"""
from __future__ import annotations

import argparse
import base64
import copy
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path

import numpy as np
from PIL import Image

from heart_of_ender_blockbench import REF

OUT = REF / 'm3_material_v3'
ACCEPTED = REF / 'm3_material_v2/heart_of_ender_material_v2.bbmodel'
ACCEPTED_SHA = '88d22edc9b13f96a0ca56a57c605894d94b64c101279bd1e69c237affdcb0f39'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text('utf8'))


def write(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', 'utf8')


def is_shell_face(element, face):
    name = element['name']
    return (name.startswith('limb_') or name.startswith('shell_body_') or
            name == 'shell_skull' and face != 'down' or
            name == 'shell_lower_jaw' and face != 'up')


def face_mask(doc, shape, shell):
    mask = np.zeros(shape, bool)
    for element in doc['elements']:
        for face, data in element['faces'].items():
            if data.get('texture') is None or is_shell_face(element, face) != shell:
                continue
            u0, v0, u1, v1 = data['uv']
            x0, y0 = np.floor([min(u0, u1), min(v0, v1)]).astype(int)
            x1, y1 = np.ceil([max(u0, u1), max(v0, v1)]).astype(int)
            mask[y0:y1, x0:x1] = True
    return mask


def build(promote=False):
    original = ACCEPTED.read_bytes()
    if sha(original) != ACCEPTED_SHA:
        raise RuntimeError('已验收 v2 源文件发生变化，停止以免覆盖新修改')
    doc = json.loads(original)
    result = copy.deepcopy(doc)
    atlas = np.array(Image.open(io.BytesIO(base64.b64decode(
        doc['textures'][0]['source'].split(',')[1]))).convert('RGBA'))
    shell = face_mask(doc, atlas.shape[:2], True)
    protected = face_mask(doc, atlas.shape[:2], False)
    if np.any(shell & protected):
        raise ValueError('外壳与眼口/小人存在共享 UV，不能原位修改')

    # Process complete source windows and their copied fade patches once, including
    # existing one-pixel duplicate gutters. Never add repeatedly for overlapping UVs.
    edit = np.zeros(atlas.shape[:2], bool)
    regions = []
    old_regions = read(REF / 'm3_material/atlas_regions.json')['regions']
    for r in old_regions:
        if r['name'].startswith('stars_'):
            regions.append({'name': r['name'], 'rect': r['atlas_rect'], 'padding': 0,
                            'origin': 'm3_material/atlas_regions.json'})
    for r in read(REF / 'm3_material_v2/atlas_regions.json')['regions']:
        if r['kind'] == 'independent_uv_alpha_profile':
            regions.append({'name': r['name'], 'rect': r['atlas_rect'], 'padding': 1,
                            'origin': 'm3_material_v2/atlas_regions.json'})
    for r in regions:
        x0, y0, x1, y1 = r['rect']
        pad = r['padding']
        edit[y0-pad:y1+pad, x0-pad:x1+pad] = True
    assert len(regions) == 60
    assert not np.any(shell & ~edit)
    assert not np.any(edit & protected)

    source_path = REF / 'MCD_Heart_of_Ender.png'
    source = np.array(Image.open(source_path).convert('RGBA'))
    sample_xy = [434, 522]
    sample = source[sample_xy[1], sample_xy[0]].copy()
    assert sample.tolist() == [12, 3, 15, 255]
    value = atlas[:, :, :3].max(axis=2).astype(float)
    # Strong stars are exact; the lift continuously reaches zero at value=24.
    # This adds no noise, rings, painted spots or geometric halo.
    weight = np.maximum(0, 1-value/24)**2
    changed = atlas.copy()
    lifted = np.floor(atlas[:, :, :3].astype(float) +
                      weight[:, :, None]*sample[:3] + .5).clip(0, 255).astype('uint8')
    changed[edit, :3] = lifted[edit]
    assert np.array_equal(changed[:, :, 3], atlas[:, :, 3])
    assert np.array_equal(changed[protected], atlas[protected])
    assert np.array_equal(changed[value >= 24], atlas[value >= 24])

    OUT.mkdir(exist_ok=True)
    atlas_path = OUT / 'atlas.png'
    Image.fromarray(changed).save(atlas_path)
    Image.fromarray((edit*255).astype('uint8')).save(OUT / 'body_region_mask.png')
    result['textures'][0]['source'] = 'data:image/png;base64,' + base64.b64encode(atlas_path.read_bytes()).decode()
    result['textures'][0]['name'] = 'heart_of_ender_material_v3.png'
    result['unhandled_root_fields']['material_status'].update({
        'version': 'M3 material v3',
        'glow': 'source-sampled faint purple shell dark-area emission; accepted eyes/mouth unchanged; no screen bloom',
        'body_glow': 'source RGB(12,3,15) at render pixel(434,522); dark-area weight=max(0,1-maxRGB/24)^2',
        'runtime': 'v2 accepted by user after user-run game test; this v3 revision awaits user visual review'})
    target = OUT / 'heart_of_ender_material_v3.bbmodel'
    write(target, result)
    delta = np.any(changed != atlas, axis=2)
    audit = {
        'accepted_baseline': str(ACCEPTED), 'accepted_baseline_sha256': ACCEPTED_SHA,
        'acceptance_evidence': '用户实测后回复：可以的，我希望全身都有淡淡的紫光发出',
        'bbmodel_sha256': sha(target.read_bytes()), 'atlas_sha256': sha(atlas_path.read_bytes()),
        'source': {'file': source_path.name, 'sha256': sha(source_path.read_bytes()),
                   'pixel_xy': sample_xy, 'rgba': sample.tolist()},
        'formula': 'RGB_out=round(RGB_in + source_RGB * max(0,1-max(RGB_in)/24)^2) only in registered shell regions; A_out=A_in',
        'inference': 'User-requested extension of one measured low-intensity body color to the whole shell; not recovered official shader parameters',
        'regions': regions, 'changed_pixels': int(delta.sum()),
        'shell_faces': sum(is_shell_face(e, f) for e in doc['elements'] for f, d in e['faces'].items() if d.get('texture') is not None),
        'checks': {'geometry_uv_unchanged': result['elements'] == doc['elements'],
                   'bones_unchanged': result['groups'] == doc['groups'] and result['outliner'] == doc['outliner'],
                   'all_7_clips_unchanged': result['animations'] == doc['animations'],
                   'all_alpha_bytes_unchanged': np.array_equal(changed[:, :, 3], atlas[:, :, 3]),
                   'eyes_teeth_mouth_inner_rgba_unchanged': np.array_equal(changed[protected], atlas[protected]),
                   'stars_at_value_24_or_more_exact': np.array_equal(changed[value >= 24], atlas[value >= 24]),
                   'no_changes_outside_registered_regions': not np.any(delta & ~edit),
                   'raw44_rgba_unchanged': np.array_equal(changed[88:132,432:476], atlas[88:132,432:476])},
        'parts': 21, 'cubes': len(doc['elements']), 'native_export_verified': False,
        'authoring': 'Python serializes accepted Blockbench document; only embedded atlas and material metadata differ',
        'limitations': ['Surface emission only; no bloom, particle halo or light cast on nearby blocks',
                        'Fullbright display and light_emission15 retained; Java directional item shading still applies',
                        'Raw44 RGBA preserved, not an independently consumed shader mask',
                        'No new real-game image captured by the assistant for this revision']}
    audit['checks'] = {k: bool(v) for k, v in audit['checks'].items()}
    if not all(audit['checks'].values()):
        raise ValueError('v3 材质差异检查失败')
    write(OUT / 'material_changes.json', audit)
    if promote:
        main = REF / 'heart_of_ender.bbmodel'
        allowed = {ACCEPTED_SHA}
        active = OUT / 'active_material.json'
        if active.exists():
            allowed.add(read(active)['bbmodel_sha256'])
        if sha(main.read_bytes()) not in allowed:
            raise RuntimeError('主模型含未登记修改，拒绝覆盖')
        main.write_bytes(target.read_bytes())
        write(active, {'bbmodel_sha256': sha(main.read_bytes()), 'variant': 'M3 material v3',
                       'source_model': 'm3_material_v3/heart_of_ender_material_v3.bbmodel',
                       'baseline': 'm3_material_v2/heart_of_ender_material_v2.bbmodel', 'runtime_verified': False})
    print(json.dumps({k: audit[k] for k in ('bbmodel_sha256', 'atlas_sha256', 'changed_pixels', 'shell_faces', 'parts', 'checks')}, ensure_ascii=False))


def sync_probe():
    """Continue the explicit independent-probe sync permission; never change the RPG pack."""
    probe = OUT / 'probe'
    generated = read(probe / 'GENERATED_FILES.json')['files']
    receipt_path = OUT / 'sync_receipt.json'
    previous = read(receipt_path if receipt_path.exists() else REF / 'm3_material_v2/sync_receipt.json')
    if previous.get('user_authorized') is not True:
        raise RuntimeError('没有独立探针同步授权记录')
    instance = Path(r'D:\minecraft\PCL启动器\.minecraft\versions\1.21.11-Fabric 0.19.3')
    roots = {'resourcepack': instance / 'resourcepacks/he_material_probe',
             'datapack': instance / 'saves/新的世界/datapacks/he_material_probe'}
    prior = {Path(x['destination']).resolve(): x['sha256'] for x in previous['files']}
    planned = {}
    for relative, checksum in generated.items():
        rel = Path(relative)
        if rel.parts[0] not in roots:
            continue
        source = probe / rel
        root = roots[rel.parts[0]].resolve()
        destination = (root / Path(*rel.parts[1:])).resolve()
        if root not in destination.parents or sha(source.read_bytes()) != checksum:
            raise RuntimeError('探针来源或目标边界检查失败')
        planned[destination] = (source.read_bytes(), checksum)
    if set(planned) != set(prior):
        raise RuntimeError('同步文件集合与已授权探针不一致')
    for destination, checksum in prior.items():
        if not destination.is_file() or sha(destination.read_bytes()) != checksum:
            raise RuntimeError(f'实例探针存在外部修改，停止覆盖：{destination}')
    changed = 0
    for destination, (data, checksum) in planned.items():
        if prior[destination] != checksum:
            destination.write_bytes(data)
            changed += 1
        if sha(destination.read_bytes()) != checksum:
            raise RuntimeError(f'同步后校验失败：{destination}')
    manifest = read(probe / 'probe_manifest.json')
    write(receipt_path, {'user_authorized': True,
                        'scope': previous['scope'],
                        'model_sha256': manifest['model_sha256'],
                        'synced_at_utc': datetime.now(timezone.utc).isoformat(),
                        'files_changed_this_sync': changed,
                        'files': [{'destination': str(p), 'sha256': v[1]} for p, v in planned.items()],
                        'game_reload_performed': False,
                        'game_reload_note': '用户自行测试；本轮未操作游戏，需用户F3+T刷新资源'})
    print(json.dumps({'files_verified': len(planned), 'files_changed': changed,
                      'receipt': str(receipt_path)}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--promote', action='store_true')
    parser.add_argument('--sync-probe', action='store_true', help='仅同步已授权独立探针；要求先生成v3 probe，校验旧收据后更新')
    args = parser.parse_args()
    if args.sync_probe:
        if args.promote:
            parser.error('--sync-probe 必须单独运行，先生成并校验候选探针')
        sync_probe()
    else:
        build(args.promote)
