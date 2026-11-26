scoreboard players operation #b rpg_pa = @s rpg_pb_17
scoreboard players operation #b rpg_pa %= #2 rpg_pa
execute if score #b rpg_pa matches 0 run scoreboard players add @s rpg_pb_17 1
