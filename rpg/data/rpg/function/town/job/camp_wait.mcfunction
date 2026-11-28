function rpg:town/job/items with storage rpg:town m
scoreboard players add #wt rpg_tw 1
function rpg:town/job/loaded with storage rpg:town m
execute if score #ld rpg_tw matches 0 if score #wt rpg_tw matches ..60 run return 0
execute if score #ld rpg_tw matches 1 run function rpg:town/job/camp_go with storage rpg:town m
execute if score #ld rpg_tw matches 1 run function #rpg:camp_built
function rpg:town/job/fl_rem with storage rpg:town m
function rpg:town/job/done
