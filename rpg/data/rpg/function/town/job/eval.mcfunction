scoreboard players add #wt rpg_tw 1
function rpg:town/job/loaded with storage rpg:town m
execute if score #ld rpg_tw matches 0 if score #wt rpg_tw matches ..90 run return 0
execute if score #ld rpg_tw matches 1 if score #lw rpg_tw matches 0 run scoreboard players operation #lw rpg_tw = #wt rpg_tw
scoreboard players operation #since rpg_tw = #wt rpg_tw
scoreboard players operation #since rpg_tw -= #lw rpg_tw
execute if score #ld rpg_tw matches 1 if score #since rpg_tw matches ..2 run return 0
execute if score #ld rpg_tw matches 0 run return run function rpg:town/job/reject
function rpg:town/job/judge with storage rpg:town m
execute if score #ok rpg_tw matches 1 run return run function rpg:town/job/accept
function rpg:town/job/reject
