execute unless entity @e[type=minecraft:vindicator,tag=rpg.pf.sac,limit=1] run return run function rpg:pope_fight/boss/blood_broken
execute if score #st rpg_pf matches 50.. run return run function rpg:pope_fight/boss/blood_done
execute if score #st rpg_pf matches 18 positioned ^0.43 ^2.90 ^0.57 run function rpg:pope_fight/fx/line
execute if score #st rpg_pf matches 18.. if score #h rpg_pf matches 0 run function rpg:pope_fight/boss/blood_line
