# 驱魔熟练（原驱魔等级）：退出成长体系后按裁决次数算（add_sephira.py）
scoreboard players operation @s rpg_ex_prev = @s rpg_ex_lvl
scoreboard players add @s rpg_ex_rites 0
scoreboard players set @s rpg_ex_lvl 1
execute if score @s rpg_ex_rites matches 1.. run scoreboard players set @s rpg_ex_lvl 2
execute if score @s rpg_ex_rites matches 3.. run scoreboard players set @s rpg_ex_lvl 4
execute if score @s rpg_ex_rites matches 6.. run scoreboard players set @s rpg_ex_lvl 5
execute if score @s rpg_ex_lvl > @s rpg_ex_prev if score @s rpg_ex_prev matches 1.. run function rpg:inquest/career/level_up
execute if score @s rpg_ex_lvl > @s rpg_ex_prev if score @s rpg_ex_prev matches ..0 run function rpg:inquest/career/claim
scoreboard players operation @s rpg_ex_seen = @s rpg_ex_rites
