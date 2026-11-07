# -*- coding: utf-8 -*-
"""粒子与特效的单一来源（docs/VFX-SPEC.md）。

颜色仍然只在 rpg_ui_style 里定义一份；这里只管「用哪种粒子、放多少、给谁看」：

* TIERS      —— 六档强度，每档的数量／速度／尺寸上限，以及能不能用 force。
* tier_of()  —— 按函数路径判档。规则按顺序匹配，第一条命中的生效。
* conform()  —— 把一条 particle 命令收进它那一档的上限（polish_vfx 在构建末端调用）。
* flash() / ring() / VOCAB —— 生成器直接写规范粒子时用的帮助函数和词表。

force 会无视玩家的「粒子：减少／最少」设置，并把可见距离从 32 格拉到 512 格。
它是玩法信号，不是装饰：只留给「伤害前的预警」和「大招」（用户 2026-11-03 拍板）。
"""

import math
import re

import rpg_ui_style as ui


# ---------------------------------------------------------------------------
# 强度分级
# ---------------------------------------------------------------------------
# count：单条命令的粒子数上限；speed：速度上限（只对按速度飞散的粒子生效）；
# spread：散布（|dx|,|dy|,|dz| 的最大值）上限，只警告不收口 —— 散布就是玩法范围；
# scale：dust 尺寸上限（ART-STYLE §6 的三档尺寸）；force：本档是否允许 force。
TIERS = {
    "ambient":   dict(count=4,  speed=0.05, spread=1.0,  scale=1.0, force=False),   # 每刻都画
    "pulse":     dict(count=24, speed=0.08, spread=2.5,  scale=1.2, force=False),   # 十刻以上一拍
    "hit":       dict(count=24, speed=0.25, spread=2.0,  scale=1.6, force=False),   # 命中、受击、个人反馈
    "skill":     dict(count=80, speed=0.30, spread=6.0,  scale=2.0, force=False),   # 招式、成功、仪式节点
    "telegraph": dict(count=64, speed=0.08, spread=12.0, scale=3.0, force=True),    # 伤害前的预警／蓄势
    "ult":       dict(count=96, speed=0.35, spread=18.0, scale=3.0, force=True),    # 大招、罪约、罪域
}

# 一次调用里所有粒子加起来的建议上限。只由 check_vfx_budget 警告。
# 同一个函数里按不同计时分段（`matches 12` / `matches 1`）的，按最重的那一段算。
EVENT_TOTAL = {"hit": 64, "skill": 200, "telegraph": 200, "ult": 400}

# 常驻预算：同一个实体每刻最多画几颗；全场常驻（不含生命之树这种图形）每刻合计上限。
AMBIENT_PER_ENTITY = 4
AMBIENT_TOTAL = 48

# 这些粒子的 speed 不是飞散速度（是起点偏移或固有动画），不按速度上限收。
SPEED_EXEMPT = {
    "portal", "reverse_portal", "enchant", "nautilus", "bubble_column_up",
    "sonic_boom", "sweep_attack", "explosion", "explosion_emitter", "flash",
    "gust", "gust_emitter_small", "gust_emitter_large", "elder_guardian",
}


# ---------------------------------------------------------------------------
# 哪些目录受规范约束
# ---------------------------------------------------------------------------
# full：数量、速度、尺寸、force 全部收口。force_only：只执行 force 规则 ——
# 武器特效是作者的设计（ART-STYLE §6），数量与颜色保留原样。
FULL_ZONES = ("taint/", "inquest/", "divine/", "rite/", "pact/", "minion/",
              "entities/warden/", "vacant/", "doll/", "mammon/", "ritual/",
              "exorcism", "pope_fight/")
FORCE_ONLY_ZONES = ("item/",)
# 展示实体生物归建模会话；死代码不动。
SKIP = re.compile(r"^(tower_guard|beelzebub|leviathan|vanguard|sunken_skeleton)/"
                  r"|^entities/warden/warden/g\d$")


def zone(rel):
    if SKIP.search(rel):
        return None
    if rel.startswith(FULL_ZONES):
        return "full"
    if rel.startswith(FORCE_ONLY_ZONES):
        return "force_only"
    return None


# 路径 -> 档位。按顺序匹配；都不中就是 skill。
TIER_RULES = [
    # 图形：生命之树每十刻重画一次，四百多个点各一颗，由 check_life_tree_particles 管密度。
    (r"^ritual/life_tree/draw$", "pulse"),
    # 每刻
    (r"^entities/warden/phase\d_entity$", "ambient"),
    (r"/(bound_tick|anchor_tick|shine)$", "ambient"),
    (r"^rite/beat_(inv|pure)$", "ambient"),
    (r"^item/legacy/projectiles_active$", "ambient"),
    (r"^pope_fight/fx/(blast|fall|beam)$", "ambient"),
    (r"^pope_fight/(stage3_spiral|boss/blood_step|heart/weak_fx)$", "pulse"),
    (r"^pope_fight/(stage2_enter|fx/burst|stage4_enter|heart/shatter)$", "ult"),
    # 十刻以上一拍
    (r"^taint/step$", "pulse"),
    (r"^rite/pool_beat$", "pulse"),
    (r"^inquest/counter/\w+_wait$", "pulse"),
    # 预警与蓄势
    (r"(_warn|_charge|pressure_warning)$", "telegraph"),
    (r"^inquest/phase2/warning(/\d+)?$", "telegraph"),
    (r"^inquest/counter/start\d$", "telegraph"),
    # 大招
    (r"^taint/ult\d$", "ult"),
    (r"^inquest/phase2/(pressure/\d_\d|wave/\d_\d|shockwave|pressure_core)$", "ult"),
    (r"^divine/(invoke_old|invoke_new_field|gather/finish)$", "ult"),
    (r"^rite/(v\d|inv_burst)$", "ult"),
    (r"^taint/advent_at$", "ult"),
    (r"^ritual/life_tree/complete$", "ult"),
    (r"^entities/warden/phase\d_boss$", "ult"),
    # 命中与个人反馈
    (r"(_hit|_hit_holy|/hurt|/strike|_target|/receive|_seize|/seize|_take|/take"
     r"|_reap|_drain|_crush|_bite|_sting|/execute|/tear|/scald)$", "hit"),
]
_RULES = [(re.compile(p), t) for p, t in TIER_RULES]

# 落在每个玩家身上的那一份（`as @a[...] at @s run particle`）永远是个人反馈。
PER_PLAYER = re.compile(r"\b(?:as|at) @a\[[^\]]*\](?: at @s)? run particle ")


def tier_of(rel):
    for rx, tier in _RULES:
        if rx.search(rel):
            return tier
    return "skill"


def line_tier(rel, line):
    if PER_PLAYER.search(line):
        return "hit"
    return tier_of(rel)


# ---------------------------------------------------------------------------
# 解析与收口
# ---------------------------------------------------------------------------
_HEAD = re.compile(r"(?:^|\brun )particle ")


def split(line):
    """(prefix, name, args) —— name 带 {...} 参数；不是 particle 命令时返回 None。"""
    m = _HEAD.search(line)
    if not m or line.lstrip().startswith("#"):
        return None
    start = m.end()
    depth, i = 0, start
    while i < len(line):
        c = line[i]
        if c in "{[":
            depth += 1
        elif c in "}]":
            depth -= 1
        elif c == " " and depth == 0:
            break
        i += 1
    return line[:start], line[start:i], line[i:].split()


def _short(name):
    return name.split("{", 1)[0].replace("minecraft:", "")


def _fmt(x):
    s = ("%.3f" % x).rstrip("0").rstrip(".")
    return s if s not in ("", "-0") else "0"


def conform(line, tier, force_only=False):
    """把一条 particle 命令收进 ``tier`` 的上限。返回 (新行, 改动说明列表)。"""
    parts = split(line)
    if parts is None:
        return line, []
    prefix, name, args = parts
    cap = TIERS[tier]
    notes = []
    # args: x y z dx dy dz speed count [mode [viewers]]
    if len(args) >= 9 and args[8] == "force" and not cap["force"]:
        args[8] = "normal"
        notes.append("force")
    if not force_only:
        if len(args) >= 8 and args[7].isdigit() and int(args[7]) > cap["count"]:
            notes.append("count %s>%d" % (args[7], cap["count"]))
            args[7] = str(cap["count"])
        if len(args) >= 7 and _short(name) not in SPEED_EXEMPT:
            try:
                speed = float(args[6])
            except ValueError:
                speed = None
            if speed is not None and speed > cap["speed"]:
                notes.append("speed %s>%s" % (args[6], _fmt(cap["speed"])))
                args[6] = _fmt(cap["speed"])
        sm = re.search(r"scale:([\d.]+)", name)
        if sm and float(sm.group(1)) > cap["scale"]:
            notes.append("scale %s>%s" % (sm.group(1), _fmt(cap["scale"])))
            name = name[:sm.start(1)] + _fmt(cap["scale"]) + name[sm.end(1):]
    if not notes:
        return line, []
    return prefix + name + " " + " ".join(args), notes


# ---------------------------------------------------------------------------
# 颜色：闪光与旧色折叠
# ---------------------------------------------------------------------------
def flash(colour):
    """flash 粒子：颜色取色板值（整数 RGB）。"""
    return "flash{color:%d}" % int(ui.hex_of(colour).lstrip("#"), 16)


def pillar_flash(key):
    """领主的闪光一律取亮色。深色闪光在白天几乎看不见。"""
    return flash(ui.pillar(key)["lit"])


def _flash_folds():
    """旧的柱色／深色闪光 -> 柱亮色。"""
    out = []
    for p in ui.PILLARS:
        for old in ui.PILLAR_LEGACY[p["slug"]] + (p["deep"],):
            out.append((old, p["lit"]))
    out.append((ui.NAMELESS["deep"], ui.NAMELESS["lit"]))
    out.append(("#D23B47", ui.NAMELESS["lit"]))       # 无名者旧亮色
    out.append(("#E74D55", ui.NAMELESS["lit"]))
    return out


FLASH_FOLDS = _flash_folds()
FLASH_NEUTRAL = {"#FFFFF0": ui.WHITE}               # 象牙白冲击闪光并入白
# 已经是色板值的闪光一律不动：例如无名者亮色 #DC4450 离萨麦尔旧色、
# HOLY_DARK 离玛门旧色都不远，不能被「就近折叠」误改。
_PALETTE = {c.upper() for c in (
    ui.WHITE, ui.HOLY, ui.HOLY_LIGHT, ui.HOLY_DARK, ui.RITUAL, ui.CYAN, ui.CYAN_LIGHT,
    ui.READY, ui.WARN, ui.PASSION, ui.MUTED, ui.NAMELESS["lit"])}
_PALETTE |= {p["lit"].upper() for p in ui.PILLARS}


def fold_flash(colour_int):
    """把旧色闪光折回色板。返回新的整数颜色，或 None（不需要改）。"""
    h = "#%06X" % colour_int
    if h in FLASH_NEUTRAL:
        return int(FLASH_NEUTRAL[h].lstrip("#"), 16)
    if h in _PALETTE:
        return None
    best = min(FLASH_FOLDS, key=lambda kv: ui.delta_e(kv[0], h))
    # 旧的罪约闪光与登记的旧色相差都在 ΔE 0.5 以内；阈值留得很窄。
    if ui.delta_e(best[0], h) < 1.5 and best[1].upper() != h:
        return int(best[1].lstrip("#"), 16)
    return None


# ---------------------------------------------------------------------------
# 词表：每个阵营用什么粒子
# ---------------------------------------------------------------------------
# dust：渐变两端（亮 -> 深）。motes：质感粒子。accent：点缀，只能和 dust 一起出现。
VOCAB = {
    "holy": dict(dust=(ui.HOLY, ui.HOLY_DARK), flash=ui.HOLY_LIGHT,
                 motes=("end_rod", "totem_of_undying"), accent=("enchanted_hit", "wax_off")),
    "authority": dict(dust=(ui.CYAN_LIGHT, ui.CYAN), flash=ui.CYAN_LIGHT,
                      motes=("end_rod", "electric_spark"), accent=("enchanted_hit",)),
    "kabbalah": dict(dust=tuple(ui.SEPHIROT.values()), flash=ui.RITUAL,
                     motes=("enchant",), accent=("end_rod",)),
    "demon": dict(dust=(ui.NAMELESS["lit"], ui.NAMELESS["deep"]), flash=ui.NAMELESS["lit"],
                  motes=("squid_ink", "large_smoke", "sculk_soul", "soul"),
                  accent=("trial_spawner_detection_ominous", "trial_omen", "reverse_portal")),
}
for _p in ui.PILLARS:
    VOCAB[_p["slug"]] = dict(dust=(_p["lit"], _p["deep"]), flash=_p["lit"],
                             motes=(_p["mote"],), accent=())


def ring(particle, radius, y=0.1, points=16, tail="0 0 0 0 1", mode="normal"):
    """在 ~ ~y ~ 周围画一圈点（每点一颗）。用来标出伤害或安全范围的边界。"""
    out = []
    for i in range(points):
        a = 2 * math.pi * i / points
        out.append("particle %s ~%s ~%s ~%s %s %s" % (
            particle, _fmt(radius * math.cos(a)), _fmt(y), _fmt(radius * math.sin(a)),
            tail, mode))
    return out
