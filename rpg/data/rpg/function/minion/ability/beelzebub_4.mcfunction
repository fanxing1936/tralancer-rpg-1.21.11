# 塞列欧斯 · 咒使（别西卜）
scoreboard players set @s rpg_mn_cd 100
particle dust_color_transition{from_color:[0.70,0.84,0.34],to_color:[0.18,0.23,0.05],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 12
particle spore_blossom_air ~ ~1 ~ 0.45 0.65 0.45 0.025 10
playsound minecraft:entity.spider.ambient hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
effect give @a[distance=..8,gamemode=!spectator,gamemode=!creative] minecraft:hunger 3 0 true
effect give @a[distance=..8,gamemode=!spectator,gamemode=!creative] minecraft:weakness 4 0 true
particle reverse_portal ~ ~1 ~ 0.85 0.75 0.85 0.04 15
