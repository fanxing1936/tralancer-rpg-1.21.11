execute if score #do rpg_ob matches 9 run scoreboard players set @s rpg_ob 12
execute if score #do rpg_ob matches 9 run return run function rpg:onboard/show
scoreboard players set #ok rpg_ob 0
execute if score #do rpg_ob matches 30 if score @s rpg_ob_w matches 0..2 run function rpg:onboard/tut/rune_ember
execute if score #do rpg_ob matches 31 if score @s rpg_ob_w matches 0..2 run function rpg:onboard/tut/rune_echo
execute if score #do rpg_ob matches 32 if score @s rpg_ob_w matches 0..2 run function rpg:onboard/tut/rune_execute
execute if score #do rpg_ob matches 33 if score @s rpg_ob_w matches 0..2 run function rpg:onboard/tut/rune_backstab
execute if score #do rpg_ob matches 34 if score @s rpg_ob_w matches 0..2 run function rpg:onboard/tut/rune_bloodpact
execute if score #do rpg_ob matches 35 if score @s rpg_ob_w matches 0..2 run function rpg:onboard/tut/rune_poise
execute if score #do rpg_ob matches 36 if score @s rpg_ob_w matches 3.. run function rpg:onboard/tut/rune_hunt
execute if score #do rpg_ob matches 37 if score @s rpg_ob_w matches 3.. run function rpg:onboard/tut/rune_split
execute if score #do rpg_ob matches 38 if score @s rpg_ob_w matches 3.. run function rpg:onboard/tut/rune_meteor
execute if score #do rpg_ob matches 39 if score #never rpg_ob matches 1 run function rpg:onboard/tut/rune_recoil
execute if score #do rpg_ob matches 40 if score #never rpg_ob matches 1 run function rpg:onboard/tut/rune_lastbreath
execute if score #do rpg_ob matches 41 if score #never rpg_ob matches 1 run function rpg:onboard/tut/rune_stillwater
execute if score #do rpg_ob matches 42 if score #never rpg_ob matches 1 run function rpg:onboard/tut/rune_swift
execute if score #ok rpg_ob matches 1 run scoreboard players set @s rpg_ob 15
function rpg:onboard/show
