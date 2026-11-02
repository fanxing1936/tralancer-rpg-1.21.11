# 圣卫每刻入口：场上没有圣卫就只剩这两条带类型的存在性判定。
execute if entity @e[type=minecraft:vindicator,tag=rpg.tg,limit=1] as @e[type=minecraft:vindicator,tag=rpg.tg] at @s run function rpg:tower_guard/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.tg.part,predicate=!rpg:tower_guard/riding,limit=1] run function rpg:tower_guard/orphans
