scoreboard players set @s rpg_mk_c 0
execute if score #ult rpg_mk matches 9 run scoreboard players add @s rpg_mk_ur 1
execute if score #ult rpg_mk matches 9 if score @s rpg_mk_ur matches 4.. run scoreboard players set @s rpg_mk_ur 1
execute if score #ult rpg_mk matches 9 run scoreboard players operation #ult rpg_mk = @s rpg_mk_ur
scoreboard players operation @s rpg_mk_ur = #ult rpg_mk
execute if score #ult rpg_mk matches 1 run tag @s add rpg.mkb.u1
execute if score #ult rpg_mk matches 2 run tag @s add rpg.mkb.u2
execute if score #ult rpg_mk matches 3 run tag @s add rpg.mkb.u3
execute if score @s rpg_mk matches 1 if score #ult rpg_mk matches 1 run function rpg:michael_boss/ult/who
execute if score @s rpg_mk matches 1 if score #ult rpg_mk matches 2 run function rpg:michael_boss/ult/sanctus
execute if score @s rpg_mk matches 1 if score #ult rpg_mk matches 3 run function rpg:michael_boss/ult/trumpet
execute if score @s rpg_mk matches 2 if score #ult rpg_mk matches 1 run function rpg:michael_boss/ult/bones
execute if score @s rpg_mk matches 2 if score #ult rpg_mk matches 2 run function rpg:michael_boss/ult/seraph
execute if score @s rpg_mk matches 2 if score #ult rpg_mk matches 3 run function rpg:michael_boss/ult/stars
