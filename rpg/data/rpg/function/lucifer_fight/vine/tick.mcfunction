scoreboard players operation #id rpg_l2_id = @s rpg_l2_id
execute if score @s rpg_l2_t matches 1 run function rpg:lucifer_fight/vine/warn_all
execute if score @s rpg_l2_t matches 5 run function rpg:lucifer_fight/vine/warn_all
execute if score @s rpg_l2_t matches 9 run function rpg:lucifer_fight/vine/warn_all
execute if score @s rpg_l2_t matches 13 run function rpg:lucifer_fight/vine/warn_all
execute if score @s rpg_l2_t matches 17 run function rpg:lucifer_fight/vine/warn_all
execute if score @s rpg_l2_t matches 22 run function rpg:lucifer_fight/vine/burst
execute if score @s rpg_l2_t matches 38 run function rpg:lucifer_p2/play/jungleabomination_vineattackidle
execute if score @s rpg_l2_t matches 58 if score @s rpg_l2_v matches 1 run function rpg:lucifer_p2/play/jungleabomination_vineattacksucessful
execute if score @s rpg_l2_t matches 58 unless score @s rpg_l2_v matches 1 run function rpg:lucifer_p2/play/jungleabomination_vineattackunsucessful
execute if score @s rpg_l2_t matches 95 if score @s rpg_l2_v matches 1 run return run function rpg:lucifer_fight/free
execute if score @s rpg_l2_t matches 88 unless score @s rpg_l2_v matches 1 run function rpg:lucifer_fight/vuln/start
