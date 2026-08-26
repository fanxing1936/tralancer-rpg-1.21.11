# 桀派 · 先锋（别西卜）：腐宴护壳
scoreboard players add #casts rpg_mn_tick 1
scoreboard players set @s rpg_mn_cd 122
scoreboard players set @s rpg_mn_cast 10
tag @s add rpg.demon.minion.casting
tellraw @a[distance=..12,gamemode=!spectator] ["",{"text":"[罪仆术式] ","color":"#596B18","bold":true,"italic":false},{"text":"桀派 · ","color":"#B5D957","bold":false,"italic":false},{"text":"腐宴护壳","color":"#B5D957","bold":true,"italic":false},{"text":"｜先锋","color":"gray","bold":false,"italic":false},{"text":"　饕宴残渣凝成带刺甲壳","color":"dark_gray","bold":false,"italic":false}]
playsound minecraft:entity.spider.ambient hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
playsound minecraft:item.shield.block hostile @a[distance=..14] ~ ~ ~ 0.28 0.92
particle dust_color_transition{from_color:[0.70,0.84,0.34],to_color:[0.18,0.23,0.05],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 4
particle enchant ~ ~1 ~ 0.72 0.18 0.72 0.025 8
