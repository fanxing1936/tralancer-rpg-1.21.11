# 进行中（每秒）：参与者跟着走；超时就失败
scoreboard players add #et rpg_te 1
execute in minecraft:overworld as @e[type=minecraft:marker,tag=rpg.tw.c] if score @s rpg_tw_id = #run rpg_te at @s run tag @a[distance=..110,gamemode=!spectator] add rpg.tw.in
bossbar set rpg:town_ev players @a[tag=rpg.tw.in]
execute if score #et rpg_te matches 900.. run return run function rpg:town/ev/fail
execute if score #kind rpg_te matches 1 run function rpg:town/ev/g/step
execute if score #kind rpg_te matches 2 run function rpg:town/ev/h/step
execute if score #kind rpg_te matches 3 run function rpg:town/ev/w/step
