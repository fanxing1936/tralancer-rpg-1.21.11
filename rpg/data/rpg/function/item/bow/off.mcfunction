execute as @e[type=minecraft:arrow] on origin if entity @s[tag=rpg.h.dark_tag1] at @s run tag @e[type=arrow,distance=0..2] add dark
execute as @e[tag=dark] at @s run particle dust_color_transition{from_color:[0.19,0.05,0.33],to_color:[0.0,0.0,0.0],scale:1} ~0.1 ~0.1 ~0.1 -0.2 -0.2 -0.2 1 10
execute as @e[tag=dark] at @s if entity @e[distance=0..1] unless entity @a[distance=0..1,tag=rpg.h.dark_tag1] at @s run tag @e[distance=0..1,type=!arrow] add darkness
execute if entity @e[tag=darkness] run function rpg:item/bow/off/g0
execute as @e[tag=darkness,scores={dark=200..}] at @s run tag @s remove darkness
execute as @e[scores={dark=200..}] at @s run scoreboard players reset @s dark 



execute as @a[tag=rpg.h.projectiles_tag1] at @s run item modify entity @s weapon.mainhand rpg:item/bow/projectiles
