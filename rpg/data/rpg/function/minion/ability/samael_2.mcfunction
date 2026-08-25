# 因波斯 · 猎手（萨麦尔）
scoreboard players set @s rpg_mn_cd 85
particle dust_color_transition{from_color:[0.94,0.20,0.18],to_color:[0.25,0.01,0.01],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 12
particle soul_fire_flame ~ ~1 ~ 0.45 0.65 0.45 0.025 10
playsound minecraft:entity.ravager.roar hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
effect give @a[distance=..10,gamemode=!spectator,gamemode=!creative] minecraft:glowing 4 0 true
particle crit ~ ~1 ~ 0.8 0.6 0.8 0.05 12
