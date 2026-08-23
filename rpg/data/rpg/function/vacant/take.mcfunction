# 又空了一个。
tag @s add rpg.vacant
tag @s add rpg.vac.seen
scoreboard players set @s rpg_vac_x 0
particle sculk_charge_pop ~ ~1.2 ~ 0.3 0.4 0.3 0.05 16
particle soul ~ ~1.2 ~ 0.2 0.3 0.2 0.02 8
playsound minecraft:block.sculk_shrieker.shriek hostile @a[distance=..20] ~ ~ ~ 0.6 1.4
