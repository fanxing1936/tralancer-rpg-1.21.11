scoreboard players operation @s rpg_lu_dx = @s rpg_lu_x
scoreboard players operation @s rpg_lu_dz = @s rpg_lu_z
function rpg:lucifer_lord/movement/store
scoreboard players operation @s rpg_lu_dx -= @s rpg_lu_x
scoreboard players operation @s rpg_lu_dz -= @s rpg_lu_z
scoreboard players set @s rpg_lu_move 0
execute unless score @s rpg_lu_dx matches -3..3 run scoreboard players set @s rpg_lu_move 1
execute unless score @s rpg_lu_dz matches -3..3 run scoreboard players set @s rpg_lu_move 1
execute if score @s rpg_lu_anim matches 0 if score @s rpg_lu_move matches 1 run function rpg:lucifer_lord/anim/enter/walk
execute if score @s rpg_lu_anim matches 1 if score @s rpg_lu_move matches 0 run function rpg:lucifer_lord/anim/enter/idle
