# -*- coding: utf-8 -*-
"""达阿特试炼 · 影子对决（docs/DAATH-DESIGN.md）。

    python add_daath.py ../rpg ../resourcepack

在 add_sephira.py 之后跑：替换 rpg:sephira/daath/start 的自动放行，改成原质页上的按钮。
  daath_lib     常量与小工具
  daath_world   维度、场地、进出、快照、归还
  daath_frame   召唤、每刻、血量、记住你、调度、夺械、切段
  daath_moves   连招、弓弩与各招
  daath_ults    五个大招、绝境、结局
外观（骨架、盔甲复制、约九十段动作）在 add_daath_model.py；血条与图标在 add_daath_art.py。
"""
import io
import json
import os
import shutil

import daath_frame
import daath_moves
import daath_ults
import daath_world
import rpg_ui_style as ui
from daath_lib import *  # noqa: F401,F403
from daath_lib import B, COUNT, DIM, DP, FUNC, LINES, MID, O, OUT, REF, RP, SIL, VOICE, WHITE, fx, hook_tag, lang_key, msg, txt, w, wj


def shard():
    """[遗物] 达阿特的碎镜：右键看自己的档案，没有数值。"""
    rule = ui.comp(ui.RULE_TEXT, ui.WHITE)
    lore = [rule, ui.comp("深渊里带上来的一片", ui.GRAY), ui.comp("长按右键，看一眼自己", ui.GRAY), rule]
    wj(os.path.join(DP, "data", "rpg", "loot_table", "daath", "shard.json"), {"type": "minecraft:generic", "pools": [{"rolls": 1, "entries": [{
        "type": "minecraft:item", "name": "minecraft:paper", "functions": [{"function": "minecraft:set_components", "components": {
            "minecraft:custom_name": ["", ui.comp("[遗物]", ui.HOLY, True), ui.comp("达阿特的碎镜", ui.WHITE)],
            "minecraft:lore": [["", x] for x in lore], "minecraft:item_model": "rpg:daath_shard", "minecraft:max_stack_size": 1,
            "minecraft:food": {"nutrition": 0, "saturation": 0.0, "can_always_eat": True},
            "minecraft:consumable": {"consume_seconds": 0.8, "animation": "none", "sound": "minecraft:block.amethyst_block.chime", "has_consume_particles": False},
            "minecraft:custom_data": {"rpg_daath_shard": 1}}}]}]}]})
    wj(os.path.join(DP, "data", "rpg", "advancement", "daath", "shard.json"), {
        "criteria": {"u": {"trigger": "minecraft:consume_item", "conditions": {"item": {"predicates": {"minecraft:custom_data": "{rpg_daath_shard:1}"}}}}},
        "rewards": {"function": B + "/shard/use"}})
    rows = [("死过", "rpg_dt_de", " 次"), ("杀过精英", "rpg_el_kill", " 只"), ("裁决", "rpg_ex_rites", " 次"), ("阅历", "rpg_ex_xp", ""), ("原质", "rpg_sef", " 阶"), ("下过深渊", "rpg_dt_win", " 次")]
    parts = [ui.comp("〖碎镜〗", SIL, True), ui.comp("　")]
    for zh, sco, unit in rows:
        parts += [ui.comp(zh + " ", ui.BROADCAST_BODY), {"score": {"name": "@s", "objective": sco}, "color": ui.BROADCAST_NAME, "bold": True}, ui.comp(unit + "　", ui.BROADCAST_BODY)]
    w("shard/use", ["# 用完还回手里", "advancement revoke @s only rpg:daath/shard", "loot give @s loot rpg:daath/shard"] +
      ["scoreboard players add @s %s 0" % r[1] for r in rows] + ["tellraw @s " + ui.row(*parts), "playsound minecraft:block.glass.place player @s ~ ~ ~ 1 0.6"])


def sephira():
    """原质页与达阿特接口。"""
    F = os.path.join(FUNC, "sephira")

    def rd(n):
        return io.open(os.path.join(F, *n.split("/")) + ".mcfunction", encoding="utf-8").read()

    def wr(n, s):
        io.open(os.path.join(F, *n.split("/")) + ".mcfunction", "w", encoding="utf-8", newline="\n").write(s)
    tell = msg([txt("深渊在你脚下打开了。", SIL, True), txt("在「原质」页里按「踏入深渊」。", "#E6DFCF")])
    wr("daath/start", "\n".join([
        "# 到第 7 阶：只提示一次，进不进由玩家在原质页自己按（add_daath.py）。绝不自动传送。",
        "execute if entity @s[tag=rpg.dt.told] run return 0", "tag @s add rpg.dt.told",
        "playsound minecraft:block.end_portal.spawn player @s ~ ~ ~ 0.4 0.6",
        "particle minecraft:squid_ink ~ ~0.1 ~ 1 0.05 1 0.02 40", tell]) + "\n")
    s = rd("daath/pass")
    assert "rpg_ex_xp 100" in s or "rpg_ex_xp 400" in s
    wr("daath/pass", s.replace("rpg_ex_xp 100", "rpg_ex_xp 400").replace("阅历 +100", "阅历 +400"))
    s = rd("press")
    if "daath_fight" not in s:
        wr("press", s + "execute if score #do rpg_sef matches 30 at @s run function %s/ask\nexecute if score #do rpg_sef matches 31 at @s run function %s/go\n" % (B, B))
    s = rd("page/open")
    if "set 30" not in s:
        def btn(label):
            return ("data modify storage rpg:panel ui.actions append value " +
                    json.dumps({"label": ui.comp(label, SIL, True), "action": {"type": "minecraft:run_command", "command": "/trigger rpg_sef_do set 30"}}, ensure_ascii=False, separators=(",", ":")))
        lines = s.rstrip("\n").split("\n")
        k = [i for i, ln in enumerate(lines) if "返回面板" in ln][0]
        lines[k:k] = ["execute if score @s rpg_sef matches 7.. unless score @s rpg_daath matches 1 run " + btn("踏入深渊"),
                      "execute if score @s rpg_daath matches 1 run " + btn("再照一次")]
        wr("page/open", "\n".join(lines) + "\n")


def voices():
    """配音：登记 rpg:vo.daath.*（没有 picks.json 就跳过）。"""
    if not VOICE:
        return 0
    out = os.path.join(RP, "assets", "rpg", "sounds", "vo", "daath")
    os.makedirs(out, exist_ok=True)
    p = os.path.join(RP, "assets", "rpg", "sounds.json")
    doc = json.load(io.open(p, encoding="utf-8"))
    for lid, f in VOICE.items():
        shutil.copyfile(f, os.path.join(out, lid.lower() + ".ogg"))
        doc["vo.daath." + lid.lower()] = {"sounds": [{"name": "rpg:vo/daath/%s" % lid.lower(), "attenuation_distance": 1024}]}
    wj(p, dict(sorted(doc.items())))
    return len(VOICE)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    daath_world.dimension()
    daath_world.arena()
    daath_world.travel()
    daath_frame.build()
    daath_moves.build()
    daath_ults.build()
    daath_ults.despair()
    daath_frame.hooks()
    shard()
    sephira()
    fx.build()
    hook_tag(DP, "load", B + "/load", False)
    hook_tag(DP, "load", B + "/bar/load", False)
    hook_tag(DP, "load", B + "/sec", False)
    hook_tag(DP, "tick", B + "/tick", True)
    n = voices()
    print("daath: %d functions, %d voiced lines" % (COUNT[0], n))


if __name__ == "__main__":
    main()
