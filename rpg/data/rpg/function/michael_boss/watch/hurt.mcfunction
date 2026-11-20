# 玩家打到了守望者（as 玩家）：三成机会，它传送走
advancement revoke @s only rpg:michael_boss/hit_watch
execute as @e[type=minecraft:vindicator,tag=rpg.mkb.w,distance=..8,limit=1,sort=nearest] unless score @s rpg_mk_ws matches 1..2 if predicate rpg:michael_boss/flee at @s run function rpg:michael_boss/watch/flee
