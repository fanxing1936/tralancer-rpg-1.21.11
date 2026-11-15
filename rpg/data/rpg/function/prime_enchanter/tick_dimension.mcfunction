execute as @e[distance=0..,type=minecraft:vindicator,tag=rpg.prime_enchanter] at @s run function rpg:prime_enchanter/follow
execute if entity @e[distance=0..,type=minecraft:item_display,tag=rpg.prime_enchanter.part,predicate=!rpg:prime_enchanter/riding,limit=1] run kill @e[distance=0..,type=minecraft:item_display,tag=rpg.prime_enchanter.part,predicate=!rpg:prime_enchanter/riding]
