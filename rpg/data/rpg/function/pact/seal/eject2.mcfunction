execute unless score @s rpg_pact_s2 matches 1.. run return run function rpg:pact/say/seal_empty
scoreboard players operation #seal rpg_pact = @s rpg_pact_s2
function rpg:pact/seal/give
scoreboard players set @s rpg_pact_s2 0
function rpg:pact/seal/apply
