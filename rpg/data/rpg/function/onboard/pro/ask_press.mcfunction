execute if score #do rpg_ob matches 1 run scoreboard players set @s rpg_ob 1
execute if score #do rpg_ob matches 1 run return run function rpg:onboard/pro/try
execute unless score #do rpg_ob matches 2 run return 0
scoreboard players set @s rpg_ob 3
function rpg:onboard/show
