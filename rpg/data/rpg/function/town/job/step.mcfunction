execute if score #cool rpg_tw matches 1.. run return run scoreboard players remove #cool rpg_tw 1
execute if score #ph rpg_tw matches 0 run return run function rpg:town/job/probe
execute if score #ph rpg_tw matches 1 run return run function rpg:town/job/eval
execute if score #ph rpg_tw matches 2 run return run function rpg:town/job/wait_build
execute if score #ph rpg_tw matches 3 run return run function rpg:town/job/camp_wait
execute if score #ph rpg_tw matches 4 run return run function rpg:town/job/re_wait
