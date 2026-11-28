scoreboard players set @s rpg_mk_c 0
execute if score #ult rpg_mk_i3 matches 9 run scoreboard players add @s rpg_mk_ur 1
execute if score #ult rpg_mk_i3 matches 9 if score @s rpg_mk_ur matches 4.. run scoreboard players set @s rpg_mk_ur 1
execute if score #ult rpg_mk_i3 matches 9 run scoreboard players operation #ult rpg_mk_i3 = @s rpg_mk_ur
scoreboard players operation @s rpg_mk_ur = #ult rpg_mk_i3
execute if score #ult rpg_mk_i3 matches 1 run tag @s add rpg.mkb.u1
execute if score #ult rpg_mk_i3 matches 2 run tag @s add rpg.mkb.u2
execute if score #ult rpg_mk_i3 matches 3 run tag @s add rpg.mkb.u3
execute if score @s rpg_mk_i3 matches 1 if score #ult rpg_mk_i3 matches 1 run function rpg:michael_boss_i3/ult/who
execute if score @s rpg_mk_i3 matches 1 if score #ult rpg_mk_i3 matches 2 run function rpg:michael_boss_i3/ult/sanctus
execute if score @s rpg_mk_i3 matches 1 if score #ult rpg_mk_i3 matches 3 run function rpg:michael_boss_i3/ult/trumpet
execute if score @s rpg_mk_i3 matches 2 if score #ult rpg_mk_i3 matches 1 run function rpg:michael_boss_i3/ult/bones
execute if score @s rpg_mk_i3 matches 2 if score #ult rpg_mk_i3 matches 2 run function rpg:michael_boss_i3/ult/seraph
execute if score @s rpg_mk_i3 matches 2 if score #ult rpg_mk_i3 matches 3 run function rpg:michael_boss_i3/ult/stars
