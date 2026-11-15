execute unless entity @s[type=minecraft:armor_stand,tag=rpg.he] run return 0
execute if score @s rpg_he_anim matches 0 run scoreboard players set @s rpg_he_run 1
execute if score @s rpg_he_anim matches 1 run scoreboard players set @s rpg_he_run 1
execute if score @s rpg_he_anim matches 2 if score @s rpg_he_t matches ..79 run scoreboard players set @s rpg_he_run 1
execute if score @s rpg_he_anim matches 3 if score @s rpg_he_t matches ..79 run scoreboard players set @s rpg_he_run 1
execute if score @s rpg_he_anim matches 4 if score @s rpg_he_t matches ..39 run scoreboard players set @s rpg_he_run 1
execute if score @s rpg_he_anim matches 5 if score @s rpg_he_t matches ..47 run scoreboard players set @s rpg_he_run 1
execute if score @s rpg_he_anim matches 6 if score @s rpg_he_t matches ..79 run scoreboard players set @s rpg_he_run 1
