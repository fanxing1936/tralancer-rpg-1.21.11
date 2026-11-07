advancement revoke @s only rpg:pact/kill_hostile
execute unless score @s rpg_pact matches 2 run return 0
execute unless predicate rpg:pact_wet run return 0
scoreboard players set #gain rpg_pact 2
function rpg:pact/oath/gain
