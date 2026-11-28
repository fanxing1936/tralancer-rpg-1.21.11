execute if entity @a[tag=rpg.tw.in,distance=..3,gamemode=!spectator] run return run tp @s ~ ~ ~ facing entity @p[tag=rpg.tw.in] feet
execute unless entity @a[tag=rpg.tw.in,distance=..24,gamemode=!spectator] run return 0
execute facing entity @p[tag=rpg.tw.in] feet rotated ~ 0 positioned ^ ^ ^0.17 positioned over motion_blocking_no_leaves run tp @s ~ ~ ~ ~ 0
