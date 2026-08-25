
execute store result score @s random run random value 1..10
execute if score @s random matches 1 run effect give @e[tag=rpg.legacy.advanced_target,limit=1] wither 10 4 true
execute if score @s random matches 1 run function rpg:effect/pseudo_explosion/owned_p2
execute if score @s random matches 1 run particle dust_color_transition{from_color:[1.0,0.36,0.83],to_color:[1.0,1.0,1.0],scale:1} ~ ~1 ~ 0.8 0.8 0.8 0.2 24
execute if score @s random matches 2 run effect give @e[tag=rpg.legacy.advanced_target,limit=1] wither 6 2 true
execute if score @s random matches 2 run particle soul_fire_flame ~ ~1 ~ 0.8 0.8 0.8 0.15 40
execute if score @s random matches 3 run effect give @e[tag=rpg.legacy.advanced_target,limit=1] slowness 4 4 true
execute if score @s random matches 3 run particle wax_off ~ ~1 ~ 0.8 0.8 0.8 0.2 36
execute if score @s random matches 4 at @e[tag=rpg.legacy.advanced_target,limit=1] run summon lightning_bolt
execute if score @s random matches 4 run particle soul ~ ~1 ~ 0.8 0.8 0.8 0.15 36
effect give @e[tag=rpg.legacy.advanced_target,limit=1] weakness 4 2 true
particle dust_color_transition{from_color:[1.0,0.36,0.83],to_color:[0.0,0.98,1.0],scale:2} ~ ~1 ~ 0.7 0.7 0.7 0.15 16
scoreboard players reset @s random
scoreboard players reset @s saber
