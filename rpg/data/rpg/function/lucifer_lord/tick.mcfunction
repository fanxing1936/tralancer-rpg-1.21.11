execute as @e[tag=rpg.lu,tag=rpg.lu.phase2] at @s run function rpg:lucifer_lord/undress
execute as @e[type=minecraft:vindicator,tag=rpg.advent,tag=!rpg.lu,tag=!rpg.lu.phase2,scores={rpg_dm_lord=1}] at @s run function rpg:lucifer_lord/dress
# 最终 Boss 路西法（add_lucifer_boss.py）
execute as @e[type=minecraft:vindicator,tag=rpg.lub,tag=!rpg.lu,tag=!rpg.lu.phase2] at @s run function rpg:lucifer_lord/dress
execute as @e[type=minecraft:vindicator,tag=rpg.lu,tag=!rpg.lu.phase2] at @s run function rpg:lucifer_lord/follow
execute as @e[type=minecraft:item_display,tag=rpg.lu.part] unless predicate rpg:lucifer_lord/riding at @s run function rpg:lucifer_lord/orphan
