"""HE 同形头替换的独立离线审阅；只写 arch_visage_ref/head_match_v1。

直接从两版 bbmodel 渲染，不重染旧 PNG。中性对照明确剥离 HE 的
shell_root/shell_head rest 旋转，仅把原始局部几何的后铰链移到原点。
"""
from __future__ import annotations
import argparse, base64, hashlib, html, io, json, math, re
from pathlib import Path
from types import SimpleNamespace
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import display_mob as dm
import heart_of_ender_material_preview as cpu
from heart_of_ender_emission import mask_records

HERE = Path(__file__).resolve().parent
AV = HERE / 'arch_visage_ref'
HE = HERE / 'heart_of_ender_ref'
OUT = AV / 'head_match_v1'
OLD = OUT / 'previous_arch_visage.bbmodel'
NEW = AV / 'arch_visage.bbmodel'
HE_MODEL = HE / 'heart_of_ender.bbmodel'
EXPECTED = 'e80846861ae9a42c964192642e0c8a8828b5e761f4752bbef0de50b735cd5da3'
KEYS = [0, 2, 4, 5, 8, 12, 16, 17, 18, 20, 35, 50, 65, 76, 79, 80, 82, 86, 89, 91, 92, 121]
QUICK = [2, 5, 12, 16, 20, 76, 92]
FONT = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 18)
SMALL = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 15)
HE_NAMES = {
    'shell_skull', 'shell_lower_jaw', 'front_eyes_surface',
    'eyes_source_wrapped_purple_halo', 'front_teeth_surface',
    'front_teeth_purple_halo_surface', 'side_teeth_surface',
    'side_teeth_purple_halo_surface', 'upper_mouth_raw44', 'lower_mouth_raw44',
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def atlas(doc):
    return base64.b64decode(doc['textures'][0]['source'].split(',')[1])


def source_path(frame):
    return HE / f'frames/MCD_Arch-Visage_Spawn_Attack_in_game/frame_{frame:04d}.png'


def reference(frame):
    image = Image.open(source_path(frame)).convert('RGBA')
    bg = Image.new('RGBA', image.size, (*cpu.BG, 255))
    bg.alpha_composite(image)
    return bg.convert('RGB')


def with_ground(model):
    # This only changes a temporary copy of the atlas used by the CPU renderer.
    pixels = model.atlas.copy()
    pixels[1023, 1023] = [*cpu.BG, 255]
    faces = list(model.faces)
    for face in cpu.FACE_NAMES:
        faces.append(cpu.Face(cpu.face_corners([-200, -200, -200], [200, 0, 200], face),
                              np.array([1023, 1023, 1024, 1024]), 'assumed_ground/' + face))
    return cpu.Model(faces, pixels, model.resolution, model.evidence)


def neutral_head(doc, source):
    """Raw cube geometry, explicitly no hierarchy rest pose or animation."""
    hinge = np.array([0, 26, 1.61051] if source else doc['unhandled_root_fields']['head_match']['common_hinge'])
    tints = {(r['element_uuid'], r['face']): tuple(r['tint_rgb']) for r in mask_records(doc)}
    faces = []
    canonical = {}
    for element in doc['elements']:
        if source and element['name'] not in HE_NAMES:
            continue
        assert not any(element.get('rotation') or [0, 0, 0])
        lo, hi = np.array(element['from']) - hinge, np.array(element['to']) - hinge
        for name, face in element['faces'].items():
            if face.get('texture') is None:
                continue
            key = element['name']
            if key == 'shell_skull_down_light':
                key = 'shell_skull'
            if key == 'shell_lower_jaw_up_light':
                key = 'shell_lower_jaw'
            key += '/' + name
            points = cpu.face_corners(lo, hi, name)
            tint = tints.get((element['uuid'], name), (255, 255, 255))
            canonical[key] = {'points': points, 'uv': np.array(face['uv']), 'tint': tint}
            faces.append(cpu.Face(points, np.array(face['uv']), key, tint))
    # Equal ordering prevents coplanar transparent surfaces from receiving a
    # different approximate CPU draw order just because a face changed owner.
    faces.sort(key=lambda f: f.name)
    png = atlas(doc)
    return cpu.Model(faces, np.asarray(Image.open(io.BytesIO(png)).convert('RGBA')),
                     np.array([doc['resolution']['width'], doc['resolution']['height']]),
                     {'kind': 'neutral raw head; rear hinge normalized to origin; no hierarchy rest/clip',
                      'removed_head_and_root_rest': bool(source)}), canonical


def reference_camera():
    calibration = read(AV / 'calibration.json')
    scale = calibration['pixels_per_model_unit']
    basis = np.array(calibration['camera_basis'])
    sx, sy = calibration['screen_origin']
    target = basis[0] * (250 - sx) / scale + basis[1] * (sy - 250) / scale
    return {'target': target.tolist(), 'viewer': basis[2].tolist(), 'right': basis[0].tolist(),
            'up': basis[1].tolist(), 'height': 500 / scale, 'size': 500}


def save_render(model, camera, path, evidence, extra):
    array, stats = cpu.render(model, camera)
    Image.fromarray(array).save(path)
    changed = np.any(array != np.array(cpu.BG), axis=2)
    record = dict(extra, file=path.relative_to(OUT).as_posix(), png_sha256=sha(path.read_bytes()),
                  camera=camera, stats=stats, pixels_different_from_background=int(changed.sum()))
    evidence['renders'].append(record)
    return array


def side_by_side(views, titles, path, title, width=500):
    board = Image.new('RGB', (width * len(views), width + 66), (37, 41, 49))
    draw = ImageDraw.Draw(board)
    draw.text((10, 4), title, font=FONT, fill='white')
    for index, (image, text) in enumerate(zip(views, titles)):
        draw.text((index * width + 10, 33), text, font=FONT, fill='white')
        board.paste(image.resize((width, width), Image.Resampling.NEAREST), (index * width, 66))
    board.save(path)


def build_checks(old, new, source, faces_he, faces_av):
    checks = {}
    checks['expected_current_sha'] = sha(NEW.read_bytes()) == EXPECTED
    checks['atlas_png_identical_HE'] = atlas(new) == atlas(source)
    checks['same_neutral_face_keys'] = faces_he.keys() == faces_av.keys()
    offsets = {'shell_skull/down': -.002, 'shell_lower_jaw/up': .002,
               'upper_mouth_raw44/down': -.004, 'lower_mouth_raw44/up': .004}
    delta = max(float(np.max(np.abs(faces_he[k]['points'] - faces_av[k]['points']))) for k in faces_he)
    corrected_delta = max(float(np.max(np.abs(faces_he[k]['points'] + np.array([0, offsets.get(k, 0), 0]) - faces_av[k]['points']))) for k in faces_he)
    checks['neutral_positions_same_except_declared_emission_offsets'] = corrected_delta < 1e-10
    checks['neutral_head_uv_same'] = all(np.array_equal(faces_he[k]['uv'], faces_av[k]['uv']) for k in faces_he)
    checks['neutral_head_tints_same'] = all(faces_he[k]['tint'] == faces_av[k]['tint'] for k in faces_he)
    src_elements = {e['name']: e for e in source['elements']}
    dst_elements = {e['name']: e for e in new['elements']}
    checks['opaque_mouth_cap_uv_from_HE_existing_stars'] = (
        dst_elements['shell_skull']['faces']['down']['uv'] == src_elements['shell_skull']['faces']['up']['uv']
        and dst_elements['shell_lower_jaw']['faces']['up']['uv'] == src_elements['shell_lower_jaw']['faces']['down']['uv'])
    changed = []
    unpermitted = []
    count = 0
    for before, after in zip(old['animations'], new['animations']):
        for aid, track in after['animators'].items():
            for ok, nk in zip(before['animators'][aid]['keyframes'], track['keyframes']):
                count += 1
                if ok != nk:
                    changed.append([after['name'], track['name'], nk['channel'], nk['time']])
                    if (track['name'], nk['channel']) not in [('head', 'position'), ('root', 'position')]:
                        unpermitted.append(changed[-1])
                if ok['time'] != nk['time'] or ok['channel'] != nk['channel']:
                    unpermitted.append(['timing/channel', nk['time']])
    checks['unchanged_rotation_timing_eye_mouth_tracks'] = not unpermitted
    checks['988_keys'] = count == 988
    config = read(AV / 'config.json')
    checks['parts5_elements12_bones6_clips3'] = len(config['parts']) == 5 and len(new['elements']) == 12 and len(new['groups']) == 6 and len(new['animations']) == 3
    mob = SimpleNamespace(bbmodel=NEW, anim_from=None)
    bones, _, _ = dm.load_bbmodel(mob)
    clip = dm.load_animations(mob)['spawn_attack']
    pivot = np.array(next(g for g in new['groups'] if g['name'] == 'head')['origin'] + [1.0])
    hinge_error = 0.
    for t in sorted(set([i / 25 for i in range(123)] + [min(i / 20, 4.88) for i in range(99)])):
        a, b = [np.array(dm.posed_matrix(bones, name, clip, t)) @ pivot for name in ('head', 'jaw')]
        hinge_error = max(hinge_error, float(np.max(np.abs(a - b))))
    checks['shared_hinge_connected_25_and20Hz'] = hinge_error < 1e-10
    return {'checks': checks, 'success': all(checks.values()), 'neutral_face_count': len(faces_he),
            'max_neutral_vertex_difference': delta, 'max_vertex_error_after_declared_offsets': corrected_delta,
            'emission_plane_y_offsets_from_HE': offsets, 'max_hinge_difference': hinge_error,
            'changed_key_count': len(changed), 'changed_keys': changed, 'unpermitted_changes': unpermitted}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--quick', action='store_true')
    parser.add_argument('--report-only', action='store_true', help='复核既有本版输出，不重复渲染')
    args = parser.parse_args()
    if args.report_only:
        evidence, checks = read(OUT / 'render_evidence.json'), read(OUT / 'review_validation.json')
        assert evidence['current_model_sha256'] == sha(NEW.read_bytes()) == EXPECTED
        finalize(evidence, checks, False)
        print(json.dumps({'success': checks['success'], 'report_only': True,
                          'artifacts': len(evidence['all_image_artifacts'])}, ensure_ascii=False))
        return
    for directory in ('preview/new', 'preview/old', 'neutral', 'boards'):
        (OUT / directory).mkdir(parents=True, exist_ok=True)
    new, old, source = read(NEW), read(OLD), read(HE_MODEL)
    he_neutral, he_faces = neutral_head(source, True)
    av_neutral, av_faces = neutral_head(new, False)
    checks = build_checks(old, new, source, he_faces, av_faces)
    assert checks['success'], checks
    evidence = {'current_model_sha256': sha(NEW.read_bytes()), 'previous_model_sha256': sha(OLD.read_bytes()),
                'HE_model_sha256': sha(HE_MODEL.read_bytes()), 'kind': 'offline CPU from actual bbmodel, not Blockbench, not Minecraft; nearest-neighbor; no bloom',
                'ground': 'temporary assumed opaque volume top modelY0, not an observed game terrain',
                'neutral_convention': 'remove HE hierarchy rest rotations and normalize both rear hinge positions to origin; all original face RGBA/UV/tints retained; not an idle frame',
                'renders': [], 'full122': not args.quick, 'boards': []}
    # Same center/scale/camera for source head and replacement head.
    cams = cpu.shared_cameras(he_neutral, av_neutral, 500)
    neutral_differences = {}
    tiles = []
    for view, camera in cams.items():
        pair = []
        for label, model in [('HE', he_neutral), ('AV', av_neutral)]:
            array = save_render(model, camera, OUT / f'neutral/{view}_{label}.png', evidence,
                                {'kind': 'neutral_local_head', 'model': label, 'view': view})
            pair.append(array)
        neutral_differences[view] = int(np.any(pair[0] != pair[1], axis=2).sum())
        path = OUT / f'neutral/{view}_comparison.png'
        side_by_side([Image.fromarray(a) for a in pair], ['HE 主模型孤立中性头', '新 AV 中性头'], path,
                     cpu.LABELS[view] + ' | 同相机同尺寸；剥离 HE 全身 rest，不是 idle')
        tiles.append(Image.open(path))
        evidence['boards'].append(path.relative_to(OUT).as_posix())
        if view == 'front':
            (OUT / 'neutral_front_comparison.png').write_bytes(path.read_bytes())
    combined = Image.new('RGB', (1000, 566 * 4), (37, 41, 49))
    for i, tile in enumerate(tiles):
        combined.paste(tile, (0, 566 * i))
    combined.save(OUT / 'neutral_four_views.png')
    checks['neutral_pixel_differences'] = neutral_differences
    # Added dark cavity caps and the small emission depth offsets may affect
    # transparency ordering in the angled view. Record that difference rather
    # than misrepresenting it as a byte-identical rendering of every view.
    checks['checks']['neutral_three_orthographic_views_pixel_identical'] = all(neutral_differences[v] == 0 for v in ('front', 'right_side', 'back'))

    camera = reference_camera()
    evidence['source_reference_camera'] = camera
    frames = QUICK if args.quick else list(range(122))
    for frame in frames:
        for label, path in [('old', OLD), ('new', NEW)]:
            model = with_ground(cpu.load_model(path, 'spawn_attack', frame / 25))
            save_render(model, camera, OUT / f'preview/{label}/frame_{frame:04d}.png', evidence,
                        {'kind': 'spawn_attack', 'model': label, 'source_frame': frame, 'source_time': frame / 25,
                         'model_time': frame / 25, 'source_png_sha256': sha(source_path(frame).read_bytes())})
        if frame in QUICK:
            path = OUT / f'boards/key_{frame:03d}.png'
            side_by_side([reference(frame), Image.open(OUT / f'preview/old/frame_{frame:04d}.png'),
                          Image.open(OUT / f'preview/new/frame_{frame:04d}.png')],
                         ['原 in_game GIF（有动图）', '旧 AV：原厚颚', '新 AV：按用户要求统一 HE 头'], path,
                         f's{frame:03d} | 源 t={frame/25:.2f}s → 模型 t={frame/25:.2f}s | 离线预览，非 BB / 非游戏')
            evidence['boards'].append(path.relative_to(OUT).as_posix())
    # Explicit front/side/back inspection of the attack pose, separate from the
    # neutral exact-geometry comparison above.
    attack = cpu.load_model(NEW, 'spawn_attack', .8)
    attack_cams = cpu.shared_cameras(attack, attack, 500)
    attack_board = Image.new('RGB', (1000, 1060), (37, 41, 49))
    d = ImageDraw.Draw(attack_board)
    for i, (view, cam) in enumerate(attack_cams.items()):
        array = save_render(with_ground(attack), cam, OUT / f'preview/attack_{view}.png', evidence,
                            {'kind': 'attack_four_views', 'model': 'new', 'view': view, 'model_time': .8})
        x, y = i % 2 * 500, i // 2 * 530
        d.text((x + 8, y + 4), f'{cpu.LABELS[view]} | spawn_attack 0.80s', font=FONT, fill='white')
        attack_board.paste(Image.fromarray(array), (x, y + 30))
    attack_board.save(OUT / 'attack_four_views.png')

    if not args.quick:
        pages = []
        for start in range(0, 122, 6):
            page = Image.new('RGB', (1500, 3 * 288), (37, 41, 49))
            d = ImageDraw.Draw(page)
            for j, frame in enumerate(range(start, min(start + 6, 122))):
                x, y = j % 2 * 750, j // 2 * 288
                d.text((x + 6, y + 3), f's{frame:03d}  {frame/25:.2f}s → {frame/25:.2f}s | 原GIF / 旧AV / 新AV', font=SMALL, fill='white')
                for k, image in enumerate([reference(frame), Image.open(OUT / f'preview/old/frame_{frame:04d}.png'),
                                           Image.open(OUT / f'preview/new/frame_{frame:04d}.png')]):
                    page.paste(image.resize((250, 250), Image.Resampling.NEAREST), (x + k * 250, y + 31))
            name = f'boards/frames_{start:03d}_{min(start+5,121):03d}.png'
            page.save(OUT / name)
            pages.append(name)
        evidence['pages'] = pages
        key_board = Image.new('RGB', (1500, len(KEYS) * 288), (37, 41, 49))
        d = ImageDraw.Draw(key_board)
        for j, frame in enumerate(KEYS):
            y = j * 288
            d.text((8, y + 3), f's{frame:03d} | 源/模型 {frame/25:.2f}s | 原GIF / 旧AV / 新AV（全列同相机）', font=FONT, fill='white')
            for k, image in enumerate([reference(frame), Image.open(OUT / f'preview/old/frame_{frame:04d}.png'),
                                       Image.open(OUT / f'preview/new/frame_{frame:04d}.png')]):
                key_board.paste(image.resize((250, 250), Image.Resampling.NEAREST), (k * 500 + 125, y + 31))
        key_board.save(OUT / 'key_pose_comparison.png')
        animation = [Image.open(OUT / f'preview/new/frame_{i:04d}.png').convert('RGB') for i in range(122)]
        animation[0].save(OUT / 'spawn_attack_preview.gif', save_all=True, append_images=animation[1:], duration=40, loop=0, disposal=2)
        blank = [0, 1] + list(range(92, 122))
        by_frame = {r['source_frame']: r for r in evidence['renders'] if r.get('kind') == 'spawn_attack' and r.get('model') == 'new'}
        checks['blank_frame_visible_pixels'] = {str(i): by_frame[i]['pixels_different_from_background'] for i in blank}
        checks['checks']['32_expected_blank_frames_hidden'] = all(v == 0 for v in checks['blank_frame_visible_pixels'].values())

    checks['checks']['source_models_unchanged_during_review'] = sha(NEW.read_bytes()) == evidence['current_model_sha256'] and sha(OLD.read_bytes()) == evidence['previous_model_sha256'] and sha(HE_MODEL.read_bytes()) == evidence['HE_model_sha256']
    checks['checks']['every_output_png_hash_verified'] = all(sha((OUT / r['file']).read_bytes()) == r['png_sha256'] for r in evidence['renders'])
    checks['success'] = all(checks['checks'].values())
    checks.update(current_model_sha256=evidence['current_model_sha256'], render_count=len(evidence['renders']),
                  full122=not args.quick, real_game_seen=False, render_method='CPU offline; not native Blockbench')
    finalize(evidence, checks, args.quick)
    print(json.dumps({'success': checks['success'], 'sha': evidence['current_model_sha256'],
                      'renders': len(evidence['renders']), 'quick': args.quick,
                      'neutral_pixel_differences': neutral_differences}, ensure_ascii=False))


def finalize(evidence, checks, quick):
    evidence_name = 'quick_render_evidence.json' if quick else 'render_evidence.json'
    checks_name = 'quick_review_validation.json' if quick else 'review_validation.json'
    native_path = HE / 'final_validation/head_match_v1/native_report.json'
    if native_path.exists():
        native_report = read(native_path)
        matched = [t for t in native_report.get('tests', [])
                   if t.get('model') == 'arch_visage' and t.get('source_sha256') == evidence['current_model_sha256']]
        if matched:
            native = matched[0]
            semantic = native['semantic_comparison']
            metadata = native['metadata_semantic_comparison']
            verified = bool(native.get('passed') and native.get('input_matches_current_authoritative_source')
                            and native.get('atlas_rgba_equal') and native.get('face_uv_texture_tint_equal')
                            and semantic.get('equal_with_native_normalization')
                            and not semantic.get('unexplained_differences')
                            and metadata.get('equal_with_native_normalization')
                            and not metadata.get('unexplained_differences'))
            checks['native_blockbench'] = {
                'verified': verified,
                'report_file': '../../heart_of_ender_ref/final_validation/head_match_v1/native_report.json',
                'report_sha256': sha(native_path.read_bytes()),
                'source_sha256': native['source_sha256'],
                'export_sha256': native['native_export_sha256'],
                'application': native['native_application'],
                'counts': native['counts'], 'keyframes_count': native['keyframes_count'],
                'atlas_rgba_equal': native['atlas_rgba_equal'],
                'face_uv_texture_tint_equal': native['face_uv_texture_tint_equal'],
                'max_geometry_animation_numeric_delta': semantic['maximum_numeric_delta'],
                'max_metadata_numeric_delta': metadata['maximum_numeric_delta'],
                'metadata_normalization_count': len(metadata['accepted_normalizations']),
                'unexplained_difference_count': 0,
                'byte_identity_claimed': False,
                'real_game_seen': False,
            }
            checks['checks']['current_model_native_Blockbench_roundtrip_verified'] = verified
    if not quick:
        images = sorted(OUT.rglob('*.png')) + [OUT / 'spawn_attack_preview.gif']
        evidence['all_image_artifacts'] = [{'file': p.relative_to(OUT).as_posix(), 'sha256': sha(p.read_bytes())} for p in images]
        checks['checks']['all_image_artifact_hashes_verified'] = all(
            sha((OUT / r['file']).read_bytes()) == r['sha256'] for r in evidence['all_image_artifacts'])
    write(OUT / evidence_name, evidence)
    write(OUT / checks_name, checks)
    write_report(evidence, checks, quick)
    references = re.findall(r'(?:href|src)="([^"#]+)"', (OUT / 'index.html').read_text(encoding='utf-8'))
    missing = [p for p in references if '://' not in p and not (OUT / p).exists()]
    checks['missing_html_links'] = missing
    checks['checks']['all_html_local_links_exist'] = not missing
    checks['success'] = all(checks['checks'].values())
    write(OUT / checks_name, checks)
    write_report(evidence, checks, quick)


def write_report(evidence, checks, quick):
    state = '关键姿态首轮，完整122帧尚未生成' if quick else '完整122时点已重新渲染；21页逐帧三列对照'
    native = checks.get('native_blockbench', {})
    native_note = '当前本报告未获得本版原生 Blockbench 或真实客户端视觉证据；相关后续验证由总报告分别记录。'
    native_link = ''
    if native.get('verified'):
        native_link = f' · <a href="{native["report_file"]}">本版 Blockbench 原生验证</a>'
        native_note = (f'本版已通过 [Blockbench 5.2.2 原生打开/另存验证]({native["report_file"]})，来源 SHA 与当前 e808 版本一致；'
                       f'12 元素、6 骨骼、3 动作、988 关键帧保留，图集 RGBA 与面的 UV/texture/tint 完整。'
                       f'几何与动作最大数值差 `{native["max_geometry_animation_numeric_delta"]:.9g}`；'
                       f'metadata 的 {native["metadata_normalization_count"]} 处坐标最大差 `{native["max_metadata_numeric_delta"]:.9g}`，均为原生另存数值正规化，0 项未解释差异。'
                       '不宣称另存文件逐字节相同，原主模型未被覆盖。**本版仍未在真实 Minecraft 客户端看过**；原生格式往返通过不等于游戏视觉通过。')
    links = '\n'.join(f'<li><a href="{html.escape(p)}">{html.escape(p)}</a></li>' for p in evidence.get('pages', []))
    body = f'''<!doctype html><html lang="zh"><meta charset="utf-8"><title>Arch-Visage 统一 HE 头部</title>
<style>body{{max-width:1400px;margin:30px auto;padding:0 20px;background:#20242c;color:#e9ecf0;font:17px/1.6 system-ui}}a{{color:#bcb0ff}}img{{max-width:100%;height:auto}}code{{overflow-wrap:anywhere}}section{{margin:36px 0}}</style>
<h1>末影面容：统一为末影之心头部</h1><p>{state}。所有图直接读取当前 bbmodel；离线 CPU、无 bloom，不是 Blockbench 或真实游戏截图。</p>
<p>当前 SHA：<code>{evidence['current_model_sha256']}</code></p>
<p><a href="HEAD_MATCH_REPORT.md">变更与局限</a> · <a href="{'quick_review_validation.json' if quick else 'review_validation.json'}">独立检查</a> · <a href="{'quick_render_evidence.json' if quick else 'render_evidence.json'}">图像证据与相机</a>{native_link}</p>
<section><h2>同相机中性头四视</h2><p>两侧均去掉层级 rest 姿态并以闭口后铰链归一；不是 HE idle 抽帧。外壳、眼牙比例与UV相同；嘴腔另有暗面遮挡和微小亮面深度偏移。<a href="neutral_front_comparison.png">紧凑正面对照</a></p><a href="neutral_four_views.png"><img src="neutral_four_views.png"></a></section>
<section><h2>动作重点：原GIF / 旧AV / 新AV</h2>'''
    for frame in [2, 5, 12, 16, 20, 76, 92]:
        body += f'<p><a href="boards/key_{frame:03d}.png"><img src="boards/key_{frame:03d}.png"></a></p>'
    body += '<section><h2>张口正、侧、背及四分之三</h2><img src="attack_four_views.png"></section>'
    if not quick:
        body += f'<section><h2>全122帧</h2><p><a href="spawn_attack_preview.gif">25fps 连续离线预览</a> · <a href="key_pose_comparison.png">22个关键时点总板</a></p><ul>{links}</ul></section>'
    body += '<p>用户指定统一形状，因此新薄颚不再按原AV厚颚轮廓拟合；旧M4轮廓分数不适用于本版。假想地面仅用于显示出地/沉地遮挡。</p></html>'
    (OUT / 'index.html').write_text(body, encoding='utf-8')
    notes = f'''# Arch-Visage 统一 Heart of Ender 头部

已按用户要求，把末影面容改为末影之心主模型的头、薄下颚、眼牙与发光材质。头部原始尺寸和 UV 原样复用，不拉伸；保留末影面容出地、张口、沉地的动作时序。本版属于用户指定的统一造型，旧 M4 对原 Arch-Visage 厚颚的轮廓分数不再适用。

- [打开图像审阅入口](index.html)：{state}。
- [同相机四视对照](neutral_four_views.png)、[紧凑正面对照](neutral_front_comparison.png)：HE 孤立中性头与新 AV 中性头。剥离 HE 的全身及头部 rest 旋转，将两者后铰链归到同一原点；不是比较 HE 的 idle 与 AV 的闭口姿态。
- [张口四视](attack_four_views.png)；关键图：[005 闭口](boards/key_005.png)、[012](boards/key_012.png)、[016](boards/key_016.png)、[020 张口](boards/key_020.png)。每张均为原 GIF、旧 AV、新 AV 三列。
- [独立检查]({'quick_review_validation.json' if quick else 'review_validation.json'})、[渲染证据]({'quick_render_evidence.json' if quick else 'render_evidence.json'})、[生成器验证](validation.json)、[几何来源](geometry_transfer.json)、[高度调整逐帧值](placement_adjustments.json)。

当前模型 SHA-256：`{evidence['current_model_sha256']}`。旧 AV：`{evidence['previous_model_sha256']}`；HE 来源：`{evidence['HE_model_sha256']}`。

## 几何、动作与材质

HE 头的 10 个元素统一平移 `(0, -17.8060535329898, +4.988303283718423)`，不施加 HE 全身或头部的 rest 倾斜；再将原 skull.down 与 jaw.up 两面拆成独立亮面，共 **12 元素、6 骨骼、5 个 item_display 部件**。上头与下颚共享后铰链 `(0, 8.193946467010202, 6.598813283718423)`。原上头独立 position 归零，以防薄颚张口后铰链断开。

为保留 AV 张口前的暗嘴时段，壳体 down 和下颚 up 保留不透明星空遮挡面，分别复用 HE 头顶和下颚底部原 UV；否则亮面移入壳内后仍会从开口透出。嘴腔亮面沿各自外法线偏移 0.002 单位，原 raw44 层在源位置基础上再向外偏移 0.004 单位，避免共面。没有新增纹理像素或增加显示部件。

保持 **3 clips、988 关键帧**，所有旋转、时间点、眼白核心显隐和嘴腔显隐轨道逐值保持。改变的是上头 position，以及 root 的 Y 高度：出地早期按旧上沿渐变到下沿，主体按下沿，沉地末期从下沿渐变到上沿。不能将薄颚整段固定下移，否则张口阶段的下口面会埋入地面。`spawn_attack` 源长 4.88 秒，20 Hz 运行时量化为 4.90 秒；idle/walk 仍是地下静止兼容占位，不称原作动作。

星空、眼牙、环绕紫光、上下嘴腔及 44×44 遮罩全部来自当前 HE 主模型，同一内嵌 PNG 字节完全相同。环绕紫光归上头持续显示；白色眼核心沿用 AV 原短暂显隐。上嘴腔保持 down 面（-Y 法线），下嘴腔保持 up 面（+Y 法线），未翻转 UV 或对调上下亮面。原 44×44 RGBA 保留，嘴内两层实际取其亮区 `[0,2,33,44)`，使用源截图取色 `[255,211,255]` 的 constant tint；全亮显示不等于屏幕后期 bloom，也不会照亮周围方块。

持续显示的 HE 环绕紫光本身含明亮紫色双眼印记，因此出地早期和后半段即使白色 core 已隐藏，仍可能先后看见紫色眼形。这是本轮统一 HE 头部的明确选择，与原 AV 动图部分时段没有清晰眼形不同。012/016 张口前不再提前出现大片亮嘴；020 上下口内面仍朝外发亮，背面保持星空黑壳。

## 本轮验证边界

中性对照对应 HE 的 {checks['neutral_face_count']} 个源面，另有上述两张暗口遮挡面。对应源面 UV 与 tint 一致，扣除登记的亮面偏移后，几何最大数值差 `{checks['max_vertex_error_after_declared_offsets']:.3g}`；未扣除偏移的最大差为 `{checks['max_neutral_vertex_difference']:.3g}` 单位。四视输出差异像素 `{checks['neutral_pixel_differences']}`：正、侧、背为 0，四分之三视角的少量像素差来自暗口遮挡面与亮面深度偏移，不宣称四视全部逐像素相同。共享后铰链在 25 Hz 和 20 Hz 采样的最大位置差 `{checks['max_hinge_difference']:.3g}`。当前独立检查：`{sum(checks['checks'].values())}/{len(checks['checks'])}` 通过。

全部图直接读取新版与旧版 bbmodel，以最近邻取样重新渲染，没有重染旧 PNG。CPU 模拟采用全亮、普通 alpha 混合、alpha≥0.1 与简化深度排序；不能证明游戏内透明排序或光晕观感。出地与沉地用顶面 Y=0 的假想不透明地块体积遮挡，未验证真实地形。旧版截图、旧版 Blockbench 原生另存与旧实机观察，均不能作为本版验证。

{native_note}

图中可见新头更紧凑、下颚更薄，眼牙位置与原 AV 渲染存在有意改变；不再声称逐像素复刻原动图。原视频没有提供完整隐藏三维形态，继承的独立俯仰与根旋转仍含三维推断。没有加入光束、弹体、粒子、玩法或新 AI。素材版权属于 Mojang，本项目非商业且与 Mojang 无关联；原始来源与归档校验见 [SOURCES](../SOURCES.md) 及 HE 来源报告。

复现：`python _tools/arch_visage_head_match_review.py`。此脚本只写本 revision 目录，不改任何模型或生成器。
'''
    if not quick:
        notes += '\n[全关键姿态总板](key_pose_comparison.png) · [连续离线预览](spawn_attack_preview.gif)。32 个预期空白时点均检查地面上是否残留可见像素，详细结果在独立检查 JSON。\n'
    (OUT / 'HEAD_MATCH_REPORT.md').write_text(notes, encoding='utf-8')


if __name__ == '__main__':
    main()
