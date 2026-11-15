"""汇总教皇 M3 审阅材料；只读最终模型和实测报告，不冒充游戏验证。"""
import hashlib,html,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

REF=Path(__file__).resolve().parent/'pope_ref';M3=REF/'m3'
LABELS={'idle':'站立','walk':'跑步','attack':'攻击','summon':'环形召唤','cast':'施法','appear':'登场','teleport_in':'瞬移出现','teleport_out':'瞬移离场','whirlwind':'旋风吸入'}
def read(p):return json.loads(p.read_text(encoding='utf-8'))

def main():
    meta=read(M3/'clipmeta.json');model=REF/'pope.bbmodel';digest=hashlib.sha256(model.read_bytes()).hexdigest()
    validation=read(M3/'validation/motion_validation.json')
    render=read(M3/'preview/render_evidence.json')
    assert validation['bbmodel_sha256']==digest and render['bbmodel_sha256']==digest
    assert validation['ok']
    font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',25)
    board=Image.new('RGB',(1800,3*535),(31,38,49));draw=ImageDraw.Draw(board)
    picks={'idle':0.,'walk':.25,'attack':.5,'summon':.45,'cast':.9,'appear':.35,'teleport_in':.25,'teleport_out':.25,'whirlwind':3.35}
    for i,c in enumerate(meta['clips']):
        name=c['name'];x,y=(i%3)*600,(i//3)*535
        pic=Image.open(M3/f'preview/{name}/compare_{picks[name]:05.2f}.jpg').resize((600,345),Image.Resampling.LANCZOS)
        board.paste(pic,(x,y+65));draw.text((x+12,y+16),f"{c['id']}  {name}  ·  {c['length']:.2f}s",font=font,fill='white')
        draw.text((x+12,y+420),LABELS[name]+' / 左原作，右模型',font=font,fill='#cbd5e1')
        note='出手 '+', '.join(f'{t:.2f}s' for t in c['release_times']) if c['release_times'] else ('循环' if c['loop'] else '一次')
        draw.text((x+12,y+460),note,font=font,fill='#ffe5ad')
    board.save(M3/'M3_OVERVIEW.jpg',quality=94)
    lines=['# 教皇 M3 动作审阅','',
      '当前状态：九段动作已保存到 `../pope.bbmodel`，等待用户确认；尚未开始 M4 接入。',
      '',f'模型 SHA-256：`{digest}`。',
      '', '已确认的 B 眼神、44个元素、170个可见面、原贴图图集、17根骨骼及12个item_display部件保持不变。没有在 Blockbench 中做生成脚本无法复现的手改。',
      '', '## 时长与玩法约定', '', '| ID | clip | 时长/秒 | 循环 | 出手/秒 | 依据 |','|---|---|---:|---|---|---|']
    for c in meta['clips']:
        lines.append(f"| {c['id']} | {c['name']} | {c['length']:.2f} | {'是' if c['loop'] else '否'} | {', '.join(f'{t:.2f}' for t in c['release_times']) or '—'} | {c['evidence']} |")
    lines+=['','attack/summon/cast的出手时刻分别约定为0.50/0.65/0.90秒，用于玩法侧同步。它们对应前压到位、转身横扫、举杖悬浮稳定段；GIF没有弹丸/召唤实体出生事件，不能把这些值当作从原游戏提取的事件时间。attack只制作原GIF的一次前压，三连能量弹仍由玩法侧控制。',
      '', '## 逐段对照与必要适配', '',
      '- idle：参考4.00秒周期，轻微身体起伏、杖顶旋转；原作发光颜色变化没有制作，固定原贴图。',
      '- walk：接口名保持walk，来源为Run；1.80秒内四轮步态，持杖在胸前。负X的后摆使披布向+Z背后抬起；侧面/背面图可复核。',
      '- attack：先抬杖并换握，再一次前压，腿向袍后收起；皇冠有反向俯仰补偿，手/杖位置按原帧可见点重建。初稿的杖顶曾低于地面，最终重选未被单视图确定的深度解，并在快速前摆段用5ms数值关键帧保持父子补偿、微调手腕弧线。1ms与局部细化复核得到顶块中心最低约+0.079019格；0.50秒约+0.094435格。该帧二维锚点最大误差约10.84px（原500px画布），未用玩法补丁或socket偏移掩盖。这里只证明挂点中心高度，顶块棱角和游戏客户端插值尚待M4验证。',
      '- summon：保留完整负向转身横扫、前压与回收；yaw累计越过−360°，没有用最短角往返替代转圈。',
      '- cast：中段发光方块独立离开托盘上浮，不把整根权杖一起抬到同样高度。',
      '- 袍摆限制：原作布面会弯曲，当前body与cape是刚性部件，只能复现整体摆向；施法等姿态可见独立后布与主体袍侧的分片，未声称已复刻布料形变。',
      '- appear：只取原GIF前0..1.80秒，到站姿结束；原GIF后面的再举杖/离场和透明尾帧未并入。',
      '- teleport_in：共享短GIF的0..1.20秒映射为0.90秒。teleport_out：使用其真实离场段1.20..2.12秒映射为0.90秒，连续转身收腿，并非倒放出现。',
      '- appear和两段teleport：管线没有scale/alpha，完整体型的转身、升降和收腿可重建；原作从微小体积出现/缩到透明的效果没有制作。当前动画自身不会隐藏模型，不能称为完整隐现复刻。',
      '- whirlwind：人物绕杖翻滚、杖脱手后上移、皇冠约2.70秒附近漂离后继续漂动。0..6.40秒依据游戏GIF；6.40..7.00秒所有12个刚性部件的包围盒中心收拢到模型坐标[0,12,0]，属于项目推断。体积不会缩为零，仍能看到重叠部件；最终移除/换形由玩法负责。',
      '', '## 还原证据的边界', '',
      '关键姿态先取原GIF帧号与累计时间，再制作数值轨道，最后在Blockbench原生WebGL渲染。逐段固定相机；原图保持纵横比，没有按每一帧重新居中或拉伸。三段技能的机位由原图首帧六个头盒角点拟合；转场机位、深度和遮挡部位的角度是重建候选。二维标点与拟合残差见 `motion_attack_cast/`、`action_fit_report.json`、`motion_transition/`。这些是单视图约束，不能唯一恢复原游戏三维骨骼。',
      '', '每段 `preview/<clip>/keyposes.jpg` 给出同一时刻原图/模型；`three_views.jpg` 包含参考视角、侧面和背面。GIF/MP4是原生模型动态并排，没有添加旋风、能量弹、透明或发光后期。审阅视频无声，并额外保留clip末帧50ms，因此媒体时长比上表多50ms；不是游戏内录像。',
      '', '## 挂点与声音', '',
      '`../sockets.json` 从保存后的bbmodel和共享posed_matrix计算，包含idle及所有审阅时刻，明确标出三段出手采样；提供Java模型坐标、缩放后的局部格坐标及Minecraft ^左 ^上 ^前坐标。staff_tip定义为发光顶块几何中心，cast浮升时跟随顶块；head_top为头本体顶部，不是皇冠尖。',
      '', '`audio_cues.json`包含17组39个原名OGG以及sounds/cues/enter_cues配置。出手音效按本项目约定帧绑定，未声称原GIF自带同步音轨。intro三段、撞击、笑声等只注册，没有自动触发。原whirlwind音频约13秒、mirror_in约3.315秒、mirror_out约2.201秒，长于对应clip；没有裁剪/变速或私加stopsound，尾音需在M4接入时注明。',
      '', '## 验证和交接', '',
      '通过：已确认M2静态语义哈希不变、九段名称和顺序、时长与循环、仅数字rotation/position、12部件坐标限制、全轨道有限矩阵、idle/walk闭环、whirlwind末帧12中心汇聚。从磁盘完整重开bbmodel后，几何/图集与全部数值轨道再次导出一致。原生Blockbench各审阅帧世界矩阵与display_mob计算一致，详见preview/render_evidence.json。',
      '', '制作中修复：Blockbench将极小数转成1e-7字符串后会被其Molang解析误读；动作值统一保留6位小数，并将绝对值小于1e-6置0，验证器拒绝e/E数值字符串。未改display_mob.py。历史失败日志以resolved_scientific_notation命名保留，当前模型已经重验。',
      '', '**未在真实游戏内看过。** 本阶段未运行rp_build.sh/build.sh/rp_validate.py/server_test.py，没有同步测试实例，也没有接入或改动玩法。构建与实体清理验证属于用户确认M3后的M4。',
      '', '后续build.sh顺序按用户更新：add_tower_wraith.py → add_pope_model.py → add_pope_fight.py；rp_build.sh放在add_tower_guard.py之后。本阶段未触碰共享构建文件。',
      '', '复现入口：先pope_transition_poses.py与pope_fit_actions.py生成已标注候选，pope_animate.py --replace-authored经Blockbench导出，再pope_motion_preview.py及其--movies生成审阅；数值验证、挂点与本报告使用各自pope专用脚本。已有用户手改时禁止盲目重建。', '']
    (M3/'M3_REVIEW.md').write_text('\n'.join(lines),encoding='utf-8')
    rows=[]
    for c in meta['clips']:
        n=c['name'];rows.append(f'''<article id="{n}"><h2>{c['id']} · {n} — {LABELS[n]} · {c['length']:.2f} 秒</h2>
        <p>{html.escape(c['evidence'])}。出手：{', '.join(f'{t:.2f}秒' for t in c['release_times']) or '—'}</p>
        <video controls loop muted preload="metadata" poster="preview/{n}/compare_{picks[n]:05.2f}.jpg" src="preview/{n}/{n}_comparison.mp4"></video>
        <details><summary>全部关键帧并排</summary><img loading="lazy" src="preview/{n}/keyposes.jpg"></details>
        <details><summary>参考视角 / 侧面 / 背面</summary><img loading="lazy" src="preview/{n}/three_views.jpg"></details></article>''')
    page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>教皇 M3 动作审阅</title>
    <style>body{margin:0;background:#141d2b;color:#e9edf4;font:16px/1.7 system-ui,"Microsoft YaHei"}main{max-width:1220px;margin:auto;padding:30px}h1{font-size:34px}h2{font-size:24px}a{color:#9ed1ff}nav{display:flex;gap:18px;flex-wrap:wrap;position:sticky;top:0;background:#141d2b;padding:14px 0;z-index:2}article{margin:30px 0;border-top:1px solid #445064;padding:20px 0}video,img{display:block;width:100%;height:auto}summary{cursor:pointer;padding:12px;background:#263348;margin:12px 0}.notice{padding:18px;background:#39402c;border-left:5px solid #e0b553}</style><main>
    <h1>教皇 · M3 动作审阅</h1><p>已保留 B 眼神与确认的静态模型。左侧原作 / Mojang，右侧 Blockbench 模型。未在真实游戏内看过。</p>
    <div class="notice">当前停在 M3，等待用户确认。原作瞬移缩放/透明没有制作；旋风末尾0.6秒收拢是推断，部件体积没有消失。动态颜色与特效未制作。</div>
    <nav>'''+''.join(f'<a href="#{n}">{n}</a>' for n in LABELS)+'''</nav>
    <p><a href="M3_REVIEW.md">完整报告</a> · <a href="../sockets.json">挂点</a> · <a href="clipmeta.json">时长/出手/帧映射</a> · <a href="audio_cues.json">音效时刻</a></p>
    <img src="M3_OVERVIEW.jpg" alt="九段关键姿态总览">'''+''.join(rows)+'''<p>原作素材版权属于 Mojang。本项目为非商业同人，与 Mojang 无关联。详见 <a href="../SOURCES.md">SOURCES.md</a>。</p></main></html>'''
    (M3/'index.html').write_text(page,encoding='utf-8')
    print('M3报告/总览/审阅页已生成')

if __name__=='__main__':main()
