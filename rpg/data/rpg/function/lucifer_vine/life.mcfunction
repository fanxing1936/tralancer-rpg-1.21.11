scoreboard players remove @s rpg_luv_l 1
execute if score @s rpg_luv_l matches ..0 if entity @s[tag=rpg.luv.dying] run return run function rpg:lucifer_vine/clear
execute if score @s rpg_luv_l matches ..0 run function rpg:lucifer_vine/retract
