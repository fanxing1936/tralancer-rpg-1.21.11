scoreboard objectives add rpg_pl dummy
scoreboard objectives add rpg_pl_best dummy
scoreboard objectives add rpg_pl_kill dummy
scoreboard objectives add rpg_pl_lv dummy
scoreboard objectives add rpg_pl_px dummy
scoreboard objectives add rpg_pl_pz dummy
scoreboard objectives add rpg_pl_er dummy
scoreboard objectives add rpg_pl_tree dummy
scoreboard objectives add rpg_pl_dc deathCount
scoreboard players add #built rpg_pl 0
scoreboard players set #2 rpg_pl 2
scoreboard players set #100 rpg_pl 100
scoreboard players add #c1 rpg_pl 0
scoreboard players add #c2 rpg_pl 0
scoreboard players add #c3 rpg_pl 0
scoreboard players add #c4 rpg_pl 0
scoreboard players set #2 rpg_el 2
scoreboard players set #4 rpg_el 4
execute if score #built rpg_pl matches 2..8 run function rpg:pl/prepare
scoreboard objectives add rpg_pl_tb dummy
scoreboard objectives add rpg_pl_fort dummy
