# 因波斯 · 猎手（萨麦尔）：血猎标记
scoreboard players add #casts rpg_mn_tick 1
scoreboard players set @s rpg_mn_cd 101
scoreboard players set @s rpg_mn_cast 20
tag @s add rpg.demon.minion.casting
tellraw @a[distance=..10,gamemode=!spectator] ["",{"text":"[罪仆术式] ","color":"#7B241C","bold":true,"italic":false},{"text":"因波斯 · ","color":"#FF665E","bold":false,"italic":false},{"text":"血猎标记","color":"#FF665E","bold":true,"italic":false},{"text":"｜猎手","color":"gray","bold":false,"italic":false},{"text":"　猎手沿血光咬住最近目标","color":"dark_gray","bold":false,"italic":false}]
playsound minecraft:entity.ravager.roar hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
playsound minecraft:item.crossbow.shoot hostile @a[distance=..14] ~ ~ ~ 0.28 0.92
particle dust_color_transition{from_color:[0.94,0.20,0.18],to_color:[0.25,0.01,0.01],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 4
execute at @a[distance=..10,sort=nearest,limit=1,gamemode=!spectator,gamemode=!creative] run particle crit ~ ~1 ~ 0.28 0.55 0.28 0.035 8
effect give @a[distance=..10,sort=nearest,limit=1,gamemode=!spectator,gamemode=!creative] minecraft:glowing 1 0 true
