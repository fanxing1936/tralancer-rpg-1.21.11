execute as @e[type=minecraft:vindicator,tag=rpg.mis,tag=!rpg.michael_spirit.carrier] at @s run function rpg:michael_spirit/undress
execute as @e[type=minecraft:vindicator,tag=rpg.michael_spirit.carrier,tag=!rpg.mis] at @s run function rpg:michael_spirit/dress
execute as @e[type=minecraft:vindicator,tag=rpg.michael_spirit.carrier,tag=rpg.mis] at @s run function rpg:michael_spirit/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.mis.part,predicate=!rpg:michael_spirit/riding,limit=1] run kill @e[type=minecraft:item_display,tag=rpg.mis.part,predicate=!rpg:michael_spirit/riding]
