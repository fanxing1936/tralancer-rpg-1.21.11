# 伸手不一定够得着。
execute store result score @s rpg_vac run random value 1..4
execute if entity @s[scores={rpg_vac=1}] run function rpg:vacant/creep_do
