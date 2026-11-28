$execute if score #s$(i) rpg_tw matches 3 run return run function rpg:town/home/arrive
$execute if score #s$(i) rpg_tw matches 4 run return run function rpg:town/home/other
$execute if score #s$(i) rpg_tw matches 0 run scoreboard players set #s$(i) rpg_tw 1
function rpg:town/home/hold
