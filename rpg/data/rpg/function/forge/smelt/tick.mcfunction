# 冶炼中的火点：3 秒魂火，然后出炉。
particle minecraft:soul_fire_flame ~ ~0.8 ~ 0.25 0.4 0.25 0.02 6
particle minecraft:sculk_soul ~ ~1.2 ~ 0.2 0.3 0.2 0.02 2
execute if score @s rpg_fg_t matches 20 run playsound minecraft:block.anvil.use block @a[distance=..16] ~ ~ ~ 0.6 0.7
execute if score @s rpg_fg_t matches 40 run playsound minecraft:block.anvil.use block @a[distance=..16] ~ ~ ~ 0.6 0.9
scoreboard players remove @s rpg_fg_t 1
execute if score @s rpg_fg_t matches ..0 run function rpg:forge/smelt/make
