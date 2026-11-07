scoreboard players remove @s rpg_pact_fx 1
scoreboard players operation #c rpg_pact = @s rpg_pact_fx
scoreboard players operation #c rpg_pact %= #ten rpg_pact
execute unless score #c rpg_pact matches 0 run return 0
tag @s add rpg.pact.swarm
function rpg:pact/s/p4_swarm
tag @s remove rpg.pact.swarm
