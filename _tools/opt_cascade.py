# -*- coding: utf-8 -*-
"""掐断变种召唤的滚雪球。

图鉴写的是：「普通僵尸、骷髅、苦力怕在出生瞬间会被数据包重新洗牌…并有几率
**直接替换**成强化变种。」实现里两件事都没做到：

1. **召出来的变种没有"已处理"标记。** 于是它自己也算"新出生的僵尸"，
   下一刻被批处理捞起来再掷一次点 —— 又有几率再召出变种。一代接一代。
2. **原本那只没有被杀掉。** 所谓"替换"实际上是"追加"。

两件事叠起来是一个**亚临界分支过程**：僵尸那一支每处理一只，期望再产出
0.75 只未标记的僵尸（掷点 8 出 1 只、9 出 2 只、10 出 2 只、14–15 出 5 只，
除以 20）。0.75 < 1 所以不会爆炸，但收敛值是 1/(1-0.75) = **4 倍** ——
世界里每自然生成一只僵尸，最后会变成四只。

无头实测正是这个数：投放 60 只，稳定在 214 只（≈3.6 倍），
而 240 只实体时 200 刻的 sprint 跑了 46 秒都没跑完（>230 ms/刻，预算是 50）。

这一趟做两件事：

* 给每一个召唤出来的变种（含 `Passengers` 里嵌套的那些）打上族群标记，
  它们就不会再被当成新出生的重掷一遍 —— 雪球到此为止
* 掷点命中变种时把原本那只杀掉，让"替换"名副其实

只改这两处，不动任何掷点概率与变种数值。
"""

import io
import os
import re
import sys

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
SPAWN = os.path.join(DP, "data/rpg/function/command/spawn")

# 文件 -> (族群标记, 属于这个族群的实体 id)
FAMILY = {
    "zombie": ("zombie", {"zombie", "zombie_villager", "husk", "drowned",
                          "zombified_piglin", "giant"}),
    "skeleton": ("skeleton", {"skeleton", "stray", "wither_skeleton", "bogged"}),
    "creeper": ("creeper", {"creeper"}),
}

ROLL = re.compile(r"if score @s random matches ([0-9]+(?:\.\.[0-9]+)?)")


def tag_nbt(line, fam, ids):
    """给这一行里每一个属于本族群的实体都插上族群标记。

    顶层 `summon <id> ~ ~ ~ {` 与嵌套的 `{id:<id>,` / `{id:<id>}` 都要插 ——
    叠罗汉那一条的五只僵尸有四只是 Passengers，漏掉它们雪球照样滚。
    """
    def top(m):
        return ('summon %s%s {Tags:["%s"],' % (m.group(1), m.group(2), fam)
                if m.group(1).split(":")[-1] in ids else m.group(0))
    line = re.sub(r"summon ((?:minecraft:)?\w+)( ~ ~ ~) \{", top, line)

    def nested(m):
        if m.group(1).split(":")[-1] not in ids:
            return m.group(0)
        sep = m.group(2)
        return '{id:%s,Tags:["%s"]%s' % (m.group(1), fam,
                                         "" if sep == "}" else ",") + (
            "}" if sep == "}" else "")
    line = re.sub(r"\{id:((?:minecraft:)?\w+)([,}])", nested, line)
    return line


def main():
    total_tagged = total_killed = 0
    for stem, (fam, ids) in sorted(FAMILY.items()):
        p = os.path.join(SPAWN, stem + ".mcfunction")
        if not os.path.isfile(p):
            continue
        src = io.open(p, encoding="utf-8").read()
        if 'Tags:["%s"]' % fam in src:
            continue                                   # 已经改过
        out, rolls = [], []
        for line in src.split("\n"):
            if line.lstrip().startswith("#") or "summon" not in line:
                out.append(line)
                continue
            new = tag_nbt(line, fam, ids)
            if new != line:
                total_tagged += 1
            out.append(new)
            m = ROLL.search(line)
            if m and m.group(1) not in rolls:
                rolls.append(m.group(1))

        # 掷点命中变种 -> 原本那只让位。图鉴写的就是"直接替换"。
        if rolls:
            out.append("")
            out.append("# 命中变种的掷点，原本那只让位 —— 图鉴写的是"
                       "「直接替换成强化变种」，")
            out.append("# 而这里原本只是追加。不杀掉的话，一次生成会留下两只。")
            for r in rolls:
                out.append("execute if score @s random matches %s run kill @s" % r)
                total_killed += 1
        io.open(p, "w", encoding="utf-8", newline="\n").write("\n".join(out))

    print("cascade: %d summon(s) marked as already-processed, "
          "%d replace-the-original line(s)" % (total_tagged, total_killed))


if __name__ == "__main__":
    main()
