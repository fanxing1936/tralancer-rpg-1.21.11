"""只读原作导出，制作城镇英雄六套外观。"""
import copy
import json
import sys
from pathlib import Path
import numpy as np
from PIL import Image
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import dungeons_models as M
G, B = (M.G, M.BP)
ROOT = Path(__file__).resolve().parent
EXPORT = ROOT / '_work' / 'hero_export'
HERO = M.UP / 'jacques'
SKIN_ASSETS = M.UP / 'chartex' / 'assets'
SKINS = SKIN_ASSETS / 'Dungeons/Content/Actors/Characters/Player/Master/Skins'
MESH = 'Dungeons/Content/Actors/Characters/Player/Master/SK_Player_Master'
GLB = HERO / 'assets' / (MESH + '.glb')
META = HERO / 'metadata' / MESH / 'SK_Player_Master.meta.json'
SPECS = {
    'town_priest': ('SoulRobe', 'T_SpiritRobe', 'priest', 'Pake'),
    'town_bard': ('BardsGarb_Unique1', 'T_BardsGarb_Unique1', None, 'Baako'),
    'town_watchman': ('ReinforcedMail', 'T_ReinforcedMail', None, 'Darian'),
    'town_witch': ('BardsGarb', 'T_BardsGarb', 'witch', 'Hedwig'),
    'town_edgewalker': ('EvocationRobe', 'T_EvocationRobe', 'edge', 'Shikoba'),
    'town_inquisitor': ('DarkArmor', 'T_DarkArmor', 'inq', 'Warrior'),
}

def recolor(src, dst, style):
    a = np.array(Image.open(src).convert('RGBA'))
    rgb = a[:, :, :3].astype(float)
    lum = rgb @ np.array([0.2126, 0.7152, 0.0722]) / 255
    if style == 'priest':
        trim = np.all(rgb == [36, 36, 45], axis=2)
        highlight = np.all(rgb == [70, 73, 105], axis=2)
        accents = trim | highlight
        base = np.array([255, 255, 245])
        dark = np.array([155, 151, 135])
        gold = np.array([255, 216, 90])
        light = np.array([255, 242, 168])
    elif style == 'witch':
        accents = (rgb.max(2) - rgb.min(2) > 40) & (rgb[:, :, 0] > rgb[:, :, 2] * 1.15)
        dark = np.array([50, 20, 65])
        base = np.array([91, 44, 111])
        gold = np.array([180, 138, 216])
        light = gold
    elif style == 'edge':
        accents = rgb.max(2) - rgb.min(2) > 45
        dark = np.array([53, 37, 66])
        base = np.array([162, 118, 190])
        gold = base
        light = np.array([206, 177, 225])
    else:
        accents = (rgb[:, :, 0] >= 100) & (a[:, :, 3] > 0)
        dark = np.array([15, 12, 15])
        base = np.array([42, 36, 40])
        gold = np.array([212, 175, 55])
        light = np.array([246, 224, 153])
    visible = a[:, :, 3] > 0
    for mask, low, high in ((~accents, dark, base), (accents, gold, light)):
        mask = mask & visible
        values = lum[mask]
        if values.size:
            shade = (values - values.min()) / max(float(np.ptp(values)), 1e-6)
            a[:, :, :3][mask] = np.rint(low + (high - low) * shade[:, None]).astype('uint8')
    Image.fromarray(a).save(dst)
    return {'method': 'source RGB palette and luminance mapping; alpha and pixel coordinates unchanged', 'source': str(src), 'style': style}

def trim_priest_talk(document, clip_report):
    """取 idle 的前 1.5 秒，并在截点保留每个通道的插值姿势。"""
    endpoint = 1.5
    animation = next(a for a in document['animations'] if a['name'] == 'animation.talk')
    for animator in animation['animators'].values():
        channels = sorted({frame['channel'] for frame in animator['keyframes']})
        trimmed = []
        for channel in channels:
            frames = sorted((f for f in animator['keyframes'] if f['channel'] == channel), key=lambda f: f['time'])
            left = max((f for f in frames if f['time'] <= endpoint), key=lambda f: f['time'])
            right = min((f for f in frames if f['time'] >= endpoint), key=lambda f: f['time'], default=left)
            end_frame = copy.deepcopy(left)
            end_frame['uuid'] = G.uid('town_priest/talk/' + animator['name'] + '/' + channel + '/end')
            end_frame['time'] = endpoint
            end_frame['interpolation'] = 'linear'
            fraction = (endpoint - left['time']) / (right['time'] - left['time']) if right['time'] > left['time'] else 0.0
            end_frame['data_points'] = [{axis: str(float(left['data_points'][0][axis]) + fraction * (float(right['data_points'][0][axis]) - float(left['data_points'][0][axis]))) for axis in ('x', 'y', 'z')}]
            trimmed.extend(copy.deepcopy(f) for f in frames if f['time'] < endpoint)
            trimmed.append(end_frame)
        animator['keyframes'] = trimmed
    animation['length'] = endpoint
    clip = next(c for c in clip_report if c['clip'] == 'talk')
    clip.update(seconds=endpoint, ticks=30, source_interval_seconds=[0.0, endpoint], fallback='取 idle 的前 1.5 秒')
    clip['notifies'] = [n for n in clip['notifies'] if n[0] <= endpoint]

for key, (armor, tex, style, skin_name) in SPECS.items():
    if len(sys.argv) > 1 and key not in sys.argv[1:]:
        continue
    out = HERE / (key + '_dungeons_ref')
    out.mkdir(exist_ok=True)
    bp = next((EXPORT / 'metadata').rglob('BP_' + armor))
    sockets = B.sockets([HERO / 'metadata'])
    atts = []
    for var, (scs, p) in B._components(bp).items():
        if not p.get('StaticMesh'):
            continue
        if key == 'town_witch' and 'Helmet' in var:
            continue
        if key == 'town_edgewalker' and 'Helmet' in var:
            continue
        attach = scs['AttachToName']
        bone, socket = sockets.get(attach, (attach, np.eye(4)))
        rel = B._object_path(p['StaticMesh'])
        mat = socket @ B.relative(p)
        atts.append({'name': 'armor_' + var.lower(), 'mesh': EXPORT / 'assets' / (rel + '.glb'), 'bone': bone, 'matrix': mat, 'material': 'TOWN_ARMOR', 'component': var, 'attach': attach})
    if key == 'town_edgewalker':
        hood_bp = next((EXPORT / 'metadata').rglob('BP_SoulRobe'))
        hood_scs, hood_props = B._components(hood_bp)['Helmet_FurArmor']
        hood_attach = hood_scs['AttachToName']
        hood_bone, hood_socket = sockets[hood_attach]
        hood_rel = B._object_path(hood_props['StaticMesh'])
        atts.append({'name': 'armor_soul_hood', 'mesh': EXPORT / 'assets' / (hood_rel + '.glb'), 'bone': hood_bone, 'matrix': hood_socket @ B.relative(hood_props), 'material': 'TOWN_HOOD', 'component': 'Helmet_FurArmor', 'attach': hood_attach})
    texture = next((EXPORT / 'assets').rglob(tex + '.png'))
    recolor_info = None
    if style:
        original = texture
        texture = out / 'armor_recolored.png'
        recolor_info = recolor(original, texture, style)
    skin_texture = SKINS / skin_name / f'T_{skin_name}_Skin.png'
    override = {'MI_Valorie': (skin_texture, None), 'TOWN_ARMOR': (texture, None)}
    if key == 'town_edgewalker':
        hood_texture = out / 'hood_recolored.png'
        recolor(next((EXPORT / 'assets').rglob('T_SpiritRobe.png')), hood_texture, 'edge')
        override['TOWN_HOOD'] = (hood_texture, None)
    doc, report = G.convert(GLB, META, HERO, out, name=key, unit_scale=M.UNIT, attachments=atts, material_textures_override=override)
    clips = [('Player_Master_Idle_Glaive', 'idle', True)]
    if key == 'town_inquisitor':
        clips += [('Player_Master_Walk_Glaive', 'walk', True), ('Player_Master_GlaiveUnique1Combo_Attack1', 'attack', False)]
    if key == 'town_priest':
        clips += [('Player_Master_Idle_Glaive', 'talk', False)]
    doc, clip_report = G.author(doc, META, GLB, [HERO / 'metadata'], clips)
    if key == 'town_priest':
        trim_priest_talk(doc, clip_report)
    if key != 'town_inquisitor':
        orientation_id = G.uid(key + '/source_orientation')
        doc['groups'].append({'name': 'town_source_orientation', 'uuid': orientation_id, 'origin': [0.0, 0.0, 0.0], 'rotation': [0.0, 180.0, 0.0], 'export': True, 'visibility': True, 'isOpen': True})
        doc['outliner'] = [{'uuid': orientation_id, 'children': doc['outliner']}]
    (out / (key + '.bbmodel')).write_text(json.dumps(doc, ensure_ascii=False, indent=1) + '\n', encoding='utf8')
    h = M.source_height_cm('jacques', MESH)
    cfg = {'model_scale': 1.87 * 16 / (h * M.UNIT), 'height_blocks': 1.87, 'source_height_cm': h, 'turn': 0 if key == 'town_inquisitor' else 180, 'merge': {}, 'held_bone': 'J_R_Weapon' if key == 'town_watchman' else None, 'attachments': [{k: str(v) if isinstance(v, Path) else v for k, v in a.items() if k != 'matrix'} for a in atts], 'source': {'mesh': MESH, 'export_root': str(HERO), 'armor_blueprint': str(bp)}, 'clips': clip_report, 'conversion': report, 'recolor': recolor_info, 'source_orientation': '+Z friendly root normalization' if key != 'town_inquisitor' else '-Z hostile native'}
    (out / 'model_config.json').write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + '\n', encoding='utf8')
    sources = [
        '# 原作资产',
        f'身体使用 `SK_Player_Master` / `{skin_texture.name}`，覆盖 `MI_Valorie` 的贴图。'
        f'原包路径为 `{skin_texture.relative_to(SKIN_ASSETS).with_suffix(".uasset").as_posix()}`。',
        f'盔甲使用 `{armor}` 与原作骨架插槽、蓝图组件变换。',
        f'盔甲贴图为 `{tex}`。' + ('仅映射颜色，保留原像素网格及透明度。' if style else '采用原贴图。'),
    ]
    if key == 'town_priest':
        sources.append('`talk` 使用原作 idle 的前 1.5 秒。')
    if key == 'town_edgewalker':
        sources.append('头部采用原作 Soul Robe 的 `Helmet_SpiritRobe` 兜帽，保留原 UV 和插槽，配色改紫。')
    (out / 'SOURCES.md').write_text('\n\n'.join(sources) + '\n', encoding='utf-8')
    print(key, report['display_parts'], report['elements'], [(c['clip'], c['seconds']) for c in clip_report], flush=True)

