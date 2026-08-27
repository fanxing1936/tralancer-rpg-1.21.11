# -*- coding: utf-8 -*-
"""把既有第一章与七柱回廊接进玩家能自然遇见的流程。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from rpg_ui_style import (GRAY, HOLY_DARK, HOLY_LIGHT, RED, RITUAL, WHITE,
                          comp, item_name, lore, prefix_message)


DP = Path(sys.argv[1] if len(sys.argv) > 1 else "../rpg").resolve()
FUNC = DP / "data" / "rpg" / "function"
ADV = DP / "data" / "rpg" / "advancement" / "entry"


def read(rel: str) -> str:
    return (FUNC / rel).read_text(encoding="utf-8")


def write(rel: str, source: str) -> None:
    target = FUNC / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source.rstrip("\n") + "\n", encoding="utf-8", newline="\n")


def patch_once(rel: str, needle: str, replacement: str) -> None:
    source = read(rel)
    if source.count(needle) != 1:
        raise RuntimeError("entry-point anchor changed in %s" % rel)
    write(rel, source.replace(needle, replacement, 1))


def tell(selector: str, payload: str) -> str:
    return "tellraw %s %s" % (selector, payload)


def active_item(base: str, name: str, item_lore: str, marker: str, sound: str) -> str:
    # 原生翻书界面不会稳定进入 using_item；书形底材保留叙事语义，长使用组件负责唯一可靠的右键入口。
    return (
        "%s[minecraft:custom_name=%s,minecraft:lore=%s,"
        "minecraft:food={nutrition:0,saturation:0f,can_always_eat:1b},"
        "minecraft:consumable={consume_seconds:100160f,animation:\"block\","
        "sound:\"%s\",has_consume_particles:false,on_consume_effects:[]},"
        "minecraft:max_stack_size=1,minecraft:enchantment_glint_override=true,"
        "minecraft:custom_data={%s:1b}]"
        % (base, name, item_lore, sound, marker)
    )


ROSTER = active_item(
    "minecraft:book",
    item_name("[调查]", "教区名册", HOLY_DARK),
    lore([
        [comp("被划去的姓名占了不止一页。", GRAY)],
        [comp("刚刚散去的空壳，只是其中一例。", WHITE)],
        [comp("这个空壳不是孤例；有人在系统地留下它们。", GRAY)],
        [comp("带到远离聚落的旷野，长按右键展开调查。", HOLY_LIGHT)],
    ]),
    "rpg_ch1_roster",
    "minecraft:item.book.page_turn",
)

CORRIDOR_TOKEN = active_item(
    "minecraft:echo_shard",
    item_name("[回廊]", "七柱回廊信物", RITUAL),
    lore([
        [comp("一柱真名落定，另外七十一道刻痕随之亮起。", GRAY)],
        [comp("它在等待一个已经见证过真名的人。", WHITE)],
        [comp("长按右键回应回廊。", HOLY_LIGHT)],
    ]),
    "rpg_endless_token",
    "minecraft:block.end_portal_frame.fill",
)


def build_invites() -> None:
    write("entry/chapter/invite.mcfunction", "\n".join([
        "execute if entity @s[tag=rpg.ch1.invited] run return 0",
        # 标签先于物品落地，背包满导致掉落也不能把同一次邀请误判为未发放。
        "tag @s add rpg.ch1.invited",
        "give @s " + ROSTER,
        tell("@s", prefix_message("[调查线索] ", HOLY_DARK,
                                  "教区名册已交给你；若背包已满，它掉在你脚边。")),
        "playsound minecraft:item.book.page_turn player @s ~ ~ ~ 0.9 0.8",
    ]))
    write("entry/endless/invite.mcfunction", "\n".join([
        "execute if entity @s[tag=rpg.endless.invited] run return 0",
        # 真名可被测试重置，邀请资格不能随之重置，否则每一柱都会补发一件信物。
        "tag @s add rpg.endless.invited",
        "give @s " + CORRIDOR_TOKEN,
        tell("@s", prefix_message("[回廊来信] ", RITUAL,
                                  "七柱回廊留下了信物；若背包已满，它掉在你脚边。")),
        "playsound minecraft:block.end_portal_frame.fill player @s ~ ~ ~ 0.8 1.2",
    ]))

    taint_line = "execute as @a[distance=..8] run scoreboard players remove @s rpg_taint 5"
    patch_once(
        "rite/free.mcfunction",
        taint_line,
        taint_line + "\nexecute as @a[distance=..8,tag=!rpg.ch1.invited] run function rpg:entry/chapter/invite",
    )
    for pillar in range(1, 8):
        tag_line = "tag @s add rpg.name.%d" % pillar
        patch_once(
            "inquest/reveal/%d.mcfunction" % pillar,
            tag_line,
            tag_line + "\nexecute unless entity @s[tag=rpg.endless.invited] run function rpg:entry/endless/invite",
        )


def build_advancement(name: str, marker: str, reward: str) -> None:
    ADV.mkdir(parents=True, exist_ok=True)
    doc = {
        "criteria": {"use": {
            "trigger": "minecraft:using_item",
            "conditions": {"item": {"predicates": {
                "minecraft:custom_data": "{%s:1b}" % marker,
            }}},
        }},
        "rewards": {"function": reward},
    }
    (ADV / (name + ".json")).write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8", newline="\n")


def build_use_routes() -> None:
    chapter_busy = prefix_message("[名册未展开] ", RED,
                                  "已有章节或回廊实例正在运行；请先完成或结束它。")
    wrong_world = prefix_message("[名册未展开] ", RED,
                                  "请回到主世界、退出旁观模式，再到旷野打开名册。")
    settlement = prefix_message("[名册未展开] ", RED,
                                "这里离聚落太近。带着名册走到旷野（72 格内无村民与铁傀儡）再打开。")
    conflict = prefix_message("[名册未展开] ", RED,
                              "附近还有恶魔战斗或活动法阵；先收尾，再到旷野打开名册。")
    write("entry/chapter/use.mcfunction", "\n".join([
        # using_item 在按住期间持续判定；延迟重置只负责去抖，不引入新的每刻遍历。
        "schedule function rpg:entry/chapter/rearm 20t replace",
        "execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] run return run " + tell("@s", chapter_busy),
        "execute if entity @e[type=minecraft:marker,tag=rpg.end.controller,limit=1] run return run " + tell("@s", chapter_busy),
        "execute if entity @s[gamemode=spectator] run return run " + tell("@s", wrong_world),
        "execute unless dimension minecraft:overworld run return run " + tell("@s", wrong_world),
        "execute if entity @e[type=minecraft:villager,distance=..72,limit=1] run return run " + tell("@s", settlement),
        "execute if entity @e[type=minecraft:iron_golem,distance=..72,limit=1] run return run " + tell("@s", settlement),
        "execute if entity @e[tag=rpg.advent,distance=..72,limit=1] run return run " + tell("@s", conflict),
        "execute if entity @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..72,limit=1] run return run " + tell("@s", conflict),
        "tag @s add rpg.ch1.roster.open",
        "function rpg:campaign/beelzebub/start",
        "tag @s remove rpg.ch1.roster.open",
    ]))
    write("entry/chapter/rearm.mcfunction",
          "advancement revoke @a only rpg:entry/chapter_use")

    endless_busy = prefix_message("[信物沉寂] ", RED,
                                  "已有七柱回廊正在运行；请加入，或等本轮结束后再回应。")
    chapter_running = prefix_message("[信物沉寂] ", RED,
                                     "第一章调查尚未结束；结案后再回应回廊。")
    write("entry/endless/use.mcfunction", "\n".join([
        "schedule function rpg:entry/endless/rearm 20t replace",
        "execute if entity @e[type=minecraft:marker,tag=rpg.end.controller,limit=1] run return run " + tell("@s", endless_busy),
        "execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] run return run " + tell("@s", chapter_running),
        "function rpg:endless/start",
    ]))
    write("entry/endless/rearm.mcfunction",
          "advancement revoke @a only rpg:entry/endless_use")

    build_advancement("chapter_use", "rpg_ch1_roster", "rpg:entry/chapter/use")
    build_advancement("endless_use", "rpg_endless_token", "rpg:entry/endless/use")


def patch_preflight_message() -> None:
    rel = "campaign/beelzebub/scene/preflight.mcfunction"
    source = read(rel)
    old = source.splitlines()[-1]
    if "采样覆盖" not in old:
        raise RuntimeError("chapter terrain preflight message changed")
    human = tell("@s", prefix_message(
        "[名册未展开] ", "#8B2500",
        "前方铺不开调查现场。面朝一片至少 37×65 格、上方净空 5 格的平整旷野再打开。"))
    # 管理入口保留诊断坐标；玩家从名册进入时只收到能据此换地方的尺寸提示。
    replacement = (
        "execute if entity @s[tag=rpg.ch1.roster.open] run return run " + human + "\n"
        "execute unless entity @s[tag=rpg.ch1.roster.open] run " + old
    )
    patch_once(rel, old, replacement)


def main() -> None:
    build_invites()
    build_use_routes()
    patch_preflight_message()
    print("entry points: parish roster -> chapter 1 / true-name token -> endless corridor")


if __name__ == "__main__":
    main()
