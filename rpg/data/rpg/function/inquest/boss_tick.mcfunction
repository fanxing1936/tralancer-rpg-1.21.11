# 只收七柱降临者；无名者仍沿用原来的直接战斗处置。
execute unless score @s rpg_dm_lord matches 1..7 run return 0
execute unless entity @s[tag=rpg.health700] run function rpg:inquest/init_health
execute unless entity @s[tag=rpg.inquest.intro] run function rpg:inquest/intro
scoreboard players add @s rpg_ex_stage 0
execute store result score @s rpg_ex_hp run data get entity @s Health 1
execute if entity @s[scores={rpg_ex_stage=0,rpg_ex_hp=..420}] run function rpg:inquest/suppress
execute if entity @s[scores={rpg_ex_stage=1}] run function rpg:inquest/stage1
execute if entity @s[scores={rpg_ex_stage=2..4}] run function rpg:inquest/bound_tick
