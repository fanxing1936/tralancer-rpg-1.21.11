# 人走了，或者人倒了。图腾自己碎掉，罪一点没少。
particle large_smoke ~ ~0.7 ~ 0.5 0.5 0.5 0.05 60
particle campfire_signal_smoke ~ ~0.8 ~ 0.3 0.3 0.3 0.02 20
playsound minecraft:block.glass.break master @a[distance=..24] ~ ~ ~ 1 0.6
playsound minecraft:entity.blaze.death master @a[distance=..24] ~ ~ ~ 0.8 0.5
execute as @a[tag=rpg.inv.subject] run function rpg:rite/inv_abort
kill @s
