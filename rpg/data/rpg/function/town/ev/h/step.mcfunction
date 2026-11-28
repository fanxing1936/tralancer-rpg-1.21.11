# 每秒：救人、清点
execute as @e[type=minecraft:villager,tag=rpg.te.taken] at @s if entity @a[tag=rpg.tw.in,distance=..3] run function rpg:town/ev/h/rescued
execute as @e[type=minecraft:villager,tag=rpg.te.taken] at @s run particle minecraft:soul ~ ~1 ~ 0.3 0.4 0.3 0.01 4
execute in minecraft:overworld as @e[type=minecraft:marker,tag=rpg.tw.c] if score @s rpg_tw_id = #run rpg_te at @s as @e[tag=rpg.te.hol,distance=..5] run function rpg:town/ev/h/reached
execute if score #reach rpg_te matches 6.. run return run function rpg:town/ev/fail
execute store result score #left rpg_te if entity @e[tag=rpg.te.hol]
execute if score #left rpg_te matches 0 if score #wave rpg_te matches ..2 run return run function rpg:town/ev/h/wave
execute if score #left rpg_te matches 0 if score #wave rpg_te matches 3 run function rpg:town/ev/h/dawn
