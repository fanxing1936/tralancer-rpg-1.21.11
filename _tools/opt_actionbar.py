# -*- coding: utf-8 -*-
"""把所有直接写 actionbar 的地方收回统一 HUD。

驱魔那一版立过一条规矩：**屏幕下方那条 actionbar 全局只有一个出口**，
因为它只有一行，谁最后写谁赢。当时把利维坦、熔火之锤、藤蔓之鞭三处收了进去。

之后加的东西没守这条规矩 —— 契约、佣兵、人偶、天启星、仪式、空缺者……
一共几十处又开始各写各的。于是每刻都在渲染的进度条和这些一次性提示互相盖：
提示刚闪出来就被下一刻的魔化条冲掉，或者反过来把条冲掉。

这一趟不是手工改那几十处，而是**扫描 + 改写**：找出所有
`title <选择器> actionbar <文本>`，去重编号，把调用点换成"往消息槽里写一个号"，
再由 HUD 按优先级渲染。以后新加的提示只要还是这个写法，下一次构建就会被一起收编。

优先级：一次性提示（2 秒） > 蓄力条 > 状态条。
提示活着的时候压住所有条；它一过期，条自己就回来了。
"""

import io
import os
import re
import sys

import add_exorcism as ex

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data/rpg/function")

TTL = 40                      # 一次性提示活多久（刻）

# HUD 自己那几个文件当然要跳过 —— 它们**就是**那个出口
SKIP = ("hud/",)

BARE = re.compile(r"^title (@\S+) actionbar (.+)$")
RUN = re.compile(r"^(execute .+?) run title (@\S+) actionbar (.+)$")


def walk():
    for root, dirs, files in os.walk(FUNC):
        dirs.sort()
        for f in sorted(files):
            if f.endswith(".mcfunction"):
                p = os.path.join(root, f)
                rel = os.path.relpath(p, FUNC).replace(os.sep, "/")
                if not rel.startswith(SKIP):
                    yield rel, p


def main():
    msgs = {}                 # 文本 -> 编号
    order = []
    edits = 0
    files = 0

    for rel, p in walk():
        src = io.open(p, encoding="utf-8").read().split("\n")
        out, touched = [], False
        for line in src:
            body = line.strip()
            if body.startswith("#") or not body:
                out.append(line)
                continue

            m = BARE.match(body)
            prefix = None
            if m:
                sel, comp = m.group(1), m.group(2)
            else:
                m = RUN.match(body)
                if not m:
                    out.append(line)
                    continue
                prefix, sel, comp = m.group(1), m.group(2), m.group(3)

            comp = comp.strip()
            if comp not in msgs:
                msgs[comp] = len(order) + 1
                order.append(comp)
            n = msgs[comp]

            call = "function rpg:hud/m%d" % n
            if sel == "@s":
                new = (prefix + " run " + call) if prefix else call
            elif prefix:
                new = prefix + " as " + sel + " run " + call
            else:
                new = "execute as " + sel + " run " + call
            out.append(new)
            touched = True
            edits += 1

        if touched:
            io.open(p, "w", encoding="utf-8", newline="\n").write("\n".join(out))
            files += 1

    if not order:
        print("actionbar: nothing to route")
        return

    # 每条提示一个"往消息槽里写号"的入口
    for comp, n in sorted(msgs.items(), key=lambda kv: kv[1]):
        ex.wf("hud/m%d.mcfunction" % n,
              "# 往消息槽里写一个号，真正的渲染在 rpg:hud/msg。\n"
              "# 直接写 actionbar 会和每刻渲染的进度条互相盖 —— 这条 actionbar\n"
              "# 全局只有一行，所以全包只留一个出口。\n"
              "scoreboard players set @s rpg_hud_m %d\n"
              "scoreboard players set @s rpg_hud_mt %d" % (n, TTL))

    body = ["# 一次性提示的渲染。按号分支 —— 与进度条走同一个出口，所以两者不会互相盖。"]
    for comp, n in sorted(msgs.items(), key=lambda kv: kv[1]):
        body.append("execute if entity @s[scores={rpg_hud_m=%d}] run title @s actionbar %s"
                    % (n, comp))
    ex.wf("hud/msg.mcfunction", "\n".join(body))

    ex.wf("hud/msg_tick.mcfunction",
          "# 提示每刻掉一格寿命，掉完条自己就回来了。\n"
          "scoreboard players remove @s rpg_hud_mt 1\n"
          "function rpg:hud/msg")

    # 调度层：提示压过一切，并且所有条都要让位
    p = os.path.join(FUNC, "hud/hud.mcfunction")
    s = io.open(p, encoding="utf-8").read()
    if "rpg_hud_mt" not in s:
        s = s.replace(
            "scoreboard players add @s rpg_hud_t 0",
            "scoreboard players add @s rpg_hud_t 0\n"
            "scoreboard players add @s rpg_hud_mt 0\n"
            "\n"
            "# 一次性提示压过所有条，只活 %d 刻；它一过期，条自己就回来。\n"
            "execute if entity @s[scores={rpg_hud_mt=1..}] run function rpg:hud/msg_tick"
            % TTL)
        # 每一条**渲染**分支都加上"没有提示占着"这个前提。
        # 只改跳去渲染函数的那些行 —— 末尾那条寿命递减必须照常跑，
        # 否则提示占着的两秒里蓄力条不老化，提示一散就残留一条过期的条。
        s = re.sub(r"(scores=\{)(rpg_hud_t=[^\]]*\] run function rpg:hud/)",
                   r"\1rpg_hud_mt=..0,\2", s)
        io.open(p, "w", encoding="utf-8", newline="\n").write(s)

    # 两个新记分项
    q = os.path.join(FUNC, "command/soreboard.mcfunction")
    t = io.open(q, encoding="utf-8").read()
    add = [o for o in ("rpg_hud_m", "rpg_hud_mt") if o not in t]
    if add:
        io.open(q, "w", encoding="utf-8", newline="\n").write(
            t.rstrip("\n") + "\n"
            + "\n".join("scoreboard objectives add %s dummy" % o for o in add) + "\n")

    print("actionbar: %d call site(s) in %d file(s) routed through the HUD, "
          "%d distinct message(s)" % (edits, files, len(order)))


if __name__ == "__main__":
    main()
