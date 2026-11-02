# 收场：撤掉陈列、领主、圣卫和生命之树，不碰别的实体。
function promo:armory/clear
kill @e[type=minecraft:vindicator,tag=rpg.bz]
kill @e[type=minecraft:vindicator,tag=rpg.tg]
kill @e[tag=rpg.tg.part]
kill @e[tag=rpg.bz.part]
function rpg:ritual/life_tree/clear_all
tellraw @s {"text": "[宣传片] 场地已清空。", "color": "#D9C9A3"}
