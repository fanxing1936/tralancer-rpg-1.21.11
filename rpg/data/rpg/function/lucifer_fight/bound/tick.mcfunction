execute unless entity @s[tag=rpg.lu2f.bound] run function rpg:lucifer_fight/bound/enter
scoreboard players add @s rpg_l2_t 1
execute if score @s rpg_l2_t matches 36 run function rpg:lucifer_p2/play/jungleabomination_vulnerablestuncycle
