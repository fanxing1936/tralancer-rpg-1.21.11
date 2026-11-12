execute unless score @s rpg_lu2_anim matches 15 unless score @s rpg_lu2_anim matches 17 run return run function rpg:lucifer_p2/flower/stop
scoreboard players remove @s rpg_lu2_flower 1
execute if score @s rpg_lu2_flower matches ..0 run function rpg:lucifer_p2/flower/repeat
