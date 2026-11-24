tag @s add rpg.mer.old
execute rotated as @s run function rpg:merchant/place/mystery
scoreboard players operation @e[type=minecraft:villager,tag=rpg.mer.mystery,tag=!rpg.mer.old,distance=..0.1] rpg_mer_day = #day rpg_ev
particle minecraft:poof ~ ~1 ~ 0.3 0.6 0.3 0.05 20
function rpg:merchant/gone
