# 亚蒙 · 猎手（利维坦）：寒潮猎印
scoreboard players add #casts rpg_mn_tick 1
scoreboard players set @s rpg_mn_cd 89
scoreboard players set @s rpg_mn_cast 20
tag @s add rpg.demon.minion.casting
tellraw @a[distance=..10,gamemode=!spectator] ["",{"text":"[罪仆术式] ","color":"#4F9EF0","bold":true,"italic":false},{"text":"亚蒙 · ","color":"#FFFFFF","bold":false,"italic":false},{"text":"寒潮猎印","color":"#4F9EF0","bold":true,"italic":false},{"text":"｜猎手","color":"gray","bold":false,"italic":false},{"text":"　暗潮缠住最近的脚步","color":"dark_gray","bold":false,"italic":false}]
playsound minecraft:entity.guardian.attack hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
playsound minecraft:item.crossbow.shoot hostile @a[distance=..14] ~ ~ ~ 0.28 0.92
particle dust_color_transition{from_color:[0.31,0.62,0.94],to_color:[0.11,0.31,0.45],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 4
execute at @a[distance=..10,sort=nearest,limit=1,gamemode=!spectator,gamemode=!creative] run particle crit ~ ~1 ~ 0.28 0.55 0.28 0.035 8
effect give @a[distance=..10,sort=nearest,limit=1,gamemode=!spectator,gamemode=!creative] minecraft:glowing 1 0 true
