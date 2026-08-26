# 布涅 · 先锋（贝利尔）：紫宴护幕
scoreboard players add #casts rpg_mn_tick 1
scoreboard players set @s rpg_mn_cd 130
scoreboard players set @s rpg_mn_cast 10
tag @s add rpg.demon.minion.casting
tellraw @a[distance=..12,gamemode=!spectator] ["",{"text":"[罪仆术式] ","color":"#57256B","bold":true,"italic":false},{"text":"布涅 · ","color":"#C28BE0","bold":false,"italic":false},{"text":"紫宴护幕","color":"#C28BE0","bold":true,"italic":false},{"text":"｜先锋","color":"gray","bold":false,"italic":false},{"text":"　静止本身成为同柱的护甲","color":"dark_gray","bold":false,"italic":false}]
playsound minecraft:entity.illusioner.prepare_blindness hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
playsound minecraft:item.shield.block hostile @a[distance=..14] ~ ~ ~ 0.28 0.92
particle dust_color_transition{from_color:[0.76,0.47,0.88],to_color:[0.18,0.04,0.25],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 4
particle enchant ~ ~1 ~ 0.72 0.18 0.72 0.025 8
