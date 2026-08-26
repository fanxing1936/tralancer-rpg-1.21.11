# 佛拉斯 · 先锋（玛门）：金契护体
scoreboard players add #casts rpg_mn_tick 1
scoreboard players set @s rpg_mn_cd 134
scoreboard players set @s rpg_mn_cast 10
tag @s add rpg.demon.minion.casting
tellraw @a[distance=..12,gamemode=!spectator] ["",{"text":"[罪仆术式] ","color":"#987B08","bold":true,"italic":false},{"text":"佛拉斯 · ","color":"#FFD85A","bold":false,"italic":false},{"text":"金契护体","color":"#FFD85A","bold":true,"italic":false},{"text":"｜先锋","color":"gray","bold":false,"italic":false},{"text":"　财富替同柱承受第一道伤口","color":"dark_gray","bold":false,"italic":false}]
playsound minecraft:block.amethyst_block.chime hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
playsound minecraft:item.shield.block hostile @a[distance=..14] ~ ~ ~ 0.28 0.92
particle dust_color_transition{from_color:[1.0,0.79,0.20],to_color:[0.28,0.17,0.01],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 4
particle enchant ~ ~1 ~ 0.72 0.18 0.72 0.025 8
