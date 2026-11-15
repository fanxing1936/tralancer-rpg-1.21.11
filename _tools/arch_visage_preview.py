"""Arch-Visage 全122参考帧对照；真实模型CPU投影，非Blockbench或游戏。"""
from pathlib import Path
import argparse,json,hashlib,math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import heart_of_ender_material_preview as cpu

HERE=Path(__file__).resolve().parent;REF=HERE/'heart_of_ender_ref';OUT=HERE/'arch_visage_ref';PRE=OUT/'preview'
FONT=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',18)
KEYS=[0,2,4,5,8,12,16,17,18,20,35,50,65,76,79,80,82,86,89,91,92,121]
def sha(b):return hashlib.sha256(b).hexdigest()
def reference(i):
    a=Image.open(REF/f'frames/MCD_Arch-Visage_Spawn_Attack_in_game/frame_{i:04d}.png').convert('RGBA');b=Image.new('RGBA',a.size,(*cpu.BG,255));b.alpha_composite(a);return b.convert('RGB')
def ground(model):
    atlas=model.atlas.copy();atlas[1023,1023]=[*cpu.BG,255];faces=list(model.faces)
    lo=[-200,-200,-200];hi=[200,0,200]
    for face in cpu.FACE_NAMES:faces.append(cpu.Face(cpu.face_corners(lo,hi,face),np.array([1023,1023,1024,1024]),'research_ground/'+face))
    return cpu.Model(faces,atlas,model.resolution,model.evidence)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--keys-only',action='store_true');args=ap.parse_args();PRE.mkdir(exist_ok=True)
    cal=json.loads((OUT/'calibration.json').read_text());k=cal['pixels_per_model_unit'];basis=np.array(cal['camera_basis']);sx,sy=cal['screen_origin'];target=basis[0]*(250-sx)/k+basis[1]*(sy-250)/k
    camera={'target':target.tolist(),'viewer':basis[2].tolist(),'right':basis[0].tolist(),'up':basis[1].tolist(),'height':500/k,'size':500}
    evidence={'bbmodel_sha256':sha((OUT/'arch_visage.bbmodel').read_bytes()),'kind':'offline CPU; not Blockbench, not real Minecraft; source nearest-neighbor; constant source camera; ground is an assumed opaque volume with top modelY0','camera':camera,'renders':[],'source_frame_count':122}
    frames=KEYS if args.keys_only else range(122)
    for i in frames:
        model=ground(cpu.load_model(OUT/'arch_visage.bbmodel','spawn_attack',i/25));arr,stats=cpu.render(model,camera);im=Image.fromarray(arr);path=PRE/f'frame_{i:04d}.png';im.save(path)
        evidence['renders'].append({'file':path.name,'source_frame':i,'source_time':i/25,'model_time':i/25,'png_sha256':sha(path.read_bytes()),'stats':stats})
    # Key board: full source and candidate are always compared at identical t.
    board=Image.new('RGB',(1000,math.ceil(len(KEYS)/2)*285),(37,41,49));d=ImageDraw.Draw(board)
    for j,i in enumerate(KEYS):
        x=(j%2)*500;y=(j//2)*285;d.text((x+8,y+3),f'f{i:03d} / {i/25:.2f}s   原GIF  |  模型',font=FONT,fill='white')
        for off,im in [(0,reference(i)),(250,Image.open(PRE/f'frame_{i:04d}.png'))]:board.paste(im.resize((250,250),Image.Resampling.NEAREST),(x+off,y+30))
    board.save(OUT/'key_pose_comparison.png')
    static=cpu.load_model(OUT/'arch_visage.bbmodel','spawn_attack',.8)
    cams=cpu.shared_cameras(static,static,500)
    four=Image.new('RGB',(1000,1060),(37,41,49));d=ImageDraw.Draw(four)
    for j,(view,cam)in enumerate(cams.items()):
        arr,stats=cpu.render(ground(static),cam);im=Image.fromarray(arr);im.save(PRE/(view+'.png'));x=(j%2)*500;y=(j//2)*530;four.paste(im,(x,y+30));d.text((x+8,y+4),cpu.LABELS[view]+' / spawn_attack 0.80s',font=FONT,fill='white')
        evidence['renders'].append({'file':view+'.png','model_time':.8,'view':view,'png_sha256':sha((PRE/(view+'.png')).read_bytes()),'camera':cam,'stats':stats})
    four.save(OUT/'four_views.png')
    if not args.keys_only:
        pages=[]
        for start in range(0,122,6):
            page=Image.new('RGB',(1000,855),(37,41,49));d=ImageDraw.Draw(page)
            for j,i in enumerate(range(start,min(start+6,122))):
                x=(j%2)*500;y=(j//2)*285;d.text((x+8,y+3),f'f{i:03d}  源t={i/25:.2f}s → 模型t={i/25:.2f}s',font=FONT,fill='white')
                for off,im in [(0,reference(i)),(250,Image.open(PRE/f'frame_{i:04d}.png'))]:page.paste(im.resize((250,250),Image.Resampling.NEAREST),(x+off,y+30))
            name=f'frames_{start:03d}_{min(start+5,121):03d}.png';page.save(PRE/name);pages.append(name)
        evidence['pages']=pages
        ims=[Image.open(PRE/f'frame_{i:04d}.png').convert('RGB')for i in range(122)];ims[0].save(OUT/'spawn_attack_preview.gif',save_all=True,append_images=ims[1:],duration=40,loop=0,disposal=2)
    (OUT/'render_evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'renders':len(evidence['renders']),'keys_only':args.keys_only,'model':evidence['bbmodel_sha256']}))
if __name__=='__main__':main()
