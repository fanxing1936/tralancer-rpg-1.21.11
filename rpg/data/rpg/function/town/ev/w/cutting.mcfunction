execute as @a[tag=rpg.te.cut] at @s unless entity @e[tag=rpg.te.witch,distance=..3] run tag @s remove rpg.te.cut
execute if entity @a[tag=rpg.te.cut] run scoreboard players add #cut rpg_te 1
execute if score #cut rpg_te matches 3.. run function rpg:town/ev/w/freed
