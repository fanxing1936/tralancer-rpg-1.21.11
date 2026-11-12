scoreboard players add #d rpg_l2_v 1
execute if entity @s[distance=..1.3] run return 0
execute positioned ~ ~-1.6 ~ if entity @s[distance=..1.3] run return 0
execute if score #d rpg_l2_v matches ..24 positioned ^ ^ ^1 run function rpg:lucifer_fight/fx/line_step
