# 圣卫只打晕：血量低到三成就跪下（不再动、不再挨打）
execute as @e[tag=rpg.te.g,tag=!rpg.te.down] store result score #h rpg_te run data get entity @s Health
execute as @e[tag=rpg.te.g,tag=!rpg.te.down] run function rpg:town/ev/w/stun_one
