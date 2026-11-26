# 每盏灯（as/at 灯）：rpg_dt_lt 亮着的剩余刻，rpg_dt_pcd 冷却
execute if score @s rpg_dt_lt matches 1.. run function rpg:daath_fight/lamp/burn
execute if score @s rpg_dt_pcd matches 1.. run scoreboard players remove @s rpg_dt_pcd 1
scoreboard players set #hit rpg_dt 0
execute if data entity @s attack run scoreboard players set #hit rpg_dt 1
execute if data entity @s interaction run scoreboard players set #hit rpg_dt 1
execute if score #hit rpg_dt matches 0 run return 0
data remove entity @s attack
data remove entity @s interaction
execute if score @s rpg_dt_lt matches 1.. run return 0
execute if score @s rpg_dt_pcd matches 1.. run return run playsound minecraft:block.candle.fall block @a[distance=..16] ~ ~2 ~ 1 0.6
execute store result score #on rpg_dt if entity @e[type=minecraft:marker,tag=rpg.dt.pool,distance=..60]
execute if score #on rpg_dt matches 2.. run return run playsound minecraft:block.candle.fall block @a[distance=..16] ~ ~2 ~ 1 0.6
function rpg:daath_fight/lamp/lit
