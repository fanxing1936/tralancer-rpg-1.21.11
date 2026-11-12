scoreboard players add @s rpg_l2_t 1
execute if score @s rpg_l2_sk matches 11 run return run function rpg:lucifer_fight/p1/sin/tick
execute if score @s rpg_l2_sk matches 12 run return run function rpg:lucifer_fight/p1/spear/tick
execute if score @s rpg_l2_sk matches 13 run return run function rpg:lucifer_fight/p1/high/tick
execute if score @s rpg_l2_sk matches 14 run return run function rpg:lucifer_fight/p1/fall/tick
execute if score @s rpg_l2_sk matches 15 run return run function rpg:lucifer_fight/p1/throne/tick
execute if score @s rpg_l2_sk matches 16 run return run function rpg:lucifer_fight/p1/ult/tick
execute if score @s rpg_l2_sk matches 19 run return run function rpg:lucifer_fight/p1/jab/tick
function rpg:lucifer_fight/free
