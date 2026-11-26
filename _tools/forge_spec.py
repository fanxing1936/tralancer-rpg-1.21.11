# -*- coding: utf-8 -*-
"""装备养成重置（docs/EQUIP-REWORK.md）的数据表。

这里只有表，没有逻辑：材料、六源、符文、符石、冶炼产物的基础数值、
掉落概率和旧数据换算。`add_forge.py` 读这些表写出数据包和资源包。
颜色全部从 rpg_ui_style 推出来，不写 Hex 字面量。
"""

import rpg_ui_style as ui

# ---------------------------------------------------------------------------
# 颜色
# ---------------------------------------------------------------------------
C_LABEL = ui.WHITE
C_BODY = ui.GRAY
C_MUTED = ui.MUTED
C_FORGE = ui.mix(ui.HOLY_DARK, ui.WARN, 0.35)          # [锻造] 材料前缀
C_GILD = ui.HOLY_DARK
C_HOLY = ui.PASSION
C_LV_MAX = ui.tier_colour("legend")
C_MELEE = ui.mix(ui.WARN, ui.HOLY_DARK, 0.45)          # 近战符文：赤铜
C_RANGED = ui.mix(ui.READY, ui.HOLY_DARK, 0.35)        # 远程符文：苔绿
C_ARMOR = ui.mix(ui.CYAN, ui.pillar("leviathan")["lit"], 0.5)
C_STONE = ui.RITUAL

QUALITY = [  # (上限, 名字, 颜色) —— q 是百分比偏移，-10..15
    (-6, "残次", ui.MUTED),
    (5, "普通", ui.GRAY),
    (10, "精良", ui.tier_colour("brave")),
    (15, "完美", ui.tier_colour("legend")),
]
Q_MIN, Q_MAX = -10, 15
LV_MAX = 10
XP_STEP = 20                 # 升到下一级需要 20 × 当前等级
XP_KILL = (1, 5, 50)         # 普通 / 精英（恶魔仆从等）/ boss
XP_STONE = 100               # 铸造之石
KILL_BOSS_TAGS = ["rpg.pope", "rpg.mkb", "rpg.jqb", "rpg.lub", "rpg.usb", "rpg.slb", "rpg.dtb"]
KILL_BOSS_TYPES = ["minecraft:wither", "minecraft:ender_dragon", "minecraft:elder_guardian", "minecraft:warden"]
KILL_ELITE_TAGS = ["rpg.demon", "rpg.demon.minion", "rpg.mkw", "rpg.jqd", "rpg.slg", "rpg.el"]   # rpg.el：世界精英（add_elites.py）
KILL_ELITE_TYPES = ["minecraft:ravager", "minecraft:evoker", "minecraft:piglin_brute", "minecraft:breeze"]

# ---------------------------------------------------------------------------
# 材料
# ---------------------------------------------------------------------------
# id -> (名字, 前缀, 前缀色, 两行说明)
MATERIALS = {
    "blank": ("器胚", "[锻造]", C_FORGE, ["未成形的暗铁坯料", "手持对准灵魂营火右键冶炼"]),
    "soul": ("残魂", "[锻造]", C_FORGE, ["冶炼时每多放一枚，品质多抽一次", "随冶炼自动从背包扣取"]),
    "forge_stone": ("铸造之石", "[锻造]", C_FORGE, ["副手拿装备，主手右键", "装备经验 +%d" % XP_STONE]),
    "wash_gem": ("洗炼钻", "[锻造]", C_FORGE, ["副手拿装备，主手右键", "重抽装备品质，新旧二选一"]),
    "gild_leaf": ("镀金箔", "[锻造]", C_FORGE, ["副手拿装备，主手右键", "随机一条附魔 +1 级，每件限一次"]),
}

# ---------------------------------------------------------------------------
# 六源
# ---------------------------------------------------------------------------
P = {p["slug"]: p for p in ui.PILLARS}
SOURCES = [
    # id, 名, 阵营, 名字色, 效果描述, 代价描述, 旧 weapon_tree 号
    dict(id="faith", name="信念", side="holy", colour=ui.PASSION, old=1,
         text="对亡灵与恶魔伤害 +25%", cost=""),
    dict(id="hope", name="希望", side="holy", colour=ui.HOLY_LIGHT, old=2,
         text="击杀回复 4 点生命并再生 3 秒", cost=""),
    dict(id="resolve", name="不屈", side="holy", colour=ui.HOLY, old=3,
         text="受击后 3 秒内下一击 +30%", cost=""),
    dict(id="malice", name="邪念", side="devil", colour=P["belial"]["lit"], old=4,
         text="伤害 +15%", cost="持有时缓慢累积魔化"),
    dict(id="hatred", name="仇恨", side="devil", colour=P["samael"]["lit"], old=5,
         text="连击同一目标每击 +5%，至多 +30%", cost="换目标时自损 1 点生命"),
    dict(id="pride", name="傲慢", side="devil", colour=P["lucifer"]["lit"], old=6,
         text="满血时伤害 +30%", cost="自身受到伤害 +15%"),
]
SOURCE_BOSS = {  # 源 -> (boss 生成器目录, 胜利时的中心标记；None 表示就地)
    "faith": ("pope_fight", None),
    "hope": ("michael_boss", "rpg.mkb.center"),
    "resolve": ("jacques_boss", "rpg.jqb.center"),
    "pride": ("lucifer_boss", "rpg.lub.center"),
    "malice": ("usurper_boss", "rpg.usb.center"),
    "hatred": ("saul_boss", "rpg.slb.center"),
}
BOSS_SOURCE_CHANCE = 0.30
HOLY_SOURCE_LV = 5           # 神圣之源的武器到这一级才算圣器
# 名字前的源图标（字体 rpg:forge_src 的码位）
SOURCE_GLYPH = {"faith": chr(0xE000), "hope": chr(0xE001), "resolve": chr(0xE002),
                "malice": chr(0xE003), "hatred": chr(0xE004), "pride": chr(0xE005)}
BOSS_STONE_CHANCE = 0.25

# ---------------------------------------------------------------------------
# 符文
# ---------------------------------------------------------------------------
# part: melee / ranged / armor
RUNES = [
    dict(id="ember", name="余烬", part="melee", text="连击同一目标叠灼痕，5 层引爆 6 点火焰伤害"),
    dict(id="echo", name="回响", part="melee", text="每第 4 击，0.5 秒后补一次 60% 回声斩"),
    dict(id="execute", name="处决", part="melee", text="对生命低于 25% 的目标伤害 +40%"),
    dict(id="backstab", name="背刺", part="melee", text="从目标背后命中伤害 +35%"),
    dict(id="bloodpact", name="血契", part="melee", text="自身每少 10% 生命，伤害 +4%，至多 +36%"),
    dict(id="poise", name="蓄势", part="melee", text="2 秒未出手后，下一击 +50% 并击退"),
    dict(id="hunt", name="追猎", part="ranged", text="箭矢命中标记目标 6 秒，你对它近战 +25%"),
    dict(id="split", name="裂矢", part="ranged", text="满蓄力的箭命中后分出 2 支弹向附近敌人"),
    dict(id="meteor", name="坠星", part="ranged", text="仰角大于 45° 的箭在落点引发冲击"),
    dict(id="recoil", name="反震", part="armor", text="受近战伤害后 1 秒内，下一击 +40%"),
    dict(id="lastbreath", name="余生", part="armor", text="生命跌到 3 点以下时抗性 V 2 秒，冷却 120 秒"),
    dict(id="stillwater", name="静水", part="armor", text="3 秒未受伤后获得 4 点吸收护盾"),
    dict(id="swift", name="疾行", part="armor", text="击杀后获得速度 II 3 秒"),
]
PART_NAME = {"melee": "近战武器", "ranged": "弓弩", "armor": "护甲"}
PART_COLOUR = {"melee": C_MELEE, "ranged": C_RANGED, "armor": C_ARMOR}

# ---------------------------------------------------------------------------
# 符石
# ---------------------------------------------------------------------------
STONES = [
    dict(id="rift", name="裂地", part="melee", text="向前方扇形打出冲击波，8 点伤害并击飞"),
    dict(id="frost", name="寒潮", part="melee", text="冻结周围 5 格内的敌人 2 秒"),
    dict(id="shadow", name="影步", part="melee", text="瞬移到 12 格内目标身后，下一击 +60%"),
    dict(id="blood", name="血祭", part="melee", text="献出当前生命的 20%，8 秒内攻击吸血 25%"),
    dict(id="gale", name="风墙", part="any", text="前方立起风墙 4 秒，推回敌人与投射物"),
    dict(id="volley", name="箭雨", part="ranged", text="准星落点降下 3 秒箭雨"),
    dict(id="banner", name="战旗", part="any", text="插下战旗 10 秒，6 格内友方力量 I 与抗性 I"),
]
STONE_COLOUR = {
    "rift": ui.mix(ui.HOLY_DARK, ui.WARN, 0.2), "frost": ui.CYAN, "shadow": ui.BROADCAST_VOID,
    "blood": ui.WARN, "gale": ui.CYAN_LIGHT, "volley": ui.READY, "banner": ui.HOLY,
}
ENERGY_MAX = 100
ENERGY = {"melee": 8, "ranged": 12, "hurt": 5}

# ---------------------------------------------------------------------------
# 魂火冶炼
# ---------------------------------------------------------------------------
TIERS = [  # key, 显示（None = 无档）, 主材 [(物品, 数量)]
    ("plain", None, [("iron_ingot", 6)]),
    ("brave", "brave", [("diamond", 4)]),
    ("epic", "epic", [("netherite_ingot", 1), ("diamond", 4)]),
]
TIER_MAT_NAME = {"iron_ingot": "铁锭", "diamond": "钻石", "netherite_ingot": "下界合金锭"}
SOUL_MAX = 3

# type, 名字, 种类, 每档的底材
SMELT_TYPES = [
    ("sword", "长剑", "melee", ("iron_sword", "diamond_sword", "netherite_sword")),
    ("axe", "战斧", "melee", ("iron_axe", "diamond_axe", "netherite_axe")),
    ("mace", "重锤", "melee", ("mace", "mace", "mace")),
    ("bow", "长弓", "ranged", ("bow", "bow", "bow")),
    ("crossbow", "劲弩", "ranged", ("crossbow", "crossbow", "crossbow")),
    ("head", "头盔", "armor", ("iron_helmet", "diamond_helmet", "netherite_helmet")),
    ("chest", "胸甲", "armor", ("iron_chestplate", "diamond_chestplate", "netherite_chestplate")),
    ("legs", "护腿", "armor", ("iron_leggings", "diamond_leggings", "netherite_leggings")),
    ("feet", "战靴", "armor", ("iron_boots", "diamond_boots", "netherite_boots")),
]
# 武器：(总伤害, 攻速)；护甲：(护甲, 韧性, 击退抗性)
MELEE_STATS = {
    "sword": ((6, 1.6), (7, 1.6), (8, 1.6)),
    "axe": ((9, 0.9), (10, 1.0), (11, 1.0)),
    "mace": ((7, 0.6), (8, 0.6), (9, 0.7)),
}
RANGED_ENCH = {"bow": "power", "crossbow": "quick_charge"}
ARMOR_STATS = {
    "head": ((2, 0, 0), (3, 2, 0), (3, 3, 0.1)),
    "chest": ((6, 0, 0), (8, 2, 0), (8, 3, 0.1)),
    "legs": ((5, 0, 0), (6, 2, 0), (6, 3, 0.1)),
    "feet": ((2, 0, 0), (3, 2, 0), (3, 3, 0.1)),
}
ARMOR_SLOT = {"head": "head", "chest": "chest", "legs": "legs", "feet": "feet"}
NAME_PREFIXES = ["锐利的", "千锤百炼的", "坚固的", "精制的", "骑兵的", "哨兵的", "老兵的", "无名的"]

# ---------------------------------------------------------------------------
# 掉落（docs/EQUIP-REWORK.md §12）
# ---------------------------------------------------------------------------
DROP_COMMON = {"soul": 0.05, "blank": 0.01}       # 七张自写的生物表
DROP_MINION = {"soul": 0.25, "rune": 0.04}        # 35 张恶魔仆从表

# ---------------------------------------------------------------------------
# 旧数据换算（§13）
# ---------------------------------------------------------------------------
OLD_RUNE_TO_NEW = {
    "damage_tag": "bloodpact", "blow_tag": "execute",
    "wilt_tag": "ember", "deep_tag": "backstab", "ink_tag": "execute", "sunder_tag": "poise",
    "projectiles_tag": "split", "dark_tag": "meteor", "pin_tag": "hunt",
    "health_tag": "lastbreath", "absorption_tag": "stillwater", "boom_tag": "recoil", "ebb_tag": "swift",
}
OLD_STONE_TO_NEW = {
    "sweep_tag": "rift", "wind_tag": "gale", "flame_tag": "blood",
    "tide_tag": "frost", "quake_tag": "rift", "shade_tag": "shadow",
}
OLD_MATERIAL_TO_NEW = [  # (旧 custom_data 判定, 新材料, 倍数)
    ("{echo_tag:1b}", "soul", 1),
    ("{echo_tag:2b}", "soul", 3),
    ("{fec_tag:1b}", "blank", 1),
    ("{embryo_tag:1b}", "blank", 1),
    ("{level_item:1b}", "forge_stone", 1),
    ("{diamond_tag:1b}", "wash_gem", 1),
    ("{gold_tag:1b}", "gild_leaf", 1),
    ("{enchant_tag:1b}", "gild_leaf", 1),
]
