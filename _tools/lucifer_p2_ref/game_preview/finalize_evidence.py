from pathlib import Path
from PIL import Image
from scipy.ndimage import label
import hashlib,json,re,shutil
import numpy as np

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'evidence'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
peak=OUT/'phase50_peak.png';trough=OUT/'phase150_trough.png'
a=np.array(Image.open(peak).convert('RGB')).astype(int)
b=np.array(Image.open(trough).convert('RGB')).astype(int)
yy,xx=np.indices(a.shape[:2])
candidate=(np.maximum(a.max(2),b.max(2))>45)&(xx>430)&(xx<890)&(yy>150)&(yy<730)
labels,n=label(candidate)
counts=np.bincount(labels.ravel());counts[0]=0
mask=counts[labels]>=8
d=a-b
changed=np.any(d!=0,axis=2)&mask
y,x=np.nonzero(changed)
report={'resolution':[a.shape[1],a.shape[0]],
        'mask_method':'4-connected components of max(peak,trough).RGB >45, area >=8, within x430..890/y150..730; excludes isolated sky stars',
        'model_mask_pixels':int(mask.sum()),'changed_model_pixels':int(changed.sum()),
        'positive_difference_pixels':int(((d>0).any(2)&mask).sum()),
        'negative_difference_pixels':int(((d<0).any(2)&mask).sum()),
        'max_delta_rgb':d[mask].max(0).tolist(),'min_delta_rgb':d[mask].min(0).tolist(),
        'mean_delta_rgb':d[mask].mean(0).tolist(),
        'change_bbox':[int(x.min()),int(y.min()),int(x.max()),int(y.max())],
        'peak_sha256':sha(peak),'trough_sha256':sha(trough),
        'note':'Positive = phase50 minus phase150. Diagnostic mask is not a complete silhouette/visible-texel mask. Original full F2 screenshots are preserved unmodified.'}
(OUT/'pulse_pixel_difference.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
Image.fromarray(np.uint8(mask)*255).save(OUT/'model_comparison_mask.png')
Image.fromarray(np.uint8(np.minimum(np.abs(d)*16,255))*mask[:,:,None]).save(OUT/'pulse_model_difference_x16.png')
shutil.copy2(ROOT/'client_console.log',OUT/'client_console_snapshot.log')
shutil.copy2(ROOT/'server/console.log',OUT/'private_server_console.log')
shutil.copy2(ROOT/'server/status.json',OUT/'private_server_status.json')
shutil.copy2(ROOT/'launch_manifest.json',OUT/'launch_manifest.json')
lines=(OUT/'client_console_snapshot.log').read_text(encoding='utf-8').splitlines()
shader_errors=[s for s in lines if re.search(r'shader|program|pipeline|uniform',s,re.I) and re.search(r'ERROR|Failed|Exception|Invalid|Couldn.t',s,re.I)]
resource_errors=[s for s in lines if re.search(r'Unable to load|Missing texture|Unable to resolve texture|Failed to load model|Couldn.t load texture|Failed to compile',s,re.I)]
warnings=[s for s in lines if '/WARN]' in s]
errors=[s for s in lines if '/ERROR]' in s]
runtime=ROOT/'game/resourcepacks/LuciferP2-Isolated'
rp=Path(r'D:\agent\dungeons_extract\phase2_b\build_workspace\resourcepack')
shaders={}
for ext in ('vsh','fsh'):
    rel=Path('assets/minecraft/shaders/core/rendertype_item_entity_translucent_cull.'+ext)
    shaders[str(rel)]={'runtime_sha256':sha(runtime/rel),'build_sha256':sha(rp/rel),'equal':(runtime/rel).read_bytes()==(rp/rel).read_bytes()}
review={'resource_manager_loaded':['vanilla','file/LuciferP2-Isolated'],
        'item_atlas_observed':'8192x8192x0','shader_or_pipeline_error_matches':shader_errors,
        'texture_model_or_compile_error_matches':resource_errors,'shader_files':shaders,
        'all_error_headers':errors,'all_warning_headers':warnings,
        'known_error_explanations':{
           'offline_auth':'Dummy token 0 caused expected user-properties/Realms authentication failures; no login attempted.',
           'test_helper':'First p2_visual:setup contained tick freeze, unavailable at function permission level 2. Removed before /reload at 14:37:55; later reloads and setup succeeded. Not a production RPG function.',
           'temporary_path':'Initial LWJGL extract directory did not yet exist at early storage-space probe. The subsequent renderer initialized; launcher now creates this isolated directory.',
           'initial_passengers':'39 Received passengers for unknown entity warnings occurred together at first singleplayer join 14:37:30. They did not recur after reload/scene setup; displayed model was visibly complete. This is retained as an integration warning, not silently treated as no-warning.',
           'performance':'Full RPG ticking initially reported 40-148 ticks behind. Visual fixture later replaces tick list to isolate material/pose; this test is not a production performance pass.'}}
(OUT/'client_log_review.json').write_text(json.dumps(review,indent=2),encoding='utf-8')
originals=[]
for src,label_name,phase in [(ROOT/'game/screenshots/2026-11-08_14.39.34.png','phase50_peak.png',50),(ROOT/'game/screenshots/2026-11-08_14.40.01.png','phase150_trough.png',150)]:
    assert src.read_bytes()==(OUT/label_name).read_bytes()
    originals.append({'original_path':str(src),'evidence_copy':label_name,'phase':phase,'mtime_ns':src.stat().st_mtime_ns,'bytes':src.stat().st_size,'sha256':sha(src)})
(OUT/'original_screenshots.json').write_text(json.dumps(originals,indent=2),encoding='utf-8')
manifest={str(p.relative_to(OUT)):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in OUT.rglob('*') if p.is_file() and p.name!='manifest.json'}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps({'pixel_comparison':report,'shader_error_count':len(shader_errors),'resource_error_count':len(resource_errors),'warning_count':len(warnings),'error_headers':errors},indent=2))
