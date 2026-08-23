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


def strip_passengers(line):
    """把 `Passengers:[ ... ]` 整段挖掉。

    `summon` 捕到的是**坐骑**的类型，而 Passengers 里那些 Tags 长在**骑手**
    身上。包里的溺尸骑士正是这个形状：

        summon horse ~ ~ ~ {... Passengers:[{id:drowned, Tags:["king_tag"] ...}]}

    不挖掉的话，king_tag 会被记成 horse，重写出来的
    `@e[type=minecraft:horse,tag=king_tag]` **一个实体都匹配不到** ——
    语法合法，validate 与服务器都不会吭声，功能却静悄悄地没了。

    这里选择保守：挖掉整段，让里面的标签一律算作"来路不明"，于是不会被收窄。
    也可以去解析骑手自己的 `id:`，但嵌套骑乘会让这件事变复杂 ——
    而在一个自动批量重写器里，多省几处遍历远不如"绝不改错"值钱。

    返回 (挖干净的那一行, 被挖走的骑手块列表)。
    """
    out, ridden, i = [], [], 0
    while True:
        m = re.search(r"Passengers:\[", line[i:])
        if not m:
            out.append(line[i:])
            return "".join(out), ridden
        start = i + m.start()
        out.append(line[i:start])
        j, depth = i + m.end() - 1, 0
        while j < len(line):
            if line[j] == "[":
                depth += 1
            elif line[j] == "]":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        ridden.append(line[start:j + 1])
        i = j + 1
        if j >= len(line):                    # 括号没闭合，剩下的整段丢弃
            return "".join(out), ridden


def collect():
    """标签 -> 召唤它的实体类型集合；以及所有"来路不明"的标签。

    来路不明有两种：被 `tag ... add` 挂上去的（可能落在任何实体上），
    以及出现在 `Passengers:` 里的。后者单靠挖掉还不够安全 ——
    假如同一个标签既直接召唤在 A 类型上、又作为 B 类型的骑手出现，
    挖掉之后只看得见 A，收窄成 A 就会漏掉所有 B。
    所以凡是在骑手块里露过面的标签，一律不收窄。
    """
    from_summon = {}
    unknown = set()
    for p in walk():
        text = io.open(p, encoding="utf-8").read()
        for line in text.split("\n"):
            if line.lstrip().startswith("#"):
                continue
            outer, ridden = strip_passengers(line)
            for m in SUMMON.finditer(outer):
                etype, rest = m.group(1), m.group(2)
                for tm in TAGS_NBT.finditer(rest):
                    for t in re.findall(r'"([^"]+)"', tm.group(1)):
                        from_summon.setdefault(t, set()).add(etype)
            for chunk in ridden:
                for tm in TAGS_NBT.finditer(chunk):
                    unknown.update(re.findall(r'"([^"]+)"', tm.group(1)))
            for m in TAG_ADD.finditer(line):
                unknown.add(m.group(1))
    return from_summon, unknown


def main():
    from_summon, unknown = collect()

    safe = {}
    for tag, types in sorted(from_summon.items()):
        if tag in unknown:
            continue            # 可能落在任何实体上，补类型会改语义
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
