# 佛拉斯 · 先锋（玛门）
scoreboard players set @s rpg_mn_cd 110
particle dust_color_transition{from_color:[1.0,0.79,0.20],to_color:[0.28,0.17,0.01],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 12
particle wax_on ~ ~1 ~ 0.45 0.65 0.45 0.025 10
playsound minecraft:block.amethyst_block.chime hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
effect give @e[tag=rpg.advent,scores={rpg_dm_lord=7},distance=..12,limit=1] minecraft:absorption 4 0 true
effect give @e[tag=rpg.demon.minion,scores={rpg_mn_lord=7},distance=..8] minecraft:absorption 4 0 true
particle enchant ~ ~1 ~ 0.8 0.7 0.8 0.04 12
