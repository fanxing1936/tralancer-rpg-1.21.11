# 打开第 18 路径「战车」（as 玩家）
scoreboard players set @s rpg_ps_18 1
scoreboard players set @s rpg_pa_18 0
scoreboard players add #new rpg_pa 1
scoreboard players operation #s rpg_pa = @s rpg_pa_sp
scoreboard players operation #s rpg_pa /= #100 rpg_pa
scoreboard players operation @s rpg_pb_18 = #s rpg_pa
scoreboard players operation @s rpg_pb_18 = @s rpg_pl_best
