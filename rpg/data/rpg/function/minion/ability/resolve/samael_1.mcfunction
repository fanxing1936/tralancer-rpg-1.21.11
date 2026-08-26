# 怒血共鸣：延迟结算；单次总粒子预算不超过 28。
tag @s remove rpg.demon.minion.casting
scoreboard players set @s rpg_mn_cast 0
particle soul_fire_flame ~ ~1 ~ 0.38 0.55 0.38 0.025 2
playsound minecraft:item.shield.block hostile @a[distance=..14] ~ ~ ~ 0.32 1.05
effect give @e[tag=rpg.advent,scores={rpg_dm_lord=5},distance=..12,limit=1] minecraft:strength 4 0 true
effect give @e[tag=rpg.demon.minion,scores={rpg_mn_lord=5},distance=..8] minecraft:strength 4 0 true
effect give @e[tag=rpg.demon.minion,scores={rpg_mn_lord=5},distance=..8] minecraft:resistance 3 0 true
particle enchant ~ ~1 ~ 0.8 0.7 0.8 0.04 10
