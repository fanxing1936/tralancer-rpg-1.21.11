
scoreboard players add @s sakura_step 1
execute if score @s sakura_step matches 5.. run scoreboard players set @s sakura_step 1
execute if score @s sakura_step matches 1 run effect give @e[tag=rpg.legacy.advanced_target,limit=1] levitation 1 1 true
execute if score @s sakura_step matches 2 run effect give @e[tag=rpg.legacy.advanced_target,limit=1] slowness 3 3 true
execute if score @s sakura_step matches 3 run effect give @s instant_health 1 1 true
execute if score @s sakura_step matches 4 run damage @e[tag=rpg.legacy.advanced_target,limit=1] 9 minecraft:magic by @s
execute if score @s sakura_step matches 4 run effect give @e[tag=rpg.legacy.advanced_target,limit=1] darkness 3 0 true
execute if score @s sakura_step matches 4 run function rpg:hud/m16
particle dust_color_transition{from_color:[0.4,0.0,1.0],to_color:[0.0,0.0,0.0],scale:2} ~ ~1 ~ 0.7 0.7 0.7 0.12 18
execute if entity @s[tag=rpg.e.offhand_sakura_tag1] run particle sweep_attack ~ ~1 ~ 0.5 0.5 0.5 0.1 8
scoreboard players reset @s sakura
