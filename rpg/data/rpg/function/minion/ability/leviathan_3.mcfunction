# 巴巴托斯 · 司祭（利维坦）
scoreboard players set @s rpg_mn_cd 125
particle dust_color_transition{from_color:[0.25,0.78,0.93],to_color:[0.02,0.16,0.31],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 12
particle nautilus ~ ~1 ~ 0.45 0.65 0.45 0.025 10
playsound minecraft:entity.guardian.attack hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
effect give @e[tag=rpg.advent,scores={rpg_dm_lord=2},distance=..14,limit=1] minecraft:instant_health 1 0 true
effect give @e[tag=rpg.demon.minion,scores={rpg_mn_lord=2},distance=..10] minecraft:regeneration 4 0 true
effect give @e[tag=rpg.demon.minion,scores={rpg_mn_lord=2},distance=..10] minecraft:speed 4 0 true
particle heart ~ ~1.4 ~ 0.75 0.6 0.75 0.03 9
