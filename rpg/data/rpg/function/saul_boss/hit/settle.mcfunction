# 结算上一刻那一下（as 玩家）：增量 = 统计 - 上一刻的基准
tag @s remove rpg.slb.pend
scoreboard players operation #dd rpg_sl = @s rpg_sl_dd
scoreboard players operation #dd rpg_sl -= @s rpg_sl_dd0
execute if score #dd rpg_sl matches ..0 run return 0
execute if score @s rpg_sl_v matches 1..2 as @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,distance=..24,limit=1,sort=nearest] run function rpg:saul_boss/hit/refund
execute if score @s rpg_sl_v matches 3 as @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,distance=..24,limit=1,sort=nearest] run function rpg:saul_boss/hit/extra
