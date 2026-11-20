scoreboard players set @s rpg_sl_c 0
# 三招轮流：血线各放一次；时钟到点放下一个（rpg_sl_ur 记着轮到第几个）
execute if score #ult rpg_sl matches 9 run scoreboard players add @s rpg_sl_ur 1
execute if score #ult rpg_sl matches 9 if score @s rpg_sl_ur matches 4.. run scoreboard players set @s rpg_sl_ur 1
execute if score #ult rpg_sl matches 9 run scoreboard players operation #ult rpg_sl = @s rpg_sl_ur
scoreboard players operation @s rpg_sl_ur = #ult rpg_sl
execute if score #ult rpg_sl matches 1 run tag @s add rpg.slb.u1
execute if score #ult rpg_sl matches 2 run tag @s add rpg.slb.u2
execute if score #ult rpg_sl matches 3 run tag @s add rpg.slb.u3
execute if score @s rpg_sl matches 1 if score #ult rpg_sl matches 1 run function rpg:saul_boss/ult/line
execute if score @s rpg_sl matches 1 if score #ult rpg_sl matches 2 run function rpg:saul_boss/ult/circle
execute if score @s rpg_sl matches 1 if score #ult rpg_sl matches 3 run function rpg:saul_boss/ult/echoes
execute if score @s rpg_sl matches 2 if score #ult rpg_sl matches 1 run function rpg:saul_boss/ult/cuts
execute if score @s rpg_sl matches 2 if score #ult rpg_sl matches 2 run function rpg:saul_boss/ult/rain
execute if score @s rpg_sl matches 2 if score #ult rpg_sl matches 3 run function rpg:saul_boss/ult/last
