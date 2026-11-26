# 打开第 22 路径「正义」（as 玩家）
scoreboard players set @s rpg_ps_22 1
scoreboard players set @s rpg_pa_22 0
scoreboard players add #new rpg_pa 1
scoreboard players operation #s rpg_pa = @s rpg_bt_total
scoreboard players operation @s rpg_pb_22 = #s rpg_pa
