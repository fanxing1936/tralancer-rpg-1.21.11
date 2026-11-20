# 玩家打到了扫罗（as 玩家）。原版在这之后才把这一下记进伤害统计，所以这里只判定怎么算，下一刻再按增量结算。
advancement revoke @s only rpg:saul_boss/hit
scoreboard players set @s rpg_sl_v 0
tag @s add rpg.slb.att
execute as @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,distance=..24,limit=1,sort=nearest] at @s run function rpg:saul_boss/hit/unit
tag @s remove rpg.slb.att
execute if score @s rpg_sl_v matches 1.. run tag @s add rpg.slb.pend
