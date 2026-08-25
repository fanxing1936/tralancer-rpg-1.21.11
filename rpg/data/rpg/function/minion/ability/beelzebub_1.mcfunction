# 桀派 · 先锋（别西卜）
scoreboard players set @s rpg_mn_cd 110
particle dust_color_transition{from_color:[0.70,0.84,0.34],to_color:[0.18,0.23,0.05],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 12
particle spore_blossom_air ~ ~1 ~ 0.45 0.65 0.45 0.025 10
playsound minecraft:entity.spider.ambient hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
effect give @e[tag=rpg.advent,scores={rpg_dm_lord=4},distance=..12,limit=1] minecraft:absorption 4 0 true
effect give @e[tag=rpg.demon.minion,scores={rpg_mn_lord=4},distance=..8] minecraft:absorption 4 0 true
particle enchant ~ ~1 ~ 0.8 0.7 0.8 0.04 12
