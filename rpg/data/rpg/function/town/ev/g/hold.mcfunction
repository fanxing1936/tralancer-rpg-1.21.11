# 守阵（每秒）：蝇群靠近法阵就掉稳定度，有人站在法阵里回一点
scoreboard players add #tt rpg_te 1
execute as @e[type=minecraft:marker,tag=rpg.te.cm] at @s store result score #near rpg_te if entity @e[tag=rpg.te.fly,distance=..4]
scoreboard players operation #stab rpg_te -= #near rpg_te
execute as @e[type=minecraft:marker,tag=rpg.te.cm] at @s if entity @a[tag=rpg.tw.in,distance=..3] run scoreboard players add #stab rpg_te 1
execute if score #stab rpg_te matches 101.. run scoreboard players set #stab rpg_te 100
execute store result bossbar rpg:town_ev value run scoreboard players get #stab rpg_te
execute as @e[type=minecraft:marker,tag=rpg.te.cm] at @s run particle minecraft:dust{color:[1.0,0.85,0.35],scale:1.0} ~ ~0.2 ~ 1.6 0.05 1.6 0 14
scoreboard players operation #m rpg_te = #tt rpg_te
scoreboard players operation #m rpg_te %= #12 rpg_te
execute if score #m rpg_te matches 0 run function rpg:town/ev/g/flies
execute if score #tt rpg_te matches 60 run function rpg:town/ev/g/half
execute if score #stab rpg_te matches ..0 run return run function rpg:town/ev/fail
execute if score #tt rpg_te matches 120.. run function rpg:town/ev/g/kneel
