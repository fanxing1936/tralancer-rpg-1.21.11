# 收场：撤掉陈列、领主、圣卫和生命之树，不碰别的实体。
function promo:armory/clear
execute as @e[type=minecraft:vindicator,scores={rpg_dm_lord=4}] on passengers run kill @s
kill @e[type=minecraft:vindicator,scores={rpg_dm_lord=4}]
execute as @e[type=minecraft:vindicator,tag=rpg.tg] on passengers run kill @s
kill @e[type=minecraft:vindicator,tag=rpg.tg]
function rpg:ritual/life_tree/clear_all
tellraw @s {"text": "[宣传片] 场地已清空。", "color": "#D9C9A3"}
