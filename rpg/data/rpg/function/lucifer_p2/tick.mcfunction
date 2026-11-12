# Appearance only: no add/remove of the external phase signal.
function rpg:lucifer_p2/material/tick
execute as @e[type=minecraft:vindicator,tag=rpg.lu2,tag=!rpg.lu.phase2] at @s run function rpg:lucifer_p2/undress
execute as @e[type=minecraft:vindicator,tag=rpg.lu2] at @s unless score @s rpg_dm_lord matches 1 run function rpg:lucifer_p2/undress
execute as @e[type=minecraft:vindicator,scores={rpg_dm_lord=1},tag=rpg.lu.phase2,tag=!rpg.lu2] at @s run function rpg:lucifer_p2/dress
execute as @e[type=minecraft:vindicator,scores={rpg_dm_lord=1},tag=rpg.lu.phase2,tag=rpg.lu2] at @s run function rpg:lucifer_p2/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.lu2.part,predicate=!rpg:lucifer_p2/riding,limit=1] run function rpg:lucifer_p2/orphans
