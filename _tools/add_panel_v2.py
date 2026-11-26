# -*- coding: utf-8 -*-
"""新面板（方案书「原质二十二路径与面板重构」第二部分，2026-11-26 用户「全部照默认」）。

- 一套版式：rpg:panel/ui/show 改成「页签条 + 卡片（物品条目）+ 正文 + 底栏」。
  旧页面仍只填 ui.title / ui.body / ui.actions；新键 ui.tab（0..6）与 ui.cards 可选，show 自己补默认。
- 六个页签：生命之树 · 路径 · 力 · 契约与驱魔 · 旅程 · 设置。都走 rpg_panel（人人可用的触发器）。
- 入口：G（原版「快捷操作」）与暂停菜单 → 静态的页签菜单；头颅右键直接开主页（不再要停 12 刻）。
- 主页：一棵会亮的生命之树（位图字体 rpg:tree，十个原质 32 像素印 + 二十二条路径）。
- 选择改造：主柱与觉醒改成并排卡片 + 确认；称号改成下拉单选；技能页顶上加页签条。

排在 add_paths 之后、add_give_boxes 之前（往各系统写好的面板产物里改）。
"""

import io
import json
import os
import re
import sys

import rpg_ui_style as ui
from add_sephira_tiers import TIERS

DP = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "../rpg")
RP = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else None
FUNC = os.path.join(DP, "data/rpg/function")
HERE = os.path.dirname(os.path.abspath(__file__))
GOLD, GLOSS, BODY, NAME, MUTED = ui.BROADCAST_HOLY, ui.BROADCAST_GLOSS, ui.BROADCAST_BODY, ui.BROADCAST_NAME, ui.MUTED
STORE = "storage rpg:panel"
TABS = [  # (编号, 名, 哥特小注, rpg_panel 值)
    (1, "生命之树", "Arbor", 8),
    (2, "路径", "Paths", 20),
    (3, "力", "Virtus", 21),
    (4, "契约与驱魔", "Covenant", 3),
    (5, "旅程", "Journey", 22),
    (6, "设置", "Settings", 6),
]
TAB_OF = {  # 函数 → 页签
    "panel/open": 1, "sephira/page/open": 1,
    "panel/pact": 4, "panel/inquest": 4, "inquest/career": 4,
    "events/jr/body": 5, "events/jr/recipes": 5, "pl/page_m": 5,
    "panel/help": 6,
}
# 生命之树画布（2 倍分辨率：贴图 240×356，屏幕上 120×178）
CW, CH, GH = 240, 356, 178
NODE = {1: (120, 334), 2: (120, 290), 3: (34, 250), 4: (206, 250), 5: (120, 200), 6: (34, 160), 7: (206, 160),
        8: (34, 70), 9: (206, 70), 10: (120, 24)}
DAATH = (120, 116)
TREE_FONT = "rpg:tree"
NEG = ""
COUNT = [0]
# 页签与工作台图标（Codex：paths_ref/art/tab_*.png，缩到 16×16；没到的只显示字）
ICON_DIR = os.path.join(HERE, "paths_ref/art")
ICONS = ["tab_tree", "tab_paths", "tab_force", "tab_pact", "tab_journey", "tab_settings",
         "tab_smelt", "tab_grow", "tab_forge", "tab_convert", "tab_brew"]
TAB_ICON = {1: "tab_tree", 2: "tab_paths", 3: "tab_force", 4: "tab_pact", 5: "tab_journey", 6: "tab_settings"}


def icon(name):
    """图标字形（暗色板之外：#FFFFFE 不被 darken 改色）；图没到返回 None。"""
    if not os.path.exists(os.path.join(ICON_DIR, name + ".png")):
        return None
    return {"text": chr(0xE300 + ICONS.index(name)), "font": "rpg:ui_icons", "color": "#FFFFFE", "bold": False, "italic": False}


def build_icons():
    if not RP:
        return
    from PIL import Image
    import add_daath_art as A
    sheet = Image.new("RGBA", (16 * len(ICONS), 16), (0, 0, 0, 0))
    chars = ""
    for i, name in enumerate(ICONS):
        p = os.path.join(ICON_DIR, name + ".png")
        if os.path.exists(p):
            sheet.alpha_composite(A.colour(Image.open(p), 16).convert("RGBA"), (16 * i, 0))
        chars += chr(0xE300 + i)
    out = os.path.join(RP, "assets/rpg/textures/font/panel")
    os.makedirs(out, exist_ok=True)
    sheet.save(os.path.join(out, "icons.png"))
    with io.open(os.path.join(RP, "assets/rpg/font/ui_icons.json"), "w", encoding="utf-8") as h:
        json.dump({"providers": [{"type": "bitmap", "file": "rpg:font/panel/icons.png", "ascent": 8, "height": 10, "chars": [chars]}]}, h, ensure_ascii=False)


def txt(s, c=BODY, b=False):
    return {"text": s, "color": c, "bold": b, "italic": False}


def dump(v):
    return json.dumps(ui.darken(v), ensure_ascii=False, separators=(",", ":"))


def raw(v):
    return json.dumps(v, ensure_ascii=False, separators=(",", ":"))


def path_of(rel):
    return os.path.join(FUNC, rel.replace("/", os.sep) + ".mcfunction")


def read(rel):
    return io.open(path_of(rel), encoding="utf-8").read()


def write(rel, lines):
    p = path_of(rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if isinstance(lines, list):
        lines = "\n".join(lines).rstrip("\n") + "\n"
    with io.open(p, "w", encoding="utf-8", newline="\n") as h:
        h.write(lines)
    COUNT[0] += 1


def jw(rel, doc):
    p = os.path.join(DP, "data", rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as h:
        json.dump(doc, h, ensure_ascii=False, indent=2)


def hook_tag(kind, name, entry):
    p = os.path.join(DP, "data/minecraft/tags", kind, name + ".json")
    doc = json.load(io.open(p, encoding="utf-8")) if os.path.exists(p) else {"values": []}
    if entry not in doc["values"]:
        doc["values"].append(entry)
    jw("minecraft/tags/%s/%s.json" % (kind, name), doc)


def tab_bar(active):
    """页签条：当前页暗金加粗、带 ◆；其余灰。点了就是 /trigger rpg_panel set N。"""
    parts = [""]
    for i, (n, name, gloss, val) in enumerate(TABS):
        if i:
            parts.append(txt("  ·  ", GLOSS))
        on = n == active
        ic = icon(TAB_ICON[n])
        if ic:
            parts.append(dict(ic, click_event={"action": "run_command", "command": "/trigger rpg_panel set %d" % val}))
            parts.append(txt(" ", MUTED))
        parts.append({"text": ("" if ic else "◆ " if on else "") + name, "color": GOLD if on else MUTED, "bold": on, "italic": False,
                      "click_event": {"action": "run_command", "command": "/trigger rpg_panel set %d" % val},
                      "hover_event": {"action": "show_text", "value": txt(ui.fraktur(gloss), GLOSS)}})
    return {"type": "minecraft:plain_message", "width": 360, "contents": ui.darken(parts)}


# ---- 版式 ---------------------------------------------------------------------

def build_template():
    exit_action = {"label": txt("合上", BODY)}
    bars = [tab_bar(i) for i in range(0, 7)]
    write("panel/v2/load", ["data modify %s bars set value %s" % (STORE, raw(bars)),
                            "scoreboard objectives add rpg_panel_u dummy"])
    hook_tag("function", "load", "rpg:panel/v2/load")
    write("panel/ui/show", [
        "# 面板统一版式（add_panel_v2.py）：页签条 → 卡片 → 正文 → 底栏。ui.tab / ui.cards 可不填",
        "execute unless data %s ui.tab run data modify %s ui.tab set value 0" % (STORE, STORE),
        "execute unless data %s ui.cards run data modify %s ui.cards set value []" % (STORE, STORE),
        "execute unless data %s ui.body[0] run data modify %s ui.body set value [\"\"]" % (STORE, STORE),
        "execute unless data %s ui.actions[0] run data modify %s ui.actions append value %s" % (
            STORE, STORE, dump({"label": txt("‹ 生命之树", BODY), "action": {"type": "minecraft:run_command", "command": "/trigger rpg_panel set 8"}})),
        "data modify %s ui.els set value []" % STORE,
        "function rpg:panel/ui/bar with %s ui" % STORE,
        "data modify %s ui.els append from %s ui.cards[]" % (STORE, STORE),
        "data modify %s ui.els append value {type:\"minecraft:plain_message\",width:340,contents:\"\"}" % STORE,
        "data modify %s ui.els[-1].contents set from %s ui.body" % (STORE, STORE),
        "execute if data %s ui.bw run data modify %s ui.els[-1].width set from %s ui.bw" % (STORE, STORE, STORE),
        "function rpg:panel/ui/show2 with %s ui" % STORE,
        "data remove %s ui.tab" % STORE, "data remove %s ui.cards" % STORE, "data remove %s ui.bw" % STORE])
    write("panel/ui/bar", ["$data modify %s ui.els append from %s bars[$(tab)]" % (STORE, STORE)])
    write("panel/ui/show2", [
        '$dialog show @s {"type":"minecraft:multi_action","title":$(title),"body":$(els),'
        '"actions":$(actions),"columns":2,"exit_action":%s,'
        '"can_close_with_escape":true,"pause":false,"after_action":"close"}' % dump(exit_action)])
    # 各页记上自己的页签
    for rel, tab in TAB_OF.items():
        s = read(rel)
        line = "data modify %s ui.tab set value %d" % (STORE, tab)
        if line in s:
            continue
        a = "function rpg:panel/ui/show with %s ui" % STORE
        assert a in s, rel
        write(rel, s.replace(a, line + "\n" + a))


def build_routes():
    """页签都走 rpg_panel：20 路径、21 力、22 旅程、23 称号。"""
    s = read("panel/tick")
    end = "execute if score @s rpg_panel matches 1.. run scoreboard players set @s rpg_panel 0"
    assert end in s
    if "rpg:paths/page/list" not in s:
        add = ["execute if score @s rpg_panel matches 20 run function rpg:paths/page/list",
               "execute if score @s rpg_panel matches 21 run function rpg:panel/v2/force",
               "execute if score @s rpg_panel matches 22 run function rpg:events/jr/open",
               "execute if score @s rpg_panel matches 23 run function rpg:quest/titles"]
        s = s.replace(end, "\n".join(add) + "\n" + end)
    # 头颅：右键开（rpg:panel/v2/head_use），不再要在手上停 12 刻
    for old in ("execute if entity @s[tag=rpg.h.player_tag1,tag=!rpg.panel.open] run scoreboard players add @s rpg_panel_h 1\n",
                "execute if entity @s[tag=!rpg.panel.open,scores={rpg_panel_h=12..}] run function rpg:panel/open\n"):
        s = s.replace(old, "")
    if "panel/v2/head_swap" not in s:
        s = s.replace("scoreboard players enable @s rpg_panel\n",
                      "scoreboard players enable @s rpg_panel\n"
                      "execute if entity @s[tag=rpg.h.player_tag1] if items entity @s weapon.mainhand minecraft:player_head run function rpg:panel/v2/head_swap\n"
                      "execute if score @s rpg_panel_u matches 1.. run scoreboard players remove @s rpg_panel_u 1\n", 1)
    write("panel/tick", s)
    write("panel/v2/force", ["# 力页签：觉醒了就去技能页，没有就说明",
                             "execute if score @s rpg_force matches 1.. run return run function rpg:force/page/default",
                             "data modify %s ui set value {title:{text:\"\"},body:[],actions:[],tab:3}" % STORE,
                             "data modify %s ui.title set value %s" % (STORE, dump(["", txt("力", GOLD, True), txt(" " + ui.fraktur("Virtus"), GLOSS)])),
                             "data modify %s ui.body append value %s" % (STORE, dump(["", txt("到美丽阶（第 5 阶）会第一次感觉到力：", BODY), txt("圣力", ui.HOLY, True),
                                                                                     txt(" 拿命换，", BODY), txt("魔力", ui.BROADCAST_VOID, True), txt(" 拿魔化换。觉醒以后这里是技能树与技能槽。\n", BODY)])),
                             "execute if score @s rpg_sef matches 5.. run data modify %s ui.actions append value %s" % (STORE, dump(
                                 {"label": txt("觉醒", ui.HOLY, True), "action": {"type": "minecraft:run_command", "command": "/trigger rpg_sef_do set 19"}})),
                             "function rpg:panel/ui/show with %s ui" % STORE])
    # 设置页：HUD 开关回到设置页
    s = read("panel/hud_toggle").replace("function rpg:panel/open", "function rpg:panel/help")
    write("panel/hud_toggle", s)


def build_entries():
    """G 与暂停菜单：静态页签菜单（快捷操作只能放静态对话框）。"""
    actions = []
    for n, name, gloss, val in TABS:
        actions.append({"label": txt(name, GOLD if n == 1 else NAME, n == 1), "tooltip": txt(ui.fraktur(gloss), GLOSS),
                        "action": {"type": "minecraft:run_command", "command": "/trigger rpg_panel set %d" % val}})
    doc = {"type": "minecraft:multi_action",
           "title": ["", txt("玩家面板", GOLD, True), txt(" " + ui.fraktur("Dossier"), GLOSS)],
           "external_title": txt("玩家面板", GOLD, True),
           "body": {"type": "minecraft:plain_message", "width": 300,
                    "contents": txt("选一页。头颅右键、Shift+F（拿着圣徽或罪印）也能直达。", BODY)},
           "actions": actions, "columns": 3, "can_close_with_escape": True, "pause": False, "after_action": "close"}
    jw("rpg/dialog/panel.json", ui.darken(doc))
    hook_tag("dialog", "quick_actions", "rpg:panel")
    hook_tag("dialog", "pause_screen_additions", "rpg:panel")


def build_head():
    """头颅换成一张印着头像的纸：右键是「使用」不是放方块。"""
    consumable = '{consume_seconds:100000f,animation:"none",has_consume_particles:false,sound:"minecraft:intentionally_empty"}'
    write("panel/v2/head_swap", [
        "# 手上的档案头颅（玩家头颅）换成同名、同头像的纸（as 玩家）",
        "data remove %s head" % STORE,
        "data modify %s head.p set from entity @s SelectedItem.components.\"minecraft:profile\"" % STORE,
        "item replace entity @s weapon.mainhand with minecraft:paper[minecraft:item_model=\"rpg:panel/head\",minecraft:consumable=%s,"
        "minecraft:custom_data={player_tag:1b},minecraft:max_stack_size=1,minecraft:enchantment_glint_override=true]" % consumable,
        "execute if data %s head.p run function rpg:panel/v2/head_copy with %s head" % (STORE, STORE)])
    write("panel/v2/head_copy", [
        "$item modify entity @s weapon.mainhand {function:\"minecraft:set_components\",components:{\"minecraft:profile\":$(p)}}"])
    jw("rpg/advancement/panel/head_use.json", {"criteria": {"u": {"trigger": "minecraft:using_item", "conditions": {
        "item": {"predicates": {"minecraft:custom_data": {"player_tag": True}}}}}}, "rewards": {"function": "rpg:panel/v2/head_use"}})
    write("panel/v2/head_use", ["advancement revoke @s only rpg:panel/head_use",
                                "execute unless score @s rpg_panel_u matches 1.. run function rpg:panel/open",
                                "scoreboard players set @s rpg_panel_u 6"])
    # 新领的头颅也走同一个换法：skull_tag → player 之后马上换
    s = read("command/com")
    a = "execute as @a[tag=rpg.h.skull_tag1] at @s if entity @s[tag=!rpg.h.player_tag1] run item modify entity @s weapon.mainhand rpg:command/player\n"
    assert a in s
    if "head_swap" not in s:
        write("command/com", s.replace(a, a + "execute as @a[tag=rpg.h.skull_tag1] if items entity @s weapon.mainhand minecraft:player_head[minecraft:custom_data~{player_tag:1b}] run function rpg:panel/v2/head_swap\n"))
    if RP:
        p = os.path.join(RP, "assets/rpg/items/panel/head.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with io.open(p, "w", encoding="utf-8") as h:
            json.dump({"model": {"type": "minecraft:special", "base": "minecraft:item/template_skull", "model": {"type": "minecraft:player_head"}}}, h)


# ---- 主页：生命之树 -------------------------------------------------------------

def tree_paths():
    import add_paths as AP
    return AP.PATHS, AP.colour


def tree_cells():
    """(字符序号, 名) → 画布层。0 底；1..22 路径开（序号按 PATHS）；23..44 路径走完；45..54 原质到过；55..64 当前阶；65 达阿特。"""
    paths, _ = tree_paths()
    cells = {"base": 0}
    for i, p in enumerate(paths):
        cells["open%d" % p[0]] = 1 + i
        cells["done%d" % p[0]] = 23 + i
    for t in range(1, 11):
        cells["lit%d" % t] = 44 + t
        cells["cur%d" % t] = 54 + t
    cells["daath"] = 65
    return cells


def ch(i):
    return chr(0xE000 + i)


def build_tree_art():
    if not RP:
        return
    from PIL import Image, ImageDraw
    import add_daath_art as A
    paths, colour = tree_paths()
    cells = tree_cells()
    ref = os.path.join(HERE, "daath_ref/tree")
    keys = {t[0]: t[1] for t in TIERS}

    def rgba(c, a=255):
        return tuple(int(x * 255) for x in ui.rgb(c)) + (a,)

    seal = {}
    for t in range(1, 11):
        im = A.colour(Image.open(os.path.join(ref, "seal_%s.png" % keys[t])), 32).convert("RGBA")
        seal[t] = im
    dseal = A.colour(Image.open(os.path.join(ref, "seal_daath.png")), 32).convert("RGBA")

    def grey(im, k=0.45):
        out = im.copy()
        px = out.load()
        for y in range(out.size[1]):
            for x in range(out.size[0]):
                r, g, b, a = px[x, y]
                v = int((r * 0.3 + g * 0.59 + b * 0.11) * k)
                px[x, y] = (v + 10, v + 6, v + 14, a)
        return out

    def place(img, im, xy):
        img.alpha_composite(im, (xy[0] - im.size[0] // 2, xy[1] - im.size[1] // 2))

    def seg(d, a, b, fill, w):
        import math
        (x0, y0), (x1, y1) = a, b
        L = math.hypot(x1 - x0, y1 - y0)
        ux, uy = (x1 - x0) / L, (y1 - y0) / L
        r = 17
        d.line([x0 + ux * r, y0 + uy * r, x1 - ux * r, y1 - uy * r], fill=fill, width=w)

    layers = [None] * 66
    base = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(base)
    for p in paths:
        seg(d, NODE[p[1]], NODE[p[2]], rgba(ui.mix(ui.MUTED, ui.TOOLTIP_GROUND, 0.45)), 3)
    place(base, grey(dseal, 0.3), DAATH)
    for t in range(1, 11):
        place(base, grey(seal[t]), NODE[t])
    layers[0] = base
    for p in paths:
        for kind, fill, w in (("open", rgba(GLOSS), 3), ("done", rgba(colour(p[0])), 3)):
            im = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
            dd = ImageDraw.Draw(im)
            seg(dd, NODE[p[1]], NODE[p[2]], fill, w)
            if kind == "done":       # 亮线外一圈暗金描边
                halo = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
                seg(ImageDraw.Draw(halo), NODE[p[1]], NODE[p[2]], rgba(GLOSS, 150), 5)
                halo.alpha_composite(im)
                im = halo
            layers[cells["%s%d" % (kind, p[0])]] = im
    for t in range(1, 11):
        im = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
        place(im, seal[t], NODE[t])
        layers[cells["lit%d" % t]] = im
        im = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
        x, y = NODE[t]
        dd = ImageDraw.Draw(im)
        dd.ellipse([x - 21, y - 21, x + 21, y + 21], outline=rgba(GOLD), width=2)
        dd.ellipse([x - 24, y - 24, x + 24, y + 24], outline=rgba(GLOSS, 140), width=1)
        layers[cells["cur%d" % t]] = im
    # 界面卡片用的原质印物品（32×32，主柱选择等）
    base = os.path.join(RP, "assets/rpg")
    for d in ("items/panel", "models/item/panel", "textures/item/panel"):
        os.makedirs(os.path.join(base, d), exist_ok=True)
    for t in range(1, 11):
        k = keys[t]
        seal[t].save(os.path.join(base, "textures/item/panel/seal_%s.png" % k))
        with io.open(os.path.join(base, "items/panel/seal_%s.json" % k), "w", encoding="utf-8") as h:
            json.dump({"model": {"type": "minecraft:model", "model": "rpg:item/panel/seal_%s" % k}}, h)
        with io.open(os.path.join(base, "models/item/panel/seal_%s.json" % k), "w", encoding="utf-8") as h:
            json.dump({"parent": "minecraft:item/generated", "textures": {"layer0": "rpg:item/panel/seal_%s" % k}}, h)
    im = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    place(im, dseal, DAATH)
    layers[cells["daath"]] = im
    # 字体图集只有 256×256：每层切成上下两半（240×178），下半用负 ascent 画在同一行再往下 89 格
    cols = 11
    rows = (len(layers) + cols - 1) // cols
    hh = CH // 2
    out = os.path.join(RP, "assets/rpg/textures/font/panel")
    os.makedirs(out, exist_ok=True)
    provs = []
    for half, base_cp, ascent in (("a", 0xE000, 8), ("b", 0xE100, 8 - GH // 2)):
        sheet = Image.new("RGBA", (CW * cols, hh * rows), (0, 0, 0, 0))
        chars = []
        for r in range(rows):
            s = ""
            for c in range(cols):
                i = r * cols + c
                if i < len(layers):
                    part = layers[i].crop((0, 0 if half == "a" else hh, CW, hh if half == "a" else CH))
                    # 位图字形的宽 = 最右一列不透明像素：右下角放一个 alpha 1 的点，每层都量成整宽，退格才对得上
                    if part.getpixel((CW - 1, hh - 1))[3] == 0:
                        part.putpixel((CW - 1, hh - 1), (0, 0, 0, 1))
                    sheet.alpha_composite(part, (c * CW, r * hh))
                    s += chr(base_cp + i)
                else:
                    s += "\u0000"
            chars.append(s)
        sheet.save(os.path.join(out, "tree_%s.png" % half))
        provs.append({"type": "bitmap", "file": "rpg:font/panel/tree_%s.png" % half, "ascent": ascent, "height": GH // 2, "chars": chars})
    provs.append({"type": "space", "advances": {NEG: -(GH * CW // CH + 1)}})
    with io.open(os.path.join(RP, "assets/rpg/font/tree.json"), "w", encoding="utf-8") as h:
        json.dump({"providers": provs}, h, ensure_ascii=False)


def pair(i):
    """一层 = 上半 + 退格 + 下半（净宽 = 一层宽）。"""
    return ch(i) + NEG + chr(0xE100 + i)


def glyph(i):
    return {"text": NEG + pair(i), "font": TREE_FONT, "color": "white"}


def build_home():
    paths, _ = tree_paths()
    cells = tree_cells()
    L = ["# 主页的生命之树（as 玩家）：底图 + 开着的路径 + 走完的路径 + 到过的原质 + 当前阶",
         "data modify %s ui.body append value %s" % (STORE, raw({"text": "", "extra": [{"text": pair(0), "font": TREE_FONT, "color": "white"}]}))]
    T = "data modify %s ui.body[-1].extra append value %s"
    for p in paths:
        n = p[0]
        L.append(("execute if score @s rpg_ps_%d matches 1 run " % n) + T % (STORE, raw(glyph(cells["open%d" % n]))))
        L.append(("execute if score @s rpg_ps_%d matches 2.. run " % n) + T % (STORE, raw(glyph(cells["done%d" % n]))))
    L.append("execute if score @s rpg_daath matches 1 run " + T % (STORE, raw(glyph(cells["daath"]))))
    for t in range(1, 11):
        L.append(("execute if score @s rpg_sef matches %d.. run " % t) + T % (STORE, raw(glyph(cells["lit%d" % t]))))
        L.append(("execute if score @s rpg_sef matches %d run " % t) + T % (STORE, raw(glyph(cells["cur%d" % t]))))
    L.append(T % (STORE, raw({"text": "\n" * (GH // 9 + 1)})))
    # 下一步
    nxt = [
        ("unless score @s rpg_sef matches 1..", "走完新手开局，就进入第 1 阶 · 王国。"),
        ("if score @s rpg_sef matches 2.. unless score @s rpg_pillar matches 1..3", "选一根主柱（下面的按钮）。"),
        ("if score @s rpg_sef matches 5.. if score @s rpg_force matches 0", "你可以觉醒了：圣力或魔力。"),
        ("if score @s rpg_sef matches 7 unless score @s rpg_daath matches 1", "达阿特在等你：「踏入深渊」。"),
        ("if score @s rpg_pa_wt = @s rpg_sef", "综合能力够了：先走完一条连着这一阶的路径。"),
    ]
    L.append("data modify %s nx set value \"\"" % STORE)
    for cond, s in nxt:
        L.append("execute %s run data modify %s nx set value %s" % (cond, STORE, raw(s)))
    L.append("execute unless data %s {nx:\"\"} run function rpg:panel/v2/next with %s" % (STORE, STORE))
    write("panel/v2/tree", L)
    write("panel/v2/next", ["$data modify %s ui.body append value %s" % (STORE, dump(["", txt("下一步　", GOLD, True), txt("$(nx)", NAME), {"text": "\n"}]))])
    # 主页：拿掉已经变成页签的跳转按钮与 HUD 行，树放最上面
    s = read("panel/pages/panel_open")
    keep = []
    paradise = None
    for line in s.rstrip("\n").split("\n"):
        if "ui.actions append" in line and re.search(r'"/trigger (rpg_panel set (1|2|3|5|6|12)|rpg_jr_do set 1)"', line):
            if '"/trigger rpg_panel set 12"' in line:
                paradise = line          # 「失乐园」按钮搬到旅程页
            continue
        if "ui.body append" in line and "HUD " in line:
            continue
        keep.append(line)
    write("panel/pages/panel_open", keep)
    s = read("events/jr/body")
    if paradise and "rpg_panel set 12" not in s:
        a = "data modify %s ui.tab set value 5" % STORE
        assert a in s
        write("events/jr/body", s.replace(a, paradise + "\n" + a))
    s = read("panel/open")
    a = "function rpg:panel/pages/panel_open"
    if "panel/v2/tree" not in s:
        s = s.replace(a, "function rpg:panel/v2/tree\n" + a, 1)
        write("panel/open", s)
    # 设置页：HUD 状态与开关、称号
    s = read("panel/help")
    a = "function rpg:panel/ui/show with %s ui" % STORE
    if "rpg_panel set 23" not in s:
        add = ["execute if entity @s[tag=rpg.panel.hud_off] run data modify %s ui.body append value %s" % (STORE, dump(["", {"text": "\n"}, txt("HUD ", BODY), txt("已隐藏", ui.VERDICTS["封印"], True), {"text": "\n"}])),
               "execute unless entity @s[tag=rpg.panel.hud_off] run data modify %s ui.body append value %s" % (STORE, dump(["", {"text": "\n"}, txt("HUD ", BODY), txt("显示中", ui.READY, True), {"text": "\n"}])),
               "data modify %s ui.actions set value []" % STORE,
               "data modify %s ui.actions append value %s" % (STORE, dump({"label": txt("HUD 开关", GOLD, True), "action": {"type": "minecraft:run_command", "command": "/trigger rpg_panel set 5"}})),
               "data modify %s ui.actions append value %s" % (STORE, dump({"label": txt("称号", GOLD, True), "action": {"type": "minecraft:run_command", "command": "/trigger rpg_panel set 23"}}))]
        write("panel/help", s.replace(a, "\n".join(add) + "\n" + a))
    s = read("panel/pages/panel_help").replace("切到玩家面板并停留片刻就会打开；切走再切回可重开。", "按 G、暂停菜单里的「玩家面板」，或右键档案头颅。")
    s = s.replace('"text":"操作速查"', '"text":"设置"').replace(ui.fraktur("Handbook"), ui.fraktur("Settings"))
    write("panel/pages/panel_help", s)


# ---- 选择改造 -----------------------------------------------------------------

def item_card(item_model, head, lines, colour):
    return {"type": "minecraft:item", "item": {"id": "minecraft:paper", "count": 1, "components": {"minecraft:item_model": item_model}},
            "description": {"contents": ["", txt(head + "\n", colour, True)] + [txt(l + ("\n" if i < len(lines) - 1 else ""), BODY) for i, l in enumerate(lines)],
                            "width": 260},
            "show_decorations": False, "show_tooltip": False, "width": 16, "height": 16}


def confirm(title, body, yes_cmd, no_cmd):
    return {"type": "minecraft:confirmation", "title": title,
            "body": {"type": "minecraft:plain_message", "width": 300, "contents": body},
            "yes": {"label": txt("确定", GOLD, True), "action": {"type": "minecraft:run_command", "command": yes_cmd}},
            "no": {"label": txt("再想想", BODY), "action": {"type": "minecraft:run_command", "command": no_cmd}},
            "can_close_with_escape": True, "pause": False, "after_action": "close"}


def build_choices():
    T = {t[0]: t for t in TIERS}
    # 主柱
    pillars = [(1, "严厉柱", T[6][5], "rpg:panel/seal_geburah", ["进攻：第 3、6 阶伤害各 +5%，第 8 阶攻速 +10%", "技能树里最熟的是「审判 / 毁灭」"], "光辉、严厉、理解"),
               (2, "慈悲柱", T[7][5], "rpg:panel/seal_chesed", ["守护与续命：第 4、7 阶护甲各 +2", "第 9 阶起 6 格内友方抗性 I"], "胜利、慈悲、智慧"),
               (3, "中柱", T[5][5], "rpg:panel/seal_tiphareth", ["控制与机动：第 10 阶力条上限再 +40", "技能树里最熟的是「秘仪 / 诡道」"], "王国、基础、美丽、王冠")]
    title = ["", txt("选择主柱", GOLD, True), txt(" " + ui.fraktur("Pillar"), GLOSS)]
    body = [tab_bar(1)] + [item_card(m, name, lines + ["柱上的原质：" + on + "（碰到它们的路径多给技能点 1）"], c) for n, name, c, m, lines, on in pillars]
    body.append({"type": "minecraft:plain_message", "width": 320, "contents": txt("主柱选了就不能改。", MUTED)})
    acts = []
    for n, name, c, m, lines, on in pillars:
        acts.append({"label": txt(name, c, True), "action": {"type": "minecraft:show_dialog", "dialog": confirm(
            title, ["", txt("以", BODY), txt(name, c, True), txt("为主柱？\n\n", BODY), txt("选了就不能改。", MUTED)],
            "/trigger rpg_sef_do set %d" % n, "/trigger rpg_sef_do set 9")}})
    dlg = {"type": "minecraft:multi_action", "title": title, "body": body, "actions": acts, "columns": 3,
           "exit_action": {"label": txt("以后再选", BODY)}, "can_close_with_escape": True, "pause": False, "after_action": "close"}
    write("sephira/pillar/ask", ["dialog show @s " + dump(dlg)])

    # 觉醒
    forces = [(11, "圣力", ui.HOLY, "rpg:force/holy_sigil", ["拿命换：放圣力、握圣器都会扣生命力", "对恶魔与亡灵更狠；圣徽 Shift+F 打开技能"]),
              (12, "魔力", ui.BROADCAST_VOID, "rpg:force/sin_sigil", ["拿魔化换：击杀和造成伤害回魔力", "魔化涨到一定程度会招来领主；罪印 Shift+F 打开技能"])]
    title = ["", txt("觉醒", GOLD, True), txt(" " + ui.fraktur("Awakening"), GLOSS)]
    body = [tab_bar(3)] + [item_card(m, name, lines, c) for n, name, c, m, lines in forces]
    body.append({"type": "minecraft:plain_message", "width": 320, "contents": txt("觉醒只有一次。", MUTED)})
    acts = [{"label": txt(name, c, True), "action": {"type": "minecraft:show_dialog", "dialog": confirm(
        title, ["", txt("觉醒为", BODY), txt(name, c, True), txt("？\n\n", BODY), txt("只有一次，不能改。", MUTED)],
        "/trigger rpg_sef_do set %d" % n, "/trigger rpg_sef_do set 19")}} for n, name, c, m, lines in forces]
    dlg = {"type": "minecraft:multi_action", "title": title, "body": body, "actions": acts, "columns": 2,
           "exit_action": {"label": txt("以后再说", BODY)}, "can_close_with_escape": True, "pause": False, "after_action": "close"}
    s = read("sephira/force/awaken_ask").rstrip("\n").split("\n")
    s = [l for l in s if "dialog show" not in l] + ["dialog show @s " + dump(dlg)]
    write("sephira/force/awaken_ask", s)

    # 称号：下拉单选
    s = read("quest/titles")
    lines = s.rstrip("\n").split("\n")
    i = next(k for k, l in enumerate(lines) if l.startswith("dialog show @s "))
    d = json.loads(lines[i][len("dialog show @s "):])
    if "inputs" not in d:      # 没改过才改
        lines[i] = "dialog show @s " + raw(titles_dialog(d))
    if "scoreboard players enable @s rpg_q_do" not in lines:
        lines.insert(0, "scoreboard players enable @s rpg_q_do")
    write("quest/titles", lines)
    force_bars()


def titles_dialog(d):
    opts = []
    for a in d["actions"]:
        lab = a["label"]
        name = "".join(c.get("text", "") for c in (lab if isinstance(lab, list) else [lab]) if isinstance(c, dict)).strip()
        m = re.search(r"set (\d+)$", a["action"]["command"])
        opts.append({"id": m.group(1), "display": name or "不戴"})
    body = d["body"] if isinstance(d["body"], list) else [d["body"]]
    d2 = {"type": "minecraft:multi_action", "title": d["title"], "body": [tab_bar(5)] + body,
          "inputs": [{"type": "minecraft:single_option", "key": "t", "label": txt("称号", NAME), "label_visible": True, "width": 260, "options": opts}],
          "actions": [{"label": txt("戴上", GOLD, True), "action": {"type": "minecraft:dynamic/run_command", "template": "/trigger rpg_q_do set $(t)"}},
                      {"label": txt("‹ 旅程", BODY), "action": {"type": "minecraft:run_command", "command": "/trigger rpg_panel set 22"}}],
          "columns": 2, "can_close_with_escape": True, "pause": False, "after_action": "close"}
    return d2


def force_bars():
    """技能页：顶上加页签条。"""
    for k in range(1, 9):
        rel = "force/page/p%d" % k
        s = read(rel)
        if '"body":[' in s:
            continue
        a = '"body":{"type":"minecraft:plain_message"'
        assert a in s, rel
        j = s.index(a) + len('"body":')
        e = match_brace(s, j)
        s = s[:j] + "[" + raw(tab_bar(3)) + "," + s[j:e + 1] + "]" + s[e + 1:]
        write(rel, s)


def match_brace(s, i):
    assert s[i] == "{"
    depth, q, esc = 0, False, False
    for k in range(i, len(s)):
        c = s[k]
        if q:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                q = False
            continue
        if c == '"':
            q = True
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return k
    raise ValueError("unbalanced")


def main():
    build_template()
    build_routes()
    build_entries()
    build_head()
    build_tree_art()
    build_icons()
    build_home()
    build_choices()
    print("panel v2: %d functions written" % COUNT[0])


if __name__ == "__main__":
    main()
