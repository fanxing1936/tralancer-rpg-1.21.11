# -*- coding: utf-8 -*-
"""把旧玩家头颅面板升级成多人安全的可点击信息终端。

本脚本必须在驱魔扩展之后运行：面板会读取驱魔职业、真名调查、契约、
侵蚀与佣兵目标，并把所有聊天交互收束到普通玩家可用的 trigger。
"""

import io
import json
import os
import re
import sys


DP = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "../rpg")
FUNC = os.path.join(DP, "data/rpg/function")
MOD = os.path.join(DP, "data/rpg/item_modifier/command")


def fpath(rel):
    return os.path.join(FUNC, rel.replace("/", os.sep))


def read(rel):
    with io.open(fpath(rel), encoding="utf-8") as f:
        return f.read()


def write(rel, content):
    path = fpath(rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content.rstrip("\n") + "\n")


def patch_once(rel, needle, replacement):
    src = read(rel)
    if replacement in src:
        return
    if needle not in src:
        raise RuntimeError("patch anchor missing in %s" % rel)
    write(rel, src.replace(needle, replacement, 1))


def text(value, colour="white", bold=False, click=None):
    out = {"text": value, "color": colour, "italic": False}
    if bold:
        out["bold"] = True
    if click:
        out["click_event"] = {"action": "run_command", "command": click}
    return out


def score(objective, colour="white"):
    return {"score": {"name": "@s", "objective": objective},
            "color": colour, "italic": False}


def row(*parts):
    return [""] + list(parts)


def raw(*parts):
    return json.dumps(row(*parts), ensure_ascii=False, separators=(",", ":"))


def button(label, colour, value):
    return text("[%s]" % label, colour, True,
                "/trigger rpg_panel set %d" % value)


def home_line():
    return "tellraw @s " + raw(text("[返回面板]", "#D4AF37", True,
                                      "/trigger rpg_panel set 8"))


def tell(*parts):
    return "tellraw @s " + raw(*parts)


def build_lore():
    rule = row(text("+-------- 玩家档案 --------+", "#D4AF37", True))
    lore = [
        rule,
        row(text("执档者：", "gray"), {"selector": "@s", "color": "#FFF2A8",
                                     "bold": True, "italic": False}),
        row(text("等级 ", "gray"), score("player_level", "gold"),
            text("　生命 ", "gray"), score("health", "#FF806B")),
        row(text("攻击 ", "gray"), score("player_attack_damage_", "white"),
            text(".", "dark_gray"), score("player_attack_damage", "white"),
            text("　攻速 ", "gray"), score("player_attack_speed_", "white"),
            text(".", "dark_gray"), score("player_attack_speed", "white")),
        row(text("护甲 ", "gray"), score("player_armor_", "#8FC7FF"),
            text(".", "dark_gray"), score("player_armor", "#8FC7FF"),
            text("　韧性 ", "gray"), score("player_armor_toughness_", "#8FC7FF"),
            text(".", "dark_gray"), score("player_armor_toughness", "#8FC7FF")),
        row(text("+------- 驱魔师档案 -------+", "#FFF2A8", True)),
        row(text("驱魔等级 ", "gray"), score("rpg_ex_lvl", "#FFF2A8"),
            text("　阅历 ", "gray"), score("rpg_ex_xp", "#FFD85A")),
        row(text("侵蚀 ", "gray"), score("rpg_taint", "#D596F2"),
            text(" / 100　契约序列 ", "gray"), score("rpg_pact", "#D596F2")),
        row(text("切换至此物品：打开可点击功能页", "#AAB4C3")),
        row(text("切走再切回即可重新打开", "dark_gray")),
        rule,
    ]
    return lore


def write_modifiers():
    lore = build_lore()
    panel_name = ["", text("[档案]", "#D4AF37", True),
                  text("玩家面板", "#FFF2A8", True)]
    common = [
        {
            # player_value 也会运行这一项：存档中的旧 [introduce] 面板无需重领。
            "function": "minecraft:set_name",
            "name": panel_name,
            "entity": "this",
        },
        {
            "function": "minecraft:set_components",
            "components": {
                "minecraft:enchantment_glint_override": True,
                "minecraft:max_stack_size": 1,
            },
        },
        {
            "function": "minecraft:set_lore",
            "lore": lore,
            "mode": "replace_all",
            "entity": "this",
        },
        {
        "function": "set_custom_data",
            "tag": {"player_tag": 1, "rpg_panel": 1},
        },
    ]
    os.makedirs(MOD, exist_ok=True)
    for name, value in (("player.json", common), ("player_value.json", common)):
        with io.open(os.path.join(MOD, name), "w", encoding="utf-8", newline="\n") as f:
            json.dump(value, f, ensure_ascii=False, indent=2)
            f.write("\n")


def patch_panel_item():
    rel = "command/give/weapon.mcfunction"
    src = read(rel)
    lines = src.splitlines()
    found = 0
    new = ("give @a player_head[custom_name=" +
           json.dumps(["", text("[档案]", "#D4AF37", True),
                       text("玩家面板", "#FFF2A8", True)], ensure_ascii=False,
                      separators=(",", ":")) +
           ",enchantment_glint_override=true,max_stack_size=1," +
           "custom_data={skull_tag:1b,rpg_panel:1b}]")
    for i, line in enumerate(lines):
        if line.startswith("give @a player_head[") and "skull_tag:1b" in line:
            lines[i] = new
            found += 1
    if found != 1:
        raise RuntimeError("expected one player panel give, got %d" % found)
    write(rel, "\n".join(lines))


def menu_functions():
    write("panel/open.mcfunction", "\n".join([
        "tag @s add rpg.panel.open",
        "playsound minecraft:item.book.page_turn player @s ~ ~ ~ 0.65 1.25",
        tell(text("+-------- 玩家面板 --------+", "#D4AF37", True)),
        tell(text("驱魔等级 ", "gray"), score("rpg_ex_lvl", "#FFF2A8"),
             text("　阅历 ", "gray"), score("rpg_ex_xp", "#FFD85A"),
             text("　侵蚀 ", "gray"), score("rpg_taint", "#D596F2"),
             text("/100", "dark_gray")),
        tell(button("驱魔师档案", "#FFF2A8", 1), text("  "),
             button("真名调查", "#62D9E8", 2), text("  "),
             button("契约·侵蚀", "#D596F2", 3)),
        tell(button("佣兵小队", "#D4AF37", 4), text("  "),
             button("HUD 开关", "#8FC7FF", 5), text("  "),
             button("操作速查", "#AAB4C3", 6)),
        tell(text("切走再切回面板，可再次打开此页。", "dark_gray")),
        tell(text("+--------------------------+", "#D4AF37", True)),
    ]))

    write("panel/tick.mcfunction", "\n".join([
        "scoreboard players enable @s rpg_panel",
        "scoreboard players add @s rpg_panel 0",
        "execute if entity @s[tag=rpg.h.player_tag1,tag=!rpg.panel.open] run function rpg:panel/open",
        "execute unless entity @s[tag=rpg.h.player_tag1] run tag @s remove rpg.panel.open",
        "execute if score @s rpg_panel matches 1 run function rpg:inquest/career",
        "execute if score @s rpg_panel matches 2 run function rpg:panel/inquest",
        "execute if score @s rpg_panel matches 3 run function rpg:panel/pact",
        "execute if score @s rpg_panel matches 4 run function rpg:panel/squad",
        "execute if score @s rpg_panel matches 5 run function rpg:panel/hud_toggle",
        "execute if score @s rpg_panel matches 6 run function rpg:panel/help",
        "execute if score @s rpg_panel matches 8 run function rpg:panel/open",
        "execute if score @s rpg_panel matches 1.. run scoreboard players set @s rpg_panel 0",
    ]))

    names = [
        (1, "路西法 · 傲慢", "#00491C"),
        (2, "利维坦 · 嫉妒", "#1B4F72"),
        (3, "亚巴顿 · 怠惰", "#6A6A70"),
        (4, "别西卜 · 暴食", "#5A6B1E"),
        (5, "萨麦尔 · 暴怒", "#7B241C"),
        (6, "贝利尔 · 色欲", "#5B2C6F"),
        (7, "玛门 · 贪婪", "#B7950B"),
    ]
    lines = [tell(text("+------ 真名与弱点调查 ------+", "#62D9E8", True))]
    for n, name, colour in names:
        hidden = raw(text("◇ ", "dark_gray"), text(name, colour), text("　见证 ", "gray"),
                     score("rpg_case%d" % n, "white"), text(" / 3", "dark_gray"))
        known = raw(text("◆ ", colour), text(name, colour, True),
                    text("　真名已确认", "#FFF2A8", True))
        lines.append("execute unless entity @s[tag=rpg.name.%d] run tellraw @s %s" % (n, hidden))
        lines.append("execute if entity @s[tag=rpg.name.%d] run tellraw @s %s" % (n, known))
    lines += [tell(text("携带圣器见证三种不同招式，即可确认真名。", "gray")),
              home_line()]
    write("panel/inquest.mcfunction", "\n".join(lines))

    pact_lines = [
        tell(text("+-------- 契约与侵蚀 --------+", "#D596F2", True)),
        tell(text("当前侵蚀：", "gray"), score("rpg_taint", "#D596F2"),
             text(" / 100", "dark_gray")),
        "execute if score @s rpg_pact matches ..0 run tellraw @s " +
        raw(text("当前契约：无", "gray")),
    ]
    for n, name, colour in names:
        pact_lines.append("execute if score @s rpg_pact matches %d run tellraw @s %s" %
                          (n, raw(text("当前契约：", "gray"), text(name, colour, True))))
    pact_lines += [
        "execute if score @s rpg_pact_cd matches 1.. run tellraw @s " +
        raw(text("契约回响冷却：", "gray"), score("rpg_pact_cd", "#D596F2"),
            text(" 刻", "dark_gray")),
        "execute if score @s rpg_pact matches 1..7 unless score @s rpg_pact_cd matches 1.. run tellraw @s " +
        raw(text("契约回响：可用", "#70DB70", True)),
        "execute unless score @s rpg_pact matches 1..7 run tellraw @s " +
        raw(text("契约回响：尚未缔结契约", "dark_gray")),
        "execute if entity @s[tag=rpg.seal.carrier] run tellraw @s " +
        raw(text("封印状态：正携带恶魔遗物", "#62D9E8", True)),
        home_line(),
    ]
    write("panel/pact.mcfunction", "\n".join(pact_lines))

    write("panel/squad.mcfunction", "\n".join([
        "scoreboard players set #panel_count rpg_squad 0",
        "scoreboard players operation #panel_squad rpg_squad = @s rpg_squad",
        "execute if entity @s[tag=rpg.sq.lead] as @e[type=minecraft:husk,tag=rpg.squad] if score @s rpg_squad = #panel_squad rpg_squad run scoreboard players add #panel_count rpg_squad 1",
        "scoreboard players operation @s rpg_sq_n = #panel_count rpg_squad",
        tell(text("+---------- 佣兵小队 ----------+", "#D4AF37", True)),
        "execute unless entity @s[tag=rpg.sq.lead] run tellraw @s " + raw(text("尚未建立佣兵编制。", "gray")),
        "execute if entity @s[tag=rpg.sq.lead] run tellraw @s " +
        raw(text("当前编制：", "gray"), score("rpg_sq_n", "#D4AF37"), text(" / 4", "dark_gray")),
        "execute if entity @s[tag=rpg.sq.lead,scores={rpg_sq_stance=0}] run tellraw @s " + raw(text("全队姿态：跟随", "#70DB70")),
        "execute if entity @s[tag=rpg.sq.lead,scores={rpg_sq_stance=1}] run tellraw @s " + raw(text("全队姿态：驻守", "#8FC7FF")),
        tell(text("募兵旗：招募/晋升　指挥旗：集火/配装/姿态/解雇", "gray")),
        tell(text("姿态切换：潜行 + 指挥旗长按右键", "dark_gray")),
        home_line(),
    ]))

    write("panel/hud_toggle.mcfunction", "\n".join([
        "tag @s remove rpg.panel.was_off",
        "execute if entity @s[tag=rpg.panel.hud_off] run tag @s add rpg.panel.was_off",
        "execute if entity @s[tag=rpg.panel.was_off] run tag @s remove rpg.panel.hud_off",
        "execute unless entity @s[tag=rpg.panel.was_off] run tag @s add rpg.panel.hud_off",
        "execute if entity @s[tag=rpg.panel.hud_off] run title @s actionbar {\"text\":\"\"}",
        "execute if entity @s[tag=rpg.panel.hud_off] run tellraw @s " + raw(text("[玩家面板] HUD 已隐藏", "#8FC7FF", True)),
        "execute unless entity @s[tag=rpg.panel.hud_off] run tellraw @s " + raw(text("[玩家面板] HUD 已恢复", "#70DB70", True)),
        "tag @s remove rpg.panel.was_off",
        home_line(),
    ]))

    write("panel/help.mcfunction", "\n".join([
        tell(text("+---------- 操作速查 ----------+", "#AAB4C3", True)),
        tell(text("面板：切换到玩家面板自动打开；切走再切回可重开。", "gray")),
        tell(text("真名：携带圣器，见证同一恶魔三种不同招式。", "gray")),
        tell(text("仪式：点燃图腾 → 投入媒介 → 宣读真名 → 选择裁决。", "gray")),
        tell(text("告解铃可打断反仪式；圣钉、粉笔与净罪香投入法阵生效。", "gray")),
        tell(text("所有面板按钮仅作用于点击者，不要求管理员权限。", "dark_gray")),
        home_line(),
    ]))


def patch_runtime():
    # 目标在扩展脚本最后生成，因此这里收尾接入。
    sore = read("command/soreboard.mcfunction")
    if "scoreboard objectives add rpg_panel trigger" not in sore:
        anchor = "scoreboard objectives add rpg_ex_choice trigger\n"
        if anchor not in sore:
            raise RuntimeError("rpg_ex_choice objective anchor missing")
        write("command/soreboard.mcfunction",
              sore.replace(anchor, anchor + "scoreboard objectives add rpg_panel trigger\n", 1))

    player_tick = read("inquest/player_tick.mcfunction")
    if "function rpg:panel/tick" not in player_tick:
        write("inquest/player_tick.mcfunction", player_tick + "\nfunction rpg:panel/tick")

    # 档案不再要求玩家记忆 /function；路线、槽位与返回入口都在面板内。
    write("inquest/career.mcfunction", "\n".join([
        "scoreboard players add @s rpg_ex_xp 0",
        "scoreboard players add @s rpg_ex_lvl 0",
        "scoreboard players add @s rpg_ex_path 0",
        "scoreboard players add @s rpg_ex_slots 0",
        "function rpg:inquest/career/sync",
        tell(text("+---------- 驱魔师档案 ----------+", "#FFF2A8", True)),
        tell(text("阶位 ", "gray"), score("rpg_ex_lvl", "white"),
             text("　阅历 ", "gray"), score("rpg_ex_xp", "#FFD85A"),
             text("　仪式槽 ", "gray"), score("rpg_ex_slots", "#62D9E8")),
        "execute if score @s rpg_ex_path matches 0 run tellraw @s " +
        raw(text("选择道路　", "gray"),
            text("[审判]", "#FF806B", True, "/trigger rpg_ex_choice set 21"), text("  "),
            text("[守护]", "#8FC7FF", True, "/trigger rpg_ex_choice set 22"), text("  "),
            text("[秘仪]", "#D596F2", True, "/trigger rpg_ex_choice set 23")),
        "execute if score @s rpg_ex_path matches 1 run tellraw @s " +
        raw(text("审判之道", "#FF806B", True), text("　识破 · 打断 · 处决", "gray")),
        "execute if score @s rpg_ex_path matches 2 run tellraw @s " +
        raw(text("守护之道", "#8FC7FF", True), text("　固阵 · 减损 · 封印", "gray")),
        "execute if score @s rpg_ex_path matches 3 run tellraw @s " +
        raw(text("秘仪之道", "#D596F2", True), text("　净化 · 加速 · 通晓", "gray")),
        "function rpg:inquest/career/claim",
        home_line(),
    ]))
    level_up = read("inquest/career/level_up.mcfunction")
    level_up = level_up.replace("使用 /function rpg:inquest/career 查看档案",
                                "切换至玩家面板，查看驱魔师档案")
    write("inquest/career/level_up.mcfunction", level_up)

    hud = read("hud/hud.mcfunction")
    guard = """# 玩家面板的个人 HUD 开关：状态仍正常结算，只跳过屏幕绘制。
execute if entity @s[tag=rpg.panel.hud_off] run scoreboard players add @s rpg_hud_t 0
execute if entity @s[tag=rpg.panel.hud_off] run scoreboard players add @s rpg_hud_mt 0
execute if entity @s[tag=rpg.panel.hud_off] run scoreboard players add @s rpg_hud_dmt 0
execute if entity @s[tag=rpg.panel.hud_off,scores={rpg_hud_t=1..}] run scoreboard players remove @s rpg_hud_t 1
execute if entity @s[tag=rpg.panel.hud_off,scores={rpg_hud_mt=1..}] run scoreboard players remove @s rpg_hud_mt 1
execute if entity @s[tag=rpg.panel.hud_off,scores={rpg_hud_dmt=1..}] run scoreboard players remove @s rpg_hud_dmt 1
execute if entity @s[tag=rpg.panel.hud_off] run return 0

"""
    if "rpg.panel.hud_off" not in hud:
        write("hud/hud.mcfunction", guard + hud)


def validate():
    assert "scoreboard objectives add rpg_panel trigger" in read("command/soreboard.mcfunction")
    assert "function rpg:panel/tick" in read("inquest/player_tick.mcfunction")
    assert "tag=rpg.panel.hud_off" in read("hud/hud.mcfunction")
    assert "custom_data={skull_tag:1b,rpg_panel:1b}" in read("command/give/weapon.mcfunction")
    for rel in ("panel/open.mcfunction", "panel/tick.mcfunction",
                "panel/inquest.mcfunction", "panel/pact.mcfunction",
                "panel/squad.mcfunction", "panel/hud_toggle.mcfunction",
                "panel/help.mcfunction"):
        body = read(rel)
        assert "tellraw @a" not in body, rel
        assert '"command":"/function ' not in body, rel
    # 所有按钮必须走普通玩家可用的 trigger，禁止偷偷要求 OP。
    clicks = re.findall(r'"command":"([^"]+)"', read("panel/open.mcfunction"))
    assert clicks and all(x.startswith("/trigger rpg_panel set ") for x in clicks)
    print("player panel: lore=%d lines, menu=%d buttons, multiplayer scope=PASS" %
          (len(build_lore()), len(clicks)))


def main():
    write_modifiers()
    patch_panel_item()
    menu_functions()
    patch_runtime()
    validate()


if __name__ == "__main__":
    main()
