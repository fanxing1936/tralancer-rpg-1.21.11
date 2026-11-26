# 打开第 25 路径「节制」（as 玩家）
scoreboard players set @s rpg_ps_25 1
scoreboard players set @s rpg_pa_25 0
scoreboard players add #new rpg_pa 1
scoreboard players operation #s rpg_pa = @s rpg_alc_made
scoreboard players operation @s rpg_pb_25 = #s rpg_pa
