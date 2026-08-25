# 西迪 · 猎手（亚巴顿）
scoreboard players set @s rpg_mn_cd 85
particle dust_color_transition{from_color:[0.76,0.76,0.82],to_color:[0.10,0.10,0.12],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 12
particle sculk_soul ~ ~1 ~ 0.45 0.65 0.45 0.025 10
playsound minecraft:entity.warden.heartbeat hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
effect give @a[distance=..10,gamemode=!spectator,gamemode=!creative] minecraft:poison 4 0 true
particle crit ~ ~1 ~ 0.8 0.6 0.8 0.05 12
