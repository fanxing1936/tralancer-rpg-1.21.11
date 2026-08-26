# 塞列欧斯 · 咒使（别西卜）：蝇幕蚀志
scoreboard players add #casts rpg_mn_tick 1
scoreboard players set @s rpg_mn_cd 112
scoreboard players set @s rpg_mn_cast 20
tag @s add rpg.demon.minion.casting
tellraw @a[distance=..8,gamemode=!spectator] ["",{"text":"[罪仆术式] ","color":"#596B18","bold":true,"italic":false},{"text":"塞列欧斯 · ","color":"#B5D957","bold":false,"italic":false},{"text":"蝇幕蚀志","color":"#B5D957","bold":true,"italic":false},{"text":"｜咒使","color":"gray","bold":false,"italic":false},{"text":"　腐败气息令众人饥饿作呕","color":"dark_gray","bold":false,"italic":false}]
playsound minecraft:entity.spider.ambient hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
playsound minecraft:entity.evoker.cast_spell hostile @a[distance=..14] ~ ~ ~ 0.28 0.92
particle dust_color_transition{from_color:[0.70,0.84,0.34],to_color:[0.18,0.23,0.05],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 4
particle spore_blossom_air ~8 ~0.18 ~0 0 0 0 0 1
particle spore_blossom_air ~-8 ~0.18 ~0 0 0 0 0 1
particle spore_blossom_air ~0 ~0.18 ~8 0 0 0 0 1
particle spore_blossom_air ~0 ~0.18 ~-8 0 0 0 0 1
particle spore_blossom_air ~5.6 ~0.18 ~5.6 0 0 0 0 1
particle spore_blossom_air ~-5.6 ~0.18 ~5.6 0 0 0 0 1
particle spore_blossom_air ~5.6 ~0.18 ~-5.6 0 0 0 0 1
particle spore_blossom_air ~-5.6 ~0.18 ~-5.6 0 0 0 0 1
