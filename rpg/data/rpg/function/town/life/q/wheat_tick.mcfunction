execute if entity @e[type=minecraft:marker,tag=rpg.tw.in.granary,distance=..12] run scoreboard players add #wq rpg_tl 1
execute if entity @e[type=minecraft:marker,tag=rpg.tw.in.granary,distance=..12] run function rpg:town/life/q/wheat_step
