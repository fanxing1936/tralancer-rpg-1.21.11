# 派蒙 · 咒使（利维坦）
scoreboard players set @s rpg_mn_cd 100
particle dust_color_transition{from_color:[0.25,0.78,0.93],to_color:[0.02,0.16,0.31],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 12
particle nautilus ~ ~1 ~ 0.45 0.65 0.45 0.025 10
playsound minecraft:entity.guardian.attack hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
effect give @a[distance=..8,gamemode=!spectator,gamemode=!creative] minecraft:slowness 3 0 true
effect give @a[distance=..8,gamemode=!spectator,gamemode=!creative] minecraft:mining_fatigue 4 0 true
particle reverse_portal ~ ~1 ~ 0.85 0.75 0.85 0.04 15
