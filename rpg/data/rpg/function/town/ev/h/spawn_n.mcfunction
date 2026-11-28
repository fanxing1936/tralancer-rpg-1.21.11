execute store result score #rx rpg_te run random value -6..6
execute store result score #rz rpg_te run random value -5..5
execute store result storage rpg:town hv.x int 1 run scoreboard players get #rx rpg_te
execute store result storage rpg:town hv.z int 1 run scoreboard players get #rz rpg_te
function rpg:town/ev/h/spawn_one with storage rpg:town hv
scoreboard players remove #k rpg_te 1
execute if score #k rpg_te matches 1.. run function rpg:town/ev/h/spawn_n
