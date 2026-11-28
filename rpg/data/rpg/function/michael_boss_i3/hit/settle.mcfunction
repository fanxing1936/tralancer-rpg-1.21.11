# 结算上一刻那一下（as 玩家）：增量 = 统计 - 上一刻的基准
tag @s remove rpg.mkb.pend
scoreboard players operation #dd rpg_mk_i3 = @s rpg_mk_dd
scoreboard players operation #dd rpg_mk_i3 -= @s rpg_mk_dd0
execute if score #dd rpg_mk_i3 matches ..0 run return 0
execute if score @s rpg_mk_v matches 3 as @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,distance=..24,limit=1,sort=nearest] run function rpg:michael_boss_i3/hit/extra
execute if score @s rpg_mk_v matches 4 run scoreboard players set #f rpg_mk_i3 3
execute if score @s rpg_mk_v matches 5 run scoreboard players set #f rpg_mk_i3 8
execute if score @s rpg_mk_v matches 4..5 as @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,distance=..24,limit=1,sort=nearest] run function rpg:michael_boss_i3/hit/refund
