# -*- coding: utf-8 -*-
"""序章多开（用户 2026-11-28：「序章改一改，和达阿特试炼一样，可以好多组同时打序章，开局新手过场结束后直接进入序章，
四人直接分配一组，序章结束再正式游戏」）。

    python prologue_multi.py ../rpg

序章（rpg:prologue）和它借用的米迦勒战（rpg:michael_boss）都是按「同一时间只有一场」写的：坐标是绝对的，状态在全局假玩家上。
所以这里不改写它们，而是在构建的最后，把两棵函数树各复制 N 份，每份一个独立的维度（rpg:armageddon、rpg:armageddon_2 ……），
坐标原样不动；复制时按命令语法改名：
  · 函数、进度、谓词、函数标签：rpg:prologue/ → rpg:prologue_iK/，rpg:michael_boss/ → rpg:michael_boss_iK/
  · 有状态的计分项 rpg_pr、rpg_mk，存储 rpg:pr、rpg:michael_boss，血条 rpg:prologue_zh/en、rpg:michael_boss → 加 _iK
  · 维度 rpg:armageddon → 第 K 个维度
  · 玩家标签 rpg.pr → rpg.priK（同时保留 rpg.pr，别的模块靠它豁免魔化、HUD 等）；rpg.pr.join → rpg.pr.joinK
  · 选实体的选择器补上 distance=0..（只选执行维度里的实体，2026-11-28 在服务器上验证过），所以各份互不干扰
原版的米迦勒战（主世界里召唤的那场）不复制，它的选择器补上 predicate=!rpg:in_prologue，碰不到序章维度里的东西。

原来的 rpg:prologue 树复制完就删掉，同一路径下写一个「调度」：入队、四人一组分配空闲的战场、掉线重连、管理员的开始与中止。
"""
import io
import json
import os
import re
import shutil
import sys

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
DATA = os.path.join(DP, "data", "rpg")
FUNC = os.path.join(DATA, "function")
N = 4
DIMS = {k: "rpg:armageddon" if k == 1 else "rpg:armageddon_%d" % k for k in range(1, N + 1)}
HUB = "# prologue_multi hub"
H = "rpg_prh"                 # 调度自己的假玩家
TREES = ("prologue", "michael_boss")
REGS = ("function", "advancement", "predicate")
BARS = ("rpg:prologue_zh", "rpg:prologue_en", "rpg:michael_boss")
STORES = ("rpg:pr", "rpg:michael_boss")
OBJS = ("rpg_pr", "rpg_mk")
POSITIONAL = re.compile(r"(?:^|,)\s*(?:distance|dx|dy|dz|x|y|z)\s*=")
COUNT = [0]
# 资源 ID：复制时不许动
RES = (r'item_model"?\s*[:=]\s*"rpg:[^"]+"', r'"font"\s*:\s*"[^"]+"', r"rpg:bgm\.[\w.]+", r'"translate"\s*:\s*"[^"]+"', r"rpg:armageddon/[\w/]+", r"rpg:vo\.[\w.]+")


def P(k):
    return "rpg:prologue_i%d" % k


def ptag(k):
    return "rpg.pri%d" % k


# ---------------------------------------------------------------------------- 选择器
def selectors(s, fix):
    """把文本里每个 @x / @x[...] 交给 fix(kind, body or None) 改写；body 不含方括号。"""
    out, i, n = [], 0, len(s)
    while i < n:
        c = s[i]
        if c == "@" and i + 1 < n and s[i + 1] in "aeprns" and (i + 2 >= n or not (s[i + 2].isalnum() or s[i + 2] == "_")):
            kind = s[i + 1]
            j = i + 2
            if j < n and s[j] == "[":
                depth, k, q = 0, j, None
                while k < n:
                    ch = s[k]
                    if q:
                        if ch == "\\":
                            k += 1
                        elif ch == q:
                            q = None
                    elif ch in "\"'":
                        q = ch
                    elif ch in "[{":
                        depth += 1
                    elif ch in "]}":
                        depth -= 1
                        if depth == 0:
                            break
                    k += 1
                body = s[j + 1:k]
                out.append(fix(kind, body))
                i = k + 1
            else:
                out.append(fix(kind, None))
                i = j
            continue
        out.append(c)
        i += 1
    return "".join(out)


def top_args(body):
    """选择器参数里顶层的部分（去掉 {...} 与 [...] 里的内容），用来判断有没有位置参数。"""
    res, depth, q = [], 0, None
    for ch in body:
        if q:
            if ch == q:
                q = None
            continue
        if ch in "\"'":
            q = ch
            continue
        if ch in "{[":
            depth += 1
        elif ch in "}]":
            depth -= 1
        elif depth == 0:
            res.append(ch)
    return "".join(res)


def sel(kind, body, extra):
    return "@%s[%s]" % (kind, extra if not body else body + "," + extra)


def fix_copy(k):
    pt = ptag(k)

    def fix(kind, body):
        if kind == "s":
            return "@s" if body is None else "@s[%s]" % body
        top = top_args(body or "")
        if POSITIONAL.search(top):
            return "@%s[%s]" % (kind, body)
        if re.search(r"tag=!?(?:%s|rpg\.pr\.join%d)(?=[,\]]|$)" % (re.escape(pt), k), top):
            return "@%s[%s]" % (kind, body)
        return sel(kind, body, "distance=0..")
    return fix


def fix_orig(kind, body):
    if kind == "s":
        return "@s" if body is None else "@s[%s]" % body
    top = top_args(body or "")
    if POSITIONAL.search(top) or "rpg:in_prologue" in top:
        return "@%s[%s]" % (kind, body)
    return sel(kind, body, "predicate=!rpg:in_prologue")


# ---------------------------------------------------------------------------- 改名
def rename(s, k, is_json=False):
    i = "_i%d" % k
    # 函数（含 schedule、函数标签、宏行）
    s = re.sub(r"(function\s+#?)rpg:(prologue|michael_boss)/", lambda m: "%srpg:%s%s/" % (m.group(1), m.group(2), i), s)
    # 进度
    s = re.sub(r"(advancement\s+\w+\s+\S+\s+\w+\s+)rpg:(prologue|michael_boss)/", lambda m: "%srpg:%s%s/" % (m.group(1), m.group(2), i), s)
    # 谓词
    s = re.sub(r"(predicate=!?|predicate\s+)rpg:(prologue|michael_boss)/", lambda m: "%srpg:%s%s/" % (m.group(1), m.group(2), i), s)
    if is_json:
        s = re.sub(r'("function"\s*:\s*")rpg:(prologue|michael_boss)/', lambda m: '%srpg:%s%s/' % (m.group(1), m.group(2), i), s)
        s = re.sub(r'"(#?)rpg:(prologue|michael_boss)/', lambda m: '"%srpg:%s%s/' % (m.group(1), m.group(2), i), s)
    # 血条
    for b in BARS:
        s = re.sub(r"(bossbar\s+(?:add|set|remove|get)\s+)%s(?![\w/])" % re.escape(b), r"\g<1>%s%s" % (b, i), s)
        s = re.sub(r"(store\s+(?:result|success)\s+bossbar\s+)%s(?![\w/])" % re.escape(b), r"\g<1>%s%s" % (b, i), s)
    # 存储
    for st in STORES:
        s = re.sub(r"(storage\s+)%s(?![\w/:.])" % re.escape(st), r"\g<1>%s%s" % (st, i), s)
    # 计分项
    for o in OBJS:
        s = re.sub(r"(?<![\w.:#/-])%s(?![\w])" % o, o + i, s)
    # 维度
    s = re.sub(r"rpg:armageddon(?![\w/])", DIMS[k], s)
    # 标签
    s = re.sub(r"(?<![\w.])rpg\.pr\.join(?![\w.])", "rpg.pr.join%d" % k, s)
    s = re.sub(r"(tag=!?)rpg\.pr(?=[,\]])", r"\g<1>" + ptag(k), s)
    return s


def tag_lines(s, k):
    """tag … add/remove rpg.pr：两个标签一起加减。"""
    out = []
    for ln in s.split("\n"):
        out.append(ln)
        if re.search(r"\btag\s+\S+\s+(?:add|remove)\s+rpg\.pr\s*$", ln):
            out.append(re.sub(r"rpg\.pr\s*$", ptag(k), ln))
    return "\n".join(out)


# ---------------------------------------------------------------------------- 文件
def rd(p):
    return io.open(p, encoding="utf-8").read()


def wr(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(s)


def fn(name, lines):
    wr(os.path.join(FUNC, "prologue", name + ".mcfunction"), HUB + "\n" + "\n".join(lines) + "\n")
    COUNT[0] += 1


def walk(root):
    for r, _, fs in os.walk(root):
        for f in fs:
            yield os.path.join(r, f)


def clean():
    assert os.path.isfile(os.path.join(FUNC, "prologue", "flow", "cut1.mcfunction")), "prologue_multi: 先跑 add_prologue.py（原件不在）"
    for reg in REGS + ("tags/function",):
        base = os.path.join(DATA, *reg.split("/"))
        if not os.path.isdir(base):
            continue
        for d in os.listdir(base):
            if re.match(r"(prologue|michael_boss)_i\d+$", d):
                shutil.rmtree(os.path.join(base, d))
    # 上一次写的调度文件（这次 add_prologue 没有覆盖掉的）不能被当成原件复制
    for p in list(walk(os.path.join(FUNC, "prologue"))):
        if rd(p).startswith(HUB):
            os.remove(p)
    for k in range(2, N + 1):
        q = os.path.join(DATA, "dimension", "armageddon_%d.json" % k)
        if os.path.exists(q):
            os.remove(q)


def copy_trees():
    sched = {}
    for k in range(1, N + 1):
        i = "_i%d" % k
        for reg in REGS + ("tags/function",):
            for t in TREES:
                src = os.path.join(DATA, *reg.split("/"), t)
                if not os.path.isdir(src):
                    continue
                for p in walk(src):
                    rel = os.path.relpath(p, src)
                    dst = os.path.join(DATA, *reg.split("/"), t + i, rel)
                    s = rd(p)
                    if p.endswith(".mcfunction"):
                        before = s
                        # 原件上一次被 patch_original_michael 改过（没重新生成时）：复制品里不要那些
                        s = s.replace(",predicate=!rpg:in_prologue", "").replace("predicate=!rpg:in_prologue,", "").replace("[predicate=!rpg:in_prologue]", "")
                        s = "\n".join(l for l in s.split("\n") if not l.startswith("execute if entity @s[tag=rpg.pr] run return run advancement revoke"))
                        s = rename(s, k)
                        fx = fix_copy(k)
                        # 带 rpg.pr.joinK 的行是在主世界里挑人的，不限维度
                        s = "\n".join(l if "rpg.pr.join" in l else selectors(l, fx) for l in s.split("\n"))
                        s = tag_lines(s, k)
                        for pat in RES:
                            if sorted(re.findall(pat, before)) != sorted(re.findall(pat, s)):
                                raise SystemExit("prologue_multi: %s 的资源 ID 被改动了（%s）" % (p, pat))
                        for m in re.finditer(r"schedule function (rpg:\S+)", s):
                            sched.setdefault(k, set()).add(m.group(1))
                    else:
                        s = rename(s, k, is_json=True)
                    wr(dst, s)
        # 计划任务在主世界的上下文里跑：包一层 execute in
        for tgt in sorted(sched.get(k, ())):
            wrap = tgt.replace("rpg:prologue_i%d/" % k, "rpg:prologue_i%d/_sched/" % k).replace("rpg:michael_boss_i%d/" % k, "rpg:michael_boss_i%d/_sched/" % k)
            ns, path = wrap.split(":", 1)
            wr(os.path.join(FUNC, path + ".mcfunction"), "execute in %s run function %s\n" % (DIMS[k], tgt))
            for p in walk(os.path.join(FUNC, "prologue" + i)):
                s = rd(p)
                if "schedule function " + tgt in s:
                    wr(p, s.replace("schedule function " + tgt + " ", "schedule function " + wrap + " "))
        if k > 1:
            d = json.loads(rd(os.path.join(DATA, "dimension", "armageddon.json")))
            wr(os.path.join(DATA, "dimension", "armageddon_%d.json" % k), json.dumps(d, ensure_ascii=False, indent=1) + "\n")


def edit(path, f):
    p = os.path.join(FUNC, path + ".mcfunction")
    s = rd(p)
    s2 = f(s)
    assert s2 != s, "prologue_multi: %s 没改动" % path
    wr(p, s2)


def patch_copies():
    for k in range(1, N + 1):
        pi, mi, o, j = "prologue_i%d" % k, "michael_boss_i%d" % k, "rpg_pr_i%d" % k, "rpg.pr.join%d" % k
        # 入口由调度挑人：去掉「附近 16 格」的挑法
        edit(pi + "/start", lambda s: "\n".join(l for l in s.split("\n")
                                                 if not re.match(r"tag @a(\[distance=..16[^\]]*\])? (add|remove) " + re.escape(j), l)))
        # 掉线重连由调度按组号转进来
        edit(pi + "/tick", lambda s: "\n".join(l for l in s.split("\n") if "rpg_pr_lv=1.." not in l))
        # 背包欠条：木桶里存着谁的东西，这个战场就不能给下一组用
        edit(pi + "/join", lambda s: s.replace("function rpg:%s/iso/save with storage rpg:pr_i%d tmp\n" % (pi, k),
                                               "function rpg:%s/iso/save with storage rpg:pr_i%d tmp\nscoreboard players add #owe %s 1\n" % (pi, k, o), 1))
        edit(pi + "/iso/restore", lambda s: s.replace("\nclear @s\n", "\nscoreboard players remove #owe %s 1\nscoreboard players reset @s rpg_pr_g\nclear @s\n" % o, 1))
        # 场地没备好：新手开局里的人直接进正式游戏
        edit(pi + "/prep_fail", lambda s: s.replace("tag @a remove %s" % j,
                                                    "execute as @a[tag=%s] run scoreboard players reset @s rpg_pr_g\n"
                                                    "execute as @a[tag=%s,tag=rpg.ob] run function rpg:onboard/pro/after\ntag @a remove %s" % (j, j, j), 1))
        # 分到这一组的人一个都没进来（掉线了）：放掉场地
        edit(pi + "/prep", lambda s: s + "execute if score #bt %s matches 60.. unless entity @a[tag=%s] run function rpg:%s/cleanup\n" % (o, ptag(k), pi))
        # 进度奖励：只认这一组的人；别的组的人碰到也要收回进度，免得卡住
        for reg_dir, t in (("advancement", pi), ("advancement", mi)):
            base = os.path.join(DATA, reg_dir, t)
            for p in walk(base):
                d = json.loads(rd(p))
                f = d.get("rewards", {}).get("function")
                if not f:
                    continue
                aid = "rpg:%s/%s" % (t, os.path.relpath(p, base).replace("\\", "/")[:-5])
                guard = "execute unless entity @s[tag=%s] run return run advancement revoke @s only %s" % (ptag(k), aid)
                fp = os.path.join(FUNC, f.split(":", 1)[1] + ".mcfunction")
                s = rd(fp)
                if guard not in s:
                    wr(fp, guard + "\n" + s)


def patch_original_michael():
    """主世界那场米迦勒战：选择器避开序章维度；序章里的人打到序章的米迦勒时，原件的进度奖励收回就走。"""
    for p in walk(os.path.join(FUNC, "michael_boss")):
        s = rd(p)
        s2 = selectors(s, fix_orig)
        if s2 != s:
            wr(p, s2)
    base = os.path.join(DATA, "advancement", "michael_boss")
    for p in walk(base):
        d = json.loads(rd(p))
        f = d.get("rewards", {}).get("function")
        aid = "rpg:michael_boss/%s" % os.path.relpath(p, base).replace("\\", "/")[:-5]
        guard = "execute if entity @s[tag=rpg.pr] run return run advancement revoke @s only %s" % aid
        fp = os.path.join(FUNC, f.split(":", 1)[1] + ".mcfunction")
        s = rd(fp)
        if guard not in s:
            wr(fp, guard + "\n" + s)
    # 米迦勒的外观：序章模式原来看全局的 #pro rpg_mk，现在看他在不在序章维度
    p = os.path.join(FUNC, "michael", "look", "solid.mcfunction")
    s = rd(p)
    s = s.replace("execute if score #pro rpg_mk matches 1 run return run function rpg:michael/look/prologue",
                  "execute if predicate rpg:in_prologue run return run function rpg:michael/look/prologue")
    assert "rpg:in_prologue" in s, "michael/look/solid 改过了"
    wr(p, s)
    wr(os.path.join(DATA, "predicate", "in_prologue.json"), json.dumps({
        "condition": "minecraft:any_of",
        "terms": [{"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"location": {"dimension": DIMS[k]}}}
                  for k in range(1, N + 1)]}, indent=1) + "\n")


def drop_original():
    """原件的序章树、进度、谓词删掉（复制品已经齐了）。"""
    shutil.rmtree(os.path.join(FUNC, "prologue"))
    for reg in ("advancement", "predicate"):
        q = os.path.join(DATA, reg, "prologue")
        if os.path.isdir(q):
            shutil.rmtree(q)
    # 原版米迦勒战的序章血线钩子：序章的函数都在复制品里了
    for p in walk(os.path.join(DATA, "tags", "function", "michael_boss")):
        d = json.loads(rd(p))
        d["values"] = [v for v in d.get("values", []) if "rpg:prologue/" not in (v if isinstance(v, str) else v.get("id", ""))]
        wr(p, json.dumps(d, ensure_ascii=False, indent=1) + "\n")


# ---------------------------------------------------------------------------- 调度
def hub():
    o = lambda k: "rpg_pr_i%d" % k
    note = lambda text: 'title @s actionbar {"text":"%s","color":"#E8D9B0"}' % text
    load = ["# 序章调度（prologue_multi.py）：每个战场的计分项、血条在各自的 load 里",
            "scoreboard objectives add rpg_pr_g dummy",
            "scoreboard objectives add rpg_pr_qt dummy",
            "scoreboard objectives add %s dummy" % H]
    for k in range(1, N + 1):
        load += ["execute in %s run function %s/load" % (DIMS[k], P(k)),
                 "execute in %s run function rpg:michael_boss_i%d/load" % (DIMS[k], k),
                 "execute unless score #owe %s matches 0.. run scoreboard players set #owe %s 0" % (o(k), o(k))]
    fn("load", load)
    tick = ["execute as @a[scores={rpg_pr_lv=1..}] run function rpg:prologue/rejoin"]
    for k in range(1, N + 1):
        tick += ["execute in %s run function %s/tick" % (DIMS[k], P(k)),
                 "execute if score #fight rpg_mk_i%d matches 1 in %s run function rpg:michael_boss_i%d/tick" % (k, DIMS[k], k)]
    tick += ["scoreboard players add #sec %s 1" % H,
             "execute if score #sec %s matches 20.. run function rpg:prologue/queue" % H]
    fn("tick", tick)
    rej = ["# 重新登录（as 玩家）：按组号交给自己的战场；分了组却没来得及进去的，重新排队",
           "execute if entity @s[tag=!rpg.pr] if score @s rpg_pr_g matches 1.. run function rpg:prologue/requeue",
           "execute unless score @s rpg_pr_g matches 1.. run return run scoreboard players reset @s rpg_pr_lv"]
    for k in range(1, N + 1):
        rej.append("execute if score @s rpg_pr_g matches %d in %s run function %s/rejoin" % (k, DIMS[k], P(k)))
    fn("rejoin", rej)
    fn("requeue", ["scoreboard players reset @s rpg_pr_g", "scoreboard players reset @s rpg_pr_lv"] +
       ["tag @s remove rpg.pr.join%d" % k for k in range(1, N + 1)] +
       ["execute if entity @s[tag=rpg.ob] run function rpg:prologue/enqueue"])
    fn("enqueue", ["# 排进序章的队（as 玩家）：凑满四人或等不到别人就开一组",
                   "execute if entity @s[tag=rpg.pr] run return 0",
                   "tag @s add rpg.pr.q",
                   "scoreboard players set @s rpg_pr_qt 0"])
    q = ["# 每秒：排队的人分进空闲的战场（四人一组）",
         "scoreboard players set #sec %s 0" % H,
         "execute store result score #q %s if entity @a[tag=rpg.pr.q]" % H,
         "execute if score #q %s matches 0 run return 0" % H,
         "scoreboard players add @a[tag=rpg.pr.q] rpg_pr_qt 1",
         "scoreboard players set #free %s 0" % H]
    for k in range(N, 0, -1):
        q.append("execute if score #state %s matches 0 if score #owe %s matches ..0 run scoreboard players set #free %s %d" % (o(k), o(k), H, k))
    q += ["execute if score #free %s matches 0 as @a[tag=rpg.pr.q] run %s" % (H, note("序章的战场都有人在打，空出来就轮到你…… All battlefields are busy.")),
          "execute if score #free %s matches 0 run return 0" % H,
          "# 还有人在走开局（起名、抽身份、锻造教学）：多等一会儿，凑成一组",
          "execute store result score #pend %s if entity @a[tag=rpg.ob,tag=!rpg.pr.q,tag=!rpg.pr]" % H,
          "scoreboard players set #go %s 0" % H,
          "execute if score #q %s matches 4.. run scoreboard players set #go %s 1" % (H, H),
          "execute if score #pend %s matches 0 if entity @a[tag=rpg.pr.q,scores={rpg_pr_qt=3..}] run scoreboard players set #go %s 1" % (H, H),
          "execute if entity @a[tag=rpg.pr.q,scores={rpg_pr_qt=60..}] run scoreboard players set #go %s 1" % H,
          "execute if score #go %s matches 0 as @a[tag=rpg.pr.q] run function rpg:prologue/wait_note" % H,
          "execute if score #go %s matches 0 run return 0" % H,
          "tag @a[tag=rpg.pr.q,limit=4] add rpg.pr.pick"]
    for k in range(1, N + 1):
        q.append("execute if score #free %s matches %d run function rpg:prologue/go_%d" % (H, k, k))
    fn("queue", q)
    fn("wait_note", ["scoreboard players operation #n %s = #q %s" % (H, H),
                     "execute if score #n %s matches 5.. run scoreboard players set #n %s 4" % (H, H)] +
       ["execute if score #n %s matches %d run %s" % (H, n, note("正在等待同伴一起进入序章（%d/4）…… Waiting for companions (%d/4)" % (n, n))) for n in range(1, 5)])
    for k in range(1, N + 1):
        fn("go_%d" % k, ["# 这一组进第 %d 号战场（%s）" % (k, DIMS[k]),
                         "execute as @a[tag=rpg.pr.pick] run function rpg:prologue/assign_%d" % k,
                         "execute in %s run function %s/start" % (DIMS[k], P(k))])
        fn("assign_%d" % k, ["tag @s remove rpg.pr.pick", "tag @s remove rpg.pr.q", "scoreboard players reset @s rpg_pr_qt",
                             "scoreboard players set @s rpg_pr_g %d" % k, "tag @s add rpg.pr.join%d" % k])
    fn("start", ["# 管理员：把执行位置 16 格内最多 4 名玩家立刻编成一组送进序章（有空闲战场时）",
                 "tag @a[distance=..16,gamemode=!spectator,tag=!rpg.pr,limit=4,sort=nearest] add rpg.pr.q",
                 "scoreboard players set @a[tag=rpg.pr.q,distance=..16] rpg_pr_qt 60",
                 "function rpg:prologue/queue"])
    clear = ["# 管理员：中止所有战场，所有人还原，排队清空"]
    for k in range(1, N + 1):
        clear += ["execute in %s as @a[tag=%s] run function %s/iso/restore" % (DIMS[k], ptag(k), P(k)),
                  "execute in %s run function %s/cleanup" % (DIMS[k], P(k)),
                  "scoreboard players set #owe %s 0" % o(k)]
    clear += ["tag @a remove rpg.pr.q", "tag @a remove rpg.pr.pick", "scoreboard players reset @a rpg_pr_g",
              'tellraw @s {"text":"[序章] 所有战场已中止。","color":"#E8D9B0"}']
    fn("clear", clear)
    fn("status", ["# 管理员：各战场的状态"] + [
        'tellraw @s ["",{"text":"[序章] 战场 %d · 状态 ","color":"#E8D9B0"},{"score":{"name":"#state","objective":"%s"}},'
        '{"text":" · 欠背包 "},{"score":{"name":"#owe","objective":"%s"}}]' % (k, o(k), o(k)) for k in range(1, N + 1)])


def check():
    """复制品里不该出现原件的名字；资源 ID（物品模型、字体、声音、翻译键、地物）不能被改动。"""
    bad = []
    for k in range(1, N + 1):
        for t in TREES:
            src = os.path.join(FUNC, t) if t != "prologue" else None
            for p in walk(os.path.join(FUNC, "%s_i%d" % (t, k))):
                s = rd(p)
                for pat in (r"function #?rpg:prologue/", r"function #?rpg:michael_boss/", r"\brpg_pr\b(?!_)", r"\brpg_mk\b(?!_)", r"storage rpg:pr ",
                            r"rpg:armageddon(?![\w/])" if k > 1 else r"(?!x)x"):
                    if re.search(pat, s):
                        bad.append((p, pat))
    if bad:
        for b in bad[:20]:
            print("prologue_multi: 残留", b)
        raise SystemExit("prologue_multi: 复制品里还有原件的名字")


def main():
    clean()
    copy_trees()
    patch_copies()
    patch_original_michael()
    drop_original()
    hub()
    check()
    n = sum(1 for k in range(1, N + 1) for t in TREES for _ in walk(os.path.join(FUNC, "%s_i%d" % (t, k))))
    print("prologue_multi: %d battlefields (%s), %d copied functions, %d hub functions" % (N, ", ".join(DIMS.values()), n, COUNT[0]))


if __name__ == "__main__":
    main()
