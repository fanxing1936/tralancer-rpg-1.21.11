# 潜行 + 副手有东西 = 解雇最近的自己人。
tag @s add rpg.sq.boss
tag @s add rpg.sq.firing
execute as @e[type=minecraft:husk,tag=rpg.squad,distance=..8] if score @s rpg_squad = #sq rpg_squad run tag @s add rpg.sq.pick
execute unless entity @e[type=minecraft:husk,tag=rpg.sq.pick,distance=..8] run function rpg:squad/none_near
execute as @e[type=minecraft:husk,tag=rpg.sq.pick,distance=..8,limit=1,sort=nearest] at @s run function rpg:squad/dismiss
tag @e[type=minecraft:husk,tag=rpg.sq.pick,distance=..8] remove rpg.sq.pick
tag @s remove rpg.sq.firing
tag @s remove rpg.sq.boss
