# -*- coding: utf-8 -*-
"""七十二柱契约的完整体系：立约、侍奉、深契、清算，加从契（docs/PACT-DESIGN.md）。

add_pact.py 写七柱和书本身；这里写其余一切，并在 add_divine_covenants.py 之后
运行，因为要接管它们之后的 enchanted_book 模型表、面板和 HUD。

现有接口不动：rpg_pact、rpg.pact、rpg_pact_cd、书的 custom_data、pact/p1..p7、
pact/break、pact/burn。新状态全部在 pact/depth/clear 里清掉。
"""

import io
import json
import os
import re
import shutil
import sys

sys.argv = sys.argv[:1] + [os.path.abspath(a) for a in sys.argv[1:]]

import add_demon_minions as dm
import add_pact as pa
from add_seal_relic import HOSTILE_TYPES
import rpg_ui_style as ui
import rpg_vfx as vfx

DP = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath("../rpg")
RP = sys.argv[2] if len(sys.argv) > 2 else os.path.abspath("../resourcepack")
HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "pact_art")
DATA = os.path.join(DP, "data/rpg")
FUNC = os.path.join(DATA, "function")

PILLARS = pa.PILLARS
DEPTH = pa.DEPTH
TIERS = pa.TIER_NAMES
SLUG = pa.SLUG

CD2 = 400                # 二阶技能冷却（刻）
CD3 = 3600               # 化身冷却（刻）
AVATAR = 400             # 附身时长（刻）
SWARM = 100              # 蝇群时长（刻）
BOND_MAX = 100
AFTER_UP = 30            # 升阶后的契合
AFTER_FALL = 50          # 掉阶后的契合
TABOO_BOND = 10
TABOO_TAINT = 5
FLOOR_TAINT = 20         # 一阶契合归零时加的魔化
UP_ITEMS = 4             # 升二阶：五职材料各要几个
PAGE_CHANCE = 0.12
SEAL_CHANCE = 0.04
PAGE_CMD = 1110120       # 柱页：PAGE_CMD + N
SEAL_CMD = 1110200       # 柱印：SEAL_CMD + 编号

HUD_DENY = 80            # 冷却中
HUD_LOCKED = 81          # 阶位不够
HUD_TIER = 82            # 升阶
HUD_TABOO = 84           # 84..90：七柱的违约提示
HUD_FALL = 91            # 掉阶

HOSTILE = "type=#rpg:seal_hostile"
BY = "by @a[tag=rpg.pact.cast,limit=1,sort=nearest]"
# 这些目标的位置由各自的 AI 或仪式决定，技能不能把它们拽走。
MOVABLE = "tag=!rpg.advent,tag=!rpg.pf.boss,tag=!rpg.pf.heart,tag=!rpg.exorcism.bound"

ROLE_NAMES = {r: dm.ROLES[r]["name"] for r in dm.ROLES}
ROLE_ITEMS = [("minecraft:iron_nugget", "铁粒"), ("minecraft:arrow", "箭"),
              ("minecraft:glowstone_dust", "荧石粉"), ("minecraft:spider_eye", "蜘蛛眼"),
              ("minecraft:redstone", "红石粉")]
SEAL_TEXT = {1: "先锋：护甲与击退抗性", 2: "猎手：移速与触及距离",
             3: "司祭：生命上限，并定时回复", 4: "咒使：命中使敌人虚弱",
             5: "处刑者：攻击提升，并追斩残血"}


def write(rel, text):
    path = os.path.join(FUNC, rel.replace("/", os.sep))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    body = text if isinstance(text, str) else "\n".join(text)
    with io.open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(body.rstrip("\n") + "\n")


def read(rel):
    with io.open(os.path.join(FUNC, rel.replace("/", os.sep)), encoding="utf-8") as handle:
        return handle.read()


def write_json(rel, value):
    path = os.path.join(DATA, rel.replace("/", os.sep))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def text(value, color=ui.GRAY, bold=False):
    return {"text": value, "color": color, "bold": bold, "italic": False}


def raw(*parts):
    return json.dumps([""] + list(parts), ensure_ascii=False, separators=(",", ":"))


def spirit_of(seal):
    """编号 1..35 -> (柱, 职, 魔神中文名)。"""
    n, role = (seal - 1) // 5 + 1, (seal - 1) % 5 + 1
    return n, role, dm.LORDS[n]["spirits"][role - 1][1]


def targets(radius, extra=""):
    return "@e[%s,distance=..%d%s]" % (HOSTILE, radius, "," + extra if extra else "")


def hits(radius, fn, extra=""):
    return "execute as %s at @s run function rpg:pact/s/%s" % (targets(radius, extra), fn)


# ---------------------------------------------------------------------------
# 物品：柱页与柱印
# ---------------------------------------------------------------------------
LONG_USE = {
    "food": {"nutrition": 0, "saturation": 0.0, "can_always_eat": True},
    "consumable": {"consume_seconds": 100120.0, "animation": "block",
                   "sound": "minecraft:block.enchantment_table.use",
                   "has_consume_particles": False, "on_consume_effects": []},
}


def components(name, lore, cmd, data, stack):
    return {
        "minecraft:custom_name": name,
        "minecraft:lore": lore,
        "minecraft:custom_model_data": {"floats": [float(cmd)]},
        "minecraft:max_stack_size": stack,
        "minecraft:food": LONG_USE["food"],
        "minecraft:consumable": LONG_USE["consumable"],
        "minecraft:custom_data": data,
    }


def snbt_of(comps):
    parts = []
    for key, value in comps.items():
        short = key.split(":")[1]
        rendered = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        parts.append("%s=%s" % (short, rendered))
    return "minecraft:paper[%s]" % ",".join(parts)


def rule():
    return text(ui.RULE_TEXT, "white")


def say(key, line_):
    """条件不足时直接说缺什么：小提示两秒就没了，玩家不知道为什么没生效。"""
    write("pact/say/%s.mcfunction" % key, [
        "tellraw @s " + raw(text("〖契约〗", ui.VERDICTS["契约"], True),
                            text(" " + ui.fraktur("Covenant"), ui.BROADCAST_GLOSS),
                            text(ui.GAP + line_, ui.BROADCAST_BODY)),
        "playsound minecraft:block.note_block.bass player @s ~ ~ ~ 0.7 0.6",
    ])
    return "function rpg:pact/say/" + key


def page_comps(n, role):
    p = PILLARS[n - 1]
    spirit = dm.LORDS[n]["spirits"][role - 1][1]
    name = ["", text("[柱页]", p["lit"], True), text(spirit, "white")]
    lore = [rule(),
            ["", text("%s麾下%s的残页" % (p["who"], ROLE_NAMES[role]))],
            ["", text("集齐五职各一页后长按右键，合成"), text(p["who"] + "之柱", p["lit"], True)],
            rule()]
    data = "{pact_page:%d,pact_role:%d}" % (n, role)
    return components(name, lore, PAGE_CMD + n, data, 16)


def seal_comps(seal):
    n, role, spirit = spirit_of(seal)
    p = PILLARS[n - 1]
    name = ["", text("[柱印]", p["lit"], True), text(spirit, "white")]
    lore = [rule(),
            ["", text("%s麾下的从属契约" % p["who"])],
            ["", text("🜏从契", "white", True), text("　" + SEAL_TEXT[role], p["lit"])],
            ["", text("与主契约同柱时效果增强", ui.MUTED)],
            rule(),
            ["", text("长按右键镶入契约：魂誓开一槽，真名开两槽")],
            rule()]
    return components(name, lore, SEAL_CMD + seal, "{rpg_seal:%d}" % seal, 1)


def build_items():
    lines = ["", "##柱页"]
    for n in range(1, 8):
        for role in range(1, 6):
            lines.append("give @a %s 1" % snbt_of(page_comps(n, role)))
    lines += ["", "##柱印"]
    gives = []
    for seal in range(1, 36):
        item = snbt_of(seal_comps(seal))
        lines.append("give @a %s 1" % item)
        gives.append("execute if score #seal rpg_pact matches %d run give @s %s 1" % (seal, item))
    write("pact/seal/give.mcfunction", gives)
    src = read("command/give/extra.mcfunction")
    if "##柱页" not in src:
        write("command/give/extra.mcfunction", src.rstrip("\n") + "\n" + "\n".join(lines))


def build_loot():
    """罪仆按所属领主掉柱页和柱印，只掉自己那一份。"""
    for n, lord in dm.LORDS.items():
        for index, spirit in enumerate(lord["spirits"], 1):
            rel = "loot_table/minion/%s/%s.json" % (lord["slug"], spirit[0])
            path = os.path.join(DATA, rel.replace("/", os.sep))
            with io.open(path, encoding="utf-8") as handle:
                table = json.load(handle)
            pools = [p for p in table["pools"] if not p.get("rpg_pact")]
            seal = (n - 1) * 5 + index
            for chance, comps in ((PAGE_CHANCE, page_comps(n, index)), (SEAL_CHANCE, seal_comps(seal))):
                pools.append({
                    "rolls": 1,
                    "conditions": [{"condition": "minecraft:killed_by_player"},
                                   {"condition": "minecraft:random_chance", "chance": chance}],
                    "entries": [{"type": "minecraft:item", "name": "minecraft:paper",
                                 "functions": [{"function": "minecraft:set_components",
                                                "components": comps}]}],
                })
            table["pools"] = pools
            write_json(rel, table)


# ---------------------------------------------------------------------------
# 立约：柱页合书、条款界面、祭品
# ---------------------------------------------------------------------------
def dialog_common(title, body, actions):
    return ui.darken({
        "type": "minecraft:multi_action",
        "title": title,
        "body": {"type": "minecraft:plain_message", "width": 320, "contents": body},
        "actions": actions,
        "columns": 2,
        "exit_action": {"label": text("合上", "gray")},
        "can_close_with_escape": True,
        "pause": False,
        "after_action": "close",
    })


def button(label, value, colour):
    return {"label": text(label, colour, True),
            "action": {"type": "minecraft:run_command", "command": "/trigger rpg_pact_do set %d" % value}}


def line(*parts):
    return list(parts) + [text("\n")]


def blank():
    return text("\n")


def tagged(label, *parts):
    """§2.2 的一行：🜏标签白色加粗，后面才是内容。"""
    return line(text("🜏" + label, "white", True), text("　"), *parts)


def dialog_title(prefix, p):
    return ["", text(prefix, p["lit"], True), text(p["who"] + "之柱", "white"),
            text(" " + ui.fraktur(ui.SIN_ENGLISH[p["sin"]]), ui.BROADCAST_GLOSS)]


def terms_body(p):
    """第一层是恩赐和枷锁，第二层是力量，第三层是戒律，最轻的是祭品和说明。"""
    d = DEPTH[p["n"]]
    out = []
    out += tagged("恩赐", text(d["boon"][0], p["lit"], True))
    out += tagged("枷锁", text(d["bane"][0], ui.WARN, True))
    out += [blank()]
    out += tagged("力量", text("[%s]" % p["power"], p["lit"], True))
    out += line(text(p["power_text"]))
    out += [blank()]
    out += tagged("供奉", text(d["oath"]))
    out += tagged("禁忌", text(d["taboo"]))
    out += [blank()]
    out += line(text("祭品　", ui.MUTED), text("%s ×%d" % (d["tribute"][1], pa.TRIBUTE), "white", True),
                text("　持有 ", ui.MUTED), text("$(have)", "white", True))
    out += [text("守约累积契合，犯禁扣契合并加魔化", ui.MUTED)]
    return out


def build_sign():
    for p in PILLARS:
        n, d = p["n"], DEPTH[p["n"]]
        # 对话框写在函数里，不注册进数据包：注册表要重进存档才更新，/reload 换不掉。
        dialog = dialog_common(dialog_title("[契约]", p), terms_body(p), [button("签下", 10 + n, p["lit"])])
        write("pact/ui/terms%d.mcfunction" % n, [
            "tag @s add rpg.pact.ui",
            "scoreboard players enable @s rpg_pact_do",
            "execute store result storage rpg:pact ui.have int 1 run clear @s %s[!minecraft:custom_data] 0" % d["tribute"][0],
            "function rpg:pact/ui/terms_show%d with storage rpg:pact ui" % n,
        ])
        write("pact/ui/terms_show%d.mcfunction" % n,
              "$dialog show @s " + json.dumps(dialog, ensure_ascii=False, separators=(",", ":")))
        write("pact/confirm%d.mcfunction" % n, [
            "# 点下「签下」。界面开着的时候书可能已经换手，所以重新认一次。",
            "execute if entity @s[tag=rpg.pact] run return 0",
            "tag @s remove rpg.pact.off",
            "execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{pact:%d}] run tag @s add rpg.pact.off" % n,
            "execute if entity @s[tag=rpg.pact.off] unless items entity @s weapon.offhand *[minecraft:custom_data~{pact:%d}] run return run %s" % (
                n, say("no_book", "书不在手上，契约没有签下。")),
            "execute if entity @s[gamemode=creative] run return run function rpg:pact/grant%d" % n,
            "execute store result score #c rpg_pact run clear @s %s[!minecraft:custom_data] 0" % d["tribute"][0],
            "execute if score #c rpg_pact matches ..%d run return run %s" % (
                pa.TRIBUTE - 1, say("tribute%d" % n, "祭品不足：需要%s ×%d，契约没有签下。" % (d["tribute"][1], pa.TRIBUTE))),
            "clear @s %s[!minecraft:custom_data] %d" % (d["tribute"][0], pa.TRIBUTE),
            "function rpg:pact/grant%d" % n,
        ])
        write("pact/grant%d.mcfunction" % n, ["function rpg:pact/oath/fresh", "function rpg:pact/sign%d" % n])

    write("pact/oath/fresh.mcfunction", [
        "# 第一次立约：所有进度从头开始，统计项归零，免得旧账算到这份契约上。",
        "scoreboard players set @s rpg_pact_lv 1",
        "scoreboard players set @s rpg_pact_dom 0",
        "scoreboard players set @s rpg_pact_bond 0",
        "scoreboard players set @s rpg_pact_seep 0",
        "scoreboard players set @s rpg_pact_cd2 0",
        "scoreboard players set @s rpg_pact_cd3 0",
        "scoreboard players set @s rpg_pact_av 0",
        "scoreboard players set @s rpg_pact_fx 0",
        "scoreboard players set @s rpg_pact_s1 0",
        "scoreboard players set @s rpg_pact_s2 0",
        "scoreboard players set @s rpg_pv_a 0",
        "scoreboard players set @s rpg_pv_b 0",
        "scoreboard players set @s rpg_pv_t 0",
        "scoreboard players set @s rpg_ps_dmg 0",
        "scoreboard players set @s rpg_ps_taken 0",
        "scoreboard players set @s rpg_ps_sprint 0",
        "scoreboard players set @s rpg_ps_crouch 0",
        "scoreboard players set @s rpg_ps_dead 0",
    ])
    write("pact/oath/migrate.mcfunction", [
        "# 旧存档的立约者：按一阶补齐。",
        "function rpg:pact/oath/fresh",
        "function rpg:pact/attr",
    ])

    # 柱页合书
    use = ["advancement revoke @s only rpg:pact/page",
           "execute if entity @s[scores={rpg_pact_t=1..}] run return 0",
           "scoreboard players set @s rpg_pact_t 8"]
    for p in PILLARS:
        n = p["n"]
        use.append("execute if items entity @s weapon.* *[minecraft:custom_data~{pact_page:%d}] run return run function rpg:pact/page/try%d" % (n, n))
        need = ["execute unless items entity @s container.* *[minecraft:custom_data~{pact_page:%d,pact_role:%d}] run return run %s"
                % (n, r, say("page%d_%d" % (n, r), "还缺%s的柱页：%s。" % (p["who"], dm.LORDS[n]["spirits"][r - 1][1])))
                for r in range(1, 6)]
        take = ["clear @s minecraft:paper[minecraft:custom_data~{pact_page:%d,pact_role:%d}] 1" % (n, r)
                for r in range(1, 6)]
        write("pact/page/try%d.mcfunction" % n, need + take + [
            "give @s %s 1" % pa.item_snbt(p, False),
            "playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 0.7",
            "particle %s ~ ~1 ~ 0.4 0.5 0.4 0.02 24" % ui.pillar_dust(n, 1.2),
        ])
    write("pact/page/use.mcfunction", use)
    write_json("advancement/pact/page.json", {
        "criteria": {"requirement": {"trigger": "minecraft:using_item", "conditions": {
            "item": {"predicates": {"minecraft:custom_data": "{pact_role:1}"}}}},
            **{"r%d" % r: {"trigger": "minecraft:using_item", "conditions": {
                "item": {"predicates": {"minecraft:custom_data": "{pact_role:%d}" % r}}}} for r in range(2, 6)}},
        "requirements": [["requirement", "r2", "r3", "r4", "r5"]],
        "rewards": {"function": "rpg:pact/page/use"}})


# ---------------------------------------------------------------------------
# 侍奉：戒律与契合度
# ---------------------------------------------------------------------------
def build_oath():
    gain = ["# 涨契合，封顶 %d。#gain 由调用方给。" % BOND_MAX,
            "scoreboard players operation @s rpg_pact_bond += #gain rpg_pact",
            "execute if score @s rpg_pact_bond matches %d.. run scoreboard players set @s rpg_pact_bond %d" % (BOND_MAX + 1, BOND_MAX)]
    write("pact/oath/gain.mcfunction", gain)
    write("pact/oath/violate.mcfunction", [
        "# 犯了禁忌。",
        "scoreboard players remove @s rpg_pact_bond %d" % TABOO_BOND,
        "scoreboard players add @s rpg_taint %d" % TABOO_TAINT,
        "playsound minecraft:entity.wither.hurt player @s ~ ~ ~ 0.6 0.6",
        "function rpg:pact/oath/taboo_msg",
        "execute if score @s rpg_pact_bond matches ..0 run function rpg:pact/oath/fall",
    ])
    write("pact/oath/taboo_msg.mcfunction",
          ["execute if score @s rpg_pact matches %d run function rpg:hud/m%d" % (p["n"], HUD_TABOO + p["n"] - 1) for p in PILLARS])
    write("pact/oath/fall.mcfunction", [
        "# 契合归零。一阶没有可掉的，魔神直接往里压。",
        "execute if score @s rpg_pact_lv matches ..1 run scoreboard players add @s rpg_taint %d" % FLOOR_TAINT,
        "execute if score @s rpg_pact_lv matches ..1 run return run scoreboard players set @s rpg_pact_bond %d" % AFTER_UP,
        "scoreboard players remove @s rpg_pact_lv 1",
        "scoreboard players set @s rpg_pact_bond %d" % AFTER_FALL,
        "function rpg:pact/attr",
        "function rpg:pact/seal/trim",
        "function rpg:pact/book/resync",
        "function rpg:hud/m%d" % HUD_FALL,
        "playsound minecraft:block.glass.break player @s ~ ~ ~ 1 0.5",
    ])

    write("pact/book/resync.mcfunction", [
        "# 书不一定在手上：在手就原地换，在背包就收走重发，一本都没有就不发。",
        "tag @s remove rpg.pact.off",
        "execute if items entity @s weapon.mainhand *[minecraft:custom_data~{pact_signed:1b}] run return run function rpg:pact/book/fresh",
        "tag @s add rpg.pact.off",
        "execute if items entity @s weapon.offhand *[minecraft:custom_data~{pact_signed:1b}] run return run function rpg:pact/book/fresh",
        "tag @s remove rpg.pact.off",
        "execute store result score #c rpg_pact run clear @s minecraft:enchanted_book[minecraft:custom_data~{pact_signed:1b}] 0",
        "execute if score #c rpg_pact matches ..0 run return 0",
        "clear @s minecraft:enchanted_book[minecraft:custom_data~{pact_signed:1b}]",
        "tag @s add rpg.pact.give",
        "function rpg:pact/book/fresh",
        "tag @s remove rpg.pact.give",
    ])

    # 每 2 秒一次，只有立约者进来。
    step = [
        "# 戒律的结算，由 taint/step 每 40 刻调用一次。",
        "execute unless score @s rpg_pact_lv matches 1.. run function rpg:pact/oath/migrate",
        "execute if score @s rpg_ps_dead matches 1.. if score @s rpg_ps_hp matches 1.. run function rpg:pact/oath/respawn",
        "scoreboard players add @s rpg_pv_t 1",
        "execute if score @s rpg_pv_t matches 30.. run scoreboard players set @s rpg_pv_t 0",
        "execute if score @s rpg_pv_a matches 1.. run scoreboard players remove @s rpg_pv_a 1",
        "execute if entity @s[tag=rpg.pact.s3] if score @s rpg_pv_t matches 0 run effect give @s minecraft:regeneration 4 0 true",
        "execute if entity @s[tag=rpg.pact.s3] if score @s rpg_pv_t matches 15 run effect give @s minecraft:regeneration 4 0 true",
    ]
    step += ["execute if score @s rpg_pact matches %d run function rpg:pact/oath/p%d" % (n, n) for n in (2, 3, 4, 5, 6, 7)]
    write("pact/oath/step.mcfunction", step)

    write("pact/oath/respawn.mcfunction", [
        "# 死亡会抹掉属性修饰符，复活后重新挂上。附身也随之结束。",
        "scoreboard players set @s rpg_ps_dead 0",
        "scoreboard players set @s rpg_pact_av 0",
        "function rpg:pact/attr",
        "function rpg:pact/seal/apply",
        "execute if score @s rpg_pact matches 1 run function rpg:pact/oath/violate",
    ])
    write("pact/oath/p2.mcfunction", [
        "# 利维坦：碰水就不算断。",
        "execute if predicate rpg:pact_wet run return run scoreboard players set @s rpg_pv_b 0",
        "scoreboard players add @s rpg_pv_b 1",
        "execute if score @s rpg_pv_b matches 300.. run function rpg:pact/oath/taboo_reset",
    ])
    write("pact/oath/p3.mcfunction", [
        "# 亚巴顿：潜行且这两秒没挪窝，累计 10 秒换 1 点契合。",
        "execute if predicate rpg:sneaking if score @s rpg_ps_crouch matches 0 run scoreboard players add @s rpg_pv_b 1",
        "scoreboard players set @s rpg_ps_crouch 0",
        "execute if score @s rpg_pv_b matches 5.. run function rpg:pact/oath/still",
        "execute if score @s rpg_pv_t matches 0 if score @s rpg_ps_sprint matches 30000.. run function rpg:pact/oath/violate",
        "execute if score @s rpg_pv_t matches 0 run scoreboard players set @s rpg_ps_sprint 0",
    ])
    write("pact/oath/still.mcfunction", [
        "scoreboard players set @s rpg_pv_b 0",
        "scoreboard players set #gain rpg_pact 1",
        "function rpg:pact/oath/gain",
    ])
    write("pact/oath/taboo_reset.mcfunction", [
        "scoreboard players set @s rpg_pv_b 0",
        "function rpg:pact/oath/violate",
    ])
    write("pact/oath/p4.mcfunction", [
        "# 别西卜：饿着就犯禁，每分钟至多一次。",
        "execute if score @s rpg_ps_food matches ..5 if score @s rpg_pv_t matches 0 run function rpg:pact/oath/violate",
    ])
    write("pact/oath/p5.mcfunction", [
        "# 萨麦尔：每 30 点伤害换 1 点契合；五分钟不动手就犯禁。",
        "execute if score @s rpg_ps_dmg matches 300.. run function rpg:pact/oath/rage",
        "execute if score @s rpg_ps_dmg > @s rpg_pv_a run scoreboard players set @s rpg_pv_b 0",
        "scoreboard players operation @s rpg_pv_a = @s rpg_ps_dmg",
        "scoreboard players add @s rpg_pv_a 1",
        "scoreboard players add @s rpg_pv_b 1",
        "execute if score @s rpg_pv_b matches 150.. run function rpg:pact/oath/taboo_reset",
    ])
    write("pact/oath/rage.mcfunction", [
        "scoreboard players remove @s rpg_ps_dmg 300",
        "scoreboard players set @s rpg_pv_b 0",
        "scoreboard players set #gain rpg_pact 1",
        "function rpg:pact/oath/gain",
    ])
    write("pact/oath/p6.mcfunction", [
        "# 贝利尔：每献 10 点血换 2 点契合；五分钟满血就犯禁。",
        "execute if score @s rpg_ps_taken matches 100.. run function rpg:pact/oath/blood",
        "execute store result score #max rpg_pact run attribute @s minecraft:max_health get",
        "execute if score @s rpg_ps_hp < #max rpg_pact run return run scoreboard players set @s rpg_pv_b 0",
        "scoreboard players add @s rpg_pv_b 1",
        "execute if score @s rpg_pv_b matches 150.. run function rpg:pact/oath/taboo_reset",
    ])
    write("pact/oath/blood.mcfunction", [
        "scoreboard players remove @s rpg_ps_taken 100",
        "scoreboard players set #gain rpg_pact 2",
        "function rpg:pact/oath/gain",
    ])
    write("pact/oath/p7.mcfunction", [
        "# 玛门：身无分文就犯禁，每分钟至多一次。",
        "execute if entity @s[level=..4] if score @s rpg_pv_t matches 0 run function rpg:pact/oath/violate",
    ])

    # 由击杀和进食触发的供奉：走进度，空闲时零开销。
    write_json("predicate/pact_wet.json", {
        "condition": "minecraft:any_of",
        "terms": [
            {"condition": "minecraft:location_check", "predicate": {"fluid": {"fluids": "#minecraft:water"}}},
            {"condition": "minecraft:all_of", "terms": [
                {"condition": "minecraft:weather_check", "raining": True},
                {"condition": "minecraft:location_check", "predicate": {"can_see_sky": True}}]}]})
    write_json("advancement/pact/kill_demon.json", {
        "criteria": {
            tag: {"trigger": "minecraft:player_killed_entity", "conditions": {"entity": [
                {"condition": "minecraft:entity_properties", "entity": "this",
                 "predicate": {"nbt": '{Tags:["%s"]}' % name}}]}}
            for tag, name in (("demon", "rpg.demon"), ("minion", "rpg.demon.minion"))},
        "requirements": [["demon", "minion"]],
        "rewards": {"function": "rpg:pact/oath/kill_demon"}})
    # 进度在标签绑定前解析，这里不能写 #rpg:seal_hostile，要展开成列表。
    write_json("advancement/pact/kill_hostile.json", {
        "criteria": {"requirement": {"trigger": "minecraft:player_killed_entity", "conditions": {"entity": [
            {"condition": "minecraft:entity_properties", "entity": "this",
             "predicate": {"type": HOSTILE_TYPES}}]}}},
        "rewards": {"function": "rpg:pact/oath/kill_hostile"}})
    write_json("advancement/pact/eat.json", {
        "criteria": {"requirement": {"trigger": "minecraft:consume_item"}},
        "rewards": {"function": "rpg:pact/oath/eat"}})
    write("pact/oath/kill_demon.mcfunction", [
        "advancement revoke @s only rpg:pact/kill_demon",
        "execute unless score @s rpg_pact matches 1 run return 0",
        "scoreboard players set #gain rpg_pact 4",
        "function rpg:pact/oath/gain",
    ])
    write("pact/oath/kill_hostile.mcfunction", [
        "advancement revoke @s only rpg:pact/kill_hostile",
        "execute unless score @s rpg_pact matches 2 run return 0",
        "execute unless predicate rpg:pact_wet run return 0",
        "scoreboard players set #gain rpg_pact 2",
        "function rpg:pact/oath/gain",
    ])
    write("pact/oath/eat.mcfunction", [
        "advancement revoke @s only rpg:pact/eat",
        "execute unless score @s rpg_pact matches 4 run return 0",
        "execute if score @s rpg_pv_a matches 1.. run return 0",
        "scoreboard players set @s rpg_pv_a 5",
        "scoreboard players set #gain rpg_pact 3",
        "function rpg:pact/oath/gain",
    ])


# ---------------------------------------------------------------------------
# 深契：升阶、二阶技能、化身
# ---------------------------------------------------------------------------
SECOND = {
    1: ("""\
playsound minecraft:entity.phantom.flap player @a[distance=..24] ~ ~ ~ 1 0.55
playsound minecraft:entity.ender_dragon.flap player @a[distance=..24] ~ ~ ~ 0.7 1.45
particle dragon_breath ~ ~1.5 ~ 3 1.2 3 0.08 48
""" + hits(8, "p1_hit"), {"p1_hit": """\
effect give @s minecraft:levitation 2 1 true
effect give @s minecraft:weakness 5 1 true
damage @s 10 minecraft:magic %(BY)s
"""}),
    2: ("""\
playsound minecraft:entity.generic.splash player @a[distance=..24] ~ ~ ~ 1.2 0.65
playsound minecraft:block.conduit.attack.target player @a[distance=..24] ~ ~ ~ 0.8 0.7
particle nautilus ~ ~1 ~ 4 1.2 4 0.12 60
particle bubble_column_up ~ ~0.4 ~ 4 0.5 4 0.35 70
""" + hits(4, "p2_out") + "\n" + "execute as @e[%s,distance=4.01..10] at @s run function rpg:pact/s/p2_in" % HOSTILE,
        {"p2_out": """\
execute if entity @s[%(MOVE)s] facing entity @a[tag=rpg.pact.cast,limit=1] feet run tp @s ^ ^ ^-2.4
damage @s 8 minecraft:drown %(BY)s
""", "p2_in": """\
execute if entity @s[%(MOVE)s] facing entity @a[tag=rpg.pact.cast,limit=1] feet run tp @s ^ ^ ^2.4
damage @s 8 minecraft:drown %(BY)s
"""}),
    3: ("""\
playsound minecraft:block.amethyst_block.resonate player @a[distance=..24] ~ ~ ~ 1 0.35
playsound minecraft:entity.warden.heartbeat player @a[distance=..24] ~ ~ ~ 1 0.42
particle sculk_soul ~ ~1 ~ 4 1 4 0.04 56
""" + hits(10, "p3_hit"), {"p3_hit": """\
effect give @s minecraft:slowness 3 255 true
effect give @s minecraft:weakness 6 2 true
damage @s 6 minecraft:magic %(BY)s
"""}),
    4: ("""\
playsound minecraft:entity.bee.loop_aggressive player @a[distance=..24] ~ ~ ~ 1 0.6
particle spore_blossom_air ~ ~1 ~ 2 1 2 0.05 40
scoreboard players set @s rpg_pact_fx %d
""" % SWARM, {"p4_swarm": """\
particle spore_blossom_air ~ ~1 ~ 2.5 1 2.5 0.04 14
particle ash ~ ~1 ~ 2.5 1 2.5 0.04 14
""" + hits(6, "p4_hit"), "p4_hit": """\
damage @s 3 minecraft:magic by @a[tag=rpg.pact.swarm,limit=1,sort=nearest]
effect give @s minecraft:hunger 4 1 true
"""}),
    5: ("""\
playsound minecraft:entity.ravager.roar player @a[distance=..24] ~ ~ ~ 0.8 1.3
""" + "execute as @e[%s,distance=..14,sort=nearest,limit=1] at @s run function rpg:pact/s/p5_hit" % HOSTILE,
        {"p5_hit": """\
tp @a[tag=rpg.pact.cast,limit=1] ^ ^ ^-1
particle soul_fire_flame ~ ~1 ~ 0.6 0.8 0.6 0.08 36
particle crit ~ ~1 ~ 0.6 0.8 0.6 0.2 24
playsound minecraft:entity.player.attack.crit player @a[distance=..24] ~ ~ ~ 1 0.7
effect give @s minecraft:wither 5 1 true
damage @s 14 minecraft:magic %(BY)s
"""}),
    6: ("""\
playsound minecraft:entity.illusioner.prepare_blindness player @a[distance=..24] ~ ~ ~ 1 0.7
particle witch ~ ~1 ~ 3 1 3 0.2 56
""" + hits(8, "p6_hit"), {"p6_hit": """\
effect give @s minecraft:glowing 6 0 true
effect give @s minecraft:weakness 6 1 true
tag @s add rpg.pact.lured
damage @s 4 minecraft:magic by @e[%s,tag=!rpg.pact.lured,distance=..8,sort=nearest,limit=1]
tag @s remove rpg.pact.lured
""" % HOSTILE}),
    7: ("""\
playsound minecraft:block.chain.break player @a[distance=..24] ~ ~ ~ 1 0.6
playsound minecraft:block.amethyst_block.chime player @a[distance=..24] ~ ~ ~ 1 0.7
particle wax_on ~ ~1 ~ 3 1 3 0.1 56
""" + hits(8, "p7_hit"), {"p7_hit": """\
effect give @s minecraft:slowness 6 6 true
effect give @s minecraft:mining_fatigue 6 2 true
particle wax_on ~ ~0.6 ~ 0.3 0.4 0.3 0.05 10
summon minecraft:experience_orb ~ ~1 ~ {Value:8}
damage @s 8 minecraft:magic %(BY)s
"""}),
}

# (属性, 数值)：附身时加在 rpg:pact/avatar/N 上。scale 是所有柱共有的。
AVATAR_MODS = {
    1: [("attack_damage", 6)],
    2: [("movement_speed", 0.04), ("attack_damage", 2)],
    3: [("max_health", 20), ("armor", 4)],
    4: [("attack_speed", 1.5)],
    5: [("attack_damage", 4), ("movement_speed", 0.03)],
    6: [("armor", 8), ("armor_toughness", 4)],
    7: [("attack_damage", 3), ("armor", 4), ("luck", 3)],
}
AVATAR_ATTRS = sorted({attr for mods in AVATAR_MODS.values() for attr, _ in mods} | {"scale"})


def ring(radius, count, warmup):
    return ["$execute rotated %d 0 positioned ^ ^ ^%d run summon minecraft:evoker_fangs ~ ~ ~ {Warmup:%d,Owner:$(uuid)}"
            % (i * 360 // count, radius, warmup) for i in range(count)]


AVATAR_BURST = {
    1: ("""\
data modify storage rpg:pact uuid set from entity @s UUID
function rpg:pact/s/a1_rings with storage rpg:pact
playsound minecraft:entity.evoker.cast_spell player @a[distance=..32] ~ ~ ~ 1 0.6
particle dragon_breath ~ ~1 ~ 4 1 4 0.1 64
""" + hits(8, "a1_hit"), {"a1_rings": "\n".join(ring(3, 8, 2) + ring(5, 10, 8) + ring(7, 12, 14)),
                          "a1_hit": "damage @s 12 minecraft:magic %(BY)s\n"}),
    2: ("""\
playsound minecraft:entity.elder_guardian.curse player @a[distance=..32] ~ ~ ~ 1 0.5
particle nautilus ~ ~1 ~ 5 1.2 5 0.2 80
particle bubble_column_up ~ ~0.4 ~ 5 0.5 5 0.35 80
""" + hits(12, "a2_hit"), {"a2_hit": """\
execute if entity @s[%(MOVE)s] facing entity @a[tag=rpg.pact.cast,limit=1] feet run tp @s ^ ^ ^3
damage @s 16 minecraft:drown %(BY)s
effect give @s minecraft:slowness 5 2 true
"""}),
    3: ("""\
playsound minecraft:entity.warden.sonic_boom player @a[distance=..32] ~ ~ ~ 0.8 0.7
playsound minecraft:block.sculk_shrieker.shriek player @a[distance=..32] ~ ~ ~ 1 0.6
particle sculk_soul ~ ~1 ~ 5 1 5 0.03 80
particle soul ~ ~0.5 ~ 5 0.6 5 0.04 60
""" + hits(10, "a3_hit"), {"a3_hit": """\
damage @s 16 minecraft:magic %(BY)s
effect give @s minecraft:wither 6 1 true
particle soul ~ ~1 ~ 0.2 0.4 0.2 0.06 10
effect give @a[tag=rpg.pact.cast,limit=1] minecraft:instant_health 1 0 true
"""}),
    4: ("""\
playsound minecraft:entity.ender_dragon.growl player @a[distance=..32] ~ ~ ~ 0.8 1.4
particle ash ~ ~1 ~ 5 1.4 5 0.05 90
particle spore_blossom_air ~ ~1 ~ 5 1 5 0.05 60
""" + hits(10, "a4_hit"), {"a4_hit": """\
damage @s 20 minecraft:magic %(BY)s
effect give @s minecraft:hunger 10 2 true
"""}),
    5: ("""\
playsound minecraft:entity.ravager.roar player @a[distance=..32] ~ ~ ~ 1 0.8
playsound minecraft:entity.generic.explode player @a[distance=..32] ~ ~ ~ 0.8 0.7
particle soul_fire_flame ~ ~1 ~ 5 1 5 0.08 90
particle lava ~ ~1 ~ 4 1 4 0 24
""" + hits(10, "a5_hit"), {"a5_hit": """\
damage @s 18 minecraft:magic %(BY)s
effect give @s minecraft:wither 6 1 true
"""}),
    6: ("""\
playsound minecraft:entity.evoker.prepare_summon player @a[distance=..32] ~ ~ ~ 1 0.6
playsound minecraft:block.beacon.power_select player @a[distance=..32] ~ ~ ~ 0.8 0.5
particle enchant ~ ~1.2 ~ 5 1.5 5 1 90
particle witch ~ ~1 ~ 5 1 5 0.2 60
""" + hits(12, "a6_hit"), {"a6_hit": """\
execute if entity @s[%(MOVE)s] facing entity @a[tag=rpg.pact.cast,limit=1] feet run tp @s ^ ^ ^3
effect give @s minecraft:slowness 5 3 true
effect give @s minecraft:weakness 8 2 true
damage @s 16 minecraft:magic %(BY)s
"""}),
    7: ("""\
playsound minecraft:entity.player.levelup player @a[distance=..32] ~ ~ ~ 1 0.6
playsound minecraft:block.anvil.land player @a[distance=..32] ~ ~ ~ 0.7 0.7
particle wax_on ~ ~1 ~ 5 1 5 0.1 90
particle end_rod ~ ~1 ~ 5 1 5 0.05 40
""" + hits(10, "a7_hit"), {"a7_hit": """\
damage @s 22 minecraft:magic %(BY)s
summon minecraft:experience_orb ~ ~1 ~ {Value:16}
"""}),
}


def expand(body):
    return body.replace("%(BY)s", BY).replace("%(MOVE)s", MOVABLE)


def build_skills():
    second = [
        "# 二阶技能：潜行长按。",
        "execute unless score @s rpg_pact_lv matches 2.. run return run function rpg:hud/m%d" % HUD_LOCKED,
        "execute if score @s rpg_pact_cd2 matches 1.. run return run function rpg:hud/m%d" % HUD_DENY,
        "execute if score @s rpg_pact matches 5 unless entity %s run return run %s" % (targets(14, "limit=1"), say("no_target", "14 格内没有可以突入的敌人。")),
        "scoreboard players set @s rpg_pact_cd2 %d" % CD2,
        "scoreboard players add @s rpg_taint %d" % pa.SECOND_TAINT,
        "tag @s add rpg.pact.cast",
    ]
    second += ["execute if score @s rpg_pact matches %d run function rpg:pact/s/p%d" % (n, n) for n in range(1, 8)]
    second += ["tag @s remove rpg.pact.cast"]
    write("pact/depth/second.mcfunction", second)

    for n, (body, parts) in SECOND.items():
        p = PILLARS[n - 1]
        write("pact/s/p%d.mcfunction" % n,
              expand(body) + "\nparticle %s ~ ~1 ~ 3 1 3 0.04 30" % ui.pillar_dust(n, 2))
        for name, part in parts.items():
            write("pact/s/%s.mcfunction" % name, expand(part))

    avatar = [
        "# 化身：潜行抬头长按。大招加 20 秒附身。",
        "execute unless score @s rpg_pact_lv matches 3.. run return run function rpg:hud/m%d" % HUD_LOCKED,
        "execute if score @s rpg_pact_cd3 matches 1.. run return run function rpg:hud/m%d" % HUD_DENY,
        "scoreboard players set @s rpg_pact_cd3 %d" % CD3,
        "scoreboard players add @s rpg_taint %d" % pa.AVATAR_TAINT,
        "scoreboard players set @s rpg_pact_av %d" % AVATAR,
        "tag @s add rpg.pact.cast",
    ]
    avatar += ["execute if score @s rpg_pact matches %d run function rpg:pact/s/a%d" % (n, n) for n in range(1, 8)]
    avatar += ["tag @s remove rpg.pact.cast"]
    write("pact/depth/avatar.mcfunction", avatar)

    for n, (body, parts) in AVATAR_BURST.items():
        p = PILLARS[n - 1]
        mods = [("scale", 0.15)] + AVATAR_MODS[n]
        write("pact/s/a%d.mcfunction" % n, expand(body) + "\n" + "\n".join(
            ["attribute @s minecraft:%s modifier remove rpg:pact/avatar" % attr for attr, _ in mods] +
            ["attribute @s minecraft:%s modifier add rpg:pact/avatar %s add_value" % (attr, amount) for attr, amount in mods]) +
            "\nparticle %s ~ ~1 ~ 0 0 0 0 1" % vfx.flash(p["lit"]) +
            "\n" + pa.event_title(p, DEPTH[n]["avatar"], "附身 %d 秒" % (AVATAR // 20)))
        for name, part in parts.items():
            write("pact/s/%s.mcfunction" % name, expand(part))
        write("pact/s/aura%d.mcfunction" % n, "particle %s ~ ~1 ~ 0.4 0.7 0.4 0.02 6" % ui.pillar_dust(n, 1.2))

    tick = [
        "# 立约者的一刻：三条冷却、附身和蝇群。",
        "execute if score @s rpg_pact_cd2 matches 1.. run scoreboard players remove @s rpg_pact_cd2 1",
        "execute if score @s rpg_pact_cd3 matches 1.. run scoreboard players remove @s rpg_pact_cd3 1",
        "execute if score @s rpg_pact_av matches 1.. at @s run function rpg:pact/depth/avatar_tick",
        "execute if score @s rpg_pact_fx matches 1.. at @s run function rpg:pact/depth/swarm_tick",
    ]
    write("pact/depth/tick.mcfunction", tick)
    write("pact/depth/avatar_tick.mcfunction", [
        "scoreboard players remove @s rpg_pact_av 1",
        "execute if score @s rpg_pact_av matches 0 run return run function rpg:pact/depth/avatar_end",
        "scoreboard players operation #c rpg_pact = @s rpg_pact_av",
        "scoreboard players operation #c rpg_pact %= #five rpg_pact",
        "execute unless score #c rpg_pact matches 0 run return 0",
    ] + ["execute if score @s rpg_pact matches %d run function rpg:pact/s/aura%d" % (n, n) for n in range(1, 8)])
    write("pact/depth/avatar_off.mcfunction", [
        "attribute @s minecraft:%s modifier remove rpg:pact/avatar" % attr for attr in AVATAR_ATTRS])
    write("pact/depth/avatar_end.mcfunction", [
        "function rpg:pact/depth/avatar_off",
        "effect give @s minecraft:weakness 8 1 true",
        "playsound minecraft:block.beacon.deactivate player @s ~ ~ ~ 0.8 0.7",
    ])
    write("pact/depth/swarm_tick.mcfunction", [
        "scoreboard players remove @s rpg_pact_fx 1",
        "scoreboard players operation #c rpg_pact = @s rpg_pact_fx",
        "scoreboard players operation #c rpg_pact %= #ten rpg_pact",
        "execute unless score #c rpg_pact matches 0 run return 0",
        "tag @s add rpg.pact.swarm",
        "function rpg:pact/s/p4_swarm",
        "tag @s remove rpg.pact.swarm",
    ])

    write("pact/depth/clear.mcfunction", [
        "# 契约断了：退回柱印，清掉深契的全部状态。",
        "function rpg:pact/seal/eject_all",
        "function rpg:pact/depth/avatar_off",
        "scoreboard players set @s rpg_pact_lv 0",
        "scoreboard players set @s rpg_pact_dom 0",
        "scoreboard players set @s rpg_pact_bond 0",
        "scoreboard players set @s rpg_pact_cd2 0",
        "scoreboard players set @s rpg_pact_cd3 0",
        "scoreboard players set @s rpg_pact_av 0",
        "scoreboard players set @s rpg_pact_fx 0",
    ])

    up = [
        "# 深契。条件不足时只提示，不扣东西。",
        "execute if score @s rpg_pact_lv matches 3.. run return run " + say("up_max", "已至真名，没有下一阶了。"),
        "execute if entity @s[gamemode=creative] run return run function rpg:pact/up_done",
        "execute unless score @s rpg_pact_bond matches %d.. run return run %s" % (
            BOND_MAX, say("up_bond", "契合度还不够，深契需要 %d。" % BOND_MAX)),
        "execute if score @s rpg_pact_lv matches 1 run return run function rpg:pact/up_soul",
        "function rpg:pact/up_name",
    ]
    write("pact/up.mcfunction", up)
    soul = []
    for item, _ in ROLE_ITEMS:
        soul += ["execute store result score #c rpg_pact run clear @s %s[!minecraft:custom_data] 0" % item,
                 "execute if score #c rpg_pact matches ..%d run return run %s" % (
                     UP_ITEMS - 1, say("up_items", "材料不足：%s各 %d。" % ("、".join(n for _, n in ROLE_ITEMS), UP_ITEMS)))]
    soul += ["clear @s %s[!minecraft:custom_data] %d" % (item, UP_ITEMS) for item, _ in ROLE_ITEMS]
    soul.append("function rpg:pact/up_done")
    write("pact/up_soul.mcfunction", soul)
    write("pact/up_name.mcfunction",
          ["execute if score @s rpg_pact matches %d unless entity @s[tag=rpg.pw.%d] run return run %s"
           % (n, n, say("up_lord%d" % n, "还没有击败过%s，真名不会交给你。" % PILLARS[n - 1]["who"]))
           for n in range(1, 8)] + ["function rpg:pact/up_done"])
    write("pact/up_done.mcfunction", [
        "scoreboard players add @s rpg_pact_lv 1",
        "scoreboard players set @s rpg_pact_bond %d" % AFTER_UP,
        "function rpg:pact/attr",
        "function rpg:pact/book/resync",
        "function rpg:hud/m%d" % HUD_TIER,
        "playsound minecraft:block.end_portal.spawn master @s ~ ~ ~ 0.8 0.7",
        "playsound minecraft:entity.wither.spawn master @a[distance=..32] ~ ~ ~ 0.4 1.4",
        "execute at @s run particle sculk_charge_pop ~ ~1 ~ 0.5 0.8 0.5 0.1 60",
    ] + ["execute if score @s rpg_pact matches %d run function rpg:pact/up_title%d" % (n, n) for n in range(1, 8)])
    for p in PILLARS:
        titles = []
        for lv in (2, 3):
            for line_ in pa.event_title(p, "深契 · " + TIERS[lv - 1], "柱中的东西离你更近了", ui.BROADCAST_HOLY).split("\n"):
                titles.append("execute if score @s rpg_pact_lv matches %d run %s" % (lv, line_))
        write("pact/up_title%d.mcfunction" % p["n"], titles)

    write("pact/do_sign.mcfunction",
          ["execute if score @s rpg_pact_do matches %d run function rpg:pact/confirm%d" % (10 + n, n) for n in range(1, 8)])
    write("pact/do.mcfunction", [
        "# 契约界面的按钮。trigger 用过一次就关，下次打开界面时才重新开。",
        "execute if score @s rpg_pact_do matches 11..17 run function rpg:pact/do_sign",
        "execute if score @s rpg_pact_do matches 2 if entity @s[tag=rpg.pact] run function rpg:pact/up",
        "execute if score @s rpg_pact_do matches 3 if entity @s[tag=rpg.pact] run function rpg:pact/seal/eject1",
        "execute if score @s rpg_pact_do matches 4 if entity @s[tag=rpg.pact] run function rpg:pact/seal/eject2",
        "execute if score @s rpg_pact_do matches 5 if score @s rpg_pact matches 7 run function rpg:pact/oath/gold",
        "scoreboard players set @s rpg_pact_do 0",
    ])
    write("pact/oath/gold.mcfunction", [
        "# 玛门的供奉：一次最多献 16 个金锭，每个 2 点契合。",
        "execute store result score #c rpg_pact run clear @s minecraft:gold_ingot[!minecraft:custom_data] 16",
        "execute if score #c rpg_pact matches ..0 run return run " + say("no_gold", "背包里没有金锭。"),
        "scoreboard players operation #gain rpg_pact = #c rpg_pact",
        "scoreboard players operation #gain rpg_pact *= #two rpg_pact",
        "function rpg:pact/oath/gain",
        "playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 1.2",
    ])


# ---------------------------------------------------------------------------
# 契约界面
# ---------------------------------------------------------------------------
def build_ui():
    names = ["# 把两个槽位的柱印名写进界面。",
             'data modify storage rpg:pact ui.s1 set value "空"',
             'data modify storage rpg:pact ui.s2 set value "空"',
             'execute unless score @s rpg_pact_lv matches 2.. run data modify storage rpg:pact ui.s1 set value "魂誓开启"',
             'execute unless score @s rpg_pact_lv matches 3.. run data modify storage rpg:pact ui.s2 set value "真名开启"']
    for seal in range(1, 36):
        _, _, spirit = spirit_of(seal)
        for slot in (1, 2):
            names.append('execute if score @s rpg_pact_s%d matches %d run data modify storage rpg:pact ui.s%d set value "%s"'
                         % (slot, seal, slot, spirit))
    write("pact/ui/names.mcfunction", names)

    opened = [
        "# 潜行低头长按书。文字里的数字靠宏写进去，所以每次打开都现算。",
        "tag @s add rpg.pact.ui",
        "scoreboard players enable @s rpg_pact_do",
        "execute store result storage rpg:pact ui.bond int 1 run scoreboard players get @s rpg_pact_bond",
        "execute store result storage rpg:pact ui.taint int 1 run scoreboard players get @s rpg_taint",
        "scoreboard players operation #c rpg_pact = @s rpg_pact_cd2",
        "scoreboard players operation #c rpg_pact /= #twenty_t rpg_pact",
        "execute store result storage rpg:pact ui.cd2 int 1 run scoreboard players get #c rpg_pact",
        "scoreboard players operation #c rpg_pact = @s rpg_pact_cd3",
        "scoreboard players operation #c rpg_pact /= #twenty_t rpg_pact",
        "execute store result storage rpg:pact ui.cd3 int 1 run scoreboard players get #c rpg_pact",
    ]
    for lv in (1, 2, 3):
        opened.append('execute if score @s rpg_pact_lv matches %d run data modify storage rpg:pact ui.tier set value "第%s阶 · %s"'
                      % (lv, "一二三"[lv - 1], TIERS[lv - 1]))
    opened += ['data modify storage rpg:pact ui.dom set value ""',
               'execute if score @s rpg_pact_dom matches 1 run data modify storage rpg:pact ui.dom set value " · 支配"',
               "function rpg:pact/ui/names"]
    opened += ["execute if score @s rpg_pact matches %d run function rpg:pact/ui/next%d" % (n, n) for n in range(1, 8)]
    opened += ["execute if score @s rpg_pact matches %d run function rpg:pact/ui/show%d with storage rpg:pact ui" % (n, n) for n in range(1, 8)]
    write("pact/ui/open.mcfunction", opened)

    items = "、".join(name for _, name in ROLE_ITEMS)
    for p in PILLARS:
        n, d = p["n"], DEPTH[p["n"]]
        write("pact/ui/next%d.mcfunction" % n, [
            'execute if score @s rpg_pact_lv matches 1 run data modify storage rpg:pact ui.next set value "契合 100，并献上%s各 %d"' % (items, UP_ITEMS),
            'execute if score @s rpg_pact_lv matches 2 run data modify storage rpg:pact ui.next set value "契合 100，并击败过%s"' % p["who"],
            'execute if score @s rpg_pact_lv matches 3 run data modify storage rpg:pact ui.next set value "已至真名"',
        ])
        body = []
        body += line(text("$(tier)$(dom)", p["lit"], True))
        body += line(text("契合 ", ui.MUTED), text("$(bond)", "white", True), text(" / %d" % BOND_MAX, ui.MUTED),
                     text("　　魔化 ", ui.MUTED), text("$(taint)", ui.WARN, True), text(" / 100", ui.MUTED))
        body += [blank()]
        body += tagged("魂誓", text("[%s]" % d["second"], p["lit"], True), text("　冷却 $(cd2) 秒", ui.MUTED))
        body += tagged("真名", text("[%s]" % d["avatar"], p["lit"], True), text("　冷却 $(cd3) 秒", ui.MUTED))
        body += tagged("从契", text("$(s1)　/　$(s2)", p["lit"]))
        body += [blank()]
        body += tagged("供奉", text(d["oath"]))
        body += tagged("禁忌", text(d["taboo"]))
        body += [blank()]
        body += [text("下一阶　", ui.MUTED), text("$(next)")]
        actions = [button("深契", 2, ui.HOLY_DARK), button("取下第一枚柱印", 3, "gray"),
                   button("取下第二枚柱印", 4, "gray")]
        if n == 7:
            actions.append(button("献上金锭", 5, p["lit"]))
        dialog = dialog_common(dialog_title("[已立约]", p), body, actions)
        write("pact/ui/show%d.mcfunction" % n, "$dialog show @s " + json.dumps(dialog, ensure_ascii=False, separators=(",", ":")))


# ---------------------------------------------------------------------------
# 从契：柱印
# ---------------------------------------------------------------------------
# (属性, 普通, 同柱)。
SEAL_MODS = {
    1: [("armor", 2, 3), ("knockback_resistance", 0.05, 0.1)],
    2: [("movement_speed", 0.005, 0.008), ("entity_interaction_range", 0.5, 1)],
    3: [("max_health", 2, 4)],
    4: [],
    5: [("attack_damage", 1, 2)],
}
SEAL_ATTRS = sorted({m[0] for mods in SEAL_MODS.values() for m in mods})


def build_seals():
    use = ["advancement revoke @s only rpg:pact/seal",
           "execute if entity @s[scores={rpg_pact_t=1..}] run return 0",
           "scoreboard players set @s rpg_pact_t 8",
           "execute unless entity @s[tag=rpg.pact] run return run " + say("seal_nopact", "还没有立约，柱印无处可镶。"),
           "scoreboard players set #seal rpg_pact 0"]
    use += ["execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:%d}] run scoreboard players set #seal rpg_pact %d" % (s, s)
            for s in range(1, 36)]
    use += [
        "execute if score #seal rpg_pact matches 0 run return 0",
        "execute if score @s rpg_pact_lv matches 2.. if score @s rpg_pact_s1 matches 0 run return run function rpg:pact/seal/put1",
        "execute if score @s rpg_pact_lv matches 3.. if score @s rpg_pact_s2 matches 0 run return run function rpg:pact/seal/put2",
        say("seal_full", "没有空的槽位：魂誓开一槽，真名开两槽。"),
    ]
    write("pact/seal/use.mcfunction", use)
    write_json("advancement/pact/seal.json", {
        "criteria": {"s%d" % s: {"trigger": "minecraft:using_item", "conditions": {
            "item": {"predicates": {"minecraft:custom_data": "{rpg_seal:%d}" % s}}}} for s in range(1, 36)},
        "requirements": [["s%d" % s for s in range(1, 36)]],
        "rewards": {"function": "rpg:pact/seal/use"}})

    take = ["execute if score #seal rpg_pact matches %d run clear @s minecraft:paper[minecraft:custom_data~{rpg_seal:%d}] 1" % (s, s)
            for s in range(1, 36)]
    write("pact/seal/take.mcfunction", take)
    for slot in (1, 2):
        write("pact/seal/put%d.mcfunction" % slot, [
            "function rpg:pact/seal/take",
            "scoreboard players operation @s rpg_pact_s%d = #seal rpg_pact" % slot,
            "function rpg:pact/seal/apply",
            "playsound minecraft:block.amethyst_block.place player @s ~ ~ ~ 1 0.7",
            "execute at @s run particle wax_on ~ ~1 ~ 0.4 0.5 0.4 0.05 16",
        ])
        write("pact/seal/eject%d.mcfunction" % slot, [
            "execute unless score @s rpg_pact_s%d matches 1.. run return run %s" % (slot, say("seal_empty", "这个槽位是空的。")),
            "scoreboard players operation #seal rpg_pact = @s rpg_pact_s%d" % slot,
            "function rpg:pact/seal/give",
            "scoreboard players set @s rpg_pact_s%d 0" % slot,
            "function rpg:pact/seal/apply",
        ])
    write("pact/seal/trim.mcfunction", [
        "# 掉阶：多出来的槽退回柱印。",
        "execute if score @s rpg_pact_lv matches ..2 if score @s rpg_pact_s2 matches 1.. run function rpg:pact/seal/eject2",
        "execute if score @s rpg_pact_lv matches ..1 if score @s rpg_pact_s1 matches 1.. run function rpg:pact/seal/eject1",
    ])
    write("pact/seal/eject_all.mcfunction", [
        "execute if score @s rpg_pact_s1 matches 1.. run function rpg:pact/seal/eject1",
        "execute if score @s rpg_pact_s2 matches 1.. run function rpg:pact/seal/eject2",
        "scoreboard players set @s rpg_pact_s1 0",
        "scoreboard players set @s rpg_pact_s2 0",
    ])

    # 两槽各按自己的职与柱挂修饰符；只在镶入、取下、复活时算一次。
    apply_lines = ["# 重算两个槽的效果。"]
    for attr in SEAL_ATTRS:
        for slot in (1, 2):
            apply_lines.append("attribute @s minecraft:%s modifier remove rpg:pact/seal/%d" % (attr, slot))
    apply_lines += ["tag @s remove rpg.pact.s3", "tag @s remove rpg.pact.s4", "tag @s remove rpg.pact.s5",
                    "tag @s remove rpg.pact.onhit"]
    for slot in (1, 2):
        apply_lines += [
            "execute unless score @s rpg_pact_s%d matches 1.. run scoreboard players set @s rpg_pact_s%d 0" % (slot, slot),
            "execute if score @s rpg_pact_s%d matches 1.. run function rpg:pact/seal/slot%d" % (slot, slot),
        ]
    write("pact/seal/apply.mcfunction", apply_lines)
    for slot in (1, 2):
        lines = ["scoreboard players operation #r rpg_pact = @s rpg_pact_s%d" % slot,
                 "scoreboard players remove #r rpg_pact 1",
                 "scoreboard players operation #q rpg_pact = #r rpg_pact",
                 "scoreboard players operation #r rpg_pact %= #five rpg_pact",
                 "scoreboard players operation #q rpg_pact /= #five rpg_pact",
                 "scoreboard players add #q rpg_pact 1",
                 "scoreboard players set #same rpg_pact 0",
                 "execute if score #q rpg_pact = @s rpg_pact run scoreboard players set #same rpg_pact 1"]
        for role, mods in SEAL_MODS.items():
            for same in (0, 1):
                if not mods:
                    continue
                lines.append("execute if score #r rpg_pact matches %d if score #same rpg_pact matches %d run function rpg:pact/seal/m%d_%d_%d"
                             % (role - 1, same, slot, role, same))
                write("pact/seal/m%d_%d_%d.mcfunction" % (slot, role, same),
                      ["attribute @s minecraft:%s modifier add rpg:pact/seal/%d %s add_value" % (m[0], slot, m[1 + same]) for m in mods])
        lines += ["execute if score #r rpg_pact matches 2 run tag @s add rpg.pact.s3",
                  "execute if score #r rpg_pact matches 3 run tag @s add rpg.pact.s4",
                  "execute if score #r rpg_pact matches 3 run tag @s add rpg.pact.onhit",
                  "execute if score #r rpg_pact matches 4 run tag @s add rpg.pact.s5",
                  "execute if score #r rpg_pact matches 4 run tag @s add rpg.pact.onhit"]
        write("pact/seal/slot%d.mcfunction" % slot, lines)

    write("pact/seal/victim.mcfunction", [
        "# 同 samael_victim：先锁定受击者，再换到攻击者身上判柱印。",
        "tag @s add rpg.seal.victim",
        "execute on attacker if entity @s[tag=rpg.pact.onhit] run function rpg:pact/seal/hit",
        "tag @s remove rpg.seal.victim",
    ])
    write("pact/seal/hit.mcfunction", [
        "execute if entity @s[tag=rpg.pact.s4] as @e[tag=rpg.seal.victim,limit=1] run effect give @s minecraft:weakness 3 0 true",
        "execute if entity @s[tag=rpg.pact.s5] as @e[tag=rpg.seal.victim,limit=1] run function rpg:pact/seal/finish",
    ])
    write("pact/seal/finish.mcfunction", [
        "# 处刑者：生命低于两成时追一刀。",
        "execute store result score #h rpg_pact run data get entity @s Health 5",
        "execute store result score #m rpg_pact run attribute @s minecraft:max_health get",
        "execute if score #h rpg_pact < #m rpg_pact run damage @s 8 minecraft:magic",
    ])


# ---------------------------------------------------------------------------
# 清算：降临者认主、支配结局
# ---------------------------------------------------------------------------
def build_clear():
    write("pact/clear/bind.mcfunction", [
        "# 这个人身上挣出来的领主记下他，阶位越高来的越强。",
        "execute unless entity @s[tag=rpg.pact] run return 0",
        "scoreboard players add #bid rpg_pact_bid 1",
        "scoreboard players operation @s rpg_pact_bid = #bid rpg_pact_bid",
        "scoreboard players operation #lv rpg_pact = @s rpg_pact_lv",
        "execute as @e[type=minecraft:vindicator,tag=rpg.advent,distance=..4,sort=nearest,limit=1] unless score @s rpg_pact_bid matches 1.. run function rpg:pact/clear/bind_lord",
    ])
    write("pact/clear/bind_lord.mcfunction", [
        "scoreboard players operation @s rpg_pact_bid = #bid rpg_pact_bid",
        "execute on passengers run scoreboard players operation @s rpg_pact_bid = #bid rpg_pact_bid",
        "execute if score #lv rpg_pact matches 2 run attribute @s minecraft:armor modifier add rpg:pact/lord 6 add_value",
        "execute if score #lv rpg_pact matches 2 run attribute @s minecraft:attack_damage modifier add rpg:pact/lord 4 add_value",
        "execute if score #lv rpg_pact matches 3 run attribute @s minecraft:armor modifier add rpg:pact/lord 12 add_value",
        "execute if score #lv rpg_pact matches 3 run attribute @s minecraft:attack_damage modifier add rpg:pact/lord 8 add_value",
    ])
    write("pact/clear/fell.mcfunction", [
        "# 领主倒下：@s 是到达裁决的领主本人，或他留下的死亡探针。",
        "execute unless score @s rpg_dm_lord matches 1..7 run return 0",
        "scoreboard players operation #lord rpg_pact = @s rpg_dm_lord",
        "scoreboard players set #fell rpg_pact 0",
        "execute if score @s rpg_pact_bid matches 1.. run scoreboard players operation #fell rpg_pact = @s rpg_pact_bid",
        "execute as @a[distance=..32,gamemode=!spectator] run function rpg:pact/clear/witness",
    ])
    witness = ["execute if score #lord rpg_pact matches %d run tag @s add rpg.pw.%d" % (n, n) for n in range(1, 8)]
    witness += [
        "execute unless entity @s[tag=rpg.pact] run return 0",
        "execute if score #fell rpg_pact matches 0 run return 0",
        "execute unless score @s rpg_pact_bid = #fell rpg_pact run return 0",
        "scoreboard players set @s rpg_pact_bid 0",
        "execute unless score @s rpg_pact = #lord rpg_pact run return 0",
        "execute if score @s rpg_pact_dom matches 1 run return 0",
        "function rpg:pact/clear/dominate",
    ]
    write("pact/clear/witness.mcfunction", witness)
    write("pact/clear/dominate.mcfunction", [
        "# 打败了从自己身上挣出来的东西。",
        "scoreboard players set @s rpg_pact_dom 1",
        "scoreboard players set @s rpg_taint 0",
        "scoreboard players set @s rpg_fall 0",
        "tag @s remove rpg.taint.full",
        "attribute @s minecraft:attack_damage modifier remove rpg:fall",
        "function rpg:pact/attr",
        "function rpg:pact/book/resync",
        "playsound minecraft:block.end_portal.spawn master @s ~ ~ ~ 0.8 0.9",
        "execute at @s run particle end_rod ~ ~1 ~ 0.6 0.8 0.6 0.2 60",
    ] + ["execute if score @s rpg_pact matches %d run function rpg:pact/clear/title%d" % (n, n) for n in range(1, 8)])
    for p in PILLARS:
        write("pact/clear/title%d.mcfunction" % p["n"],
              pa.event_title(p, "支 配", "柱中的东西从此听你的", ui.BROADCAST_HOLY))


# ---------------------------------------------------------------------------
# 接线：计分项、逐刻入口、HUD、面板、资源
# ---------------------------------------------------------------------------
OBJECTIVES = [
    ("rpg_pact_bond", "dummy"), ("rpg_pact_cd2", "dummy"), ("rpg_pact_cd3", "dummy"),
    ("rpg_pact_av", "dummy"), ("rpg_pact_fx", "dummy"), ("rpg_pact_bid", "dummy"),
    ("rpg_pact_s1", "dummy"), ("rpg_pact_s2", "dummy"), ("rpg_pv_a", "dummy"),
    ("rpg_pv_b", "dummy"), ("rpg_pv_t", "dummy"), ("rpg_pact_do", "trigger"),
    ("rpg_ps_dmg", "minecraft.custom:minecraft.damage_dealt"),
    ("rpg_ps_taken", "minecraft.custom:minecraft.damage_taken"),
    ("rpg_ps_sprint", "minecraft.custom:minecraft.sprint_one_cm"),
    ("rpg_ps_crouch", "minecraft.custom:minecraft.crouch_one_cm"),
    ("rpg_ps_dead", "deathCount"), ("rpg_ps_hp", "health"), ("rpg_ps_food", "food"),
]


def patch_scoreboard():
    src = read("command/soreboard.mcfunction")
    add = ["scoreboard objectives add %s %s" % pair for pair in OBJECTIVES
           if "objectives add %s " % pair[0] not in src]
    add += ["scoreboard players set #five rpg_pact 5", "scoreboard players set #ten rpg_pact 10",
            "scoreboard players set #twenty_t rpg_pact 20"]
    if "#twenty_t" not in src:
        write("command/soreboard.mcfunction", src.rstrip("\n") + "\n" + "\n".join(add))


def patch_tick():
    src = read("exorcism.mcfunction")
    if "rpg:pact/depth/tick" not in src:
        write("exorcism.mcfunction", src.rstrip("\n") + """

# 深契：立约者逐刻，柱印的命中效果，以及契约界面的按钮。
execute as @a[tag=rpg.pact] run function rpg:pact/depth/tick
execute if entity @a[tag=rpg.pact.onhit,limit=1] as @e[tag=rpg.hurt] run function rpg:pact/seal/victim
execute as @a[scores={rpg_pact_do=1..}] run function rpg:pact/do
execute as @a[tag=rpg.pact.ui,scores={rpg_pact_t=0}] run tag @s remove rpg.pact.ui
""")


def patch_lifecycle():
    src = read("taint/advent.mcfunction")
    needle = "execute at @s run function rpg:taint/advent_at"
    assert needle in src
    if "pact/clear/bind" not in src:
        write("taint/advent.mcfunction", src.replace(needle, needle + "\nexecute at @s run function rpg:pact/clear/bind"))
    src = read("taint/demon_soul.mcfunction")
    needle = "execute on vehicle run scoreboard players set #ride rpg_fall 1"
    assert needle in src
    if "pact/clear/fell" not in src:
        write("taint/demon_soul.mcfunction", src.replace(
            needle, needle + "\nexecute if score #ride rpg_fall matches 0 at @s run function rpg:pact/clear/fell"))
    src = read("inquest/start_verdict.mcfunction")
    needle = "scoreboard players set @s rpg_ex_stage 4"
    assert needle in src
    if "pact/clear/fell" not in src:
        write("inquest/start_verdict.mcfunction", src.replace(needle, (
            "execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14] "
            "if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] rpg_rite_id "
            "at @s run function rpg:pact/clear/fell\n") + needle, 1))
    src = read("pact/mammon.mcfunction")
    line_re = re.compile(r"^execute as @e\[type=minecraft:item,distance=0\.6\.\.6,(.*)$", re.M)
    match = line_re.search(src)
    assert match
    lines = ["execute if score @s rpg_pact_lv matches %s as @e[type=minecraft:item,distance=0.6..%d,%s"
             % (gate, radius, match.group(1)) for gate, radius in (("..1", 6), ("2", 9), ("3..", 12))]
    write("pact/mammon.mcfunction", line_re.sub("\n".join(lines), src))


def patch_hud():
    messages = {
        HUD_DENY: ["", text("[契约]", ui.RITUAL, True), text("　柱中之力还没回气")],
        HUD_LOCKED: ["", text("[契约]", ui.RITUAL, True), text("　契约还不够深")],
        HUD_TIER: ["", text("[深契]", ui.HOLY_DARK, True), text("　契约更进一阶"), text(" ✦", "white")],
        HUD_FALL: ["", text("[违约]", ui.WARN, True), text("　契合散尽，阶位跌落")],
    }
    for p in PILLARS:
        messages[HUD_TABOO + p["n"] - 1] = ["", text("[违约]", ui.WARN, True),
                                            text("　" + DEPTH[p["n"]]["taboo"] + " —— ", ui.GRAY),
                                            text(p["who"] + "记下了", p["lit"])]
    msg = read("hud/msg.mcfunction").rstrip("\n").splitlines()
    msg = [l for l in msg if not any("rpg_hud_m=%d}" % m in l for m in messages)]
    for mid, comp in messages.items():
        write("hud/m%d.mcfunction" % mid,
              "scoreboard players set @s rpg_hud_m %d\nscoreboard players set @s rpg_hud_mt 40" % mid)
        msg.append("execute if entity @s[scores={rpg_hud_m=%d}] run title @s actionbar %s"
                   % (mid, json.dumps(comp, ensure_ascii=False, separators=(",", ":"))))
    write("hud/msg.mcfunction", msg)

    # 契约对象段：柱名、阶位，再加魂誓和化身的就绪标记。
    ready, wait = pa.seg("◆", ui.READY), pa.seg("◇", ui.MUTED)
    for p in PILLARS:
        def identity(lv, *marks):
            return pa.row(pa.seg("　│　契约 ", "dark_gray"), pa.seg(p["who"], p["lit"], True),
                          pa.seg(" · " + TIERS[lv - 1], p["lit"]), pa.seg(" ", "gray"), *marks)

        def put(gate, comp):
            return "execute %s run data modify storage rpg:hud b set value '%s'" % (gate, comp)

        lines = [put("if score @s rpg_pact_lv matches ..1", identity(1)),
                 put("if score @s rpg_pact_lv matches 2 if score @s rpg_pact_cd2 matches 0", identity(2, ready)),
                 put("if score @s rpg_pact_lv matches 2 if score @s rpg_pact_cd2 matches 1..", identity(2, wait))]
        for gate2, mark2 in (("0", ready), ("1..", wait)):
            for gate3, mark3 in (("0", ready), ("1..", wait)):
                lines.append(put("if score @s rpg_pact_lv matches 3 if score @s rpg_pact_cd2 matches %s if score @s rpg_pact_cd3 matches %s"
                                 % (gate2, gate3), identity(3, mark2, mark3)))
        lines.append(put("if score @s rpg_pact_av matches 1..", identity(3, pa.seg("◆◆", ui.HOLY_DARK, True))))
        write("hud/pact%d.mcfunction" % p["n"], lines)


def patch_borrow():
    """新约借力也认副手的书，否则放在副手时白扣共享冷却。"""
    src = read("divine/borrow.mcfunction")
    write("divine/borrow.mcfunction", src.replace("weapon.mainhand *[", "weapon.* *["))


def patch_panel():
    src = read("panel/pact.mcfunction").rstrip("\n").splitlines()
    home = next(i for i, l in enumerate(src) if "[返回面板]" in l)
    extra = []
    for lv in (1, 2, 3):
        extra.append("execute if score @s rpg_pact matches 1..7 if score @s rpg_pact_lv matches %d run tellraw @s %s"
                     % (lv, raw(text("契约阶位："), text("第%s阶 · %s" % ("一二三"[lv - 1], TIERS[lv - 1]), ui.RITUAL, True))))
    extra.append("execute if score @s rpg_pact matches 1..7 run tellraw @s %s"
                 % raw(text("契合度："), {"score": {"name": "@s", "objective": "rpg_pact_bond"}, "color": ui.RITUAL, "italic": False},
                       text(" / %d" % BOND_MAX, "dark_gray")))
    extra.append("execute if score @s rpg_pact_dom matches 1 run tellraw @s %s" % raw(text("支配：枷锁减半", ui.HOLY_DARK, True)))
    for p in PILLARS:
        d = DEPTH[p["n"]]
        extra.append("execute if score @s rpg_pact matches %d run tellraw @s %s"
                     % (p["n"], raw(text("供奉："), text(d["oath"], "white"), text("　禁忌："), text(d["taboo"], ui.WARN))))
    extra.append("execute if score @s rpg_pact matches 1..7 run tellraw @s %s" % raw(text("潜行低头长按书，打开契约", ui.MUTED)))
    write("panel/pact.mcfunction", src[:home] + extra + src[home:])


def build_art():
    td = os.path.join(RP, "assets/rpg/textures/item")
    md = os.path.join(RP, "assets/rpg/models/item")
    items = os.path.join(RP, "assets/minecraft/items")

    def install(name):
        shutil.copyfile(os.path.join(ART, name + ".png"), os.path.join(td, name + ".png"))
        with io.open(os.path.join(md, name + ".json"), "w", encoding="utf-8", newline="\n") as handle:
            json.dump({"parent": "item/generated", "textures": {"layer0": "rpg:item/" + name}}, handle)

    def entry(cmd, name):
        return {"threshold": cmd, "model": {"type": "minecraft:model", "model": "rpg:item/" + name}}

    path = os.path.join(items, "enchanted_book.json")
    with io.open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    keep = [e for e in data["model"]["entries"] if e["threshold"] < pa.CMD_T2]
    for p in PILLARS:
        for lv in (2, 3):
            name = "pact_%s_t%d" % (SLUG[p["n"]], lv)
            install(name)
            keep.append(entry(pa.book_cmd(p["n"], lv), name))
    data["model"]["entries"] = sorted(keep, key=lambda e: e["threshold"])
    with io.open(path, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)

    paper = []
    for p in PILLARS:
        name = "page_" + SLUG[p["n"]]
        install(name)
        paper.append(entry(PAGE_CMD + p["n"], name))
    for seal in range(1, 36):
        n, role, _ = spirit_of(seal)
        name = "seal_%s_%d" % (SLUG[n], role)
        install(name)
        paper.append(entry(SEAL_CMD + seal, name))
    with io.open(os.path.join(items, "paper.json"), "w", encoding="utf-8", newline="\n") as handle:
        json.dump({"model": {"type": "minecraft:range_dispatch", "property": "minecraft:custom_model_data",
                             "index": 0, "fallback": {"type": "minecraft:model", "model": "minecraft:item/paper"},
                             "entries": paper}}, handle, ensure_ascii=False, indent=2)


def build_debug():
    write("pact/debug/bond.mcfunction", ["# 契合度加满。", "scoreboard players set @s rpg_pact_bond %d" % BOND_MAX])
    write("pact/debug/up.mcfunction", ["# 直接升一阶，不要材料也不要击败领主。",
                                       "execute if score @s rpg_pact_lv matches 3.. run return 0",
                                       "function rpg:pact/up_done"])
    write("pact/debug/materials.mcfunction", ["# 七柱祭品和五职材料各一组。"] +
          ["execute run give @s %s %d" % (DEPTH[n]["tribute"][0], pa.TRIBUTE) for n in range(1, 8)] +
          ["execute run give @s %s %d" % (item, UP_ITEMS) for item, _ in ROLE_ITEMS])
    write("pact/debug/lords.mcfunction", ["# 记为已击败七位领主。"] + ["tag @s add rpg.pw.%d" % n for n in range(1, 8)])


def main():
    shutil.rmtree(os.path.join(DATA, "dialog"), ignore_errors=True)
    patch_scoreboard()
    build_debug()
    build_items()
    build_loot()
    build_sign()
    build_oath()
    build_skills()
    build_ui()
    build_seals()
    build_clear()
    patch_tick()
    patch_lifecycle()
    patch_borrow()
    patch_hud()
    patch_panel()
    build_art()
    print("pact depth: 3 tiers, 7 oaths, 14 skills, 35 pages, 35 seals")


if __name__ == "__main__":
    main()
