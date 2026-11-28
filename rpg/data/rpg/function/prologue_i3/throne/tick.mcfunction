# 被打碎的眼轮：模型上对应的那只换成空模型（史莱姆 rpg.pr.w<i> ↔ 眼轮 上/下/左/右）
execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne,tag=!rpg.pr.thb0,distance=0..] unless entity @e[type=minecraft:slime,tag=rpg.pr.w0,distance=0..] run function rpg:prologue_i3/throne/break0
execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne,tag=!rpg.pr.thb1,distance=0..] unless entity @e[type=minecraft:slime,tag=rpg.pr.w1,distance=0..] run function rpg:prologue_i3/throne/break1
execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne,tag=!rpg.pr.thb2,distance=0..] unless entity @e[type=minecraft:slime,tag=rpg.pr.w2,distance=0..] run function rpg:prologue_i3/throne/break2
execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne,tag=!rpg.pr.thb3,distance=0..] unless entity @e[type=minecraft:slime,tag=rpg.pr.w3,distance=0..] run function rpg:prologue_i3/throne/break3
execute unless entity @e[type=minecraft:vindicator,tag=rpg.pr.throne,distance=0..] run return 0
scoreboard players add #thr rpg_pr_i3 1
execute store result score #wl rpg_pr_i3 if entity @e[type=minecraft:slime,tag=rpg.pr.wheel,distance=0..]
execute if score #first rpg_pr_i3 matches 0 if score #wl rpg_pr_i3 matches ..3 run scoreboard players operation #first rpg_pr_i3 = #thr rpg_pr_i3
execute if score #wl rpg_pr_i3 matches 0 run return run function rpg:prologue_i3/throne/die
scoreboard players operation #m rpg_pr_i3 = #thr rpg_pr_i3
scoreboard players operation #m rpg_pr_i3 -= #first rpg_pr_i3
execute if score #first rpg_pr_i3 matches 1.. if score #m rpg_pr_i3 matches 60.. run function rpg:prologue_i3/throne/close
scoreboard players operation #m rpg_pr_i3 = #thr rpg_pr_i3
scoreboard players set #k rpg_pr_i3 50
scoreboard players operation #m rpg_pr_i3 %= #k rpg_pr_i3
execute if score #m rpg_pr_i3 matches 0 as @e[type=minecraft:vindicator,tag=rpg.pr.throne,distance=0..] at @s as @r[tag=rpg.pri3,gamemode=adventure,distance=..32] run function rpg:prologue_i3/throne/beam
execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne,distance=0..] at @s run particle minecraft:end_rod ~ ~ ~ 1.2 1.2 1.2 0.01 2
