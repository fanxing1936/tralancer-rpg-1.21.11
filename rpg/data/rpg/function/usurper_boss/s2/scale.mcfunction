# 二阶段读血前（as 载体）：Health×10 和上次比，少了就按状态退回一半或再扣一半
execute store result score #hp rpg_ub run data get entity @s Health 10
scoreboard players operation #lost rpg_ub = @s rpg_ub_l
scoreboard players operation #lost rpg_ub -= #hp rpg_ub
execute if score #lost rpg_ub matches 1.. run function rpg:usurper_boss/s2/hurt
execute store result score @s rpg_ub_l run data get entity @s Health 10
