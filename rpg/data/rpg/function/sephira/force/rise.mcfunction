# 回头：重回圣力，同化清零
scoreboard players set @s rpg_force 1
tag @s remove rpg.fallen
scoreboard players set @s rpg_assim 0
scoreboard players set @s rpg_taint 0
scoreboard players set @s rpg_fz_tp 0
scoreboard players set @s rpg_mana 0
scoreboard players set @s rpg_fz_b -1
title @s times 10 70 20
title @s title {"text":"重回圣力","color":"#FFD85A","bold":true,"italic":false}
playsound minecraft:block.beacon.activate player @s ~ ~ ~ 1 1.2
function rpg:force/refund_m
function rpg:quest/egg/waverer
