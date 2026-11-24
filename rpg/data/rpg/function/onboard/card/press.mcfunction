execute if score #do rpg_ob matches 2 run function rpg:onboard/card/roll
execute if score #do rpg_ob matches 2 run playsound minecraft:item.book.page_turn master @s ~ ~ ~ 1 1
execute if score #do rpg_ob matches 2 run return run function rpg:onboard/show
execute unless score #do rpg_ob matches 1 run return 0
scoreboard players set @s rpg_ob 4
function rpg:onboard/show
