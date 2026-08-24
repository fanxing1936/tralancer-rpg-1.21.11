# -*- coding: utf-8 -*-
"""攻击用的爆炸改成真正瞬发：苦力怕换成引信为零的 TNT。

作者要的是「立刻爆炸」。`ignited:1b` 做不到 —— 它只是**点燃引信**，
苦力怕照样要鼓 1.5 秒才炸，这期间它还会朝人走两步。实测同一刻去数，
点了火的苦力怕还站在那里。

而 `summon minecraft:tnt {fuse:0s}` 是**同刻就没了**（实测：召唤之后
同一刻计数已经是 0）。TNT 的 `fuse` 与 `explosion_power` 两个字段在
1.21.11 都还在（实测读回 186s / 5.0f），所以威力也能一一对上原来的
`ExplosionRadius`。

对应关系：ExplosionRadius:N  ->  explosion_power:Nf，默认 4（原版 TNT 的威力）。

这一步跑在变种体系删除之后：那时包里剩下的苦力怕召唤**全部**是武器
或技能效果，没有一只是世界里该走动的。
"""
import io
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(ROOT, "data/rpg/function")

# summon minecraft:creeper <坐标> {……}
CALL = re.compile(
    r"summon\s+(?:minecraft:)?creeper\s+(?P<pos>\S+\s+\S+\s+\S+)\s*"
    r"\{(?P<nbt>[^{}]*(?:\{[^{}]*\}[^{}]*)*)\}")
RADIUS = re.compile(r'"?ExplosionRadius"?\s*:\s*([0-9.]+)')


def convert(m):
    nbt = m.group("nbt")
    r = RADIUS.search(nbt)
    power = r.group(1) if r else "4"
    if "." not in power:
        power += ".0"
    # Silent 留着：TNT 本来也不出声，但保住作者的原意不丢
    silent = ",Silent:1b" if "Silent:1b" in nbt else ""
    return ("summon minecraft:tnt %s {fuse:0s,explosion_power:%sf%s}"
            % (m.group("pos"), power, silent))


def main():
    hit, files = 0, 0
    for base, _d, names in os.walk(FUNC):
        for f in names:
            if not f.endswith(".mcfunction"):
                continue
            p = os.path.join(base, f)
            s = io.open(p, encoding="utf-8").read()
            t, n = CALL.subn(convert, s)
            if n:
                io.open(p, "w", encoding="utf-8", newline="\n").write(t)
                hit += n
                files += 1
    print("instant boom: %d 处苦力怕改成 fuse:0 的 TNT（%d 个文件）" % (hit, files))


if __name__ == "__main__":
    main()
