# 空壳散去。村民留下，罪从他身上剥离；跑出来的碎片一并收走。
tag @s remove rpg.vacant
tag @s remove rpg.vac.torn
scoreboard players set @s rpg_vac_x 0
particle sculk_soul ~ ~1 ~ 0.3 0.5 0.3 0.06 40
particle end_rod ~ ~1 ~ 0.3 0.5 0.3 0.03 24
playsound minecraft:entity.evoker.celebrate hostile @a[distance=..20] ~ ~ ~ 1 1.3
effect give @s minecraft:glowing 4 0 true
kill @e[type=minecraft:vex,tag=rpg.vac.shard,distance=..12]
execute as @a[distance=..8] run scoreboard players remove @s rpg_taint 5
execute at @s run summon minecraft:experience_orb ~ ~1 ~ {Value:24}
