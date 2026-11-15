"""Render paired original GIF and native Blockbench keyframes at source times."""

import argparse
import base64
import io
from types import SimpleNamespace

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from author import HERE, REF, MODEL, BlockbenchMCP, js, read, select, sha, write
import display_mob as dm
from scale_motion import posed_matrix, read_clips

OUT = HERE / 'preview'
BG = '#222b3a'
CAMERA = (-.77, .61, -.66)
CALIBRATION = {'appear': 56}
FEATURE = dict(idle=14, walk=12, appear=7, death=112, forward_strike=36,
               fury_fist=132, launch=53, lightning_slam=64, overcharge=46, hurt=11, summon=14)
FONT = 'C:/Windows/Fonts/msyh.ttc'


def source_images(file, ids):
    result = {}
    with Image.open(file) as im:
        for idx in sorted(ids):
            im.seek(idx)
            result[idx] = im.convert('RGBA')
    return result


def capture(client, prefix, name, rows, view, matrices):
    script = '''
    Modes.options.animate.select();
    const a=Animation.all.find(a=>a.name===input.name);if(!a)throw Error('Animation missing');a.select();
    const view=input.view;
    const preview=new Preview({id:'prime_enchanter_m3_offscreen',offscreen:true,antialias:false});
    preview.setProjectionMode(true);preview.resize(view.width,view.height);preview.renderer.setPixelRatio(1);
    const target=new THREE.Vector3(...view.target);
    const pos=target.clone().addScaledVector(new THREE.Vector3(...view.direction).normalize(),500);
    preview.camOrtho.position.copy(pos);preview.controls.target.copy(target);
    preview.camOrtho.up.set(0,1,0);preview.camOrtho.lookAt(target);
    preview.camOrtho.zoom=(view.height/40)/view.world_height;
    preview.camOrtho.updateProjectionMatrix();preview.controls.update();
    const result=[];
    for(const row of input.rows){
      Timeline.setTime(row.time);Animator.preview();Canvas.scene.updateMatrixWorld(true);
      let png;Canvas.withoutGizmos(()=>{preview.render();png=preview.canvas.toDataURL('image/png');});
      const matrices=input.matrices?Object.fromEntries(Group.all.map(g=>[g.name,g.mesh.matrixWorld.toArray()])):null;
      result.push({time:row.time,png,matrices});
    }
    preview.renderer.dispose();
    return result;
    '''
    payload = dict(name='animation.' + name, rows=rows, view=view, matrices=matrices)
    return client.evaluate('(()=>{' + prefix + 'const input=' + js(payload) + ';' + script + '})()')


def decode(uri):
    return Image.open(io.BytesIO(base64.b64decode(uri.split(',', 1)[1]))).convert('RGBA')


def calibrate(client, prefix, name, ref, at):
    # Scale and framing are calibrated once against the reference pose, then
    # locked across every sample in a clip so translations remain visible.
    d = np.array(CAMERA)
    d /= np.linalg.norm(d)
    right = np.cross([0, 1, 0], d)
    right /= np.linalg.norm(right)
    up = np.cross(d, right)
    target0 = np.array([0., 18., 0.])
    trial = dict(width=500, height=500, target=target0.tolist(), direction=d.tolist(), world_height=70.)
    shot = capture(client, prefix, name, [dict(time=at)], trial, False)[0]
    actual = decode(shot['png']).getchannel('A').getbbox()
    expect = ref.getchannel('A').getbbox()
    if not actual or not expect:
        raise ValueError('Calibration pose not visible: ' + name)
    mcx, mcy = (actual[0]+actual[2])/2, (actual[1]+actual[3])/2
    scx, scy = (expect[0]+expect[2])/2, (expect[1]+expect[3])/2
    model_center = target0 + right*(mcx-250)*70/500 - up*(mcy-250)*70/500
    units_per_source_px = ((actual[3]-actual[1])*70/500) / (expect[3]-expect[1])
    target = model_center - right*(scx-ref.width/2)*units_per_source_px + up*(scy-ref.height/2)*units_per_source_px
    scale = min(1., 460/max(ref.size))
    return dict(width=round(ref.width*scale), height=round(ref.height*scale), target=target.tolist(),
                direction=d.tolist(), world_height=units_per_source_px*ref.height,
                calibration_time=at, source_bbox=list(expect))


def verify_matrices(bones, clip, sample):
    max_error = 0.
    cache = {}
    for name, flat in sample['matrices'].items():
        expected = np.array(posed_matrix(bones, name, clip, sample['time'], cache)) @ np.array(dm.translate(*bones[name]['pivot']))
        actual = np.array(flat).reshape(4, 4).T
        max_error = max(max_error, float(np.max(np.abs(expected-actual))))
    if max_error > .0002:
        raise ValueError(f'Animation transform mismatch at {sample["time"]}: {max_error}')
    return max_error


def board(name, source, rendered, keyposes, out, detail=False):
    tile_w, tile_h = 480, 294
    title = ImageFont.truetype(FONT, 21)
    small = ImageFont.truetype(FONT, 16)
    img = Image.new('RGB', (tile_w*2, 64 + len(keyposes)*tile_h), BG)
    draw = ImageDraw.Draw(img)
    draw.text((18, 11), f'{name} · 原作 GIF', font=title, fill='#fff')
    draw.text((tile_w+18, 11), 'Blockbench · 同时刻模型', font=title, fill='#fff')
    note = '局部放大，便于检查肢体' if detail else '整段相机固定，保留画面内位移'
    draw.text((tile_w+18, 38), note, font=small, fill='#bfd0e2')
    for index, row in enumerate(keyposes):
        f = row['frame']
        y0 = 64+index*tile_h
        draw.line((0, y0, tile_w*2, y0), fill='#48566a')
        for col, pic in enumerate((source[f], rendered[f])):
            if detail and (bounds := pic.getchannel('A').getbbox()):
                pic = pic.crop(bounds)
            if detail:
                factor = min((tile_w-24)/pic.width, (tile_h-72)/pic.height)
                pic = pic.resize((max(1, round(pic.width*factor)), max(1, round(pic.height*factor))),
                                 Image.Resampling.LANCZOS)
            else:
                pic = pic.copy()
                pic.thumbnail((tile_w-24, tile_h-72), Image.Resampling.LANCZOS)
            x0 = col*tile_w
            img.paste(pic, (x0+(tile_w-pic.width)//2, y0+30+(tile_h-72-pic.height)//2), pic)
            label = f'原帧 {f:03d}' if col == 0 else '模型'
            if not pic.getchannel('A').getbbox():
                label += ' · 画面内不可见'
            draw.text((x0+16, y0+4), f'{label}   {row["start_ms"]/1000:.3f} s', font=small, fill='#eef4ff')
        draw.text((16, y0+tile_h-31), row['pose'], font=small, fill='#c5d5e6')
    img.save(out, quality=91, subsampling=0)


def scale_board(name, source, rendered, rows, out):
    """Follow vertical travel with a fixed-size crop shared by both columns."""
    bounds = {}
    for row in rows:
        frame = row['frame']
        boxes = [pic.getchannel('A').getbbox() for pic in (source[frame], rendered[frame])]
        assert all(boxes)
        bounds[frame] = min(b[1] for b in boxes), max(b[3] for b in boxes)
    w, h = next(iter(rendered.values())).size
    crop_height = min(h, max(bottom-top for top,bottom in bounds.values())+16)
    factor = min(446/w, 226/crop_height)
    size = round(w*factor), round(crop_height*factor)
    board_image = Image.new('RGB', (960, 66 + len(rows)*294), BG)
    draw = ImageDraw.Draw(board_image)
    title = ImageFont.truetype(FONT, 21)
    label = ImageFont.truetype(FONT, 16)
    draw.text((18, 9), f'{name} · 原作 GIF', font=title, fill='white')
    draw.text((498, 9), 'Blockbench · 同时刻模型', font=title, fill='white')
    draw.text((18, 37), '全表使用同一显示比例，两栏在每帧用同一位置裁切', font=label, fill='#bfd0e2')
    for i, row in enumerate(rows):
        f = row['frame']
        y = 66+i*294
        low, high = bounds[f]
        top = min(h-crop_height, max(0, (low+high-crop_height)//2))
        draw.line((0,y,960,y),fill='#48566a')
        for column, original in enumerate((source[f], rendered[f])):
            pic = original.crop((0,top,w,top+crop_height)).resize(size, Image.Resampling.LANCZOS)
            board_image.paste(pic, (column*480+(480-pic.width)//2, y+33), pic)
        draw.text((18,y+5), f'f{f:03d}  ·  {row["start_ms"]/1000:.3f} s', font=label, fill='white')
        draw.text((18,y+264), row['pose'], font=label, fill='#c5d5e6')
    board_image.save(out, quality=93, subsampling=0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--clips', nargs='*')
    args = parser.parse_args()
    meta = read(HERE / 'clipmeta.json')
    assert sha(MODEL) == meta['model_sha256']
    client = BlockbenchMCP()
    prefix = select(meta['project']['uuid']) + 'if(!p)throw Error("Motion project missing");p.select();'
    ready = client.evaluate('(()=>{' + prefix + 'return Texture.all.every(t=>t.img.complete&&t.img.naturalWidth>0);})()')
    assert ready
    mob = SimpleNamespace(bbmodel=MODEL)
    bones, _, _ = dm.load_bbmodel(mob)
    animations = read_clips(read(MODEL))
    report_path = OUT / 'render_evidence.json'
    report = read(report_path) if report_path.is_file() else {}
    if report.get('model_sha256') != sha(MODEL):
        report = dict(model_sha256=sha(MODEL), engine='Blockbench native WebGL animation preview', clips={})
    for clip in meta['clips']:
        name = clip['name']
        if args.clips and name not in args.clips:
            continue
        out = OUT / name
        out.mkdir(parents=True, exist_ok=True)
        rows = clip['keyposes']
        ref_file = REF / 'originals' / clip['gif']
        assert sha(ref_file) == clip['source_sha256']
        f0 = CALIBRATION.get(name, 0)
        source = source_images(ref_file, {row['frame'] for row in rows} | {f0})
        at = next((row['start_ms']/1000 for row in rows if row['frame'] == f0), 0.)
        view = calibrate(client, prefix, name, source[f0], at)
        request = [dict(frame=row['frame'], time=row['start_ms']/1000) for row in rows]
        rendered, error = {}, 0.
        for start in range(0, len(request), 6):
            batch = request[start:start+6]
            samples = capture(client, prefix, name, batch, view, True)
            for req, sample in zip(batch, samples, strict=True):
                error = max(error, verify_matrices(bones, animations[name], sample))
                rendered[req['frame']] = decode(sample['png'])
        comparison_files = ['keyframes.jpg','details.jpg','featured.jpg','side_back.jpg']
        if clip['scale_source_frames']:
            # Put the original into the exact pixel gate used for the model before taking the common crop.
            aligned = {f: pic.resize((view['width'],view['height']),Image.Resampling.LANCZOS) for f,pic in source.items()}
            scale_frames = set(clip['scale_source_frames'])
            scale_board(name, aligned, rendered, [row for row in rows if row['frame'] in scale_frames],
                        out/'scale_comparison.jpg')
            comparison_files.append('scale_comparison.jpg')
        board(name, source, rendered, rows, out / 'keyframes.jpg')
        board(name, source, rendered, rows, out / 'details.jpg', detail=True)
        featured = next(row for row in rows if row['frame'] == FEATURE[name])
        board(name, source, rendered, [featured], out / 'featured.jpg', detail=True)
        release = featured['start_ms']/1000
        auxiliary_clip = animations[name]
        root_transform = posed_matrix(bones, 'root', auxiliary_clip, release)
        root_center = [root_transform[i][3] for i in range(3)]
        views = []
        for direction in ((-1,0,0),(0,0,1)):
            local_view = dict(view, direction=direction, target=[root_center[0],root_center[1]+15,root_center[2]],
                              width=420, height=430, world_height=52)
            views.append(decode(capture(client, prefix, name, [dict(time=release)], local_view, False)[0]['png']))
        tri = Image.new('RGB', (840, 468), BG)
        for i, (pic, label) in enumerate(zip(views, ('侧面','背面'))):
            tri.paste(pic, (i*420,38), pic)
            ImageDraw.Draw(tri).text((i*420+15, 8), f'{name}  {release:.3f} s · {label}',
                                     font=ImageFont.truetype(FONT,19), fill='white')
        tri.save(out/'side_back.jpg', quality=92)
        blank_source_frames = [f for f in rendered if source[f].getchannel('A').getbbox() is None]
        blank_model_frames = [f for f in rendered if rendered[f].getchannel('A').getbbox() is None]
        report['clips'][name] = dict(samples=len(rows), matrix_error=error, camera=view,
                                     auxiliary_view_time=release,
                                     source_blank_samples=blank_source_frames, model_blank_samples=blank_model_frames,
                                     panels={f:sha(out/f) for f in comparison_files})
        print(f'{name}: {len(rows)} sampled pairs, max matrix error {error:.3g}', flush=True)
    write(report_path, report)
    if 'idle' in report['clips']:
        capture(client, prefix, 'idle', [dict(time=0)], report['clips']['idle']['camera'], False)
    client.evaluate('(()=>{' + prefix + 'p.saved=true;return true;})()')


if __name__ == '__main__':
    main()
