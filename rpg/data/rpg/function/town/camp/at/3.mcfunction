scoreboard players set #hm rpg_tw -999
execute positioned ~-12 0 ~-39 positioned over motion_blocking_no_leaves unless block ~ ~-1 ~ #rpg:town_clear run function rpg:town/s/max
execute positioned ~-12 0 ~-24 positioned over motion_blocking_no_leaves unless block ~ ~-1 ~ #rpg:town_clear run function rpg:town/s/max
execute positioned ~-12 0 ~-10 positioned over motion_blocking_no_leaves unless block ~ ~-1 ~ #rpg:town_clear run function rpg:town/s/max
execute positioned ~0 0 ~-39 positioned over motion_blocking_no_leaves unless block ~ ~-1 ~ #rpg:town_clear run function rpg:town/s/max
execute positioned ~0 0 ~-24 positioned over motion_blocking_no_leaves unless block ~ ~-1 ~ #rpg:town_clear run function rpg:town/s/max
execute positioned ~0 0 ~-10 positioned over motion_blocking_no_leaves unless block ~ ~-1 ~ #rpg:town_clear run function rpg:town/s/max
execute positioned ~12 0 ~-39 positioned over motion_blocking_no_leaves unless block ~ ~-1 ~ #rpg:town_clear run function rpg:town/s/max
execute positioned ~12 0 ~-24 positioned over motion_blocking_no_leaves unless block ~ ~-1 ~ #rpg:town_clear run function rpg:town/s/max
execute positioned ~12 0 ~-10 positioned over motion_blocking_no_leaves unless block ~ ~-1 ~ #rpg:town_clear run function rpg:town/s/max
scoreboard players remove #hm rpg_tw 2
execute store result storage rpg:town m.y int 1 run scoreboard players get #hm rpg_tw
function rpg:town/camp/put/3 with storage rpg:town m
