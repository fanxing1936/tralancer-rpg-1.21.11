scoreboard players set #mn rpg_tw 9999
scoreboard players set #mx rpg_tw -9999
scoreboard players set #ok rpg_tw 1
execute positioned ~12 0 ~-15 positioned over motion_blocking_no_leaves run function rpg:town/s/mm
execute positioned ~12 0 ~0 positioned over motion_blocking_no_leaves run function rpg:town/s/mm
execute positioned ~12 0 ~14 positioned over motion_blocking_no_leaves run function rpg:town/s/mm
execute positioned ~24 0 ~-15 positioned over motion_blocking_no_leaves run function rpg:town/s/mm
execute positioned ~24 0 ~0 positioned over motion_blocking_no_leaves run function rpg:town/s/mm
execute positioned ~24 0 ~14 positioned over motion_blocking_no_leaves run function rpg:town/s/mm
execute positioned ~36 0 ~-15 positioned over motion_blocking_no_leaves run function rpg:town/s/mm
execute positioned ~36 0 ~0 positioned over motion_blocking_no_leaves run function rpg:town/s/mm
execute positioned ~36 0 ~14 positioned over motion_blocking_no_leaves run function rpg:town/s/mm
scoreboard players operation #sp rpg_tw = #mx rpg_tw
scoreboard players operation #sp rpg_tw -= #mn rpg_tw
execute if score #ok rpg_tw matches 0 run scoreboard players add #sp rpg_tw 1000
execute if score #mn rpg_tw matches ..62 run scoreboard players add #sp rpg_tw 1000
execute if score #sp rpg_tw < #best rpg_tw run scoreboard players set #bn rpg_tw 7
execute if score #sp rpg_tw < #best rpg_tw run scoreboard players operation #best rpg_tw = #sp rpg_tw
