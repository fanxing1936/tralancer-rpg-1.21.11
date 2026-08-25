scoreboard players remove @s rpg_ex_ctime 1
particle wax_on ~ ~0.8 ~ 0.8 0.25 0.8 0.03 3 normal
execute if score @s rpg_ex_ctime matches ..0 run function rpg:inquest/counter/mammon_default
