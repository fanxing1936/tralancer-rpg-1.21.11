execute if score #do rpg_ob matches 9 run scoreboard players set @s rpg_ob 12
execute if score #do rpg_ob matches 9 run return run function rpg:onboard/show
scoreboard players set #ok rpg_ob 0
execute if score #do rpg_ob matches 50 if score @s rpg_ob_w matches 0..2 run function rpg:onboard/tut/stone_rift
execute if score #do rpg_ob matches 51 if score @s rpg_ob_w matches 0..2 run function rpg:onboard/tut/stone_frost
execute if score #do rpg_ob matches 52 if score @s rpg_ob_w matches 0..2 run function rpg:onboard/tut/stone_shadow
execute if score #do rpg_ob matches 53 if score @s rpg_ob_w matches 0..2 run function rpg:onboard/tut/stone_blood
execute if score #do rpg_ob matches 54 run function rpg:onboard/tut/stone_gale
execute if score #do rpg_ob matches 55 if score @s rpg_ob_w matches 3.. run function rpg:onboard/tut/stone_volley
execute if score #do rpg_ob matches 56 run function rpg:onboard/tut/stone_banner
execute if score #ok rpg_ob matches 1 run scoreboard players set @s rpg_ob 15
function rpg:onboard/show
