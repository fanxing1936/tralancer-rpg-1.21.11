#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""穷举原贴图U区间，拟合权杖三可见面；输出只在本目录。"""
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT=Path(__file__).resolve().parent
REF=OUT.parents[1]
FONT=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',18)
SMALL=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',14)
N=72
T=np.linspace(.025,.975,N)
SS,TT=np.meshgrid(T,T)
FACE_QUADS={
    'leftthin':[[0,174],[106,20],[200,0],[95,155]],
    'big':[[95,155],[200,0],[342,127],[236,280]],
    'bottom':[[0,174],[95,155],[236,280],[143,301]],
}

def read(p):return np.asarray(Image.open(p).convert('RGBA'))
def rectify(image,quad):
    q=np.asarray(quad,float)
    p=(1-SS)[...,None]*(1-TT)[...,None]*q[0]+SS[...,None]*(1-TT)[...,None]*q[1]+SS[...,None]*TT[...,None]*q[2]+(1-SS)[...,None]*TT[...,None]*q[3]
    xy=np.rint(p).astype(int)
    return image[xy[:,:,1],xy[:,:,0],:3].astype(float)

def source_patch(source,u0,u1,axis,flip_u,flip_v):
    au=SS if axis=='s' else TT
    av=TT if axis=='s' else SS
    if flip_u:au=1-au
    if flip_v:av=1-av
    x=np.minimum(31,np.maximum(0,np.floor(u0+au*(u1-u0)).astype(int)))
    y=np.minimum(31,np.maximum(0,np.floor(av*32).astype(int)))
    return source[y,x,:3].astype(float)

def score(src,tar):
    scale=float(np.sum(src*tar)/np.sum(src*src))
    err=src*scale-tar
    return scale,float(np.sqrt(np.mean(err*err))),float(np.mean(np.abs(err))),float(np.median(np.abs(err)))

def main():
    reference=read(REF/'MCD_Arch-Illagers_Staff.png')
    source=read(REF/'T_SuperCube.png')
    fit={'method':'全部528个整数U区间 × 2轴 × 2种U方向 × 2种V方向；V固定0..32整高；逐面单一中性系数s=dot(S,T)/dot(S,S)，无RGB各通道调色、无offset。',
         'sample_grid':{'size':[N,N],'normalized_range':[.025,.975], 'mapping':'四边形双线性坐标；参考最近邻；source floor UV像素'},
         'source_sha256':hashlib.sha256((REF/'T_SuperCube.png').read_bytes()).hexdigest(),
         'reference_sha256':hashlib.sha256((REF/'MCD_Arch-Illagers_Staff.png').read_bytes()).hexdigest(),
         'official_uv_recovered':False,'faces':{}}
    actual={}; best_imgs={};full_imgs={}
    for name,quad in FACE_QUADS.items():
        tar=rectify(reference,quad);actual[name]=tar
        top=[];full=None
        for u0 in range(32):
            for u1 in range(u0+1,33):
                for axis in ('s','t'):
                    for fu in (False,True):
                        for fv in (False,True):
                            src=source_patch(source,u0,u1,axis,fu,fv)
                            scale,rmse,mae,median=score(src,tar)
                            rec={'source_rect':[u0,0,u1,32], 'source_u_increases_with':axis,
                                 'flip_u':fu,'flip_v':fv,'neutral_shading_scale':scale,
                                 'rmse_rgb_0_255':rmse,'mae_rgb_0_255':mae,'median_abs_error':median}
                            if len(top)<8 or rmse<top[-1]['rmse_rgb_0_255']:
                                top.append(rec);top.sort(key=lambda r:r['rmse_rgb_0_255']);top=top[:8]
                            if u0==0 and u1==32 and (full is None or rmse<full['rmse_rgb_0_255']):full=rec
        best=top[0]
        # 三条色带中心的样本，独立列出便于手算比例，非筛选拟合输入。
        centers=[]
        for v in (.1,.5,.9):
            s,t=(.5,v) if best['source_u_increases_with']=='t' else (v,.5)
            q=np.asarray(quad,float);p=(1-s)*(1-t)*q[0]+s*(1-t)*q[1]+s*t*q[2]+(1-s)*t*q[3]
            x,y=np.rint(p).astype(int)
            centers.append({'normalized_st':[s,t],'reference_xy':[int(x),int(y)],'reference_rgb':reference[y,x,:3].tolist()})
        fit['faces'][name]={'reference_quad_tl_tr_br_bl':quad,'best':best,'top8':top,'full_texture_best':full,'band_center_samples':centers}
        for rec,table in [(best,best_imgs),(full,full_imgs)]:
            src=source_patch(source,rec['source_rect'][0],rec['source_rect'][2],rec['source_u_increases_with'],rec['flip_u'],rec['flip_v'])
            table[name]=(src,np.clip(np.rint(src*rec['neutral_shading_scale']),0,255).astype('uint8'))
    fit['limits']=[
        '三面只恢复被采样的颜色列与方向；不是原作完整mesh UV文件。',
        '贴图垂直方向仅1级左右RGB变化，多种V范围/翻向可给近似同色；固定全高避免挑特定行，V无法唯一确定。',
        '四边形点人工按像素角点标注，约1px误差；边界处采样残差可高于色带内部。',
        '中性shading仅用于比对，不写入候选贴图。最终材质保留原RGB/alpha，由Blockbench/游戏自己受光。',
        'Java north/east/up等面名随staff_glow rest旋转而变；报告用原图四边形锚点定义big/leftthin/bottom。',
        '不可见三面可采用对应可见面的原裁片复用，必须标工作补全而不是原作已证实。',
    ]
    (OUT/'cube_fit.json').write_text(json.dumps(fit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    sheet=Image.new('RGB',(1550,1080),'#202630');d=ImageDraw.Draw(sheet)
    d.text((20,15),'T_SuperCube 数值拟合：原RGBA裁片 + 每面一个中性受光系数',font=FONT,fill='white')
    titles=['原渲染面展开','原RGBA裁片（未调色）','同一裁片 × 拟合中性系数','整32×32 × 最佳中性系数']
    for j,title in enumerate(titles):d.text((220+j*320,65),title,font=SMALL,fill='#ffda8b')
    for i,name in enumerate(('leftthin','big','bottom')):
        y=110+i*295; rec=fit['faces'][name];b=rec['best'];fb=rec['full_texture_best']
        d.text((15,y+10),name,font=FONT,fill='white');d.text((15,y+45),str(b['source_rect']),font=SMALL,fill='#9cdbff')
        d.text((15,y+75),'s = %.5f'%b['neutral_shading_scale'],font=SMALL,fill='white')
        d.text((15,y+105),'RMSE = %.3f'%b['rmse_rgb_0_255'],font=SMALL,fill='#9ee9b6')
        ims=[actual[name],best_imgs[name][0],best_imgs[name][1],full_imgs[name][1]]
        for j,a in enumerate(ims):
            pic=Image.fromarray(np.clip(a,0,255).astype('uint8')).resize((250,250),Image.Resampling.NEAREST)
            sheet.paste(pic,(220+j*320,y))
        d.text((1180,y+258),'整图RMSE %.3f'%fb['rmse_rgb_0_255'],font=SMALL,fill='#ffabab')
    d.text((20,1010),'全部528个U区间穷举；V固定全高，未挑单色行。误差单位：RGB 0–255。不是官方UV恢复。',font=FONT,fill='white')
    sheet.save(OUT/'cube_numeric_fit.png')
    sourcepic=Image.fromarray(source).resize((640,640),Image.Resampling.NEAREST)
    board=Image.new('RGB',(1170,760),'#202630');d=ImageDraw.Draw(board)
    board.paste(sourcepic.convert('RGB'),(500,70))
    for rect,col,label in [([7,0,10,32],'#79d7ff','leftthin U=7..10'),([10,0,13,32],'#ffdc6c','big / bottom U=10..13')]:
        x0,y0,x1,y1=rect;d.rectangle((500+x0*20,70,500+x1*20-1,709),outline=col,width=4)
        d.text((500,18 if x0==7 else 40),label,font=FONT,fill=col)
    refcrop=Image.fromarray(reference).crop((0,0,342,310));bg=Image.new('RGBA',refcrop.size,'#37414c');bg.alpha_composite(refcrop)
    board.paste(bg.resize((444,403),Image.Resampling.NEAREST).convert('RGB'),(20,80))
    d.text((20,510),'leftthin：从外侧向big共边变亮',font=FONT,fill='#79d7ff')
    d.text((20,545),'big：从leftthin共边向右下外边变亮',font=FONT,fill='#ffdc6c')
    d.text((20,580),'bottom：从左下外边向右上共边变亮',font=FONT,fill='#ffdc6c')
    d.text((20,665),'UV候选只采原图对应三列；原图完整保留。',font=SMALL,fill='white')
    board.save(OUT/'cube_source_rectangles.png')
    rows=['| 可见面 | 原像素矩形 | source U沿参考(s,t) | flip U/V | 中性系数 | RGB RMSE | 全图最佳RMSE |', '|---|---|---|---|---|---|---|']
    for name,rec in fit['faces'].items():
        b=rec['best'];rows.append('| %s | `%s` | %s | %s / %s | %.6f | %.4f | %.4f |'%(name,b['source_rect'],b['source_u_increases_with'],b['flip_u'],b['flip_v'],b['neutral_shading_scale'],b['rmse_rgb_0_255'],rec['full_texture_best']['rmse_rgb_0_255']))
    doc='''# T_SuperCube：三列UV裁片的数值拟合

本研究只使用公开原始 `T_SuperCube.png` 与无发光 `MCD_Arch-Illagers_Staff.png`。候选材质不改一个RGB/alpha；拟合中性系数只显示在研究对照中，不烘入材质。

方法：为原渲染三个可见面标四边形，每面取72×72内部点（归一化0.025–0.975）。枚举全部528个整数U区间，V固定整高0–32，再穷举源U沿参考s/t、U反向、V反向，共4224候选/面。每个候选只拟合一个标量 `s=Σ(source·target)/Σ(source²)`，不允许RGB通道独立系数或offset。按三通道RMSE排名。

'''+ '\n'.join(rows)+'''

## 可直接采用的来源范围

- `leftthin = [7,0,10,32]`，原图三列7、8、9。
- `big = [10,0,13,32]`，三列10、11、12。
- `bottom = [10,0,13,32]`，同三列10、11、12。

这不是目测取“差不多的黄色”。例如big三个带中心为 `(199,191,52)`、`(199,199,68)`、`(199,199,75)`，对应源列10–12约 `(255,245,66)`、`(255,255,87/88)`、`(255,255,96)` 乘同一个约0.78系数。底面约乘2/3，侧窄面约0.89。整图0–32再怎么转向或乘中性系数也保留橙红区域，因此误差明显更大。

## 方向（不用未经验证的Java面名）

原图像素锚点：A=(0,174)、B=(106,20)、C=(200,0)、D=(342,127)、E=(236,280)、F=(143,301)、G=(95,155)。

- leftthin四边形A→B→C→G。源U从外边A–B向共边G–C增加，即橙黄到浅黄；源V沿A→B另一方向全高。
- big四边形G→C→D→E。源U从共边G–C向外边E–D增加，即浅黄到亮黄；源V沿G→C全高。
- bottom四边形A→G→E→F。源U从外边A–F向共边G–E增加；源V沿A→F全高。

`cube_fit.json` 保存每个最佳候选的轴与flip（最佳V flip由极小1级色差产生，不应当成已恢复原作者朝向）。V近乎常色，原作具体V范围/翻向无法唯一识别；这里固定整高避免任挑某一行制造匹配。以上面名是画面几何标签；主模型应按自己的 `staff_glow` rest旋转把梯度放到相应屏幕方向，不能猜Java north/east。隐藏三面若按对面复用，要标为补全候选。

## 边界与证据

四边形角点约1像素误差、色带交界取样和源图垂直微变会留下小残差；这不是官方mesh或完整UV恢复。原渲染的中性受光系数也不是游戏内发光参数。原图属于Mojang；本项目非商业，与Mojang无关联。

- [三个面与整图基线对照](cube_numeric_fit.png)
- [原图采样范围](cube_source_rectangles.png)
- [机器可读全部最佳结果](cube_fit.json)

复现：在仓库根运行 `python _tools/pope_ref/m2/uv_study/fit_cube.py`。只写当前研究目录，不改bbmodel或原素材。
'''
    (OUT/'CUBE_FIT.md').write_text(doc,encoding='utf-8')
    print(json.dumps({k:{'best':v['best'],'full_rmse':v['full_texture_best']['rmse_rgb_0_255']} for k,v in fit['faces'].items()},ensure_ascii=False))

if __name__=='__main__':main()
