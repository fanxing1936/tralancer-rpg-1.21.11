# 阿斯摩太 · 猎手（玛门）：债印
scoreboard players add #casts rpg_mn_tick 1
scoreboard players set @s rpg_mn_cd 109
scoreboard players set @s rpg_mn_cast 20
tag @s add rpg.demon.minion.casting
tellraw @a[distance=..10,gamemode=!spectator] ["",{"text":"[罪仆术式] ","color":"#987B08","bold":true,"italic":false},{"text":"阿斯摩太 · ","color":"#FFD85A","bold":false,"italic":false},{"text":"债印","color":"#FFD85A","bold":true,"italic":false},{"text":"｜猎手","color":"gray","bold":false,"italic":false},{"text":"　金光记下最近目标的欠款","color":"dark_gray","bold":false,"italic":false}]
playsound minecraft:block.amethyst_block.chime hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
playsound minecraft:item.crossbow.shoot hostile @a[distance=..14] ~ ~ ~ 0.28 0.92
particle dust_color_transition{from_color:[1.0,0.79,0.20],to_color:[0.28,0.17,0.01],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 4
execute at @a[distance=..10,sort=nearest,limit=1,gamemode=!spectator,gamemode=!creative] run particle crit ~ ~1 ~ 0.28 0.55 0.28 0.035 8
effect give @a[distance=..10,sort=nearest,limit=1,gamemode=!spectator,gamemode=!creative] minecraft:glowing 1 0 true
