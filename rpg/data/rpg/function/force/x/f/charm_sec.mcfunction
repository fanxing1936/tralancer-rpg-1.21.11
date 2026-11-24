execute if score @s rpg_fo_end <= #now rpg_fo run return run function rpg:force/x/f/charm_end
particle minecraft:witch ~ ~2.1 ~ 0.2 0.1 0.2 0 3
tag @s add rpg.fo.chs
execute as @e[type=#rpg:seal_hostile,tag=!rpg.ally,distance=..10,limit=1,sort=nearest] at @s run function rpg:force/x/f/charm_bite
tag @s remove rpg.fo.chs
