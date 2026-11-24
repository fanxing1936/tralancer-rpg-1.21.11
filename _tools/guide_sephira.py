# -*- coding: utf-8 -*-
"""图鉴「XVI 原质与力」一章：身份、原质十阶、主柱、圣力与魔力、技能表、王冠终式、传承书、身份能力。

数字全部读 add_sephira / add_force / force_ext / onboard_spec 里的表，改了数据包重跑 emit_guide.py 就跟着变。
"""
import add_force as F
import add_sephira as S
import force_ext as X
import onboard_spec as OB
from guide_tutorial import _part, _steps, _table

FORCE = {0: "无（美丽阶觉醒）", 1: "圣力", 2: "魔力", 3: "圣力与魔力"}
IDENT_POWER = {
    1: "阅历 +20%；恶魔附近新上身的负面效果时长 −30%",
    2: "6 格内的空缺者显形；魔力技能冷却 −10%",
    3: "圣力技能的生命力消耗 −30%",
    4: "本柱罪性的被动；本柱契约的魔化减半；锻自己那一柱罪器只要 4 片罪印；买本柱契约书半价",
    5: "对恶魔与亡灵 +25% 伤害",
    6: "保惠师光环：12 格内友方生命恢复；每 10 秒，圣力者的生命力 +1",
    7: "教皇的「收回契约」不来；每 20 分钟一次「第三日」",
}


def _ranks(v, unit=""):
    return "/".join("%g" % x for x in v) + unit if len(set(v)) > 1 else "%g%s" % (v[0], unit)


def _skills(tree):
    rows = []
    for n, tr, br, name, desc, cost, extra, cd, passive in F.SKILLS:
        if tr != tree:
            continue
        b = F.BRANCH[tree][br]
        if passive:
            rows.append((b[0] + "・" + b[1], "<span class=\"nm\">%s</span>" % name, desc, "被动", "—"))
        else:
            second = ("生命力 " if tree == 1 else "魔化 +") + _ranks(extra)
            rows.append((b[0] + "・" + b[1], "<span class=\"nm\">%s</span>" % name, desc,
                         "%s %s，%s" % (F.TREES[tree][0], _ranks(cost), second), _ranks(cd, " 秒")))
    return _table(["分支", "技能", "效果（1/2/3 级）", "代价", "冷却"], rows)


def section():
    p = []
    a = p.append
    a('''<section class="plate" id="s18">
<div class="plate-h"><span class="num">XVI</span><h2>原质与力</h2><span class="sub">身份 · 十阶 · 主柱 · 圣力与魔力 · 技能</span></div>
<p class="tut-lead">角色的成长是生命之树：从<strong>王国</strong>一阶一阶走到<strong>王冠</strong>。不绑定任何 Boss，怎么练都行。
经验等级不再加生命，旧的驱魔等级也退出了成长。</p>''')
    a(_part("p-ident", "身份", "开局抽一次", _table(["身份", "是谁", "生来的力", "身份能力（美丽阶起翻倍）"], [
        ("<span class=\"nm\">%s</span>" % name, desc, FORCE[S.IDENT_FORCE[n]], IDENT_POWER[n]) for n, _k, name, _c, desc in OB.IDENTITIES])))
    gates = []
    for n, _k, name, latin, _heb, _c, _pl in S.TIERS:
        mats = "、".join("%s ×%d" % (S.MAT_NAME[m], c) for m, c in S.MATS.get(n, [])) or "—"
        note = {2: "选主柱", 5: "无知者在这里觉醒，选圣力或魔力", 7: "之后过达阿特", 10: "王冠终式"}.get(n, "")
        gates.append((n, "<span class=\"nm\">%s</span>" % name, latin, S.THR[n], "+%d" % (4 * (n - 1)), S.SP[n], mats, note))
    a(_part("p-tier", "原质十阶", "只看综合能力", "<p><b>综合能力</b> = 阅历 + 装备分（四件护甲与主手的装备等级之和 ×10）。到了门槛自动晋阶。"
            "阅历来自击杀（普通怪每天前 %d 只各 1，精英 5，首领再加 15）、裁决 10、驱逐 3、悬赏 10，六个 Boss 首杀 80、之后每天每个前 3 次 15。</p>" % S.DAILY_KILLS
            + _table(["阶", "原质", "拉丁", "综合能力", "生命", "技能点", "晋阶给的材料", "这一阶"], gates)))
    a(_part("p-pillar", "三根主柱", "第 2 阶选，不能改", _table(["主柱", "方向", "加成"], [
        ("严厉柱", "进攻", "第 3、6 阶伤害各 +5%，第 6 阶起对 Boss 再 +5%，第 8 阶攻速 +10%"),
        ("慈悲柱", "守护与续命", "第 4、7 阶护甲各 +2；第 7 阶受致命伤时 3 秒抗性 II（冷却 3 分钟）；第 9 阶 6 格内友方抗性 I"),
        ("中柱", "控制与机动", "圣力恢复 +15%；第 10 阶力条上限再 +40"),
    ]) + "<p>主柱那一支的技能升到 3 级少花 1 点。力条上限 %d，第 4、7、9 阶各 +20。</p>" % S.MANA_BASE))
    a(_part("p-force", "圣力与魔力", "状态行里各一根条", _table(["", "圣力", "魔力"], [
        ("怎么回", "每秒 +1，站着不动（祷告）+3，燃着的驱魔图腾 8 格内翻倍", "不会自己回：每造成 2 点伤害 +1，击杀 +4，魔化每涨 1 点 +3"),
        ("代价", "技能还要花<b>生命力</b>", "技能会涨<b>魔化</b>"),
        ("施法物", "圣徽", "罪印"),
    ]) + '<div class="note"><b>生命力：</b>圣力者的魔化那一行换成生命力。沾上的每一点魔化变成 1 点生命力损失和 1 点<b>同化</b>。'
         '每分钟 +1，睡一觉 +40，在灵魂营火 2 格内每秒 +1。归零是<b>燃尽</b>：圣力不回应、圣器不保护你，回到 30 才解除。</div>'
         '<div class="note"><b>同化：</b>圣力者也能签七柱契约，代价是同化。满 100 堕入魔力；解约且魔化回到 0 就回到圣力，得了新约的人可以直接回头。</div>'))
    a(_part("p-use", "怎么学、怎么放", "", _steps([
        ("拿到施法物", "<p>有了力，就会得到<b>圣徽</b>或<b>罪印</b>。丢了可以在技能页里重新领。</p>", ""),
        ("打开技能页", "<p>主手拿着施法物按 <kbd>Shift</kbd>+<kbd>F</kbd>。学技能、升级、放进三个格子、洗点都在这里。同一分支按顺序解锁。</p>", ""),
        ("施放", "<p><kbd>右键</kbd> 放第 1 格，<kbd>潜行</kbd>+<kbd>右键</kbd> 放第 2 格，<kbd>F</kbd> 放第 3 格。力不够、在冷却时，状态行会告诉你。</p>", ""),
    ])))
    a(_part("p-holy", "圣力技能", "12 个 · 三支", _skills(1)))
    a(_part("p-mana", "魔力技能", "12 个 · 三支", _skills(2)))
    ex = {e[0]: e for e in F.EXTRA}
    lords = {1: "路西法", 2: "利维坦", 3: "亚巴顿", 4: "别西卜", 5: "萨麦尔", 6: "贝利尔", 7: "玛门"}
    a(_part("p-crown", "王冠终式", "第 10 阶自动习得", _table(["谁", "终式", "效果"], [
        ("圣力", "<span class=\"nm\">%s</span>" % ex[25][2], ex[25][3]),
        ("圣子", "<span class=\"nm\">审判</span>", "替换「哈利路亚」"),
        ("圣灵", "<span class=\"nm\">复活</span>", "替换「哈利路亚」：60 秒内倒下的队友站起来，每 10 分钟一次"),
        ("魔力", "<span class=\"nm\">%s</span>" % ex[26][2], ex[26][3]),
    ] + [("七罪之仆・" + lords[n], "<span class=\"nm\">%s</span>" % v[0], v[1]) for n, v in X.LORD_FIN.items()])))
    a(_part("p-legacy", "传承书", "六个 Boss 各一本", "<p>首次击败必得，之后每次 20%。读了就会，不占技能点，两棵树的格子都能放。</p>"
            + _table(["出自", "技能", "效果", "冷却"], [
                (X.BOSS_NAME[e[7]][0], "<span class=\"nm\">%s</span>" % e[2], e[3], "%d 秒" % e[6]) for e in F.EXTRA if e[7]])))
    a("</section>")
    return "\n".join(p)
