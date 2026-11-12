scoreboard players add @s rpg_l2_t 1
execute if score @s rpg_l2_t matches 36 run function rpg:lucifer_p2/play/jungleabomination_vulnerablestuncycle
execute if score @s rpg_l2_t matches 96 run attribute @s minecraft:armor modifier remove rpg:lu2f_open
execute if score @s rpg_l2_t matches 96 run function rpg:lucifer_p2/play/jungleabomination_vulnerablegetup
execute if score @s rpg_l2_t matches 173 run function rpg:lucifer_fight/free
