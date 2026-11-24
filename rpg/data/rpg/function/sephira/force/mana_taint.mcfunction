# 魔力者（as 玩家）：魔化每涨 1 点，魔力 +3；弥赛亚的魔化增长减半
scoreboard players operation #d rpg_sef = @s rpg_taint
scoreboard players operation #d rpg_sef -= @s rpg_fz_tp
execute if score #d rpg_sef matches 1.. if score @s rpg_messiah matches 1 run function rpg:sephira/force/halve
execute if score #d rpg_sef matches 1.. run scoreboard players operation #d rpg_sef *= #3 rpg_sef
execute if score #d rpg_sef matches 1.. if score @s rpg_force matches 2 run scoreboard players operation @s rpg_mana += #d rpg_sef
execute if score #d rpg_sef matches 1.. if score @s rpg_force matches 3 run scoreboard players operation @s rpg_mana2 += #d rpg_sef
scoreboard players operation @s rpg_fz_tp = @s rpg_taint
