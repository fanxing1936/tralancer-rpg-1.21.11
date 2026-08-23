# -*- coding: utf-8 -*-
"""把与 @s 无关的存在性判定从循环里提出来。

`entities/warden/warden` 开头两行长这样：

    execute as @e on attacker if entity @e[tag=devil] at @s run effect clear ...

`as @e` 是**世界上每一个实体**；对其中每一个，`if entity @e[tag=devil]` 又要
**再走一遍全表**。这是 O(n²) —— 83 个实体就是约 6900 次选择器求值，两行一万四。
而那个判定问的是"世界上有没有恶魔"，**与当前是哪个实体毫无关系**，
每一轮的答案都一样。

提到循环外面就是 O(n)；而在没有 Boss 的常态下（也就是绝大多数时间）
它直接变成 O(1) —— 一次判定落空，整段跳过。

安全条件：内层选择器**不能**带任何与位置或排序相关的过滤
（`distance` / `dx` / `sort` / `limit` / 坐标），否则它的答案就依赖执行上下文，
提出去会改变语义。带这些的一律不动。

`opt_guard` 没有抓到这两行，是因为它找的是**行首**就能守卫的形状，
而这里的判定夹在 `as @e` 和 `at @s` 中间。
"""

import io
import os
import re
import sys

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data/rpg/function")

# 依赖执行上下文的过滤 —— 出现任何一个就不能外提
POSITIONAL = ("distance=", "dx=", "dy=", "dz=", "sort=", "limit=",
              "x=", "y=", "z=")

LINE = re.compile(r"^(execute as @e(?:\[[^\]]*\])?\b.*?)"
                  r"(\bif entity (@e\[[^\]]*\])\s)"
                  r"(.*)$")


def hoistable(line):
    m = LINE.match(line.strip())
    if not m:
        return None
    inner = m.group(3)
    if any(k in inner for k in POSITIONAL):
        return None
    return inner, (m.group(1) + m.group(4)).strip()


def main():
    made = hoisted = 0
    for root, dirs, files in os.walk(FUNC):
        dirs.sort()
        for f in sorted(files):
            if not f.endswith(".mcfunction"):
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, FUNC).replace(os.sep, "/")[:-len(".mcfunction")]
            src = io.open(p, encoding="utf-8").read().split("\n")

            out, i, n = [], 0, 0
            while i < len(src):
                got = None if src[i].lstrip().startswith("#") else hoistable(src[i])
                if not got:
                    out.append(src[i])
                    i += 1
                    continue
                inner, _ = got
                body = []
                while i < len(src):
                    g = None if src[i].lstrip().startswith("#") else hoistable(src[i])
                    if not g or g[0] != inner:
                        break
                    body.append(g[1])
                    i += 1

                n += 1
                sub = "%s/h%d" % (rel, n)
                io_p = os.path.join(FUNC, sub + ".mcfunction")
                d = os.path.dirname(io_p)
                if not os.path.isdir(d):
                    os.makedirs(d)
                head = ("# 这 %d 行原本各自在 `as @e` 的循环里再问一遍 "
                        "`if entity %s` —— 那是 O(n²)，\n"
                        "# 而那个判定与当前是哪个实体无关。现在由上层一次判定后统一进入。\n"
                        "# 行内容与顺序原样保留。" % (len(body), inner))
                io.open(io_p, "w", encoding="utf-8", newline="\n").write(
                    head + "\n" + "\n".join(body) + "\n")
                # limit=1：存在性判定，找到一个就够
                guard = inner[:-1] + (",limit=1]" if inner[-2] != "[" else "limit=1]")
                out.append("execute if entity %s run function rpg:%s" % (guard, sub))
                made += 1
                hoisted += len(body)

            if n:
                io.open(p, "w", encoding="utf-8", newline="\n").write("\n".join(out))

    print("hoist: %d guard(s) lifted out of per-entity loops, covering %d line(s)"
          % (made, hoisted))


if __name__ == "__main__":
    main()
