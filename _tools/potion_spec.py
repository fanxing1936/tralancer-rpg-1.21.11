# -*- coding: utf-8 -*-
"""药水与制器的数据表（策划书「药水、遗物与器物纹理」，用户 2026-11-24 全部按建议）。

POTIONS：键 → (名, 档, 用法, 颜色, 原版效果 [(id, 刻, 等级-1)], 特效函数 or None, 效果一行, 题记 [[片段…]], 配方 [(原版物品, 数)], 特殊材料 or None)
题记片段是 (文字, 是否高亮)。前 8 种是作者原来的药水，效果与题记不动。
"""
import rpg_ui_style as ui

TIER = {"brave": ("勇者", 1, 0, 16, 8), "epic": ("史诗", 3, 1, 8, 15), "legend": ("传说", 5, 3, 4, 60)}  # 名, 原质门槛, 残魂, 堆叠, 共用冷却秒
USE = {"drink": ("potion", "饮用"), "throw": ("splash_potion", "投掷"), "linger": ("lingering_potion", "滞留")}
H, _ = True, False

POTIONS = {
    "blood": ("精血药水", "brave", "throw", 16728576, [("instant_health", 1, 1)], None, "瞬间治疗 II",
              [[("精血炼制的", _), ("药水", H)], [("快速", _), ("回血", H)]], [("rotten_flesh", 8), ("spider_eye", 2)], None),
    "decay": ("衰败药水", "brave", "linger", 4673362, [("wither", 120, 2)], None, "凋零 III，6 秒",
              [[("恶毒的魔药", _)], [("投掷造成", _), ("凋零效果", H)]], [("rotten_flesh", 6), ("gunpowder", 4)], None),
    "beast": ("动物朋友", "brave", "drink", 63450, [("conduit_power", 600, 1), ("dolphins_grace", 600, 1)], None, "潮涌能量 II、海豚的恩惠 II，30 秒",
              [[("这个世界不光属于我们", _)], [("还属于我和我的动物朋友，", _), ("芝士雪豹", H)]], [("prismarine_shard", 4), ("prismarine_crystals", 2)], None),
    "soothe": ("镇痛药水", "brave", "drink", 0xF2A6B8, [("regeneration", 200, 1)], None, "生命恢复 II，10 秒",
               [[("裹在布里的", _), ("草药", H)]], [("string", 6), ("rotten_flesh", 6)], None),
    "fireproof": ("抗火药水", "brave", "drink", 0xE38B2C, [("fire_resistance", 2400, 0)], None, "抗火，2 分钟",
                  [[("从火里取来的", _), ("壳", H)]], [("magma_cream", 2), ("blaze_powder", 2)], None),
    "cleanse": ("净口药水", "brave", "drink", 0xE8F4F0, [], "cleanse", "清掉身上全部负面效果",
                [[("漱一口，", _), ("什么都吐出来", H)]], [("bone", 8), ("glowstone_dust", 4)], None),
    "venom": ("剧毒药水", "brave", "throw", 0x5FA832, [("poison", 200, 1)], None, "中毒 II，10 秒",
              [[("毒牙里挤出来的", _), ("汁", H)]], [("spider_eye", 4), ("redstone", 4)], None),
    "revive": ("复生药水", "epic", "throw", 16722944, [("instant_health", 1, 3)], None, "瞬间治疗 IV",
               [[("秘制的配方", _)], [("获得", _), ("大幅回血", H)]], [("ghast_tear", 1), ("prismarine_crystals", 3)], None),
    "shield": ("护盾药水", "epic", "throw", 16763904, [("absorption", 1200, 4)], None, "伤害吸收 V，60 秒",
               [[("守护他人的力量", _)], [("获得", _), ("伤害吸收护盾", H)]], [("shulker_shell", 1), ("bone", 8)], None),
    "fatigue": ("疲惫药水", "epic", "throw", 7733497, [("darkness", 600, 1), ("nausea", 600, 1), ("slowness", 600, 2)], None,
                "黑暗、反胃、缓慢 III，30 秒", [[("放大敌人的弱点", _)], [("恶魔", H), ("亲自炼制的", _), ("邪恶药水", H)]],
                [("phantom_membrane", 2), ("spider_eye", 3)], None),
    "vigor": ("体能药水", "epic", "drink", 5107200, [("speed", 600, 1), ("jump_boost", 600, 1)], None, "速度 II、跳跃提升 II，30 秒",
              [[("强化", _), ("体能", H), ("的神秘魔药", _)], [("劝诫人们", _), ("强健身体", H)]], [("breeze_rod", 1), ("string", 6)], None),
    "stone": ("石肤药水", "epic", "drink", 0x9A9A94, [("resistance", 300, 1), ("slowness", 300, 0)], None, "抗性提升 II、缓慢 I，15 秒",
              [[("皮肤一寸寸变成", _), ("石头", H)]], [("prismarine_shard", 6), ("shulker_shell", 1)], None),
    "shadow": ("影行药水", "epic", "drink", 0x20263C, [("invisibility", 300, 0)], "shadow", "隐身 15 秒；第一下近战伤害 +50%，打出后现形",
               [[("影子先于你", _), ("到达", H)]], [("ender_pearl", 2), ("phantom_membrane", 1)], None),
    "blaze": ("烈焰药水", "epic", "drink", 0xF07818, [("fire_resistance", 300, 0)], "blaze", "15 秒内近战点燃目标，自己不怕火",
              [[("喝下去的是", _), ("火", H)]], [("blaze_powder", 4), ("gunpowder", 4)], None),
    "exorcise": ("驱邪药水", "epic", "drink", 0xFFF2A8, [], "exorcise", "魔化 −15；圣力者改为同化 −5",
                 [[("把里面的东西", _), ("请出去", H)]], [("glowstone_dust", 6), ("ghast_tear", 1)], None),
    "prayer": ("祷告药水", "epic", "drink", 0xFFD85A, [], "prayer", "圣力 +40、生命力 +15",
               [[("含着它念完", _), ("一段经文", H)]], [("glowstone_dust", 4), ("breeze_rod", 1)], None),
    "rite": ("血祭药水", "epic", "drink", 0x7A1030, [], "rite", "魔力 +50、魔化 +8",
             [[("别人的血，", _), ("你的力", H)]], [("redstone", 6), ("rotten_flesh", 8)], None),
    "frenzy": ("血战药水", "legend", "drink", 16755200, [("wither", 80, 4), ("strength", 600, 2)], None, "凋零 V 4 秒，力量 III 30 秒",
               [[("放手一搏吧！！！别顾虑太多", _)], [("扣除6滴", _), ("血量", H), ("并获得", _), ("力量三", H)]],
               [("blaze_powder", 6), ("redstone", 6)], "core"),
    "undying": ("不灭药水", "legend", "drink", 0x8FA088, [], "undying", "60 秒内撑住一次致命伤，并有 3 秒抗性 III",
                [[("坟里的人", _), ("不肯走", H)]], [("ghast_tear", 2), ("ender_pearl", 4)], "soil"),
    "lure": ("引潮药水", "legend", "drink", 0x1E3C78, [], "lure", "60 秒内，48 格里刷出的怪物精英机率 ×3",
             [[("潮水闻到了", _), ("血", H)]], [("breeze_rod", 2), ("phantom_membrane", 3)], "star"),
}

# 制器：键 → (名, give 函数, 配方 [(原版物品, 数)], 特殊材料 or None, 要求 ("sef"|"rites", 值))
RITES = {
    "doll": ("替死人偶", "alc/give/doll", [("string", 12), ("phantom_membrane", 2)], None, ("sef", 2)),
    "totem": ("驱魔图腾", "alc/give/totem", [("shulker_shell", 2), ("prismarine_shard", 8)], None, ("sef", 3)),
    "star": ("天启星", "alc/give/star", [("ender_pearl", 4)], "star", ("sef", 4)),
    "nail": ("银质圣钉", "inquest/give/nail", [("iron_nugget", 8), ("arrow", 4)], None, ("rites", 1)),
    "bell": ("告解铃", "inquest/give/bell", [("iron_nugget", 8), ("breeze_rod", 1)], None, ("rites", 1)),
    "incense": ("净罪香", "inquest/give/incense", [("blaze_powder", 4), ("glowstone_dust", 6)], None, ("rites", 1)),
    "lantern": ("封魔灯", "inquest/give/lantern", [("magma_cream", 4), ("glowstone_dust", 8)], None, ("rites", 1)),
    "chalk1": ("守御粉笔", "inquest/give/chalk1", [("bone", 16)], None, ("rites", 3)),
    "chalk2": ("压制粉笔", "inquest/give/chalk2", [("bone", 16)], None, ("rites", 3)),
    "chalk3": ("疾行粉笔", "inquest/give/chalk3", [("bone", 16)], None, ("rites", 3)),
}
# 圣水用空瓶，在炼药页做：键 → (名, 函数, 配方, 另要的东西 (谓词, 数, 名), 要求)
WATERS = {
    "holy": ("驱魔圣水", "alc/give/holy", [("ghast_tear", 1), ("prismarine_crystals", 4)], None, ("sef", 2)),
    "strong": ("浓缩驱魔圣水", "inquest/give/strong_water", [], ("*[minecraft:custom_data~{rite_tag:1b},!minecraft:custom_data~{rpg_strong_water:1b}]", 2, "驱魔圣水"), ("rites", 3)),
}


def item_name(item):
    import world_loot_spec as W
    if item in W.RELIC_MINION:
        return W.RELIC_MINION[item][0]
    for _g, (_n, mobs, *_r) in W.GROUPS.items():
        for ds in mobs.values():
            for d in ds:
                if d[0] == item:
                    return d[1]
    raise KeyError(item)


def seg(text, colour, bold=False):
    return {"text": text, "color": colour, "bold": bold, "italic": False}


def potion_components(key):
    """→ (物品 id, 组件 dict)"""
    name, tier, use, colour, effs, fnk, line, flavour, _rec, _sp = POTIONS[key]
    tname, _sef, _soul, stack, cd = TIER[tier]
    tag, tcol = "[%s]" % tname, ui.tier_colour(tier)
    rule = ["", seg(ui.RULE_TEXT, ui.WHITE)]
    lore = [rule] + [[""] + [seg(t, tcol if h else ui.GRAY, h) for t, h in row] for row in flavour]
    lore += [["", seg(USE[use][1] + "　", ui.MUTED), seg(line, ui.GRAY)], rule]
    comps = {
        "minecraft:custom_name": ["", seg(tag, tcol, True), seg(name, ui.WHITE)],
        "minecraft:lore": lore,
        "minecraft:potion_contents": {"custom_color": colour, "custom_effects": [
            {"id": "minecraft:" + e, "duration": d, "amplifier": a} for e, d, a in effs]},
        "minecraft:tooltip_display": {"hidden_components": ["minecraft:potion_contents"]},
        "minecraft:max_stack_size": stack,
        "minecraft:use_cooldown": {"seconds": float(cd), "cooldown_group": "rpg:potion_" + tier},
        "minecraft:custom_data": {"rpg_potion": key},
    }
    if use == "drink":
        comps["minecraft:use_remainder"] = {"id": "minecraft:paper", "count": 1, "components": vial_components()}
    return "minecraft:" + USE[use][0], comps


def material(tag, colour, name, lines, mat, model):
    rule = ["", seg(ui.RULE_TEXT, ui.WHITE)]
    return {
        "minecraft:custom_name": ["", seg(tag, colour, True), seg(name, ui.WHITE)],
        "minecraft:lore": [rule] + [["", seg(l, ui.GRAY)] for l in lines] + [rule],
        "minecraft:item_model": model,
        "minecraft:consumable": {"consume_seconds": 1234567.0, "animation": "none", "sound": "minecraft:intentionally_empty",
                                 "has_consume_particles": False},
        "minecraft:max_stack_size": 64,
        "minecraft:custom_data": {"rpg_fm": True, "rpg_mat": mat},
    }


def vial_components():
    return material("[药剂]", ui.GRAY_HEX if hasattr(ui, "GRAY_HEX") else "#AAAAAA", "空瓶",
                    ["手持对准灵魂营火右键炼药", "喝完饮用的药水会还一个"], "vial", "rpg:relic/empty_vial")


def blank_components():
    return material("[驱魔]", ui.HOLY, "空白圣具", ["还没刻字的圣具坯", "手持对准灵魂营火右键制器"], "blank_rite", "rpg:relic/blank_rite")
