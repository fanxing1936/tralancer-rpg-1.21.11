"""Reopen the saved Blockbench file, verify it, and render the four review views."""

import base64
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from make_static import BlockbenchMCP, HERE, MODEL, NAME, project_selector, write_json

PREVIEW = HERE / 'preview'
CHECK_NAME = 'prime_enchanter_m2_disk_check'
CAMERAS = {
    'front': (0, 0, -1),
    'side': (-1, 0, 0),
    'back': (0, 0, 1),
    'three_quarter': (-.77, .61, -.66),
}


def model_data(doc):
    return {key: doc.get(key) for key in ('resolution', 'elements', 'outliner', 'animations')} | {
        'groups': [{k: row[k] for k in ('name', 'uuid', 'origin', 'rotation')}
                   for row in doc['groups']],
        'texture': doc['textures'][0]['source'],
    }


def native_images():
    spec = json.loads((HERE / 'model_spec.json').read_text(encoding='utf-8'))
    original = json.loads(MODEL.read_text(encoding='utf-8'))
    model_hash = hashlib.sha256(MODEL.read_bytes()).hexdigest()
    assert model_hash == spec['model_sha256']
    client = BlockbenchMCP()
    client.tool('create_project', {'name': CHECK_NAME, 'format': 'bedrock'})
    reopen = '''
    if(Project.name!==checkName)throw Error('M2 check project mismatch');
    const disk=JSON.parse(require('fs').readFileSync(modelPath,'utf8'));
    Codecs.project.parse(disk);
    Project.name=checkName;
    return {uuid:Project.uuid,version:Blockbench.version,format:Format.id};
    '''
    inputs = 'const checkName=' + json.dumps(CHECK_NAME) + ',modelPath=' + json.dumps(str(MODEL)) + ';'
    info = client.evaluate('(()=>{' + inputs + reopen + '})()')
    prefix = project_selector(info['uuid']).replace(json.dumps(NAME), json.dumps(CHECK_NAME))
    render = '''
    if(!Texture.all.every(t=>t.img.complete&&t.img.naturalWidth>0))throw Error('Texture not decoded');
    const preview=new Preview({id:'prime_enchanter_m2_offscreen',offscreen:true,antialias:false});
    preview.setProjectionMode(true);preview.resize(620,740);preview.renderer.setPixelRatio(1);
    Canvas.scene.updateMatrixWorld(true);
    const bounds=new THREE.Box3();Cube.all.forEach(c=>bounds.expandByObject(c.mesh));
    const center=bounds.getCenter(new THREE.Vector3());
    const views={};
    function capture(name,dir){
      const target=center.clone();
      const pos=target.clone().addScaledVector(new THREE.Vector3(...dir).normalize(),100);
      preview.camOrtho.position.copy(pos);preview.controls.target.copy(target);
      preview.camOrtho.up.set(0,1,0);preview.camOrtho.lookAt(target);
      preview.camOrtho.zoom=(740/40)/43;preview.camOrtho.updateProjectionMatrix();preview.controls.update();
      Canvas.withoutGizmos(()=>{preview.render();views[name]=preview.canvas.toDataURL('image/png');});
    }
    for(const [name,dir] of Object.entries(cameras))capture(name,dir);
    const neutralBones=new Set(['body','head','right_arm','left_arm','right_hand','left_hand','right_leg','left_leg']);
    const rest=Group.all.filter(bone=>neutralBones.has(bone.name)).map(bone=>[bone,bone.rotation.slice()]);
    try {
      for(const [bone] of rest)bone.rotation.splice(0,3,0,0,0);
      Canvas.updateAll();Canvas.scene.updateMatrixWorld(true);
      capture('neutral_detail',[-.26,.09,-1]);
    } finally {
      for(const [bone,angle] of rest)bone.rotation.splice(0,3,...angle);
      Canvas.updateAll();Canvas.scene.updateMatrixWorld(true);
    }
    preview.renderer.dispose();
    return {doc:Codecs.project.compile({raw:true}),views,bounds:[bounds.min.toArray(),bounds.max.toArray()]};
    '''
    result = client.evaluate('(()=>{' + prefix + 'const cameras=' + json.dumps(CAMERAS) + ';' + render + '})()')
    assert model_data(original) == model_data(result['doc']), 'Blockbench disk roundtrip changed model data'
    for name, uri in result['views'].items():
        (PREVIEW / (name + '.png')).write_bytes(base64.b64decode(uri.split(',', 1)[1]))
    write_json(PREVIEW / 'render_evidence.json', dict(
        model_sha256=model_hash, source='disk reopen via Blockbench native project codec',
        model_roundtrip=True, original_png_embedded=True, native=info,
        cameras=CAMERAS, viewport=[620, 740], bounds=result['bounds'],
        detail_pose='native render with temporary neutral arm, torso and leg rotations, restored before compile',
        detail_sha256=hashlib.sha256((PREVIEW / 'neutral_detail.png').read_bytes()).hexdigest(),
        image_sha256={name: hashlib.sha256((PREVIEW / (name + '.png')).read_bytes()).hexdigest()
                      for name in CAMERAS}))
    author_id = json.dumps(spec['blockbench']['uuid'])
    author_name = json.dumps(NAME)
    client.evaluate('(async()=>{' + prefix + 'p.saved=true;await p.close();'
                    f'const author=ModelProject.all.find(q=>q.uuid==={author_id}&&q.name==={author_name});'
                    'if(author)author.select();return true;})()')


def compose():
    width, height = 1120, 660
    bg = '#202631'
    main = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 26)
    small = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 17)
    views = [
        ('front', '正面', 'neutral_front.png', '原作角色的近正面渲染，双臂垂下', '核对眉眼、长鼻、青核和胸袍纹样'),
        ('side', '左侧', 'side_rear.png', '实机 15.50 秒，侧偏背的迈步姿态', '核对侧帽片、拳腕体积和披风离背距离'),
        ('back', '背面', 'rear.png', '实机 15.00 秒，转身甩起披风', '核对帽后三带、背片和披风的双片结构'),
        ('three_quarter', '四分之三', 'guard_3q.png', 'Wiki 原作渲染，抬拳姿态', '核对两拳高低、帽袍轮廓与相对比例'),
    ]
    board = Image.new('RGB', (width, height * 4), bg)
    grid = Image.new('RGB', (width, height * 2), bg)

    def place(pane, file, column):
        with Image.open(file) as src:
            src = src.convert('RGBA')
        box = src.getchannel('A').getbbox()
        src = src.crop(box) if box else src
        scale = min((width // 2 - 52) / src.width, (height - 130) / src.height)
        src = src.resize((round(src.width * scale), round(src.height * scale)), Image.Resampling.LANCZOS)
        x = column * (width // 2) + (width // 2 - src.width) // 2
        y = 63 + (height - 127 - src.height) // 2
        pane.paste(src, (x, y), src)

    for i, (name, label, ref, source, focus) in enumerate(views):
        pane = Image.new('RGB', (width, height), bg)
        draw = ImageDraw.Draw(pane)
        draw.rectangle((0, 0, width, 57), fill='#181d27')
        draw.line((width // 2, 0, width // 2, height), fill='#495268')
        draw.text((24, 10), '参考 · ' + label, font=main, fill='white')
        draw.text((width // 2 + 24, 10), 'Blockbench · ' + label, font=main, fill='white')
        place(pane, HERE / 'reference' / ref, 0)
        place(pane, PREVIEW / (name + '.png'), 1)
        draw.text((24, height - 46), source, font=small, fill='#d0deee')
        draw.text((width // 2 + 24, height - 46), focus, font=small, fill='#d0deee')
        pane.save(PREVIEW / (name + '_comparison.jpg'), quality=95, subsampling=0)
        board.paste(pane, (0, i * height))
        grid.paste(pane.crop((width // 2, 0, width, height)), (i % 2 * width // 2, i // 2 * height))
    board.save(PREVIEW / 'four_views_comparison.jpg', quality=95, subsampling=0)
    grid.save(PREVIEW / 'four_views_model.jpg', quality=95, subsampling=0)

    detail = Image.new('RGB', (width, 1000), bg)
    draw = ImageDraw.Draw(detail)
    for col, (label, file) in enumerate([
        ('参考 · 垂臂', HERE / 'reference/neutral_front.png'),
        ('Blockbench · 垂臂检查姿态', PREVIEW / 'neutral_detail.png'),
    ]):
        with Image.open(file) as src:
            src = src.convert('RGBA')
        src = src.crop(src.getchannel('A').getbbox())
        x0 = col * (width // 2)
        draw.text((x0 + 24, 18), label, font=main, fill='white')
        for row, (lo, hi, note) in enumerate([
            (.00, .51, '红领上沿与青肩罩外缘'),
            (.58, 1.00, '袍摆外张与白色下缘'),
        ]):
            tile = src.crop((0, round(src.height * lo), src.width, round(src.height * hi)))
            scale = min(480 / tile.width, 378 / tile.height)
            tile = tile.resize((round(tile.width * scale), round(tile.height * scale)), Image.Resampling.LANCZOS)
            y0 = 55 + row * 466
            detail.paste(tile, (x0 + (width // 2 - tile.width) // 2, y0 + (394 - tile.height) // 2), tile)
            draw.text((x0 + 24, y0 + 405), note, font=small, fill='#d0deee')
    draw.line((width // 2, 0, width // 2, 1000), fill='#495268')
    detail.save(PREVIEW / 'collar_shoulder_skirt_comparison.jpg', quality=95, subsampling=0)


if __name__ == '__main__':
    PREVIEW.mkdir(exist_ok=True)
    native_images()
    compose()
