# -*- coding: utf-8 -*-
"""友军单位接入（docs/JACQUES-ALLY.md §3）：构建末尾的一道改写，让敌方技能像对待玩家一样对待友军。

    python add_ally_units.py ../rpg [--report]

友军（目前只有友军雅克，带 rpg.ally）每刻带着四个「单位」标签；玩家的这四个标签由 rpg:jacques_ally/units
在每刻最开头刷新（rpg.unit 全部玩家；.ns 非旁观；.nc 非创造；.f 非旁观非创造）。

1. 敌方模块（HOSTILE：各 Boss、领主、罪仆、仆从、圣卫、恶魔降临的技能层 taint ……）里，凡是选玩家的
   @a / @p / @r 改写成 @e[tag=<单位标签>,...]：
     @a[gamemode=!spectator,gamemode=!creative,...] → @e[tag=rpg.unit.f,...]（只去掉这两种否定的游戏模式条件）
     @p → 加 sort=nearest,limit=1；@r → 加 sort=random,limit=1；@p / @r 不带游戏模式条件时用 .ns（它们本来就不选旁观者）
   只给玩家用的命令参数不改（tellraw、title、playsound 的听众、particle 的观众、bossbar 的 players、
   give、clear、xp、advancement、item/loot 对玩家物品栏 ……），文字组件里的选择器也不改。
   这样选目标、范围伤害、打标签、计分都会把友军算进去，播报、音效、血条仍只给玩家。
2. 其余模块（玩家的武器、契约、驱魔、符文 ……）里「不点名的范围选择」——@e[...] 没有正向 type、tag、
   scores、name 条件的——加上 tag=!rpg.ally：玩家的范围技能和投射物不会打到友军。

改写只在构建末尾跑一遍（build.sh 每次从 _orig 重建 rpg/），所以不需要幂等标记。
"""

import io
import os
import re
import sys

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
REPORT = "--report" in sys.argv
FUNC = os.path.join(DP, "data", "rpg", "function")

HOSTILE = {
    "abaddon", "arch_visage", "beelzebub", "belial_lord", "belial_servant", "end_illager", "entities",
    "heart_of_ender", "jacques_boss", "leviathan", "lucifer_boss", "lucifer_fight", "lucifer_lord", "lucifer_p2",
    "lucifer_servant", "lucifer_vine", "mammon", "mammon_lord", "mammon_servant", "minion", "pope_fight",
    "prime_enchanter", "royal_guard", "samael_lord", "samael_servant", "sunken_skeleton", "taint", "tower_guard",
    "tower_wraith", "usurper_boss", "vanguard", "vacant", "holy_guard", "saul_boss", "michael_boss",
}
# 友军自己的函数、外观与动画：两道都不碰
SKIP = {"jacques_ally", "jacques", "david", "pope", "usurper", "saul", "saul_ghost", "michael", "watchling"}
# 无主的伪爆炸（传说怪物的攻击瞬爆）照样炸到友军，像炸到玩家一样；带射手的（玩家旧弓）才避开友军
NO_GUARD = re.compile(r"effect[\\/]pseudo_explosion[\\/]p\d")

# 选择器前一个词是这些时，参数是「给玩家看/听/拿」的，不改
PLAYER_ONLY_PREV = {"tellraw", "title", "give", "clear", "xp", "msg", "tell", "w", "teammsg", "spawnpoint",
                    "gamemode", "stopsound", "players", "show", "spectate", "join", "leave", "recipe"}
SOUND_CATEGORIES = {"master", "music", "record", "weather", "block", "hostile", "neutral", "player", "ambient",
                    "voice", "ui"}
UNIT = {(): "rpg.unit", ("spectator",): "rpg.unit.ns", ("creative",): "rpg.unit.nc",
        ("creative", "spectator"): "rpg.unit.f"}

SEL = re.compile(r"@([apre])(?![A-Za-z0-9_])")


def match_bracket(text, i):
    """text[i] == '['; return the index just past the matching ']' (quotes and nested {} [] respected)."""
    depth, quote, j = 0, None, i
    while j < len(text):
        ch = text[j]
        if quote:
            if ch == "\\":
                j += 2
                continue
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
            if depth == 0:
                return j + 1
        j += 1
    return -1


def split_args(body):
    out, depth, quote, cur = [], 0, None, ""
    for ch in body:
        if quote:
            cur += ch
            if ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote = ch
        elif ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
        if ch == "," and depth == 0:
            out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur.strip())
    return out


def in_quotes(line, i):
    """Is position i inside a JSON/SNBT string (a selector inside a text component)?"""
    quote = None
    k = 0
    while k < i:
        ch = line[k]
        if quote:
            if ch == "\\":
                k += 2
                continue
            if ch == quote:
                quote = None
        elif ch == '"':
            quote = ch
        k += 1
    return quote is not None


def player_only(line, i):
    before = line[:i].rstrip().split()
    if not before:
        return False
    prev = before[-1]
    if prev in PLAYER_ONLY_PREV:
        return True
    if prev in SOUND_CATEGORIES and "playsound" in before:
        return True
    if prev in ("force", "normal") and "particle" in before:
        return True
    if prev in ("grant", "revoke") and "advancement" in before:
        return True
    if prev in ("add", "set", "query") and len(before) >= 2 and before[-2] in ("xp", "experience"):
        return True
    if prev == "entity" and any(b in ("item", "loot") for b in before):
        return True                             # item replace / item modify / loot replace on a player's slots
    return False


def rewrite_hostile(line, stats):
    if line.lstrip().startswith("#"):
        return line
    out, pos = [], 0
    for m in SEL.finditer(line):
        kind = m.group(1)
        if kind == "e" or m.start() < pos:
            continue
        start = m.start()
        end = m.end()
        args = []
        if end < len(line) and line[end] == "[":
            close = match_bracket(line, end)
            if close < 0:
                continue
            args = split_args(line[end + 1:close - 1])
            end = close
        if start > 0 and not line[start - 1].isspace():
            continue                            # inside a text component / not a command argument
        if in_quotes(line, start) or player_only(line, start):
            stats["kept"] += 1
            continue
        gm = sorted(a.split("=!", 1)[1] for a in args if a.replace(" ", "") in ("gamemode=!spectator", "gamemode=!creative"))
        rest = [a for a in args if a.replace(" ", "") not in ("gamemode=!spectator", "gamemode=!creative")]
        if any(a.replace(" ", "").startswith("gamemode=") for a in rest):
            stats["kept"] += 1
            continue                            # some other game-mode test: leave it a player selector
        if kind in "pr" and not gm:
            gm = ["spectator"]
        tag = UNIT[tuple(gm)]
        keys = {a.split("=", 1)[0].strip() for a in rest}
        if kind == "p" and "sort" not in keys:
            rest.append("sort=nearest")
        if kind == "r" and "sort" not in keys:
            rest.append("sort=random")
        if kind in "pr" and "limit" not in keys:
            rest.append("limit=1")
        out.append(line[pos:start])
        out.append("@e[" + ",".join(["tag=" + tag] + rest) + "]")
        pos = end
        stats["rewritten"] += 1
    out.append(line[pos:])
    return "".join(out)


def rewrite_friendly(line, stats):
    if line.lstrip().startswith("#") or "@e[" not in line:
        return line
    out, pos = [], 0
    for m in re.finditer(r"@e\[", line):
        if m.start() < pos:
            continue
        close = match_bracket(line, m.end() - 1)
        if close < 0:
            continue
        args = split_args(line[m.end():close - 1])
        named = False
        for a in args:
            k, _, v = a.partition("=")
            k, v = k.strip(), v.strip()
            if k in ("type", "tag", "name") and v and not v.startswith("!"):
                named = True
            if k in ("scores", "predicate") and not v.startswith("!"):
                named = True
        if named or not args or "tag=!rpg.ally" in args or in_quotes(line, m.start()):
            continue
        out.append(line[pos:m.end()])
        out.append(",".join(args + ["tag=!rpg.ally"]) + "]")
        pos = close
        stats["guarded"] += 1
    out.append(line[pos:])
    return "".join(out)


def main():
    stats = {"rewritten": 0, "kept": 0, "guarded": 0, "files": 0}
    for top in sorted(os.listdir(FUNC)):
        path = os.path.join(FUNC, top)
        mod = top[:-len(".mcfunction")] if top.endswith(".mcfunction") else top
        if mod in SKIP:
            continue
        hostile = mod in HOSTILE
        files = [path] if os.path.isfile(path) else [os.path.join(r, f) for r, _, fs in os.walk(path) for f in fs]
        for f in files:
            if not f.endswith(".mcfunction"):
                continue
            with io.open(f, encoding="utf-8") as fh:
                text = fh.read()
            if not hostile and NO_GUARD.search(f):
                continue
            fn = rewrite_hostile if hostile else rewrite_friendly
            new = "\n".join(fn(line, stats) for line in text.split("\n"))
            if new != text:
                stats["files"] += 1
                with io.open(f, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(new)
                if REPORT:
                    print(os.path.relpath(f, FUNC))
    print("ally units: %(rewritten)d player selectors now take allies, %(kept)d kept player-only, "
          "%(guarded)d broad selectors spare allies, %(files)d files" % stats)


if __name__ == "__main__":
    main()
