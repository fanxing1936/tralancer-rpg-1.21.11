# 莫拉格斯 · 先锋（萨麦尔）
scoreboard players set @s rpg_mn_cd 110
particle dust_color_transition{from_color:[0.94,0.20,0.18],to_color:[0.25,0.01,0.01],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 12
particle soul_fire_flame ~ ~1 ~ 0.45 0.65 0.45 0.025 10
playsound minecraft:entity.ravager.roar hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
effect give @e[tag=rpg.advent,scores={rpg_dm_lord=5},distance=..12,limit=1] minecraft:strength 4 0 true
effect give @e[tag=rpg.demon.minion,scores={rpg_mn_lord=5},distance=..8] minecraft:strength 4 0 true
particle enchant ~ ~1 ~ 0.8 0.7 0.8 0.04 12
