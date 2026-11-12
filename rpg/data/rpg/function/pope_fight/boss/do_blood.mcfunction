execute unless entity @e[type=minecraft:vindicator,tag=rpg.pf.sac,limit=1] run return run function rpg:pope_fight/boss/blood_broken
execute if score #st rpg_pf matches 34.. run return run function rpg:pope_fight/boss/blood_done
execute if score #st rpg_pf matches 7 positioned ^0.54 ^1.68 ^1.68 run function rpg:pope_fight/fx/line
execute if score #st rpg_pf matches 7.. if score #h rpg_pf matches 0 run function rpg:pope_fight/boss/blood_line
