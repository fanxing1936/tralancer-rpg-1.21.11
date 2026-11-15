"""单帧肢体歧义的两方案原生渲染；从不替换正式模型。"""
import copy
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
from heart_of_ender_blockbench import REF
from heart_of_ender_motion_preview import render

def inner_options(doc, original):
    proposals=json.loads((REF/'m3_motion/inner_endpoint_proposals.json').read_text('utf8'))
    request_doc=json.loads((REF/'m3_motion/inner_render_requests.json').read_text('utf8'))
    request_doc['views']['inner']['follow_bone']='shell_root'
    request_doc['frames']=[{'id':'pose','clip':'cross_beam','time':2.8,'view':'inner'}]
    out=REF/'m3_preview/f45_options';out.mkdir(exist_ok=True)
    request=out/'request.json';request.write_text(json.dumps(request_doc),'utf8')
    ids={g['name']:g['uuid'] for g in doc['groups']};records=[]
    for option in proposals['proposals']:
        candidate=copy.deepcopy(doc);animation=next(a for a in candidate['animations'] if a['name']=='animation.cross_beam')
        for override in option['overrides']:
            key=next(k for k in animation['animators'][ids[override['bone']]]['keyframes'] if k['channel']=='rotation' and abs(k['time']-2.8)<1e-6)
            key['data_points']=[dict(zip('xyz',override['value']))]
        path=out/(option['id']+'.bbmodel');path.write_text(json.dumps(candidate,ensure_ascii=False),'utf8')
        evidence=render(request,out/option['id'],model=path)
        records.append({'id':option['id'],'bbmodel_sha256':evidence['bbmodel_sha256'],'matrix_max_error_vs_pipeline':evidence['matrix_max_error_vs_pipeline']})
    board=Image.new('RGBA',(1500,570),(55,60,70,255));font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',22)
    columns=[('原片 Fourside f045',REF/'frames/MCD_Arch-Illager_Fourside/frame_0045.png'),
        ('E1：向后收肢（主稿，深度推断）',out/'E1_behind/pose.png'),
        ('E2：朝相机侧（候选，深度推断）',out/'E2_front/pose.png')]
    for i,(label,path) in enumerate(columns):
        ImageDraw.Draw(board).text((i*500+8,14),label,font=font,fill='white')
        board.alpha_composite(Image.open(path).convert('RGBA'),(i*500,60))
    board.convert('RGB').save(out/'comparison.png')
    (out/'evidence.json').write_text(json.dumps({'main_bbmodel_sha256':hashlib.sha256(original).hexdigest(),'main_unchanged':True,'options':records},ensure_ascii=False,indent=2)+'\n','utf8')

def main():
    target=REF/'heart_of_ender.bbmodel';original=target.read_bytes();doc=json.loads(original)
    options=json.loads((REF/'m3_motion/shell_b_f015_options.json').read_text('utf8'))
    out=REF/'m3_preview/b_f015_options';out.mkdir(parents=True,exist_ok=True)
    c=options['camera'];view={'position':c['position'],'target':c['target'],'height':c['orthographic_height'],'width':500,'height_px':500}
    request=out/'request.json';request.write_text(json.dumps({'views':{'shell':view},'frames':[{'id':'pose','clip':'idle','time':.6,'view':'shell'}]}),'utf8')
    groups={g['name']:g['uuid'] for g in doc['groups']};records=[]
    for option in options['options']:
        candidate=copy.deepcopy(doc);a=next(a for a in candidate['animations'] if a['name']=='animation.idle')
        for bone,val in option['animation_rotation_replacements'].items():
            k=next(k for k in a['animators'][groups[bone]]['keyframes'] if k['channel']=='rotation' and abs(k['time']-.6)<1e-5)
            k['data_points']=[dict(zip('xyz',val))]
        path=out/(option['id']+'.bbmodel');path.write_text(json.dumps(candidate,ensure_ascii=False),'utf8')
        e=render(request,out/option['id'],model=path)
        records.append({'id':option['id'],'bbmodel_sha256':e['bbmodel_sha256'],'matrix_max_error_vs_pipeline':e['matrix_max_error_vs_pipeline']})
    board=Image.new('RGBA',(1500,980),(55,60,70,255));d=ImageDraw.Draw(board)
    font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',23);small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',17)
    titles=['原片 f015 / 0.60s','主稿：末端位置优先','候选：可见朝向优先']
    paths=[REF/options['source_path'],out/'endpoint_priority/pose.png',out/'visible_axis_priority/pose.png']
    for i,(title,path) in enumerate(zip(titles,paths)):
        im=Image.open(path).convert('RGBA');x=i*500
        d.text((x+12,14),title,font=font,fill='white');board.alpha_composite(im,(x,56))
        crop=im.crop((0,180,200,320)).resize((500,350),Image.Resampling.NEAREST);board.alpha_composite(crop,(x,592))
        d.text((x+10,558),'同一区域放大 2.5×（不移动参考或裁片）',font=small,fill='white')
    d.text((10,951),'固定已验收几何：主稿朝向差约82°；候选末端偏约78px。需审阅烟雾下的肢段归属/连接假设。',font=small,fill=(255,213,157))
    board.convert('RGB').save(out/'comparison.png')
    assert target.read_bytes()==original,'候选流程不得更改主模型'
    (out/'evidence.json').write_text(json.dumps({'main_bbmodel_sha256':hashlib.sha256(original).hexdigest(),'main_unchanged':True,'options':records},ensure_ascii=False,indent=2)+'\n','utf8')
    inner_options(doc,original)
    assert target.read_bytes()==original,'候选流程不得更改主模型'
    print('两种肢体取舍已原生渲染，正式模型逐字节未改变')

if __name__=='__main__':main()
