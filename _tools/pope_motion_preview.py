"""Blockbench 原生动画预览；逐段固定相机并排原GIF，不裁切逐帧轨迹。

Pillow仅排版/透明背景合成；模型像素始终来自Blockbench。
"""
import argparse,base64,hashlib,json,math,subprocess
from pathlib import Path
from types import SimpleNamespace
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import display_mob as dm
from pope_blockbench import BlockbenchMCP

REF=Path(__file__).resolve().parent/'pope_ref';OUT=REF/'m3/preview'
BG=(52,59,68,255);FONT='C:/Windows/Fonts/msyh.ttc'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def composite(im):
    b=Image.new('RGBA',im.size,BG);b.alpha_composite(im);return b

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--clips',nargs='*');ap.add_argument('--movies',action='store_true');args=ap.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    meta=read(REF/'m3/clipmeta.json');info=read(REF/'m3/blockbench_project.json');c=BlockbenchMCP()
    prefix="const project=ModelProject.all.find(p=>p.uuid==="+json.dumps(info['uuid'])+");if(!project||project.name!=='pope_m3_motion')throw Error('项目隔离');project.select();"
    ready=c.evaluate('(function(){'+prefix+'return {texture:Texture.all.every(t=>t.img.complete&&t.img.naturalWidth>0),animations:Animation.all.map(a=>a.name)};})()')
    assert ready['texture']
    bones,_,_=dm.load_bbmodel(SimpleNamespace(bbmodel=REF/'pope.bbmodel'))
    clips=dm.load_animations(SimpleNamespace(bbmodel=REF/'pope.bbmodel',anim_from=None))
    timing=read(REF/'m1/motion/gif_timing.json')
    evidence={'engine':'Blockbench 5.2.2 native animation WebGL','bbmodel_sha256':hashlib.sha256((REF/'pope.bbmodel').read_bytes()).hexdigest(),'in_game_verified':False,'clips':{}}
    size=600
    for clip in meta['clips']:
        name=clip['name']
        if name not in clips or (args.clips and name not in args.clips):continue
        out=OUT/name;out.mkdir(exist_ok=True)
        request=[{'time':k['proposed_clip_time_seconds'],'source_frame':k['source_frame']} for k in clip['key_poses']]
        source_key=clip['source_key']
        # Fixed camera for each whole clip, calibrated only from a source rest pose.
        # Whirlwind has no standing frame: source rod length ~300px maps to18 units.
        yaw,pitch=math.radians(43),math.radians(19)
        direction=[-math.sin(yaw)*math.cos(pitch),math.sin(pitch),-math.cos(yaw)*math.cos(pitch)]
        target=[-2,15,0]
        height=54
        source_rest={'idle':0,'walk':0,'attack':0,'summon':0,'cast':0,'appear':45,'teleport_in':30,'teleport_out':30}.get(name)
        calibration=None
        if name=='whirlwind':
            height=72;target=[0,18,0]
        else:
            source=Image.open(REF/f'm1/motion/frames/{source_key}/{source_rest:04}.png').convert('RGBA')
            bbox=source.getbbox()
            # Rest rig 30.6 units high; projected resting height from model default.
            # Walk reference is a lean/run pose: fixed calibration uses known crown/head scale.
            height=32.8*source.height/(bbox[3]-bbox[1])
            if name=='walk':height=500/10.6
            sx=((bbox[0]+bbox[2])/2-source.width/2)/source.height
            sy=(bbox[1]+bbox[3])/2/source.height-.5
            d=np.array(direction);d/=np.linalg.norm(d)
            right=np.cross([0,1,0],d);right/=np.linalg.norm(right);up=np.cross(d,right)
            target=(np.array([-2,15,0])-right*sx*height+up*sy*height).tolist()
            calibration={'source_rest_frame':source_rest,'source_bbox':list(bbox),'per_frame_camera_fit':False}
        fitted_cameras={'attack':(43.57,18.52,8.4059,243.17,366),
                        'summon':(42.98,19.42,7.9485,266.48,359.07),
                        'cast':(43.30,18.54,12.1637,253.59,448.58)}
        if name in fitted_cameras:
            yaw,pitch,px,u,v=fitted_cameras[name];yaw=math.radians(yaw);pitch=math.radians(pitch)
            direction=[-math.sin(yaw)*math.cos(pitch),math.sin(pitch),-math.cos(yaw)*math.cos(pitch)]
            right=np.array([-math.cos(yaw),0,math.sin(yaw)]);up=np.cross(direction,right)
            height=500/px;target=(right*(250-u)/px+up*(v-250)/px).tolist()
            calibration={'source_rest_frame':0,'method':'六个原作头盒角点与已确认12x7x6头部最小二乘；逐段一次','per_frame_camera_fit':False}
        transition_camera=REF/'m3/transition_cameras.json'
        if transition_camera.exists() and name in read(transition_camera)['cameras']:
            cam=read(transition_camera)['cameras'][name]
            direction=cam['direction'];height=cam['size']/cam['px']
            center=cam['size']/2;u,v=cam['origin']
            target=(np.array(cam['right'])*(center-u)/cam['px']+np.array(cam['up'])*(v-center)/cam['px']).tolist()
            calibration={'method':'源头/杖逐帧投影约束；固定相机与尺度为重建候选','per_frame_camera_fit':False,'source':cam}
        views=[{'name':'reference','direction':direction,'height':height,'target':target}]
        # Side and back retained for limb and cape orientation inspection at one pose.
        if not args.movies:
            views += [{'name':'side','direction':[-1,0,0],'height':max(52,height*1.2),'target':[0,18,0]},
                      {'name':'back','direction':[0,0,1],'height':max(52,height*1.2),'target':[0,18,0]}]
        render_requests=request
        if args.movies:
            render_requests=[{'time':round(i/20,5),'source_frame':None} for i in range(round(clip['length']*20)+1)]
        frames={};matrix_error=0;matrix_failures=[]
        # Batches avoid giant MCP response and allow frequent progress output.
        for start in range(0,len(render_requests),8):
            batch=render_requests[start:start+8]
            code="""(function(){PREFIX
              Modes.options.animate.select();const a=Animation.all.find(a=>a.name===ANIMATION);if(!a)throw Error('clip不存在');a.select();
              const p=new Preview({id:'pope_m3_offscreen',offscreen:true,antialias:false});p.setProjectionMode(true);p.resize(SIZE,SIZE);p.renderer.setPixelRatio(1);
              const output=[];
              for(const req of REQUEST){Timeline.setTime(req.time);Animator.preview();Canvas.scene.updateMatrixWorld(true);
                const images={};for(const v of VIEWS){const target=new THREE.Vector3(...v.target);const pos=target.clone().addScaledVector(new THREE.Vector3(...v.direction).normalize(),100);
                  p.camOrtho.position.copy(pos);p.controls.target.copy(target);p.camOrtho.up.set(0,1,0);p.camOrtho.lookAt(target);p.camOrtho.zoom=(SIZE/40)/v.height;p.camOrtho.updateProjectionMatrix();p.controls.update();
                  Canvas.withoutGizmos(()=>{p.render();images[v.name]=p.canvas.toDataURL('image/png')});}
                output.push({time:req.time,images,matrices:Object.fromEntries(Group.all.map(g=>[g.name,g.mesh.matrixWorld.toArray()]))});
              }p.renderer.dispose();return output;})()""".replace('PREFIX',prefix).replace('ANIMATION',json.dumps('animation.'+name)).replace('REQUEST',json.dumps(batch)).replace('VIEWS',json.dumps(views)).replace('SIZE',str(size))
            result=c.evaluate(code)
            for r in result:
                t=r['time'];frames[t]={}
                for view,encoded in r['images'].items():
                    file=out/f'{t:05.2f}_{view}.png';file.write_bytes(base64.b64decode(encoded.split(',')[1]));frames[t][view]=file
                for bone,flat in r['matrices'].items():
                    expected=np.array(dm.posed_matrix(bones,bone,clips[name],t))@np.array(dm.translate(*bones[bone]['pivot']))
                    actual=np.array(flat).reshape(4,4).T
                    error=float(np.max(np.abs(actual-expected)))
                    matrix_error=max(matrix_error,error)
                    if error>2e-4:matrix_failures.append({'time':t,'bone':bone,'error':error})
        if matrix_error>2e-4:
            write(out/'matrix_mismatch.json',matrix_failures)
            raise ValueError(f'{name} BB/runtime matrix mismatch {matrix_error}; first={matrix_failures[:3]}')
        font=ImageFont.truetype(FONT,25);small=ImageFont.truetype(FONT,19)
        def pair(req):
            pane=Image.new('RGBA',(size*2,size+90),BG);d=ImageDraw.Draw(pane)
            sf=req['source_frame'];t=req['time']
            if sf is not None:
                source=Image.open(REF/f'm1/motion/frames/{source_key}/{sf:04}.png').convert('RGBA')
                factor=size/max(source.size);source=source.resize((round(source.width*factor),round(source.height*factor)),Image.Resampling.NEAREST)
                pane.alpha_composite(source,((size-source.width)//2,70+(size-source.height)//2))
                duration=.03 if source_key=='walk' else .04
                d.text((15,8),f'原作 / Mojang · 帧{sf} · {sf*duration:.2f}s',font=font,fill='white')
            else:d.text((15,8),'推断：无原作对应帧',font=font,fill='#ffcf76')
            pane.alpha_composite(Image.open(frames[t]['reference']).convert('RGBA'),(size,70))
            d.text((size+15,8),f'{name} · 模型 {t:.2f}s',font=font,fill='white')
            d.text((size+15,41),'固定相机 / Blockbench 原生 / 未在游戏内验证',font=small,fill='#d1d8df')
            return pane.convert('RGB')
        if args.movies:
            movie=[];keyposes=clip['key_poses']
            for req in render_requests:
                t=req['time']
                points=[k for k in keyposes if k['source_frame'] is not None]
                if name=='whirlwind' and t>6.4:sf=None
                else:
                    times=[k['proposed_clip_time_seconds'] for k in points]
                    fs=[k['source_frame'] for k in points]
                    sf=int(round(float(np.interp(t,times,fs))))
                movie.append(pair({'time':t,'source_frame':sf}).resize((960,552),Image.Resampling.LANCZOS))
            movie[0].save(out/(name+'_comparison.gif'),save_all=True,append_images=movie[1:],duration=50,loop=0,disposal=2)
            # MP4 useful for long whirlwind without an enormous GIF.
            import imageio_ffmpeg
            subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-nostdin','-hide_banner','-loglevel','error','-y',
                '-i',str(out/(name+'_comparison.gif')),'-r','20','-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(out/(name+'_comparison.mp4'))],check=True)
        else:
            board=Image.new('RGB',(size*2,(size+90)*len(request)),BG[:3])
            for i,req in enumerate(request):
                p=pair(req);p.save(out/f"compare_{req['time']:05.2f}.jpg",quality=92);board.paste(p,(0,i*(size+90)))
            board.save(out/'keyposes.jpg',quality=91)
            review_time=clip['release_times'][0] if clip['release_times'] else request[min(2,len(request)-1)]['time']
            if review_time not in frames:review_time=request[0]['time']
            tri=Image.new('RGBA',(size*3,size+60),BG)
            for i,v in enumerate(('reference','side','back')):
                tri.alpha_composite(Image.open(frames[review_time][v]),(i*size,60));ImageDraw.Draw(tri).text((i*size+10,10),f'{name} {review_time:.2f}s / {v}',font=font,fill='white')
            tri.convert('RGB').save(out/'three_views.jpg',quality=92)
        evidence['clips'][name]={'views':views,'calibration':calibration,'samples':len(render_requests),'native_vs_pipeline_matrix_max_error':matrix_error,'per_frame_camera_fit':False}
        write(OUT/('movie_evidence.json' if args.movies else 'render_evidence.json'),evidence)
        print(json.dumps({'clip':name,'samples':len(render_requests),'max_matrix_error':matrix_error}),flush=True)

if __name__=='__main__':main()
