# 亚斯塔禄 · 咒使（贝利尔）：感官倒悬
scoreboard players add #casts rpg_mn_tick 1
scoreboard players set @s rpg_mn_cd 120
scoreboard players set @s rpg_mn_cast 20
tag @s add rpg.demon.minion.casting
tellraw @a[distance=..8,gamemode=!spectator] ["",{"text":"[罪仆术式] ","color":"#57256B","bold":true,"italic":false},{"text":"亚斯塔禄 · ","color":"#C28BE0","bold":false,"italic":false},{"text":"感官倒悬","color":"#C28BE0","bold":true,"italic":false},{"text":"｜咒使","color":"gray","bold":false,"italic":false},{"text":"　沉重梦境封住周围的动作","color":"dark_gray","bold":false,"italic":false}]
playsound minecraft:entity.illusioner.prepare_blindness hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
playsound minecraft:entity.evoker.cast_spell hostile @a[distance=..14] ~ ~ ~ 0.28 0.92
particle dust_color_transition{from_color:[0.76,0.47,0.88],to_color:[0.18,0.04,0.25],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 4
particle witch ~8 ~0.18 ~0 0 0 0 0 1
particle witch ~-8 ~0.18 ~0 0 0 0 0 1
particle witch ~0 ~0.18 ~8 0 0 0 0 1
particle witch ~0 ~0.18 ~-8 0 0 0 0 1
particle witch ~5.6 ~0.18 ~5.6 0 0 0 0 1
particle witch ~-5.6 ~0.18 ~5.6 0 0 0 0 1
particle witch ~5.6 ~0.18 ~-5.6 0 0 0 0 1
particle witch ~-5.6 ~0.18 ~-5.6 0 0 0 0 1
