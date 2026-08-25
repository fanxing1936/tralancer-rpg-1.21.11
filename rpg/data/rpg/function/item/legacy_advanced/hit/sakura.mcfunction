
scoreboard players add @s sakura_step 1
execute if score @s sakura_step matches 5.. run scoreboard players set @s sakura_step 1
execute if score @s sakura_step matches 1 run particle sweep_attack ~ ~1 ~ 0.6 0.6 0.6 0.1 14
execute if score @s sakura_step matches 2 run particle dust_pillar{block_state:{Name:cherry_leaves}} ~ ~1 ~ 0.7 0.7 0.7 0.12 24
execute if score @s sakura_step matches 2 run effect give @e[tag=rpg.legacy.advanced_target,limit=1] wind_charged 3 1 true
execute if score @s sakura_step matches 3 run particle cherry_leaves ~ ~1.3 ~ 0.8 0.8 0.8 0.15 28
execute if score @s sakura_step matches 3 run effect give @s instant_health 1 0 true
execute if score @s sakura_step matches 4 run particle dust_color_transition{from_color:[1.0,0.47,0.47],to_color:[1.0,1.0,1.0],scale:3} ~ ~1 ~ 0.9 0.9 0.9 0.15 40
execute if score @s sakura_step matches 4 run damage @e[tag=rpg.legacy.advanced_target,limit=1] 8 minecraft:player_attack by @s
execute if score @s sakura_step matches 4 at @e[tag=rpg.legacy.advanced_target,limit=1] run summon lightning_bolt
execute if score @s sakura_step matches 4 run effect give @s resistance 1 3 true
execute if score @s sakura_step matches 4 run function rpg:hud/m17
particle cherry_leaves ~ ~1.2 ~ 0.45 0.7 0.45 0.08 7
damage @e[tag=rpg.legacy.advanced_target,limit=1] 2 minecraft:player_attack by @s
scoreboard players reset @s sakura
