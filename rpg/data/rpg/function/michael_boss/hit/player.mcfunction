# 玩家打到了米迦勒（as 玩家）。原版在这之后才记伤害统计，所以这里只判定怎么算，下一刻再按增量结算。
advancement revoke @s only rpg:michael_boss/hit
scoreboard players set @s rpg_mk_v 0
tag @s add rpg.mkb.att
execute as @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,distance=..24,limit=1,sort=nearest] at @s run function rpg:michael_boss/hit/unit
tag @s remove rpg.mkb.att
execute if score @s rpg_mk_v matches 1.. run tag @s add rpg.mkb.pend
