execute unless score #do rpg_ob matches 2 run return 0
tag @s remove rpg.ob.queued
scoreboard players set @s rpg_ob 3
function rpg:onboard/show
