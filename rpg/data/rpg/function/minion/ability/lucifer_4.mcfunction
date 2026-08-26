# 萨米基纳 · 咒使（路西法）：失坠敕令
scoreboard players add #casts rpg_mn_tick 1
scoreboard players set @s rpg_mn_cd 100
scoreboard players set @s rpg_mn_cast 20
tag @s add rpg.demon.minion.casting
tellraw @a[distance=..8,gamemode=!spectator] ["",{"text":"[罪仆术式] ","color":"#00491C","bold":true,"italic":false},{"text":"萨米基纳 · ","color":"#72D99A","bold":false,"italic":false},{"text":"失坠敕令","color":"#72D99A","bold":true,"italic":false},{"text":"｜咒使","color":"gray","bold":false,"italic":false},{"text":"　压低周围凡人的力量与动作","color":"dark_gray","bold":false,"italic":false}]
playsound minecraft:entity.evoker.prepare_attack hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
playsound minecraft:entity.evoker.cast_spell hostile @a[distance=..14] ~ ~ ~ 0.28 0.92
particle dust_color_transition{from_color:[0.19,0.85,0.49],to_color:[0.0,0.18,0.07],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 4
particle end_rod ~8 ~0.18 ~0 0 0 0 0 1
particle end_rod ~-8 ~0.18 ~0 0 0 0 0 1
particle end_rod ~0 ~0.18 ~8 0 0 0 0 1
particle end_rod ~0 ~0.18 ~-8 0 0 0 0 1
particle end_rod ~5.6 ~0.18 ~5.6 0 0 0 0 1
particle end_rod ~-5.6 ~0.18 ~5.6 0 0 0 0 1
particle end_rod ~5.6 ~0.18 ~-5.6 0 0 0 0 1
particle end_rod ~-5.6 ~0.18 ~-5.6 0 0 0 0 1
