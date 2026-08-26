# 巴钦 · 司祭（别西卜）：吞食反哺
scoreboard players add #casts rpg_mn_tick 1
scoreboard players set @s rpg_mn_cd 137
scoreboard players set @s rpg_mn_cast 20
tag @s add rpg.demon.minion.casting
tellraw @a[distance=..14,gamemode=!spectator] ["",{"text":"[罪仆术式] ","color":"#596B18","bold":true,"italic":false},{"text":"巴钦 · ","color":"#B5D957","bold":false,"italic":false},{"text":"吞食反哺","color":"#B5D957","bold":true,"italic":false},{"text":"｜司祭","color":"gray","bold":false,"italic":false},{"text":"　以腐宴喂养受伤的同柱","color":"dark_gray","bold":false,"italic":false}]
playsound minecraft:entity.spider.ambient hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
playsound minecraft:block.enchantment_table.use hostile @a[distance=..14] ~ ~ ~ 0.28 0.92
particle dust_color_transition{from_color:[0.70,0.84,0.34],to_color:[0.18,0.23,0.05],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 4
execute facing entity @e[tag=rpg.demon.minion,scores={rpg_mn_lord=4},distance=0.1..10,sort=nearest,limit=1] eyes run particle end_rod ^ ^1 ^1 0.05 0.05 0.05 0.01 2
execute facing entity @e[tag=rpg.demon.minion,scores={rpg_mn_lord=4},distance=0.1..10,sort=nearest,limit=1] eyes run particle end_rod ^ ^1 ^2 0.05 0.05 0.05 0.01 2
execute facing entity @e[tag=rpg.demon.minion,scores={rpg_mn_lord=4},distance=0.1..10,sort=nearest,limit=1] eyes run particle end_rod ^ ^1 ^3 0.05 0.05 0.05 0.01 2
execute facing entity @e[tag=rpg.demon.minion,scores={rpg_mn_lord=4},distance=0.1..10,sort=nearest,limit=1] eyes run particle end_rod ^ ^1 ^4 0.05 0.05 0.05 0.01 2
