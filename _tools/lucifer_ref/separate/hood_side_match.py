"""Bounded diffuse-only visible hood-side correspondence study; never edits a model."""
from pathlib import Path
import json, hashlib, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.optimize import differential_evolution

HERE=Path(__file__).resolve().parent
REF=HERE.parent
source=np.asarray(Image.open(REF/'Root_Rot_Armor_texture.png').convert('RGBA'),dtype=float)
render=np.asarray(Image.open(REF/'MCD_Root_Rot_Armor.png').convert('RGB'),dtype=float)
ss,tt=np.meshgrid(np.linspace(.10,.90,12),np.linspace(.12,.72,12))
ss,tt=ss.ravel(),tt.ravel()
BOUNDS=[(302,310),(84,93),(47,58),(4,13),(-31,-23),(158,174)]
INITIAL=[306,88,52,8,-27,166]
SIZES=[(w,h) for w in (4,5,6,8,10) for h in (8,10,12)]

def samples(projection):
    ox,oy,ux,uy,vx,vy=projection
    x=np.rint(ox+ss*ux+tt*vx).astype(int)
    y=np.rint(oy+ss*uy+tt*vy).astype(int)
    return render[y,x],np.column_stack([x,y])

def orient(a,k,flip):
    a=np.rot90(a,k)
    return a[:,::-1] if flip else a

def candidate(uv,k,flip):
    u,v,U,V=uv
    a=orient(source[v:V,u:U],k,flip)
    y=np.minimum(a.shape[0]-1,np.floor(tt*a.shape[0]).astype(int))
    x=np.minimum(a.shape[1]-1,np.floor(ss*a.shape[1]).astype(int))
    return a[y,x]

def lighting(c,target):
    cc=c-c.mean(axis=-2,keepdims=True)
    yc=target-target.mean(axis=-2,keepdims=True)
    slope=(cc*yc).sum(axis=-2)/np.maximum((cc*cc).sum(axis=-2),1e-9)
    slope=np.clip(slope,.25,5)
    offset=np.clip(target.mean(axis=-2)-slope*c.mean(axis=-2),-35,80)
    predicted=c*slope[...,None,:]+offset[...,None,:]
    mse=((predicted-target)**2).mean(axis=(-2,-1))
    return mse,slope,offset,predicted

def shortlist(projection,limit=30):
    target,_=samples(projection)
    winners=[]
    for w,h in SIZES:
        windows=np.lib.stride_tricks.sliding_window_view(source,(h,w),axis=(0,1)).transpose(0,1,3,4,2)
        ny,nx=windows.shape[:2]
        flat=windows.reshape(-1,h,w,4)
        for k in range(4):
            for flip in (False,True):
                a=np.rot90(flat,k,axes=(1,2))
                if flip:a=a[:,:,::-1]
                ys=np.minimum(a.shape[1]-1,np.floor(tt*a.shape[1]).astype(int))
                xs=np.minimum(a.shape[2]-1,np.floor(ss*a.shape[2]).astype(int))
                c=a[:,ys,xs]
                ok=(c[:,:,3]==255).all(axis=1)&(c[:,:,:3].std(axis=(1,2))>3)
                if not ok.any():continue
                idx=np.flatnonzero(ok)
                mse,_,_,_=lighting(c[ok,:,:3],target)
                take=np.argsort(mse)[:3]
                for z in take:
                    i=int(idx[z]);x=i%nx;y=i//nx
                    winners.append({'uv':[x,y,x+w,y+h],'rotate_ccw_quarters':k,'flip_after_rotation':flip,'initial_mse':float(mse[z])})
    winners.sort(key=lambda r:r['initial_mse'])
    return winners[:limit]

def refine(row):
    c=candidate(row['uv'],row['rotate_ccw_quarters'],row['flip_after_rotation'])[:,:3]
    def objective(x):return float(lighting(c,samples(x)[0])[0])
    res=differential_evolution(objective,BOUNDS,seed=17,popsize=9,maxiter=130,polish=False,tol=.0005)
    target,positions=samples(res.x)
    mse,slope,offset,predicted=lighting(c,target)
    return {**row,'rmse':math.sqrt(float(mse)),'mse':float(mse),'projection':res.x.tolist(),'lighting_slope_rgb':slope.tolist(),'lighting_offset_rgb':offset.tolist(),'sample_positions_xy':positions.tolist(),'reference_sample_rgb':target.tolist(),'source_sample_rgb':c.tolist(),'predicted_rgb':predicted.tolist()}

def main():
    first=shortlist(INITIAL,24)
    fits=[refine(row) for row in first]
    fits.sort(key=lambda r:r['mse'])
    second=shortlist(fits[0]['projection'],12)
    seen={(tuple(r['uv']),r['rotate_ccw_quarters'],r['flip_after_rotation']) for r in fits}
    for row in second:
        key=(tuple(row['uv']),row['rotate_ccw_quarters'],row['flip_after_rotation'])
        if key not in seen:fits.append(refine(row));seen.add(key)
    current=refine({'uv':[10,8,20,18],'rotate_ccw_quarters':0,'flip_after_rotation':False,'label':'current_candidate'})
    fits.sort(key=lambda r:r['mse'])
    best=fits[0]
    result={'status':'correspondence_study_only_not_exact_acceptance','source_sha256':{n:hashlib.sha256((REF/n).read_bytes()).hexdigest() for n in ['Root_Rot_Armor_texture.png','MCD_Root_Rot_Armor.png']},'method':'144 fixed normalized sample points within visible side plane; nearest render sampling; bounded six-parameter affine projection; one global RGB slope+offset; diffuse only, no shadow material and no pixel-specific recoloring','domain':{'normalized_s_range':[.10,.90],'normalized_t_range':[.12,.72],'projection_bounds':BOUNDS,'initial_projection':INITIAL,'source_sizes':SIZES,'source_origins':'all in-bounds original 64x64 origins','orientations':'4 quarter turns x optional horizontal reflection','shortlist_rounds':[24,12],'refinement_seed':17,'refinement_maxiter':130,'refinement_popsize':9,'slope_bounds':[.25,5],'offset_bounds':[-35,80]},'best':best,'current_candidate':current,'ranking':fits[:12],'limitations':['Only visible inner portion; rear hood fold and shoulder-occluded bottom deliberately excluded.','A nonzero residual supports correspondence only; not exact original UV proof.','The tested rectangle sizes are bounded; untested sizes or piecewise surfaces could fit differently.','Lighting is a single channel-wise affine fit per face, not the original material.','No model or UV was modified.']}
    (HERE/'hood_side_match.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    lines=['# 可见兜帽侧面：有界数值匹配','','只比较原作可见侧面的内区；避开远端折边和肩部遮挡。只用diffuse PNG，不用ShadowTexture，不逐像素调色。**非零残差不构成“一模一样”验收。**','','## 最佳候选与现方案','',f"最佳：原区 `{best['uv']}`，逆时针旋转 {best['rotate_ccw_quarters']*90}°，旋转后水平反转={best['flip_after_rotation']}；RMSE **{best['rmse']:.4f}/255**。",f"当前 `[10,8,20,18]`、不旋转不翻转：RMSE **{current['rmse']:.4f}/255**。",'','## 候选排名','','| 原图UV | 逆时针旋转 | 水平反转 | RMSE/255 |','|---|---:|---|---:|']
    for r in fits[:12]:lines.append(f"| {r['uv']} | {r['rotate_ccw_quarters']*90}° | {r['flip_after_rotation']} | {r['rmse']:.4f} |")
    lines+=['','## 方法与限制','','144个固定归一化点：s∈[0.10,0.90]，t∈[0.12,0.72]。遍历宽4/5/6/8/10、高8/10/12的连续原图矩形及8种方向，只取采样处完全不透明的候选；先固定投影排名，再对24个候选与一次12名复查进行有界仿射优化。','',f"最佳投影 [ox,oy,ux,uy,vx,vy]：`{best['projection']}`。",f"统一光照 slope RGB：`{best['lighting_slope_rgb']}`；offset RGB：`{best['lighting_offset_rgb']}`。",'','完整边界、采样位置、源RGB、原图采样RGB和预测RGB在JSON中。单次全局颜色拟合只能补偿相同面照明，不能重现原版材质。搜索是有限的，结果不能排除未测试尺寸或分片面。原图折边/下缘没有包含在本次验证，因此不能用内区匹配推导整个帽侧，更不能推导背面。','', '没有修改模型或最终UV。原素材版权归Mojang；本项目非商业，与Mojang无关联。']
    (HERE/'hood_side_match.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    fnt='C:/Windows/Fonts/msyh.ttc';font=ImageFont.truetype(fnt,20);small=ImageFont.truetype(fnt,16)
    canvas=Image.new('RGB',(1400,680),'#172029');d=ImageDraw.Draw(canvas);d.text((25,20),'兜帽可见侧面内区｜有限数值对应，不是完整面验收',font=font,fill='white')
    base=Image.fromarray(render.astype(np.uint8));canvas.paste(base,(20,80));d=ImageDraw.Draw(canvas)
    for x,y in best['sample_positions_xy']:d.ellipse((20+x-1,80+y-1,20+x+1,80+y+1),fill='#ff8c4c')
    for j,(title,array) in enumerate([('源纹理采样',best['source_sample_rgb']),('原作采样',best['reference_sample_rgb']),('统一光照预测',best['predicted_rgb'])]):
        x=555+j*275;a=np.array(array).reshape(12,12,3);im=Image.fromarray(np.clip(a,0,255).astype(np.uint8)).resize((240,360),Image.Resampling.NEAREST);canvas.paste(im,(x,130));d.text((x,90),title,font=font,fill='white')
    d.text((555,525),f"UV {best['uv']} / rot {best['rotate_ccw_quarters']*90} / flip {best['flip_after_rotation']}",font=font,fill='#d9e5e9')
    d.text((555,565),f"RMSE {best['rmse']:.4f}/255；当前方案 {current['rmse']:.4f}/255",font=font,fill='#d9e5e9')
    d.text((25,635),'固定内区144点；无ShadowTexture、无逐像素调色；折边/遮挡区未验证。',font=small,fill='#aabac5');canvas.save(HERE/'hood_side_match.png')
    print(json.dumps({'best_uv':best['uv'],'rotation':best['rotate_ccw_quarters'],'flip':best['flip_after_rotation'],'best_rmse':best['rmse'],'current_rmse':current['rmse'],'ranked_count':len(fits)},ensure_ascii=False))

if __name__=='__main__':main()
