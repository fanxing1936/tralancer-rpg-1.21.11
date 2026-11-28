execute store result score #r rpg_te run random value 0..1
execute if score #r rpg_te matches 0 run return run function rpg:town/ev/r/rw02
execute if score #r rpg_te matches 1 run return run function rpg:town/ev/r/rw04
