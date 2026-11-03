# 阿加雷斯 · 猎手（路西法）：罪痕标定
scoreboard players add #casts rpg_mn_tick 1
scoreboard players set @s rpg_mn_cd 85
scoreboard players set @s rpg_mn_cast 20
tag @s add rpg.demon.minion.casting
tellraw @a[distance=..10,gamemode=!spectator] ["",{"text":"[罪仆术式] ","color":"#5FD68C","bold":true,"italic":false},{"text":"阿加雷斯 · ","color":"#FFFFFF","bold":false,"italic":false},{"text":"罪痕标定","color":"#5FD68C","bold":true,"italic":false},{"text":"｜猎手","color":"gray","bold":false,"italic":false},{"text":"　锁定最近的见证者并令其失重","color":"dark_gray","bold":false,"italic":false}]
playsound minecraft:entity.evoker.prepare_attack hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
playsound minecraft:item.crossbow.shoot hostile @a[distance=..14] ~ ~ ~ 0.28 0.92
particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 4
execute at @a[distance=..10,sort=nearest,limit=1,gamemode=!spectator,gamemode=!creative] run particle crit ~ ~1 ~ 0.28 0.55 0.28 0.035 8
effect give @a[distance=..10,sort=nearest,limit=1,gamemode=!spectator,gamemode=!creative] minecraft:glowing 1 0 true
