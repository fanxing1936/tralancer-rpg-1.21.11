execute if block ~ ~ ~ minecraft:soul_campfire align xyz positioned ~0.5 ~ ~0.5 run return run function rpg:bench/mark
execute unless block ~ ~ ~ #minecraft:replaceable run return 0
scoreboard players remove #i rpg_bn 1
execute if score #i rpg_bn matches 1.. positioned ^ ^ ^0.25 run function rpg:bench/ray
