execute unless entity @s[type=minecraft:armor_stand,tag=rpg.av] run return 0
execute if score @s rpg_av_anim matches 0 run scoreboard players set @s rpg_av_run 1
execute if score @s rpg_av_anim matches 1 run scoreboard players set @s rpg_av_run 1
execute if score @s rpg_av_anim matches 2 if score @s rpg_av_t matches ..97 run scoreboard players set @s rpg_av_run 1
