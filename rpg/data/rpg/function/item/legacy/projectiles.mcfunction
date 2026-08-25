
# 普通箭首次分类后离开；只有三种技能箭进入持续热路径。
execute if entity @e[type=#minecraft:arrows,tag=!rpg.legacy.seen,limit=1] run function rpg:item/legacy/projectiles_new
execute as @e[type=#minecraft:arrows,tag=rpg.legacy.active] at @s run function rpg:item/legacy/projectiles_active
