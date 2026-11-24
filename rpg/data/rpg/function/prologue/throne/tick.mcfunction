# 被打碎的眼轮：模型上对应的那只换成空模型（史莱姆 rpg.pr.w<i> ↔ 眼轮 上/下/左/右）
execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne,tag=!rpg.pr.thb0] unless entity @e[type=minecraft:slime,tag=rpg.pr.w0] run function rpg:prologue/throne/break0
execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne,tag=!rpg.pr.thb1] unless entity @e[type=minecraft:slime,tag=rpg.pr.w1] run function rpg:prologue/throne/break1
execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne,tag=!rpg.pr.thb2] unless entity @e[type=minecraft:slime,tag=rpg.pr.w2] run function rpg:prologue/throne/break2
execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne,tag=!rpg.pr.thb3] unless entity @e[type=minecraft:slime,tag=rpg.pr.w3] run function rpg:prologue/throne/break3
execute unless entity @e[type=minecraft:vindicator,tag=rpg.pr.throne] run return 0
scoreboard players add #thr rpg_pr 1
execute store result score #wl rpg_pr if entity @e[type=minecraft:slime,tag=rpg.pr.wheel]
execute if score #first rpg_pr matches 0 if score #wl rpg_pr matches ..3 run scoreboard players operation #first rpg_pr = #thr rpg_pr
execute if score #wl rpg_pr matches 0 run return run function rpg:prologue/throne/die
scoreboard players operation #m rpg_pr = #thr rpg_pr
scoreboard players operation #m rpg_pr -= #first rpg_pr
execute if score #first rpg_pr matches 1.. if score #m rpg_pr matches 60.. run function rpg:prologue/throne/close
scoreboard players operation #m rpg_pr = #thr rpg_pr
scoreboard players set #k rpg_pr 50
scoreboard players operation #m rpg_pr %= #k rpg_pr
execute if score #m rpg_pr matches 0 as @e[type=minecraft:vindicator,tag=rpg.pr.throne] at @s as @r[tag=rpg.pr,gamemode=adventure,distance=..32] run function rpg:prologue/throne/beam
execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne] at @s run particle minecraft:end_rod ~ ~ ~ 1.2 1.2 1.2 0.01 2
