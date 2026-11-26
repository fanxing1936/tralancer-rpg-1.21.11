# 打开第 13 路径「女祭司」（as 玩家）
scoreboard players set @s rpg_ps_13 1
scoreboard players set @s rpg_pa_13 0
scoreboard players add #new rpg_pa 1
scoreboard players operation #s rpg_pa = @s rpg_dt_win
scoreboard players operation @s rpg_pb_13 = #s rpg_pa
