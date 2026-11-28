scoreboard players add #wt rpg_tw 1
function rpg:town/job/big_loaded with storage rpg:town m
execute if score #ld rpg_tw matches 0 if score #wt rpg_tw matches ..90 run return 0
function rpg:town/job/wide with storage rpg:town m
execute if score #ok rpg_tw matches 0 run return run function rpg:town/job/wide_fail
function rpg:town/job/build
