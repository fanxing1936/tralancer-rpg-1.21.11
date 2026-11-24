# 失乐园页（as 玩家）
scoreboard players add @s rpg_pl_best 0
scoreboard players add @s rpg_pl_kill 0
scoreboard players add #moon rpg_pl 0
execute store result storage rpg:paradise v.best int 1 run scoreboard players get @s rpg_pl_best
execute store result storage rpg:paradise v.kill int 1 run scoreboard players get @s rpg_pl_kill
execute store result storage rpg:paradise v.moon int 1 run scoreboard players get #moon rpg_pl
function rpg:pl/page_m with storage rpg:paradise v
