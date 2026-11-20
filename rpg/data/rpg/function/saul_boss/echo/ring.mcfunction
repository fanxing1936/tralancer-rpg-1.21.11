# 三个残影（at 玩家）：120° 一个，5 格外，朝着玩家
execute rotated as @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1] rotated ~0 0 positioned ^ ^ ^-5 facing entity @e[tag=rpg.unit.ns,sort=nearest,limit=1] feet rotated ~ 0 run function rpg:saul_boss/echo/one
execute rotated as @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1] rotated ~120 0 positioned ^ ^ ^-5 facing entity @e[tag=rpg.unit.ns,sort=nearest,limit=1] feet rotated ~ 0 run function rpg:saul_boss/echo/one
execute rotated as @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1] rotated ~240 0 positioned ^ ^ ^-5 facing entity @e[tag=rpg.unit.ns,sort=nearest,limit=1] feet rotated ~ 0 run function rpg:saul_boss/echo/one
