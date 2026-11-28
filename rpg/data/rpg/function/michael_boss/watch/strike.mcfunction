# 挥臂（as/at 它）
execute positioned ^ ^ ^1.6 run tag @e[tag=rpg.unit.f,distance=..1.8] add rpg.mkb.hit
execute as @e[tag=rpg.unit,tag=rpg.mkb.hit,predicate=!rpg:in_prologue] run damage @s 6 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.mkb.w,limit=1,sort=nearest,predicate=!rpg:in_prologue]
tag @e[tag=rpg.unit,predicate=!rpg:in_prologue] remove rpg.mkb.hit
particle minecraft:sweep_attack ^ ^1.4 ^1.4 0.3 0.2 0.3 0 1
