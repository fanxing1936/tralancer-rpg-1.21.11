# 一支图腾一拍。净化与反转两套节拍，从这里分开。
execute if entity @s[tag=rpg.totem.inv] run function rpg:rite/beat_inv
execute unless entity @s[tag=rpg.totem.inv] run function rpg:rite/beat_pure
