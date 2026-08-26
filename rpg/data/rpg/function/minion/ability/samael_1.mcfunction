# 莫拉格斯 · 先锋（萨麦尔）：怒血共鸣
scoreboard players add #casts rpg_mn_tick 1
scoreboard players set @s rpg_mn_cd 126
scoreboard players set @s rpg_mn_cast 10
tag @s add rpg.demon.minion.casting
tellraw @a[distance=..12,gamemode=!spectator] ["",{"text":"[罪仆术式] ","color":"#7B241C","bold":true,"italic":false},{"text":"莫拉格斯 · ","color":"#FF665E","bold":false,"italic":false},{"text":"怒血共鸣","color":"#FF665E","bold":true,"italic":false},{"text":"｜先锋","color":"gray","bold":false,"italic":false},{"text":"　暴怒将伤口锻成力量","color":"dark_gray","bold":false,"italic":false}]
playsound minecraft:entity.ravager.roar hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
playsound minecraft:item.shield.block hostile @a[distance=..14] ~ ~ ~ 0.28 0.92
particle dust_color_transition{from_color:[0.94,0.20,0.18],to_color:[0.25,0.01,0.01],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 4
particle enchant ~ ~1 ~ 0.72 0.18 0.72 0.025 8
