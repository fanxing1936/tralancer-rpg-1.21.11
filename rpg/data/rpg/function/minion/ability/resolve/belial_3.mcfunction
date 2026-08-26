# 献身回流：延迟结算；单次总粒子预算不超过 28。
tag @s remove rpg.demon.minion.casting
scoreboard players set @s rpg_mn_cast 0
particle witch ~ ~1 ~ 0.38 0.55 0.38 0.025 2
playsound minecraft:block.enchantment_table.use hostile @a[distance=..14] ~ ~ ~ 0.32 1.05
effect give @e[tag=rpg.advent,scores={rpg_dm_lord=6},distance=..14,limit=1] minecraft:instant_health 1 0 true
effect give @e[tag=rpg.demon.minion,scores={rpg_mn_lord=6},distance=..10] minecraft:regeneration 4 0 true
effect give @e[tag=rpg.demon.minion,scores={rpg_mn_lord=6},distance=..10] minecraft:regeneration 4 0 true
effect give @e[tag=rpg.demon.minion,scores={rpg_mn_lord=6},distance=..10] minecraft:resistance 3 0 true
particle heart ~ ~1.4 ~ 0.75 0.6 0.75 0.03 10
