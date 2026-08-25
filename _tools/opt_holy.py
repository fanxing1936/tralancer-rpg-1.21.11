# -*- coding: utf-8 -*-
"""在玩家索引里加一条「圣器在身」，并且**穿戴也算**。

原本"持圣器"只看主手（`rpg.h.holy_weapon_tag1`）。护甲拿在手里才算数是荒谬的 ——
圣荆棘冠、都灵裹尸布这些当然应该穿着算。

为什么另开 `rpg.holy` 而不是扩写原来那个：`rpg.h.` 前缀的语义是**手里握着**，
神圣分支武器的命中特效（`item/sword/legend/holy/holy.mcfunction`）读的就是它。
把穿戴混进去，会变成戴着圣冠打人也冒圣光。所以分成两个语义：

* `rpg.h.holy_weapon_tag1` —— 手里握着（分支特效继续用，语义不变）
* `rpg.holy`　　　　　　　 —— 圣器在身（驱魔体系用：空缺者显形、魔化消退、
  濒临魔化时的灼手，以及免疫黑暗与失明）

黑暗与失明不能只在某几个攻击函数里加 `unless`：原包 Boss、毁约、逆圣化失败、
魔化阶段都会施加这两种效果，玩家还可能在拿起圣器之前就已经带着持续效果。
因此统一在最后执行的 `command/tick_end` 逐个处理 `rpg.holy` 玩家。这样本包这一刻
不论从哪条路径施加，都会在同一刻结算末尾清掉；既存效果也一样清除。

这一趟必须跑在 `opt_index.py` **之后** —— index_player 是那一步才生成出来的。
"""

import io
import json
import os
import sys

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data/rpg/function")
COMMAND = os.path.join(FUNC, "command")

# 圣器可以在这些槽位上生效
SLOTS = ("weapon.mainhand", "weapon.offhand",
         "armor.head", "armor.chest", "armor.legs", "armor.feet")

# 神圣分支有**三级**：item_modifier 的 holy / holy2 / holy3 分别写
# holy_weapon_tag 1b / 2b / 3b（实测确认是 byte）。
# 原来这里只判 1b —— 于是武器升到二三级之后反而不算圣器了，正好反过来。
#
# 槽位组 `armor.*` 在 `if items entity` 里匹配不到（实测），
# 所以六个槽位各写三条。都是直接读槽位、不搜实体，很便宜。
LEVELS = (1, 2, 3)

HOLY_EFFECTS = """# 圣器在身：黑暗与失明无法停留。
# 由 tick_end 以每名 rpg.holy 玩家为 @s 调用，玩家之间互不影响。
effect clear @s minecraft:blindness
effect clear @s minecraft:darkness
"""

TICK_END_CALL = (
    "execute as @a[tag=rpg.holy] run function rpg:command/holy_effects")


def main():
    p = os.path.join(FUNC, "command/index_player.mcfunction")
    if not os.path.isfile(p):
        print("holy worn: index_player not found, skipped")
        return
    s = io.open(p, encoding="utf-8").read()
    if "rpg.holy" not in s:
        # 清标记要和其余 rpg.h.* 一起做，放在第一条检测行之前
        first = "execute if items entity @s"
        assert first in s, "index_player 不是预期的形状"
        i = s.index(first)
        s = s[:i] + "tag @s remove rpg.holy\n" + s[i:]

        s = s.rstrip("\n") + "\n\n" + (
            "# 圣器在身。与 rpg.h.holy_weapon_tag1 分开：那个的语义是「手里握着」，\n"
            "# 神圣分支的命中特效读的是它；而驱魔体系问的是「身上有没有圣性之物」，\n"
            "# 护甲当然应该穿着算。\n"
            + "\n".join(
                "execute if items entity @s %s "
                "*[minecraft:custom_data~{holy_weapon_tag:%db}] run tag @s add rpg.holy"
                % (slot, lv) for slot in SLOTS for lv in LEVELS)
            + "\n")
        io.open(p, "w", encoding="utf-8", newline="\n").write(s)
        print("holy worn: rpg.holy set from %d slot(s) x %d level(s) (held + worn)"
              % (len(SLOTS), len(LEVELS)))
    else:
        print("holy worn: already present")

    # 所有来源共用一个结算末尾的净化点。tick_end 是构建流水线保证的
    # #minecraft:tick 最后一项，所以原包其余 tick 函数刚施加的效果也不会漏过。
    effect_p = os.path.join(COMMAND, "holy_effects.mcfunction")
    io.open(effect_p, "w", encoding="utf-8", newline="\n").write(HOLY_EFFECTS)

    tick_p = os.path.join(COMMAND, "tick_end.mcfunction")
    assert os.path.isfile(tick_p), "tick_end 不存在，无法保证结算顺序"
    tick_tag_p = os.path.join(DP, "data/minecraft/tags/function/tick.json")
    tick_tag = json.load(io.open(tick_tag_p, encoding="utf-8"))
    assert tick_tag.get("values", [])[-1:] == ["rpg:command/tick_end"], (
        "tick_end 不是 #minecraft:tick 最后一项，圣器免疫可能被同刻后续效果覆盖")
    tick = io.open(tick_p, encoding="utf-8").read().rstrip("\n")
    if TICK_END_CALL not in tick:
        tick += "\n\n# 最后一刻清除圣器持有者的视觉遮蔽。\n" + TICK_END_CALL
        io.open(tick_p, "w", encoding="utf-8", newline="\n").write(tick + "\n")
    print("holy effects: blindness + darkness cleared per holy player at tick_end")


if __name__ == "__main__":
    main()
