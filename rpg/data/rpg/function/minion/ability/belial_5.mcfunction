# 佛纽司 · 处刑者（贝利尔）：强制朝拜
scoreboard players add #casts rpg_mn_tick 1
scoreboard players set @s rpg_mn_cd 95
scoreboard players set @s rpg_mn_cast 10
tag @s add rpg.demon.minion.casting
tellraw @a[distance=..4,gamemode=!spectator] ["",{"text":"[罪仆术式] ","color":"#57256B","bold":true,"italic":false},{"text":"佛纽司 · ","color":"#C28BE0","bold":false,"italic":false},{"text":"强制朝拜","color":"#C28BE0","bold":true,"italic":false},{"text":"｜处刑者","color":"gray","bold":false,"italic":false},{"text":"　越想挣扎，镰刃便越沉重","color":"dark_gray","bold":false,"italic":false}]
playsound minecraft:entity.illusioner.prepare_blindness hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
playsound minecraft:entity.player.attack.strong hostile @a[distance=..14] ~ ~ ~ 0.28 0.92
particle dust_color_transition{from_color:[0.76,0.47,0.88],to_color:[0.18,0.04,0.25],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 4
particle crit ~4 ~0.18 ~0 0 0 0 0 1
particle crit ~-4 ~0.18 ~0 0 0 0 0 1
particle crit ~0 ~0.18 ~4 0 0 0 0 1
particle crit ~0 ~0.18 ~-4 0 0 0 0 1
particle crit ~2.8 ~0.18 ~2.8 0 0 0 0 1
particle crit ~-2.8 ~0.18 ~2.8 0 0 0 0 1
particle crit ~2.8 ~0.18 ~-2.8 0 0 0 0 1
particle crit ~-2.8 ~0.18 ~-2.8 0 0 0 0 1
