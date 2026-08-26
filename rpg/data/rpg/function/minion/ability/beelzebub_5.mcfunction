# 布松 · 处刑者（别西卜）：饥啮
scoreboard players add #casts rpg_mn_tick 1
scoreboard players set @s rpg_mn_cd 87
scoreboard players set @s rpg_mn_cast 10
tag @s add rpg.demon.minion.casting
tellraw @a[distance=..4,gamemode=!spectator] ["",{"text":"[罪仆术式] ","color":"#596B18","bold":true,"italic":false},{"text":"布松 · ","color":"#B5D957","bold":false,"italic":false},{"text":"饥啮","color":"#B5D957","bold":true,"italic":false},{"text":"｜处刑者","color":"gray","bold":false,"italic":false},{"text":"　饥饿在近身处同时张口","color":"dark_gray","bold":false,"italic":false}]
playsound minecraft:entity.spider.ambient hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
playsound minecraft:entity.player.attack.strong hostile @a[distance=..14] ~ ~ ~ 0.28 0.92
particle dust_color_transition{from_color:[0.70,0.84,0.34],to_color:[0.18,0.23,0.05],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 4
particle crit ~4 ~0.18 ~0 0 0 0 0 1
particle crit ~-4 ~0.18 ~0 0 0 0 0 1
particle crit ~0 ~0.18 ~4 0 0 0 0 1
particle crit ~0 ~0.18 ~-4 0 0 0 0 1
particle crit ~2.8 ~0.18 ~2.8 0 0 0 0 1
particle crit ~-2.8 ~0.18 ~2.8 0 0 0 0 1
particle crit ~2.8 ~0.18 ~-2.8 0 0 0 0 1
particle crit ~-2.8 ~0.18 ~-2.8 0 0 0 0 1
