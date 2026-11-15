# 一条荆棘线（as 玩家）：从树根出发，朝这名玩家此刻的方向
execute at @e[type=minecraft:vindicator,tag=rpg.lub,limit=1,sort=nearest] facing entity @s feet rotated ~ 0 run function rpg:lucifer_boss/fs/thorn/root
