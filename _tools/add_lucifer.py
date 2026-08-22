# -*- coding: utf-8 -*-
"""路西法 -- the fifth demon weapon, built on 1.21.11's real spear item.

Same specification as 亚巴顿 / 别西卜 / 萨麦尔 / 贝利尔: `[DEVIL]` prefix in
#999999, a two-line epithet, one skill block, five enchantments, `unbreakable`
with the tooltip line hidden.

Two things make this one different from every other active in the pack:

* The base is `minecraft:netherite_spear`, a genuine 1.21.11 item, so the model
  follows vanilla's shape -- a `select` on `display_context` giving a flat
  sprite in the GUI and a dedicated in-hand sprite everywhere else.
* It does **not** use the `food` + `consumable` trick.  The spear has a real
  use action of its own ("Charges with Spear" / "Spear lunges" in the language
  file), so `minecraft:using_item` fires on it directly.  That keeps the
  spear's native charge and lunge intact instead of replacing it with an
  eating animation.  The trigger repeats every tick while the charge is held,
  so the reward function is gated behind a short per-player cooldown.
"""

import collections
import io
import json
import os
import sys

import png_tool as P

RP = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
DP = sys.argv[2] if len(sys.argv) > 2 else "../rpg"

RPG_MODELS = os.path.join(RP, "assets/rpg/models/item")
RPG_TEX = os.path.join(RP, "assets/rpg/textures/item")
MC_ITEMS = os.path.join(RP, "assets/minecraft/items")
FUNC = os.path.join(DP, "data/rpg/function")
ADV = os.path.join(DP, "data/rpg/advancement/item")
JAR = r"F:/筑梦 MCBE/HMCL启动器/新建文件夹/versions/1.21.11-Fabric/1.21.11-Fabric.jar"

BASE = "netherite_spear"
CMD = 1110014
NATIVE = 32          # the author's sprite grid, recovered in build_texture()
REACH = 12           # how far the lance travels, in blocks
COOLDOWN = 30        # ticks; `using_item` repeats while the charge is held

# ---------------------------------------------------------------------------
# palette, measured off the author's sprite (share of opaque pixels)
# ---------------------------------------------------------------------------
VIPER = 4895350      # #4AB276  21.1%  bright scale green
DEEP = 2257486       # #22724E  23.0%  body green, the dominant colour
PALE = 9882230       # #96CA76   8.1%  highlight along the spine
VENOM = 14344834     # #DAE282   4.3%  the eyes
BONE = 15918814      # #F2E6DE   2.5%  fangs

P_VIPER = "[0.290,0.698,0.463]"
P_DEEP = "[0.133,0.447,0.306]"
P_PALE = "[0.588,0.792,0.463]"
P_VENOM = "[0.855,0.886,0.510]"

ART = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "lucifer_art", "lucifer.png")


def wj(path, doc):
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def wf(rel, text):
    path = os.path.join(FUNC, rel)
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text.rstrip("\n") + "\n")


# ---------------------------------------------------------------------------
# art
# ---------------------------------------------------------------------------
def _palette(w, h, rgba, limit=24):
    """The sprite's own colours, from confidently-opaque pixels only."""
    hist = collections.Counter()
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            s = (y * w + x) * 4
            if rgba[s + 3] >= 240:
                hist[(rgba[s] >> 2, rgba[s + 1] >> 2, rgba[s + 2] >> 2)] += 1
    pal = []
    for (r, g, b), _n in hist.most_common():
        c = (r << 2 | 2, g << 2 | 2, b << 2 | 2)
        if any(abs(c[0] - p[0]) + abs(c[1] - p[1]) + abs(c[2] - p[2]) < 40 for p in pal):
            continue
        pal.append(c)
        if len(pal) >= limit:
            break
    return pal


def reconstruct(w, h, rgba, n, inset=0.24):
    """Recover an n x n sprite from a smoothly-resampled render.

    The upload is not a clean nearest-neighbour blow-up -- it has been
    resampled, so sampling every k-th pixel (what import_twin_art.py does)
    would pick up edge blending.  Instead each output cell takes the majority
    vote of its interior, snapped to the sprite's own palette: interior pixels
    outnumber the blurred edges, so the original grid comes back exactly.
    """
    pal = _palette(w, h, rgba)

    def snap(c):
        best, bd = pal[0], 1 << 30
        for p in pal:
            d = (c[0] - p[0]) ** 2 + (c[1] - p[1]) ** 2 + (c[2] - p[2]) ** 2
            if d < bd:
                bd, best = d, p
        return best

    step = w / float(n)
    out = bytearray(n * n * 4)
    for cy in range(n):
        for cx in range(n):
            x0 = int(cx * step + step * inset)
            x1 = max(x0 + 1, int((cx + 1) * step - step * inset))
            y0 = int(cy * step + step * inset)
            y1 = max(y0 + 1, int((cy + 1) * step - step * inset))
            votes = collections.Counter()
            solid = total = 0
            for y in range(y0, min(y1, h)):
                for x in range(x0, min(x1, w)):
                    s = (y * w + x) * 4
                    total += 1
                    if rgba[s + 3] >= 128:
                        solid += 1
                        votes[snap((rgba[s], rgba[s + 1], rgba[s + 2]))] += 1
            if total and solid * 2 >= total and votes:
                c = votes.most_common(1)[0][0]
                o = (cy * n + cx) * 4
                out[o], out[o + 1], out[o + 2], out[o + 3] = c[0], c[1], c[2], 255
    return bytes(out)


def mirror(n, rgba):
    out = bytearray(n * n * 4)
    for y in range(n):
        for x in range(n):
            s = (y * n + x) * 4
            d = (y * n + (n - 1 - x)) * 4
            out[d:d + 4] = rgba[s:s + 4]
    return bytes(out)


def build_texture():
    if not os.path.isfile(ART):
        raise SystemExit("missing spear art: put the sprite at %s" % ART)
    if not os.path.isdir(RPG_TEX):
        os.makedirs(RPG_TEX)
    w, h, rgba = P.read(ART)
    gui = reconstruct(w, h, rgba, NATIVE)
    P.write(os.path.join(RPG_TEX, "lucifer.png"), NATIVE, NATIVE, gui)
    # Vanilla draws the in-hand spear along the opposite diagonal to the GUI
    # sprite (compare netherite_spear.png with netherite_spear_in_hand.png), so
    # the in-hand art is the same sprite mirrored -- lossless on pixel art.
    P.write(os.path.join(RPG_TEX, "lucifer_in_hand.png"),
            NATIVE, NATIVE, mirror(NATIVE, gui))
    used = len(set(gui[i * 4:i * 4 + 4] for i in range(NATIVE * NATIVE)
                   if gui[i * 4 + 3]))
    return "%dx%d from %dx%d, %d colours (+ mirrored in-hand)" % (
        NATIVE, NATIVE, w, h, used)


def build_models():
    for name in ("lucifer", "lucifer_in_hand"):
        wj(os.path.join(RPG_MODELS, name + ".json"),
           {"parent": "minecraft:item/spear_in_hand" if name.endswith("in_hand")
            else "item/generated",
            "textures": {"layer0": "rpg:item/" + name}})

    # Mirror vanilla's own structure: flat sprite in the GUI / on the ground,
    # the in-hand model everywhere else.  The whole thing is wrapped in a
    # custom_model_data dispatch so vanilla spears keep working untouched.
    path = os.path.join(MC_ITEMS, BASE + ".json")
    if os.path.isfile(path):
        doc = json.load(io.open(path, encoding="utf-8"))
    else:
        import zipfile
        with zipfile.ZipFile(JAR) as z:
            doc = json.loads(
                z.read("assets/minecraft/items/%s.json" % BASE).decode("utf-8"))

    mine = {"type": "minecraft:select",
            "property": "minecraft:display_context",
            "cases": [{"when": ["gui", "ground", "fixed", "on_shelf"],
                       "model": {"type": "minecraft:model",
                                 "model": "rpg:item/lucifer"}}],
            "fallback": {"type": "minecraft:model",
                         "model": "rpg:item/lucifer_in_hand"}}

    node = doc["model"]
    if (node.get("type") or "").split(":")[-1] != "range_dispatch":
        node = {"type": "minecraft:range_dispatch",
                "property": "minecraft:custom_model_data",
                "fallback": node, "entries": []}
        doc["model"] = node
    entries = node.setdefault("entries", [])
    entries[:] = [e for e in entries if e["threshold"] != CMD]
    entries.append({"threshold": CMD, "model": mine})
    entries.sort(key=lambda e: e["threshold"])
    wj(path, doc)


# ---------------------------------------------------------------------------
# the item
# ---------------------------------------------------------------------------
# Each demon carries its own accent, used for the [DEVIL] prefix, the bold
# half of each epithet and the skill name (萨麦尔 #b00057, 贝利尔 #660099).
# 路西法 takes the deep green of the serpent art.
DEVIL = "#00491c"
RULE = '["",{"text":"+------------------+","italic":false,"color":"white"}]'


def seg(text, colour="white", bold=False):
    return ('{"text":"%s","italic":false,"color":"%s"%s}'
            % (text, colour, ',"bold":true' if bold else ""))


def row(*segs):
    return '["",%s]' % ",".join(segs)


# every one of these five is legal on a spear: spears are in
# #enchantable/melee_weapon and #enchantable/lunge, but NOT in
# #enchantable/sweeping, so sweeping_edge is deliberately absent
LUCIFER = ("give @a %s[" % BASE +
           "custom_name=" + row(seg("[DEVIL]", DEVIL, True),
                                seg("路西法", "aqua")) + ","
           "lore=[" + ",".join([
               RULE,
               row(seg("明亮之星"), seg(" 早晨之子", DEVIL, True)),
               row(seg("伊甸园里盘绕的蛇"), seg(" 众罪之始路西法", DEVIL, True)),
               RULE,
               row(seg("🗡主动技能"), seg("[原罪]", DEVIL, True)),
               row(seg("蓄力沿视线刺出蛇矛，幻魔者尖牙同路破土")),
               row(seg("贯穿者种下原罪：受伤加重，并向近旁蔓延")),
               RULE]) + "],"
           "enchantments={sharpness:4,bane_of_arthropods:5,looting:3,"
           "knockback:1,lunge:2},"
           "attribute_modifiers=["
           # the spear: the longest reach in the pack, paid for in speed
           '{type:"entity_interaction_range",amount:3,operation:add_value,slot:mainhand,id:"rpg:devil/lucifer/0"},'
           '{type:"block_interaction_range",amount:1,operation:add_value,slot:mainhand,id:"rpg:devil/lucifer/1"},'
           '{type:"attack_damage",amount:12,operation:add_value,slot:mainhand,id:"rpg:devil/lucifer/2"},'
           '{type:"attack_speed",amount:-2.9,operation:add_value,slot:mainhand,id:"rpg:devil/lucifer/3"},'
           # 蛇的轻捷，与堕落的代价
           '{type:"movement_speed",amount:0.06,operation:add_multiplied_base,slot:mainhand,id:"rpg:devil/lucifer/4"},'
           '{type:"max_health",amount:-0.15,operation:add_multiplied_base,slot:mainhand,id:"rpg:devil/lucifer/5"}],'
           "unbreakable={},"
           'tooltip_display={hidden_components:["minecraft:unbreakable"]},'
           "custom_model_data={floats:[%d.0f]}," % CMD +
           "custom_data={lucifer_tag:1b,sword_tag:1b,devil_tag:1b}]")


def build_give():
    path = os.path.join(FUNC, "command/give/extra.mcfunction")
    s = io.open(path, encoding="utf-8").read()
    if "路西法" in s:
        return False
    body = [s.rstrip("\n"), "",
            "# 第五位恶魔：路西法（长枪·主动技能［原罪］）",
            LUCIFER, ""]
    io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(body))
    return True


def build_advancement():
    # No food/consumable anywhere: the spear's own charge is a real use action,
    # so using_item fires on it.  The custom_data predicate keeps a plain
    # netherite spear from triggering anything.
    wj(os.path.join(ADV, "lucifer.json"), {
        "criteria": {"requirement": {
            "trigger": "minecraft:using_item",
            "conditions": {"item": {
                "items": "minecraft:" + BASE,
                "predicates": {"minecraft:custom_data": "{lucifer_tag:1b}"},
            }}}},
        "rewards": {"function": "rpg:item/extra/lucifer_trigger"},
    })


# ---------------------------------------------------------------------------
# 原罪 -- the skill
# ---------------------------------------------------------------------------
TRIGGER = """\
# 路西法［原罪］—— 由 rpg:advancement/item/lucifer 在蓄力长枪时触发。
# using_item 在蓄力期间每刻都会响，所以这里压一道 {CD} 刻的冷却，
# 否则按住右键会把经验一路抽干。
advancement revoke @s only rpg:item/lucifer
execute if entity @s[scores={{rpg_luci_use=1..}}] run return 0
execute if entity @s[level=..1] run playsound minecraft:entity.villager.no player @s
execute if entity @s[level=2..] run function rpg:item/extra/lucifer_cast
"""

CAST = """\
# 刺出蛇矛：沿视线一路贯穿，中者种下原罪。
# 长枪本身的攻击范围已是全包最远（+3 格），这一击把它推到 {REACH} 格。
xp add @s -2 levels
scoreboard players set @s rpg_luci_use {CD}
tag @s add rpg.luci.cast
particle dust_color_transition{{from_color:{PALE},to_color:{VIPER},scale:1}} ~ ~1.1 ~ 0.3 0.3 0.3 0.02 14
playsound minecraft:entity.ender_dragon.flap player @a[distance=..24] ~ ~ ~ 0.7 1.7
playsound minecraft:block.sculk_catalyst.bloom player @a[distance=..24] ~ ~ ~ 1 0.6
execute at @s anchored eyes run function rpg:item/extra/lucifer_lance
execute at @s rotated ~ 0 run function rpg:item/extra/lucifer_fangs
tag @s remove rpg.luci.cast
"""

# 幻魔者尖牙沿枪线破土而出。
# `rotated ~ 0` 把俯仰归零，所以无论抬头低头，尖牙都贴着地面一路前推；
# Warmup 逐段加大，于是它们像唤魔者那样一节节炸开，而不是同时弹起。
FANG = ("execute positioned ^ ^ ^{N} run summon minecraft:evoker_fangs ~ ~ ~ "
        '{{Warmup:{W},Tags:["rpg.luci.fang"]}}\n')

FANG_TAIL = """\

# 认主：不设 Owner 的尖牙会连施法者一起咬
execute as @e[tag=rpg.luci.fang] run data modify entity @s Owner set from entity @a[tag=rpg.luci.cast,limit=1,sort=nearest] UUID
tag @e[tag=rpg.luci.fang] remove rpg.luci.fang
playsound minecraft:entity.evoker_fangs.attack hostile @a[distance=..24] ~ ~ ~ 1 0.6
"""

# one unrolled step of the lance -- `positioned ^ ^ ^N` is measured along the
# caster's look vector, so the whole line needs no recursion
STEP = """\
execute positioned ^ ^ ^{N} run particle dust_color_transition{{from_color:{VIPER},to_color:{PALE},scale:1}} ~ ~ ~ 0.17 0.17 0.17 0.02 5
execute positioned ^ ^ ^{N} run particle sculk_soul ~ ~ ~ 0.1 0.1 0.1 0 1
execute positioned ^ ^ ^{N} as @e[distance=..1.4,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,tag=!rpg.luci.sin] at @s run function rpg:item/extra/lucifer_bite
execute positioned ^ ^ ^{N} as @e[distance=..1.4,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run damage @s 9 minecraft:magic by @a[tag=rpg.luci.cast,limit=1,sort=nearest]
"""

BITE = """\
# 种下原罪：10 秒，期间受伤加重，并会向近旁蔓延
tag @s add rpg.luci.sin
scoreboard players set @s rpg_luci_sin 200
scoreboard players set @s rpg_luci_cd 0
effect give @s minecraft:poison 8 1 true
effect give @s minecraft:glowing 10 0 true
particle dust_color_transition{{from_color:{VENOM},to_color:{DEEP},scale:2}} ~ ~1 ~ 0.4 0.5 0.4 0.05 26
particle minecraft:flash{{color:{VENOM}}} ~ ~1.1 ~ 0 0 0 0 1
playsound minecraft:entity.ender_dragon.hurt hostile @a[distance=..20] ~ ~ ~ 0.5 1.9
"""

SPREAD = """\
# 罪的蔓延：把原罪递给最近的一个尚且干净的邻居
execute as @e[distance=0.1..4,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,tag=!rpg.luci.sin,limit=1,sort=nearest] at @s run function rpg:item/extra/lucifer_bite
particle dust_color_transition{{from_color:{DEEP},to_color:{VENOM},scale:1}} ~ ~0.9 ~ 1.6 0.6 1.6 0.02 30
"""

STING = """\
# 带罪者每次挨打都要多还一笔。15 刻的间隔避开无敌帧，也断了自伤触发自伤的循环。
scoreboard players set @s rpg_luci_cd 15
damage @s 4 minecraft:magic
particle dust_color_transition{{from_color:{VENOM},to_color:{VIPER},scale:2}} ~ ~1 ~ 0.35 0.45 0.35 0.05 20
particle minecraft:flash{{color:{VENOM}}} ~ ~1 ~ 0 0 0 0 1
playsound minecraft:entity.warden_ambient player @a[distance=..16] ~ ~ ~ 0.4 2
"""

TICK = """\
# 原罪的存续：加重、蔓延、倒数。
# 由 rpg:item/extra/skills 守卫调用 —— 没人拿枪、场上也没有带罪者时整段跳过。
execute as @e[tag=rpg.luci.sin,tag=rpg.hurt,scores={{rpg_luci_cd=..0}}] at @s run function rpg:item/extra/lucifer_sting
execute as @e[tag=rpg.luci.sin,scores={{rpg_luci_sin=150}}] at @s run function rpg:item/extra/lucifer_spread
execute as @e[tag=rpg.luci.sin,scores={{rpg_luci_sin=100}}] at @s run function rpg:item/extra/lucifer_spread
execute as @e[tag=rpg.luci.sin,scores={{rpg_luci_sin=50}}] at @s run function rpg:item/extra/lucifer_spread
execute as @e[tag=rpg.luci.sin] at @s run particle dust_color_transition{{from_color:{DEEP},to_color:{VIPER},scale:1}} ~ ~1 ~ 0.3 0.4 0.3 0.01 3

execute as @e[tag=rpg.luci.sin,scores={{rpg_luci_cd=1..}}] run scoreboard players remove @s rpg_luci_cd 1
execute as @e[tag=rpg.luci.sin,scores={{rpg_luci_sin=1..}}] run scoreboard players remove @s rpg_luci_sin 1
tag @e[tag=rpg.luci.sin,scores={{rpg_luci_sin=..0}}] remove rpg.luci.sin
# 蓄力冷却
execute as @a[scores={{rpg_luci_use=1..}}] run scoreboard players remove @s rpg_luci_use 1
"""

PAL_ARGS = dict(VIPER=VIPER, PALE=PALE, VENOM=VENOM, DEEP=DEEP,
                REACH=REACH, CD=COOLDOWN)


def build_functions():
    wf("item/extra/lucifer_trigger.mcfunction", TRIGGER.format(**PAL_ARGS))
    wf("item/extra/lucifer_cast.mcfunction", CAST.format(**PAL_ARGS))
    lance = ["# 蛇矛的 %d 段。`positioned ^ ^ ^N` 沿视线取点，所以整条线不需要递归。"
             % REACH]
    for n in range(1, REACH + 1):
        lance.append(STEP.format(N=n, **PAL_ARGS).rstrip("\n"))
    wf("item/extra/lucifer_lance.mcfunction", "\n".join(lance))
    fangs = ["# 幻魔者尖牙：与枪线同路，贴地推进 %d 格。" % REACH]
    for n in range(1, REACH + 1):
        fangs.append(FANG.format(N=n, W=(n - 1) * 2).rstrip("\n"))
    fangs.append(FANG_TAIL)
    wf("item/extra/lucifer_fangs.mcfunction", "\n".join(fangs))
    wf("item/extra/lucifer_bite.mcfunction", BITE.format(**PAL_ARGS))
    wf("item/extra/lucifer_spread.mcfunction", SPREAD.format(**PAL_ARGS))
    wf("item/extra/lucifer_sting.mcfunction", STING.format(**PAL_ARGS))
    wf("item/extra/lucifer.mcfunction", TICK.format(**PAL_ARGS))

    path = os.path.join(FUNC, "item/extra/skills.mcfunction")
    s = io.open(path, encoding="utf-8").read()
    dispatch = (
        "execute if entity @a[tag=rpg.h.lucifer_tag1] "
        "run function rpg:item/extra/lucifer\n"
        # 原罪落在任意生物上，没有类型可先筛；它只持续十秒，
        # 握持判定已经覆盖，不值得每刻为它全场扫一遍
        "")
    if "item/extra/lucifer" not in s:
        io.open(path, "w", encoding="utf-8", newline="\n").write(
            s.rstrip("\n") + "\n" + dispatch)


def add_objectives():
    path = os.path.join(FUNC, "command/soreboard.mcfunction")
    s = io.open(path, encoding="utf-8").read()
    add = [n for n in ("rpg_luci_sin", "rpg_luci_cd", "rpg_luci_use")
           if n not in s]
    if add:
        io.open(path, "w", encoding="utf-8", newline="\n").write(
            s.rstrip("\n") + "\n"
            + "\n".join("scoreboard objectives add %s dummy" % n for n in add) + "\n")
    return add


def register_index():
    """optimize.py learns the per-tick flag index from the original pack's
    legacy `nbt={SelectedItem:...}` selectors, so a brand-new weapon has to add
    its own main-hand flag.  opt_index.py folds these lines afterwards."""
    path = os.path.join(FUNC, "command/index.mcfunction")
    lines = io.open(path, encoding="utf-8").read().split("\n")
    have = set(lines)
    clear = "tag @a remove rpg.h.lucifer_tag1"
    add = ("execute as @a if items entity @s weapon.mainhand "
           "*[minecraft:custom_data~{lucifer_tag:1b}] run tag @s add rpg.h.lucifer_tag1")
    if add in have:
        return False
    out, done_clear, done_add = [], False, False
    for l in lines:
        if not done_clear and l.startswith("execute as @a if items entity @s weapon.mainhand"):
            if clear not in have:
                out.append(clear)
            done_clear = True
        if not done_add and done_clear and l.startswith("## "):
            out.extend([add, ""])
            done_add = True
        out.append(l)
    if not done_add:
        if clear not in have:
            out.append(clear)
        out.append(add)
    io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    return True


def main():
    art = build_texture()
    build_models()
    fresh = build_give()
    build_advancement()
    build_functions()
    indexed = register_index()
    obj = add_objectives()
    print("lucifer: art %s" % art)
    print("lucifer: base=%s cmd=%d give=%s index=%s objectives=%s"
          % (BASE, CMD, "added" if fresh else "already present",
             "registered" if indexed else "present", obj or "-"))


if __name__ == "__main__":
    main()
