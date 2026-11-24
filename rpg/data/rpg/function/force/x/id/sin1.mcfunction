# 傲慢：满血时伤害 +10%（美丽阶起 +20%）
attribute @s minecraft:attack_damage modifier remove rpg:fo_sin
execute store result score #h rpg_fo run data get entity @s Health 10
execute store result score #mh rpg_fo run attribute @s minecraft:max_health get 10
execute unless score #h rpg_fo >= #mh rpg_fo run return 0
execute unless score @s rpg_sef matches 5.. run attribute @s minecraft:attack_damage modifier add rpg:fo_sin 0.1 add_multiplied_total
execute if score @s rpg_sef matches 5.. run attribute @s minecraft:attack_damage modifier add rpg:fo_sin 0.2 add_multiplied_total
