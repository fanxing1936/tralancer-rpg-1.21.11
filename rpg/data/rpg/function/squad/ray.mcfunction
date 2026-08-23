# 视线上的 24 格，每 0.5 格取一个点。`positioned ^ ^ ^N` 取点，
# 命中即 return，不用递归。取点间隔比命中半径小 —— 否则小生物会从两点之间漏过去。
execute positioned ^ ^ ^0.5 if entity @e[distance=..0.52,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^0.5 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^1 if entity @e[distance=..0.55,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^1 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^1.5 if entity @e[distance=..0.57,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^1.5 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^2 if entity @e[distance=..0.59,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^2 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^2.5 if entity @e[distance=..0.61,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^2.5 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^3 if entity @e[distance=..0.64,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^3 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^3.5 if entity @e[distance=..0.66,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^3.5 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^4 if entity @e[distance=..0.68,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^4 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^4.5 if entity @e[distance=..0.70,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^4.5 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^5 if entity @e[distance=..0.72,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^5 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^5.5 if entity @e[distance=..0.75,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^5.5 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^6 if entity @e[distance=..0.77,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^6 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^6.5 if entity @e[distance=..0.79,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^6.5 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^7 if entity @e[distance=..0.81,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^7 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^7.5 if entity @e[distance=..0.84,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^7.5 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^8 if entity @e[distance=..0.86,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^8 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^8.5 if entity @e[distance=..0.88,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^8.5 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^9 if entity @e[distance=..0.91,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^9 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^9.5 if entity @e[distance=..0.93,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^9.5 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^10 if entity @e[distance=..0.95,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^10 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^10.5 if entity @e[distance=..0.97,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^10.5 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^11 if entity @e[distance=..0.99,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^11 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^11.5 if entity @e[distance=..1.02,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^11.5 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^12 if entity @e[distance=..1.04,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^12 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^12.5 if entity @e[distance=..1.06,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^12.5 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^13 if entity @e[distance=..1.08,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^13 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^13.5 if entity @e[distance=..1.11,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^13.5 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^14 if entity @e[distance=..1.13,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^14 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^14.5 if entity @e[distance=..1.15,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^14.5 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^15 if entity @e[distance=..1.17,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^15 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^15.5 if entity @e[distance=..1.20,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^15.5 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^16 if entity @e[distance=..1.22,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^16 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^16.5 if entity @e[distance=..1.24,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^16.5 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^17 if entity @e[distance=..1.27,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^17 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^17.5 if entity @e[distance=..1.29,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^17.5 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^18 if entity @e[distance=..1.31,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^18 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^18.5 if entity @e[distance=..1.33,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^18.5 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^19 if entity @e[distance=..1.35,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^19 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^19.5 if entity @e[distance=..1.38,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^19.5 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^20 if entity @e[distance=..1.40,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^20 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^20.5 if entity @e[distance=..1.42,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^20.5 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^21 if entity @e[distance=..1.44,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^21 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^21.5 if entity @e[distance=..1.47,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^21.5 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^22 if entity @e[distance=..1.49,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^22 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^22.5 if entity @e[distance=..1.51,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^22.5 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^23 if entity @e[distance=..1.53,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^23 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^23.5 if entity @e[distance=..1.56,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^23.5 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
execute positioned ^ ^ ^24 if entity @e[distance=..1.58,type=!#rpg:sq_ignore,tag=!rpg.squad,tag=!rpg.merc,tag=!rpg.sq.board,tag=!rpg.doll,limit=1] run return run function rpg:squad/mark
execute positioned ^ ^ ^24 unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:squad/miss
function rpg:squad/miss
