scoreboard players add @s rpg_l2_t 1
execute if score @s rpg_l2_sk matches 1 run return run function rpg:lucifer_fight/vine/tick
execute if score @s rpg_l2_sk matches 2 run return run function rpg:lucifer_fight/fruit/tick
execute if score @s rpg_l2_sk matches 3 run return run function rpg:lucifer_fight/tempt/tick
execute if score @s rpg_l2_sk matches 4 run return run function rpg:lucifer_fight/fall/tick
execute if score @s rpg_l2_sk matches 5 run return run function rpg:lucifer_fight/gaze/tick
execute if score @s rpg_l2_sk matches 6 run return run function rpg:lucifer_fight/ult/tick
execute if score @s rpg_l2_sk matches 9 run return run function rpg:lucifer_fight/melee/tick
function rpg:lucifer_fight/free
