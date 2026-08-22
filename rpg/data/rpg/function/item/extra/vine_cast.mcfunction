# 甩鞭：消耗 1 级经验，把 6 格内的敌人全部拽近并挂上三秒连击
xp add @s -1 levels
tag @s add rpg.vine.src
particle minecraft:tinted_leaves{color:12835692} ~ ~1 ~ 1.3 0.7 1.3 0.05 70
particle spore_blossom_air ~ ~1 ~ 1.3 0.7 1.3 0 20
playsound minecraft:block.cave_vines.break player @a[distance=..16] ~ ~ ~ 1 0.7
execute as @e[distance=0.1..6,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run function rpg:item/extra/vine_grab
tag @s remove rpg.vine.src
