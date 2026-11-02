# 巴力 · 先锋（路西法）：王冠护持
scoreboard players add #casts rpg_mn_tick 1
scoreboard players set @s rpg_mn_cd 110
scoreboard players set @s rpg_mn_cast 10
tag @s add rpg.demon.minion.casting
tellraw @a[distance=..12,gamemode=!spectator] ["",{"text":"[罪仆术式] ","color":"#5FD68C","bold":true,"italic":false},{"text":"巴力 · ","color":"#FFFFFF","bold":false,"italic":false},{"text":"王冠护持","color":"#5FD68C","bold":true,"italic":false},{"text":"｜先锋","color":"gray","bold":false,"italic":false},{"text":"　傲慢为同柱披上王权","color":"dark_gray","bold":false,"italic":false}]
playsound minecraft:entity.evoker.prepare_attack hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
playsound minecraft:item.shield.block hostile @a[distance=..14] ~ ~ ~ 0.28 0.92
particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 4
particle enchant ~ ~1 ~ 0.72 0.18 0.72 0.025 8
