execute if entity @s[type=minecraft:armor_stand,tag=rpg.av] at @s run return run function rpg:arch_visage/internal/resume
execute as @e[type=minecraft:armor_stand,tag=rpg.av,distance=..32,sort=nearest,limit=1] at @s run function rpg:arch_visage/internal/resume
