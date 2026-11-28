scoreboard players set #hm rpg_tw -999
execute positioned ~9 0 ~-36 positioned over motion_blocking_no_leaves unless block ~ ~-1 ~ #rpg:town_clear run function rpg:town/s/max
execute positioned ~9 0 ~-24 positioned over motion_blocking_no_leaves unless block ~ ~-1 ~ #rpg:town_clear run function rpg:town/s/max
execute positioned ~9 0 ~-12 positioned over motion_blocking_no_leaves unless block ~ ~-1 ~ #rpg:town_clear run function rpg:town/s/max
execute positioned ~24 0 ~-36 positioned over motion_blocking_no_leaves unless block ~ ~-1 ~ #rpg:town_clear run function rpg:town/s/max
execute positioned ~24 0 ~-24 positioned over motion_blocking_no_leaves unless block ~ ~-1 ~ #rpg:town_clear run function rpg:town/s/max
execute positioned ~24 0 ~-12 positioned over motion_blocking_no_leaves unless block ~ ~-1 ~ #rpg:town_clear run function rpg:town/s/max
execute positioned ~38 0 ~-36 positioned over motion_blocking_no_leaves unless block ~ ~-1 ~ #rpg:town_clear run function rpg:town/s/max
execute positioned ~38 0 ~-24 positioned over motion_blocking_no_leaves unless block ~ ~-1 ~ #rpg:town_clear run function rpg:town/s/max
execute positioned ~38 0 ~-12 positioned over motion_blocking_no_leaves unless block ~ ~-1 ~ #rpg:town_clear run function rpg:town/s/max
scoreboard players remove #hm rpg_tw 2
execute store result storage rpg:town m.y int 1 run scoreboard players get #hm rpg_tw
function rpg:town/camp/put/6 with storage rpg:town m
