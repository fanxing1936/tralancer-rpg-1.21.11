# 立约者的一刻：三条冷却、附身和蝇群。
execute if score @s rpg_pact_cd2 matches 1.. run scoreboard players remove @s rpg_pact_cd2 1
execute if score @s rpg_pact_cd3 matches 1.. run scoreboard players remove @s rpg_pact_cd3 1
execute if score @s rpg_pact_av matches 1.. at @s run function rpg:pact/depth/avatar_tick
execute if score @s rpg_pact_fx matches 1.. at @s run function rpg:pact/depth/swarm_tick
