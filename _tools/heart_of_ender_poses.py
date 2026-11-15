#!/usr/bin/env python3
"""M1 参考动作取样与关键姿态证据图；不生成模型或动画。

GIF 必须先按累计 duration 展开为 25 fps；Arch-Visage GIF 含 80 ms
及 1200 ms 合并帧，存储帧编号不能直接乘 0.04 得到时间。
"""
from pathlib import Path
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent / 'heart_of_ender_ref'
OUT = ROOT / 'analysis_poses'
FONT = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 16)
CLIPS = {
 'heart_idle':'MCD_Heart_of_Ender_Idle.gif',
 'docile':'MCD_Arch-Illager_Docile.gif',
 'anxious':'MCD_Arch-Illager_Anxious.gif',
 'fourside':'MCD_Arch-Illager_Fourside.gif',
 'visage_ingame':'MCD_Arch-Visage_Spawn_Attack_in_game.gif',
 'visage_unused':'MCD_Arch-Visage_Spawn_Attack.gif',
}
KEYS = {
 'heart_idle':[100*c+i for c in range(4) for i in (0,15,20,30,35,45,50,60,65,75,80,90,95)]+[399],
 'docile':[0,18,32,38,50,62,72,85,90,100,112,119],
 'anxious':[0,22,27,35,39,45,70,76,83,97,115,140,155,179,199],
 'fourside':[0,3,4,6,8,9,11,13,16,19,21,25,27,28,31,34,36,37,38,42,45,46,49],
 'visage_ingame':[0,2,4,5,8,12,16,17,18,20,50,76,79,80,82,86,89,91,92,121],
 'visage_unused':[0,10,20,30,40,80,90,100,110,120,149],
}
DETAIL = {
 'heart_idle':list(range(0,101,5)),
 'docile':list(range(0,120,5))+[119],
 'anxious':list(range(0,200,5))+[199],
 'fourside':list(range(50)),
 'visage_ingame':list(range(22))+list(range(76,93)),
}

def load_frames(filename):
    im = Image.open(ROOT / filename)
    frames=[]
    meta=[]
    elapsed=0
    for i in range(im.n_frames):
        im.seek(i)
        duration=im.info.get('duration',0)
        assert duration > 0 and duration % 40 == 0, (filename,i,duration)
        rgba=im.convert('RGBA').copy()
        for off in range(0,duration,40):
            frames.append(rgba)
            meta.append({'sample25':len(frames)-1,'storage_frame':i,'time_ms':elapsed+off,'storage_start_ms':elapsed,'duration_ms':duration})
        elapsed+=duration
    return frames,meta

def sheet(name,frames,meta,indices,label,side=250,columns=4):
    out=Image.new('RGB',(columns*(side+10)+10,((len(indices)+columns-1)//columns)*(side+34)+42),(31,34,42))
    d=ImageDraw.Draw(out)
    d.text((12,10),name+' / '+label+' / 25fps sample & GIF storage frame',font=FONT,fill='white')
    for j,k in enumerate(indices):
        f=frames[k]
        bg=Image.new('RGBA',f.size,(95,99,111,255))
        bg.alpha_composite(f)
        bg=bg.convert('RGB').resize((side,side),Image.Resampling.NEAREST)
        x=10+(j%columns)*(side+10);y=40+(j//columns)*(side+34)
        out.paste(bg,(x,y))
        m=meta[k]
        d.text((x,y+side+3),f"s{k:03} / g{m['storage_frame']:03} / {k/25:5.2f}s",font=FONT,fill='white')
    path=OUT / (name+'_'+label+'.png')
    out.save(path)
    return path

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    manifest={}
    for name,filename in CLIPS.items():
        frames,meta=load_frames(filename)
        manifest[name]={'source':filename,'samples25':len(frames),'sample_map':meta}
        stride=20 if name=='heart_idle' else 10 if name in ('docile','anxious','visage_unused') else 5
        indices=list(range(0,len(frames),stride))
        if indices[-1]!=len(frames)-1: indices.append(len(frames)-1)
        for pg in range(0,len(indices),24):
            sheet(name,frames,meta,indices[pg:pg+24],f'overview_{pg//24+1:02}')
        for kind,indices in [('keys',KEYS[name]),('detail',DETAIL.get(name,[]))]:
            for pg in range(0,len(indices),24):
                sheet(name,frames,meta,indices[pg:pg+24],f'{kind}_{pg//24+1:02}',300,4)
        manifest[name]['chosen_keys']=[meta[k] for k in KEYS[name]]
        if name in ('docile','anxious'):
            metrics=[]
            for i,f in enumerate(frames):
                a=np.array(f);ys,xs=np.where((a[:,:,3]>0)&(a[:,:,:3].max(2)>128))
                metrics.append({'sample25':i,'time':i/25,'bright_centroid_y':float(ys.mean()),'bright_bbox':[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())]})
            manifest[name]['screen_metrics']=metrics
        if name=='heart_idle':
            alpha=[np.array(f)[:,:,3] for f in frames]
            comparisons=[]
            for cyc in range(1,4):
                total=outside=0
                for i in range(100):
                    diff=alpha[i]!=alpha[i+100*cyc]
                    total+=int(diff.sum())
                    diff[300:500,210:360]=False
                    outside+=int(diff.sum())
                comparisons.append({'shift_frames':100*cyc,'paired_frames':100,'alpha_differing_pixels_total':total,'excluded_roi_xyxy':[210,300,360,500],'alpha_differing_pixels_outside_roi':outside})
            manifest[name]['four_second_comparison']=comparisons
    (OUT/'frame_map.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    names=['Heart_of_ender_crawling_with_decal_trail.png','Minecraft-dungeons-heart-of-ender.jpg','Heart_of_Ender_prepare_to_shoot_beams.png','Heart_Of_Ender_laser.jpg','Heart_of_Ender_start_using_ArchBeam.jpg','Heart_of_Ender_start_finish_ArchBeam.jpg','Hero_kills_Heart_of_Ender_Arch-Illager_disappear.jpg']
    tiny=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',13)
    refs=Image.new('RGB',(1300,4*390),(30,32,40));draw=ImageDraw.Draw(refs)
    for i,n in enumerate(names):
        im=Image.open(ROOT/n).convert('RGB');im.thumbnail((640,355),Image.Resampling.NEAREST)
        x=10+(i%2)*650;y=10+(i//2)*390;refs.paste(im,(x,y));draw.text((x,y+360),n,font=tiny,fill='white')
    refs.save(OUT/'inferred_references.png')

if __name__=='__main__': main()
