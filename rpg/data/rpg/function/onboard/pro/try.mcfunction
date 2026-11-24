scoreboard players set @s rpg_ob_t 0
execute if score #state rpg_pr matches 1.. run return run function rpg:onboard/pro/wait
execute if score #fight rpg_mk matches 1 run return run function rpg:onboard/pro/wait
tag @s remove rpg.ob.hold
effect clear @s minecraft:blindness
tag @s add rpg.ob.pro
function rpg:onboard/pro/go
