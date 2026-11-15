"""Resolve the mouth-facing ambiguity with explicit visible lip corners."""
from pathlib import Path
import json,copy
import numpy as np
from PIL import Image
from scipy.optimize import least_squares
import arch_visage_fit as fit

OUT=fit.OUT
def main():
    cal=json.loads((OUT/'calibration.json').read_text());doc=json.loads((OUT/'fitted_motion.json').read_text());records=doc['records']
    records[5]['pose']=[0,0,0,0,0,0,0]
    records[5]['refinement']='source005 calibrated closed pose; removed spurious 8.46-degree upper-jaw opening from silhouette optimizer'
    labels=[(0,3),(0,2),(0,6),(0,1),(0,0),(0,4),(1,2),(1,3),(1,7),(1,6)]
    targets=np.array([[198,73],[309,117],[358,212],[111,184],[219,230],[259,298],[230,392],[131,331],[165,246],[259,298]],float)
    def residual(p):
        boxes=[fit.project(cal,v)for v in fit.world_boxes(cal,p)]
        return(np.array([boxes[b][i]for b,i in labels])-targets).ravel()
    result=least_squares(residual,[50,-100,0,10,10,-6,-3],bounds=([-30,-160,-65,-45,-30,-25,-20],[140,25,65,45,30,25,20]),max_nfev=3000)
    pose=result.x;stats=[]
    for i in range(122):
        a=np.array(Image.open(fit.FRAMES/f'frame_{i:04d}.png').convert('RGBA'));y,x=np.where(a[:,:,3]>0)
        if len(x):
            center=np.array([x.mean(),y.mean()]);cov=np.cov(np.stack([x,y]));w,v=np.linalg.eigh(cov);ang=np.degrees(np.arctan2(v[1,-1],v[0,-1]));stats.append((center,ang))
        else:stats.append((np.zeros(2),0))
    k=cal['pixels_per_model_unit'];B=np.asarray(cal['camera_basis']);A=np.array([[k*B[0,0],k*B[0,1]],[-k*B[1,0],-k*B[1,1]]])
    for i in range(20,77):
        p=pose.copy();delta=np.linalg.solve(A,stats[i][0]-stats[20][0]);p[4]+=delta[0];p[5]+=delta[1]
        da=(stats[i][1]-stats[20][1]+90)%180-90;p[3]+=float(np.clip(da*.65,-3,3))
        records[i]['pose']=p.tolist();records[i]['refinement']='source20 visible face-corner constraints; per-frame source silhouette centroid and bounded PCA tilt; hidden 3D motion inferred'
    for i in [17,18,19]:
        a=(i-16)/4;p=(1-a)*np.array(records[16]['pose'])+a*pose;records[i]['pose']=p.tolist();records[i]['refinement']='recoil recovery between measured16 and mouth-constrained20; numerical interpolation, not recovered original bone curve'
    for i in [77,78,79]:
        a=(i-76)/4;p=(1-a)*np.array(records[76]['pose'])+a*np.array(records[80]['pose']);records[i]['pose']=p.tolist();records[i]['refinement']='closing transition between source76 and80, inferred interpolation'
    # Last sliver uses source silhouette endpoints rather than allowing the
    # unconstrained optimizer to leave a broad floating wedge.
    for i in [90,91]:
        p=np.array(records[89]['pose']);p[5]-=(i-89)*3.4;records[i]['pose']=p.tolist();records[i]['refinement']='position-only final sinking continuation; no scale'
    doc['mouth_correspondence']={'source_frame':20,'source_time':.8,'box_vertex_labels':labels,'source_xy':targets.tolist(),'pose':pose.tolist(),'rms_px':float(np.sqrt(np.mean(residual(pose)**2))),'status':'manual visible-front/inside-plane correspondences resolve previous silhouette-only flipped-face solution; joint rotations/depth still inferred'}
    # Orthographic footage cannot determine translation along the viewing ray.
    # Choose that hidden degree of freedom so the visible attack does not sink
    # its lower lip into our hypothetical floor. Screen coordinates are exact.
    viewer=np.asarray(cal['camera_basis'])[2]
    for r in records:
        i=r['frame'];v=np.concatenate(fit.world_boxes(cal,r['pose']));minimum=float(v[:,1].min())
        stage_weight=(i-17)/3 if 18<=i<=19 else 1.0 if 20<=i<=76 else (80-i)/4 if 77<=i<=79 else 0.0
        lift=max(0.,-minimum)/viewer[1]*stage_weight
        r['depth_lift_translation']=(viewer*lift).tolist()
        r['depth_lift_note']='unobservable orthographic view-ray translation; chosen to keep full attack geometry above assumed floor, not recovered original trajectory'
    for r in records:
        i=r['frame'];s=np.array(Image.open(fit.FRAMES/f'frame_{i:04d}.png').getchannel('A').resize((125,125),Image.Resampling.NEAREST))>0;m=fit.mask(cal,r['pose']);u=(s|m).sum();r['final_silhouette_iou_125']=float((s&m).sum()/u)if u else 1.
    (OUT/'refined_motion.json').write_text(json.dumps(doc,indent=2)+'\n');print('mouth RMS',doc['mouth_correspondence']['rms_px'])
if __name__=='__main__':main()
