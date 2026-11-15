execute if entity @s[type=minecraft:armor_stand,tag=rpg.he] at @s run return run function rpg:heart_of_ender/anim/enter/death
execute as @e[type=minecraft:armor_stand,tag=rpg.he,distance=..32,sort=nearest,limit=1] at @s run function rpg:heart_of_ender/anim/enter/death
