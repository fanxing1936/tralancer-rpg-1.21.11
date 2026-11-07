advancement revoke @s only rpg:pact/eat
execute unless score @s rpg_pact matches 4 run return 0
execute if score @s rpg_pv_a matches 1.. run return 0
scoreboard players set @s rpg_pv_a 5
scoreboard players set #gain rpg_pact 3
function rpg:pact/oath/gain
