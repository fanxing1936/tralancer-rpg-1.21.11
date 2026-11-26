# 打开第 27 路径「塔」（as 玩家）
scoreboard players set @s rpg_ps_27 1
scoreboard players set @s rpg_pa_27 0
scoreboard players add #new rpg_pa 1
scoreboard players operation @s rpg_pb_27 = @s rpg_pl_best
