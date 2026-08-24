# -*- coding: utf-8 -*-
"""删掉苦力怕的变种体系（作者决定）。

原本自然生成的苦力怕会被换成变种：掷 10 换成一只带电的大个子（30 血），
掷 9 换成三只小而快的。问题是这些是**世界里的苦力怕**，它们会跟着你走、
在你身边等着炸 —— 作者要的是干净：苦力怕就是原版苦力怕。

整条链是自足的，`creeper` 这个标签除了它自己没有第二处引用，所以可以整段摘掉：

  command/tick            那一行分派
  command/spawn/creeper_batch   每刻挑 4 只
  command/spawn/creeper         掷点换变种

删掉之后，**攻击用**的苦力怕（武器技能、boss 招式）一条都不受影响 ——
它们是各自 summon 出来的，与这套自然生成的替换无关。

必须跑在 opt_spawn / opt_cascade **之后**：那两步才刚把这些文件生成出来。
"""
import io
import os
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(ROOT, "data/rpg/function")

DEAD = ("command/spawn/creeper.mcfunction",
        "command/spawn/creeper_batch.mcfunction")

# tick 里那一行分派
CALL = "rpg:command/spawn/creeper_batch"


def main():
    gone = 0
    for rel in DEAD:
        p = os.path.join(FUNC, rel)
        if os.path.isfile(p):
            os.remove(p)
            gone += 1

    p = os.path.join(FUNC, "command/tick.mcfunction")
    cut = 0
    if os.path.isfile(p):
        lines = io.open(p, encoding="utf-8").read().split("\n")
        keep = [l for l in lines if CALL not in l]
        cut = len(lines) - len(keep)
        if cut:
            io.open(p, "w", encoding="utf-8", newline="\n").write("\n".join(keep))

    print("creeper variants: 删掉 %d 个文件，摘掉 %d 行分派" % (gone, cut))


if __name__ == "__main__":
    main()
