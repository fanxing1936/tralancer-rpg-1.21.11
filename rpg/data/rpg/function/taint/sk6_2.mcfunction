# 迷乱 —— 你分不清哪边是他。
playsound minecraft:entity.illusioner.mirror_move hostile @a[distance=..32] ~ ~ ~ 1 0.7
particle portal ~ ~1 ~ 3 1 3 0.6 120
execute as @a[distance=..8,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk6b_daze
