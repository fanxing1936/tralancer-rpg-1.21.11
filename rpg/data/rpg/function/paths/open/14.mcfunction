# 打开第 14 路径「皇后」（as 玩家）
scoreboard players set @s rpg_ps_14 1
scoreboard players set @s rpg_pa_14 0
scoreboard players add #new rpg_pa 1
scoreboard players operation #s rpg_pa = @s rpg_pa_fg
scoreboard players operation @s rpg_pb_14 = #s rpg_pa
