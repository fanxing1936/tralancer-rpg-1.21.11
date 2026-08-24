# -*- coding: utf-8 -*-
"""构建期检查：攻击用的苦力怕必须当场引爆。

这一类错误是**完全静默**的。`Fuse:0` 在 1.21.11 已经不是字段了（实测：
苦力怕的 NBT 里既没有 `Fuse` 也没有 `fuse`，写进 summon 会被直接丢掉），
于是本该当场炸开的苦力怕变成普通苦力怕，站在原地追着人跑 ——
服务器不报错，validate 也看不出来，只有在游戏里才发现。

现在让它在构建期就暴露：凡是召唤苦力怕的地方，都必须带 `ignited:1b`。

**唯一的例外**是 `command/spawn/creeper.mcfunction` —— 那不是攻击，
那是世界里自然生成的苦力怕被换成变种（带电的大只、或三只小快的）。
它们本来就该在世界里走动；给它们点上引信，等于每一只苦力怕
一出生就在原地炸个坑。所以那个文件整体豁免。
"""
import io
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(ROOT, "data/rpg/function")

# 自然生成的变种表：它们是世界里的苦力怕，不是武器效果
EXEMPT = ("command/spawn/creeper.mcfunction",)

SUMMON = re.compile(r"summon\s+(?:minecraft:)?creeper\b[^\n]*")


def main():
    bad = []
    for base, _d, files in os.walk(FUNC):
        for f in files:
            if not f.endswith(".mcfunction"):
                continue
            p = os.path.join(base, f)
            rel = os.path.relpath(p, FUNC).replace("\\", "/")
            if rel in EXEMPT:
                continue
            for i, line in enumerate(io.open(p, encoding="utf-8"), 1):
                for m in SUMMON.finditer(line):
                    if "ignited" not in m.group(0):
                        bad.append("%s:%d" % (rel, i))

    if bad:
        print("creeper check: %d 处召唤没有 ignited:1b（会站着不炸）" % len(bad))
        for b in bad:
            print("  " + b)
        return 1
    print("creeper check: 攻击用的苦力怕全部当场引爆")
    return 0


if __name__ == "__main__":
    sys.exit(main())
