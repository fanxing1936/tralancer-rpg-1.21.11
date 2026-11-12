scoreboard players operation #id rpg_l2_id = @s rpg_l2_id
execute if score @s rpg_l2_t matches ..60 as @e[type=minecraft:marker,tag=rpg.lu2f.lmark] if score @s rpg_l2_id = #id rpg_l2_id at @s run function rpg:lucifer_fight/fall/warn
execute if score @s rpg_l2_t matches 8 run function rpg:lucifer_fight/fall/leap
execute if score @s rpg_l2_t matches 15..60 if score @s rpg_l2_v matches 0 if predicate rpg:lucifer_fight/on_ground run function rpg:lucifer_fight/fall/land
execute if score @s rpg_l2_t matches 61 if score @s rpg_l2_v matches 0 run function rpg:lucifer_fight/fall/land
execute if score @s rpg_l2_t matches 15..60 if score @s rpg_l2_v matches 0 if score @s rpg_l2_t matches 15 run function rpg:lucifer_p2/play/jungleabomination_fall
execute if score @s rpg_l2_t matches 15..60 if score @s rpg_l2_v matches 0 if score @s rpg_l2_t matches 22 run function rpg:lucifer_p2/play/jungleabomination_fall
execute if score @s rpg_l2_t matches 15..60 if score @s rpg_l2_v matches 0 if score @s rpg_l2_t matches 29 run function rpg:lucifer_p2/play/jungleabomination_fall
execute if score @s rpg_l2_v matches 1.. run scoreboard players add @s rpg_l2_v 1
execute if score @s rpg_l2_v matches 60.. run function rpg:lucifer_fight/free
