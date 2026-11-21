# -*- coding: utf-8 -*-
"""图鉴第 VIII 节「生物图鉴」：七宗罪领主、所罗门罪仆、圣卫、五场 Boss 战、友军与实装记录。

    emit_guide.py 调用 section()，CSS 并进页头。

数值与设计稿（docs/POPE-DESIGN.md、LUCIFER-*.md、USURPER-DESIGN.md、JACQUES-*.md、DUNGEONS-MODELS.md）
保持一致；改了生成器里的数值，这里也要跟着改。截图在 jacques_boss_ref/guide/，图标取生成器的原件。
"""
import base64
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))

CSS = """
/* ---- bestiary (VIII) ---- */
.shots{display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:1px; background:var(--rule); border:1px solid var(--rule); margin:18px 0 0}
.shots figure{margin:0; background:var(--sunk)}
.shots img{display:block; width:100%; height:auto}
.shots figcaption{padding:8px 12px; font-size:12.5px; color:var(--muted); line-height:1.6}
.shots.wide{grid-template-columns:1fr}
.debug-lord .inner{padding:4px 18px 18px; border-top:1px solid var(--rule); font-size:14px; color:var(--muted)}
.debug-lord .inner h4{margin:18px 0 6px; font-size:14px; color:var(--ink); font-weight:700; letter-spacing:.02em}
.debug-lord .inner p{margin:6px 0}
.debug-lord .inner ul{margin:6px 0; padding-left:1.25em}
.debug-lord .inner li{margin:3px 0}
.debug-lord .inner .tw{border:1px solid var(--rule); margin:8px 0}
.debug-lord .inner table{min-width:560px; font-size:13.5px}
.models{display:grid; grid-template-columns:repeat(auto-fill,minmax(150px,1fr)); gap:8px; margin:14px 0 0}
.models figure{margin:0; border:1px solid var(--rule); background:radial-gradient(circle at 50% 38%, #2A2420 0%, var(--sunk) 72%); display:flex; flex-direction:column; align-items:center; padding:14px 10px 10px}
.models img{display:block; height:150px; width:auto; max-width:100%; object-fit:contain; image-rendering:auto}
.models figcaption{margin-top:8px; text-align:center; font-size:13px; color:var(--ink); line-height:1.45}
.models figcaption span{display:block; font-size:11px; color:var(--muted); font-family:"JetBrains Mono",monospace}
.oath-icon{width:64px; height:64px; image-rendering:pixelated; background:var(--sunk); border:1px solid var(--rule); padding:8px; box-sizing:content-box; float:left; margin:2px 16px 8px 0}
"""


def _uri(rel, mime):
    with open(os.path.join(HERE, rel), "rb") as fh:
        return "data:%s;base64,%s" % (mime, base64.b64encode(fh.read()).decode())


def _shot(name, cap):
    return ('<figure><img loading="lazy" src="%s" alt="%s"><figcaption>%s</figcaption></figure>'
            % (_uri("jacques_boss_ref/guide/%s.jpg" % name, "image/jpeg"), cap, cap))


def _models(items):
    """items: (render key, name, note). Renders: guide_renders/render_models.js (Blockbench) then guide_renders/make_web.py."""
    cells = []
    for key, name, note in items:
        cells.append('<figure><img loading="lazy" src="%s" alt="%s"><figcaption>%s<span>%s</span></figcaption></figure>'
                     % (_uri("guide_renders/web/%s.webp" % key, "image/webp"), name, name, note))
    return '<div class="models">%s</div>' % "".join(cells)


def _table(head, rows, boss_first=False):
    h = "".join("<th>%s</th>" % c for c in head)
    body = []
    for i, r in enumerate(rows):
        cls = ' class="boss"' if boss_first and i == 0 else ""
        body.append("<tr%s>%s</tr>" % (cls, "".join("<td>%s</td>" % c for c in r)))
    return '<div class="tw"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (h, "".join(body))


def _fold(title, meta, inner):
    return ('<details class="debug-lord"><summary><b>%s</b><span>%s</span></summary><div class="inner">%s</div></details>'
            % (title, meta, inner))


def _h(text, right=""):
    r = '<span class="rolls">%s</span>' % right if right else ""
    return '<h3 class="sub-h">%s%s</h3>' % (text, r)


# --------------------------------------------------------------------------- 领主与罪仆

LORDS = [
    ("1", "路西法", "傲慢", "Mossy Skeleton + Root Rot Armor，手持蛇矛",
     "单阶段「晨星之蛇」：普攻刺，原罪、蛇矛、高踞、失坠、王座回绝，罪约万蛇加冕。三角网格已还原成矩形面（不再「毛躁」）"),
    ("2", "利维坦", "嫉妒", "Skeleton Necromancer（死灵法师）",
     "身高调成骷髅大小（2 格）；杖头宝石按青色取发光"),
    ("3", "亚巴顿", "怠惰", "Wretched Wraith（悲惨幽魂）",
     "原作没有动作展示，借幽魂罪仆（Tower Wraith）的动作；双手垂挂"),
    ("4", "别西卜", "暴食", "Nameless One（无名之王）",
     "骷髅大小；两只蓝色发光眼；杖头三层套方块光球（原作是粒子，按旧版补成模型）；常驻可见"),
    ("5", "萨麦尔", "暴怒", "Redstone Monstrosity（红石巨怪）",
     "射击、冲撞重击、砸地、熔岩重击、苏醒全是原作动作"),
    ("6", "贝利尔", "色欲", "Corrupted Cauldron（腐化坩埚）",
     "药水换成 16×16、8 帧的发光旋涡贴图；原作不会走，自制「颠步」"),
    ("7", "玛门", "贪婪", "Piglin Merchant（猪灵商人）",
     "行走和投掷借猪灵动作；自制「聚金砸地」；友方 NPC 原作朝 +z，整体转 180°"),
]

SERVANTS = [
    ("路西法", "Mossy Skeleton（苔藓骷髅）", "巴力", "阿加雷斯", "瓦沙克", "萨米基纳", "马尔巴士"),
    ("利维坦", "Sunken Skeleton（沉没骷髅）", "华利弗", "亚蒙", "巴巴托斯", "派蒙", "布耶尔"),
    ("亚巴顿", "Tower Wraith（高塔幽魂）", "古辛", "西迪", "贝雷特", "列拉金", "艾利欧格"),
    ("别西卜", "Skeleton Vanguard（骷髅先锋）", "桀派", "布提斯", "巴钦", "塞列欧斯", "布松"),
    ("萨麦尔", "Mountaineer 红色变体（登山者）", "莫拉格斯", "因波斯", "艾姆", "纳贝流士", "格拉夏·拉波拉斯"),
    ("贝利尔", "Witch（女巫）", "布涅", "罗诺比", "比利士", "亚斯塔禄", "佛纽司"),
    ("玛门", "Piglin 近战变体（猪灵）", "佛拉斯", "阿斯摩太", "盖布", "佛尔佛尔", "马可西亚斯"),
]


def lords_html():
    p = [_h("七宗罪领主 · rpg:taint/lord1～7", "生命 700 · 降临十分钟")]
    p.append("<p>签了七罪契约的人魔化走完、堕落之后，柱上的领主从他身上挣出来降临。领主走驱魔系统：镇压、真名调查、捆绑；"
             "十分钟没被驱逐就自行消散。外观都换成了从《Minecraft Dungeons》本体提取的原作模型、动作和音效（2026-11-12 起默认）。</p>")
    p.append(_table(["柱", "领主", "罪", "原作外观", "说明"],
                    [(n, "<span class=\"nm\">%s</span>" % a, b, c, d) for n, a, b, c, d in LORDS]))
    p.append(_models([("lucifer", "路西法", "Mossy Skeleton"), ("leviathan", "利维坦", "Necromancer"),
                      ("abaddon", "亚巴顿", "Wretched Wraith"), ("beelzebub", "别西卜", "Nameless One"),
                      ("samael_lord", "萨麦尔", "Redstone Monstrosity"), ("belial_lord", "贝利尔", "Corrupted Cauldron"),
                      ("mammon_lord", "玛门", "Piglin Merchant")]))
    p.append(_h("所罗门罪仆 · rpg:minion", "35 名 · 五职"))
    p.append("<p>七十二柱里的 35 位魔神，每柱五职。罪仆可以独立、永久存活；死亡时掉<b>柱页</b>（12%）与<b>柱印</b>（4%），"
             "集齐五职柱页可以合成契约书，柱印镶进书里成为从契。手里画的是载体自己的原版武器，不是建模武器。</p>")
    p.append(_table(["柱", "原作外观", "先锋 · 92", "猎手 · 66", "司祭 · 76", "咒使 · 70", "处刑者 · 108"],
                    [("<span class=\"nm\">%s</span>" % r[0],) + r[1:] for r in SERVANTS]))
    p.append(_models([("lucifer_servant", "路西法的罪仆", "Mossy Skeleton"), ("sunken_skeleton", "利维坦的罪仆", "Sunken Skeleton"),
                      ("tower_wraith", "亚巴顿的罪仆", "Tower Wraith"), ("vanguard", "别西卜的罪仆", "Skeleton Vanguard"),
                      ("samael_servant", "萨麦尔的罪仆", "Mountaineer"), ("belial_servant", "贝利尔的罪仆", "Witch"),
                      ("mammon_servant", "玛门的罪仆", "Piglin")]))
    p.append('<div class="note"><b>职业与载体：</b>先锋、处刑者是卫道士，猎手是掠夺者，司祭是唤魔者。咒使原本是幻术师，'
             '但幻术师隐身时仍会画出本体和分身、无法换装，所以第二到第七柱的咒使都改成了掠夺者（会射击）。'
             '路西法的罪仆只有弓的动作，近战职业用手工补的挥臂动作。</div>')
    return "".join(p)


def guards_html():
    p = [_h("圣卫 · 教皇直属的军团", "三种 · 标签 rpg.hg")]
    p.append("<p>教廷的兵，敌对：主角最后要反抗的就是教皇。三种圣卫都由 <code>rpg:holy_guard/summon</code> 随机召出，"
             "教皇战的圣卫波次、篡夺者的「授权」和雅克的「圣殿号角」都走这一个入口。</p>")
    p.append(_table(["种类", "生命", "原作外观", "打法"], [
        ('<span class="nm">塔卫</span><span class="sm">rpg.tg</span>', "120",
         "Royal Guard 身体 + Tower Guard 蓝图上的头盔、护甲、长矛、盾",
         "持盾挡正面投射物；直线冲锋，撞墙眩晕 1.5 秒、护甲归零；累计 6 次受击破盾（背后一次算 3 次）。<b>引它撞墙，或绕后破盾</b>"),
        ('<span class="nm">重盾</span><span class="sm">rpg.rg</span>', "160", "Royal Guard（皇家卫兵）",
         "大盾退回正面伤害的 70%、弹开投射物；锤击砸地后放下盾喘息。<b>绕后或等它喘息</b>"),
        ('<span class="nm">术士</span><span class="sm">rpg.ei</span>', "70", "End Illager（终末灾厄村民）：唤魔者网格，褐袍无兜帽",
         "保持距离发射圣光弹，被贴近就闪走，并给其他圣卫回血。<b>优先击杀</b>"),
    ]))
    p.append(_models([("tower_guard", "塔卫", "Royal Guard + Tower Guard"), ("royal_guard", "重盾", "Royal Guard"),
                      ("end_illager", "术士", "End Illager")]))
    p.append('<div class="note"><b>终末灾厄村民没有原作模型：</b>它只出现在「回响虚空」的预渲染片尾里，扫遍 354 张角色贴图也没有。'
             '开发者说它像唤魔者，所以用唤魔者的网格配褐色长袍。</div>')
    return "".join(p)


# --------------------------------------------------------------------------- Boss 战

def overview_html():
    p = [_h("指令召唤的 Boss 战", "战场半径 40 · 每段 1000 血")]
    p.append("<p>六场 Boss 战都只用指令开战，在执行位置展开，没有开启流程和掉落（雅克除外，见下）。共同的规格：</p>")
    p.append('<div class="sys">'
             '<div><h3>血量</h3><p>原版卫道士最大生命上限 1024，所以每段一池 1000，切段补满、切段时无敌。'
             '副手藏一件隐形的死亡保护物品：致命一击被它吃掉，不会真死、也不会一刀跨段。</p></div>'
             '<div><h3>出招</h3><p>普攻间隔约 8～10 刻，每三次普攻接一招；大招按血线触发，到线前时钟走完（一段 45 秒、二段 60 秒）也会放。'
             '大招后有破绽：护甲归零、不出手。</p></div>'
             '<div><h3>呈现</h3><p>专用位图血条（原版条隐藏），每 50 血一档，中央饰物按阶段换，花体英文标题。'
             '播报〖名字〗加粗，阶段切换、大招和结算带哥特体小注。</p></div>'
             '<div><h3>音乐与重置</h3><p>Boss 音乐走<b>唱片机</b>音量（不少人把音乐音量关到 0），放完循环。教皇之外每个 Boss、每一段都有自己的曲子（OpenGameArt 上的 CC0 / CC-BY 曲目，作者与许可见仓库 <code>_tools/bgm_ref/SOURCES.md</code>）。'
             '全员阵亡，或全员离开 40 格满 60 秒，就清场重置。</p></div>'
             '</div>')
    p.append(_table(["Boss", "阶段 · 生命", "原作外观", "音乐", "开战"], [
        ('<span class="nm">教皇</span>', "圣卫战（4 × 120）→ 教皇 1000 → 末影之心 1000", "Arch-Illager；末影之心、末影面容为手工模型",
         "boss3 → boss2 → boss1", "<code>rpg:pope_fight/summon</code>"),
        ('<span class="nm">路西法</span><span class="sm">最终 Boss</span>', "晨星之蛇 1000 → 知善恶树 1000 →（古龙，未做）",
         "Mossy Skeleton + Root Rot Armor → Jungle Abomination", "Ancient Power Of Serpents → Dark Shrine Loop", "<code>rpg:lucifer_boss/summon</code>"),
        ('<span class="nm">篡夺者</span><span class="sm">达里奥·所罗门</span>', "所罗门之裔 1000 → 篡夺圣灵 1000",
         "Enchanter → Prime Enchanter（白金重着色 + 原作王冠）", "Boss Battle Theme → It's our battle", "<code>rpg:usurper_boss/summon</code>"),
        ('<span class="nm">圣殿大团长雅克</span>', "圣殿之誓 1000 → 火刑柱 1000",
         "英雄网格 + 赫克斯皮肤 + 冠军铠甲 + 英雄披风", "War Theme → War Theme（ver 2）", "<code>rpg:jacques_boss/summon</code>"),
        ('<span class="nm">疯人王扫罗</span>', "十字军大元帅 1000 → 甲碎 → 疯人王 1000",
         "英雄网格 + 织网者皮肤 + 坚毅铠甲，千刀", "Delusion → Red Curtain", "<code>rpg:saul_boss/summon</code>"),
        ('<span class="nm">天使长米迦勒</span>', "天使长·谁似神 1200 → 骨中之骨 → 炽天使 1200",
         "半透明灵体：英雄网格 + 云端守望者皮肤 + 霜冻铠甲 + 六翼；守望者（Watchling）", "Rise of Spirit → The Final Battle", "<code>rpg:michael_boss/summon</code>"),
    ]))
    p.append('<div class="note"><b>谁能被契约打到：</b>教皇本人、篡夺者、雅克都是人，不带 <code>rpg.demon</code>，七罪契约技能打不到；'
             '末影之心和路西法带着，契约照常生效。新约技能对末影之心改成固定伤害（新约 120、旧约 100、领域 80、裁决 100，外壳再减 70%）；'
             '对篡夺者同样固定伤害，二阶段再 ×1.25（「力」克制偷来的「权」）；雅克不带 <code>rpg.demon.fly</code>，新约打不到他。</div>')
    return "".join(p)


def pope_html():
    stages = _table(["阶段", "内容"], [
        ("圣卫战", "4 名圣卫（生命 120）降临，教皇只用台词宣告异端。圣卫全灭进入下一段"),
        ("教皇（1000）", "<b>教廷总动员</b>：100/75/50/25% 各召 2 名圣卫，场上最多 4。<b>圣血祭</b>：每 20 秒抽一名部下，读条 2.5 秒回复 60，先杀掉目标就能打断。"
                       "<b>收回契约</b>：每 60 秒压制玩家已签的那一柱 15 秒。<b>加护</b>：11 格内圣卫减伤加速，他一瞬移就断"),
        ("末影之心（1000）", "圣器反噬：教皇被旋风吸进权杖（7 秒），末影之心升起（2.4 秒），教皇困在体内。圣卫全部清场；外壳减伤 70%，十字光束期间体内小人透出、减伤取消"),
    ])
    moves = _table(["招式", "效果", "应对"], [
        ("普攻", "25 格内一发快弹 6；被贴到 3.5 格内且瞬移冷却时杖击 8", "走位"),
        ("三连圣光弹 / 天罚 / 圣环", "扇形三发；脚下与走位方向四枚圣印，1.3 秒后落光柱 12；周身两圈各 8 发光弹，第二圈错半格", "看圣印、侧移"),
        ("瞬移", "被贴进 3 格时消失 0.9 秒，在 13.5 格外出现，落地立刻出手", "—"),
        ("<b>大招 · 七印开启</b>", "七处光环锁定你此刻的位置，1.1 秒后沿细线射出 40 格金光，14", "看到细线就横移"),
        ("<b>大招 · 最后的审判</b>", "回中心铺开 30 格圣印，三处圣所亮起；5.5 秒后全场审判 30", "站进圣所（3.5 格）或跑出 30 格；之后 3.5 秒破绽"),
        ("末影之心 · 普攻", "爬行途中，8 格内咬 8，8～26 格吐虚空碎块 6", "—"),
        ("迫击 / 十字光束 / 虚空震环 / 虚空喷涌 / 面容凝视 / 潜地", "13 发紫弹落点先亮圈；四束光扫 60°；两道紫环扩到 22 格（跳起躲）；七处喷涌逐个推进；三张末影面容光束追你；钻到身边破土",
         "持续走动；跳；贴近本体"),
        ("<b>大招 · 千面降临</b>", "两圈各六张面容，光束一起转，两圈方向相反", "离开圈心，顺着光束转"),
        ("<b>大招 · 虚空坍缩</b>", "黑潮扩到 15 格并减速，5 秒后坍缩 30", "跑出紫圈；之后 3.5 秒外壳打开"),
        ("<b>大招 · 十字灾变</b>", "八束光扫过去再扫回来，缝隙比扫过的角度窄", "贴近本体，或跟着光跑"),
    ])
    impl = ("<ul>"
            "<li>生成器：战斗 <code>add_pope_fight.py</code>（<code>rpg:pope_fight/</code>，分数 <code>rpg_pf</code>），模型 <code>add_pope_model.py</code>（Codex 交付）、"
            "末影之心 <code>add_heart_of_ender.py</code>，特效贴图 <code>add_pope_fx_art.py</code>（Codex 绘制，原图在 <code>pope_fx_ref/raw/</code>）。</li>"
            "<li>末影之心的模型骑在打不到的 Marker 盔甲架上，所以另有一只隐身放大的卫道士（<code>rpg.pf.heart</code>）做判定体，模型每次随它传送；"
            "减伤是每 5 刻读一次血量、退回七成，对所有伤害类型一视同仁（<code>rpg:divine_light</code> 绕过抗性）。</li>"
            "<li>骑乘谓词里<b>绝不能写 <code>nbt</code></b>：它会把载体和全部乘客逐部件逐刻序列化（去掉后 5 ms 降到 1.6 ms）。</li>"
            "<li>原作的 TeleportIn 是消失、TeleportOut 是现身，和名字相反：按事件对调。杖在左手，杖头挂点取出手那一刻宝石的位置。</li>"
            "<li>用户要求（2026-11-05）：文本暗金、对比度高；删掉教皇身后的三重十字；圣卫声音调小；Boss 要有普攻，教皇两个大招、末影之心三个；"
            "末影面容做成一个技能加一个大招；第一、三阶段音乐对调过一次。</li>"
            "<li>末影之心与末影面容保留手工模型：原作星空是屏幕空间材质，直接转换只剩黑色外形。</li>"
            "</ul>")
    return (_h("教皇 · rpg:pope_fight", "三段 · 8～12 分钟")
            + "<p>玩家先打退圣卫，教皇亲自降临并调动整个教廷；教皇倒下时被圣器吞噬，变成末影之心——教廷的圣力早已被污染。"
              "击败后清空在场玩家的魔化值，引《约翰福音》8:32。</p>"
            + _models([("pope", "教皇", "Arch-Illager"), ("heart_of_ender", "末影之心", "手工模型"), ("arch_visage", "末影面容", "手工模型")])
            + stages
            + '<div class="debug-lords" style="margin-top:14px">'
            + _fold("招式与大招", "教皇 6 招 + 2 大招 · 末影之心 7 招 + 3 大招", moves)
            + _fold("实装记录", "生成器 · 判定体 · 性能", impl) + "</div>")


def lucifer_html():
    moves = _table(["阶段", "招式", "效果"], [
        ("蛇", "普攻「刺」与原罪、蛇矛、高踞、失坠、王座回绝", "与七罪领主同一套时间线；原版近战改成 0 伤害，近身伤害只来自「刺」"),
        ("蛇", "<b>蛇之后裔</b>（最终 Boss 独有）", "从根须法阵召 2 名苔藓骷髅罪仆，最多 4 名；满了改放晨星坠落"),
        ("蛇", "<b>晨星坠落</b>（以赛亚书 14:12）", "最多 4 人脚下淡绿预警圈，1.5 秒后落星，3 格内 14"),
        ("蛇", "<b>大招 · 万蛇加冕</b>", "万蛇法阵铺到 20 格，三圈蛇牙同时破土（625 / 375 血）"),
        ("变身", "蛇回到树上（约 5 秒）", "根须法阵、孢子光爆、蛇鳞碎片，载体放大 2.5 倍，接 Jungle Abomination 的登场"),
        ("树", "碾（普攻）、缠枝、禁果、诱惑、坠天、知善恶", "缠枝全部落空 → 花心张开的破绽；知善恶：结算时正在看它的人受伤失明"),
        ("树", "<b>荆棘与蒺藜</b>（创世记 3:18）", "朝最多 4 人各钻出一条原作藤刺线，每刻 0.6 格，8 + 缓慢；侧移"),
        ("树", "<b>火焰的剑</b>（创世记 3:24）", "内外两圈预警 1.5 秒，火焰剑绕树干扫一圈（3～14 格），10 并点燃；贴树干或站到 14 格外"),
        ("树", "<b>大招 · 失乐园</b>", "16 枚果核 + 三圈尖根（3/6/9 格）依次破土（667 / 333 血）"),
    ])
    impl = ("<ul>"
            "<li>两个路西法（2026-11-09 用户定）：七罪领主路西法只有蛇一阶段，走驱魔；最终 Boss 是三阶段，载体 <code>rpg.lub</code>，不带 <code>rpg.advent</code>，"
            "所以不走十分钟寿命和驱魔，也不记罪证。变身只认 <code>rpg.lub</code>。</li>"
            "<li>生成器：<code>add_lucifer_boss.py</code>（<code>rpg:lucifer_boss/</code>，独有四招在 <code>fs/</code>，每三次出招换一次），招式复用 <code>add_lucifer_fight.py</code> 的时间线与特效引擎；"
            "二阶段模型 <code>add_lucifer_p2_model.py</code>（102 个部件、18 段动作），血条 <code>add_lucifer_boss_art.py</code>。</li>"
            "<li>二阶段读血每 4 刻一次：载体上骑着 102 个部件，读一次要全部序列化。2.5 倍时乘客座位从 2.0 升到 5.0 格（无头实测）。</li>"
            "<li>一阶段模型 2026-11-13 改成普通材质：原来的三角网格加核心着色器在游戏里是一片绿、显得「毛躁」。三角面重新配对成矩形面，直接用原 UV，真正斜切的面按 4 倍烘焙。</li>"
            "<li>特效贴图只用 16×16 或 32×32（用户 2026-11-08），由 Codex 按简报绘制。</li>"
            "<li>第三阶段古龙未做：接口预留在 <code>rpg.lu.phase3</code> / <code>P3_AT</code>，模型和命名（路西法还是撒旦）待定。</li>"
            "</ul>")
    return (_h("路西法 · 最终 Boss · rpg:lucifer_boss", "蛇 → 树 → 龙")
            + "<p>路西法就是伊甸园里那条蛇，所以三个形态是「蛇 → 知善恶树 → 古龙」：《启示录》20:2「那龙，就是古蛇，又叫魔鬼，也叫撒但」。"
              "目前做完前两阶段。</p>"
            + _models([("lucifer", "晨星之蛇", "Mossy Skeleton + Root Rot Armor"), ("lucifer_p2", "知善恶树", "Jungle Abomination")])
            + '<div class="debug-lords" style="margin-top:14px">'
            + _fold("招式与大招", "蛇 8 招 · 树 8 招", moves)
            + _fold("实装记录", "两个路西法 · 材质 · 未做的古龙", impl) + "</div>")


def usurper_html():
    moves = _table(["阶段", "招式", "效果与应对"], [
        ("一", "普攻 书页弹 / 书页横扫", "25 格内 6；贴近 3.5 格横扫 8"),
        ("一", "附魔灌注", "对最近的罪仆射光束 6 秒：抗性 II、速度。<b>先杀被灌注的罪仆</b>，光束断开、他硬直 2 秒"),
        ("一", "七十二柱召役", "100/75/50/25% 各召 2 名七柱罪仆，最多 4 名"),
        ("一", "所罗门封印", "脚下六芒星，1.5 秒后闭合 10，并封住契约技能 8 秒"),
        ("一", "契约改写", "对签了七罪契约的人：10 秒内每用一次契约技能，魔化额外 +5"),
        ("一", "<b>大招 · 七十二柱环</b>", "周身七十二枚原作符文按七柱颜色分七段亮起射向圈心；躲进刚射完的那段"),
        ("一", "<b>大招 · 所罗门之钥</b>", "全场大六芒星，4 秒后星心爆开 26；跑到六个尖角的安全圈，之后他跪地 3 秒"),
        ("变身", "篡夺圣灵（约 6 秒）", "白金光柱；签了新约的人身上连出白金光线被抽走一截权柄（只是演出）；书碎、换二阶段模型、头顶落下白金王冠"),
        ("二", "普攻 连拳", "贴身三拳各 6，跃起砸地 10"),
        ("二", "天降 / 圣光突进 / 圣雷砸地", "光柱标记 1.2 秒后砸地 14；直线冲 12 格沿途炸光 8；电环扩到 20 格 10（跳起躲）"),
        ("二", "授权", "召 2 名圣卫，每名和他连一道白金权柄线"),
        ("二", "<b>大招 · 神力超载</b>", "浮空蓄力 6 秒免伤，全场电光；站上升起的 4 座白金圣坛（原作地卜师石柱）"),
        ("二", "<b>大招 · 伪圣审判</b>", "身前依次扫出 5 道 20 格白金光束 16；绕到身后或找缝"),
        ("二", "<b>破绽 · 有权无力</b>", "圣卫在场时他受伤 −50%；圣卫全倒后 6 秒王冠暗下、受伤 +50%；每次大招后也有 4 秒"),
    ])
    impl = ("<ul>"
            "<li>他篡夺的是<b>圣灵</b>（用户更正过「圣子」）。设定：圣灵有权无力，命令要靠圣卫执行，所以圣卫在场时减伤、倒下后露出破绽。</li>"
            "<li>生成器：战斗 <code>add_usurper_boss.py</code>（<code>rpg:usurper_boss/</code>，分数 <code>rpg_ub</code>），一阶段模型 <code>add_usurper_model.py</code>（附魔师 + 补成模型的头顶附魔书），"
            "二阶段模型 <code>add_prime_enchanter_model.py</code>（Codex 交付的 M4，11 段动作），白金重着色与王冠 <code>add_usurper_holy_look.py</code>，特效 <code>add_usurper_fx_art.py</code>。</li>"
            "<li>变身第 72 刻召出首席附魔师、把它的部件挪到篡夺者载体上，挂 <code>rpg.usb.s2</code>；一阶段外观排除这个标签。</li>"
            "<li>减伤 / 增伤每 4 刻按血量差退回或追加。神力超载的圣坛是真的屏障方块，所有出口都跑 <code>altar_clear</code>。</li>"
            "<li>特效素材优先用原作：灵魂图腾符文与法阵圈、唤魔者尖牙、方环冲击波、挥砍弧光、闪电纹理、地卜师石柱、不死图腾、王冠，原作没有的六芒星由 Codex 补画。"
            "一阶段音效是附魔师原声 39 段（minecraft.wiki 下载），二阶段原作没有音频，用原版声音。</li>"
            "<li>2026-11-14 补了专属血条，二阶段模型的肩膀上调过一次。</li>"
            "</ul>")
    return (_h("篡夺者 · 达里奥·所罗门 · rpg:usurper_boss", "两段 · 8～11 分钟")
            + "<p>所罗门王的后裔。一阶段用自己的力量作战，召来七十二柱的罪仆；二阶段篡夺圣灵所持的权柄，化为白金神力的形态。"
              "击败后白金王冠碎裂、权柄归还（签了新约的人权柄补满），引《约翰福音》10:10。</p>"
            + _models([("usurper", "所罗门之裔", "Enchanter"), ("prime_enchanter", "篡夺圣灵", "Prime Enchanter · 白金重着色")])
            + '<div class="debug-lords" style="margin-top:14px">'
            + _fold("招式与大招", "一阶段 7 · 二阶段 7", moves)
            + _fold("实装记录", "生成器 · 变身换模型 · 原作素材", impl) + "</div>")


def jacques_html():
    moves = _table(["阶段", "招式", "效果与应对"], [
        ("一", "普攻 坟墓克星三连", "贴身 4 格：下劈 7、7，第三下 80° 横扫 11；7 格外改弩单发 5，4.5～7 格不出手、走近"),
        ("一", "竖琴连弩", "上弦时弩身按原作四个阶段变形，扇形五连发各 5；侧移进箭缝"),
        ("一", "圣殿冲锋 / 后撤射击", "翻滚贴近起身下劈 10；被贴身时后翻 5 格补一箭 6，落地那刻是破绽"),
        ("一", "圣殿号角", "召 2 名圣卫（三种随机），最多 4 名；满了改连弩"),
        ("一", "<b>大招 · 十字审判</b>", "坟墓克星插地，十字四臂（宽 3、长 20）1.5 秒后炸开 18；站进对角空档，之后 1.5 秒定身"),
        ("一", "<b>大招 · 竖琴之弦</b>", "朝天连射，空中一排排「琴弦」从一端扫到另一端落下，每道 12；看准一格空隙"),
        ("变身", "火刑柱（约 6 秒）", "跪地祈祷，火刑柱升起；大卫的幽灵出现：「你不是第一个推石头的人。」他在火里站起"),
        ("二", "燃刃三连", "同一阶段，横扫留下 3 秒火线"),
        ("二", "火刑跃击", "跃起消失，落点火光 1 秒，落地 14（4 格），留火圈 4 秒"),
        ("二", "燃火连弩", "箭落点各留一小团火"),
        ("二", "莫莱的诅咒", "最近一人打上 8 秒印记，到时以他为中心炸开 12（3 格）；被诅咒的人离开队友"),
        ("二", "<b>大招 · 七座火刑柱</b>", "七根柱围成一圈依次连起火墙，最后整圈向中心收拢 16；找最后连上的缺口冲出去，之后眩晕 3 秒"),
        ("二", "<b>大招 · 最后的冲锋</b>", "三次翻滚冲锋各转向最近的人，最后一记燃火横扫 20；之后喘息 3 秒"),
        ("二", "<b>大卫的投石</b>", "他第一次起手大招时，大卫的幽灵甩出一颗石子，2 秒后命中打断，雅克眩晕 3 秒、护甲归零。石子只有一颗：打断后幽灵在天光里消散，之后的大招要你自己躲"),
    ])
    impl = ("<ul>"
            "<li>生成器：外观 <code>add_jacques_model.py</code>，战斗 <code>add_jacques_boss.py</code>（206 个函数，特效集中在 <code>vfx/</code>），血条 <code>add_jacques_boss_art.py</code>。"
            "载体 <code>rpg.jqb</code>，大卫幽灵 <code>rpg.jqd</code>，分数 <code>rpg_jq</code>。</li>"
            "<li>外观：原作玩家英雄网格（38 根骨、六个护甲插槽）+ 赫克斯皮肤（褐色衣裤改成石板青，和铠甲统一）+ 冠军铠甲第一个独特变体（英雄铠甲）六件 + 英雄披风。"
            "动作全部来自原作玩家动作，共 46 段。</li>"
            "<li>武器：常态只拿坟墓克星，弩招才换竖琴弩，每个出口都换回 <code>weapon/glaive</code>；弩的四个上弦阶段同一时刻只显示一个；<code>charge</code> 动作是 0 帧，永远不要进入。</li>"
            "<li>披风：原作靠物理模拟下垂，这里绕 X 轴转 −90°、后移 26 单位，再绕竖轴转 180°（2026-11-15 修正）：贴图左半是外面（金色徽记）、右半是里衬，第一版装反了。</li>"
            "<li>外观生成器加了 <code>carrier_type</code>：任何带 <code>rpg.jqwear</code> 的实体都会穿上雅克外观，友军就是这样借用的。</li>"
            "<li>特效（2026-11-15「特效有点素」）：天降光柱 <code>light_pillar</code>（粗光束 + 白芯，一秒内收细）、地面光环 <code>ringm</code> / <code>ringx</code>（扩到 6 / 11 格）、快转圣印 <code>spinf</code>、"
            "十字光臂 <code>armfade</code>（停 22 刻），以及外扩粒子环、螺旋火舌、沿线粒子。一阶段金白，二阶段火红。</li>"
            "<li>粒子的 delta 不能用 <code>^</code> 局部坐标（count 0 时是世界轴上的速度），所以横扫弧用静止粒子；去掉了原版 <code>explosion</code> 粒子（游戏里是白色月牙）。</li>"
            "<li>大卫的石子只打断二阶段的第一个大招，随后幽灵消散（<code>david/fade</code>，2026-11-15 用户定）；之后的大招都能完整放完。</li>"
            "</ul>")
    shots = ('<div class="shots">'
             + _shot("intro", "登场：天降光柱 + 红十字圣印")
             + _shot("cross", "十字审判炸开：双层光臂")
             + _shot("harp", "竖琴之弦：一道道金弦落下")
             + _shot("morph", "变身：火刑柱与三道火柱")
             + _shot("walls", "七座火刑柱：三层火墙")
             + _shot("leap", "火刑跃击：落地火浪")
             + "</div>")
    return (_h("圣殿大团长雅克 · rpg:jacques_boss", "两段 · 7～10 分钟")
            + "<p>教皇直属圣殿骑士团的大团长，也是整个教廷里唯一真心信神的人。全战没有阴招，每一招都有清楚的起手和破绽，像一场骑士的决斗。"
              "二阶段他被自己效忠的教廷送上火刑柱，却在火里站着继续战斗；大卫的幽灵站在玩家这边——牧童对歌利亚。"
              "倒下时说「……我守了一辈子的，是谁？」，引《撒母耳记上》17:45；战场里每个人得到一件<b>圣殿誓约</b>。</p>"
            + _models([("jacques", "雅克", "英雄 + 赫克斯 + 英雄铠甲 + 披风"), ("david", "大卫的幽灵", "原作英雄")])
            + '<div class="shots wide">' + _shot("model", "模型核对：赫克斯改色前后、背面、奔跑；下排是竖琴弩上弦的四个阶段（这张拍于披风翻转之前）") + "</div>"
            + shots
            + '<div class="debug-lords" style="margin-top:14px">'
            + _fold("招式与大招", "一阶段 6 · 二阶段 8", moves)
            + _fold("实装记录", "外观 · 武器切换 · 披风 · 特效", impl) + "</div>")


# --------------------------------------------------------------------------- 友军

def ally_html():
    icon = _uri("jacques_ally_ref/oath.png", "image/png")
    p = [_h("友军单位 · 圣殿誓约", "rpg:jacques_ally")]
    p.append('<div class="sys"><div style="grid-column:1/-1"><img class="oath-icon" src="%s" alt="圣殿誓约">'
             '<h3>［传说］圣殿誓约</h3><p class="how">右键吹号 · 冷却 3 分钟 · 击败雅克获得</p>'
             '<p>召来友军雅克，在场 20 秒和你并肩作战。冷却中右键会提示还剩几秒；物品自带原版冷却遮罩。'
             '图标是原作《地下城》风之号角的真实网格和贴图，逐像素换成圣殿配色（象牙白号身、金色吹嘴、圣殿红的箍与背带）后渲染成 32×32。</p></div></div>' % icon)
    p.append(_table(["项", "友军雅克"], [
        ("生命 / 护甲", "100 / 8；致命一击时倒下（原作倒地动作），1.5 秒后消失，倒下期间敌人不再选他"),
        ("招式", "20 格内找最近的敌人；贴身 3.2 格出坟墓克星三连（9、9、横扫 12）；6～22 格偶尔端起竖琴弩，上弦四段后放一道金色弩光 8"),
        ("移动", "每刻 0.3 格，能上一格台阶；没有敌人时跟着召唤者，离开 24 格直接跟上"),
        ("敌我", "不打苦力怕、不打无敌的；玩家误伤会把生命补回去，玩家武器和技能的范围伤害本来就避开他"),
        ("诱饵", "伤害记在他头上，被打的怪会回头打他；代价是他打死的怪不算玩家击杀"),
        ("离场", "到时前 2 秒说「时候到了」，在光柱里离开"),
    ]))
    p.append('<div class="note"><b>他是一个「玩家单位」。</b>原版的僵尸、骷髅、蜘蛛、掠夺者、劫掠兽、史莱姆都会主动攻击铁傀儡，所以载体用隐身、NoAI 的铁傀儡（缩到 0.7407 倍，正好 2 格高）。'
             '数据包里各 Boss 与怪物的技能原本只认 <code>@a</code>，构建最后一步（<code>add_ally_units.py</code>）把敌方模块里的玩家选择器改成「单位」标签：'
             '<code>rpg.unit</code>（全部玩家）、<code>.ns</code>（非旁观）、<code>.nc</code>（非创造）、<code>.f</code>（能挨打的人），友军一直带着这四个。'
             '播报、音效、血条、给物品这类只给玩家的参数不改。2026-11-15 的构建里改写 855 处、保留 1022 处，玩家侧 324 处范围选择补上了避开友军。</div>')
    p.append('<div class="shots">'
             + _shot("ally_arrive", "右键吹号：光柱里登场")
             + _shot("ally_sweep", "坟墓克星横扫")
             + _shot("ally_back", "从背后看：红披风的金色徽记朝外")
             + _shot("ally_boss", "雅克 Boss 与友军雅克对打")
             + "</div>")
    return "".join(p)


# --------------------------------------------------------------------------- 疯人王扫罗

def saul_html():
    moves = _table(["阶段", "招式", "效果与应对"], [
        ("一", "普攻 细剑三连", "贴身 4 格：两下快刺各 6，第三下前冲收剑 9；第三下前侧移"),
        ("一", "突刺", "地上先亮一条 10 格细线，0.8 秒后沿线冲刺 10；离开细线。被拉开到 6 格外时优先用"),
        ("一", "<b>招架</b>", "举剑横在身前 1.5 秒：从正面打他会被格开，他立刻双刺反击 12；绕到侧面、背后打，或等他收架"),
        ("一", "对着空气练剑", "疯病发作，转向空处跟老战友的幻影过招 3 秒，不出手、护甲减半：破绽"),
        ("一", "坚毅（被动）", "原作坚毅铠甲：正面打他，30% 的攻击被甲片弹开；打侧面和背后"),
        ("一", "<b>大招 · 第一课·直线</b>", "站回中心，依次朝五个方向刺出 30 格的银线，每道先亮 1 秒，伤害 14；站进刚刺过的那条线上"),
        ("一", "一闪", "收剑蓄势，瞬间穿过你、停在你身后；身后留下的剑痕 0.5 秒后斩开 12；看到剑痕就离开"),
        ("一", "残影剑阵", "三个半透明的残影从三个方向围住你，各亮一条线，1 秒后同时刺过来，各 8；站到线外"),
        ("一", "<b>大招 · 第二课·圆</b>", "原地旋身，由内到外扫出三圈剑环（3、7、11 格），伤害 12；站进圈与圈之间的空隙。之后转晕 2 秒"),
        ("一", "<b>大招 · 第三课·残影</b>", "四个残影站在场地四方，轮流冲过中心（各 12），最后四个一齐冲；对角线是安全的。之后转晕 2 秒"),
        ("甲碎", "约 5 秒", "头盔、左臂甲（连护肩）崩飞落地，露出缠满蛛网的脸；「斯塔福德……你又来了？那就再来！」"),
        ("二", "普攻 千刀乱刺", "千刀「攻速 +30%」：间隔 10 → 7 刻，左刺、右刺、双刺顺序随机，各 6"),
        ("二", "三连突刺", "三条细线依次亮起，每条折向你当时的位置，各 10；每条都横向躲"),
        ("二", "蛛网", "你脚下和走位方向铺开三张蛛网（不改方块），踩上去缓慢 III；网 8 秒后散"),
        ("二", "错招", "冲向空处全力一刺，刺空后踉跄 1.5 秒：破绽"),
        ("二", "招架", "同一阶段，反击变成三刺"),
        ("二", "血之千刺", "站定，1.5 秒内朝前方扇形乱刺十五下，每下 3；绕到他身后"),
        ("二", "影步斩", "消失，你身后先亮一个暗红的印，然后他在那里现身回身双斩 11；看到印就往前走"),
        ("二", "<b>大招 · 第四课·千刀</b>", "化作剑风消失，二十四道斩痕在你身边依次亮起后斩下，各 8；最后在中心现身一刺 16；之后喘息 2 秒"),
        ("二", "<b>大招 · 第五课·万剑</b>", "天上一把接一把地落下千刀（落点先亮红圈，各 10），最后一把巨剑砸在中心（5 格内 18）；之后喘息"),
        ("二", "<b>大招 · 最后一课</b>", "退到 15 格外，剑举平指向你，2 秒内地上的线跟着你转，然后全速一刺 24。在他出剑前一刻横跳：躲开了，他冲过头跪地 4 秒，护甲归零，伤害 +50%"),
        ("二", "<b>疯王之舞</b>（只一次）", "血量到 150 时：四周变暗，他围着你六次穿刺（各 8），留下六道剑痕；剑痕发亮后同时斩开 16，交汇处是死地。之后他跪地喘息，护甲归零、伤害 +50%"),
        ("结局", "死亡", "千刀滑落，他跪下、倒地，一道天光落下，他沉入地面、散成白灰"),
    ])
    impl = ("<ul>"
            "<li>生成器：外观 <code>add_saul_model.py</code>，战斗 <code>add_saul_boss.py</code>（<code>rpg:saul_boss/</code>，分数 <code>rpg_sl</code>，载体 <code>rpg.slb</code>），"
            "血条 <code>add_saul_boss_art.py</code>（占位：原作坚毅铠甲与细剑图标、哥特字体）。</li>"
            "<li>外观：原作玩家英雄网格 + 织网者皮肤（wiki 的 Web Crawler，本体是 <code>Skins/Spider</code>）+ 坚毅铠甲（强化锁甲的独特变体：原作只给它做了左右臂甲，"
            "头盔、胸甲、护腿沿用强化锁甲的网格，贴图换成 <code>T_StalwartArmor</code>）。动作全是原作玩家动作：细剑连招、武士刀待机、翻滚、表情。</li>"
            "<li>千刀：二代的东西本体里没有；用一代细剑 <code>SM_Rapier</code> 的网格，18×18 的原贴图逐色换成千刀配色（银白剑身、金护手、蓝握柄），不重画像素。</li>"
            "<li>细剑连招在本体里是从一整条 <code>RapierCombo</code> 里截出来的几段复合动作，导出器没给它们写轨道；按雅克那批的格式补了轨道文件，转换器按每段的起止时间裁切。</li>"
            "<li>招架与坚毅：玩家打到他时（<code>player_hurt_entity</code> 进度）按玩家的伤害统计算出这一下的伤害，整下退回；"
            "正面 = 攻击者在他身前 2 格那一点的 3.2 格内。友军打他不算。</li>"
            "<li>碎甲：二阶段把头盔、左臂甲两个部件换成空模型，同时在原处生成同一物品模型的展示实体，按抛物线落到地上。</li>"
            "<li>和玩家一样高（模型 1.87 格），载体不放大：放大载体会抬高乘客挂点，模型就悬在空中走。</li>"
            "<li>坚毅铠甲的臂甲（护肩 + 护手）照原作挂手骨，和英雄的手臂方块一起动。右臂甲在原作蓝图里是 Y 轴镜像，转换器把镜像折进网格、骨只取旋转（之前镜像矩阵转四元数出错，右臂甲歪挂在持剑手旁，就是那个「哑铃」）。</li>"
            "<li>每段三个大招按血线（750 / 500 / 250）或时钟轮流。所有冲刺和瞬移都要求落点脚下有地面，离场地太远或掉下去会被拉回中心。</li>"
            "<li>原作细剑和坚毅铠甲的音效只在本体里，导出器导不出音频，现在用原版声音代替。</li>"
            "</ul>")
    return (_h("疯人王扫罗 · rpg:saul_boss", "两段 · 7～10 分钟")
            + "<p>教廷上一代的十字军大元帅，史上最强的剑豪。他为西西弗的父母反叛教廷，被废掉爵位，从此疯了，只剩下剑。"
              "他从头到尾没有清醒过，把玩家错认成当年的老战友「斯塔福德」，一边打一边教：大招叫「第一课」「第二课」，躲对了他会叫好。"
              "整场只有一个人、一把剑，不召唤、不放法术。倒下时千刀滑落插在地上，他笑着跪下：「斯塔福德，你终于赢了我一次。」"
              "引大卫哀悼扫罗的《撒母耳记下》1:27。</p>"
            + _models([("saul", "十字军大元帅", "坚毅铠甲 · 千刀"), ("saul_s2", "疯人王", "碎掉头盔与左臂甲")])
            + '<div class="debug-lords" style="margin-top:14px">'
            + _fold("招式与大招", "一阶段 9 · 二阶段 11 · 疯王之舞", moves)
            + _fold("实装记录", "外观 · 千刀 · 招架判定 · 碎甲 · 体型", impl) + "</div>")


def michael_html():
    moves = _table(["阶段", "招式", "效果与应对"], [
        ("全程", "<b>灵体与显形</b>", "平时半透明，不被击退、不被打断；一到破绽就显形（模型变实、灵光熄灭），这时受到的伤害 +50%、能被击退"),
        ("全程", "<b>守望者</b>", "召来的 Watchling：漆黑半透明，十四只圣焰橙红的眼睛。传送到你身边挥臂 6 / 双臂下砸 10，挨打会传送走。"
                              "只要还有一只活着，你就「被看见」：发光、米迦勒减伤三成、落点招式瞄的是你此刻的位置；全死后改瞄你 1 秒前的位置"),
        ("全程", "<b>注视</b>（必做）", "眼睛的图案一圈一圈向外铺满场地，半睁，3 秒后全睁：全屏一闪、黑暗，全场伤害 12，每只活着的守望者 +6；全睁时背对他减半"),
        ("一", "普攻 脊骨三连", "5 格：两下各 7，第三下 270° 横扫 10（背后没有）"),
        ("一", "谁似神（骨刺）", "举脊骨蓄力 1 秒，16 格裂线上骨刺一节一节破土 12；横移两步"),
        ("一", "羽刃", "扇形五片燃烧的羽毛，各 6；从间隙穿过去"),
        ("一", "天降", "升空，圣焰圈跟着你 1.5 秒后锁定，俯冲：3 格内 14、3～6 格 6"),
        ("一", "六翼掩面", "六翼合拢 2 秒（伤害减八成），然后展开，6 格内 8 并击退；之后显形 1.5 秒"),
        ("一", "<b>大招 · 谁似神？</b>", "回到中心，骨刺沿八条放射线破土，每轮转 22.5°，三轮，各 12；站进线与线之间并跟着转"),
        ("一", "<b>大招 · 圣哉三唱</b>", "三道齐膝高的焰墙由内向外扩散（第三道两圈），脚着地才会烧到，各 12；焰墙到脚下时跳过去"),
        ("一", "<b>大招 · 第七号角</b>", "飞到中心上空吹号 7 秒，每秒一道天火落下（落点先亮 1 秒），各 10；最后一秒三道；一直跑"),
        ("骨中之骨", "约 6 秒", "他把脊骨插进场地中心成骨柱，从胸口取出两根肋骨，六翼燃起：「骨中之骨，肉中之肉。」"),
        ("二", "普攻 双肋连斩", "间隔 7 刻，每次随机两段双匕首动作，各 5"),
        ("二", "圣焰（被动）", "每次命中叠一层，3 层点燃：0.5 秒后炸开 10 并烧 3 秒；5 秒没被打中清零"),
        ("二", "炽翼突进 · 十字斩 · 天火羽雨", "贴地冲刺 12 格留火路 / 脚下的 X 0.8 秒后斩下 11 / 八个落点落下燃烧的羽毛各 6"),
        ("二", "骨柱", "插在中心的脊骨每 15 秒自己朝最近的人放一次骨刺"),
        ("二", "<b>大招 · 骨中之骨</b>", "两根肋骨沿交叉的两条圆弧绕场飞两圈（各 10），他在两个交点之间来回突进（各 8）"),
        ("二", "<b>大招 · 炽天使</b>", "6 格外的整个场地烧起来（每秒 6），只有他身边安全，但他不停连斩；6 秒后火灭"),
        ("二", "<b>大招 · 三分之一的星辰</b>", "升空；你所在的 120° 扇区先亮红，流星落下（扇区内 8），三轮顺时针；最后大星砸中心 5 格 18"),
        ("二", "<b>六翼燃尽</b>（只一次）", "血量到 150：四周一白，他扑击六次（3 格 12），每扑一次烧掉一片翼；最后无翼落地，显形跪倒 3 秒"),
        ("结局", "死亡", "肋骨落下，他跪在骨柱前：「……主责备你吧。」灵体一层层变淡散去；在场的人各得米迦勒脊骨、米迦勒肋骨"),
    ])
    impl = ("<ul>"
            "<li>生成器：模型 <code>build_michael_model.py</code>（方块版灵体 + Codex 六翼工程的翼 + 扫罗、雅克同骨架的补充动作），"
            "外观 <code>add_michael_model.py</code>，战斗 <code>add_michael_boss.py</code> 与 <code>michael_boss_*.py</code>"
            "（<code>rpg:michael_boss/</code>，分数 <code>rpg_mk</code>，载体 <code>rpg.mkb</code>），血条 <code>add_michael_boss_art.py</code>（占位），特效贴图 <code>add_michael_fx_art.py</code>。</li>"
            "<li>六翼：Codex 工程里是 Blockbench 网格；每片翼的翼骨和翼膜在翼组里绕 X 轴倾斜同一个角度，加一个带倾角的子组就成了轴对齐的方块，"
            "每片翼单独一个部件，正好给六翼燃尽逐片隐藏。</li>"
            "<li>颜色贴近工程文件：不开全亮，图集不透明度 ×1.8、颜色 ×0.7；武器维持工程文件原有的贴图。显形 / 消散是另外两套图集。</li>"
            "<li>特效（2026-11-18「特效太朴素了，贴图太少」）：米迦勒有一整套自己的贴图，字体 <code>rpg:michael_vfx</code> 27 组 154 帧、"
            "地面印记与贴花 34 张；原作特效素材加 Codex 画的序列帧（睁眼、六翼爆开、燃羽、坠星、天火柱、十字斩、光环、单簇圣焰、三张圣印），"
            "颜色按一阶段暖白金、二阶段圣焰烘焙在贴图里。每招分预警、出手、命中、余烬几层；注视全睁时四帧闪光渐褪，四周泛红。骨刺保持方块样子。</li>"
            "<li>守望者：本体叫 WatcherOfTheEnd，网格是末影族共用的 <code>SK_Enderling</code>；身体保持原作的黑、透明度 40%～56%，眼睛换成圣焰橙红并发光。</li>"
            "<li>注视的「背对」判定：从玩家视线方向 100 格外取一点，米迦勒不在这一点 100 格内，就算背对（近似半空间，不用算角度）。</li>"
            "<li>圣哉三唱的焰墙用宏函数按半径选人（<code>distance=$(lo)..$(hi)</code>），只烧脚着地的人。</li>"
            "<li>图鉴图由 <code>guide_renders/soft_render.py</code> 画（Blockbench 没连上时的后备）。原作音效导不出，现在用原版声音。</li>"
            "</ul>")
    return (_h("天使长米迦勒 · rpg:michael_boss", "两段 · 8～11 分钟")
            + "<p>路西法之后的天使长，当年亲手把路西法撕成两半。玩家面对的是他半透明的灵体，只剩权柄的影子，寄在他自己的骨头里。"
              "天使没有自我，这一战是审判：他闻到你身上拂晓之星的气味。一阶段持脊骨，二阶段把脊骨插进大地、取出两根肋骨，六翼燃起成为炽天使。"
              "满身眼睛的守望者是他的眼睛。打赢后灵体散去，留下的脊骨和肋骨就是日后的两件圣器。引《犹大书》1:9。</p>"
            + _models([("michael", "天使长·谁似神", "脊骨 · 六翼"), ("michael_s2", "炽天使", "双肋骨"), ("watchling", "守望者", "Watchling")])
            + '<div class="debug-lords" style="margin-top:14px">'
            + _fold("招式与大招", "全程 3 · 一阶段 8 · 二阶段 9 · 六翼燃尽", moves)
            + _fold("实装记录", "模型 · 六翼 · 颜色 · 守望者 · 注视判定", impl) + "</div>")


# --------------------------------------------------------------------------- 实装记录

def records_html():
    assets = ("<ul>"
              "<li>2026-11-12 起，利维坦、别西卜、亚巴顿、教皇、三种罪仆（先锋、沉没、幽魂）、圣卫默认用从本体提取的原作模型；设环境变量 <code>&lt;KEY&gt;_MODEL=legacy</code> 退回手工模型。"
              "工具：<code>dungeons_models.py</code>、<code>dungeons_variant.py</code>、<code>dungeons_conversion/{generic,blueprint}.py</code>，每个怪的来源写在 <code>_tools/&lt;key&gt;_dungeons_ref/SOURCES.md</code>。</li>"
              "<li>蓝图挂件（头盔、盾、护甲、长矛）按插槽一并转进来，每个挂件是一根有语义名的骨；手持物挂在原作武器插槽 <code>J_R_Weapon</code> 上。</li>"
              "<li>原作音效 191 段从 minecraft.wiki 下载（<code>_tools/dungeons_sounds/</code>）；没有原声的用原版声音事件。直接 curl 会被 403，要经内置浏览器 fetch 再下载。</li>"
              "<li>所有原作素材版权归 Mojang，本项目开源免费、与 Mojang 无关联，署名在 README「素材来源」。</li>"
              "</ul>")
    build = ("<ul>"
             "<li><code>rp_build.sh</code> 从 <code>_orig_rp/</code> 重建资源包，会<b>先清空</b>；<code>build.sh</code> 从 <code>_orig/</code> 重建数据包，同时往资源包里<b>追加</b>约 145 个文件。"
             "所以 <code>build.sh</code> 永远最后跑。2026-11-15 单独重跑了一次 <code>rp_build.sh</code>，资源包从 2665 掉到 2520，PCL 里贴图混乱丢失。</li>"
             "<li>同步前用 <code>rp_validate.py</code> 核对文件总数（2026-11-15：资源包 2668、数据包 14711），不能只看「no problems found」。</li>"
             "<li><code>add_ally_units.py</code> 必须在所有生成器和特效收口之后跑。新加 Boss 或怪物时，把它的函数目录加进脚本里的 <code>HOSTILE</code>，否则它的技能不会打友军。</li>"
             "<li>检查脚本的配合：<code>check_adv.py</code> 加了 <code>player_hurt_entity.entity</code> 白名单；<code>check_demon_minions.py</code> 读入时把单位选择器还原成 <code>@a[</code>。</li>"
             "</ul>")
    vfx = ("<ul>"
           "<li>形状交给展示实体，能量交给粒子。发光体用 <code>text_display</code> 位图字形（不受光照，但只有正面可见，要朝相机或做成多片），地面贴花和实物用 <code>item_display</code>（朝上满亮，侧面五到七成）。</li>"
           "<li>动画用一次 <code>data merge</code> 设目标，交给客户端插值；飞行物用 <code>teleport_duration</code>；不新增逐刻的 <code>nbt=</code> 选择器。特效实体按场次标签和寿命清除，同屏峰值约 40。</li>"
           "<li>贴图只用 16×16 或 32×32；新贴图由 Codex 绘制，再按色板落到像素网格。</li>"
           "<li>恶魔领主身上的黑烟缩小过一次（2026-11-03）；模型逐刻采样改成每 4 刻一次（<code>STRIDE=4</code>），受伤语音只在 <code>rpg.hurt</code> 时响，解决卡顿。</li>"
           "</ul>")
    tests = ("<ul>"
             "<li>无头服务器：探测前 <code>forceload</code>（没有玩家时区块不跑生物，受击无敌时间也不倒数）；每条探测命令之间约隔 14 刻；世界在两次运行之间保留，先清场。</li>"
             "<li>私有测试客户端只驱动自己的进程，不碰你开着的游戏；截图前把 Boss 用 tp + NoAI 钉住、关刷怪，或用创造模式看大招。</li>"
             "<li>没测：友军多名同时在场、多人联机的主人跟随；无头环境测不到箭和诅咒对真人的命中。路西法第三阶段与无名者模型未做。</li>"
             "</ul>")
    return (_h("原作素材与实装记录", "给维护者")
            + '<div class="debug-lords">'
            + _fold("原作模型与音效", "Minecraft Dungeons 本体提取", assets)
            + _fold("构建顺序与友军改写", "rp_build.sh → build.sh", build)
            + _fold("特效与性能规范", "展示实体 + 粒子", vfx)
            + _fold("测试方法与未测项", "无头服务器 · 私有客户端", tests)
            + "</div>")


def section(devil_table=""):
    return ('<section class="plate" id="s9">\n'
            '<div class="plate-h"><span class="num">VIII</span><h2>生物图鉴</h2><span class="sub">领主 · 罪仆 · 圣卫 · Boss 战</span></div>\n'
            '<p>僵尸、骷髅、苦力怕与溺尸保持原版生成和装备逻辑；旧版强化变种、风袭掠夺者、溺尸军团与猪灵军团已经完整退役。'
            '自定义生物分三块：恶魔阵营的七宗罪领主与所罗门罪仆，教廷的圣卫，以及六场指令召唤的 Boss 战。'
            '外观大多是从《Minecraft Dungeons》本体提取的原作模型、动作和音效。</p>\n'
            + devil_table + lords_html() + guards_html() + overview_html()
            + pope_html() + lucifer_html() + usurper_html() + jacques_html() + ally_html() + saul_html() + michael_html() + records_html()
            + "\n</section>")
