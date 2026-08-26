# 马尔巴士 · 处刑者（路西法）：王座裁落
scoreboard players add #casts rpg_mn_tick 1
scoreboard players set @s rpg_mn_cd 75
scoreboard players set @s rpg_mn_cast 10
tag @s add rpg.demon.minion.casting
tellraw @a[distance=..4,gamemode=!spectator] ["",{"text":"[罪仆术式] ","color":"#00491C","bold":true,"italic":false},{"text":"马尔巴士 · ","color":"#72D99A","bold":false,"italic":false},{"text":"王座裁落","color":"#72D99A","bold":true,"italic":false},{"text":"｜处刑者","color":"gray","bold":false,"italic":false},{"text":"　在近身处落下傲慢的裁决","color":"dark_gray","bold":false,"italic":false}]
playsound minecraft:entity.evoker.prepare_attack hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
playsound minecraft:entity.player.attack.strong hostile @a[distance=..14] ~ ~ ~ 0.28 0.92
particle dust_color_transition{from_color:[0.19,0.85,0.49],to_color:[0.0,0.18,0.07],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 4
particle crit ~4 ~0.18 ~0 0 0 0 0 1
particle crit ~-4 ~0.18 ~0 0 0 0 0 1
particle crit ~0 ~0.18 ~4 0 0 0 0 1
particle crit ~0 ~0.18 ~-4 0 0 0 0 1
particle crit ~2.8 ~0.18 ~2.8 0 0 0 0 1
particle crit ~-2.8 ~0.18 ~2.8 0 0 0 0 1
particle crit ~2.8 ~0.18 ~-2.8 0 0 0 0 1
particle crit ~-2.8 ~0.18 ~-2.8 0 0 0 0 1
