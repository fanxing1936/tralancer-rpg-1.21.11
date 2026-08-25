# 调查阶段保留 25% 生命底线，伤害仍会真实显示。
execute store result score @s rpg_lt_hp run data get entity @s Health 100
scoreboard players remove @s rpg_lt_hp 17500
execute if score @s rpg_lt_max > @s rpg_lt_hp run scoreboard players operation @s rpg_lt_max = @s rpg_lt_hp
execute if score @s rpg_lt_max matches 1.. run function rpg:divine/damage/apply_score
