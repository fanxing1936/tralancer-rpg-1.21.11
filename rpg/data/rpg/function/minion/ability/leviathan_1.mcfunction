# 华利弗 · 先锋（利维坦）：妒潮护幕
scoreboard players add #casts rpg_mn_tick 1
scoreboard players set @s rpg_mn_cd 114
scoreboard players set @s rpg_mn_cast 10
tag @s add rpg.demon.minion.casting
tellraw @a[distance=..12,gamemode=!spectator] ["",{"text":"[罪仆术式] ","color":"#1B4F72","bold":true,"italic":false},{"text":"华利弗 · ","color":"#62D9E8","bold":false,"italic":false},{"text":"妒潮护幕","color":"#62D9E8","bold":true,"italic":false},{"text":"｜先锋","color":"gray","bold":false,"italic":false},{"text":"　嫉妒复制最坚固的鳞片","color":"dark_gray","bold":false,"italic":false}]
playsound minecraft:entity.guardian.attack hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
playsound minecraft:item.shield.block hostile @a[distance=..14] ~ ~ ~ 0.28 0.92
particle dust_color_transition{from_color:[0.25,0.78,0.93],to_color:[0.02,0.16,0.31],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 4
particle enchant ~ ~1 ~ 0.72 0.18 0.72 0.025 8
