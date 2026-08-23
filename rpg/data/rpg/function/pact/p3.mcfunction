# 收割：周身一圈灵魂被抽走，抽一个回一颗心。
particle sculk_soul ~ ~1 ~ 3 1 3 0.02 120
particle soul ~ ~0.5 ~ 3 0.6 3 0.04 80
particle sculk_charge_pop ~ ~1 ~ 2.5 1 2.5 0.06 40
playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..28] ~ ~ ~ 0.8 0.7
playsound minecraft:block.sculk_shrieker.shriek hostile @a[distance=..28] ~ ~ ~ 1 0.6
execute as @e[distance=0.1..6,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:item_display] at @s run function rpg:pact/p3_reap
