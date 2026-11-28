# 恢复灵体（as 他）
tag @s remove rpg.mkb.solid
scoreboard players set @s rpg_mk_so 0
execute unless entity @s[tag=rpg.mkb.end] unless score #pro rpg_mk_i2 matches 1 run function rpg:michael/look/spirit
attribute @s minecraft:knockback_resistance base set 1
execute at @s run particle minecraft:end_rod ~ ~1.2 ~ 0.4 0.7 0.4 0.03 10
