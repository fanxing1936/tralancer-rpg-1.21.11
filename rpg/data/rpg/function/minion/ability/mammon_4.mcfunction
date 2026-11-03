# 佛尔佛尔 · 咒使（玛门）：重税
scoreboard players add #casts rpg_mn_tick 1
scoreboard players set @s rpg_mn_cd 124
scoreboard players set @s rpg_mn_cast 20
tag @s add rpg.demon.minion.casting
tellraw @a[distance=..8,gamemode=!spectator] ["",{"text":"[罪仆术式] ","color":"#E6A23C","bold":true,"italic":false},{"text":"佛尔佛尔 · ","color":"#FFFFFF","bold":false,"italic":false},{"text":"重税","color":"#E6A23C","bold":true,"italic":false},{"text":"｜咒使","color":"gray","bold":false,"italic":false},{"text":"　无形债契拖慢所有偿还者","color":"dark_gray","bold":false,"italic":false}]
playsound minecraft:block.amethyst_block.chime hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
playsound minecraft:entity.evoker.cast_spell hostile @a[distance=..14] ~ ~ ~ 0.28 0.92
particle dust_color_transition{from_color:[0.9,0.64,0.24],to_color:[0.72,0.58,0.04],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 4
particle wax_on ~8 ~0.18 ~0 0 0 0 0 1
particle wax_on ~-8 ~0.18 ~0 0 0 0 0 1
particle wax_on ~0 ~0.18 ~8 0 0 0 0 1
particle wax_on ~0 ~0.18 ~-8 0 0 0 0 1
particle wax_on ~5.6 ~0.18 ~5.6 0 0 0 0 1
particle wax_on ~-5.6 ~0.18 ~5.6 0 0 0 0 1
particle wax_on ~5.6 ~0.18 ~-5.6 0 0 0 0 1
particle wax_on ~-5.6 ~0.18 ~-5.6 0 0 0 0 1
