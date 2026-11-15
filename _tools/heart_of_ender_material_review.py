"""材质修订的原像素并排证据，不在渲染结果上补画效果。"""
from PIL import Image,ImageDraw,ImageFont
from heart_of_ender_blockbench import REF
from heart_of_ender_review_board import fit
P=REF/'m3_material_v2'
FONT=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',22)
SMALL=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',17)

def panel(im):return fit(im.convert('RGBA'),(480,480))
def main():
    board=Image.new('RGBA',(1500,1130),(55,60,70,255));d=ImageDraw.Draw(board)
    d.text((16,10),'M3 材质修订 · 局部渐隐、紫色光晕与嘴腔渐变',font=FONT,fill='white')
    d.text((16,46),'模型为原生编辑器预览：模拟 Java 的 alpha 阈值/背剔除；尚非游戏内截图，没有屏幕 bloom。',font=SMALL,fill=(210,215,225))
    for row,items in enumerate([
        [('原渲染 · 不同姿态',Image.open(REF/'MCD_Heart_of_Ender.png')),('上一版 · idle 0s',Image.open(P/'before/idle_shell.png')),('修订版 · idle 0s',Image.open(P/'preview/idle_shell.png'))],
        [('游戏截图嘴腔 · 局部原像素',Image.open(REF/'Heart_of_Ender_prepare_to_shoot_beams.png').crop((980,110,1220,300))),('上一版 · 张嘴俯视',Image.open(P/'before/mouth_above.png')),('修订版 · 张嘴俯视',Image.open(P/'preview/mouth_above.png'))]
    ]):
        for col,(label,im) in enumerate(items):
            x=col*500;y=85+row*510;d.text((x+12,y),label,font=FONT,fill='white')
            board.alpha_composite(panel(im),(x+10,y+30))
    d.text((16,1110),'渐隐宽度、隐藏内壁的映射为推断；颜色与透明度剖面取自原素材。核心眼牙、骨架和七段动作未改。',font=SMALL,fill=(255,216,173))
    board.convert('RGB').save(P/'comparison.png')
    views=Image.new('RGBA',(1040,1660),(55,60,70,255));d=ImageDraw.Draw(views)
    d.text((16,12),'局部透明 · 正面 / 侧面 / 背面（相同姿态和相机）',font=FONT,fill='white')
    for row,view in enumerate(('front','side','back')):
        for col,folder in enumerate(('before','preview')):
            y=55+row*530;x=col*520;d.text((x+12,y),('旧版' if col==0 else '修订版')+' / '+view,font=FONT,fill='white')
            views.alpha_composite(Image.open(P/folder/f'idle_{view}.png').convert('RGBA'),(x+10,y+30))
    views.convert('RGB').save(P/'views.png')
    (P/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Heart of Ender 材质修订</title>
<style>body{background:#20242a;color:#eee;font:17px system-ui;max-width:1200px;margin:30px auto;padding:0 20px;line-height:1.65}a{color:#d5adff}img{max-width:100%;display:block;margin:16px 0}</style>
<h1>M3 材质修订</h1><p>局部透明渐隐、眼口紫光渐变，以及张嘴后的内部亮核。保持 R2 主体几何和七段动作；新增三张附着的光晕面，仍为21个展示部件。</p>
<p>这是 Blockbench 原生预览，并模拟 alpha 0.1 阈值、背面剔除、普通混合和深度写入。没有实现 Minecraft 的分批排序与方向光，不能冒充游戏实测；没有屏幕 bloom 或紫色投射光。</p>
<p><a href="MATERIAL_V2_REPORT.md">修订报告</a> · <a href="heart_of_ender_material_v2.bbmodel">模型</a> · <a href="REFERENCE_GRADIENTS.md">原图取样</a> · <a href="research/ENGINE_NOTES.md">真实客户端渲染规则</a></p>
<a href="comparison.png"><img src="comparison.png" alt="原图和前后材质对照"></a>
<a href="views.png"><img src="views.png" alt="正侧背材质对照"></a>
<p>44×44 原始遮罩 RGBA 保留；Java 原版单材质没有独立遮罩槽，不声称它已实现原作遮罩着色。原素材版权属于 Mojang；本项目非商业，与 Mojang 无关联。</p>''','utf8')
    print('材质前后、嘴腔与正侧背对照已生成')

if __name__=='__main__':main()
