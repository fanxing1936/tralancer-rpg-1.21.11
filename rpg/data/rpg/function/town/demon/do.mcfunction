scoreboard players operation #do rpg_dm = @s rpg_dm_do
scoreboard players set @s rpg_dm_do 0
scoreboard players enable @s rpg_dm_do
execute if score #do rpg_dm matches 1 run return run function rpg:town/demon/buy
execute if score #do rpg_dm matches 2 run return run function rpg:town/demon/altar_info
execute if score #do rpg_dm matches 11 run return run function rpg:town/demon/sign
execute if score #do rpg_dm matches 12 run return run function rpg:town/demon/refuse
