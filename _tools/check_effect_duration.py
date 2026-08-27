# -*- coding: utf-8 -*-
"""构建期检查：`effect give` 的时长不许带刻后缀。

`effect give <目标> <效果> <时长> ...` 的时长只收**整数秒**或 `infinite`。
`12t` 那种写法是 `/time` 与 `schedule` 的语法，写进 `effect give` 会让
**整个函数在加载时被服务器拒绝** —— 不是那一行失效，是整份文件不生效。

为什么值得单开一道检查：这一类错误 `validate.py` 看不出来（它检查的是
括号配对与宏行，不解析参数类型），服务器日志里只有一行 Java 异常，
而玩家侧的表现是"这个能力毫无反应"。实际踩过一次：别西卜的吞噬残魂写成
`regeneration 12t 3`，算得很准（再生 IV 每 6 刻跳一次，12/18/24/36 刻正好
回 2/3/4/6 点），但整份 ability 文件从未加载。

顺带也拦住 `effect clear` 之外的同类笔误：时长位置出现任何非数字尾巴。
"""
import io
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(ROOT, "data/rpg/function")

# effect give <sel> <effect> <duration> —— 抓时长那一段带字母尾巴的写法
BAD = re.compile(r"effect\s+give\s+\S+\s+[\w:]+\s+(\d+)([a-zA-Z]+)\b")


def main():
    bad = []
    for base, _d, files in os.walk(FUNC):
        for f in files:
            if not f.endswith(".mcfunction"):
                continue
            p = os.path.join(base, f)
            rel = os.path.relpath(p, FUNC).replace("\\", "/")
            for i, line in enumerate(io.open(p, encoding="utf-8"), 1):
                m = BAD.search(line)
                if m and m.group(2) != "infinite":
                    bad.append("%s:%d  时长写成 %s%s（只收整数秒）"
                               % (rel, i, m.group(1), m.group(2)))
    if bad:
        print("effect duration check FAILED (%d):" % len(bad))
        for b in bad:
            print("  - " + b)
        return 1
    print("effect duration check PASS: 没有带刻后缀的 effect give")
    return 0


if __name__ == "__main__":
    sys.exit(main())
