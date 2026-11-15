"""从逐帧记录生成 M3 原生渲染请求和对照页索引。"""
import json
from pathlib import Path
from heart_of_ender_blockbench import REF

def read(p):return json.loads(p.read_text('utf8'))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n','utf8')

def main():
    motion=REF/'m3_motion';out=REF/'m3_preview';out.mkdir(exist_ok=True)
    shell=read(motion/'shell_motion.json');inner=read(motion/'inner_render_requests.json')
    records=read(motion/'shell_measurements.json')['records']
    c=shell['camera'];ground=shell['ground_y']
    views={'shell':{'position':c['position'],'target':c['target'],'height':c['orthographic_height'],'width':500,'height_px':500},
        'overview':{'position':[-54,54,-54],'target':[0,17,0],'height':80,'width':500,'height_px':500,'ground_y':ground},
        'front':{'position':[0,17,-100],'target':[0,17,0],'height':80,'width':500,'height_px':500,'ground_y':ground},
        'side':{'position':[100,17,0],'target':[0,17,0],'height':80,'width':500,'height_px':500,'ground_y':ground},
        'back':{'position':[0,17,100],'target':[0,17,0],'height':80,'width':500,'height_px':500,'ground_y':ground},
        **inner['views']}
    views['inner']['follow_bone']='shell_root'
    views['cross_near_front']={'position':[0,66.261826,-90.630779],'target':[0,24,0],
        'height':80,'width':500,'height_px':500,'ground_y':ground}
    # 抬肢后轮廓更高；整段固定较宽取景，避免上肢在预览顶边被裁。
    for v in ('overview','front','side','back'):
        base=views[v]
        views['cross_'+v]={**base,'height':96,
            'position':[base['position'][0],base['position'][1]+9,base['position'][2]],
            'target':[base['target'][0],base['target'][1]+9,base['target'][2]]}
    frames=[];sections=[]
    for cycle in range(4):
        sec={'id':f'idle_cycle_{cycle+1}','title':f'idle · 第{cycle+1}周期 · 有动图','subtitle':'左：原GIF同刻；右：Blockbench模型；外壳固定相机，小人另按Docile重定时','pairs':[]}
        for rec in records:
            if int(rec['source_frame']//100)!=cycle:continue
            ident=f"idle/{rec['id']}"
            frames.append({'id':ident,'clip':'idle','time':rec['time'],'view':'shell','source_path':rec['source_path']})
            sec['pairs'].append({'source':rec['source_path'],'model':f'm3_preview/{ident}.png',
                'label':f"f{rec['source_frame']:03d} · t={rec['time']:.2f}s",'source_label':'原片 / 有动图','model_label':'保存模型 / 同刻'})
        sections.append(sec)
    for category,title,clip in [('docile','Docile → idle · 三周期、90%速度','idle'),('anxious','Anxious → walk · 有动图','walk'),('fourside','Fourside → cross_beam · 有动图','cross_beam')]:
        sec={'id':category,'title':title,'subtitle':'左：独立小人原GIF；右：剥离壳根整体运动的近景，固定大小，无逐帧缩放','pairs':[]}
        for f in inner['frames']:
            if not f['id'].startswith('inner_'+category+'_'):continue
            frame=dict(f);frame['id']='inner/'+f['id'];frames.append(frame)
            n=int(f['source_path'].rsplit('_',1)[1].split('.')[0]);source_t=n/25
            sec['pairs'].append({'source':f['source_path'],'model':f"m3_preview/{frame['id']}.png",
                'label':f"源 f{n:03d} {source_t:.2f}s → 模型 {f['time']:.5f}s",
                'source_label':'原片 / 有动图','model_label':'Blockbench / 独立近景'})
        sections.append(sec)
    refs={'walk':'Heart_of_ender_crawling_with_decal_trail.png','mortar':'Minecraft-dungeons-heart-of-ender.jpg',
        'cross_beam':'Heart_of_Ender_prepare_to_shoot_beams.png','sink':'Heart_of_Ender_in_game.png',
        'rise':'Heart_of_Ender_in_game.png','death':'Hero_kills_Heart_of_Ender_Arch-Illager_disappear.jpg'}
    for clip in shell['clips'][1:]:
        name=clip['name'];sec={'id':name,'title':name+' · 外壳推断动作','subtitle':'左：依据截图（不是同帧）；右：模型时间轴。节奏/接地次序没有原动图证据。','pairs':[]}
        for p in clip['key_poses']:
            ident=f"{name}/{name}_{p['time']:05.2f}"
            frames.append({'id':ident,'clip':name,'time':p['time'],'view':'cross_overview' if name=='cross_beam' else 'overview'})
            sec['pairs'].append({'source':refs[name],'model':f'm3_preview/{ident}.png','label':f"{name} · t={p['time']:.2f}s",
                'source_label':'依据截图 / 不同帧','model_label':'推断姿态 / Blockbench'})
        sections.append(sec)
    ident='cross_beam/cross_near_front'
    frames.append({'id':ident,'clip':'cross_beam','time':2,'view':'cross_near_front'})
    sections.append({'id':'cross_reference_view','title':'cross_beam · 抬肢近正面检查',
        'subtitle':'近正面略俯视是假设相机；保留 R2 肢根和骨长，上层肢体比截图更高。源根部被烟雾遮挡，未改静态连接来追图。',
        'pairs':[{'source':'Heart_of_Ender_prepare_to_shoot_beams.png','model':'m3_preview/'+ident+'.png',
            'label':'C1 · 2.00s · 固定肢根','source_label':'依据截图 / 推断','model_label':'原生模型 / 近正面'}]})
    side_samples={'idle':2.6,'walk':.5,'mortar':1.2,'cross_beam':2,'sink':.8,'rise':1.2,'death':3.8}
    for name,time in side_samples.items():
        sec={'id':name+'_views','title':name+' · 正侧背连接检查','subtitle':'这页左右均为模型；用于检查关节和背部，不声称有原作侧背素材。','pairs':[]}
        ids={}
        for view in ('overview','front','side','back'):
            ident=f'views/{name}_{view}';ids[view]=f'm3_preview/{ident}.png'
            frames.append({'id':ident,'clip':name,'time':time,'view':'cross_'+view if name=='cross_beam' else view})
        sec['pairs']=[{'source':ids['overview'],'model':ids['front'],'label':f'{name} {time:.2f}s','source_label':'模型 / 四分之三','model_label':'模型 / 正面'},
            {'source':ids['side'],'model':ids['back'],'label':f'{name} {time:.2f}s','source_label':'模型 / 右侧','model_label':'模型 / 背面'}]
        sections.append(sec)
    write(motion/'review_requests.json',{'views':views,'frames':frames})
    write(motion/'review_index.json',{'sections':sections})
    movies=[]
    for clip in shell['clips']:
        name=clip['name'];fps=12.5
        for i in range(round(clip['length']*fps)+1):
            t=round(i/fps,5)
            if t>clip['length']+1e-6:continue
            movies.append({'id':f'movies/{name}/frame_{i:04d}','clip':name,'time':t,'view':'shell' if name=='idle' else 'cross_overview' if name=='cross_beam' else 'overview'})
    write(motion/'movie_requests.json',{'views':views,'frames':movies})
    print(f"关键姿态 {len(frames)} 张；连续预览 {len(movies)} 张（12.5fps）")

if __name__=='__main__':main()
