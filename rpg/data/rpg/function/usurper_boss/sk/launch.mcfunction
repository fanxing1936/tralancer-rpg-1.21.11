execute if score @s rpg_ub_t matches 20 at @e[tag=rpg.unit.f,distance=..25,sort=random,limit=1] run function rpg:usurper_boss/launch/mark
execute if score @s rpg_ub_t matches 20 unless entity @e[type=minecraft:marker,tag=rpg.usb.land] run function rpg:usurper_boss/launch/mark
execute if score @s rpg_ub_t matches 23 run data merge entity @s {Invulnerable:1b,NoGravity:1b}
execute if score @s rpg_ub_t matches 23 at @s run tp @s ~ ~14 ~
execute if score @s rpg_ub_t matches 43 at @e[type=minecraft:marker,tag=rpg.usb.land,limit=1] run tp @s ~ ~ ~
execute if score @s rpg_ub_t matches 44 at @s run function rpg:usurper_boss/launch/land
execute if score @s rpg_ub_t matches 79.. run function rpg:usurper_boss/sk/end
