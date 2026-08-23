# 圣水浇在空壳上。壳撑不了那么久 —— 被浇过的裂得快得多。
effect give @s minecraft:glowing 4 0 true
scoreboard players add @s rpg_vac_x 20
particle sculk_soul ~ ~1.2 ~ 0.3 0.4 0.3 0.04 16
particle smoke ~ ~1 ~ 0.2 0.3 0.2 0.02 10
playsound minecraft:block.lava.extinguish hostile @a[distance=..16] ~ ~ ~ 0.8 1.4
execute if entity @s[scores={rpg_vac_x=60..},tag=!rpg.vac.torn] run function rpg:vacant/tear
