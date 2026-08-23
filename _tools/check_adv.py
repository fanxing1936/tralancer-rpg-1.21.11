# -*- coding: utf-8 -*-
"""比对进度触发器的条件字段名 —— 拿原版当字典。

写错一个字段名是**完全静默**的：`minecraft:item_used_on_block` 没有 `item`
字段（物品判定要塞进 `location` 里的 `match_tool`），而我按 `using_item` 的
样子写了 `"item": {...}`。那个键被整个忽略，条件变成空的，于是
**放任何一块方块**都会触发驱魔图腾。

`validate.py` 不报，服务器不报，无头测试也测不到（没有玩家就不会触发进度）。
只有在游戏里放一块石头才看得见。

所以这里不猜规则，直接**拿原版的 1584 个进度当字典**：统计每个触发器实际用过
哪些条件字段，再拿本包的进度去比。原版没用过的键就是可疑的。

这只是警告不是断言 —— 原版未必把每个合法字段都用过一遍。但它给出的信息足够
让人判断：报出来的时候，同时列出原版在这个触发器上用过什么。
"""

import io
import json
import os
import sys
import zipfile

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
JAR = (sys.argv[2] if len(sys.argv) > 2 else
       r"F:/筑梦 MCBE/HMCL启动器/新建文件夹/versions/1.21.11-Fabric/1.21.11-Fabric.jar")


def vanilla_vocab():
    """触发器 -> 原版实际用过的条件字段名集合。"""
    vocab = {}
    if not os.path.isfile(JAR):
        return None
    with zipfile.ZipFile(JAR) as z:
        for n in z.namelist():
            if "advancement" not in n or not n.endswith(".json"):
                continue
            try:
                doc = json.loads(z.read(n))
            except Exception:
                continue
            for crit in (doc.get("criteria") or {}).values():
                t = crit.get("trigger")
                if not t:
                    continue
                vocab.setdefault(t, set()).update((crit.get("conditions") or {}).keys())
    return vocab


def pack_advancements():
    root = os.path.join(DP, "data")
    for ns in sorted(os.listdir(root)):
        d = os.path.join(root, ns, "advancement")
        if not os.path.isdir(d):
            continue
        for sub, _dirs, files in os.walk(d):
            for f in sorted(files):
                if f.endswith(".json"):
                    p = os.path.join(sub, f)
                    yield os.path.relpath(p, root).replace(os.sep, "/"), p


def main():
    vocab = vanilla_vocab()
    if vocab is None:
        print("advancement fields: client jar not found, skipped")
        return
    bad = []
    checked = 0
    for rel, p in pack_advancements():
        try:
            doc = json.load(io.open(p, encoding="utf-8"))
        except Exception as e:
            bad.append((rel, "-", "无法解析：%s" % e, ""))
            continue
        for name, crit in (doc.get("criteria") or {}).items():
            t = crit.get("trigger")
            if not t:
                continue
            checked += 1
            known = vocab.get(t)
            if known is None:
                continue                       # 原版没用过这个触发器，无从比对
            for key in (crit.get("conditions") or {}):
                if key not in known:
                    bad.append((rel, t, key, ", ".join(sorted(known)) or "(原版从不带条件)"))

    print("advancement fields: %d criteria checked against %d vanilla triggers"
          % (checked, len(vocab)))
    if not bad:
        print("  no unknown condition fields")
        return
    print("  !! %d suspicious field(s) -- vanilla never uses these on that trigger:" % len(bad))
    for rel, t, key, known in bad:
        print("     %-46s %s" % (rel, t))
        print("       用了 `%s`，而原版在这个触发器上只用过：%s" % (key, known))
    sys.exit(1)


if __name__ == "__main__":
    main()
