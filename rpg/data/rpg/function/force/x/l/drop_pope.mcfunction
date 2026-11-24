# 首杀必掉，之后每次 20%
execute if score @s rpg_bk_pope matches 1 run return run function rpg:force/x/l/give_31
execute store result score #r rpg_fo run random value 1..5
execute if score #r rpg_fo matches 1 run function rpg:force/x/l/give_31
