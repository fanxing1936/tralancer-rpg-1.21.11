"""Re-render all 254 registered poses using the final model and actual mask tints."""
from pathlib import Path
import hashlib, html
import heart_of_ender_m3_review as review

review.MODEL = review.REF/'heart_of_ender.bbmodel'
review.OUT = review.REF/'final_material/motion_review'
review.EXPECTED = hashlib.sha256(review.MODEL.read_bytes()).hexdigest()
review.GENERATOR = Path(__file__).name

def html_index(boards,evidence,output):
    figures=''.join('<figure><figcaption>'+html.escape(b['title'])+'</figcaption><a href="'+b['file']+'"><img loading="lazy" src="'+b['file']+'"></a></figure>' for b in boards)
    text='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>末影之心最终动作对照</title>
<style>body{background:#20242a;color:#eee;font:17px system-ui;max-width:1120px;margin:28px auto;padding:0 20px;line-height:1.6}a{color:#dab8ff}img{max-width:100%;display:block;margin:12px 0}figure{margin:34px 0}code{word-break:break-all}</style>
<h1>末影之心 · 最终模型动作对照</h1><p>以下图像从当前保存的模型重新计算，包含已恢复的粗眉与眼白，以及原44×44遮罩的局部紫色染色。离线CPU预览，非游戏截图；不包含bloom。推断动作的左列是依据截图，不冒充同帧原作动画。</p>
<p>模型SHA：<code>'''+review.EXPECTED+'''</code></p><p><a href="MOTION_REVIEW_REPORT.md">说明</a> · <a href="../../heart_of_ender.bbmodel">模型</a> · <a href="render_evidence.json">逐帧证据</a></p><img src="overview.png" alt="七动作总览">'''+figures+'</html>'
    output.write('index.html',text.encode('utf8'))

def report(evidence,boards,output):
    text=f'''# 末影之心最终模型动作对照

模型 SHA-256：`{review.EXPECTED}`。254 个姿态、{len(boards)} 页对照；21 个展示部件、51 个元素、26 个骨骼、7 段动作与 3401 个关键帧。

包含正面、侧面、背面及四分之三视角，77 个小人近景涵盖 Docile 12 姿态、Anxious 15 姿态与 Fourside 50 个源帧。全部图像重新读取当前 bbmodel 和内嵌图集，不使用旧PNG改色。

- idle：外壳有16秒动图；Docile有动图，16秒嵌入3周期，速度为原作90%。
- walk：外壳依据爬行截图和攻击间隙爬行文字推断；Anxious有8秒动图，原速。
- cross_beam：外壳抬身为截图与页面文字推断；Fourside有动图，第1–3秒按25fps源50帧复现。
- mortar、sink、rise、death：依据截图与文字推断，逐图标注，没有特效。

精确源文件/源时刻和模型时刻见 [review_index.json](review_index.json)。既有动作研究见 [M3报告](../../M3_REPORT.md)。关键姿态与相机不因本次材质调整而重新拟合。

此次新增眉眼为原64贴图分片UV重建；静态UV不能还原动图全部瞳孔变化。冠根与Fourside45帧既有轮廓残差、单骨肢体与隐藏深度的推断仍保留，不能以程序验证代替视觉判断。

原44遮罩RGBA未改，两个嘴腔平面以原白色区UV和参考图采样紫色作运行时乘色；alpha按原值混合。相同染色参与本组离线图。嘴腔映射仍是实现推断，没有屏幕bloom或动态照亮方块。

CPU正交预览采用最近邻采样、原色全亮、面中心排序、alpha0.1剔除和普通透明混合，不等同Minecraft真实透明批次/方向光/客户端插值。真实服务端、Blockbench原生读写、资源包验证结果在最终交付报告分别记录，不混为视觉验收。

原素材版权归Mojang；本项目非商业，与Mojang无关联。来源见 [SOURCES.md](../../SOURCES.md)。
'''
    output.write('MOTION_REVIEW_REPORT.md',text.encode('utf8'))

review.html_index=html_index
review.report=report

if __name__=='__main__':review.main()
