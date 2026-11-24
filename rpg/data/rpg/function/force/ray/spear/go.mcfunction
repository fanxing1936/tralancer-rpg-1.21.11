scoreboard players set #r rpg_fo 40
scoreboard players set #stop rpg_fo 0
execute anchored eyes positioned ^ ^ ^0.6 run function rpg:force/ray/spear/step
tag @e[tag=rpg.fo.hit] remove rpg.fo.hit
