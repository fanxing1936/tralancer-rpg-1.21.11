# -*- coding: utf-8 -*-
"""构建末端的特效收口（docs/VFX-SPEC.md）。

和 polish_ui 处理文字颜色一样：前面二十来个生成器各自写粒子，这里按
rpg_vfx 的分级表统一收口，生成器不必各自记住上限。

* force 只留给预警和大招；其余一律 normal。
* 数量、速度、dust 尺寸收进各档上限（只降不升）。
* 旧的柱色／深色闪光折回柱亮色。

作者的武器特效（item/**）只执行 force 规则，外加七柱旧色闪光折回亮色（ART-STYLE §6、
审计 S2-4 的 #B00057／#660099）。展示实体生物与死代码不动。
重复运行结果不变。
"""

import io
import os
import re
import sys
from collections import Counter

import rpg_vfx as vfx

DP = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "../rpg")
FUNC = os.path.join(DP, "data", "rpg", "function")
FLASH = re.compile(r"flash\{color:(\d+)\}")


def polish_line(rel, line, zone, stats):
    if "particle " not in line:
        return line
    tier = vfx.line_tier(rel, line)
    line, notes = vfx.conform(line, tier, force_only=(zone == "force_only"))
    for n in notes:
        stats[n.split()[0]] += 1
    if zone in ("full", "force_only"):
        def fold(m):
            new = vfx.fold_flash(int(m.group(1)))
            if new is None:
                return m.group(0)
            stats["flash"] += 1
            return "flash{color:%d}" % new
        line = FLASH.sub(fold, line)
    return line


def main():
    stats = Counter()
    touched = 0
    for dp, _, files in os.walk(FUNC):
        for f in sorted(files):
            if not f.endswith(".mcfunction"):
                continue
            path = os.path.join(dp, f)
            rel = os.path.relpath(path, FUNC).replace(os.sep, "/")[:-len(".mcfunction")]
            zone = vfx.zone(rel)
            if zone is None:
                continue
            with io.open(path, encoding="utf-8") as fh:
                text = fh.read()
            out = "\n".join(polish_line(rel, l, zone, stats) for l in text.split("\n"))
            if out != text:
                touched += 1
                with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(out)
    print("特效收口：%d 个函数；force→normal %d，数量 %d，速度 %d，尺寸 %d，闪光折色 %d" % (
        touched, stats["force"], stats["count"], stats["speed"], stats["scale"], stats["flash"]))


if __name__ == "__main__":
    main()
