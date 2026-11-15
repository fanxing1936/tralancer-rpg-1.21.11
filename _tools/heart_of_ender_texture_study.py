#!/usr/bin/env python3
"""M1 source-only texture diagnostics, not a model atlas or generated art."""
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

REF = Path(__file__).resolve().parent / 'heart_of_ender_ref'
OUT = REF / 'analysis_texture'
FONT = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 19)
SMALL = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 15)


def composite(im, size=None):
    im = im.convert('RGBA')
    if size:
        im = im.resize(size, Image.Resampling.NEAREST)
    bg = Image.new('RGBA', im.size, '#373b43')
    bg.alpha_composite(im)
    return bg.convert('RGB')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    names = ['MCD_Decal_Puddle_(texture).png', 'MCD_Heart_of_Ender_(glow_effect_texture).png',
             'T_ArchIllagerUndressed.png', 'T_ArchIllagerUndressed_S.png',
             'MCD_Arch-Illager_(texture).png', 'MCD_Arch-Illager_(shadow_texture).png']
    result = {'note':'Original pixels preserved. Preview enlargement uses nearest neighbour; gray is a preview background only.', 'images':{}}
    for name in names:
        im = Image.open(REF/name).convert('RGBA')
        a = np.array(im)
        colors,counts=np.unique(a.reshape(-1,4),axis=0,return_counts=True)
        top=np.argsort(counts)[::-1][:12]
        result['images'][name]={'size':list(im.size),'opaque_pixels':int((a[:,:,3]==255).sum()),
            'partial_alpha_pixels':int(((a[:,:,3]>0)&(a[:,:,3]<255)).sum()),
            'transparent_pixels':int((a[:,:,3]==0).sum()),'unique_rgba':len(colors),
            'alpha_values':np.unique(a[:,:,3]).tolist(),
            'top_rgba':[{'rgba':colors[i].tolist(),'count':int(counts[i])} for i in top]}
    und=np.array(Image.open(REF/names[2]).convert('RGBA'))
    regular=np.array(Image.open(REF/names[4]).convert('RGBA'))
    diff=np.any(und!=regular,axis=2)
    ys,xs=np.where(diff)
    result['undressed_vs_regular']={'different_pixels':int(diff.sum()),
        'diff_bbox_xyxy_exclusive':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],
        'different_pixel_coordinates_xy':np.stack([xs,ys],axis=1).tolist()}
    sheet=Image.new('RGB',(1360,850),'#20242c'); d=ImageDraw.Draw(sheet)
    d.text((20,15),'M1 原始贴图核对｜最近邻放大，灰底仅用于显示透明像素',font=FONT,fill='white')
    for i,name in enumerate(names[1:]):
        col=i%3;row=i//3;x=20+col*445;y=70+row*385
        im=Image.open(REF/name).convert('RGBA'); n=5 if im.width==64 else 7
        thumb=composite(im,(im.width*n,im.height*n));sheet.paste(thumb,(x,y+45))
        d.text((x,y),name,font=SMALL,fill='white')
        rec=result['images'][name]
        d.text((x,y+23),f"{im.width}×{im.height} | RGBA种类 {rec['unique_rgba']}",font=SMALL,fill='#b4c9df')
    sheet.save(OUT/'texture_maps_nearest.png')

    # Source-only candidate windows. The atlas mapping will be decided in M2.
    windows={'A_head_candidate':[24,24,152,152],'B_body_candidate':[260,32,388,160],
             'C_limb_candidate':[472,112,600,240],'D_limb_candidate':[72,440,200,568],
             'E_limb_candidate':[290,346,418,474],'F_limb_candidate':[498,478,626,606]}
    star=Image.open(REF/names[0]).convert('RGBA')
    sheet=Image.new('RGB',(1600,960),'#20242c');d=ImageDraw.Draw(sheet)
    d.text((20,15),'星空原图与候选裁窗｜原图 711×711，裁窗均128×128，右侧最近邻×2',font=FONT,fill='white')
    sheet.paste(composite(star),(20,85))
    palette=['#ffcf62','#68d0e8','#ec89d0','#82e39b','#c0a1ff','#ff927d']
    for i,(label,box) in enumerate(windows.items()):
        color=palette[i]
        d.rectangle((20+box[0],85+box[1],20+box[2]-1,85+box[3]-1),outline=color,width=2)
        d.text((22+box[0],87+box[1]),label[0],font=FONT,fill=color)
        x=770+(i%3)*274;y=85+(i//3)*365
        crop=star.crop(box)
        sheet.paste(composite(crop,(256,256)),(x,y+52))
        d.text((x,y),f'{label[0]}  {box}',font=SMALL,fill=color)
        arr=np.array(crop)
        count=int((np.max(arr[:,:,:3],axis=2)>0).sum())
        d.text((x,y+26),f'非黑像素 {count}/16384',font=SMALL,fill='#d1d8e1')
        transparent=int((arr[:,:,3]==0).sum())
        assert transparent==0, 'Candidate window must not include source transparent stripes'
        result.setdefault('star_windows',{})[label]={'source_rect_xyxy_exclusive':box,'nonblack_rgb_pixels':count,'transparent_pixels':transparent,'sample_method':'crop only; nearest x2 for preview, not atlas'}
    a=np.array(star)
    ys,xs=np.where(a[:,:,3]==0)
    result['star_alpha_zero_location']={'bbox_xyxy_exclusive':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],
        'interior_pixels':int(((xs>0)&(xs<star.width-1)&(ys>0)&(ys<star.height-1)).sum()),
        'note':'Transparent runs occur inside the image near y330..338 and y648..654, not only at the outer edge.'}
    d.text((20,825),'候选区域只是来源登记，不是最终UV；M2按头宽与星点尺寸决定纹素密度。',font=FONT,fill='white')
    d.text((20,865),'保留原图颜色；紫色发光/色调不能从文件名或RGB通道自行推断。',font=FONT,fill='white')
    sheet.save(OUT/'star_windows.png')

    crops=[('HE_left_eye','MCD_Heart_of_Ender.png',[248,292,301,334]),
           ('HE_right_eye','MCD_Heart_of_Ender.png',[322,321,372,364]),
           ('HE_teeth','MCD_Heart_of_Ender.png',[272,350,442,420]),
           ('AV_mouth','MCD_Arch-Visage.png',[116,311,505,635])]
    sheet=Image.new('RGB',(1450,850),'#20242c');d=ImageDraw.Draw(sheet)
    d.text((20,15),'发光形状来源裁片｜原像素最近邻，无补画、无调色；含透视和辉光，尚未制成贴图',font=FONT,fill='white')
    for i,(label,name,box) in enumerate(crops):
        src=Image.open(REF/name).convert('RGBA');crop=src.crop(box)
        crop.save(OUT/(label+'_source_crop.png'))
        x=20+(i%2)*710;y=70+(i//2)*370
        factor=min(680//crop.width,300//crop.height)
        factor=max(1,factor)
        sheet.paste(composite(crop,(crop.width*factor,crop.height*factor)),(x,y+60))
        d.text((x,y),f'{label} | {name}',font=SMALL,fill='white')
        d.text((x,y+25),f'原图 [x0,y0,x1,y1)={box}，预览×{factor}',font=SMALL,fill='#b4c9df')
        result.setdefault('glow_crop_sources',{})[label]={'file':name,'source_rect_xyxy_exclusive':box,'preview_integer_scale':factor}
    sheet.save(OUT/'glow_source_crops.png')
    for name in ['MCD_Heart_of_Ender.png','MCD_Arch-Visage.png']:
        composite(Image.open(REF/name)).save(OUT/(Path(name).stem+'_gray_background.png'))
    source=Image.open(REF/'MCD_Heart_of_Ender.png').convert('RGBA')
    points=[(362,121),(408,156),(296,224),(336,233),(465,273),(429,273),(388,300),
            (279,314),(343,342),(300,369)]
    result['render_exact_pixel_samples']={'file':'MCD_Heart_of_Ender.png',
        'method':'exact integer coordinate read; no averaging or recolouring',
        'samples':[{'xy':list(p),'rgba':list(source.getpixel(p))} for p in points]}
    (OUT/'TEXTURE_DATA.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'out':str(OUT),'undressed_diff':result['undressed_vs_regular']['different_pixels'],'glow':result['images'][names[1]]},ensure_ascii=False))


if __name__=='__main__':
    main()
