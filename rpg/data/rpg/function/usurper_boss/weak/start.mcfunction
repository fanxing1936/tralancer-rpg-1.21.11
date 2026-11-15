# 破绽开始（as 载体；rpg_ub_x 已设好时长）：王冠暗下
tag @s add rpg.usb.exposed
execute on passengers if entity @s[tag=rpg.prime_enchanter.p.head] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[3945512]}
execute at @s positioned ~ ~2.7 ~ run function rpg:usurper_boss/weak/burst
