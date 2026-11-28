$scoreboard players set #run rpg_te $(t)
$scoreboard players operation #kind rpg_te = #ev$(t) rpg_te
$scoreboard players set #es$(t) rpg_te 1
execute if score #kind rpg_te matches 0 run scoreboard players set #kind rpg_te 1
scoreboard players set #ph rpg_te 0
scoreboard players set #et rpg_te 0
scoreboard players set #tt rpg_te 0
tag @a remove rpg.tw.in
execute in minecraft:overworld as @e[type=minecraft:marker,tag=rpg.tw.c] if score @s rpg_tw_id = #run rpg_te at @s run function rpg:town/ev/begin_at
execute store result score #np rpg_te if entity @a[tag=rpg.tw.in]
execute if score #np rpg_te matches 0 run scoreboard players set #np rpg_te 1
bossbar set rpg:town_ev players @a[tag=rpg.tw.in]
bossbar set rpg:town_ev visible true
execute if score #kind rpg_te matches 1 run function rpg:town/ev/g/start
execute if score #kind rpg_te matches 2 run function rpg:town/ev/h/start
execute if score #kind rpg_te matches 3 run function rpg:town/ev/w/start
