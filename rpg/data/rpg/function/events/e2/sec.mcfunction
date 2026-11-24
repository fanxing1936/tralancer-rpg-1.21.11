# 前 3 秒：火光从天上落到标记处；第 3 秒落地
execute if score #stage rpg_ev matches 0 at @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] run particle minecraft:flame ~ ~26 ~ 0.4 1.2 0.4 0.05 40 force
execute if score #stage rpg_ev matches 0 at @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] run particle minecraft:end_rod ~ ~26 ~ 0.3 0.8 0.3 0.02 16 force
execute if score #stage rpg_ev matches 1 at @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] run particle minecraft:flame ~ ~16 ~ 0.4 1.2 0.4 0.05 40 force
execute if score #stage rpg_ev matches 1 at @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] run particle minecraft:end_rod ~ ~16 ~ 0.3 0.8 0.3 0.02 16 force
execute if score #stage rpg_ev matches 2 at @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] run particle minecraft:flame ~ ~6 ~ 0.4 1.2 0.4 0.05 40 force
execute if score #stage rpg_ev matches 2 at @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] run particle minecraft:end_rod ~ ~6 ~ 0.3 0.8 0.3 0.02 16 force
scoreboard players add #stage rpg_ev 1
execute if score #stage rpg_ev matches 3 at @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] run function rpg:events/e2/land
execute if score #stage rpg_ev matches 4.. at @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] run particle minecraft:end_rod ~ ~1 ~ 0.6 0.6 0.6 0.01 4
execute if score #stage rpg_ev matches 5.. unless entity @e[tag=rpg.ev.star] at @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] run function rpg:events/e2/done
