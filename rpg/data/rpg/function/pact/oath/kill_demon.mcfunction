advancement revoke @s only rpg:pact/kill_demon
execute unless score @s rpg_pact matches 1 run return 0
scoreboard players set #gain rpg_pact 4
function rpg:pact/oath/gain
