# -*- coding: utf-8 -*-
"""世界怪物掉落表的数据（策划书「世界掉落、精英怪与锻造打通」第一步，用户 2026-11-23 拍板）。

全员冒险模式、没有挖矿、原版合成表禁用：锻造原料只能从怪物身上来，而且直接掉成品。
这里只有表；add_world_loot.py 写掉落表，add_drop_policy.py 把这些生物从「清空名单」里拿出来。
"""

# 锻造原料：(原版物品, 名字, 两行说明)。名字按 ART-STYLE §2.1 写成 [锻造]+本名；没有 custom_data，
# 锻造逻辑（clear …[!minecraft:custom_data]）照样认它们。
RAW = {
    "iron_ingot": ("铁锭", ["从怪物身上剥下的铁", "普通档冶炼的主材，每件 6 块"]),
    "gold_ingot": ("金锭", ["成色不纯的金", "可在锻造台换镀金箔，也能卖给商人"]),
    "gold_nugget": ("金粒", ["零碎的金屑", "玛门之柱的签约祭品"]),
    "diamond": ("钻石", ["坚硬的晶体", "勇者档冶炼的主材，每件 4 颗"]),
    "netherite_ingot": ("下界合金锭", ["地狱深处的合金", "史诗档、罪器与传说锻造都要用"]),
    "emerald": ("绿宝石", ["咒术师随身的宝石", "路西法之柱的签约祭品"]),
    "amethyst_shard": ("紫水晶碎片", ["节肢怪物甲壳里的晶屑", "贝利尔之柱的签约祭品"]),
}

# 组：(组名, 生物 → 原版产物, 原料 [(物品, 概率, 最少, 最多)], 残魂概率, 器胚概率, 货币概率)
# 原版产物：(物品, 名字, 最少, 最多, Lore 第一行的「X 的[Y]」中的 Y, 第二行)
GROUPS = {
    "undead": ("亡灵", {
        "zombie": [("rotten_flesh", "腐肉", 1, 3, "遗物", ("作为他们存在过的", "证据"))],
        "husk": [("rotten_flesh", "腐肉", 1, 3, "遗物", ("烈日也没能烧干的", "残躯"))],
        "drowned": [("rotten_flesh", "腐肉", 1, 3, "遗物", ("泡得发白的", "残躯"))],
        "zombie_villager": [("rotten_flesh", "腐肉", 1, 3, "遗物", ("曾经也是", "村民"))],
        "skeleton": [("bone", "骸骨", 1, 3, "骸骨", ("他们也是曾经的", "战士")),
                     ("arrow", "箭", 0, 2, "箭矢", ("射空了的", "箭"))],
        "stray": [("bone", "骸骨", 1, 3, "骸骨", ("冻在雪原里的", "旧兵")),
                  ("arrow", "箭", 0, 2, "箭矢", ("射空了的", "箭"))],
        "bogged": [("bone", "骸骨", 1, 3, "骸骨", ("沼泽里泡烂的", "旧兵")),
                   ("arrow", "箭", 0, 2, "箭矢", ("射空了的", "箭"))],
    }, [("iron_ingot", 0.25, 1, 1), ("gold_ingot", 0.03, 1, 1)], 0.05, 0.01, None),
    "arthropod": ("节肢", {
        "spider": [("string", "蛛丝", 0, 2, "丝", ("织网用的", "丝")), ("spider_eye", "蜘蛛眼", 0, 1, "眼", ("盯着你的", "眼"))],
        "cave_spider": [("string", "蛛丝", 0, 2, "丝", ("织网用的", "丝")), ("spider_eye", "蜘蛛眼", 0, 1, "眼", ("带毒的", "眼"))],
        "silverfish": [],
        "endermite": [],
    }, [("iron_ingot", 0.15, 1, 1), ("amethyst_shard", 0.20, 1, 2)], 0.04, 0.005, 0.10),
    "explosive": ("爆裂", {
        "creeper": [("gunpowder", "火药", 0, 1, "核心", ("他们为此而", "活"))],
    }, [("iron_ingot", 0.25, 1, 1)], 0.05, 0.01, None),
    "arcane": ("咒术", {
        "witch": [("redstone", "红石粉", 0, 2, "药渣", ("熬药剩下的", "粉末")), ("glowstone_dust", "荧石粉", 0, 2, "药渣", ("熬药剩下的", "粉末"))],
        "evoker": [],
        "vindicator": [],
        "pillager": [("arrow", "箭", 0, 2, "箭矢", ("弩上卸下的", "箭"))],
        "illusioner": [],
        "vex": [],
        "breeze": [("breeze_rod", "旋风棒", 1, 2, "核心", ("风被拧成的", "棒"))],
        "ravager": [],
    }, [("iron_ingot", 0.15, 1, 1), ("diamond", 0.02, 1, 1), ("emerald", 0.25, 1, 2)], 0.10, 0.02, 0.10),
    "nether": ("下界", {
        "blaze": [("blaze_powder", "烈焰粉", 0, 2, "余烬", ("烧不尽的", "火"))],
        "ghast": [("ghast_tear", "恶魂之泪", 0, 1, "泪", ("哭了几百年的", "泪")), ("gunpowder", "火药", 0, 2, "核心", ("它们也是", "火药桶"))],
        "magma_cube": [("magma_cream", "岩浆膏", 0, 1, "黏液", ("滚烫的", "黏液"))],
        "wither_skeleton": [("bone", "骸骨", 0, 2, "骸骨", ("焦黑的", "骨"))],
        "hoglin": [],
        "zoglin": [("rotten_flesh", "腐肉", 1, 3, "遗物", ("烂透了的", "兽肉"))],
        "zombified_piglin": [("rotten_flesh", "腐肉", 1, 2, "遗物", ("烂透了的", "猪灵"))],
        "piglin_brute": [],
    }, [("gold_nugget", 0.40, 2, 4), ("gold_ingot", 0.05, 1, 1), ("netherite_ingot", 0.005, 1, 1)], 0.08, 0.02, 0.10),
    "end": ("末地", {
        "enderman": [("ender_pearl", "末影珍珠", 0, 1, "眼珠", ("它们看着你的", "眼"))],
        "shulker": [("shulker_shell", "潜影壳", 0, 1, "壳", ("空了的", "壳"))],
        "phantom": [("phantom_membrane", "幻翼膜", 0, 1, "膜", ("夜里撕下的", "翼"))],
    }, [("diamond", 0.03, 1, 1), ("iron_ingot", 0.10, 1, 1)], 0.08, 0.02, 0.10),
    "water": ("水域", {
        "guardian": [("prismarine_shard", "海晶碎片", 0, 2, "鳞", ("守卫者的", "鳞")),
                     ("prismarine_crystals", "海晶砂粒", 0, 1, "砂", ("海底的", "砂"))],
        "elder_guardian": [("prismarine_shard", "海晶碎片", 0, 2, "鳞", ("远古守卫者的", "鳞")),
                           ("prismarine_crystals", "海晶砂粒", 0, 1, "砂", ("海底的", "砂"))],
    }, [("diamond", 0.02, 1, 1)], 0.06, 0.01, 0.10),
}

# 单独加成：凋灵骷髅下界合金 1.5%；远古守卫者必掉 2 颗钻石
EXTRA = {
    "wither_skeleton": [("netherite_ingot", 0.015, 1, 1)],
    "elder_guardian": [("diamond", 1.0, 2, 2)],
}

# 生物名（Lore 第一行「X 的[…]」）
MOB_NAME = {
    "zombie": "僵尸", "husk": "尸壳", "drowned": "溺尸", "zombie_villager": "僵尸村民", "skeleton": "骷髅",
    "stray": "流浪者", "bogged": "沼骸", "spider": "蜘蛛", "cave_spider": "洞穴蜘蛛", "silverfish": "蠹虫",
    "endermite": "末影螨", "creeper": "苦力怕", "witch": "女巫", "evoker": "唤魔者", "vindicator": "卫道士",
    "pillager": "掠夺者", "illusioner": "幻术师", "vex": "恼鬼", "breeze": "旋风人", "ravager": "劫掠兽",
    "blaze": "烈焰人", "ghast": "恶魂", "magma_cube": "岩浆怪", "wither_skeleton": "凋灵骷髅", "hoglin": "疣猪兽",
    "zoglin": "僵尸疣猪兽", "zombified_piglin": "僵尸猪灵", "piglin_brute": "猪灵蛮兵", "enderman": "末影人",
    "shulker": "潜影贝", "phantom": "幻翼", "guardian": "守卫者", "elder_guardian": "远古守卫者",
}

WORLD_TABLES = sorted(m for _g, (_n, mobs, *_r) in GROUPS.items() for m in mobs)

# 生物英文名（名牌用花体英文，用户 2026-11-24「生物的名字都用英语」）
MOB_EN = {
    "zombie": "Zombie", "husk": "Husk", "drowned": "Drowned", "zombie_villager": "Zombie Villager", "skeleton": "Skeleton",
    "stray": "Stray", "bogged": "Bogged", "spider": "Spider", "cave_spider": "Cave Spider", "silverfish": "Silverfish",
    "endermite": "Endermite", "creeper": "Creeper", "witch": "Witch", "evoker": "Evoker", "vindicator": "Vindicator",
    "pillager": "Pillager", "illusioner": "Illusioner", "vex": "Vex", "breeze": "Breeze", "ravager": "Ravager",
    "blaze": "Blaze", "ghast": "Ghast", "magma_cube": "Magma Cube", "wither_skeleton": "Wither Skeleton", "hoglin": "Hoglin",
    "zoglin": "Zoglin", "zombified_piglin": "Zombified Piglin", "piglin_brute": "Piglin Brute", "enderman": "Enderman",
    "shulker": "Shulker", "phantom": "Phantom", "guardian": "Guardian", "elder_guardian": "Elder Guardian",
}
