# 失乐园页（as 玩家）
scoreboard players add @s rpg_pl_best 0
scoreboard players add @s rpg_pl_kill 0
scoreboard players add #moon rpg_pl 0
scoreboard players add #rain rpg_pl 0
execute store result storage rpg:paradise v.best int 1 run scoreboard players get @s rpg_pl_best
execute store result storage rpg:paradise v.kill int 1 run scoreboard players get @s rpg_pl_kill
execute store result storage rpg:paradise v.moon int 1 run scoreboard players get #moon rpg_pl
scoreboard players add #rain rpg_pl 0
execute store result storage rpg:paradise v.rain int 1 run scoreboard players get #rain rpg_pl
scoreboard players add @s rpg_vt_n 0
scoreboard players add @s rpg_vt_e 0
scoreboard players add @s rpg_vt_l 0
execute store result storage rpg:paradise v.vn int 1 run scoreboard players get @s rpg_vt_n
scoreboard players set #a rpg_pl 10
scoreboard players operation #a rpg_pl -= @s rpg_vt_e
execute store result storage rpg:paradise v.ve int 1 run scoreboard players get #a rpg_pl
scoreboard players set #a rpg_pl 40
scoreboard players operation #a rpg_pl -= @s rpg_vt_l
execute store result storage rpg:paradise v.vl int 1 run scoreboard players get #a rpg_pl
function rpg:pl/page_m with storage rpg:paradise v
