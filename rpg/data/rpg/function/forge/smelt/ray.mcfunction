execute if block ~ ~ ~ #rpg:forge/soul_fire run return run function rpg:forge/smelt/found
scoreboard players remove #i rpg_fg 1
execute if score #i rpg_fg matches 1.. positioned ^ ^ ^0.2 run function rpg:forge/smelt/ray
