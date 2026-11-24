# -*- coding: utf-8 -*-
"""图鉴网页的外观层（用户 2026-11-21「完全重置一版网页……增加对应动效，完全展现你的审美技巧」）。

emit_guide.py 只负责拼内容（物品卡、表格、生物图鉴、调试表……），版式、配色、动效、插图都在这里：
  head(tokens)        <head> 里的字体、样式
  hero(counts)        首屏：插图、镀金标题、光尘画布、七柱色带
  rail()              左侧目录（与原来的锚点 s1…s15 一一对应）
  decorate(html)      给章节开头加罗马数字底纹、描金裂线与插图横幅
  SCRIPT              动效：阅读进度、目录高亮、滚动入场、首屏光尘与视差（全部尊重 prefers-reduced-motion）

设计取向：「暗夜里的泥金典籍」。底色是近黑的暖褐，唯一的高光是圣金；七柱色只出现在属于各柱的地方。
颜色一律从 rpg_ui_style 取（ART-STYLE.md 第 1 节），这里不新造色值。
插图由 Codex 按 guide_art_ref/BRIEF.md 生成，构建时缩成 webp 嵌进页面，整页仍是一个自包含的文件。
没有脚本时内容照常可见：入场动画的隐藏样式只在 <html class="js"> 下生效。
"""
import base64
import io
import os
import re

import rpg_ui_style as ui

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "guide_art_ref")

# 章节 → 横幅插图（Codex，guide_art_ref/raw/）
BANNERS = {"s9": "bestiary", "s8": "exorcism", "s12": "pacts", "s15": "kabbalah", "s10": "lore"}

RAIL = [("s16", "序", "新手教程"), ("s1", "I", "安装与调试"), ("s2", "II", "核心系统"), ("s3", "III", "武器图鉴"), ("s4", "IV", "护甲图鉴"),
        ("s5", "V", "符文与符石"), ("s6", "VI", "药剂与材料"), ("s7", "VII", "掉落总表"), ("s9", "VIII", "生物图鉴"),
        ("s8", "IX", "驱魔体系"), ("s14", "X", "驱魔道具"), ("s12", "XI", "七十二柱契约"), ("s15", "XII", "卡巴拉上位契约"),
        ("s10", "XIII", "破碎大陆"), ("s11", "XIV", "调试指令"), ("s17", "XV", "世界循环"), ("s18", "XVI", "原质与力")]

LORDS = {"lucifer": ("路西法", "傲慢", "Superbia"), "leviathan": ("利维坦", "嫉妒", "Invidia"),
         "abaddon": ("亚巴顿", "怠惰", "Acedia"), "beelzebub": ("别西卜", "暴食", "Gula"),
         "samael": ("萨麦尔", "暴怒", "Ira"), "belial": ("贝利尔", "色欲", "Luxuria"), "mammon": ("玛门", "贪婪", "Avaritia")}


def art_uri(name, width):
    """Codex art as an embedded webp (cached in guide_art_ref/web/); None while the art isn't there yet."""
    src = os.path.join(ART, "raw", name + ".png")
    if not os.path.exists(src):
        return None
    out = os.path.join(ART, "web", "%s.webp" % name)
    if not os.path.exists(out) or os.path.getmtime(out) < os.path.getmtime(src):
        from PIL import Image
        os.makedirs(os.path.dirname(out), exist_ok=True)
        im = Image.open(src).convert("RGB")
        if im.width > width:
            im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        im.save(out, "WEBP", quality=86, method=6)
    with open(out, "rb") as fh:
        return "data:image/webp;base64," + base64.b64encode(fh.read()).decode()


def pillar_tokens():
    return "".join("--p-%s:%s; --pd-%s:%s; " % (p["slug"], p["lit"], p["slug"], p["deep"]) for p in ui.PILLARS)


# ---------------------------------------------------------------------------
CSS = r"""
:root{
  color-scheme:dark;
  --ground:#0E0C0B; --ground-2:#12100F; --surface:#17140F; --surface-2:#1E1A15; --sunk:#0A0908;
  --ink:#ECE5D6; --ink-2:#CFC6B5; --muted:#988D7E; --rule:#2C2620; --rule-2:#3A322A;
  --gold:@@HOLY@@; --gold-lt:@@HOLY_LIGHT@@; --gold-dk:@@HOLY_DARK@@; --gold-soft:#8A7429;
  --ritual:@@RITUAL@@; --cyan:@@CYAN@@; --warn:@@WARN@@;
  @@TIER_TOKENS@@
  @@PILLARS@@
  --ease:cubic-bezier(.2,.7,.1,1);
  --serif:"Noto Serif SC","Songti SC",serif;
  --display:"Cinzel","Noto Serif SC",serif;
  --frak:"UnifrakturCook","Cinzel",serif;
  --mono:"JetBrains Mono",ui-monospace,monospace;
}
*{box-sizing:border-box}
html{background:var(--ground); scroll-behavior:smooth; scroll-padding-top:28px; overflow-x:clip}
body{overflow-x:clip}
body{
  margin:0; color:var(--ink); background:var(--ground);
  font-family:var(--serif); font-weight:300; font-size:16px; line-height:1.9;
  -webkit-font-smoothing:antialiased; text-rendering:optimizeLegibility;
}
/* film grain + a faint warm vignette over the whole page */
body::before{
  content:""; position:fixed; inset:0; pointer-events:none; z-index:100; opacity:.035; transform:translateZ(0);
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1  0 0 0 0 .9  0 0 0 0 .7  0 0 0 .9 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
}
body::after{
  content:""; position:fixed; inset:0; pointer-events:none; z-index:-1;
  background:
    radial-gradient(1200px 700px at 85% -10%, rgba(255,216,90,.05), transparent 60%),
    radial-gradient(900px 900px at -10% 40%, rgba(213,150,242,.025), transparent 60%),
    var(--ground);
}
::selection{background:rgba(255,216,90,.28); color:#fff}
a{color:var(--gold); text-decoration-color:rgba(255,216,90,.35); text-underline-offset:3px}
a:hover{text-decoration-color:var(--gold)}
:focus-visible{outline:2px solid var(--gold); outline-offset:3px}
strong,b{font-weight:600; color:var(--ink)}

/* ---- reading progress ---- */
.progress{position:fixed; top:0; left:0; right:0; height:2px; z-index:90; pointer-events:none}
.progress i{display:block; height:100%; width:100%; transform-origin:0 50%; transform:scaleX(var(--p,0));
  background:linear-gradient(90deg, var(--gold-dk), var(--gold) 70%, var(--gold-lt)); box-shadow:0 0 12px rgba(255,216,90,.6)}

/* ================================================================ hero */
.hero{position:relative; min-height:100vh; min-height:100svh; display:flex; align-items:flex-end; overflow:hidden; isolation:isolate}
.hero-art{position:absolute; inset:-6% 0 -6% 0; z-index:-3; background:var(--sunk) center 38%/cover no-repeat; will-change:transform;
  filter:saturate(.95) brightness(.92)}
.hero-art::after{content:""; position:absolute; inset:0;
  background:
    linear-gradient(90deg, rgba(14,12,11,.92) 0%, rgba(14,12,11,.55) 38%, rgba(14,12,11,.08) 70%, rgba(14,12,11,.35) 100%),
    linear-gradient(0deg, var(--ground) 0%, rgba(14,12,11,.75) 22%, rgba(14,12,11,0) 55%),
    linear-gradient(180deg, rgba(14,12,11,.65) 0%, rgba(14,12,11,0) 18%)}
.hero-rays{position:absolute; inset:0; z-index:-2; pointer-events:none; mix-blend-mode:screen; opacity:.55;
  background:conic-gradient(from 196deg at 66% -12%, transparent 0deg, rgba(255,216,90,.10) 6deg, transparent 12deg, rgba(255,242,168,.07) 19deg, transparent 26deg, rgba(255,216,90,.06) 34deg, transparent 44deg);
  animation:rays 14s ease-in-out infinite alternate}
.hero.off .hero-rays,.hero.off .title .word,.hero.off .cue i{animation-play-state:paused}
@keyframes rays{from{opacity:.35; transform:rotate(-1.2deg)} to{opacity:.65; transform:rotate(1.2deg)}}
#motes{position:absolute; inset:0; z-index:-1; width:100%; height:100%; pointer-events:none}
.hero-in{width:100%; max-width:1240px; margin:0 auto; padding:0 32px 64px}
.eyebrow{font-family:var(--display); font-size:11.5px; letter-spacing:.42em; text-transform:uppercase; color:var(--gold); margin:0 0 22px;
  display:flex; align-items:center; gap:14px}
.eyebrow::before{content:""; width:44px; height:1px; background:linear-gradient(90deg, transparent, var(--gold))}
.title{margin:0; font-family:var(--display); font-weight:700; line-height:.92; letter-spacing:.04em;
  font-size:clamp(56px,11vw,148px); text-transform:uppercase}
.title .word{display:inline-block;
  background:linear-gradient(100deg, #8A6A1E 0%, var(--gold-dk) 22%, var(--gold-lt) 46%, #FFFDF2 50%, var(--gold-lt) 54%, var(--gold) 70%, #7D5E17 100%);
  background-size:250% 100%; background-position:100% 0; -webkit-background-clip:text; background-clip:text; color:transparent;
  filter:drop-shadow(0 2px 30px rgba(255,216,90,.18)); animation:gild 9s ease-in-out 1.6s infinite}
@keyframes gild{0%{background-position:100% 0} 45%,100%{background-position:0 0}}
.heb{display:block; direction:rtl; text-align:left; font-family:var(--serif); font-weight:400; font-size:clamp(18px,2.2vw,26px);
  color:var(--gold-soft); letter-spacing:.06em; margin:18px 0 0}
.cn-title{display:block; font-family:var(--serif); font-weight:500; font-size:clamp(17px,2vw,22px); letter-spacing:.42em; color:var(--ink-2); margin:10px 0 0}
.lede{max-width:56ch; margin:28px 0 0; font-size:17px; color:var(--ink-2); line-height:2}
.lede.sub{font-style:italic; font-size:15.5px; color:var(--muted); margin-top:10px}
.lede strong{color:var(--gold-lt); font-weight:500}
.chips{display:flex; flex-wrap:wrap; gap:8px; margin-top:30px}
.chip{font-family:var(--mono); font-size:11.5px; letter-spacing:.05em; color:var(--muted); padding:6px 12px;
  border:1px solid var(--rule-2); background:rgba(10,9,8,.74); border-radius:2px}
.chip b{color:var(--ink); font-weight:600}
.cue{position:absolute; right:32px; bottom:26px; display:flex; flex-direction:column; align-items:center; gap:8px;
  font-family:var(--display); font-size:10px; letter-spacing:.4em; color:var(--muted); text-decoration:none}
.cue i{display:block; width:1px; height:44px; background:linear-gradient(var(--gold), transparent); transform-origin:top; animation:cue 2.6s var(--ease) infinite}
@keyframes cue{0%{transform:scaleY(0); opacity:1} 70%{transform:scaleY(1); opacity:1} 100%{transform:scaleY(1); opacity:0}}
/* hero entrance */
html.js .hero .in{opacity:0; transform:translateY(22px); animation:rise 1.2s var(--ease) forwards}
/* the title is gilded in: a left-to-right reveal, like gold ink laid down, then the sheen keeps passing */
html.js .title .word{clip-path:inset(-20% 100% -20% 0); animation:ink 1.8s var(--ease) .25s forwards, gild 9s ease-in-out 2.2s infinite}
@keyframes ink{to{clip-path:inset(-20% -2% -20% 0)}}
@keyframes rise{to{opacity:1; transform:none}}

/* ---- seven pillars band ---- */
.pillars{position:relative; max-width:1240px; margin:0 auto; padding:0 32px; display:grid; grid-template-columns:repeat(7,1fr); gap:1px;
  background:transparent}
.pillar{position:relative; padding:22px 14px 18px; text-align:center; border-top:1px solid var(--rule); overflow:hidden; cursor:default}
.pillar::before{content:""; position:absolute; left:50%; top:-1px; width:0; height:2px; background:var(--c); box-shadow:0 0 14px var(--c);
  transform:translateX(-50%); transition:width .7s var(--ease)}
.pillar::after{content:""; position:absolute; inset:0; z-index:-1; opacity:0; transition:opacity .6s var(--ease);
  background:radial-gradient(120% 90% at 50% 0%, color-mix(in srgb, var(--d) 70%, transparent), transparent 70%)}
.pillar:hover::after{opacity:1}
.pillar.in::before,.pillar:hover::before{width:72%}
.pillar .n{display:block; font-family:var(--display); font-size:10px; letter-spacing:.3em; color:var(--muted)}
.pillar .who{display:block; margin-top:6px; font-size:17px; font-weight:600; color:var(--c); letter-spacing:.12em}
.pillar .sin{display:block; font-size:12.5px; color:var(--ink-2); letter-spacing:.3em; margin-top:2px}
.pillar .lat{display:block; font-family:var(--frak); font-size:15px; color:var(--muted); margin-top:6px}
@media(max-width:820px){.pillars{grid-template-columns:repeat(4,1fr); row-gap:4px}}
@media(max-width:520px){.pillar{padding:16px 2px 12px} .pillar .who{font-size:15px; letter-spacing:.06em} .pillar .sin{letter-spacing:.14em; font-size:12px}
  .pillar .lat{display:none} .pillar .n{font-size:9px}}

/* ================================================================ layout */
.wrap{max-width:1240px; margin:0 auto; padding:0 32px 120px}
.layout{display:block}
@media(min-width:1100px){.layout{display:grid; grid-template-columns:200px minmax(0,1fr); gap:64px; align-items:start}}

.rail{display:none}
@media(min-width:1100px){
  .rail{display:block; position:sticky; top:40px; padding-top:96px}
  .rail .cap{font-family:var(--display); font-size:10px; letter-spacing:.38em; color:var(--gold-soft); margin:0 0 18px}
  .rail ol{position:relative; list-style:none; margin:0; padding:0 0 0 16px; display:flex; flex-direction:column; gap:3px;
    border-left:1px solid var(--rule)}
  .rail ol::before{content:""; position:absolute; left:-1px; top:0; width:1px; height:calc(var(--rp,0) * 100%);
    background:linear-gradient(var(--gold-dk), var(--gold)); box-shadow:0 0 8px rgba(255,216,90,.5); transition:height .25s linear}
  .rail a{position:relative; display:flex; gap:12px; align-items:baseline; padding:5px 0; text-decoration:none; color:var(--muted);
    font-size:13.5px; line-height:1.35; transition:color .3s, transform .3s var(--ease)}
  .rail a::before{content:""; position:absolute; left:-20px; top:50%; width:7px; height:7px; margin-top:-3.5px; border:1px solid var(--rule-2);
    background:var(--ground); transform:rotate(45deg); transition:background .3s, border-color .3s, box-shadow .3s}
  .rail a:hover{color:var(--ink); transform:translateX(3px)}
  .rail a.on{color:var(--gold-lt)}
  .rail a.on::before{background:var(--gold); border-color:var(--gold); box-shadow:0 0 10px var(--gold)}
  .rail .num{font-family:var(--display); font-size:10.5px; color:var(--gold-soft); min-width:30px; letter-spacing:.06em}
}

/* ================================================================ plates */
.plate{position:relative; padding-top:120px}
.plate-h{position:relative; display:grid; grid-template-columns:auto minmax(0,1fr); align-items:end; column-gap:22px; margin-bottom:34px; padding-bottom:18px}
.plate-h .num{grid-row:1/3; font-family:var(--display); font-weight:700; font-size:clamp(64px,8vw,104px); line-height:.8; letter-spacing:0;
  color:transparent; -webkit-text-stroke:1px rgba(255,216,90,.42); position:relative}
.plate-h .num::after{content:attr(data-n); position:absolute; left:0; top:0; color:var(--gold); -webkit-text-stroke:0;
  clip-path:inset(100% 0 0 0); transition:clip-path 1.6s var(--ease) .2s; opacity:.9}
.plate.in .plate-h .num::after{clip-path:inset(0 0 0 0)}
.plate-h h2{margin:0; font-family:var(--serif); font-weight:700; font-size:clamp(26px,3vw,34px); letter-spacing:.08em; line-height:1.2}
.plate-h .sub{grid-column:2; font-family:var(--mono); font-size:12px; color:var(--muted); letter-spacing:.04em; margin-top:8px}
.plate-h .crack{position:absolute; left:0; bottom:0; width:100%; height:12px; overflow:visible}
.plate-h .crack path{fill:none; stroke:url(#gildline); stroke-width:1.2; stroke-dasharray:1600; stroke-dashoffset:1600; transition:stroke-dashoffset 2.2s var(--ease) .1s}
.plate.in .plate-h .crack path{stroke-dashoffset:0}
html:not(.js) .plate-h .crack path{stroke-dashoffset:0}
.plate > p{max-width:68ch; color:var(--ink-2)}
.plate > p strong{color:var(--gold-lt); font-weight:500}

/* off-screen plates are not laid out or painted until they come near the viewport */
section.plate{content-visibility:auto; contain-intrinsic-size:auto 2400px}

/* banner art at the head of some plates */
.banner{position:relative; margin:-6px 0 34px; height:clamp(170px,22vw,280px); overflow:hidden; border:1px solid var(--rule)}
.banner img{position:absolute; inset:-12% 0; width:100%; height:124%; object-fit:cover; transform:translateY(var(--py,0)); will-change:transform;
  filter:brightness(.9) saturate(.95)}
.banner::after{content:""; position:absolute; inset:0;
  background:linear-gradient(90deg, var(--ground) 0%, transparent 18%, transparent 82%, var(--ground) 100%),
             linear-gradient(0deg, rgba(14,12,11,.85), transparent 45%)}
.banner figcaption{position:absolute; left:22px; bottom:14px; z-index:1; font-family:var(--frak); font-size:20px; color:var(--gold-lt);
  text-shadow:0 2px 12px #000; letter-spacing:.02em}

/* ---- steps ---- */
.steps{list-style:none; counter-reset:s; margin:0; padding:0; display:flex; flex-direction:column}
.steps li{counter-increment:s; display:grid; grid-template-columns:56px minmax(0,1fr); gap:18px; padding:22px 0; border-bottom:1px solid var(--rule)}
.steps li::before{content:counter(s,decimal-leading-zero); font-family:var(--display); font-size:22px; color:transparent;
  -webkit-text-stroke:1px var(--gold-soft); line-height:1.1}
.steps h3{margin:0 0 4px; font-size:17px; font-weight:600}
.steps p{margin:0; color:var(--muted); font-size:14.5px}
.steps .opt{font-family:var(--display); font-size:9.5px; letter-spacing:.2em; color:var(--gold-soft); border:1px solid var(--rule-2); padding:2px 8px; margin-left:10px; vertical-align:3px}
code,pre{font-family:var(--mono)}
code{font-size:12.8px; background:var(--sunk); padding:2px 6px; border-radius:2px; color:var(--gold-lt); border:1px solid var(--rule)}
.cmd{display:block; margin-top:10px; background:linear-gradient(90deg, rgba(255,216,90,.05), transparent 40%), var(--sunk);
  border:1px solid var(--rule); border-left:2px solid var(--gold); padding:11px 15px; font-size:13px; overflow-x:auto; white-space:pre; color:var(--ink)}

/* ---- system entries ---- */
.sys{display:grid; gap:14px}
@media(min-width:760px){.sys{grid-template-columns:1fr 1fr}}
.sys > div{position:relative; background:linear-gradient(180deg, var(--surface-2), var(--surface)); border:1px solid var(--rule); padding:24px 26px;
  transition:border-color .4s, transform .5s var(--ease), box-shadow .5s}
.sys > div::before{content:""; position:absolute; left:0; top:0; width:28px; height:28px; border-left:1px solid var(--gold); border-top:1px solid var(--gold); opacity:.5}
.sys > div:hover{border-color:var(--rule-2); transform:translateY(-2px); box-shadow:0 18px 40px -24px rgba(0,0,0,.9), 0 0 0 1px rgba(255,216,90,.06)}
.sys h3{margin:0 0 4px; font-size:17px; font-weight:700; letter-spacing:.04em}
.sys .how{font-family:var(--mono); font-size:11.5px; color:var(--gold); letter-spacing:.03em; margin:0 0 12px}
.sys p{margin:0; color:var(--muted); font-size:14.5px}
.sys ul{margin:10px 0 0; padding-left:18px; color:var(--muted); font-size:14px}

/* ---- lore (破碎大陆) ---- */
.scroll-h{text-align:center; margin:0 0 48px; padding:40px 0 34px; position:relative}
.scroll-h::before,.scroll-h::after{content:"✦"; display:block; color:var(--gold-soft); font-size:12px; letter-spacing:1em}
.scroll-h .heb{font-size:34px; line-height:1.5; color:var(--gold); direction:rtl; text-align:center; margin:14px 0 6px}
.scroll-h .rom{font-family:var(--display); font-size:13px; letter-spacing:.34em; color:var(--muted); margin:0 0 16px}
.scroll-h .say{font-size:16px; color:var(--ink); font-style:italic; line-height:2; max-width:58ch; margin:0 auto}
.scroll-h .byline{font-family:var(--mono); font-size:11px; color:var(--muted); margin:20px 0 6px; opacity:.8}
.book{margin:0 0 10px; padding:30px 0 6px; border-top:1px solid var(--rule)}
.book:first-of-type{border-top:none; padding-top:0}
.book > h3{font-family:var(--display); font-size:12px; letter-spacing:.3em; color:var(--gold-soft); margin:0 0 6px; font-weight:400}
.book > h4{margin:0 0 18px; font-size:23px; font-weight:700; color:var(--ink); letter-spacing:.06em}
.book p{margin:0 0 14px; font-size:15px; line-height:2.05; color:var(--ink-2); max-width:68ch}
.book p:first-of-type::first-letter{float:left; font-family:var(--display); font-size:3.3em; line-height:.9; padding:6px 10px 0 0; color:var(--gold)}
.book .cap{font-family:var(--mono); font-size:11px; letter-spacing:.1em; color:var(--muted); margin:24px 0 8px}
.verse{position:relative; margin:22px 0; padding:4px 0 4px 22px; border-left:1px solid var(--gold); font-size:15px; color:var(--gold-lt); font-style:italic; line-height:1.9}
.verse::before{content:"“"; position:absolute; left:8px; top:-18px; font-family:var(--display); font-size:46px; color:rgba(255,216,90,.18)}
.verse cite{display:block; margin-top:6px; font-style:normal; font-family:var(--frak); font-size:15px; color:var(--muted)}
.sins{list-style:none; margin:18px 0 0; padding:0; display:grid; grid-template-columns:repeat(auto-fill,minmax(180px,1fr)); gap:10px}
.sins li{background:var(--surface); border:1px solid var(--rule); padding:13px 16px; font-size:14px}
.sins .who{display:block; font-weight:700; color:var(--ink); margin-bottom:3px}
.sins .what{color:var(--muted); font-size:12.5px}

/* ---- filter bar ---- */
.tools{position:sticky; top:0; z-index:20; display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin:0 0 26px; padding:12px 0;
  background:linear-gradient(180deg, rgba(14,12,11,.98), rgba(14,12,11,.94)); border-bottom:1px solid var(--rule)}
.tools button{font-family:var(--serif); font-size:13.5px; color:var(--muted); background:none; border:1px solid var(--rule-2); padding:6px 15px;
  border-radius:999px; cursor:pointer; transition:color .25s, border-color .25s, background .25s, box-shadow .25s}
.tools button:hover{color:var(--ink); border-color:var(--muted)}
.tools button[aria-pressed="true"]{color:var(--ground); background:var(--ink); border-color:var(--ink)}
.tools button[data-f="holy"]{color:var(--r-holy)}
.tools button[data-f="devil"]{color:var(--ink); background-image:var(--r-devil-band); background-size:70% 2px; background-repeat:no-repeat; background-position:50% 100%}
.tools button[data-f="lgd"]{color:var(--r-lgd)}
.tools button[data-f="legend"]{color:var(--r-legend)}
.tools button[data-f="epic"]{color:var(--r-epic)}
.tools button[aria-pressed="true"][data-f]{color:var(--ground); background-color:var(--ink)}
.tools input{font-family:var(--serif); font-size:13.5px; color:var(--ink); background:var(--sunk); border:1px solid var(--rule-2); padding:7px 14px 7px 34px;
  border-radius:999px; margin-left:auto; min-width:200px; transition:border-color .25s, box-shadow .25s;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 14 14'><circle cx='6' cy='6' r='4.5' fill='none' stroke='%23988D7E' stroke-width='1.3'/><path d='M9.5 9.5 13 13' stroke='%23988D7E' stroke-width='1.3'/></svg>");
  background-repeat:no-repeat; background-position:13px 50%}
.tools input:focus{outline:none; border-color:var(--gold-soft); box-shadow:0 0 0 3px rgba(255,216,90,.08)}
.tools input::placeholder{color:var(--muted)}

/* ---- item cards: the in-game tooltip, gilded ---- */
.grid{display:grid; gap:16px; grid-template-columns:repeat(auto-fill,minmax(290px,1fr))}
.card{position:relative; background:linear-gradient(180deg, var(--surface-2), var(--surface) 60%); border:1px solid var(--rule);
  padding:20px 22px 18px; overflow:hidden; transition:transform .5s var(--ease), border-color .4s, box-shadow .5s}
.card::before{content:""; position:absolute; left:0; right:0; top:0; height:2px; background:var(--tier,var(--r-none)); opacity:.9}
.card::after{content:""; position:absolute; inset:0; pointer-events:none; opacity:0; transition:opacity .5s;
  background:radial-gradient(420px 160px at 50% 0%, color-mix(in srgb, var(--tier,var(--r-none)) 16%, transparent), transparent 70%)}
.card:hover{transform:translateY(-4px); border-color:color-mix(in srgb, var(--tier,var(--r-none)) 35%, var(--rule));
  box-shadow:0 24px 50px -28px #000, 0 0 30px -12px color-mix(in srgb, var(--tier,var(--r-none)) 45%, transparent)}
.card:hover::after{opacity:1}
.card.r-holy{--tier:var(--r-holy)} .card.r-devil{--tier:var(--r-devil)}
.card.r-legend{--tier:var(--r-legend)} .card.r-epic{--tier:var(--r-epic)}
.card.r-lgd{--tier:var(--r-lgd)} .card.r-brave{--tier:var(--r-brave)} .card.r-rite{--tier:var(--r-rite)}
.card.r-ritual{--tier:var(--r-ritual)} .card.r-sephirah{--tier:var(--r-sephirah)}
.card.r-covenant{--tier:var(--r-covenant)} .card.r-authority{--tier:var(--r-authority)}
.card[hidden]{display:none}
.card-h{display:flex; gap:14px; align-items:flex-start; margin-bottom:12px}
.card-id{min-width:0}
.icon{flex:0 0 auto; width:48px; height:48px; padding:7px; image-rendering:pixelated; object-fit:contain;
  background:radial-gradient(circle at 50% 40%, var(--surface-2), var(--sunk)); border:1px solid var(--rule-2); border-radius:2px}
.icon-none{display:block}
.icon-wrap{position:relative; display:inline-block; flex:0 0 auto; line-height:0}
.icon-wrap.glint::after{content:""; position:absolute; inset:7px; pointer-events:none;
  -webkit-mask-image:var(--sprite); mask-image:var(--sprite); -webkit-mask-size:contain; mask-size:contain;
  -webkit-mask-repeat:no-repeat; mask-repeat:no-repeat; -webkit-mask-position:center; mask-position:center;
  background:linear-gradient(115deg, transparent 41%, rgba(168,104,236,.34) 47%, rgba(214,184,255,.60) 50%, rgba(138,84,214,.32) 53%, transparent 59%);
  background-size:300% 300%; background-position:150% 0; mix-blend-mode:screen}
.card.in .icon-wrap.glint::after{animation:glint 2.2s linear .5s 1 both}
.card:hover .icon-wrap.glint::after{animation:glint 2.2s linear infinite}
td.has-icon .icon-wrap.glint::after{inset:3px; animation:none; background-position:44% 0}
@keyframes glint{from{background-position:150% 0} to{background-position:-70% 0}}
h3 .new{display:inline-block; vertical-align:middle; margin-left:9px; font-family:var(--display); font-size:9.5px; letter-spacing:.18em;
  padding:3px 7px 2px; border:1px solid var(--tier,var(--rule)); border-radius:2px; color:var(--tier,var(--muted)); font-weight:400}
td.has-icon{display:flex; gap:10px; align-items:flex-start}
td.has-icon .icon{width:38px; height:38px; padding:3px}
.tier{font-family:var(--display); font-size:10px; letter-spacing:.24em; color:var(--tier,var(--r-none)); display:block; margin-bottom:5px}
.card h3{margin:0; font-size:19px; font-weight:700; color:var(--ink); letter-spacing:.04em; line-height:1.3}
.card .base{margin:3px 0 0; font-family:var(--mono); font-size:11.5px; color:var(--muted)}
.flavour{margin:0 0 14px; font-size:14px; color:var(--muted); font-style:italic; line-height:1.75}
.skill{border-left:1px solid var(--tier,var(--r-none)); padding:1px 0 1px 13px; margin:0 0 13px}
.skill-kind{font-family:var(--display); font-size:9.5px; letter-spacing:.16em; color:var(--muted); margin-right:8px}
.skill-name{font-size:14.5px; font-weight:700; color:var(--tier,var(--ink))}
.skill p{margin:2px 0 0; font-size:13.5px; color:var(--ink-2); line-height:1.7}
.stats{display:grid; grid-template-columns:auto minmax(0,1fr); gap:3px 14px; margin:0; font-size:12.5px; padding-top:12px; border-top:1px dashed var(--rule-2)}
.stats dt{font-family:var(--display); font-size:9.5px; letter-spacing:.13em; color:var(--muted); padding-top:5px}
.stats dd{margin:0; color:var(--ink); font-variant-numeric:tabular-nums; line-height:1.7}
.stats .slot{font-family:var(--mono); font-size:10px; color:var(--muted); margin-left:4px}
.stats code{font-size:11px; background:none; padding:0; border:0; color:var(--muted)}

/* ---- tables ---- */
.tw{overflow-x:auto; border:1px solid var(--rule); background:var(--sunk)}
table{border-collapse:collapse; width:100%; min-width:640px; font-size:14px}
th,td{text-align:left; padding:12px 16px; border-bottom:1px solid var(--rule); vertical-align:top}
thead th{position:sticky; top:0; font-family:var(--display); font-size:10px; letter-spacing:.18em; color:var(--gold-soft); font-weight:500;
  background:var(--surface); border-bottom:1px solid var(--rule-2)}
tbody tr{transition:background .2s}
tbody tr:hover{background:rgba(255,216,90,.035)}
tbody tr:last-child td{border-bottom:none}
.debug-table code{white-space:nowrap}
.debug-table .risk{display:block; width:max-content; margin-top:7px; padding:1px 8px; border:1px solid var(--rule); border-radius:999px; font-family:var(--mono); font-size:10px; letter-spacing:.06em}
.debug-table .risk-safe{color:#8FB8A0; border-color:#31473A; background:#142019}
.debug-table .risk-warn{color:#E4C24A; border-color:#594C22; background:#211C0E}
.debug-table .risk-danger{color:#FF806B; border-color:#6A2D26; background:#25100D}
td.num{font-family:var(--mono); font-variant-numeric:tabular-nums; color:var(--gold-lt)}
td .nm{font-weight:700}
td .sm{display:block; color:var(--muted); font-size:12.5px; margin-top:2px}
.boss td{background:rgba(255,216,90,.03)}

/* ---- folds ---- */
.debug-lords{border:1px solid var(--rule); background:var(--sunk)}
.debug-lords>p{margin:0; padding:12px 18px; border-bottom:1px solid var(--rule)}
.debug-lord{border-bottom:1px solid var(--rule)}
.debug-lord:last-child{border-bottom:0}
.debug-lord summary{cursor:pointer; display:flex; justify-content:space-between; align-items:center; gap:16px; padding:14px 18px; color:var(--ink);
  background:var(--surface); list-style:none; transition:background .25s}
.debug-lord summary:hover{background:var(--surface-2)}
.debug-lord summary::-webkit-details-marker{display:none}
.debug-lord summary:before{content:""; flex:0 0 auto; width:7px; height:7px; border-right:1px solid var(--gold); border-bottom:1px solid var(--gold);
  transform:rotate(-45deg); transition:transform .35s var(--ease); margin-right:4px}
.debug-lord[open] summary:before{transform:rotate(45deg)}
.debug-lord summary b{margin-right:auto}
.debug-lord summary span{color:var(--muted); font-family:var(--mono); font-size:11px}
.debug-lord .tw{border:0; border-top:1px solid var(--rule)}
html.js .debug-lord[open] > :not(summary){animation:unfold .45s var(--ease)}
@keyframes unfold{from{opacity:0; transform:translateY(-6px)} to{opacity:1; transform:none}}

/* ---- chapters ---- */
.chapters{list-style:none; margin:0; padding:0; display:flex; flex-direction:column}
.chapters li{display:grid; grid-template-columns:72px minmax(0,1fr); gap:22px; padding:18px 0; border-bottom:1px solid var(--rule)}
.chapters .ch{font-family:var(--display); font-size:13px; color:var(--gold); letter-spacing:.14em; padding-top:4px}
.chapters h3{margin:0 0 4px; font-size:16.5px; font-weight:600}
.chapters p{margin:0; font-size:14px; color:var(--muted); line-height:1.8}

.sub-h{display:flex; align-items:center; gap:14px; font-family:var(--display); font-size:12px; letter-spacing:.24em; color:var(--gold-lt);
  font-weight:400; margin:44px 0 16px; text-transform:uppercase}
.sub-h::before{content:"✦"; color:var(--gold); font-size:9px}
.sub-h::after{content:""; flex:1; height:1px; background:linear-gradient(90deg, var(--rule-2), transparent)}
.sub-h .rolls{order:3; font-family:var(--mono); letter-spacing:.04em; text-transform:none; font-size:11px; color:var(--muted)}
.plate .sub-h:first-of-type{margin-top:10px}
.dim{color:var(--muted); font-size:12.5px}
.bane{color:#B4636B}
.note{position:relative; border:1px solid var(--rule); background:linear-gradient(90deg, rgba(255,216,90,.045), transparent 55%), var(--surface);
  padding:18px 22px 18px 26px; margin-top:28px; font-size:14.5px; color:var(--ink-2)}
.note::before{content:""; position:absolute; left:0; top:12px; bottom:12px; width:2px; background:linear-gradient(var(--gold), var(--gold-dk))}
.note b{color:var(--gold-lt); font-weight:500}

/* ---- bestiary ---- */
.shots{display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:10px; margin:18px 0 0}
.shots figure{margin:0; background:var(--sunk); border:1px solid var(--rule); overflow:hidden}
.shots img{display:block; width:100%; height:auto; transition:transform .8s var(--ease)}
.shots figure:hover img{transform:scale(1.04)}
.shots figcaption{padding:9px 13px; font-size:12.5px; color:var(--muted); line-height:1.6}
.shots.wide{grid-template-columns:1fr}
.debug-lord .inner{padding:6px 20px 20px; border-top:1px solid var(--rule); font-size:14px; color:var(--ink-2)}
.debug-lord .inner h4{margin:18px 0 6px; font-size:14px; color:var(--gold-lt); font-weight:600; letter-spacing:.04em}
.debug-lord .inner p{margin:6px 0}
.debug-lord .inner ul{margin:6px 0; padding-left:1.25em}
.debug-lord .inner li{margin:3px 0}
.debug-lord .inner .tw{border:1px solid var(--rule); margin:8px 0}
.debug-lord .inner table{min-width:560px; font-size:13.5px}
.models{display:grid; grid-template-columns:repeat(auto-fill,minmax(160px,1fr)); gap:12px; margin:16px 0 0}
.models figure{position:relative; margin:0; border:1px solid var(--rule); overflow:hidden;
  background:radial-gradient(circle at 50% 36%, #2E2721 0%, #15120F 55%, var(--sunk) 80%); display:flex; flex-direction:column; align-items:center; padding:16px 10px 12px;
  transition:border-color .4s, transform .5s var(--ease)}
.models figure::before{content:""; position:absolute; left:50%; bottom:46px; width:60%; height:10px; transform:translateX(-50%); border-radius:50%;
  background:radial-gradient(closest-side, rgba(0,0,0,.7), transparent)}
.models img{position:relative; display:block; height:156px; width:auto; max-width:100%; object-fit:contain; transition:transform .7s var(--ease), filter .7s}
.models figure:hover{border-color:var(--rule-2); transform:translateY(-3px)}
.models figure:hover img{transform:translateY(-6px) scale(1.04); filter:drop-shadow(0 0 18px rgba(255,216,90,.18))}
.models figcaption{margin-top:10px; text-align:center; font-size:13px; color:var(--ink); line-height:1.45}
.models figcaption span{display:block; font-size:11px; color:var(--muted); font-family:var(--mono)}
.oath-icon{width:64px; height:64px; image-rendering:pixelated; background:var(--sunk); border:1px solid var(--rule); padding:8px; box-sizing:content-box; float:left; margin:2px 16px 8px 0}

/* ---- footer ---- */
footer{position:relative; margin-top:120px; padding:42px 0 0; text-align:center; font-size:12.5px; color:var(--muted); font-family:var(--mono); line-height:2}
footer::before{content:"✦  ✦  ✦"; display:block; color:var(--gold-soft); letter-spacing:.6em; margin-bottom:22px}
footer .seal{display:block; font-family:var(--frak); font-size:22px; color:var(--gold); margin-bottom:10px}

/* ================================================================ reveal */
html.js .rv{opacity:0; transform:translateY(26px); transition:opacity .9s var(--ease), transform .9s var(--ease)}
html.js .rv.in{opacity:1; transform:none}
html.js .grid > .rv{transition-delay:calc(var(--i,0) * 45ms)}

@media(max-width:700px){
  .hero-in{padding:96px 20px 56px} .wrap{padding:0 20px 90px} .pillars{padding:0 12px} .cue{display:none}
  .lede{font-size:15.5px} .eyebrow{letter-spacing:.3em; font-size:10.5px}
  .plate{padding-top:84px} .plate-h{column-gap:14px} .tools{margin:0 -20px 22px; padding:10px 20px}
  .tools input{margin-left:0; min-width:0; flex:1 1 100%}
}
@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{animation:none!important; transition:none!important; scroll-behavior:auto!important}
  html.js .rv,html.js .hero .in{opacity:1!important; transform:none!important; filter:none!important}
  html.js .title .word{clip-path:none!important}
  .plate-h .num::after{clip-path:none!important} .plate-h .crack path{stroke-dashoffset:0!important}
  #motes{display:none}
}
"""


def head(tier_tokens):
    css = (CSS.replace("@@TIER_TOKENS@@", tier_tokens).replace("@@PILLARS@@", pillar_tokens())
           .replace("@@HOLY@@", ui.HOLY).replace("@@HOLY_LIGHT@@", ui.HOLY_LIGHT).replace("@@HOLY_DARK@@", ui.HOLY_DARK)
           .replace("@@RITUAL@@", ui.RITUAL).replace("@@CYAN@@", ui.CYAN).replace("@@WARN@@", ui.WARN))
    return ('<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<meta name="theme-color" content="#0E0C0B">\n'
            '<meta name="description" content="破碎大陆（Eretz Ha-Shevarim）—— Minecraft 1.21.11 生存 RPG 数据包图鉴：武具、七宗罪领主、驱魔与契约。">\n'
            '<title>破碎大陆 · Shevarim</title>\n'
            '<script>document.documentElement.classList.add("js")</script>\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Noto+Serif+SC:wght@300;500;700'
            '&family=JetBrains+Mono:wght@400;600&family=UnifrakturCook:wght@700&display=swap">\n'
            '<style>' + css + '</style>\n</head>\n<body>\n'
            '<div class="progress" aria-hidden="true"><i></i></div>\n'
            '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
            '<linearGradient id="gildline" x1="0" x2="1"><stop offset="0" stop-color="%s"/><stop offset=".45" stop-color="%s"/>'
            '<stop offset="1" stop-color="%s" stop-opacity="0"/></linearGradient></defs></svg>\n'
            % (ui.HOLY_DARK, ui.HOLY_LIGHT, ui.HOLY_DARK))


def _letters(word):
    return word


def hero(lede_meta):
    art = art_uri("hero", 1920)
    style = ' style="background-image:url(%s)"' % art if art else ""
    pillars = []
    for i, p in enumerate(ui.PILLARS):
        who, sin, lat = LORDS[p["slug"]]
        pillars.append('<div class="pillar rv" style="--c:%s; --d:%s; transition-delay:%dms"><span class="n">%s</span>'
                       '<span class="who">%s</span><span class="sin">%s</span><span class="lat">%s</span></div>'
                       % (p["lit"], p["deep"], 90 * i, ["I", "II", "III", "IV", "V", "VI", "VII"][i], who, sin, lat))
    return ('<header class="hero" id="top">\n'
            '<div class="hero-art"%s></div><div class="hero-rays"></div><canvas id="motes" aria-hidden="true"></canvas>\n'
            '<div class="hero-in">\n'
            '<p class="eyebrow in" style="animation-delay:.1s">Eretz Ha-Shevarim · Data Pack Codex</p>\n'
            '<h1 class="title"><span class="word">%s</span></h1>\n'
            '<span class="heb in" style="animation-delay:.9s">אֶרֶץ הַשְּׁבָרִים</span>\n'
            '<span class="cn-title in" style="animation-delay:1.05s">破碎大陆 · 碎片之地</span>\n'
            '<p class="lede in" style="animation-delay:1.25s">世界曾经完整，后来因<strong>神陨</strong>、<strong>堕天</strong>与<strong>权柄的分裂</strong>而成为碎片。'
            '这是关于光、混沌、堕落、救赎与人的书——关于<strong>权</strong>与<strong>力</strong>如何分离，又如何在末后的日子重新相遇。</p>\n'
            '<p class="lede sub in" style="animation-delay:1.4s">%s</p>\n'
            '<div class="chips in" style="animation-delay:1.55s"><span class="chip">Minecraft <b>1.21.11</b></span>'
            '<span class="chip">数据包格式 <b>94.1</b></span><span class="chip">资源包格式 <b>75.0</b></span>'
            '<span class="chip">命名空间 <b>rpg</b></span>'
            '<a class="chip" href="#s16" style="text-decoration:none; color:inherit; border-color:var(--gold)">第一次玩？<b>新手教程 →</b></a></div>\n'
            '</div>\n<a class="cue" href="#codex">SCROLL<i></i></a>\n</header>\n'
            '<section class="pillars" aria-label="七宗罪">%s</section>\n'
            % (style, _letters("Shevarim"), lede_meta, "".join(pillars)))


def rail():
    items = "".join('<li><a href="#%s"><span class="num">%s</span>%s</a></li>' % (sid, num, name) for sid, num, name in RAIL)
    return '<nav class="rail" aria-label="目录"><p class="cap">Index</p><ol>%s</ol></nav>' % items


CRACK = ('<svg class="crack" viewBox="0 0 1000 12" preserveAspectRatio="none" aria-hidden="true">'
         '<path d="M0 6 L120 6 L134 2 L150 9 L170 5 L420 6 L436 10 L452 3 L470 6 L760 6 L772 1 L786 8 L800 6 L1000 6"/></svg>')


def decorate(html):
    """Plate openers: the numeral gets a gilt overlay (data-n), a hairline crack draws under the heading,
    and some plates get their banner art.  Plates and cards are marked for the scroll reveal."""
    def opener(m):
        sid, extra, num, rest = m.group(1), m.group(2), m.group(3), m.group(4)
        out = ('<section class="plate" id="%s">\n<div class="plate-h"%s><span class="num" data-n="%s">%s</span>%s%s</div>'
               % (sid, extra, num, num, rest, CRACK))
        name = BANNERS.get(sid)
        uri = art_uri(name, 1600) if name else None
        if uri:
            caption = {"bestiary": "Bestiarium", "exorcism": "Exorcismus", "pacts": "Clavicula Salomonis",
                       "kabbalah": "Etz Chaim", "lore": "Eretz Ha-Shevarim"}[name]
            out += ('\n<figure class="banner rv"><img loading="lazy" alt="" src="%s"><figcaption>%s</figcaption></figure>' % (uri, caption))
        return out
    html = re.sub(r'<section class="plate" id="(s\d+)">\s*<div class="plate-h"([^>]*)><span class="num">([^<]+)</span>(.*?)</div>',
                  opener, html, flags=re.S)
    html = html.replace('<article class="card ', '<article class="rv card ')
    html = re.sub(r'<div class="sys">', '<div class="sys rv">', html)
    html = re.sub(r'<div class="models">', '<div class="models rv">', html)
    html = re.sub(r'<div class="note">', '<div class="note rv">', html)
    return html


SCRIPT = r"""<script>
(function(){
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var doc = document.documentElement;

  /* reading progress + rail progress */
  var bar = document.querySelector('.progress i'), railOl = document.querySelector('.rail ol');
  var plates = [].slice.call(document.querySelectorAll('section.plate[id]'));
  var links = {}; [].slice.call(document.querySelectorAll('.rail a')).forEach(function(a){ links[a.getAttribute('href').slice(1)] = a; });
  var ticking = false;
  function onScroll(){
    if (ticking) return; ticking = true;
    requestAnimationFrame(function(){
      ticking = false;
      /* reads first ... */
      var y = scrollY, vh = innerHeight, h = doc.scrollHeight - vh, p = h > 0 ? y / h : 0;
      var cur = null;
      for (var i = 0; i < plates.length; i++){ if (plates[i].getBoundingClientRect().top < vh * .35) cur = plates[i].id; }
      var moves = [];
      if (!reduce) banners.forEach(function(img){
        var r = img.parentNode.getBoundingClientRect();
        if (r.bottom < 0 || r.top > vh) return;
        moves.push([img, ((r.top + r.height / 2 - vh / 2) / vh * -36).toFixed(1) + 'px']);
      });
      /* ... then writes, so no frame forces a second layout */
      if (bar) bar.style.setProperty('--p', p.toFixed(4));
      if (railOl) railOl.style.setProperty('--rp', p.toFixed(4));
      if (cur !== lastCur){ for (var k in links){ links[k].classList.toggle('on', k === cur); } lastCur = cur; }
      if (!reduce){
        if (heroArt && y < vh * 1.2) heroArt.style.transform = 'translateY(' + (y * .28).toFixed(1) + 'px) scale(1.04)';
        moves.forEach(function(m){ m[0].style.setProperty('--py', m[1]); });
      }
    });
  }
  /* hero + banner parallax */
  var heroArt = document.querySelector('.hero-art'), lastCur;
  var banners = [].slice.call(document.querySelectorAll('.banner img'));
  addEventListener('scroll', onScroll, {passive:true});
  addEventListener('resize', onScroll);
  onScroll();

  /* scroll reveal: one observer for plates, cards and blocks */
  var rv = [].slice.call(document.querySelectorAll('.rv, section.plate'));
  if (!('IntersectionObserver' in window) || reduce){ rv.forEach(function(e){ e.classList.add('in'); }); }
  else {
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){ if (e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
    }, {rootMargin:'0px 0px -8% 0px', threshold:.06});
    rv.forEach(function(e){ io.observe(e); });
    /* stagger cards in a grid by their column */
    [].slice.call(document.querySelectorAll('.grid')).forEach(function(g){
      [].slice.call(g.children).forEach(function(c, i){ c.style.setProperty('--i', i % 4); });
    });
  }

  /* hero motes: gold dust rising through the light, a few falling shards */
  var cv = document.getElementById('motes');
  if (cv && !reduce){
    var ctx = cv.getContext('2d'), W = 0, H = 0, dpr = Math.min(devicePixelRatio || 1, 1.5), motes = [], running = true, last = 0, hero = document.querySelector('.hero');
    var N = innerWidth < 700 ? 28 : 60;
    var cols = ['255,216,90', '255,242,168', '212,175,55'];
    /* one soft glow sprite per colour, drawn once (shadowBlur on every particle every frame was the costly part) */
    var glow = {};
    cols.forEach(function(c){
      var g = document.createElement('canvas'); g.width = g.height = 32; var x = g.getContext('2d');
      var rg = x.createRadialGradient(16, 16, 0, 16, 16, 16);
      rg.addColorStop(0, 'rgba(' + c + ',1)'); rg.addColorStop(.22, 'rgba(' + c + ',.75)'); rg.addColorStop(1, 'rgba(' + c + ',0)');
      x.fillStyle = rg; x.fillRect(0, 0, 32, 32); glow[c] = g;
    });
    function size(){ W = cv.clientWidth; H = cv.clientHeight; cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); }
    function spawn(m, fresh){
      m.x = Math.random() * W; m.y = fresh ? Math.random() * H : H + 10;
      m.r = Math.random() * 1.6 + .4; m.v = Math.random() * .35 + .12; m.d = Math.random() * 6.28; m.a = Math.random() * .6 + .2;
      m.c = cols[(Math.random() * cols.length) | 0]; m.shard = Math.random() < .06;
      if (m.shard){ m.y = fresh ? Math.random() * H : -10; m.v = -(Math.random() * .5 + .35); m.r = Math.random() * 2.5 + 1.5; m.rot = Math.random() * 6.28; }
      return m;
    }
    size(); for (var i = 0; i < N; i++) motes.push(spawn({}, true));
    addEventListener('resize', size);
    new IntersectionObserver(function(es){ running = es[0].isIntersecting; if (hero) hero.classList.toggle('off', !running); if (running){ last = 0; requestAnimationFrame(frame); } }).observe(cv);
    function frame(t){
      if (!running) return;
      var dt = Math.min(48, t - (last || t)); last = t;
      ctx.clearRect(0, 0, W, H);
      for (var i = 0; i < motes.length; i++){
        var m = motes[i];
        m.y -= m.v * dt * .06 * 6; m.d += dt * .0012; m.x += Math.sin(m.d) * .25;
        if (m.shard){
          m.rot += dt * .002; ctx.save(); ctx.translate(m.x, m.y); ctx.rotate(m.rot);
          ctx.fillStyle = 'rgba(' + m.c + ',' + (m.a * .55) + ')'; ctx.fillRect(-m.r, -m.r, m.r * 2, m.r * 2); ctx.restore();
          if (m.y > H + 12) spawn(m, false);
        } else {
          var tw = .55 + .45 * Math.sin(m.d * 3), s = m.r * 7;
          ctx.globalAlpha = m.a * tw; ctx.drawImage(glow[m.c], m.x - s / 2, m.y - s / 2, s, s); ctx.globalAlpha = 1;
          if (m.y < -10) spawn(m, false);
        }
      }
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }
})();
</script>"""
