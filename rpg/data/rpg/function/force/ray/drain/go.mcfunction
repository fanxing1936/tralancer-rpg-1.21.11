scoreboard players set #r rpg_fo 32
scoreboard players set #stop rpg_fo 0
execute anchored eyes positioned ^ ^ ^0.6 run function rpg:force/ray/drain/step
tag @e[tag=rpg.fo.hit] remove rpg.fo.hit
