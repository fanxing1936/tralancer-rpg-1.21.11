# 所有特效实体的寿命。动画每两刻走一帧：#go 为 1 的那一刻走。
scoreboard players add #go rpg_pf 1
execute if score #go rpg_pf matches 2.. run function rpg:pope_fight/fx/frame_clock
execute as @e[tag=rpg.pope.fx] at @s run function rpg:pope_fight/fx/one
