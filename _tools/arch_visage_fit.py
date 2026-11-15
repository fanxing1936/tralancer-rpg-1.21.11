"""Arch-Visage 参考轮廓测量。只有几何拟合假设，不提取/重绘新纹样。"""
from pathlib import Path
import json, math
import numpy as np
from PIL import Image, ImageDraw
from scipy.optimize import least_squares, minimize
from scipy.ndimage import distance_transform_edt, binary_erosion
from scipy.spatial import ConvexHull

HERE=Path(__file__).resolve().parent
REF=HERE/'heart_of_ender_ref'
OUT=HERE/'arch_visage_ref'
FRAMES=REF/'frames/MCD_Arch-Visage_Spawn_Attack_in_game'

def rot(x=0,y=0,z=0):
    x,y,z=np.radians([x,y,z]);cx,sx=np.cos(x),np.sin(x);cy,sy=np.cos(y),np.sin(y);cz,sz=np.cos(z),np.sin(z)
    return np.array([[cz,-sz,0],[sz,cz,0],[0,0,1]])@np.array([[cy,0,sy],[0,1,0],[-sy,0,cy]])@np.array([[1,0,0],[0,cx,-sx],[0,sx,cx]])

def camera(yaw,elev,roll):
    ya,el=np.radians([yaw,elev]);v=np.array([-np.sin(ya)*np.cos(el),np.sin(el),-np.cos(ya)*np.cos(el)])
    right=np.cross([0,1,0],v);right/=np.linalg.norm(right);up=np.cross(v,right)
    rr=np.radians(roll);return np.array([np.cos(rr)*right+np.sin(rr)*up,-np.sin(rr)*right+np.cos(rr)*up,v])

def calibrate():
    # s005：沿可见黑壳棱线取点；嘴缘辉光使下沿约有2-5px不确定性。
    pixels=np.array([[148,87],[253,136],[360,100],[256,47],[135,247],[243,279],[347,250],[139,333],[235,377],[332,331]],float)
    def points(p):
        D,H,J,JW,JD=p[:5]
        return np.array([[6,J+H,-D/2],[-6,J+H,-D/2],[-6,J+H,D/2],[6,J+H,D/2],[6,J,-D/2],[-6,J,-D/2],[-6,J,D/2],[JW/2,0,-JD/2],[-JW/2,0,-JD/2],[-JW/2,0,JD/2]])
    def predict(p):
        c=camera(*p[5:8]);q=points(p)@c.T
        return q[:,:2]*[p[8],-p[8]]+[p[9],p[10]]
    x0=[12.8,15,7.3,11.2,11.8,45,25,0,13,245,330]
    fit=least_squares(lambda p:(predict(p)-pixels).ravel(),x0,bounds=([8,8,3,9,8,20,5,-20,7,100,200],[18,22,12,14,17,70,50,20,20,400,450]),max_nfev=3000)
    p=fit.x
    return {'parameters':p.tolist(),'head_dimensions':[12,p[1],p[0]],'jaw_dimensions':[p[3],p[2],p[4]],'camera_basis':camera(*p[5:8]).tolist(),'pixels_per_model_unit':p[8],'screen_origin':[p[9],p[10]],'source_frame':5,'source_time':.2,'source_landmarks':pixels.tolist(),'predicted_landmarks':predict(p).tolist(),'rms_px':float(np.sqrt(np.mean((predict(p)-pixels)**2))),'note':'fixed orthographic camera and cuboid dimensions inferred from s005 visible edges; no original geometry recovered; depth not independently observable'}

EDGES=[(i,j) for i in range(8) for j in range(i+1,8) if bin(i^j).count('1')==1]
def corners(lo,hi):
    return np.array([[hi[k] if i>>k&1 else lo[k] for k in range(3)] for i in range(8)],float)

def world_boxes(cal,p):
    D,H,J,JW,JD=cal['parameters'][:5]
    upper,lower,yaw,roll,x,y,head_y=p
    common=rot(0,yaw,roll)
    result=[]
    for lo,hi,pivot,angle,dy in [([-6,J,-D/2],[6,J+H,D/2],[0,J,D/2],upper,head_y),([-JW/2,0,-JD/2],[JW/2,J,JD/2],[0,J,JD/2],lower,0)]:
        v=corners(lo,hi);pivot=np.array(pivot);v=((v-pivot)@rot(angle).T+pivot+[0,dy,0])@common.T+[x,y,0];result.append(v)
    return result

def project(cal,v,div=1):
    q=v@np.asarray(cal['camera_basis']).T
    return (q[:,:2]*[cal['pixels_per_model_unit'],-cal['pixels_per_model_unit']]+cal['screen_origin'])/div

def mask(cal,p,size=125):
    im=Image.new('1',(size,size));d=ImageDraw.Draw(im)
    for v in world_boxes(cal,p):
        verts=list(v[v[:,1]>=0])
        for a,b in EDGES:
            if (v[a,1]<0)!=(v[b,1]<0):
                t=-v[a,1]/(v[b,1]-v[a,1]);verts.append(v[a]+t*(v[b]-v[a]))
        if len(verts)<3:continue
        xy=project(cal,np.asarray(verts),500/size)
        try:h=ConvexHull(xy)
        except Exception:continue
        d.polygon([tuple(q) for q in xy[h.vertices]],fill=1)
    return np.asarray(im,dtype=bool)

def mouth_mask(cal,p,size=125):
    im=Image.new('1',(size,size));d=ImageDraw.Draw(im);faces=[]
    viewer=np.asarray(cal['camera_basis'])[2]
    inds=[[3,2,0,1],[7,3,1,5],[6,7,5,4],[2,6,4,0],[2,3,7,6],[4,5,1,0]]
    for bi,v in enumerate(world_boxes(cal,p)):
        for fi,ix in enumerate(inds):
            q=v[ix];normal=np.cross(q[3]-q[0],q[1]-q[0])
            if normal@viewer<=0:continue
            # Occluding ground is handled by the silhouette; mouth comparison
            # is only applied before the sinking portion.
            faces.append((float(q.mean(0)@viewer),project(cal,q,500/size),int((bi==0 and fi==5)or(bi==1 and fi==4))))
    for _,xy,color in sorted(faces,key=lambda a:a[0]):d.polygon([tuple(q) for q in xy],fill=color)
    return np.asarray(im,dtype=bool)

def main():
    OUT.mkdir(exist_ok=True);cal=calibrate();(OUT/'calibration.json').write_text(json.dumps(cal,indent=2)+'\n')
    print('calibration RMS',cal['rms_px'],cal['head_dimensions'],cal['jaw_dimensions'],flush=True)
    sources=[];whites=[]
    for i in range(122):
        a=Image.open(FRAMES/f'frame_{i:04d}.png').convert('RGBA').getchannel('A').resize((125,125),Image.Resampling.NEAREST)
        sources.append(np.asarray(a)>0)
        rgb=np.array(Image.open(FRAMES/f'frame_{i:04d}.png').convert('RGBA').resize((125,125),Image.Resampling.NEAREST))
        whites.append((rgb[:,:,0]>210)&(rgb[:,:,1]>180)&(rgb[:,:,2]>210)&(rgb[:,:,3]>0))
    # Independent key-pose solves followed by per-frame local fitting retain
    # visible onset/recoil/close/sink, without interpreting bloom as a bone.
    guesses={2:[0,0,0,0,0,-16,0],5:[0,0,0,0,0,0,0],8:[20,-35,0,0,0,0,0],12:[75,0,0,0,0,0,0],16:[100,0,0,0,0,0,0],20:[-20,-60,0,0,0,0,7],50:[-20,-60,0,0,0,0,7],76:[-20,-60,0,0,0,0,7],80:[0,-10,0,0,0,0,0],82:[0,0,0,0,0,-2,0],89:[0,0,0,0,0,-14,0],91:[0,0,0,0,0,-22,0]}
    bounds=[(-65,120),(-100,35),(-45,45),(-40,40),(-12,12),(-35,10),(-8,15)]
    fitted={}
    def solve(i,start,prior=None,maxiter=100):
        target=sources[i];border=target&~binary_erosion(target);dt=distance_transform_edt(~border)
        target_n=target.sum()
        def fun(p):
            m=mask(cal,p);union=(m|target).sum()
            if not union or not m.any():return 100
            mb=m&~binary_erosion(m)
            cost=1-(m&target).sum()/union + .007*dt[mb].mean()
            if whites[i].sum()>85:
                wm=mouth_mask(cal,p);wt=whites[i];wu=(wm|wt).sum()
                if wu:cost+=.65*(1-(wm&wt).sum()/wu)
            if prior is not None:cost+=.00012*np.sum(((np.array(p)-prior)/[4,4,4,4,1,1,1])**2)
            return cost
        local_bounds=list(bounds)
        if 10<=i<=16:local_bounds[0]=(35,115)
        if 18<=i<=77:local_bounds[0]=(-60,15);local_bounds[1]=(-95,-25);local_bounds[6]=(0,15)
        if i<=5 or i>=82:local_bounds[0]=(-15,30);local_bounds[1]=(-15,30);local_bounds[6]=(-2,2)
        start=np.clip(start,np.array(local_bounds)[:,0]+.01,np.array(local_bounds)[:,1]-.01)
        result=minimize(fun,np.array(start,float),method='Powell',bounds=local_bounds,options={'maxiter':maxiter,'xtol':.03,'ftol':.00015})
        p=result.x;m=mask(cal,p)
        return p,{'frame':i,'time':i/25,'pose':p.tolist(),'silhouette_iou_125':float((m&target).sum()/(m|target).sum()),'cost':float(result.fun)}
    for i,g in guesses.items():
        candidates=[g]
        if i in [8,12,16,20]:
            candidates += [[a,b,0,0,0,0,h] for a,b,h in [(45,-20,0),(90,0,0),(-20,-60,7)]]
        best=None
        for g2 in candidates:
            p,r=solve(i,g2,maxiter=65)
            if best is None or r['cost']<best[1]['cost']:best=(p,r)
        fitted[i]=best;print('key',i,round(best[1]['silhouette_iou_125'],4),np.round(best[0],2).tolist(),flush=True)
    keys=sorted(fitted);records=[]
    prev=None
    for i in range(122):
        if i<2 or i>=92:
            p=np.array([0,0,0,0,0,-40.,0]);record={'frame':i,'time':i/25,'pose':p.tolist(),'silhouette_iou_125':1.0,'empty_reference':True}
        elif i in fitted:p,record=fitted[i]
        else:
            a=max(k for k in keys if k<i);b=min(k for k in keys if k>i)
            frac=(i-a)/(b-a);start=fitted[a][0]*(1-frac)+fitted[b][0]*frac
            if 21<=i<=75 and prev is not None:start=prev
            p,record=solve(i,start,prior=start,maxiter=30)
        records.append(record);prev=p
        if i%10==0:print('frame',i,round(record['silhouette_iou_125'],4),flush=True)
    (OUT/'fitted_motion.json').write_text(json.dumps({'coordinate_order':['head_x','jaw_x','root_y_rotation','root_z_rotation','root_x_position','root_y_position','head_y_position'],'frame_rate':25,'duration':4.88,'records':records,'fitting_limit':'silhouette and visible mouth-light constrained geometric inference; hidden depth remains unobservable; source alpha silhouette has glow and teeth that cuboids cannot exactly match'},indent=2)+'\n')
    board=Image.new('RGB',(1000,math.ceil(len(guesses)/4)*280),(55,60,70));draw=ImageDraw.Draw(board)
    for j,i in enumerate(guesses):
        target=sources[i];m=mask(cal,records[i]['pose']);a=np.zeros((125,125,3),np.uint8);a[:]=[55,60,70];a[target]=[125,125,125];a[m]=[180,100,170];a[target&m]=[210,210,210]
        board.paste(Image.fromarray(a).resize((250,250),Image.Resampling.NEAREST),((j%4)*250,(j//4)*280+25));draw.text(((j%4)*250+5,(j//4)*280+5),f'f{i:03d} IoU {records[i]["silhouette_iou_125"]:.3f}',fill='white')
    board.save(OUT/'silhouette_fit.png')

if __name__=='__main__':main()
