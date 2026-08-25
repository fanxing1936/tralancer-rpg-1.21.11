# -*- coding: utf-8 -*-
"""构建期检查：攻击瞬爆必须是无地形破坏的伪爆炸。

自然苦力怕变种已由 ``drop_creeper_variants.py`` 删除；其余旧 ``Fuse:0``
召唤都应由 ``instant_boom.py`` 变成粒子、声音与 command damage。这里同时
阻止旧苦力怕写法和 ``fuse:0``/``explosion_power`` TNT 回流。普通非零引信
TNT、TNT 矿车与玩家放置方块不在检查范围内。
"""
import io
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(ROOT, "data/rpg/function")

SUMMON_CREEPER = re.compile(r"summon\s+(?:minecraft:)?creeper\b[^\n]*")
INSTANT_TNT = re.compile(
    r"summon\s+(?:minecraft:)?tnt\b[^\n]*fuse\s*:\s*0(?:s|b|S|B)?\b")


def main():
    bad = []
    for base, _d, files in os.walk(FUNC):
        for f in files:
            if not f.endswith(".mcfunction"):
                continue
            p = os.path.join(base, f)
            rel = os.path.relpath(p, FUNC).replace("\\", "/")
            for i, line in enumerate(io.open(p, encoding="utf-8"), 1):
                if SUMMON_CREEPER.search(line):
                    bad.append("%s:%d legacy creeper" % (rel, i))
                if INSTANT_TNT.search(line):
                    bad.append("%s:%d terrain-breaking instant TNT" % (rel, i))

    if bad:
        print("pseudo boom check: %d 处仍会生成真实爆炸实体" % len(bad))
        for b in bad:
            print("  " + b)
        return 1
    fx = os.path.join(FUNC, "effect/pseudo_explosion/p4.mcfunction")
    if not os.path.isfile(fx):
        print("pseudo boom check: 缺少伪爆炸函数")
        return 1
    body = io.open(fx, encoding="utf-8").read()
    if ("damage @s" not in body or "explosion_emitter" not in body or
            re.search(r"\b(?:setblock|fill|summon\s+(?:minecraft:)?(?:tnt|creeper))\b",
                      body)):
        print("pseudo boom check: 伪爆炸函数缺少伤害/表现或会修改世界")
        return 1
    print("pseudo boom check: 全部攻击瞬爆无爆炸实体、无地形破坏")
    return 0


if __name__ == "__main__":
    sys.exit(main())
