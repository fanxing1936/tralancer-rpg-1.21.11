
execute store result score @s random run random value 1..5
execute if score @s random matches 1 run effect give @e[tag=rpg.legacy.advanced_target,limit=1] wither 5 3 true
execute if score @s random matches 1 run function rpg:effect/pseudo_explosion/owned_p3
execute if score @s random matches 1 run effect give @s resistance 2 3 true
execute if score @s random matches 1 run particle gust_emitter_small ~ ~1 ~ 0.6 0.6 0.6 0.1 8
execute if score @s random matches 2 run effect give @s instant_health 1 1 true
execute if score @s random matches 2 run particle totem_of_undying ~ ~1 ~ 0.8 0.8 0.8 0.2 28
execute if score @s random matches 3 run effect give @e[tag=rpg.legacy.advanced_target,limit=1] slowness 3 4 true
execute if score @s random matches 3 run particle enchant ~ ~1 ~ 0.8 0.8 0.8 0.2 28
effect give @e[tag=rpg.legacy.advanced_target,limit=1] wind_charged 6 2 true
particle dust_color_transition{from_color:[1.0,0.35,0.0],to_color:[1.0,1.0,1.0],scale:3} ~ ~1 ~ 0.8 0.8 0.8 0.15 20
damage @e[tag=rpg.legacy.advanced_target,limit=1] 4 minecraft:player_attack by @s
scoreboard players reset @s random
scoreboard players reset @s wukong
