#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""只读眼眉采样：原图正面校正、坐标统计；不写模型或主生成脚本。"""
import json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from scipy import ndimage

OUT=Path(__file__).resolve().parent
REF=OUT.parents[1]
W,H=1200,700
SCALE=100
FONT=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',19)
SMALL=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',14)
QUADS={
    'main':{'file':'MCD_Arch-Illager.png','quad':[[95,296],[360,427],[334,625],[68,494]],'exactness':'角点人工标记约1–2px误差；主渲染无JPEG压缩'},
    'throne':{'file':'Arch-Illager_sit_in_his_throne_room_front_view.jpg','quad':[[827,427],[1052,427],[1049,571],[830,568]],'exactness':'截图角点约2–3px误差，JPEG及游戏光照；仅作第二表情候选'},
}

def homography(dst,src):
    a=[];b=[]
    for (x,y),(u,v) in zip(dst,src):
        a.extend([[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]])
        b.extend([u,v])
    return np.r_[np.linalg.solve(np.asarray(a,float),np.asarray(b,float)),1].reshape(3,3)

def normalized_image(path,quad):
    src=np.array(Image.open(path).convert('RGB'))
    m=homography([[0,0],[W,0],[W,H],[0,H]],quad)
    yy,xx=np.mgrid[:H,:W];p=np.stack([xx+.5,yy+.5,np.ones((H,W))],-1)@m.T
    p=p[:,:,:2]/p[:,:,2:];xy=np.rint(p).astype(int)
    return src[xy[:,:,1],xy[:,:,0]],m

def bounds(mask):
    y,x=np.where(mask)
    if not len(x):return None
    # 原始画面左=角色右(+X)；Y以头顶19.5为上界。
    return {'rectified_pixel_bbox':[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)],
            'local_model_bbox_xyxy':[round(6-(x.max()+1)/SCALE,3),round(19.5-(y.max()+1)/SCALE,3),round(6-x.min()/SCALE,3),round(19.5-y.min()/SCALE,3)],
            'pixel_count':len(x)}

def clean_component(mask):
    # 去掉原渲染的1px边沿亮线/锯齿；保留最大实心连通片。
    opened=ndimage.binary_opening(mask,structure=np.ones((7,7),bool))
    labels,n=ndimage.label(opened)
    if not n:return opened
    counts=np.bincount(labels.ravel());counts[0]=0
    return labels==int(counts.argmax())

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    result={'method':'将头前面四角映到12×7模型单位；每单位100采样像素；颜色阈值仅统计原图片，不创建新眼材质。','references':{}}
    panels=[]
    yy,xx=np.mgrid[:H,:W];depth=yy/SCALE
    for name,cfg in QUADS.items():
        a,m=normalized_image(REF/cfg['file'],cfg['quad'])
        mean=a.astype(float).mean(2);spread=a.max(2).astype(int)-a.min(2).astype(int)
        if name=='main':
            brow=(mean>=49)&(mean<=62)&(spread<5)
            black=(mean>=20)&(mean<=44)&(spread<5)
            white=(a.min(2)>=235)&(spread<8)
        else:
            brow=(mean>=45)&(mean<=100)&(spread<22)
            black=brow
            white=(a.min(2)>=205)&(spread<24)
        records={}
        for side,region in [('right',xx<W/2-105),('left',xx>W/2+105)]:
            parts={
                'brow_vertical':brow&region&(depth>.4)&(depth<2.85),
                'brow_horizontal':brow&region&(depth>=2.85)&(depth<4.1),
                'pupil':black&region&(depth>=4)&(depth<5.25),
                'white':white&region&(depth>=3.8)&(depth<5.3),
            }
            records[side]={k:{'raw_bounds':bounds(mask),'largest_opened_component':bounds(clean_component(mask))}
                           for k,mask in parts.items()}
        result['references'][name]={**cfg,'transform_rectified_to_source':m.tolist(),'measurements':records}
        pic=Image.fromarray(a).resize((840,490),Image.Resampling.NEAREST)
        d=ImageDraw.Draw(pic)
        for x in range(13):
            px=x*70;d.line((px,0,px,489),fill=(205,120,80),width=1)
            if x<12:d.text((px+2,2),str(6-x),font=SMALL,fill='white',stroke_width=1,stroke_fill='black')
        for y in range(8):d.line((0,y*70,839,y*70),fill=(205,120,80),width=1)
        panels.append((name,pic))
        Image.fromarray(a).save(OUT/(name+'_head_rectified.png'))
    result['source_pixel_colors']={
        'brow_vertical':{'rect':[4,2,6,4],'rgba':[57,57,57,255]},
        'brow_horizontal':{'rect':[2,4,6,5],'rgba':[57,57,57,255]},
        'pupil_black':{'rect':[3,5,5,6],'rgba':[37,37,37,255]},
        'eye_white':{'rect':[5,5,6,6],'rgba':[255,255,255,255]},
    }
    result['current_geometry']={'brow_vertical_positive_x':[3.8,16.5,5.7,18.5],
                                'brow_horizontal_positive_x':[1.9,15.5,5.7,16.5],
                                'eye_positive_x':[2.85,14.5,5.7,15.5],
                                'issue':'眉外缘约多出0.7，眼外缘约多出1.7；眼白与眉外缘齐平，参考眼外缘应内收约1模型单位。'}
    result['recommendations']={
        'A_main_expression':{'label':'主渲染表情（先修定位，保留黑黑白比例）',
            'positive_x_brow_vertical':[3,16.5,5,18.5],
            'positive_x_brow_horizontal':[1,15.5,5,16.5],
            'positive_x_eye':[1,14.5,4,15.5],
            'positive_x_white':[3,14.5,4,15.5],
            'positive_x_black':[1,14.5,3,15.5],
            'uv_white':[5,5,6,6],'uv_black':[3,5,5,6],
            'note':'与主渲染的1白/2黑一致，但眼外端比眉外端内缩1。负X眼镜像。也可保留整3×1UV条，只修改geometry坐标。'},
        'B_throne_expression':{'label':'王座正面表情（独立候选，不称主渲染同姿势）',
            'positive_x_white':[1,14.5,4,15.5],
            'positive_x_pupil':[1.1,15.05,2.3,15.5],
            'uv_white':[5,5,6,6],'uv_pupil':[3,5,4,6],
            'note':'白底整3×1，短瞳约1.2×0.45从眉底内侧侵入；具体瞳X需按截图采样误差保留约±0.2。不得把同UV条横向拉伸冒充此表情。'},
    }
    (OUT/'eye_analysis.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    sheet=Image.new('RGB',(1720,700),'#202630');d=ImageDraw.Draw(sheet)
    for i,(name,pic) in enumerate(panels):
        x=20+i*850;sheet.paste(pic,(x,80));d.text((x,20),'主渲染：头前面校正' if name=='main' else '王座：另一眼神表情，头前面校正',font=FONT,fill='white')
    d.text((20,600),'网格每格=1模型单位；x从角色右+6向左-6；头顶Y=19.5。主图眼外缘约|X|=4，眉外缘约|X|=5。',font=FONT,fill='white')
    d.text((20,635),'当前模型眼外缘|X|=5.7，与眉外缘齐平，是主要定位错误；王座眼白比例另作为表情候选。',font=FONT,fill='#ffce88')
    sheet.save(OUT/'eye_reference_coordinates.png')
    print(json.dumps(result['references'],ensure_ascii=False))

if __name__=='__main__':main()
