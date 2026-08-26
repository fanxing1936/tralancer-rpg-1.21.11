# 西迪 · 猎手（亚巴顿）：疫矢猎印
scoreboard players add #casts rpg_mn_tick 1
scoreboard players set @s rpg_mn_cd 93
scoreboard players set @s rpg_mn_cast 20
tag @s add rpg.demon.minion.casting
tellraw @a[distance=..10,gamemode=!spectator] ["",{"text":"[罪仆术式] ","color":"#5B5B62","bold":true,"italic":false},{"text":"西迪 · ","color":"#C2C2CC","bold":false,"italic":false},{"text":"疫矢猎印","color":"#C2C2CC","bold":true,"italic":false},{"text":"｜猎手","color":"gray","bold":false,"italic":false},{"text":"　骨哨令最近的活物腐败","color":"dark_gray","bold":false,"italic":false}]
playsound minecraft:entity.warden.heartbeat hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
playsound minecraft:item.crossbow.shoot hostile @a[distance=..14] ~ ~ ~ 0.28 0.92
particle dust_color_transition{from_color:[0.76,0.76,0.82],to_color:[0.10,0.10,0.12],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 4
execute at @a[distance=..10,sort=nearest,limit=1,gamemode=!spectator,gamemode=!creative] run particle crit ~ ~1 ~ 0.28 0.55 0.28 0.035 8
effect give @a[distance=..10,sort=nearest,limit=1,gamemode=!spectator,gamemode=!creative] minecraft:glowing 1 0 true
