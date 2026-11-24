execute store result score #d rpg_q_st run time query daytime
execute unless score #d rpg_q_st matches 5000..7000 run return 0
tag @s add rpg.q.sun
scoreboard players add @s rpg_q_em 1
execute if score @s rpg_q_em matches 3 run function rpg:quest/egg/meteor_go
