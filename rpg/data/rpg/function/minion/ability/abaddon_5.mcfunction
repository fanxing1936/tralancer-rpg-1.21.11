# 艾利欧格 · 处刑者（亚巴顿）：刈魂
scoreboard players add #casts rpg_mn_tick 1
scoreboard players set @s rpg_mn_cd 83
scoreboard players set @s rpg_mn_cast 10
tag @s add rpg.demon.minion.casting
tellraw @a[distance=..4,gamemode=!spectator] ["",{"text":"[罪仆术式] ","color":"#5B5B62","bold":true,"italic":false},{"text":"艾利欧格 · ","color":"#C2C2CC","bold":false,"italic":false},{"text":"刈魂","color":"#C2C2CC","bold":true,"italic":false},{"text":"｜处刑者","color":"gray","bold":false,"italic":false},{"text":"　丧钟为近身者预告终点","color":"dark_gray","bold":false,"italic":false}]
playsound minecraft:entity.warden.heartbeat hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
playsound minecraft:entity.player.attack.strong hostile @a[distance=..14] ~ ~ ~ 0.28 0.92
particle dust_color_transition{from_color:[0.76,0.76,0.82],to_color:[0.10,0.10,0.12],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 4
particle crit ~4 ~0.18 ~0 0 0 0 0 1
particle crit ~-4 ~0.18 ~0 0 0 0 0 1
particle crit ~0 ~0.18 ~4 0 0 0 0 1
particle crit ~0 ~0.18 ~-4 0 0 0 0 1
particle crit ~2.8 ~0.18 ~2.8 0 0 0 0 1
particle crit ~-2.8 ~0.18 ~2.8 0 0 0 0 1
particle crit ~2.8 ~0.18 ~-2.8 0 0 0 0 1
particle crit ~-2.8 ~0.18 ~-2.8 0 0 0 0 1
