function rpg:pact/seal/take
scoreboard players operation @s rpg_pact_s1 = #seal rpg_pact
function rpg:pact/seal/apply
playsound minecraft:block.amethyst_block.place player @s ~ ~ ~ 1 0.7
execute at @s run particle wax_on ~ ~1 ~ 0.4 0.5 0.4 0.05 16
