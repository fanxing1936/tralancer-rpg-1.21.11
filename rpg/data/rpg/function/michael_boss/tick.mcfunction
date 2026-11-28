execute unless score #fight rpg_mk matches 1 run return 0
execute as @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,predicate=!rpg:in_prologue] at @s run function rpg:michael_boss/arena
