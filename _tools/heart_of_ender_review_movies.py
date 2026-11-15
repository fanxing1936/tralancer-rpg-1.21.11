"""把原生 PNG 帧打包为 12.5fps GIF；PNG 对照仍是颜色/时点审阅依据。"""
import json
from PIL import Image, ImageDraw, ImageFont
from heart_of_ender_blockbench import REF

def main():
    root=REF/'m3_preview';raw=root/'continuous'
    request=json.loads((REF/'m3_motion/movie_requests.json').read_text('utf8'))
    font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',16)
    grouped={}
    for f in request['frames']:grouped.setdefault(f['clip'],[]).append(f)
    result=[]
    for name,frames in grouped.items():
        if name in ('idle','walk'):frames=frames[:-1]  # 去掉与起点相同的循环端帧，维持原总时长。
        pages=[]
        for f in frames:
            im=Image.open(raw/(f['id']+'.png')).convert('RGBA')
            page=Image.new('RGBA',(500,540),(55,60,70,255));page.alpha_composite(im,(0,40))
            text=f"{name} · {f['time']:.2f}s · {'有动图' if name=='idle' else '外壳推断'}"
            ImageDraw.Draw(page).text((10,9),text,font=font,fill='white')
            pages.append(page.convert('RGB'))
        output=root/(name+'.gif')
        pages[0].save(output,save_all=True,append_images=pages[1:],duration=80,loop=0 if name in ('idle','walk') else 1,disposal=2,optimize=False)
        result.append({'clip':name,'fps':12.5,'frames':len(pages),'path':output.name,'note':'GIF颜色量化仅用于连贯预览，原生PNG为对照事实来源；单次动作预览重复一次'})
    (root/'movies.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf8')
    print('7段动作连续预览已打包')

if __name__=='__main__':main()
