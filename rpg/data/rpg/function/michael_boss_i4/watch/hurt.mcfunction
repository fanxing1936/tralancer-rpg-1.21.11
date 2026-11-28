execute unless entity @s[tag=rpg.pri4] run return run advancement revoke @s only rpg:michael_boss_i4/hit_watch
# 玩家打到了守望者（as 玩家）：三成机会，它传送走
advancement revoke @s only rpg:michael_boss_i4/hit_watch
execute as @e[type=minecraft:vindicator,tag=rpg.mkb.w,distance=..8,limit=1,sort=nearest] unless score @s rpg_mk_ws matches 1..2 if predicate rpg:michael_boss_i4/flee at @s run function rpg:michael_boss_i4/watch/flee
