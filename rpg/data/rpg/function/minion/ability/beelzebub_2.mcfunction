# 布提斯 · 猎手（别西卜）：饥印
scoreboard players add #casts rpg_mn_tick 1
scoreboard players set @s rpg_mn_cd 97
scoreboard players set @s rpg_mn_cast 20
tag @s add rpg.demon.minion.casting
tellraw @a[distance=..10,gamemode=!spectator] ["",{"text":"[罪仆术式] ","color":"#596B18","bold":true,"italic":false},{"text":"布提斯 · ","color":"#B5D957","bold":false,"italic":false},{"text":"饥印","color":"#B5D957","bold":true,"italic":false},{"text":"｜猎手","color":"gray","bold":false,"italic":false},{"text":"　腐蝇锁定最近且最鲜活的胃","color":"dark_gray","bold":false,"italic":false}]
playsound minecraft:entity.spider.ambient hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
playsound minecraft:item.crossbow.shoot hostile @a[distance=..14] ~ ~ ~ 0.28 0.92
particle dust_color_transition{from_color:[0.70,0.84,0.34],to_color:[0.18,0.23,0.05],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 4
execute at @a[distance=..10,sort=nearest,limit=1,gamemode=!spectator,gamemode=!creative] run particle crit ~ ~1 ~ 0.28 0.55 0.28 0.035 8
effect give @a[distance=..10,sort=nearest,limit=1,gamemode=!spectator,gamemode=!creative] minecraft:glowing 1 0 true
