# 挨了一下（as 载体）：打的人在盾面前方，就把这一下退回七成（同教皇外壳）；从背后或侧面打照吃
execute positioned ^ ^ ^1.8 unless entity @e[tag=rpg.unit.f,distance=..2.6] run return 0
scoreboard players operation #lost rpg_rg_v = @s damage_timing
scoreboard players operation #lost rpg_rg_v -= @s damage_action
execute if score #lost rpg_rg_v matches ..0 run return 0
scoreboard players operation #lost rpg_rg_v *= #keep rpg_rg_v
scoreboard players operation #lost rpg_rg_v /= #ten rpg_rg_v
scoreboard players operation #hp rpg_rg_v = @s damage_action
scoreboard players operation #hp rpg_rg_v += #lost rpg_rg_v
execute store result entity @s Health float 1 run scoreboard players get #hp rpg_rg_v
scoreboard players operation @s damage_timing = #hp rpg_rg_v
scoreboard players operation @s damage_action = #hp rpg_rg_v
playsound rpg:royal_guard.block hostile @a[distance=..24] ~ ~ ~ 0.8 0.9
particle minecraft:enchanted_hit ^ ^1.2 ^0.8 0.3 0.4 0.3 0.1 10 normal
