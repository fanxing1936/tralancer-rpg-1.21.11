# 列拉金 · 咒使（亚巴顿）
scoreboard players set @s rpg_mn_cd 100
particle dust_color_transition{from_color:[0.76,0.76,0.82],to_color:[0.10,0.10,0.12],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 12
particle sculk_soul ~ ~1 ~ 0.45 0.65 0.45 0.025 10
playsound minecraft:entity.warden.heartbeat hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
effect give @a[distance=..8,gamemode=!spectator,gamemode=!creative] minecraft:poison 3 0 true
effect give @a[distance=..8,gamemode=!spectator,gamemode=!creative] minecraft:darkness 4 0 true
particle reverse_portal ~ ~1 ~ 0.85 0.75 0.85 0.04 15
