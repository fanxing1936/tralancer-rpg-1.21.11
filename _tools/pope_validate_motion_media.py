"""教皇 M3 审阅媒体全解码与本地审阅页链接检查；不是资源包/游戏测试。"""
import hashlib,json,re,subprocess
from pathlib import Path
from PIL import Image
import imageio_ffmpeg

REF=Path(__file__).resolve().parent/'pope_ref';M3=REF/'m3'

def main():
    meta=json.loads((M3/'clipmeta.json').read_text(encoding='utf-8'));rows=[]
    sha=hashlib.sha256((REF/'pope.bbmodel').read_bytes()).hexdigest()
    for evidence in ('render_evidence.json','movie_evidence.json'):
        data=json.loads((M3/'preview'/evidence).read_text(encoding='utf-8'))
        assert data['bbmodel_sha256']==sha and len(data['clips'])==9
    for clip in meta['clips']:
        name=clip['name'];folder=M3/'preview'/name
        gif=folder/(name+'_comparison.gif');mp4=folder/(name+'_comparison.mp4')
        with Image.open(gif) as im:
            duration=0;frames=im.n_frames;size=list(im.size)
            for i in range(frames):im.seek(i);duration+=im.info.get('duration',0)
        run=subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-nostdin','-hide_banner','-v','error','-i',str(mp4),
                            '-progress','pipe:1','-f','null','-'],capture_output=True,text=True,timeout=45)
        assert run.returncode==0 and not run.stderr,(name,run.stderr)
        expected=round(clip['length']*20)+1
        decoded=[int(line.split('=')[1]) for line in run.stdout.splitlines() if line.startswith('frame=')][-1]
        assert decoded==expected and duration==expected*50,(name,decoded,duration)
        rows.append(dict(clip=name,gif_frames=frames,review_duration_ms=duration,mp4_decoded_frames=decoded,
                         size=size,full_decode_ok=True,mp4_bytes=mp4.stat().st_size))
    checked=[]
    for link in re.findall(r'(?:src|href|poster)="([^"]+)"',(M3/'index.html').read_text(encoding='utf-8')):
        if link.startswith(('#','https:')):continue
        assert (M3/link).is_file(),link
        checked.append(link)
    report={'source_model_sha256':sha,'note':'审阅视频保留clip末帧50ms，媒体总长比clip多50ms；无声，不是游戏录像。',
            'clips':rows,'review_page_local_links_checked':checked,'ok':True}
    (M3/'validation/media_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'clips':len(rows),'decoded_frames':sum(r['mp4_decoded_frames'] for r in rows),'links':len(checked),'ok':True}))

if __name__=='__main__':main()
