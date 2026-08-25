# 阿加雷斯 · 猎手（路西法）
scoreboard players set @s rpg_mn_cd 85
particle dust_color_transition{from_color:[0.19,0.85,0.49],to_color:[0.0,0.18,0.07],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 12
particle end_rod ~ ~1 ~ 0.45 0.65 0.45 0.025 10
playsound minecraft:entity.evoker.prepare_attack hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
effect give @a[distance=..10,gamemode=!spectator,gamemode=!creative] minecraft:glowing 4 0 true
particle crit ~ ~1 ~ 0.8 0.6 0.8 0.05 12
