# -*- coding: utf-8 -*-
"""找出「一边遍历实体、一边往这个遍历里召唤新实体」的循环。

熔岩链锯就栽在这里：

    execute as @e[distance=0.1..3.5,type=!player,type=!item,type=!experience_orb]
        at @s run summon minecraft:evoker_fangs ...

选择器排除了玩家、掉落物、经验球 —— **唯独没排除尖牙自己**。于是这一轮会在
上一轮召出的每一只尖牙旁边再召一只：第 n 代生第 n+1 代。六轮切割下来是
指数爆炸，服务器当场跪下。

这类错既不是语法错也不是逻辑错 —— 每一条命令单看都对，只有把它们连起来
跑几轮才看得见。所以在构建期扫一遍。

## 危险的判据不是"有没有排除类型"

包里有几十处 `as @e[...] run summon ...` 都不排除类型，却完全安全 ——
因为它们的选择器要求一个**新实体不可能满足**的条件：

* `@e[tag=devil,tag=boss]` 召苦力怕 —— 新召的苦力怕没有这两个标签
* `@e[tag=rpg.hurt]` 召光灵箭 —— 新召的箭不会被标成"刚受伤"
* `@e[type=item,tag=rpg.i.loot1]` 召掉落物 —— 新召的没有那个标签
* 任何带 `scores=` 的 —— 新实体身上根本没有分数

真正危险的签名是：**召出来的东西下一轮会自己撞进同一个选择器**。
也就是说选择器只有类型与距离这类"天生就满足"的条件，而召唤又没被排除。
链锯那一条正是如此。

所以判据是「这个新实体有没有可能匹配上」，而不是「有没有写 type=!」。
"""

import io
import os
import re
import sys

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data/rpg/function")

LOOP = re.compile(r"execute as (@e\[[^\]]*\]).*?\brun summon\s+((?:minecraft:)?\w+)(.*)$")


def short(t):
    return t.split(":")[-1]


def safe(sel, etype, nbt):
    """新召出来的 etype 有没有可能在下一轮撞进 sel。"""
    t = short(etype)

    # 明确排除了这个类型
    if ("type=!minecraft:%s" % t) in sel or ("type=!%s" % t) in sel:
        return True

    # 钉死成另一个具体类型
    m = re.search(r"(?:^|,|\[)type=(?!!)((?:minecraft:)?\w+)", sel)
    if m and short(m.group(1)) != t:
        return True

    # 要求分数 —— 新实体身上没有任何分数，匹配不上
    if "scores=" in sel:
        return True

    # 要求某个标签，而召唤没给它这个标签
    for tag in re.findall(r"(?:^|,|\[)tag=(?!!)([\w.]+)", sel):
        if ('"%s"' % tag) not in nbt:
            return True

    # 要求某个名字，而召唤没给它这个名字
    for nm in re.findall(r"(?:^|,|\[)name=(?!!)([\w.]+)", sel):
        if nm not in nbt:
            return True

    return False


def main():
    bad = []
    scanned = 0
    for root, dirs, files in os.walk(FUNC):
        dirs.sort()
        for f in sorted(files):
            if not f.endswith(".mcfunction"):
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, FUNC).replace(os.sep, "/")
            for i, line in enumerate(io.open(p, encoding="utf-8").read().split("\n"), 1):
                if line.lstrip().startswith("#"):
                    continue
                m = LOOP.search(line)
                if not m:
                    continue
                scanned += 1
                sel, etype, nbt = m.group(1), m.group(2), m.group(3)
                if not safe(sel, etype, nbt):
                    bad.append((rel, i, short(etype), sel))

    print("summon loops: %d checked" % scanned)
    if not bad:
        print("  none can feed itself")
        return
    print("  !! %d loop(s) whose summon can match their own selector:" % len(bad))
    for rel, i, etype, sel in bad:
        print("     %s:%d" % (rel, i))
        print("       召唤 %s，而这个选择器拦不住它：%s" % (etype, sel))
        print("       -> 上一轮召出来的会成为下一轮的目标，代数增长")
    sys.exit(1)


if __name__ == "__main__":
    main()
