# 重盾每刻入口。
execute if entity @e[type=minecraft:vindicator,tag=rpg.rg,limit=1] as @e[type=minecraft:vindicator,tag=rpg.rg] at @s run function rpg:royal_guard/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.rg.part,predicate=!rpg:royal_guard/riding,limit=1] run function rpg:royal_guard/orphans
