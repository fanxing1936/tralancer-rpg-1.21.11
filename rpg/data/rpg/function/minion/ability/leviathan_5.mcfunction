# 布耶尔 · 处刑者（利维坦）：沉锚碾落
scoreboard players add #casts rpg_mn_tick 1
scoreboard players set @s rpg_mn_cd 79
scoreboard players set @s rpg_mn_cast 10
tag @s add rpg.demon.minion.casting
tellraw @a[distance=..4,gamemode=!spectator] ["",{"text":"[罪仆术式] ","color":"#1B4F72","bold":true,"italic":false},{"text":"布耶尔 · ","color":"#62D9E8","bold":false,"italic":false},{"text":"沉锚碾落","color":"#62D9E8","bold":true,"italic":false},{"text":"｜处刑者","color":"gray","bold":false,"italic":false},{"text":"　深海之口咬住近身猎物","color":"dark_gray","bold":false,"italic":false}]
playsound minecraft:entity.guardian.attack hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
playsound minecraft:entity.player.attack.strong hostile @a[distance=..14] ~ ~ ~ 0.28 0.92
particle dust_color_transition{from_color:[0.25,0.78,0.93],to_color:[0.02,0.16,0.31],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 4
particle crit ~4 ~0.18 ~0 0 0 0 0 1
particle crit ~-4 ~0.18 ~0 0 0 0 0 1
particle crit ~0 ~0.18 ~4 0 0 0 0 1
particle crit ~0 ~0.18 ~-4 0 0 0 0 1
particle crit ~2.8 ~0.18 ~2.8 0 0 0 0 1
particle crit ~-2.8 ~0.18 ~2.8 0 0 0 0 1
particle crit ~2.8 ~0.18 ~-2.8 0 0 0 0 1
particle crit ~-2.8 ~0.18 ~-2.8 0 0 0 0 1
