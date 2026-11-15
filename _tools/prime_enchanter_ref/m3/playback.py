"""Render a synchronized visual loop for review, using the original GIF frame delays."""

import argparse
import json

from PIL import Image, ImageDraw, ImageFont, features

from author import HERE, MODEL, MOTION, REF, BlockbenchMCP, read, select, sha, write
from preview import BG, FONT, OUT, capture, decode

LABEL_FONT = ImageFont.truetype(FONT, 15)


def paired_frame(source, model, idx, time):
    # The two inputs share the same film gate; preserve that framing and match dimensions.
    assert source.size == model.size
    width = max(200, model.width+18)
    result = Image.new('RGB', (width*2, model.height+42), BG)
    draw = ImageDraw.Draw(result)
    draw.text((9, 7), f'原作 GIF · f{idx:03d}', fill='white', font=LABEL_FONT)
    draw.text((width+9, 7), 'Blockbench', fill='white', font=LABEL_FONT)
    draw.text((9, model.height+22), f'{time:.3f} s', fill='#c5d5e6', font=LABEL_FONT)
    draw.line((width, 0, width, result.height), fill='#48566a')
    for i, pic in enumerate((source, model)):
        result.paste(pic, (i*width+(width-pic.width)//2, 24), pic)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--clips', nargs='*')
    args = parser.parse_args()
    assert features.check('webp')
    meta = read(HERE/'clipmeta.json')
    render = read(OUT/'render_evidence.json')
    assert meta['model_sha256'] == render['model_sha256'] == sha(MODEL)
    timing = read(MOTION/'gif_timing.json')['clips']
    client = BlockbenchMCP()
    prefix = select(meta['project']['uuid'])+'if(!p)throw Error("Motion project missing");p.select();'
    path = OUT/'playback_evidence.json'
    evidence = read(path) if path.is_file() else {}
    if evidence.get('model_sha256') != sha(MODEL):
        evidence = dict(model_sha256=sha(MODEL), clips={})
    for c in meta['clips']:
        name = c['name']
        if args.clips and name not in args.clips:
            continue
        frames = timing[c['source']]['frames']
        view = render['clips'][name]['camera']
        request = [dict(time=min(row['start_ms']/1000,c['length'])) for row in frames]
        durations = [row['delay_ms'] for row in frames]
        output = []
        source_blank, model_blank = [], []
        with Image.open(REF/'originals'/c['gif']) as gif:
            for offset in range(0, len(frames), 8):
                batch = capture(client, prefix, name, request[offset:offset+8], view, False)
                for i, item in enumerate(batch, offset):
                    gif.seek(i)
                    model = decode(item['png'])
                    source = gif.convert('RGBA').resize(model.size, Image.Resampling.LANCZOS)
                    if not source.getchannel('A').getbbox():
                        source_blank.append(i)
                    if not model.getchannel('A').getbbox():
                        model_blank.append(i)
                    output.append(paired_frame(source, model, i, frames[i]['start_ms']/1000))
        movie = OUT/name/'playback.webp'
        output[0].save(movie, append_images=output[1:], save_all=True, duration=durations, loop=0,
                       quality=86, method=4)
        with Image.open(movie) as check:
            assert check.n_frames == len(frames)
            decoded_durations = []
            for i in range(check.n_frames):
                check.seek(i)
                check.load()
                decoded_durations.append(check.info['duration'])
            assert decoded_durations == durations
        evidence['clips'][name] = dict(sha256=sha(movie), source_frames=len(frames), duration_ms=sum(durations),
                                       source_blank_frames=source_blank, model_blank_frames=model_blank, camera=view)
        evidence['clips'] = {c['name']: evidence['clips'][c['name']] for c in meta['clips'] if c['name'] in evidence['clips']}
        write(path, evidence)
        print(json.dumps(dict(clip=name, frames=len(frames), bytes=movie.stat().st_size)), flush=True)


if __name__ == '__main__':
    main()
