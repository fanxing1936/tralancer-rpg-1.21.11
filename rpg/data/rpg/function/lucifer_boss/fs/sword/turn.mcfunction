# 剑转一格（as/at 剑）：每刻 6°，一圈 60 刻；扫到的人挨一下
tp @s ~ ~ ~ ~6 0
tag @e[type=minecraft:vindicator,tag=rpg.lub,limit=1,sort=nearest] add rpg.dm.cast
execute rotated as @s run function rpg:lucifer_boss/fs/sword/reach
tag @e[type=minecraft:vindicator,tag=rpg.lub] remove rpg.dm.cast
execute rotated as @s positioned ^ ^ ^8.5 run particle minecraft:flame ~ ~ ~ 1 0.3 1 0.02 6
execute rotated as @s positioned ^ ^ ^13 run particle minecraft:lava ~ ~ ~ 0.3 0.2 0.3 0 1
