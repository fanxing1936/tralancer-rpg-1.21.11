execute store result score #x rpg_pl run data get entity @s Pos[0] 4
execute store result score #z rpg_pl run data get entity @s Pos[2] 4
execute unless score #x rpg_pl = @s rpg_pl_px run return run function rpg:pl/leave_stop
execute unless score #z rpg_pl = @s rpg_pl_pz run return run function rpg:pl/leave_stop
scoreboard players remove @s rpg_pl_lv 1
particle minecraft:crimson_spore ~ ~1 ~ 0.5 1 0.5 0 40
execute if score @s rpg_pl_lv matches 0 run function rpg:pl/back
