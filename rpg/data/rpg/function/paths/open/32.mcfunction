# 打开第 32 路径「世界」（as 玩家）
scoreboard players set @s rpg_ps_32 1
scoreboard players set @s rpg_pa_32 0
scoreboard players add #new rpg_pa 1
scoreboard players operation #s rpg_pa = @s rpg_pa_wk
scoreboard players operation #s rpg_pa /= #100 rpg_pa
scoreboard players operation @s rpg_pb_32 = #s rpg_pa
