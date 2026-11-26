# 打开第 16 路径「教皇」（as 玩家）
scoreboard players set @s rpg_ps_16 1
scoreboard players set @s rpg_pa_16 0
scoreboard players add #new rpg_pa 1
scoreboard players operation #s rpg_pa = @s rpg_ex_rites
scoreboard players operation @s rpg_pb_16 = #s rpg_pa
