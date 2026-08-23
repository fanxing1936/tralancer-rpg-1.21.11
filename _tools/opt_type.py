# -*- coding: utf-8 -*-
"""给"只由 summon 产生"的标签选择器补上实体类型。

`@e[tag=rpg.levi.anchor]` 必须走一遍全实体表；`@e[type=minecraft:armor_stand,
tag=rpg.levi.anchor]` 走类型索引，只看那一类。语义完全相同，代价差一个数量级。

类型不用手填 —— 它就写在召唤这些实体的那条 `summon` 里。这一趟：

1. 收集每个标签的来源。`summon <type> ... Tags:["x"]` 记一笔类型；
   **`tag @... add x` 记一笔"来路不明"**。
2. 只有**从未**被 `tag ... add` 写过、且所有召唤点类型一致的标签才算安全 ——
   否则这个标签可能挂在任何实体上，补类型会改变语义。
3. 给这些标签的无类型 `@e[...]` 选择器补上 `type=`。

这不是多人专属的优化，但它和多人直接相关：全表走查的代价随世界里的实体数
增长，而实体数正是随在线人数增长的东西。
"""

import io
import os
import re
import sys

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data/rpg/function")

SUMMON = re.compile(r"summon\s+(?:minecraft:)?(\w+)\b([^\n]*)")
TAGS_NBT = re.compile(r'Tags:\[([^\]]*)\]')
TAG_ADD = re.compile(r"tag\s+@\S+\s+add\s+(\S+)")
SEL = re.compile(r"@e\[([^\]]*)\]")


def walk():
    for root, dirs, files in os.walk(FUNC):
        dirs.sort()
        for f in sorted(files):
            if f.endswith(".mcfunction"):
                yield os.path.join(root, f)


def collect():
    """标签 -> 召唤它的实体类型集合；以及被 `tag ... add` 写过的标签。"""
    from_summon = {}
    from_command = set()
    for p in walk():
        text = io.open(p, encoding="utf-8").read()
        for line in text.split("\n"):
            if line.lstrip().startswith("#"):
                continue
            for m in SUMMON.finditer(line):
                etype, rest = m.group(1), m.group(2)
                for tm in TAGS_NBT.finditer(rest):
                    for t in re.findall(r'"([^"]+)"', tm.group(1)):
                        from_summon.setdefault(t, set()).add(etype)
            for m in TAG_ADD.finditer(line):
                from_command.add(m.group(1))
    return from_summon, from_command


def main():
    from_summon, from_command = collect()

    safe = {}
    for tag, types in sorted(from_summon.items()):
        if tag in from_command:
            continue            # 也可能被挂到任意实体上，补类型会改语义
        if len(types) != 1:
            continue            # 同一个标签召唤出不止一种实体
        safe[tag] = types.pop()

    if not safe:
        print("type index: nothing safe to narrow")
        return

    order = sorted(safe, key=len, reverse=True)      # 长标签优先，避免前缀误伤
    changed = files = 0
    for p in walk():
        text = io.open(p, encoding="utf-8").read()
        out = []
        touched = False
        for line in text.split("\n"):
            if line.lstrip().startswith("#"):
                out.append(line)
                continue

            def fix(m):
                global_changed = False
                inner = m.group(1)
                if "type=" in inner:
                    return m.group(0)
                for tag in order:
                    if re.search(r"(?:^|,)tag=%s(?:,|$)" % re.escape(tag), inner):
                        return "@e[type=minecraft:%s,%s]" % (safe[tag], inner)
                return m.group(0)

            new = SEL.sub(fix, line)
            if new != line:
                touched = True
                changed += 1
            out.append(new)
        if touched:
            io.open(p, "w", encoding="utf-8", newline="\n").write("\n".join(out))
            files += 1

    print("type index: %d selector(s) narrowed across %d file(s)" % (changed, files))
    for tag in sorted(safe):
        print("  %-24s -> %s" % (tag, safe[tag]))


if __name__ == "__main__":
    main()
