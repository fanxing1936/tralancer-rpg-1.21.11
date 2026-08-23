# 照出一个空壳，并且审判它 —— 星光本身就是刑罚。
effect give @s minecraft:glowing 15 0 true
scoreboard players add @s rpg_vac_x 30
damage @s 6 minecraft:magic
particle end_rod ~ ~1.2 ~ 0.3 0.5 0.3 0.06 30
particle sculk_soul ~ ~1.2 ~ 0.3 0.4 0.3 0.03 16
playsound minecraft:block.beacon.activate hostile @a[distance=..24] ~ ~ ~ 0.8 1.5
