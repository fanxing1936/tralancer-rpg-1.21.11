# 古辛 · 先锋（亚巴顿）：死寂护幕
scoreboard players add #casts rpg_mn_tick 1
scoreboard players set @s rpg_mn_cd 118
scoreboard players set @s rpg_mn_cast 10
tag @s add rpg.demon.minion.casting
tellraw @a[distance=..12,gamemode=!spectator] ["",{"text":"[罪仆术式] ","color":"#5B5B62","bold":true,"italic":false},{"text":"古辛 · ","color":"#C2C2CC","bold":false,"italic":false},{"text":"死寂护幕","color":"#C2C2CC","bold":true,"italic":false},{"text":"｜先锋","color":"gray","bold":false,"italic":false},{"text":"　死亡为同柱封上一层墓石","color":"dark_gray","bold":false,"italic":false}]
playsound minecraft:entity.warden.heartbeat hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
playsound minecraft:item.shield.block hostile @a[distance=..14] ~ ~ ~ 0.28 0.92
particle dust_color_transition{from_color:[0.76,0.76,0.82],to_color:[0.10,0.10,0.12],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 4
particle enchant ~ ~1 ~ 0.72 0.18 0.72 0.025 8
