# 打开第 31 路径「审判」（as 玩家）
scoreboard players set @s rpg_ps_31 1
scoreboard players set @s rpg_pa_31 0
scoreboard players add #new rpg_pa 1
scoreboard players operation #s rpg_pa = @s rpg_ex_rites
scoreboard players operation @s rpg_pb_31 = #s rpg_pa
