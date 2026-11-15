"""七段动作审阅总览；各姿态原生PNG在对应子目录。"""
from PIL import Image,ImageDraw,ImageFont
from heart_of_ender_blockbench import REF
from heart_of_ender_review_board import fit

def main():
    rows=[('idle 待机 · 有动图','frames/MCD_Heart_of_Ender_Idle/frame_0065.png','idle/idle_f000.png','idle/idle_f065.png','0.00s','2.60s'),
        ('walk 爬行 · 外壳推断','Heart_of_ender_crawling_with_decal_trail.png','walk/walk_00.00.png','walk/walk_01.00.png','0.00s','1.00s'),
        ('mortar 后仰吐息 · 推断','Minecraft-dungeons-heart-of-ender.jpg','mortar/mortar_00.40.png','mortar/mortar_01.20.png','0.40s','1.20s'),
        ('cross_beam 抬身 · 外壳推断','Heart_of_Ender_prepare_to_shoot_beams.png','cross_beam/cross_beam_00.50.png','cross_beam/cross_near_front.png','0.50s','2.00s（近正面）'),
        ('sink 沉地 · 推断','Heart_of_Ender_in_game.png','sink/sink_00.40.png','sink/sink_01.70.png','0.40s','1.70s'),
        ('rise 升起 · 推断','Heart_of_Ender_in_game.png','rise/rise_00.20.png','rise/rise_01.90.png','0.20s','1.90s'),
        ('death 死亡 · 推断','Hero_kills_Heart_of_Ender_Arch-Illager_disappear.jpg','death/death_00.00.png','death/death_03.80.png','0.00s','3.80s')]
    out=REF/'m3_preview';canvas=Image.new('RGBA',(900,70+len(rows)*340),(55,60,70,255));d=ImageDraw.Draw(canvas)
    big=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',27);small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',18)
    d.text((15,10),'M3 动作总览 · R2 / 紫色材质',font=big,fill='white')
    d.text((15,45),'左列是依据素材；逐同帧对照、完整正侧背见审阅页。',font=small,fill=(210,215,225))
    for i,(label,source,a,b,ta,tb) in enumerate(rows):
        y=70+i*340;d.text((12,y+4),label,font=small,fill='white')
        for col,(p,caption) in enumerate([(REF/source,'依据素材'),(out/a,'模型 '+ta),(out/b,'模型 '+tb)]):
            canvas.alpha_composite(fit(Image.open(p),(290,280)),(5+col*300,y+32))
            d.text((12+col*300,y+312),caption,font=small,fill='white')
    canvas.convert('RGB').save(out/'overview.png')
    print('七段动作总览已生成')

if __name__=='__main__':main()
