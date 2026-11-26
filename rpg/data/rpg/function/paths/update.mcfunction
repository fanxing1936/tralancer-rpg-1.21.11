# 计数型与状态型试炼的进度（as 玩家）
execute if score @s rpg_ps_32 matches 1 run function rpg:paths/upd/32
execute if score @s rpg_ps_31 matches 1 run function rpg:paths/upd/31
execute if score @s rpg_ps_25 matches 1 run function rpg:paths/upd/25
execute if score @s rpg_ps_22 matches 1 run function rpg:paths/upd/22
execute if score @s rpg_ps_21 matches 1 run function rpg:paths/upd/21
execute if score @s rpg_ps_18 matches 1 run function rpg:paths/upd/18
execute if score @s rpg_ps_16 matches 1 run function rpg:paths/upd/16
execute if score @s rpg_ps_14 matches 1 run function rpg:paths/upd/14
execute if score @s rpg_ps_13 matches 1 run function rpg:paths/upd/13
execute if score @s rpg_ps_15 matches 1 run function rpg:paths/upd/15
execute if score @s rpg_ps_12 matches 1 run function rpg:paths/upd/12
execute if score @s rpg_ps_26 matches 1 if score @s rpg_pact matches 1.. unless score @s rpg_pact = @s rpg_pb_26 run scoreboard players set @s rpg_pa_26 300
execute if score @s rpg_ps_27 matches 1 if score @s rpg_pb_27 matches ..4 if score @s rpg_pl_best matches 5.. run scoreboard players set @s rpg_pa_27 1
execute if score @s rpg_ps_18 matches 1 if score @s rpg_pb_18 matches ..14 if score @s rpg_pl_best matches 15.. run scoreboard players set @s rpg_pa_18 3000
