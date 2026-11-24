scoreboard players operation #do rpg_ev = @s rpg_jr_do
scoreboard players set @s rpg_jr_do 0
scoreboard players enable @s rpg_jr_do
execute if score #do rpg_ev matches 11 run function rpg:events/bt/claim_1
execute if score #do rpg_ev matches 12 run function rpg:events/bt/claim_2
execute if score #do rpg_ev matches 13 run function rpg:events/bt/claim_3
execute if score #do rpg_ev matches 2 run return run function rpg:events/jr/recipes
function rpg:events/jr/open
