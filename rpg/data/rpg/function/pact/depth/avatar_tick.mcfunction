scoreboard players remove @s rpg_pact_av 1
execute if score @s rpg_pact_av matches 0 run return run function rpg:pact/depth/avatar_end
scoreboard players operation #c rpg_pact = @s rpg_pact_av
scoreboard players operation #c rpg_pact %= #five rpg_pact
execute unless score #c rpg_pact matches 0 run return 0
execute if score @s rpg_pact matches 1 run function rpg:pact/s/aura1
execute if score @s rpg_pact matches 2 run function rpg:pact/s/aura2
execute if score @s rpg_pact matches 3 run function rpg:pact/s/aura3
execute if score @s rpg_pact matches 4 run function rpg:pact/s/aura4
execute if score @s rpg_pact matches 5 run function rpg:pact/s/aura5
execute if score @s rpg_pact matches 6 run function rpg:pact/s/aura6
execute if score @s rpg_pact matches 7 run function rpg:pact/s/aura7
