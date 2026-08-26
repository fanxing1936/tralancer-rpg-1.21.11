# -*- coding: utf-8 -*-
"""Single source of truth for the public/manual debug command catalogue."""

from html import escape


def command(path, use, prerequisite, effect="局部", risk="常规"):
    return {"command": path, "use": use, "prerequisite": prerequisite,
            "effect": effect, "risk": risk}


LORDS = [
    ("lucifer", "路西法", 1, [("bael", "巴力", "先锋"), ("agares", "阿加雷斯", "猎手"), ("vassago", "瓦沙克", "司祭"), ("samigina", "萨米基纳", "咒使"), ("marbas", "马尔巴士", "处刑者")]),
    ("leviathan", "利维坦", 2, [("valefor", "华利弗", "先锋"), ("amon", "亚蒙", "猎手"), ("barbatos", "巴巴托斯", "司祭"), ("paimon", "派蒙", "咒使"), ("buer", "布耶尔", "处刑者")]),
    ("abaddon", "亚巴顿", 3, [("gusion", "古辛", "先锋"), ("sitri", "西迪", "猎手"), ("beleth", "贝雷特", "司祭"), ("leraje", "列拉金", "咒使"), ("eligos", "艾利欧格", "处刑者")]),
    ("beelzebub", "别西卜", 4, [("zepar", "桀派", "先锋"), ("botis", "布提斯", "猎手"), ("bathin", "巴钦", "司祭"), ("sallos", "塞列欧斯", "咒使"), ("purson", "布松", "处刑者")]),
    ("samael", "萨麦尔", 5, [("marax", "莫拉格斯", "先锋"), ("ipos", "因波斯", "猎手"), ("aim", "艾姆", "司祭"), ("naberius", "纳贝流士", "咒使"), ("glasya_labolas", "格拉夏·拉波拉斯", "处刑者")]),
    ("belial", "贝利尔", 6, [("bune", "布涅", "先锋"), ("ronove", "罗诺比", "猎手"), ("berith", "比利士", "司祭"), ("astaroth", "亚斯塔禄", "咒使"), ("forneus", "佛纽司", "处刑者")]),
    ("mammon", "玛门", 7, [("foras", "佛拉斯", "先锋"), ("asmoday", "阿斯摩太", "猎手"), ("gaap", "盖布", "司祭"), ("furfur", "佛尔佛尔", "咒使"), ("marchosias", "马可西亚斯", "处刑者")]),
]

STAGES = [
    "楔子｜第十三声钟",
    "发现异常｜取得 3 份相互矛盾的记录",
    "会回家的死者｜以圣器照见空缺",
    "见证人封锁线｜听完简报后迎战",
    "确认活动区域｜让三条运输记录彼此指认",
    "调查真名与弱点｜排除 2 个错误答案",
    "被撕去的判词｜准备 3 组仪式器具",
    "万蝇腐宴｜Boss 与四阶段驱魔",
    "四种不完整的裁决｜见证人印缺失",
    "活着的人必须有名字｜救下米拉",
    "边缘者登记｜选择驱魔道路后完成归档",
]

SYSTEM = [
    command("/function rpg:command/soreboard", "手动补建／修复全部计分项。", "正常由 #minecraft:load 自动执行；仅在初始化异常或独立函数测试时手动调用。", "全存档", "恢复入口"),
    command("/function rpg:command/bossbar", "手动补建四槽恶魔 Boss 血条。", "正常由 #minecraft:load 自动执行；重复执行会出现已存在提示。", "全存档", "恢复入口"),
]

GIVE = [
    command("/function rpg:command/give/box", "发放按类型整理的全套测试潜影盒。", "会发给所有在线玩家（@a）；盒内覆盖当前全部自定义物品。", "全体背包", "群体发放"),
    command("/function rpg:command/give/weapon", "发放全部武器、护甲与药剂。", "会发给所有在线玩家（@a），多人服慎用。", "全体背包", "群体发放"),
    command("/function rpg:command/give/item", "发放符文、符石、晶石与锻造材料。", "会发给所有在线玩家（@a），多人服慎用。", "全体背包", "群体发放"),
    command("/function rpg:command/give/weapon_up_item", "发放全部武器分支唱片。", "会发给所有在线玩家（@a），多人服慎用。", "全体背包", "群体发放"),
    command("/function rpg:command/give/extra", "发放额外／导入内容测试物品。", "会发给所有在线玩家（@a），可能占用较多背包格。", "全体背包", "群体发放"),
    command("/function rpg:inquest/give/all_tools", "发放七罪媒介、仪式工具、三类粉笔和真名残页。", "必须由玩家执行；用于驱魔流程联调。", "自身背包"),
    command("/function rpg:ritual/life_tree/give/all", "发放卡巴拉血契、十源质与真·十字架。", "必须由玩家执行；仅测试／管理入口。", "自身背包"),
]

RESET = [
    command("/function rpg:inquest/reset_self", "重置执行者七柱真名、见证与案件进度。", "必须由目标玩家自己执行；不会重置其他玩家。", "个人档案", "会丢进度"),
    command("/function rpg:inquest/debug/reset_career", "重置执行者驱魔阅历、等级、路线和阶段奖励领取记录。", "必须由目标玩家自己执行。", "个人档案", "会丢进度"),
    command("/function rpg:ritual/life_tree/clear", "清除执行位置 12 格内的生命之树与展示物。", "站在需要清理的法阵附近执行。", "附近实体", "清理"),
    command("/function rpg:ritual/life_tree/clear_all", "清除当前维度所有生命之树与展示物。", "不区分玩家和法阵；仅用于测试服收尾。", "整维度", "全局清理"),
]

BOSSES = [
    command("/function rpg:command/setblock", "在脚下布置试炼刷怪笼与宝库。", "站在测试点执行；会替换脚下及上方方块。", "附近方块", "会改地形"),
    command("/function rpg:command/summon", "在脚下生成通用 1000 生命恶魔 Boss 与护卫。", "预先初始化计分板和 Bossbar；两只生物未声明永久，远离后可能自然消失。", "战斗实体", "生成战斗"),
    command("/function rpg:command/summon_devil", "连续召唤七罪领主，再调用一次契约柱位分派入口。", "仅做全阵容压力测试；会生成 8 位十分钟 Boss。第 8 位受 #lord 分数影响，需先执行 /scoreboard players set #lord rpg_fall 0 才能固定为无名者。", "8 位临时 Boss", "高压生成"),
    command("/function rpg:taint/lord", "按全局 #lord 分数召唤对应领主；0 或非 1–7 时召唤无名者。", "这是契约柱位分派入口；需要固定无名者时先执行 /scoreboard players set #lord rpg_fall 0。", "1 位临时 Boss", "生成战斗"),
]
for lord_id, lord_name, lord_no, _minions in LORDS:
    BOSSES.append(command(f"/function rpg:taint/lord{lord_no}", f"在执行位置召唤七罪领主：{lord_name}（700 生命）。", "预先初始化计分板和 Bossbar；不会自动建立驱魔法阵，十分钟后会自行消散。", "临时 Boss", "生成战斗"))
BOSSES.extend([
])

MINIONS = []
for lord_id, lord_name, _lord_no, minions in LORDS:
    MINIONS.append(command(f"/function rpg:minion/summon/{lord_id}/all", f"一次召唤{lord_name}麾下五职罪仆。", "不检查 Boss、二阶段条件与人口上限；用于编队联调。", "持久实体", "生成五名"))
    for minion_id, minion_name, role in minions:
        MINIONS.append(command(f"/function rpg:minion/summon/{lord_id}/{minion_id}", f"单独召唤{lord_name}麾下{role}「{minion_name}」。", "在执行位置生成；可脱离 Boss 独立、永久存活。", "持久实体", "生成单体"))

CAMPAIGN = [
    command("/function rpg:campaign/beelzebub/start", "正式接受并创建第一章「空缺者」实例。", "安全空地、管理员；会写入正常章节状态。", "章节存档", "正式入口"),
    command("/function rpg:campaign/beelzebub/abort", "中止并清理附近第一章实例。", "必须站在目标实例／控制器 72 格内执行；永久调查与首通档案不回滚。", "章节实例", "清理"),
    command("/function rpg:campaign/beelzebub/debug/menu", "打开可点击的第一章完整调试台。", "必须由玩家执行；建议作为第一章调试总入口。", "无", "推荐"),
    command("/function rpg:campaign/beelzebub/debug/start", "以当前位置作为候选原点开启章节。", "安全空地；仍会执行正式地形与朝向校验。", "章节存档", "创建实例"),
    command("/function rpg:campaign/beelzebub/debug/give_all_items", "发放配置登记的全部第一章物品。", "必须由玩家执行；不写完成、奖励或职业进度。", "自身背包"),
    command("/function rpg:campaign/beelzebub/debug/spawn_boss", "按本章配置在实例内补生别西卜。", "附近必须已有第一章控制器；已有 Boss 时不会重复生成。", "章节实体", "生成战斗"),
    command("/function rpg:campaign/beelzebub/debug/spawn_all_minions", "按配置在实例内额外生成五名别西卜罪仆。", "附近必须已有第一章控制器；不检查现存罪仆，重复执行会每次叠加五名。", "章节持久实体", "生成五名"),
    command("/function rpg:campaign/beelzebub/debug/list_positions", "在聊天栏列出全部可配置相对坐标。", "必须由玩家执行；只读，不改变实例。", "无", "只读"),
]
for stage, label in enumerate(STAGES):
    CAMPAIGN.append(command(f"/function rpg:campaign/beelzebub/debug/stage/{stage}", f"跳转到 Stage {stage}「{label}」。", "附近必须已有第一章控制器；自动清理旧阶段现场。", "章节实例", "不写首通"))

ENDLESS = [
    command("/function rpg:endless/start", "以执行者当前位置开启无尽驱魔「七柱回廊」。", "必须由玩家在安全空地执行；第一章或其他无尽实例运行时会拒绝。", "单一公共副本", "正式入口"),
    command("/function rpg:endless/join", "加入附近 16 格内正在运行的七柱回廊。", "必须由玩家执行；从下一次层末结算开始获得奖励。", "个人副本成员", "加入"),
    command("/function rpg:endless/abort", "关闭附近的七柱回廊并清理所属敌人。", "必须站在控制器 96 格内；历史最深层记录保留。", "副本实体", "清理"),
    command("/function rpg:endless/debug/menu", "打开无尽驱魔调试台。", "必须由玩家执行；可开启、加入、清理或跳转测试层。", "无", "推荐"),
]
for floor in (1, 5, 10, 25, 50, 72, 100):
    ENDLESS.append(command(f"/function rpg:endless/debug/floor/{floor}", f"把附近七柱回廊跳转至第 {floor} 层。", "附近必须已有控制器；清理当前敌人，不补发跳过层奖励。", "副本当前层", "调试跳层"))

CATEGORIES = [
    ("初始化", "首次装包与测试世界基础设施", SYSTEM),
    ("测试物品发放", "优先用潜影盒；@a 群体发放项已单独标注", GIVE),
    ("状态重置与清场", "这些命令会移除个人进度、法阵或展示实体", RESET),
    ("Boss、试炼与军团", "均在执行位置或附近生成实体／方块", BOSSES),
    ("七柱罪仆", "每柱包含一条五职整队命令与五条单体命令", MINIONS),
    ("第一章 · 空缺者", "正式入口、调试台、补生与 Stage 0–10 跳转", CAMPAIGN),
    ("无尽驱魔 · 七柱回廊", "正式入口、多人加入、清理与 1–100 层关键节点跳转", ENDLESS),
]
ALL_COMMANDS = [item for _name, _note, items in CATEGORIES for item in items]


def render_html():
    def risk_class(label):
        if label in {"会丢进度", "全局清理", "高压生成"}:
            return "danger"
        if label in {"群体发放", "清理", "会改地形", "生成战斗", "生成军团", "生成五名", "生成单体", "创建实例"}:
            return "warn"
        return "safe"

    def rows_html(items):
        rows = []
        for item in items:
            rows.append('<tr><td class="num"><code>%s</code></td><td><b>%s</b><span class="risk risk-%s">%s</span></td><td>%s<span class="sm">影响：%s</span></td></tr>' % (escape(item["command"]), escape(item["use"]), risk_class(item["risk"]), escape(item["risk"]), escape(item["prerequisite"]), escape(item["effect"])))
        return "".join(rows)

    parts = []
    for name, note, items in CATEGORIES:
        parts.append('<h3 class="sub-h">%s<span class="rolls">%s · %d 条</span></h3>' % (escape(name), escape(note), len(items)))
        if name == "七柱罪仆":
            parts.append('<div class="debug-lords"><p class="dim">按柱位展开；每组先列五职整队入口，再列五条单体入口。</p>')
            for index, (_lord_id, lord_name, _lord_no, _minions) in enumerate(LORDS):
                lord_items = items[index * 6:(index + 1) * 6]
                parts.append('<details class="debug-lord"><summary><b>%s麾下</b><span>6 条 · 五职整队／单体</span></summary><div class="tw debug-table"><table><thead><tr><th>可复制指令</th><th>用途</th><th>前置与影响</th></tr></thead><tbody>%s</tbody></table></div></details>' % (escape(lord_name), rows_html(lord_items)))
            parts.append('</div>')
        else:
            parts.append('<div class="tw debug-table"><table><thead><tr><th>可复制指令</th><th>用途</th><th>前置与影响</th></tr></thead><tbody>%s</tbody></table></div>' % rows_html(items))
    return "".join(parts)


def render_markdown():
    out = ["# TRALANCER RPG 调试指令手册", "", f"> 共 {len(ALL_COMMANDS)} 个公开、可手动执行的调试／管理入口。适配 Minecraft Java 1.21.11。", "", "所有命令默认需要开启作弊或拥有管理员权限。带 `@s` 的入口必须由目标玩家自己执行；命令方块或服务器控制台不会自动获得玩家上下文。", "", "本手册只收录设计为人工调用的稳定入口。`*_worker`、每刻 tick、伤害结算、UI 刷新和阶段内部函数不是公共接口，手动执行可能制造半成品状态，因此不列入清单。", ""]
    for name, note, items in CATEGORIES:
        out.extend([f"## {name}", "", note, "", "| 指令 | 用途 | 前置、影响与风险 |", "|---|---|---|"])
        for item in items:
            detail = f'{item["prerequisite"]} 影响：{item["effect"]}；标记：{item["risk"]}。'
            out.append(f'| `{item["command"]}` | {item["use"]} | {detail} |')
        out.append("")
    return "\n".join(out)
