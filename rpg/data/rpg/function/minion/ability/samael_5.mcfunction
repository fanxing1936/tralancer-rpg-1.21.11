# 格拉夏·拉波拉斯 · 处刑者（萨麦尔）：怒斩
scoreboard players add #casts rpg_mn_tick 1
scoreboard players set @s rpg_mn_cd 91
scoreboard players set @s rpg_mn_cast 10
tag @s add rpg.demon.minion.casting
tellraw @a[distance=..4,gamemode=!spectator] ["",{"text":"[罪仆术式] ","color":"#7B241C","bold":true,"italic":false},{"text":"格拉夏·拉波拉斯 · ","color":"#FF665E","bold":false,"italic":false},{"text":"怒斩","color":"#FF665E","bold":true,"italic":false},{"text":"｜处刑者","color":"gray","bold":false,"italic":false},{"text":"　最短的距离只容得下一次斩击","color":"dark_gray","bold":false,"italic":false}]
playsound minecraft:entity.ravager.roar hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
playsound minecraft:entity.player.attack.strong hostile @a[distance=..14] ~ ~ ~ 0.28 0.92
particle dust_color_transition{from_color:[0.94,0.20,0.18],to_color:[0.25,0.01,0.01],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 4
particle crit ~4 ~0.18 ~0 0 0 0 0 1
particle crit ~-4 ~0.18 ~0 0 0 0 0 1
particle crit ~0 ~0.18 ~4 0 0 0 0 1
particle crit ~0 ~0.18 ~-4 0 0 0 0 1
particle crit ~2.8 ~0.18 ~2.8 0 0 0 0 1
particle crit ~-2.8 ~0.18 ~2.8 0 0 0 0 1
particle crit ~2.8 ~0.18 ~-2.8 0 0 0 0 1
particle crit ~-2.8 ~0.18 ~-2.8 0 0 0 0 1
