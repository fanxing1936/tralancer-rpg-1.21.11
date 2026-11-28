scoreboard players operation #hp rpg_te = #np rpg_te
scoreboard players operation #hp rpg_te *= #50 rpg_te
scoreboard players add #hp rpg_te 110
execute store result storage rpg:town hp.v int 1 run scoreboard players get #hp rpg_te
function rpg:town/ev/set_hp with storage rpg:town hp
