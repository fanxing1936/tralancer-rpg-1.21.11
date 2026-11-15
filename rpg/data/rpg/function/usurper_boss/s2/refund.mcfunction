# 有权无力：命令有人执行，他难以撼动
scoreboard players operation #hp rpg_ub += #lost rpg_ub
execute store result entity @s Health float 0.1 run scoreboard players get #hp rpg_ub
