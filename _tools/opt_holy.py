# -*- coding: utf-8 -*-
"""在玩家索引里加一条「圣器在身」，并且**穿戴也算**。

原本"持圣器"只看主手（`rpg.h.holy_weapon_tag1`）。护甲拿在手里才算数是荒谬的 ——
圣荆棘冠、都灵裹尸布这些当然应该穿着算。

为什么另开 `rpg.holy` 而不是扩写原来那个：`rpg.h.` 前缀的语义是**手里握着**，
神圣分支武器的命中特效（`item/sword/legend/holy/holy.mcfunction`）读的就是它。
把穿戴混进去，会变成戴着圣冠打人也冒圣光。所以分成两个语义：

* `rpg.h.holy_weapon_tag1` —— 手里握着（分支特效继续用，语义不变）
* `rpg.holy`　　　　　　　 —— 圣器在身（驱魔体系用：空缺者显形、魔化消退、
  以及濒临魔化时的灼手）

这一趟必须跑在 `opt_index.py` **之后** —— index_player 是那一步才生成出来的。
"""

import io
import os
import sys

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data/rpg/function")

# 圣器可以在这些槽位上生效
SLOTS = ("weapon.mainhand", "weapon.offhand",
         "armor.head", "armor.chest", "armor.legs", "armor.feet")


def main():
    p = os.path.join(FUNC, "command/index_player.mcfunction")
    if not os.path.isfile(p):
        print("holy worn: index_player not found, skipped")
        return
    s = io.open(p, encoding="utf-8").read()
    if "rpg.holy" in s:
        print("holy worn: already present")
        return

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
            "*[minecraft:custom_data~{holy_weapon_tag:1b}] run tag @s add rpg.holy"
            % slot for slot in SLOTS)
        + "\n")
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("holy worn: rpg.holy set from %d slot(s) (held + worn)" % len(SLOTS))


if __name__ == "__main__":
    main()
