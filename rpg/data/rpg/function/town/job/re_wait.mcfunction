scoreboard players add #wt rpg_tw 1
function rpg:town/job/big_loaded with storage rpg:town m
execute if score #ld rpg_tw matches 0 if score #wt rpg_tw matches ..120 run return 0
execute if score #ld rpg_tw matches 0 run return run function rpg:town/job/re_abort
execute store result storage rpg:town m.h int 1 run scoreboard players get #h0 rpg_tw
function rpg:town/job/re_wipe with storage rpg:town m
function rpg:town/job/build
