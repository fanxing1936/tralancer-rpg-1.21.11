# -*- coding: utf-8 -*-
"""Assemble the codex page from the generated card fragments."""

import io
import json

F = json.load(io.open("../_guide_fragments.json", encoding="utf-8"))

HEAD = u"""<title>布兰德·宿命之途</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Noto+Serif+SC:wght@300;500;700&family=JetBrains+Mono:wght@400;600&display=swap">
<style>
:root{
  --ground:#E6E1D6; --surface:#F3EFE6; --sunk:#DCD6C8;
  --ink:#241F1B; --muted:#6B6258; --rule:#CFC7B8;
  --gold:#8A6D12; --gold-soft:#B79A3E;
  --r-holy:#CC2900; --r-devil:#8E2A22; --r-legend:#8A5E0A;
  --r-epic:#5B3796; --r-brave:#0F5C66; --r-none:#6B6258;
  --shadow:0 1px 0 rgba(36,31,27,.06);
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --ground:#12100F; --surface:#1B1816; --sunk:#0C0B0A;
    --ink:#E9E3D5; --muted:#93897C; --rule:#302A25;
    --gold:#C9A227; --gold-soft:#8A7429;
    --r-holy:#FF3300; --r-devil:#DC6A62; --r-legend:#D9A02B;
    --r-epic:#A275DE; --r-brave:#57C6D6; --r-none:#93897C;
    --shadow:0 1px 0 rgba(0,0,0,.5);
  }
}
:root[data-theme="dark"]{
  --ground:#12100F; --surface:#1B1816; --sunk:#0C0B0A;
  --ink:#E9E3D5; --muted:#93897C; --rule:#302A25;
  --gold:#C9A227; --gold-soft:#8A7429;
  --r-holy:#FF3300; --r-devil:#DC6A62; --r-legend:#D9A02B;
  --r-epic:#A275DE; --r-brave:#57C6D6; --r-none:#93897C;
  --shadow:0 1px 0 rgba(0,0,0,.5);
}

*{box-sizing:border-box}
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
.mast p.lede{max-width:60ch; color:var(--muted); margin:26px 0 0; font-size:17px}
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

/* ---- filter bar ---- */
.tools{display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-bottom:26px}
.tools button{
  font-family:"Noto Serif SC",serif; font-size:13.5px; color:var(--muted);
  background:none; border:1px solid var(--rule); padding:6px 14px;
  border-radius:2px; cursor:pointer; transition:color .15s,border-color .15s;
}
.tools button:hover{color:var(--ink)}
.tools button[aria-pressed="true"]{color:var(--ground); background:var(--ink); border-color:var(--ink)}
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
.card.r-brave{--tier:var(--r-brave)}
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
<p class="eyebrow">TRALANCER RPG · Data Pack Codex</p>
<h1>Brand<span class="cn">布兰德 · 宿命之途</span></h1>
<p class="lede">一套围绕卡巴拉生命之树与末世审判展开的生存 RPG 数据包：三十余件带主动/被动技能的武具、可洗练可镶嵌可升级的装备体系、成建制的溺尸与猪灵军团，以及一条十二章的剧情线。</p>
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
<li><a href="#s5"><span class="num">V</span>符文与晶石</a></li>
<li><a href="#s6"><span class="num">VI</span>药剂与材料</a></li>
<li><a href="#s7"><span class="num">VII</span>掉落图鉴</a></li>
<li><a href="#s8"><span class="num">VIII</span>新增装备</a></li>
<li><a href="#s9"><span class="num">IX</span>生物图鉴</a></li>
<li><a href="#s10"><span class="num">X</span>剧情章节</a></li>
<li><a href="#s11"><span class="num">XI</span>指令速查</a></li>
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
<div class="plate-h"><span class="num">III</span><h2>武器图鉴</h2><span class="sub">17 件</span></div>
<p>稀有度由高到低：<strong>神圣 · 恶魔 · 传说 · 史诗</strong>。标记「主动技能」的武器需要<strong>长按右键</strong>发动（物品带 <code>consumable</code> 组件，动作与进食相同）；「被动技能」在命中敌人时按概率自动触发。属性中的百分比为乘算加成。</p>
<div class="tools" role="group" aria-label="按稀有度筛选">
<button type="button" data-f="all" aria-pressed="true">全部</button>
<button type="button" data-f="holy" aria-pressed="false">神圣</button>
<button type="button" data-f="devil" aria-pressed="false">恶魔</button>
<button type="button" data-f="legend" aria-pressed="false">传说</button>
<button type="button" data-f="epic" aria-pressed="false">史诗</button>
<input type="search" id="q" placeholder="搜索名称或技能…" aria-label="搜索武器">
</div>
<div class="grid" id="wgrid">''' + F["weapons"] + '</div></section>')

    # IV armour -----------------------------------------------------------
    a('''<section class="plate" id="s4">
<div class="plate-h"><span class="num">IV</span><h2>护甲图鉴</h2><span class="sub">14 件 · 4 套</span></div>
<p>护甲共四套：<strong>神圣</strong>（圣荆棘冠 / 都灵裹尸布）走减伤与回复，<strong>森焱</strong>套抗火与击退，<strong>王者</strong>套堆生命与伤害吸收，<strong>冰霜</strong>套是过渡装。护甲的被动技能由胸甲上的镶嵌符文提供（见下一节）。</p>
<div class="grid">''' + F["armour"] + '</div></section>')

    # V runes -------------------------------------------------------------
    a('''<section class="plate" id="s5">
<div class="plate-h"><span class="num">V</span><h2>符文与晶石</h2><span class="sub">12 符文 · 6 晶石</span></div>
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
<div class="plate-h"><span class="num">VII</span><h2>掉落图鉴</h2><span class="sub">116 件随机装备</span></div>
<p>前面几节是 <code>give</code> 指令里写死的固定装备；这一节是<strong>战利品表</strong>里的东西——怪物身上穿的、试炼刷怪笼吐出来的、宝库开出来的。它们的属性不是定值，而是每次生成时在一个<strong>区间内随机</strong>，附魔也是随机抽取的，所以同名的两把武器数值可能完全不同。</p>
<h3 class="sub-h">试炼精英武器 · rpg:trial/epic_sword<span class="rolls">6 选 1</span></h3>
<p style="margin:0 0 18px">锻造台用<b>传说冶炼石</b>产出的就是这张表。六件都带技能，且技能标签与固定武器共用同一套处理逻辑。</p>
<div class="grid">''' + F["loot_epic"] + '''</div>
''' + F["loot_trial"] + F["loot_drops"] + F["loot_reward"] + '''
<div class="note"><b>怎么读这些数字：</b>「权重」是同一个池子里被抽中的相对概率；「随机属性范围」是该词条实际会落在的区间，
生成时在区间内均匀取值；「随机附魔 ×N」表示从全部可用附魔里随机抽 N 次，等级也随机。
耐久损耗一栏说明掉落时装备已经是残破状态。</div>
</section>''')

    # VIII new items --------------------------------------------------------
    a('''<section class="plate" id="s8">
<div class="plate-h"><span class="num">VIII</span><h2>新锻装备</h2><span class="sub">7 件 · 出处一览</span></div>
<p>材质包里原本有五套<strong>做好了却从未被引用</strong>的武器贴图（弩两套、弓一套、钓竿一套、剑一套，含全部拉弓/装填/抛竿分帧），
另有两把后补的圣殿双柱。七件装备把它们全部接了上去，格式与既有装备完全一致：稀有度前缀、两行诗、技能栏、属性、附魔、模型编号、技能标签。</p>
<p><strong>技能全部为原创</strong>，没有一件照搬既有效果；实现上仍然走同一套每刻标签索引，
所以新增的每刻命令极少。拿到手后同样能参与洗练、镶嵌、附魔与武器升级。</p>
<p>它们的完整卡片<strong>已并入上面的武器篇</strong>（卡名后带「新锻」标记），此处只列出处对照。</p>
''' + F["extra"] + '''
<div class="note"><b>取得方式：</b><code>/function rpg:command/give/extra</code>。
仍有两张贴图没有用上：<code>rpg:item/baby_crossbows</code>（稚弩的双弩备用图）与
<code>rpg:item/mojang_banner_pattern</code>（旗帜图案，需要额外注册 <code>banner_pattern</code> 才能生效）。<br>
材质包另外注册了一种自定义盔甲纹饰材质 <code>holy</code>，本页所有护甲图标均按游戏内的调色板合成，
染色、纹饰与药水颜色都与实际渲染一致。</div>
</section>''')

    # VII bestiary --------------------------------------------------------
    a('''<section class="plate" id="s9">
<div class="plate-h"><span class="num">IX</span><h2>生物图鉴</h2><span class="sub">4 大阵营</span></div>
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

    # VIII chapters -------------------------------------------------------
    a('''<section class="plate" id="s10">
<div class="plate-h"><span class="num">X</span><h2>剧情章节</h2><span class="sub">进度树 rpg:events</span></div>
<p>十二段剧情以原版<strong>进度</strong>的形式呈现，标题页背景为裂纹深板岩砖。每一章都由「使用物品」触发解锁，构成一条从启示录到登临神座的线性叙事。</p>
<ol class="chapters">
<li><span class="ch">序章</span><div><h3>启示录</h3><p>那一千年完了，撒旦必被从监牢里释放，出来要迷惑四方的列国，那是歌革和玛各，他们聚集起来，他们的人数多如海沙</p></div></li>
<li><span class="ch">第一章</span><div><h3>旧日遗民</h3><p>所有的闪米特人无不盼望弥赛亚的归来，盼望着他从高天之上降下，拯救世人</p></div></li>
<li><span class="ch">第二章</span><div><h3>生命之树</h3><p>当旧日的子民走过十个原质，二十二个神之途径，必将坐在终末的王座上，以纯净的雷光涤荡大地，祓除不臣</p></div></li>
<li><span class="ch">第三章</span><div><h3>真理之冠</h3><p>传说终结那场旧日帝国的战争，正是由那五个家族发起的，他们举起反抗的旌旗，向着高天上的王座，证明着蝼蚁的强大</p></div></li>
<li><span class="ch">第四章</span><div><h3>风暴之息</h3><p>曾经，摩西在西奈山上接受神启，承接了上帝的权柄。如今，权柄傍落自尘世，自风暴的尽头，等待它的主人取回遗失的权柄</p></div></li>
<li><span class="ch">第五章</span><div><h3>莫比乌斯之环</h3><p>命运早已既定，千年前人类选择走出伊甸，千年后人类也将会为他的先祖偿还罪孽</p></div></li>
<li><span class="ch">第六章</span><div><h3>百年战争</h3><p>撒旦从地狱里爬了出来，这场持续百年的战争，是时候画上真正的休止符了</p></div></li>
<li><span class="ch">第七章</span><div><h3>罪与罚</h3><p>罪人的罪孽早已存在，但审判的高歌却从未到来，神早已长眠，无神的国度如同无人怜爱的幼儿</p></div></li>
<li><span class="ch">第八章</span><div><h3>元素之海</h3><p>在一切的起点，上帝将权柄化为元素海，祂象征着虚妄。当虚妄与真实的权柄交织，世界自此中孕育</p></div></li>
<li><span class="ch">第九章</span><div><h3>登临神座</h3><p>最后的弥赛亚啊，您已经走完了卡巴拉生命之树，伊甸中心的荆棘王座即将见证他新的主人。现在，与亚当开启神战吧，神注定只有一个</p></div></li>
<li><span class="ch">最终章</span><div><h3>世界，我们</h3><p>一路上的颠沛流离，都会在一切的重点迎来祂盛大的结局。葬于玫瑰丛的少年，王座之上，再无半点天真</p></div></li>
</ol>
</section>''')

    # IX commands ---------------------------------------------------------
    a('''<section class="plate" id="s11">
<div class="plate-h"><span class="num">XI</span><h2>指令速查</h2><span class="sub">rpg 命名空间</span></div>
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

    a('<footer>TRALANCER RPG · 图鉴依据数据包 rpg 命名空间内的物品与实体数据生成 · Minecraft Java 1.21.11</footer>')
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
