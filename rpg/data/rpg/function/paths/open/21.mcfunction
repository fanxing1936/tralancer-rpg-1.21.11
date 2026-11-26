# 打开第 21 路径「命运之轮」（as 玩家）
scoreboard players set @s rpg_ps_21 1
scoreboard players set @s rpg_pa_21 0
scoreboard players add #new rpg_pa 1
scoreboard players operation #s rpg_pa = @s rpg_vt_n
scoreboard players operation @s rpg_pb_21 = #s rpg_pa
