tag @s add rpg.pact.ui
scoreboard players enable @s rpg_pact_do
execute store result storage rpg:pact ui.have int 1 run clear @s minecraft:bone[!minecraft:custom_data] 0
function rpg:pact/ui/terms_show3 with storage rpg:pact ui
