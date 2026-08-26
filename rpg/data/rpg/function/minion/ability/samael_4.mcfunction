# 纳贝流士 · 咒使（萨麦尔）：死亡低语
scoreboard players add #casts rpg_mn_tick 1
scoreboard players set @s rpg_mn_cd 116
scoreboard players set @s rpg_mn_cast 20
tag @s add rpg.demon.minion.casting
tellraw @a[distance=..8,gamemode=!spectator] ["",{"text":"[罪仆术式] ","color":"#7B241C","bold":true,"italic":false},{"text":"纳贝流士 · ","color":"#FF665E","bold":false,"italic":false},{"text":"死亡低语","color":"#FF665E","bold":true,"italic":false},{"text":"｜咒使","color":"gray","bold":false,"italic":false},{"text":"　怒火扰乱周围的判断","color":"dark_gray","bold":false,"italic":false}]
playsound minecraft:entity.ravager.roar hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
playsound minecraft:entity.evoker.cast_spell hostile @a[distance=..14] ~ ~ ~ 0.28 0.92
particle dust_color_transition{from_color:[0.94,0.20,0.18],to_color:[0.25,0.01,0.01],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 4
particle soul_fire_flame ~8 ~0.18 ~0 0 0 0 0 1
particle soul_fire_flame ~-8 ~0.18 ~0 0 0 0 0 1
particle soul_fire_flame ~0 ~0.18 ~8 0 0 0 0 1
particle soul_fire_flame ~0 ~0.18 ~-8 0 0 0 0 1
particle soul_fire_flame ~5.6 ~0.18 ~5.6 0 0 0 0 1
particle soul_fire_flame ~-5.6 ~0.18 ~5.6 0 0 0 0 1
particle soul_fire_flame ~5.6 ~0.18 ~-5.6 0 0 0 0 1
particle soul_fire_flame ~-5.6 ~0.18 ~-5.6 0 0 0 0 1
