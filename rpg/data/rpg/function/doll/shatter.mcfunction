# 最后一道裂。人偶碎掉，把吃进去的东西一次吐干净。
particle sculk_charge_pop ~ ~0.6 ~ 0.4 0.4 0.4 0.15 60
particle end_rod ~ ~0.6 ~ 0.4 0.4 0.4 0.08 40
playsound minecraft:entity.allay.death hostile @a[distance=..24] ~ ~ ~ 1 0.7
playsound minecraft:block.amethyst_cluster.break hostile @a[distance=..24] ~ ~ ~ 1 0.5
execute as @a[distance=..12] run function rpg:hud/m1
