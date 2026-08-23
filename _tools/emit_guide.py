# -*- coding: utf-8 -*-
"""Assemble the codex page from the generated card fragments."""

import colorsys
import io
import json

F = json.load(io.open("../_guide_fragments.json", encoding="utf-8"))
S = json.load(io.open("../_guide_sections.json", encoding="utf-8"))


def on_dark(hexcol):
    """把物品用的强调色搬到这张深色页面上。

    罪器的强调色是给 Minecraft 的深色 tooltip 挑的，路西法那支
    #00491c 在这里几乎是黑的。保住色相、抬亮度、收一点饱和度 ——
    七柱各自的身份还在，字却读得出来。
    """
    r, g, b = (int(hexcol.lstrip("#")[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    hue, _l, sat = colorsys.rgb_to_hls(r, g, b)
    # 近乎中性的来源要留住中性 —— 硬抬饱和度会把亚巴顿的'虚无'染成蓝色
    sat = 0.08 if sat < 0.12 else min(max(sat, 0.30), 0.48)
    r, g, b = colorsys.hls_to_rgb(hue, 0.62, sat)
    return "#%02X%02X%02X" % (int(r * 255), int(g * 255), int(b * 255))


def n_of(key):
    """Live count for a section heading -- hardcoding these drifted."""
    return len(S.get(key) or [])


def n_rarity(key, *names):
    return sum(1 for x in (S.get(key) or []) if x.get("rarity") in names)

HEAD = u"""<title>破碎大陆</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Noto+Serif+SC:wght@300;500;700&family=JetBrains+Mono:wght@400;600&display=swap">
<style>
/* This codex is a deliberately single-look page: the dark palette is the
   design, not a response to the viewer's setting.  So the tokens live on bare
   :root with no prefers-color-scheme block and no [data-theme] override --
   nothing can flip it to a light ground, whether it is opened in the artifact
   viewer, double-clicked as a local file, or served from anywhere else.
   `color-scheme: dark` carries that through to the browser's own chrome:
   scrollbars, the search field's caret, and any default form styling. */
:root{
  color-scheme:dark;
  --ground:#12100F; --surface:#1B1816; --sunk:#0C0B0A;
  --ink:#E9E3D5; --muted:#93897C; --rule:#302A25;
  --gold:#C9A227; --gold-soft:#8A7429;
  --r-holy:#FF3300; --r-devil:#DC6A62; --r-legend:#D9A02B; --r-lgd:#FFD700;
  --r-epic:#A275DE; --r-brave:#57C6D6; --r-none:#93897C;
  --r-rite:#E4C24A;
  --shadow:0 1px 0 rgba(0,0,0,.5);
}

*{box-sizing:border-box}
html{background:var(--ground)}
body{
  margin:0; background:var(--ground); color:var(--ink);
  font-family:"Noto Serif SC","Songti SC",serif; font-weight:300;
  font-size:16px; line-height:1.85; -webkit-font-smoothing:antialiased;
}
a{color:var(--gold)}
:focus-visible{outline:2px solid var(--gold); outline-offset:3px}

.wrap{max-width:1180px; margin:0 auto; padding:0 24px 96px}
.layout{display:block}
@media(min-width:1080px){
  .layout{display:grid; grid-template-columns:186px minmax(0,1fr); gap:56px; align-items:start}
}

/* ---- masthead ---- */
.mast{padding:72px 0 40px; border-bottom:1px solid var(--rule)}
.mast .eyebrow{
  font-family:"Cinzel",serif; font-size:11px; letter-spacing:.34em;
  text-transform:uppercase; color:var(--gold); margin:0 0 20px;
}
.mast h1{
  font-family:"Cinzel","Noto Serif SC",serif; font-weight:700;
  font-size:clamp(38px,7vw,68px); line-height:1.04; letter-spacing:.02em;
  margin:0; text-wrap:balance;
}
.mast h1 .cn{display:block; font-family:"Noto Serif SC",serif; font-size:.44em; font-weight:500; letter-spacing:.22em; color:var(--muted); margin-top:18px}
.mast h1 .heb{
  display:block; font-family:"Noto Serif SC",serif; font-size:.3em; font-weight:400;
  direction:rtl; letter-spacing:.04em; color:var(--gold-soft); margin-top:20px;
}
.mast p.lede{max-width:60ch; color:var(--muted); margin:26px 0 0; font-size:17px}
.mast p.lede strong{color:var(--ink); font-weight:600}
.mast p.lede.sub{margin-top:14px; font-size:15px; font-style:italic; line-height:1.9}
.mast p.lede.meta{margin-top:22px; font-size:14.5px; padding-top:20px; border-top:1px solid var(--rule)}
.chips{display:flex; flex-wrap:wrap; gap:8px; margin-top:28px}
.chip{
  font-family:"JetBrains Mono",monospace; font-size:11.5px; letter-spacing:.06em;
  border:1px solid var(--rule); color:var(--muted);
  padding:5px 11px; border-radius:2px;
}
.chip b{color:var(--ink); font-weight:600}

/* ---- index rail ---- */
.rail{display:none}
@media(min-width:1080px){
  .rail{display:block; position:sticky; top:32px; padding-top:56px}
  .rail ol{list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:11px}
  .rail a{
    display:flex; gap:11px; text-decoration:none; color:var(--muted);
    font-size:13.5px; line-height:1.4; transition:color .15s;
  }
  .rail a:hover{color:var(--ink)}
  .rail .num{font-family:"Cinzel",serif; font-size:11px; color:var(--gold-soft); padding-top:2px; min-width:26px}
}

/* ---- plates ---- */
.plate{padding-top:72px}
.plate-h{display:flex; align-items:baseline; gap:16px; border-bottom:1px solid var(--rule); padding-bottom:14px; margin-bottom:32px}
.plate-h .num{font-family:"Cinzel",serif; font-size:13px; letter-spacing:.2em; color:var(--gold)}
.plate-h h2{font-family:"Noto Serif SC",serif; font-weight:700; font-size:25px; margin:0; letter-spacing:.04em}
.plate-h .sub{margin-left:auto; font-size:12.5px; color:var(--muted); font-family:"JetBrains Mono",monospace}
.plate > p{max-width:66ch; color:var(--muted)}
.plate > p strong{color:var(--ink); font-weight:500}

/* ---- steps ---- */
.steps{list-style:none; counter-reset:s; margin:0; padding:0; display:flex; flex-direction:column; gap:2px}
.steps li{counter-increment:s; display:grid; grid-template-columns:44px minmax(0,1fr); gap:18px; padding:18px 0; border-bottom:1px solid var(--rule)}
.steps li::before{
  content:counter(s,decimal-leading-zero); font-family:"JetBrains Mono",monospace;
  font-size:12px; color:var(--gold-soft); padding-top:5px; letter-spacing:.05em;
}
.steps h3{margin:0 0 4px; font-size:16.5px; font-weight:500}
.steps p{margin:0; color:var(--muted); font-size:14.5px}
.steps .opt{font-family:"Cinzel",serif; font-size:10px; letter-spacing:.18em; color:var(--muted); border:1px solid var(--rule); padding:2px 7px; margin-left:9px; vertical-align:2px}
code, pre{font-family:"JetBrains Mono",monospace}
code{font-size:13px; background:var(--sunk); padding:2px 6px; border-radius:2px; color:var(--ink)}
.cmd{display:block; margin-top:9px; background:var(--sunk); border-left:2px solid var(--gold-soft); padding:9px 13px; font-size:13px; overflow-x:auto; white-space:pre}

/* ---- system entries ---- */
.sys{display:grid; gap:1px; background:var(--rule); border:1px solid var(--rule)}
.sys > div{background:var(--surface); padding:22px 24px}
@media(min-width:720px){.sys{grid-template-columns:1fr 1fr}}
.sys h3{margin:0 0 3px; font-size:16.5px; font-weight:700; letter-spacing:.03em}
.sys .how{font-family:"JetBrains Mono",monospace; font-size:11.5px; color:var(--gold); letter-spacing:.04em; margin:0 0 12px}
.sys p{margin:0; color:var(--muted); font-size:14.5px}
.sys ul{margin:10px 0 0; padding-left:18px; color:var(--muted); font-size:14px}

/* ---- 破碎大陆 ---- */
.scroll-h{text-align:center; margin:0 0 40px; padding-bottom:30px; border-bottom:1px solid var(--rule)}
.scroll-h .heb{font-size:30px; line-height:1.5; color:var(--gold-soft); direction:rtl; margin:0 0 8px}
.scroll-h .rom{font-family:"Cinzel",serif; font-size:13px; letter-spacing:.3em; color:var(--muted); margin:0 0 14px}
.scroll-h .say{font-size:15px; color:var(--ink); font-style:italic; line-height:1.9; max-width:60ch; margin:0 auto}
.scroll-h .byline{font-family:"JetBrains Mono",monospace; font-size:11px; letter-spacing:.06em;
  color:var(--muted); margin:20px 0 0; opacity:.8}
.book{margin:0 0 8px; border-top:1px solid var(--rule); padding-top:26px}
.book:first-of-type{border-top:none; padding-top:0}
.book > h3{
  font-family:"Cinzel",serif; font-size:12px; letter-spacing:.24em; color:var(--gold-soft);
  margin:0 0 4px; font-weight:400;
}
.book > h4{margin:0 0 16px; font-size:21px; font-weight:700; color:var(--ink); letter-spacing:.04em}
.book p{margin:0 0 13px; font-size:14.5px; line-height:1.95; color:var(--muted)}
.book p strong{color:var(--ink); font-weight:600}
.book .cap{
  font-family:"JetBrains Mono",monospace; font-size:11px; letter-spacing:.1em;
  color:var(--muted); margin:22px 0 8px; opacity:.85;
}
.verse{
  margin:18px 0; padding:2px 0 2px 18px; border-left:2px solid var(--gold-soft);
  font-size:14px; color:var(--ink); font-style:italic; line-height:1.85;
}
.verse cite{display:block; margin-top:5px; font-style:normal; font-size:11.5px;
  letter-spacing:.06em; color:var(--muted)}
.sins{list-style:none; margin:16px 0 0; padding:0; display:grid;
  grid-template-columns:repeat(auto-fill,minmax(180px,1fr)); gap:1px;
  background:var(--rule); border:1px solid var(--rule)}
.sins li{background:var(--ground); padding:12px 15px; font-size:14px}
.sins .who{display:block; font-weight:700; color:var(--ink); margin-bottom:3px}
.sins .what{color:var(--muted); font-size:12.5px}

/* ---- filter bar ---- */
.tools{display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-bottom:26px}
.tools button{
  font-family:"Noto Serif SC",serif; font-size:13.5px; color:var(--muted);
  background:none; border:1px solid var(--rule); padding:6px 14px;
  border-radius:2px; cursor:pointer; transition:color .15s,border-color .15s;
}
.tools button:hover{color:var(--ink)}
.tools button[aria-pressed="true"]{color:var(--ground); background:var(--ink); border-color:var(--ink)}
/* the bar doubles as the rarity legend: each button wears its own tier colour */
.tools button[data-f="holy"]{color:var(--r-holy)}
.tools button[data-f="devil"]{color:var(--r-devil)}
.tools button[data-f="lgd"]{color:var(--r-lgd)}
.tools button[data-f="legend"]{color:var(--r-legend)}
.tools button[data-f="epic"]{color:var(--r-epic)}
.tools button[aria-pressed="true"][data-f]{color:var(--ground)}
.tools input{
  font-family:"Noto Serif SC",serif; font-size:13.5px; color:var(--ink);
  background:var(--surface); border:1px solid var(--rule); padding:6px 12px;
  border-radius:2px; margin-left:auto; min-width:180px;
}
.tools input::placeholder{color:var(--muted)}

/* ---- item cards (styled after the in-game tooltip) ---- */
.grid{display:grid; gap:14px; grid-template-columns:repeat(auto-fill,minmax(286px,1fr))}
.card{
  background:var(--surface); border:1px solid var(--rule);
  border-top:2px solid var(--tier,var(--r-none));
  padding:18px 20px 16px; box-shadow:var(--shadow);
}
.card.r-holy{--tier:var(--r-holy)} .card.r-devil{--tier:var(--r-devil)}
.card.r-legend{--tier:var(--r-legend)} .card.r-epic{--tier:var(--r-epic)}
.card.r-lgd{--tier:var(--r-lgd)}
.card.r-brave{--tier:var(--r-brave)}
.card.r-rite{--tier:var(--r-rite)}
.card[hidden]{display:none}
.card-h{display:flex; gap:13px; align-items:flex-start; margin-bottom:11px}
.card-id{min-width:0}
.icon{
  flex:0 0 auto; width:46px; height:46px; padding:6px; box-sizing:border-box;
  image-rendering:pixelated; object-fit:contain;
  background:var(--sunk); border:1px solid var(--rule); border-radius:2px;
}
.icon-none{display:block}
/* the enchantment sheen: a highlight sweeping across the item's own
   silhouette, the same read the game gives an enchanted item */
.icon-wrap{position:relative; display:inline-block; flex:0 0 auto; line-height:0}
.icon-wrap.glint::after{
  content:""; position:absolute; inset:6px; pointer-events:none;
  -webkit-mask-image:var(--sprite); mask-image:var(--sprite);
  -webkit-mask-size:contain; mask-size:contain;
  -webkit-mask-repeat:no-repeat; mask-repeat:no-repeat;
  -webkit-mask-position:center; mask-position:center;
  background:linear-gradient(115deg,
    transparent 41%, rgba(168,104,236,.34) 47%,
    rgba(214,184,255,.60) 50%, rgba(138,84,214,.32) 53%, transparent 59%);
  background-size:300% 300%; mix-blend-mode:screen;
  animation:glint 4.4s linear infinite;
}
/* dense table rows get a still sheen -- 100+ animated repaints is
   more cost than the effect is worth at 30px */
td.has-icon .icon-wrap.glint::after{inset:3px; animation:none; background-position:44% 0}
@keyframes glint{from{background-position:150% 0} to{background-position:-70% 0}}
@media (prefers-reduced-motion:reduce){
  .icon-wrap.glint::after{animation:none; background-position:44% 0}
}
h3 .new{
  display:inline-block; vertical-align:middle; margin-left:9px;
  font-family:"Cinzel",serif; font-size:9.5px; letter-spacing:.18em;
  padding:3px 7px 2px; border:1px solid var(--tier,var(--rule));
  border-radius:2px; color:var(--tier,var(--muted)); font-weight:400;
}
td.has-icon{display:flex; gap:10px; align-items:flex-start}
td.has-icon .icon{width:30px; height:30px; padding:3px}
.tier{font-family:"Cinzel",serif; font-size:10px; letter-spacing:.22em; color:var(--tier,var(--r-none)); display:block; margin-bottom:5px}
.card h3{margin:0; font-size:19px; font-weight:700; color:var(--tier,var(--ink)); letter-spacing:.03em; line-height:1.3}
.card .base{margin:3px 0 0; font-family:"JetBrains Mono",monospace; font-size:11.5px; color:var(--muted)}
.flavour{margin:0 0 13px; font-size:14px; color:var(--muted); font-style:italic; line-height:1.7}
.skill{border-left:2px solid var(--tier,var(--r-none)); padding:1px 0 1px 12px; margin:0 0 13px}
.skill-kind{font-family:"Cinzel",serif; font-size:9.5px; letter-spacing:.16em; color:var(--muted); margin-right:8px}
.skill-name{font-size:14.5px; font-weight:700; color:var(--ink)}
.skill p{margin:2px 0 0; font-size:13.5px; color:var(--muted); line-height:1.65}
.stats{display:grid; grid-template-columns:auto minmax(0,1fr); gap:3px 14px; margin:0; font-size:12.5px}
.stats dt{font-family:"Cinzel",serif; font-size:9.5px; letter-spacing:.13em; color:var(--muted); padding-top:5px}
.stats dd{margin:0; color:var(--ink); font-variant-numeric:tabular-nums; line-height:1.7}
.stats .slot{font-family:"JetBrains Mono",monospace; font-size:10px; color:var(--muted); margin-left:4px}
.stats code{font-size:11px; background:none; padding:0; color:var(--muted)}

/* ---- tables ---- */
.tw{overflow-x:auto; border:1px solid var(--rule)}
table{border-collapse:collapse; width:100%; min-width:640px; font-size:14px}
th,td{text-align:left; padding:11px 16px; border-bottom:1px solid var(--rule); vertical-align:top}
thead th{
  font-family:"Cinzel",serif; font-size:10px; letter-spacing:.16em;
  color:var(--muted); font-weight:500; background:var(--surface);
}
tbody tr:last-child td{border-bottom:none}
td.num{font-family:"JetBrains Mono",monospace; font-variant-numeric:tabular-nums; color:var(--ink)}
td .nm{font-weight:700}
td .sm{display:block; color:var(--muted); font-size:12.5px; margin-top:2px}
.boss td{background:var(--surface)}

/* ---- chapters ---- */
.chapters{list-style:none; margin:0; padding:0; display:flex; flex-direction:column}
.chapters li{display:grid; grid-template-columns:66px minmax(0,1fr); gap:20px; padding:16px 0; border-bottom:1px solid var(--rule)}
.chapters .ch{font-family:"Cinzel",serif; font-size:12px; color:var(--gold-soft); letter-spacing:.12em; padding-top:5px}
.chapters h3{margin:0 0 4px; font-size:16px; font-weight:500}
.chapters p{margin:0; font-size:14px; color:var(--muted); line-height:1.75}

.sub-h{display:flex; align-items:baseline; gap:12px; font-family:"JetBrains Mono",monospace;
  font-size:11.5px; letter-spacing:.08em; color:var(--muted); font-weight:400;
  margin:34px 0 14px; text-transform:none}
.sub-h .rolls{margin-left:auto; font-size:11px; color:var(--gold-soft)}
.plate .sub-h:first-of-type{margin-top:8px}
.dim{color:var(--muted); font-size:12.5px}
.bane{color:#B4636B}
.note{border:1px solid var(--rule); border-left:2px solid var(--gold-soft); background:var(--surface); padding:16px 20px; margin-top:26px; font-size:14.5px; color:var(--muted)}
.note b{color:var(--ink); font-weight:500}
footer{margin-top:80px; padding-top:22px; border-top:1px solid var(--rule); font-size:12.5px; color:var(--muted); font-family:"JetBrains Mono",monospace}
@media (prefers-reduced-motion:reduce){*{transition:none!important; animation:none!important}}
</style>
"""


def build():
    p = []
    a = p.append
    a(HEAD)
    a('<div class="wrap">')

    # masthead ------------------------------------------------------------
    a('''<header class="mast">
<p class="eyebrow">Eretz Ha-Shevarim · Data Pack Codex</p>
<h1>Shevarim<span class="heb">אֶרֶץ הַשְּׁבָרִים</span><span class="cn">破碎大陆 · 碎片之地</span></h1>
<p class="lede">这是破碎大陆的见证：世界曾经完整，后来因<strong>神陨</strong>、<strong>堕天</strong>与<strong>权柄的分裂</strong>而成为碎片。</p>
<p class="lede sub">这是关于光、混沌、堕落、救赎与人的书；<br>是关于<strong>权</strong>与<strong>力</strong>如何分离，又如何在末后的日子重新相遇的见证。</p>
<p class="lede meta">承载这段见证的是一套 Minecraft 生存 RPG 数据包：''' + str(n_of("weapons")) + ''' 件带主动／被动技能的武具（含<strong>六位魔神</strong>的罪遗武器）、''' + str(n_of("armour")) + ''' 件护甲、可洗练可镶嵌可升级的装备体系，以及成建制的溺尸与猪灵军团。</p>
<div class="chips">
<span class="chip">Minecraft <b>1.21.11</b></span>
<span class="chip">数据包格式 <b>94.1</b></span>
<span class="chip">资源包格式 <b>75.0</b></span>
<span class="chip">命名空间 <b>rpg</b></span>
</div>
</header>''')

    a('<div class="layout">')
    a('''<nav class="rail" aria-label="目录"><ol>
<li><a href="#s1"><span class="num">I</span>起始配置</a></li>
<li><a href="#s2"><span class="num">II</span>核心系统</a></li>
<li><a href="#s3"><span class="num">III</span>武器图鉴</a></li>
<li><a href="#s4"><span class="num">IV</span>护甲图鉴</a></li>
<li><a href="#s5"><span class="num">V</span>符文与符石</a></li>
<li><a href="#s6"><span class="num">VI</span>药剂与材料</a></li>
<li><a href="#s7"><span class="num">VII</span>掉落总表</a></li>
<li><a href="#s9"><span class="num">VIII</span>生物图鉴</a></li>
<li><a href="#s8"><span class="num">IX</span>驱魔体系</a></li>
<li><a href="#s14"><span class="num">X</span>驱魔道具</a></li>
<li><a href="#s12"><span class="num">XI</span>七十二柱契约</a></li>
<li><a href="#s13"><span class="num">XII</span>佣兵小队</a></li>
<li><a href="#s10"><span class="num">XIII</span>破碎大陆</a></li>
<li><a href="#s11"><span class="num">XIV</span>指令速查</a></li>
</ol></nav>''')

    a('<main>')

    # I setup -------------------------------------------------------------
    a('''<section class="plate" id="s1">
<div class="plate-h"><span class="num">I</span><h2>起始配置</h2><span class="sub">按顺序执行一次</span></div>
<p>数据包本体不会自动初始化。开新档、或第一次把数据包装进已有存档后，<strong>必须先建好计分板</strong>，否则所有武器技能、等级、洗练都不会触发。以下步骤在游戏内以管理员身份执行。</p>
<ol class="steps">
<li><div><h3>确认版本与前置</h3><p>客户端为 <code>1.21.11</code>；数据包放进 <code>存档/datapacks/</code>，材质包放进 <code>.minecraft/resourcepacks/</code> 并在选项里启用。材质包提供全部自定义武器模型，不装的话武器会显示成原版外观。</p></div></li>
<li><div><h3>建立计分板</h3><p>注册全部 60 余个计分项：武器技能触发器、等级、洗练计数、随机数等。<strong>这一步是所有功能的前提。</strong></p><code class="cmd">/function rpg:command/soreboard</code></div></li>
<li><div><h3>建立 BOSS 血条</h3><p>创建恶魔 BOSS 的血量显示条 <code>minecraft:devil</code>，红色、六段式、上限 1000。</p><code class="cmd">/function rpg:command/bossbar</code></div></li>
<li><div><h3>创建掠夺者队伍<span class="opt">必要</span></h3><p>风袭卫道士系列怪物出生时会加入 <code>green</code> 队伍；队伍不存在时服务端每次召唤都会报错。</p><code class="cmd">/team add green</code></div></li>
<li><div><h3>发放起始装备<span class="opt">可选</span></h3><p>三个发放函数会把对应类别的全部物品发给<strong>所有在线玩家</strong>，建议在创造模式测试区使用。</p><code class="cmd">/function rpg:command/give/weapon      # 武器、护甲、药剂
/function rpg:command/give/item        # 符文、晶石、锻造材料
/function rpg:command/give/weapon_up_item  # 武器分支唱片</code></div></li>
<li><div><h3>布置试炼与宝库<span class="opt">可选</span></h3><p>在脚下生成一组不祥试炼刷怪笼与宝库，掉落表指向本包的 <code>rpg:trial/*</code> 与 <code>rpg:loot/*</code>。站在要放置的位置执行。</p><code class="cmd">/function rpg:command/setblock</code></div></li>
<li><div><h3>召唤恶魔 BOSS<span class="opt">可选</span></h3><p>在脚下生成 1000 点生命的恶魔（唤魔者本体 + 卫道士护卫）。战斗全程由 <code>rpg:entities/warden/warden</code> 每刻驱动。</p><code class="cmd">/function rpg:command/summon</code></div></li>
</ol>
<div class="note"><b>玩家等级：</b>玩家的经验等级即角色等级。等级每提升一档，最大生命值会按 64/32/16/8/4/2/1 的分段自动加成，并播放升级特效——无需任何额外操作。</div>
</section>''')

    # II systems ----------------------------------------------------------
    a('''<section class="plate" id="s2">
<div class="plate-h"><span class="num">II</span><h2>核心系统</h2><span class="sub">物品扔在地上互相作用</span></div>
<p>本包的加工系统几乎不使用工作台：<strong>把两件（或多件）物品丢在地上、让它们靠得足够近（1 格内）</strong>，系统就会自动合成。成功时会有粒子与图腾音效。</p>
<div class="sys">
<div><h3>洗练</h3><p class="how">武器 / 胸甲 + 钻石 · 地面 1 格内</p><p>随机重掷装备的攻击伤害与攻击速度。每件装备最多洗练 <b>10</b> 次，次数记录在物品的 <code>xilian</code> 数据里，用尽后钻石会被直接消耗掉且不再生效。</p></div>
<div><h3>附魔</h3><p class="how">武器 + 试金石（紫水晶碎片）· 地面 1 格内</p><p>把试金石上的附魔直接写进武器。共 24 种试金石，涵盖锋利、亡灵杀手、节肢杀手、力量、穿透、横扫之刃、保护、荆棘、耐久等，等级 2–5 不等。</p></div>
<div><h3>镶嵌</h3><p class="how">武器 + 镶嵌符文 / 符石 · 地面 1 格内</p><p>符文（被动）与符石（主动）会把自己的 Lore 与技能标签追加到武器上，符文本体消失。<b>符石</b>赋予的是长按右键释放的主动技能；<b>符文</b>是常驻的触发型被动。</p></div>
<div><h3>锻造</h3><p class="how">冶炼石 + 生铁 + 剑胚 · 灵魂火上方</p><p>三件材料同时丢在<b>灵魂火</b>上即可锻造出随机武器。普通<b>冶炼石</b>产出 <code>rpg:trial/sword</code>，<b>传说冶炼石</b>产出 <code>rpg:trial/epic_sword</code>，成功后灵魂火熄灭。</p></div>
<div><h3>武器升级</h3><p class="how">武器 + 铸造之石 · 地面 1 格内</p><p>铸造之石一次提供 100 点武器经验。武器每升一级，攻击伤害 +1%、攻击速度 +0.97%，等级与经验实时显示在 Lore 第 9–11 行。</p></div>
<div><h3>武器分支</h3><p class="how">武器 + 音乐唱片 · 地面 1 格内</p><p>六张唱片把武器导向<b>神圣</b>（信仰／存续／不屈）或<b>恶魔</b>（恶念／睚眦／傲慢）分支，为武器加上对应的词缀与攻击特效，唱片消耗。</p></div>
<div><h3>玩家面板</h3><p class="how">手持玩家头颅</p><p>手持「玩家面板」头颅时，Lore 会实时刷新玩家等级、血量、攻击速度、攻击伤害、盔甲韧性与护甲值。</p></div>
<div><h3>试炼与宝库</h3><p class="how">不祥试炼刷怪笼 · 宝库</p><p>刷怪笼进入冷却时触发奖励流程；宝库钥匙掉落走 <code>rpg:loot/loot</code>（普通）与 <code>loot_ominous</code>（不祥），产出下界之星形态的战利品凭证，落地后再兑换成实际物品。</p></div>
</div>
</section>''')

    # III weapons ---------------------------------------------------------
    a('''<section class="plate" id="s3">
<div class="plate-h"><span class="num">III</span><h2>武器图鉴</h2><span class="sub">''' + str(n_of("weapons")) + ''' 件</span></div>
<p>稀有度由高到低：<strong>神圣 · 恶魔 · 限定传说 · 传说 · 史诗</strong>。
标记「主动技能」的武器<strong>长按右键</strong>发动：多数物品靠 <code>food</code> + <code>consumable</code> 组件借用进食动作，
而两把<strong>长枪</strong>（朗基努斯之枪、路西法）用的是长枪自带的蓄力动作，因此保留原本的突刺手感。
「被动技能」在命中敌人时按概率自动触发。属性中的百分比为乘算加成。</p>
<div class="tools" role="group" aria-label="按稀有度筛选">
<button type="button" data-f="all" aria-pressed="true">全部</button>
<button type="button" data-f="holy" aria-pressed="false">神圣</button>
<button type="button" data-f="devil" aria-pressed="false">恶魔</button>
<button type="button" data-f="lgd" aria-pressed="false">限定传说</button>
<button type="button" data-f="legend" aria-pressed="false">传说</button>
<button type="button" data-f="epic" aria-pressed="false">史诗</button>
<input type="search" id="q" placeholder="搜索名称或技能…" aria-label="搜索武器">
</div>
<div class="grid" id="wgrid">''' + F["weapons"] + '''</div>

<h3 class="sub-h">随机掉落武器<span class="rolls">属性与附魔每次掉落重新掷点</span></h3>
<p>下面这些不是固定装备，而是从战利品表里滚出来的：同一把武器每次掉落的属性都落在标注的区间内，附魔条数固定但内容随机。它们同样参与洗练、镶嵌与武器升级。</p>
<div class="grid">''' + F["loot_epic"] + '''</div></section>''')

    # IV armour -----------------------------------------------------------
    a('''<section class="plate" id="s4">
<div class="plate-h"><span class="num">IV</span><h2>护甲图鉴</h2><span class="sub">14 件 · 4 套</span></div>
<p>护甲共四套：<strong>神圣</strong>（圣荆棘冠 / 都灵裹尸布）走减伤与回复，<strong>森焱</strong>套抗火与击退，<strong>王者</strong>套堆生命与伤害吸收，<strong>冰霜</strong>套是过渡装。护甲的被动技能由胸甲上的镶嵌符文提供（见下一节）。</p>
<div class="grid">''' + F["armour"] + '</div></section>')

    # V runes -------------------------------------------------------------
    a('''<section class="plate" id="s5">
<div class="plate-h"><span class="num">V</span><h2>符文与符石</h2><span class="sub">''' + str(n_of("runes")) + ''' 刻印 · ''' + str(n_of("stones")) + ''' 晶石</span></div>
<p><strong>镶嵌符文</strong>（下界石英）按镶嵌部位分为剑用、胸甲用、弓弩用三类，提供触发型被动；带「镶嵌技能」字样的<strong>符石</strong>提供长按右键释放的主动技能。<strong>属性晶石</strong>（锻造模板）则是直接手持生效的百分比加成。</p>
<div class="grid">''' + F["runes"] + '</div>')
    a('<h3 style="font-family:Cinzel,serif;font-size:12px;letter-spacing:.18em;color:var(--muted);margin:40px 0 16px">属性晶石</h3>')
    a('<div class="grid">' + F["stones"] + '</div></section>')

    # VI consumables ------------------------------------------------------
    a('''<section class="plate" id="s6">
<div class="plate-h"><span class="num">VI</span><h2>药剂与材料</h2><span class="sub">12 药剂 · 8 材料</span></div>
<div class="grid">''' + F["consum"] + '</div>')
    a('<h3 style="font-family:Cinzel,serif;font-size:12px;letter-spacing:.18em;color:var(--muted);margin:40px 0 16px">锻造材料</h3>')
    a('<div class="grid">' + F["mats"] + '</div>')
    a('<div class="note"><b>试金石（紫水晶碎片）共 24 种，</b>丢在武器旁即可把附魔写入武器：' + F["ench"] + '。</div>')
    a('</section>')

    # VII loot ------------------------------------------------------------
    a('''<section class="plate" id="s7">
<div class="plate-h"><span class="num">VII</span><h2>掉落总表</h2><span class="sub">权重 · 区间 · 来源</span></div>
<p>前面几节是 <code>give</code> 指令里写死的固定装备；这一节是<strong>战利品表</strong>里的东西——怪物身上穿的、试炼刷怪笼吐出来的、宝库开出来的。它们的属性不是定值，而是每次生成时在一个<strong>区间内随机</strong>，附魔也是随机抽取的，所以同名的两把武器数值可能完全不同。</p>
<h3 class="sub-h">试炼精英武器 · rpg:trial/epic_sword<span class="rolls">6 选 1</span></h3>
<p style="margin:0 0 18px">锻造台用<b>传说冶炼石</b>产出的就是这张表。六件都带技能，且技能标签与固定武器共用同一套处理逻辑。</p>
''' + F["loot_trial"] + F["loot_drops"] + F["loot_reward"] + '''
<div class="note"><b>怎么读这些数字：</b>「权重」是同一个池子里被抽中的相对概率；「随机属性范围」是该词条实际会落在的区间，
生成时在区间内均匀取值；「随机附魔 ×N」表示从全部可用附魔里随机抽 N 次，等级也随机。
耐久损耗一栏说明掉落时装备已经是残破状态。</div>
</section>''')

    # VII bestiary --------------------------------------------------------
    a('''<section class="plate" id="s9">
<div class="plate-h"><span class="num">VIII</span><h2>生物图鉴</h2><span class="sub">4 大阵营</span></div>
<p>普通僵尸、骷髅、苦力怕在出生瞬间会被数据包重新洗牌：随机换装本包的战利品护甲，并有几率直接替换成下方的强化变种。成建制的军团则由对应函数整队召唤。</p>

<h3 style="font-family:Cinzel,serif;font-size:12px;letter-spacing:.18em;color:var(--muted);margin:32px 0 14px">溺尸军团 · rpg:entities/drowned</h3>
<div class="tw"><table>
<thead><tr><th>单位</th><th>生命</th><th>攻击</th><th>速度</th><th>装备与特征</th></tr></thead>
<tbody>
<tr class="boss"><td><span class="nm">溺尸王</span><span class="sm">骑乘 399 点生命的战马</span></td><td class="num">1000</td><td class="num">17</td><td class="num">0.40</td><td>三叉戟 + 盾牌，下界合金胸甲与护腿，攻速 4、击退 2、交互距离 7，体型 ×1.2</td></tr>
<tr><td><span class="nm">溺尸巨人</span></td><td class="num">900</td><td class="num">10</td><td class="num">0.30</td><td>体型 ×3，交互距离 10，全身下界合金</td></tr>
<tr><td><span class="nm">溺尸执行官</span><span class="sm">骑乘披甲战马</span></td><td class="num">700</td><td class="num">13</td><td class="num">0.30</td><td>三叉戟 + 花纹盾，横扫比例 1.0</td></tr>
<tr><td><span class="nm">溺尸骑士</span><span class="sm">骑乘披甲战马</span></td><td class="num">500</td><td class="num">10</td><td class="num">0.30</td><td>钻石剑 + 三叉戟，击退 1.2</td></tr>
<tr><td><span class="nm">溺尸剑士</span></td><td class="num">400</td><td class="num">13</td><td class="num">0.30</td><td>钻石剑 + 三叉戟，横扫比例 1.0</td></tr>
<tr><td><span class="nm">溺尸盾斧</span></td><td class="num">400</td><td class="num">13</td><td class="num">0.30</td><td>钻石斧 + 盾牌</td></tr>
<tr><td><span class="nm">溺尸士兵</span></td><td class="num">100</td><td class="num">7</td><td class="num">0.20</td><td>下界合金胸甲，成群出现</td></tr>
</tbody></table></div>

<h3 style="font-family:Cinzel,serif;font-size:12px;letter-spacing:.18em;color:var(--muted);margin:32px 0 14px">猪灵军团 · rpg:entities/piglin</h3>
<div class="tw"><table>
<thead><tr><th>单位</th><th>生命</th><th>攻击</th><th>速度</th><th>装备与特征</th></tr></thead>
<tbody>
<tr class="boss"><td><span class="nm">猪灵巨人</span></td><td class="num">700</td><td class="num">15</td><td class="num">0.40</td><td>体型 ×3，横扫比例 1.2，击退 1.5，方块交互距离 10</td></tr>
<tr><td><span class="nm">猪灵骑士</span><span class="sm">骑乘 200 点生命的炽足兽</span></td><td class="num">500</td><td class="num">10</td><td class="num">0.40</td><td>金剑 + 盾牌</td></tr>
<tr><td><span class="nm">猪灵剑士</span></td><td class="num">300</td><td class="num">13</td><td class="num">0.40</td><td>双持金剑</td></tr>
<tr><td><span class="nm">猪灵盾斧</span></td><td class="num">300</td><td class="num">13</td><td class="num">0.40</td><td>金斧 + 盾牌</td></tr>
<tr><td><span class="nm">猪灵士兵</span></td><td class="num">100</td><td class="num">7</td><td class="num">0.30</td><td>下界合金胸甲</td></tr>
</tbody></table></div>

<h3 style="font-family:Cinzel,serif;font-size:12px;letter-spacing:.18em;color:var(--muted);margin:32px 0 14px">恶魔 · rpg:entities/warden</h3>
<div class="tw"><table>
<thead><tr><th>单位</th><th>生命</th><th>阶段</th><th>特征</th></tr></thead>
<tbody>
<tr class="boss"><td><span class="nm">恶魔（唤魔者形态）</span><span class="sm">标签 devil + boss</span></td><td class="num">1000</td><td>第一形态</td><td>护甲 15、击退抗性 0.5、体型 ×1.2，常驻隐身并持续散出烟雾与墨汁粒子；被<b>替死人偶</b>攻击会强制显形</td></tr>
<tr><td><span class="nm">恶魔（卫道士形态）</span><span class="sm">标签 devil2 + boss</span></td><td class="num">1000</td><td>第二形态</td><td>双持下界合金剑，按 <code>devil</code> 计分推进技能序列，390 刻时召唤三名分身</td></tr>
<tr><td><span class="nm">恶魔护卫</span></td><td class="num">100</td><td>随从</td><td>Johnny 卫道士，击退 2、速度加成</td></tr>
</tbody></table></div>

<h3 style="font-family:Cinzel,serif;font-size:12px;letter-spacing:.18em;color:var(--muted);margin:32px 0 14px">风袭掠夺者 · rpg:entities/illager</h3>
<div class="tw"><table>
<thead><tr><th>单位</th><th>生命</th><th>特征</th></tr></thead>
<tbody>
<tr><td><span class="nm">风袭唤魔者</span></td><td class="num">50</td><td>手持风弹与旗帜，附带风矢充能与发光</td></tr>
<tr><td><span class="nm">风袭幻术师</span></td><td class="num">50</td><td>双持弓</td></tr>
<tr><td><span class="nm">风袭卫道士</span></td><td class="num">40</td><td>手持重锤；另有骑乘尸马（30 点生命）的版本</td></tr>
<tr><td><span class="nm">风袭掠夺者</span></td><td class="num">30</td><td>弩 + 旗帜</td></tr>
<tr><td><span class="nm">恼鬼</span></td><td class="num">—</td><td>体型 ×2，手持重锤</td></tr>
</tbody></table></div>

<h3 style="font-family:Cinzel,serif;font-size:12px;letter-spacing:.18em;color:var(--muted);margin:32px 0 14px">强化的普通怪物 · rpg:command/spawn</h3>
<div class="tw"><table>
<thead><tr><th>触发</th><th>几率</th><th>结果</th></tr></thead>
<tbody>
<tr><td>骷髅类出生</td><td class="num">1/20</td><td>流浪者（30 生命，锁链装备）</td></tr>
<tr><td>骷髅类出生</td><td class="num">1/20</td><td>骷髅骑兵（骷髅骑骷髅马，铁质装备）</td></tr>
<tr><td>骷髅类出生</td><td class="num">1/20</td><td>凋灵骷髅（40 生命，下界合金剑与全套盔甲）</td></tr>
<tr><td>僵尸类出生</td><td class="num">1/20</td><td>铁剑僵尸（50 生命、攻击 4、体型 ×1.1）</td></tr>
<tr><td>僵尸类出生</td><td class="num">1/20</td><td>抱婴僵尸 / 僵尸村民（40 生命、护甲 5）</td></tr>
<tr><td>僵尸类出生</td><td class="num">2/20</td><td>五层僵尸叠罗汉</td></tr>
<tr><td>僵尸类出生</td><td class="num">1/20</td><td>巨型僵尸（100 生命、体型 ×3）</td></tr>
<tr><td>苦力怕出生</td><td class="num">1/10</td><td>高压苦力怕（30 生命、体型 ×1.3、爆炸威力 5）</td></tr>
<tr><td>苦力怕出生</td><td class="num">3/10</td><td>迷你苦力怕（10 生命、体型 ×0.5、引信 10 刻）</td></tr>

<tr><td>骷髅 / 僵尸出生</td><td>必定</td><td>全身装备重掷为本包的 <code>rpg:armor/*</code> 战利品</td></tr>
</tbody></table></div>
</section>''')

    # IX exorcism ---------------------------------------------------------
    a('''<section class="plate" id="s8">
<div class="plate-h"><span class="num">IX</span><h2>驱魔体系</h2><span class="sub">魔化值 · 空缺者 · 仪式 · 逆圣化</span></div>
<p>包里一直有一条圣／魔轴：圣器与罪遗武器各自带着 <code>holy_weapon_tag</code> 与 <code>devil_weapon_tag</code>。
从这一版起它有了长期后果——<strong>握着魔器的人会慢慢变成它的主人</strong>。
魔化值不显示在侧边栏，而是屏幕下方那条 actionbar。</p>
<div class="note"><b>屏幕下方只有一行，所以全包只留一个出口。</b>武器蓄力条、一次性小提示、魔化与契约冷却
都走同一条 <code>rpg:hud/hud</code>，按三档优先级挑：
<br>① <b>蓄力条</b>（沉锚／熔流／缠绕／逆圣化）——它是<b>正在进行的动作</b>的实时反馈，压过一切；
<br>② <b>一次性提示</b>（配装、入队、钱不够…）——2 秒，晚看到没关系；
<br>③ <b>持续状态</b>——魔化（或圣痕）与契约冷却<b>并排</b>画在同一行，两者都是状态，不该互相顶掉。
<br>三者互不覆盖：蓄力结束、提示过期，下一档自己就回来了。</div>

<h3 class="sub-h">魔化值<span class="rolls">每 2 秒结算一次 · 上限 100</span></h3>
<p>手持恶魔本体武器 <b>+2</b>／罪遗武器 <b>+1</b>；手持圣器 <b>−1</b>，两者同时握着会互相抵消。攻击空缺者 <b>+6</b>，杀死空缺者 <b>+8</b>。</p>
<div class="tw"><table>
<thead><tr><th>区间</th><th>状态</th><th>表现</th></tr></thead>
<tbody>
<tr><td>0–30</td><td>尚可自持</td><td>无</td></tr>
<tr><td>31–60</td><td>侵蚀渐深</td><td>身上泛起暗紫色纹路</td></tr>
<tr><td>61–90</td><td>近乎失守</td><td>暗红纹路加深，伴幽匿之魂</td></tr>
<tr><td>91–100</td><td>濒临魔化</td><td>常驻<b>力量 I</b>；但手持圣器会持续灼伤（每 2 秒 2 点魔法伤害）</td></tr>
</tbody></table></div>
<div class="note"><b>魔化只有一个出口。</b>把它压下去要靠驱魔仪式；把它推到顶，则通向<b>逆圣化</b>——两条路都从同一支图腾开始。</div>

<h3 class="sub-h">空缺者<span class="rolls">约六分之一的村民</span></h3>
<p>外表与常人无异的空壳。平时和普通村民毫无分别，<strong>只有当持圣器的人走进 16 格内才会显形</strong>（发光 + 幽匿之魂粒子）。它不是靶子——放着不管会烂开，动手打反而更糟。</p>
<div class="note"><b>什么算「圣器」。</b>三类，<b>手持或穿戴</b>都算——护甲当然是穿着算：
<br>① 四件<b>驱魔道具</b>（图腾、圣水、替死人偶、天启星，见下一节）；
<br>② <b>神圣品质</b>的武具：<b>朗基努斯之枪</b>、<b>圣荆棘冠</b>、<b>都灵裹尸布</b>；
<br>③ 任何加过<b>神圣分支</b>的武器（丢神圣唱片给武器）。
<br>身上带着圣器时魔化会缓慢消退；但魔化一旦到 <b>91 以上</b>，圣器<b>会灼手</b>。</div>
<div class="sys">
<div><h3>蔓延</h3><p class="how">每 20 秒一拍 · 1/4 概率 · 8 格内</p><p>未被驱除的空缺者会把邻近村民也变成空壳。一个村子若无人过问，会慢慢整片烂掉。</p></div>
<div><h3>撕壳</h3><p class="how">被圣器照住 3 秒，或挨第一次打</p><p>伪装撑不住，壳裂开，放出两只<b>空壳碎片</b>（凋灵怪，12 生命 / 4 攻击，30 秒后自行消散）；空壳本身获得速度 II 逃窜。</p></div>
<div><h3>附身转移</h3><p class="how">杀死空缺者时</p><p>躯体死了，里面的东西<b>跳到 16 格内最近的村民身上</b>。若附近再无可用躯体，它会赤裸地留在原地，化作三只<b>无处可去者</b>（16 生命 / 5 攻击）。<br><b>剑解决不了它</b>——这正是驱魔存在的理由。</p></div>
</div>

<h3 class="sub-h">驱魔仪式<span class="rolls">驱魔图腾 + 驱魔圣水</span></h3>
<p>手持<b>驱魔图腾</b><b>长按右键</b>立起（本体是 <code>item_display</code>，没有 AI、没有碰撞）。此刻它还是熄的——要用<b>驱魔圣水</b>浇上去才点燃。
圣水必须是<strong>滞留型</strong>：喷溅型落地即散，图腾没有任何东西可以感知；滞留药水留下的 <code>area_effect_cloud</code> 才是「浇上了」的凭据。</p>
<div class="tw"><table>
<thead><tr><th>时刻</th><th>净化量</th><th>图腾尺寸</th><th>作用</th></tr></thead>
<tbody>
<tr><td>第 1 拍（10 秒）</td><td>−12</td><td>1.00</td><td rowspan="5">半径 <b>6</b> 格内：玩家扣减魔化值，空缺者被驱出（村民留下、掉落 24 经验、附近碎片一并收走）</td></tr>
<tr><td>第 2 拍（8 秒）</td><td>−10</td><td>0.88</td></tr>
<tr><td>第 3 拍（6 秒）</td><td>−8</td><td>0.74</td></tr>
<tr><td>第 4 拍（4 秒）</td><td>−6</td><td>0.58</td></tr>
<tr><td>第 5 拍（2 秒）</td><td>−4</td><td>0.40</td></tr>
<tr><td>燃尽</td><td>—</td><td>炸开</td><td>范围内空缺者一并驱出，敌意生物受 6 点魔法伤害并被震开</td></tr>
</tbody></table></div>

<h3 class="sub-h">逆圣化<span class="rolls">魔化 = 100 时点燃图腾</span></h3>
<p>魔化到顶那一刻会有一次提示。<strong>此时若有满魔化者站在图腾 7 格内，仪式不再净化，而是引燃。</strong></p>
<blockquote class="verse">但在魔化的尽头，他看见污染深处仍有一段没有被抹去的圣性。负与负相乘，污染发生反转。<cite>——卷六《百年战争书》</cite></blockquote>
<p>图腾朝着受术者烧十秒，五道灼烧共 <b>19 点</b>魔法伤害（3 / 3 / 4 / 4 / 5），每道附带缓慢 III，光从暗红一路走到纯白。
<strong>人必须站在 7 格内熬完</strong>——走开或者倒下，仪式当场作废。</p>
<div class="tw"><table>
<thead><tr><th>结果</th><th>代价 / 回报</th></tr></thead>
<tbody>
<tr><td><b>熬过去</b></td><td>魔化归零（若身上有契约，柱位一并烧断、书退回未立约），获得<b>圣痕</b> 3 分钟：力量 II、抗性提升 I、生命恢复 I、防火、伤害吸收 II；期间<b>沾不上任何魔化</b>，且 6 格内的空缺者会被自动驱出——本人就是一场行走的仪式。</td></tr>
<tr><td><b>没熬住</b></td><td>图腾碎裂，魔化一点没少，另加凋零 5 秒 + 失明 3 秒。</td></tr>
</tbody></table></div>
<div class="note"><b>关于自定义模型：</b>原版数据包<b>无法</b>为生物添加自定义模型——生物模型写死在客户端里，资源包只能替换<b>已有</b>实体的贴图与模型。
驱魔图腾用的是 <code>item_display</code>：把一件物品当作可缩放、可旋转的展示实体摆在世界里，这是 1.19.4 之后原版唯一的「自定义模型」路子，本包的图腾缩放动画就是这么做的。</div>
</section>''')

    # X rite kit -------------------------------------------------------------
    a('''<section class="plate" id="s14">
<div class="plate-h"><span class="num">X</span><h2>驱魔道具</h2><span class="sub">四件 · 自成一族</span></div>
<p>这四件功能上是同一套东西——<strong>显形、净化、仪式</strong>——所以从药剂与材料里摘了出来，单列一族。
它们也是最容易到手的<strong>「圣器」</strong>：<b>手持或穿戴</b>任何一件圣器，空缺者就会在 16 格内显形，魔化也会缓慢消退。
神圣品质的<b>朗基努斯之枪</b>、<b>圣荆棘冠</b>、<b>都灵裹尸布</b>同样算圣器——后两件<b>穿在身上</b>即可。</p>

<div class="note"><b>为什么这件事要紧。</b>「持圣器」这个前提原本<b>只有神圣分支武器</b>能满足——也就是说在拿到神圣唱片、
改造过武器之前，空缺者<b>全程隐形</b>：蔓延、撕壳、附身转移全都在照常运转，你却一个也看不见，整套驱魔体系像是没生效。
这一族补上了可获得的来源。<br>
代价是对称的：魔化一旦到 <b>91 以上</b>，握着圣器<b>会灼手</b>（每 2 秒 2 点魔法伤害）。</div>

<div class="sys">
<div><h3>驱魔图腾</h3><p class="how">长按右键立起</p><p>仪式的主体。立起后要用驱魔圣水浇上才点燃；点燃后每两秒净化一次，效力逐次递减，燃尽时炸开。
魔化满值者在场时点燃，仪式转为<b>逆圣化</b>。也是<b>毁约</b>的场所——在它燃着时长按已立约的契约之书即可解约。</p></div>
<div><h3>驱魔圣水</h3><p class="how">投掷 · 滞留型</p><p>必须是滞留型：喷溅型落地即散，图腾没有任何东西可以感知。
落地那汪水每秒洗掉 <b>1</b> 点魔化，并灼烧 4 格内的空壳——被浇过的壳<b>裂得快得多</b>。<br>
<span class="dim">原本的「圣水」已并入此物；旧瓶子仍然可用。</span></p></div>
<div><h3>替死人偶</h3><p class="how">放置即生效</p><p>立着的时候，<b>12 格内的空缺者不必持圣器也会显形</b>——这就是它 Lore 里说的「恶魔攻击其会使祂显形」。
更要紧的是<b>替死</b>：16 格内的你每一轮沾上的魔化，改由人偶承受，一次吃一点，<b>吃满 10 点就碎</b>。
全包唯一能<b>挡住</b>魔化的东西。</p></div>
<div><h3>天启星</h3><p class="how">长按右键 · 一次性</p><p>照亮 <b>32</b> 格内的一切：恶魔、空壳、以及<b>魔化 31 以上的人</b>全部现形。
空壳额外挨 6 点伤害并大幅加速裂壳。「能指引恶魔的繁星，审判罪恶」。</p></div>
</div>

<div class="grid">''' + F["rite"] + '''</div>
</section>''')

    # X pacts ---------------------------------------------------------------
    P = json.load(io.open("../_pact.json", encoding="utf-8"))
    prow = []
    for q in P["pillars"]:
        prow.append(
            '<tr><td class="num">%d</td>'
            '<td><b style="color:%s">%s</b><br><span class="dim">%s</span></td>'
            '<td>%s</td>'
            '<td><b>［%s］</b><br><span class="dim">%s</span></td>'
            '<td class="bane">%s</td></tr>'
            % (q["n"], on_dark(q["colour"]), q["who"], q["sin"], q["boon"],
               q["power"], q["power_text"], q["bane"]))
    a('''<section class="plate" id="s12">
<div class="plate-h"><span class="num">XI</span><h2>七十二柱契约</h2><span class="sub">七位领主 · 一本书</span></div>
<p>上一节的<strong>逆圣化</strong>是走出污染的路；这一节是走进去的路，而且是<strong>你自己选的</strong>。</p>
<blockquote class="verse">每一个正式边缘者都被分配一根柱位和一位魔神：边缘者借用魔神的力，魔神借契约进入边缘者的心。<cite>——卷五《魔神书》</cite></blockquote>
<p>契约是一本书。<strong>长按右键签下</strong>，柱位当场绑定，恩赐与枷锁一并生效，书也随之变成「已立约」的样子。
此后再长按右键，就是<strong>动用柱中之力</strong>——冷却 ''' + str(P["cd_seconds"]) + ''' 秒，每次再添 ''' + str(P["use_taint"]) + ''' 点魔化。</p>
<div class="sys">
<div><h3>柱位是排他的</h3><p class="how">一个人只挂在一根柱子上</p><p>已立约后，攥着别柱的书没有任何作用。想换柱位，先得把身上这一份解掉。</p></div>
<div><h3>两条解约途径</h3><p class="how">逆圣化，或在燃着的图腾旁毁约</p><p><b>逆圣化</b>会把污染连同柱位一起烧掉，契约之书也<b>退回未立约</b>。
但那要求魔化先推到 100——对签错柱位的人不是出路。所以还有第二条：<b>立一支驱魔图腾、浇上圣水，在它燃着时长按你那本已立约的书</b>。
代价是当场 <b>+20 魔化</b>、凋零 10 秒，图腾一并烧尽；书退回未立约，可以改投别的柱位。</p></div>
<div><h3>力量借的是原件</h3><p class="how">与罪器同一套施法路径</p><p>路西法的蛇矛与尖牙、利维坦的落锚，契约调用的就是罪器本身那几个函数——同一位魔神的力，表现理应一模一样。</p></div>
<div><h3>常驻代价</h3><p class="how">每 2 秒结算一次</p><p>立约本身就在渗：魔化每次结算额外 +1，与手中魔器的沾染叠加。<b>贪婪</b>那一柱渗得更快，翻倍。</p></div>
</div>
<div class="tw"><table>
<thead><tr><th>柱</th><th>魔神 · 罪</th><th>恩赐</th><th>力量</th><th>枷锁</th></tr></thead>
<tbody>''' + "".join(prow) + '''</tbody></table></div>
<div class="note"><b>关于贴图：</b>七本书暂时沿用原版附魔书的外观，
<code>custom_model_data</code> 已按柱位排好（''' + str(P["cmd0"]) + '''–''' + str(P["cmd0"] + 6) + '''）。
美术补上时只要在材质包里给 <code>enchanted_book</code> 加一段 <code>range_dispatch</code>，数据包这边一个字都不用改。</div>
<div class="note"><b>玛门补齐了第七宗罪。</b>卷五的七宗罪表里，贪婪那一格此前是空的——
六位领主各有一件罪遗武器，玛门没有。第七柱的契约填上了它：贪婪不制造东西，它只让已有的东西变多。</div>
</section>''')

    # XI squad --------------------------------------------------------------
    a('''<section class="plate" id="s13">
<div class="plate-h"><span class="num">XII</span><h2>佣兵小队</h2><span class="sub">花钱雇人 · 配刀 · 指哪打哪</span></div>
<p>一个<strong>独立分支</strong>，不与罪器、契约、驱魔任何一条耦合。你可以完全不碰前面那些体系，只带着一队人打。</p>

<div class="sys">
<div><h3>募兵旗 · 两步</h3><p class="how">长按右键 · 白色旗帜</p><p>身边没有待雇者时，先<b>招一名「待雇佣兵」到场</b>（不花钱，他中立站着）。
身边有待雇者时再长按，才是真的<b>雇下他</b>——雇的是眼前这个人，不是凭空变一个出来。
上限 <b>4</b> 人，价钱逐人递增：<b>8 / 16 / 24 / 32</b> 枚<b>［货币］</b>（粗金），全队共 80 枚。</p></div>
<div><h3>指挥旗 · 指哪打哪</h3><p class="how">长按右键 · 副手空着</p><p>沿视线找出 24 格内第一个目标并标记，全队压上；目标倒下即自动归队。</p></div>
<div><h3>配装</h3><p class="how">副手拿武器 + 长按指挥旗</p><p>交给最近的佣兵，他原本拿的<b>掉在地上</b>——那就是取回的方式。
你塞什么他就按什么打（伤害读的是他自己的攻击力属性，天然含手持武器）。佣兵战死时武器<b>必定掉落</b>。</p></div>
<div><h3>姿态与解雇</h3><p class="how">潜行 + 长按指挥旗</p><p><b>副手空着</b>切换<b>跟随 ⇄ 驻守</b>；<b>副手拿着东西</b>则解雇最近的佣兵，装备掉地并退回 4 枚货币。</p></div>
</div>

<h3 class="sub-h">佣兵<span class="rolls">尸壳 · 白天不自燃</span></h3>
<div class="tw"><table>
<thead><tr><th>属性</th><th>数值</th><th>说明</th></tr></thead>
<tbody>
<tr><td>生命</td><td class="num">40</td><td>—</td></tr>
<tr><td>护甲</td><td class="num">4</td><td>—</td></tr>
<tr><td>攻击</td><td class="num">4</td><td>写死，不随世界难度浮动；<b>手持武器的加成直接叠上去</b></td></tr>
<tr><td>攻击间隔</td><td class="num">13 刻</td><td>生物受伤后约有 10 刻无敌帧，砍得更密只是浪费</td></tr>
<tr><td>待雇状态</td><td>—</td><td>未雇佣的佣兵不跟随、不出手，也不占队伍名额</td></tr>
<tr><td>索敌半径</td><td class="num">0</td><td><b>永不主动出手</b>，见下</td></tr>
<tr><td>归队距离</td><td class="num">34 格</td><td>掉队即刻拉回雇主身边</td></tr>
</tbody></table></div>

<div class="note"><b>为什么佣兵永远不会误伤你。</b>尸壳是敌对生物，自带主动索敌，而原版命令
<b>没有任何办法清除一个生物的当前目标</b>。所以这里不是"打之前判断一下是不是自己人"——
那种写法总有漏网的一刻。唯一能从根上断掉的地方是<b>索敌半径</b>：把 <code>follow_range</code> 设成 <code>0</code>，
它就永远不会自己选中任何东西。安全性是<b>结构性</b>的，不靠判定去兜。
代价是它也不会自己打该打的人——于是移动与攻击全部由数据包驱动。</div>

<div class="note"><b>配武器不需要任何数值表。</b>伤害读的是佣兵<b>自己的 <code>attack_damage</code> 属性</b>，
而这个属性天然含手持武器（实测：空手 4，塞一把下界合金剑变 11）。
所以你把本包<b>任何一把</b>自定义武器塞给他，他就按那把武器的数值打，包括后续新加的。</div>

<div class="note"><b>两条尸壳专属的注意。</b>其一，尸壳属于 <code>#minecraft:zombies</code>，
本包每刻会给新出生的僵尸类重掷装备甚至替换成强化变种——佣兵已在那条流水线上按标签排除。
其二，<b>佣兵不下水</b>：尸壳泡水会转化成普通僵尸，而转化是换一个实体，标签与记分板一起没了，
人就凭空消失；所以踩到水会立刻召回雇主身边。</div>
</section>''')

    # VIII chapters -------------------------------------------------------
    a('''<section class="plate" id="s10">
<div class="plate-h"><span class="num">XIII</span><h2>破碎大陆</h2><span class="sub">Eretz Ha-Shevarim</span></div>

<div class="scroll-h">
<p class="heb">אֶרֶץ הַשְּׁבָרִים</p>
<p class="rom">ERETZ HA-SHEVARIM &nbsp;·&nbsp; 碎片之地</p>
<p class="say">这是破碎大陆的见证：世界曾经完整，后来因神陨、堕天与权柄的分裂而成为碎片。<br>
这是关于光、混沌、堕落、救赎与人的书；<br>是关于权与力如何分离，又如何在末后的日子重新相遇的见证。</p>
<p class="byline">世界观设定：本作作者　·　叙事文案：ChatGPT（OpenAI）</p>
</div>
<div class="book"><h3>卷一</h3><h4>创世书</h4><p class="cap">第一章　起初</p><p>起初，世界尚未有形，地是空虚混沌，黑暗覆在深渊之上。</p><blockquote class="verse">地是空虚混沌，渊面黑暗。<cite>——《创世记 1:2》</cite></blockquote><p>上帝在混沌中立定自己的权柄，其名为<strong>真实与虚妄</strong>：祂所称为真实的，就成为世界；祂所弃绝的，就归入黑暗。天堂从混沌中升起，天使被造，作祂意志的手。</p><p>但混沌深处有一物没有被创造，也没有被消灭。它没有形体，也没有王座，却与上帝相对而立——它不是另一个神，而是<strong>污染的可能</strong>。后来，人称它为<strong>敌基督</strong>。</p><p class="cap">第二章　七日</p><p>光与黑暗分开，穹苍立定，旱地显露，日月众星掌管节令，海与天充满活物。第六日，上帝照自己的意志造人，使人承受<strong>神性的火种</strong>；第七日止息，分别为圣。</p><blockquote class="verse">神看着一切所造的都甚好。<cite>——《创世记 1:31》</cite></blockquote></div><div class="book"><h3>卷二</h3><h4>伊甸书</h4><p class="cap">第一章　王冠与王国</p><p>生命树有十个源质，树根扎在<strong>王国</strong>，树冠伸入<strong>王冠</strong>。王国是肉身、土地与现实；王冠最接近上帝。人在王国出生，却被造得可以走到王冠。</p><p>道路之中有一个隐藏的节点，名为 <strong>Da’at</strong>。那里藏着未被允许的知识——既能通往真实，也能使真实破碎。</p><p class="cap">第二章　金苹果</p><p>敌基督没有以自己的形体显现，只在分别善恶树上留下一枚金色的果实。</p><blockquote class="verse">你们便如神能知道善恶。<cite>——《创世记 3:5》</cite></blockquote><p>那果子不是寻常的果子，而是人类获得的<strong>第一份魔力</strong>。人因此拥有人性，也拥有欲望、自我与自私。于是人从王冠坠落，跌入王国。</p><p>从那日起，人类一代一代下坠。可是下坠也留下了<strong>自由意志</strong>——只有拥有自我的人，才能选择重新向上。</p></div><div class="book"><h3>卷三</h3><h4>权柄书</h4><p class="cap">第一章　权与力</p><p>上帝的权柄分为<strong>权</strong>与<strong>力</strong>。权能够定义道路、授予资格、命名真实；力能够执行命令，使道路在世界中显现。</p><p>圣父掌管中枢，圣子承受救赎之力，圣灵持守权柄并监察圣子。三位同出一源。</p><blockquote class="verse">圣哉！圣哉！圣哉！万军之耶和华。<cite>——《以赛亚书 6:3》</cite></blockquote><p><strong>圣力</strong>是未被污染的权柄，<strong>魔力</strong>是被敌基督侵染后的权柄——二者并非两种创造，而是同一权柄的两种状态。圣器名为 <strong>Kli Qodesh</strong>，魔器名为 <strong>Kli Tum’ah</strong>。</p><p class="cap">第二章　弥赛亚</p><p>凡承担救世之责的人都被称为弥赛亚。摩西承受律法之权，大卫承受王权之印；他们是弥赛亚，却不是圣子。</p><p>圣子若没有圣灵，只能成为执行神迹的刀；圣灵若没有圣子，只能成为无人执行的命令。直到末后的日子，他们将在伊甸园相遇，使权与力重新合一。</p></div><div class="book"><h3>卷四</h3><h4>堕天书</h4><p class="cap">第一章　晨星坠落</p><p>路西法原是天堂中最接近上帝的天使之一。他看见权柄的光，也看见天使只是权柄的延伸，于是在心中说：<em>“为何我只能承受命令，而不能成为命令的源头？”</em></p><p>敌基督侵染了他，使他第一次拥有独立的自我。他召集三分之一的天使升向王冠。</p><blockquote class="verse">在天上就有了争战。<cite>——《启示录 12:7》</cite></blockquote><p>人类称那日为<strong>第一次神陨之战</strong>；天堂称之为第一次堕落之战；路西法称之为第一次自由之战。米迦勒得胜，三分之一的星辰坠落，天使的圣力被污染，成为恶魔。</p><p><strong>路西法是他曾经是谁，撒旦是他选择成为谁。</strong></p><p class="cap">第二章　地狱与无底坑</p><p>被撕裂的天堂坠入世界的阴影，成为地狱——恶魔的乐园，也是恶魔的囚笼。撒旦被锁在最深处的<strong>无底坑</strong>里；无底坑没有底，正如污染没有尽头。火山口是它在人间留下的楔子。</p><blockquote class="verse">那一千年完了，撒但必从监牢里被释放。<cite>——《启示录 20:7》</cite></blockquote></div><div class="book"><h3>卷五</h3><h4>魔神书</h4><p class="cap">第一章　七宗罪</p><p>撒旦坐在地狱王座上，王座之下有七位领主。七位领主各有一件<strong>罪器</strong>——罪的形体，也是污染的刀刃。</p><ul class="sins">
<li><span class="who">路西法</span><span class="what">傲慢</span></li>
<li><span class="who">利维坦</span><span class="what">嫉妒</span></li>
<li><span class="who">贝利尔</span><span class="what">放纵与色欲</span></li>
<li><span class="who">别西卜</span><span class="what">暴食</span></li>
<li><span class="who">萨麦尔</span><span class="what">暴怒</span></li>
<li><span class="who">亚巴顿</span><span class="what">虚无与怠惰</span></li>
<li><span class="who">玛门</span><span class="what">贪婪</span></li>
</ul><p>边缘者若杀死恶魔，罪器便凝结为<strong>罪遗武器</strong>。然而夺取罪器的人也夺取了罪的影子——<strong>使用越久，越接近原本的主人</strong>。</p><p class="cap">第二章　七十二柱</p><p>所罗门王是人类历史中第一个被正式记录的边缘者。他以王冠、戒指与符印进入深渊，与七十二位魔神立约——不创造，不消灭，只将它们命名、分类并封入七十二根柱中。</p><p>七十二柱成为历史封印，也成为教廷后来的军械库。每一个正式边缘者都被分配一根柱位和一位魔神：边缘者借用魔神的力，魔神借契约进入边缘者的心。<strong>边缘者若失去自我，柱中的魔神便可以夺取他的身体。</strong></p></div><div class="book"><h3>卷六</h3><h4>百年战争书</h4><p class="cap">第一章　空缺者</p><p>一百多年以前，后方城市开始出现<strong>没有死亡的死者</strong>。他们仍有姓名、面孔与记忆，却失去了人的情感——像空屋一样活着。</p><p>恶魔不是从城门外来，而是从邻人的声音、教会的档案、官员的命令和家庭的餐桌中渗入人间。</p><blockquote class="verse">我们并不是与属血气的争战。<cite>——《以弗所书 6:12》</cite></blockquote><p>主角在空缺者事件中看见教廷正在隐藏真相，也看见负责驱魔的人已经成为污染的一部分。教廷给他两个选择：加入边缘者体系，或作为污染源被处死。</p><p><strong>他没有被神选中，他是为了活下去而成为武器。</strong></p><p class="cap">第二章　后方与圣座</p><p>他逐渐发现：父母之死与教廷有关；边缘者不是被保护的人，而是可以被消耗的军械；圣器正在吸收圣徒与士兵的生命；战争也被用来延长统治。教廷宣布他为异端。</p><p class="cap">第三章　逃往前线</p><p>他逃往东南大岛——那里有奥尔曼苏丹国的军队、教廷的堡垒、阿尔比恩的贸易殖民地，以及被神陨之战烧焦的土地。与此同时，七十二柱的封印开始松动。</p><p class="cap">第四章　撒旦出坑</p><p>一千年的封印结束，无底坑打开，撒旦从火山口重返人间。主角使用七罪魔器，魔化一步步加深：手臂硬化，犄角生长，意识被罪欲撕裂，他即将失去自己的名字。</p><p>但在魔化的尽头，他看见污染深处仍有一段没有被抹去的圣性。<strong>负与负相乘，污染发生反转</strong>——从魔中诞生极致的圣，这条道路名为<strong>逆圣化</strong>。</p></div><div class="book"><h3>卷七</h3><h4>人的国度</h4><p class="cap">第一章　伊甸园</p><p>撒旦倒下以后，主角进入伊甸园，圣灵在那里等待他：权与力本是同一权柄的两面，二者相合才能重新形成上帝完整的权柄。</p><p>但他看见神的教条曾经保护人类，也曾经囚禁人类；看见撒旦反抗神，却没有真正摆脱污染；看见人类虽从王冠坠落，却因此获得了自己的意志。<strong>于是他不再请求成为新的神。</strong></p><p class="cap">第二章　人的革命</p><p>他的敌人不再是撒旦，不再是七宗罪，也不再是地狱的恶魔——而是那些借神之名阻挡历史的人，是把圣力据为己有的教廷，是以战争维持权力的贵族。</p><p>他举起的不是天堂的旗，也不是地狱的旗，而是<strong>人类革命的旗帜</strong>。</p><blockquote class="verse">你们必晓得真理，真理必叫你们得以自由。<cite>——《约翰福音 8:32》</cite></blockquote><p>第七日，上帝曾为世界安息。而在<strong>人的第七日</strong>，世界不再属于神，也不再属于魔。</p><p><strong>世界属于人。</strong></p></div>
<div class="note"><b>末后的见证：</b>圣力是权柄未被污染的声音，魔力是权柄被污染后的回响。
圣器承载神的力，魔器承载堕落的影。人类走过了王国，穿过了深渊，攀上了王冠，也看见了伊甸园——
人类已经知道神的答案，所以人类终于可以写下自己的答案。</div>
</section>''')

    # IX commands ---------------------------------------------------------
    a('''<section class="plate" id="s11">
<div class="plate-h"><span class="num">XIV</span><h2>指令速查</h2><span class="sub">rpg 命名空间</span></div>
<div class="tw"><table>
<thead><tr><th>指令</th><th>作用</th></tr></thead>
<tbody>
<tr><td class="num">/function rpg:command/soreboard</td><td>注册全部计分板<span class="sm">首次安装必须执行</span></td></tr>
<tr><td class="num">/function rpg:command/bossbar</td><td>创建恶魔 BOSS 血条</td></tr>
<tr><td class="num">/function rpg:command/give/weapon</td><td>发放全部武器、护甲与药剂</td></tr>
<tr><td class="num">/function rpg:command/give/item</td><td>发放符文、晶石与锻造材料</td></tr>
<tr><td class="num">/function rpg:command/give/weapon_up_item</td><td>发放六张武器分支唱片</td></tr>
<tr><td class="num">/function rpg:command/setblock</td><td>在脚下布置试炼刷怪笼与宝库</td></tr>
<tr><td class="num">/function rpg:command/summon</td><td>在脚下召唤恶魔 BOSS 与护卫</td></tr>
<tr><td class="num">/function rpg:entities/drowned/king</td><td>召唤溺尸王与近卫</td></tr>
<tr><td class="num">/function rpg:entities/piglin/king</td><td>召唤猪灵巨人与近卫</td></tr>
<tr><td class="num">/function rpg:entities/illager/wind_vindicator</td><td>召唤风袭掠夺者小队</td></tr>
<tr><td class="num">/team add green</td><td>创建风袭掠夺者所属队伍</td></tr>
</tbody></table></div>
<div class="note"><b>每刻运行的函数</b>由 <code>#minecraft:tick</code> 驱动，依次为 <code>rpg:command/index</code>（标志索引与伤害检测）→ <code>rpg:command/tick</code>（合成、试炼、等级）→ <code>rpg:item/sword/legend/legend1</code>（武器技能）→ <code>rpg:entities/warden/warden</code>（BOSS 战）→ <code>rpg:command/tick_end</code>。正常游玩无需手动调用。</div>
</section>''')

    a('<footer>破碎大陆 · TRALANCER RPG　—　世界观设定：本作作者　·　叙事文案：ChatGPT（OpenAI）　·　迁移、优化与图鉴生成：Claude（Anthropic）<br>图鉴依据数据包 rpg 命名空间内的物品与实体数据生成 · Minecraft Java 1.21.11</footer>')
    a('</main></div></div>')

    a('''<script>
(function(){
  var grid=document.getElementById('wgrid');
  if(!grid) return;
  var cards=[].slice.call(grid.querySelectorAll('.card'));
  var btns=[].slice.call(document.querySelectorAll('.tools button'));
  var q=document.getElementById('q');
  var filter='all';
  function apply(){
    var term=(q.value||'').trim().toLowerCase();
    cards.forEach(function(c){
      var okR = filter==='all' || c.dataset.rarity===filter;
      var okQ = !term || c.dataset.name.toLowerCase().indexOf(term)>-1;
      c.hidden = !(okR && okQ);
    });
  }
  btns.forEach(function(b){
    b.addEventListener('click',function(){
      filter=b.dataset.f;
      btns.forEach(function(o){o.setAttribute('aria-pressed', String(o===b));});
      apply();
    });
  });
  q.addEventListener('input',apply);
})();
</script>''')
    return "\n".join(p)


if __name__ == "__main__":
    io.open("../TRALANCER-RPG-图鉴.html", "w", encoding="utf-8", newline="\n").write(build())
    print("written")
