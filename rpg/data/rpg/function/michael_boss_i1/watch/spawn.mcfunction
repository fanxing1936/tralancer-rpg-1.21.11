execute if score #pro rpg_mk_i1 matches 1 run return 0
# 一只守望者从场地边缘传送进来（at 中心）：随机方向 14 格外的地面
summon minecraft:marker ~ ~ ~ {Tags:["rpg.mkb.wspot"]}
execute as @e[type=minecraft:marker,tag=rpg.mkb.wspot,distance=0..] store result entity @s Rotation[0] float 1 run random value 0..359
execute as @e[type=minecraft:marker,tag=rpg.mkb.wspot,distance=0..] at @s rotated as @s positioned ^ ^ ^14 positioned over motion_blocking_no_leaves run function rpg:michael_boss_i1/watch/summon
kill @e[type=minecraft:marker,tag=rpg.mkb.wspot,distance=0..]
