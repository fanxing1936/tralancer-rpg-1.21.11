# -*- coding: utf-8 -*-
"""特效预算审计（docs/VFX-SPEC.md §5）。

失败条件（受规范约束的目录里）：
* 单条命令超出所在档位的数量／速度／尺寸上限；
* 非预警、非大招的命令用了 force（item/** 也算）；
* 每刻常驻的函数，无条件的那几条加起来超过每实体预算；
* 罪约、罪域等柱色闪光用了深色。

只警告：散布超过档位上限；单个函数的粒子总量超过建议值；全场常驻合计超过建议值。
"""

import io
import os
import re
import sys

import rpg_ui_style as ui
import rpg_vfx as vfx

DP = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "../rpg")
FUNC = os.path.join(DP, "data", "rpg", "function")
GATED = re.compile(r"^execute .*\b(if|unless) ")
# 按计时分段的门：同一个函数在不同刻数画的东西不会同时出现
PHASE = re.compile(r"\bif score @s (\S+) matches (-?\d+)(?!\.)\b")
DEEP_FLASH = {int(p["deep"].lstrip("#"), 16) for p in ui.PILLARS}


def count_of(args):
    return int(args[7]) if len(args) >= 8 and args[7].isdigit() else 1


def main():
    problems, warnings = [], []
    ambient_total = 0
    files = lines_seen = 0
    for dp, _, names in os.walk(FUNC):
        for f in sorted(names):
            if not f.endswith(".mcfunction"):
                continue
            path = os.path.join(dp, f)
            rel = os.path.relpath(path, FUNC).replace(os.sep, "/")[:-len(".mcfunction")]
            zone = vfx.zone(rel)
            if zone is None:
                continue
            total = steady = 0
            phases = {}
            for n, line in enumerate(io.open(path, encoding="utf-8").read().split("\n"), 1):
                parts = vfx.split(line)
                if parts is None:
                    continue
                lines_seen += 1
                _, name, args = parts
                tier = vfx.line_tier(rel, line)
                cap = vfx.TIERS[tier]
                where = "%s:%d [%s]" % (rel, n, tier)
                if len(args) >= 9 and args[8] == "force" and not cap["force"]:
                    problems.append("%s force 只留给预警和大招: %s" % (where, line.strip()[:120]))
                if zone == "force_only":
                    continue
                c = count_of(args)
                ph = PHASE.search(line)
                if ph:
                    phases[ph.groups()] = phases.get(ph.groups(), 0) + c
                else:
                    total += c
                if not GATED.search(line):
                    steady += c
                if c > cap["count"]:
                    problems.append("%s 数量 %d > %d" % (where, c, cap["count"]))
                if len(args) >= 7 and vfx._short(name) not in vfx.SPEED_EXEMPT:
                    try:
                        if float(args[6]) > cap["speed"] + 1e-9:
                            problems.append("%s 速度 %s > %s" % (where, args[6], cap["speed"]))
                    except ValueError:
                        pass
                try:
                    spread = max(abs(float(x)) for x in args[3:6])
                except (ValueError, IndexError):
                    spread = 0
                if spread > cap["spread"] + 1e-9:
                    warnings.append("%s 散布 %s > %s（用边界圈表达范围）" % (where, spread, cap["spread"]))
                sm = re.search(r"scale:([\d.]+)", name)
                if sm and float(sm.group(1)) > cap["scale"] + 1e-9:
                    problems.append("%s 尺寸 %s > %s" % (where, sm.group(1), cap["scale"]))
                fm = re.search(r"flash\{color:(\d+)\}", name)
                if fm and int(fm.group(1)) in DEEP_FLASH:
                    problems.append("%s 闪光用了柱深色，应取亮色" % where)
            files += 1
            total += max(phases.values()) if phases else 0
            tier = vfx.tier_of(rel)
            if tier == "ambient":
                ambient_total += steady
                if steady > vfx.AMBIENT_PER_ENTITY:
                    problems.append("%s 每刻常驻 %d > 每实体预算 %d" % (rel, steady, vfx.AMBIENT_PER_ENTITY))
            limit = vfx.EVENT_TOTAL.get(tier)
            if limit and total > limit:
                warnings.append("%s [%s] 单次合计 %d > 建议 %d" % (rel, tier, total, limit))
    if ambient_total > vfx.AMBIENT_TOTAL:
        warnings.append("全场常驻（每类实体各一只）合计 %d > 建议 %d" % (ambient_total, vfx.AMBIENT_TOTAL))

    print("特效预算：%d 个函数、%d 条粒子命令受规范约束；常驻每刻合计 %d（每类一只）" % (
        files, lines_seen, ambient_total))
    for w in warnings:
        print("  [警告] " + w)
    if problems:
        for p in problems[:60]:
            print("  [违规] " + p)
        print("特效预算审计失败：%d 处" % len(problems))
        sys.exit(1)
    print("特效预算审计通过（%d 条警告）" % len(warnings))


if __name__ == "__main__":
    main()
