# 瓦沙克 · 司祭（路西法）
scoreboard players set @s rpg_mn_cd 125
particle dust_color_transition{from_color:[0.19,0.85,0.49],to_color:[0.0,0.18,0.07],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 12
particle end_rod ~ ~1 ~ 0.45 0.65 0.45 0.025 10
playsound minecraft:entity.evoker.prepare_attack hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
effect give @e[tag=rpg.advent,scores={rpg_dm_lord=1},distance=..14,limit=1] minecraft:instant_health 1 0 true
effect give @e[tag=rpg.demon.minion,scores={rpg_mn_lord=1},distance=..10] minecraft:regeneration 4 0 true
effect give @e[tag=rpg.demon.minion,scores={rpg_mn_lord=1},distance=..10] minecraft:resistance 4 0 true
particle heart ~ ~1.4 ~ 0.75 0.6 0.75 0.03 9
