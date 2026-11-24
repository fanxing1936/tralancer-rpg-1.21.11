execute unless score #do rpg_ob matches 20..24 run return 0
scoreboard players operation @s rpg_ob_w = #do rpg_ob
scoreboard players remove @s rpg_ob_w 20
playsound minecraft:block.blastfurnace.fire_crackle master @s ~ ~ ~ 1 0.6
playsound minecraft:block.anvil.use master @s ~ ~ ~ 0.6 0.8
function rpg:onboard/tut/make_head
function rpg:onboard/tut/make_chest
function rpg:onboard/tut/make_legs
function rpg:onboard/tut/make_feet
execute if score @s rpg_ob_w matches 0 run function rpg:onboard/tut/make_sword
execute if score @s rpg_ob_w matches 1 run function rpg:onboard/tut/make_axe
execute if score @s rpg_ob_w matches 2 run function rpg:onboard/tut/make_mace
execute if score @s rpg_ob_w matches 3 run function rpg:onboard/tut/make_bow
execute if score @s rpg_ob_w matches 4 run function rpg:onboard/tut/make_crossbow
scoreboard players set @s rpg_ob 7
function rpg:onboard/show
