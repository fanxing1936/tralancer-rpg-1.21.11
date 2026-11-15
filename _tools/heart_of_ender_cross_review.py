"""仅生成 cross 抬肢候选和原生审阅图；不改变正式模型。"""
import copy
import hashlib
import json
from heart_of_ender_blockbench import REF
from heart_of_ender_geo import uid
from heart_of_ender_motion_preview import render

def main():
    original=(REF/'heart_of_ender.bbmodel').read_bytes()
    doc=json.loads(original)
    study=json.loads((REF/'m3_motion/shell_cross_open_options.json').read_text('utf8'))
    out=REF/'m3_preview/cross_options';out.mkdir(parents=True,exist_ok=True)
    views=json.loads((REF/'m3_motion/review_requests.json').read_text('utf8'))['views']
    camera=study['centered_C1_review_camera']
    views['near_front']={'position':camera['position'],'target':camera['target'],'height':camera['orthographic_height'],'width':500,'height_px':500,'ground_y':-4.663810}
    frames=[{'id':v,'clip':'cross_beam','time':2,'view':v} for v in ('overview','front','side','back','near_front')]
    frames += [{'id':f'transition_{i}','clip':'cross_beam','time':t,'view':'near_front'} for i,t in enumerate((0,.25,.5,.75,1,2.5,3,3.25,3.5,3.75,4))]
    request=out/'request.json';request.write_text(json.dumps({'views':views,'frames':frames}),'utf8')
    groups={g['name']:g['uuid'] for g in doc['groups']}
    for option in study['options'][:1]:
        candidate=copy.deepcopy(doc)
        anim=next(a for a in candidate['animations'] if a['name']=='animation.cross_beam')
        # Replace shell tracks only; retain the complete current inner performance.
        for track in option['clip']['tracks']:
            name=track['bone'];gid=groups[name]
            item=anim['animators'].setdefault(gid,{'name':name,'type':'bone','keyframes':[]})
            item['keyframes']=[k for k in item['keyframes'] if k['channel']!=track['channel']]
            for i,key in enumerate(track['keyframes']):
                item['keyframes'].append({'uuid':uid('cross_review/'+name+'/'+track['channel']+'/'+str(i)),
                    'channel':track['channel'],'time':key['time'],'color':-1,'interpolation':'linear',
                    'data_points':[dict(zip('xyz',key['value']))]})
        path=out/(option['id']+'.bbmodel');path.write_text(json.dumps(candidate,ensure_ascii=False),'utf8')
        evidence=render(request,out/option['id'],model=path)
        print(option['id'],evidence['bbmodel_sha256'])
    assert (REF/'heart_of_ender.bbmodel').read_bytes()==original
    (out/'main_source.json').write_text(json.dumps({'sha256':hashlib.sha256(original).hexdigest(),'unchanged':True}),'utf8')

if __name__=='__main__':main()
