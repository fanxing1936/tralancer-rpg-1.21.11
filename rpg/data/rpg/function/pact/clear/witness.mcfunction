execute if score #lord rpg_pact matches 1 run tag @s add rpg.pw.1
execute if score #lord rpg_pact matches 2 run tag @s add rpg.pw.2
execute if score #lord rpg_pact matches 3 run tag @s add rpg.pw.3
execute if score #lord rpg_pact matches 4 run tag @s add rpg.pw.4
execute if score #lord rpg_pact matches 5 run tag @s add rpg.pw.5
execute if score #lord rpg_pact matches 6 run tag @s add rpg.pw.6
execute if score #lord rpg_pact matches 7 run tag @s add rpg.pw.7
execute unless entity @s[tag=rpg.pact] run return 0
execute if score #fell rpg_pact matches 0 run return 0
execute unless score @s rpg_pact_bid = #fell rpg_pact run return 0
scoreboard players set @s rpg_pact_bid 0
execute unless score @s rpg_pact = #lord rpg_pact run return 0
execute if score @s rpg_pact_dom matches 1 run return 0
function rpg:pact/clear/dominate
