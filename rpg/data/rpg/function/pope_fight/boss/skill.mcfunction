# 招式进行中。
scoreboard players add #st rpg_pf 1
execute if score #sk rpg_pf matches 1 run return run function rpg:pope_fight/boss/do_attack
execute if score #sk rpg_pf matches 2 run return run function rpg:pope_fight/boss/do_teleport
execute if score #sk rpg_pf matches 3 run return run function rpg:pope_fight/boss/do_summon
execute if score #sk rpg_pf matches 4 run return run function rpg:pope_fight/boss/do_blood
execute if score #sk rpg_pf matches 5 run return run function rpg:pope_fight/boss/do_reclaim
execute if score #sk rpg_pf matches 6 run return run function rpg:pope_fight/boss/do_enhance
execute if score #sk rpg_pf matches 7 run return run function rpg:pope_fight/boss/do_appear
execute if score #sk rpg_pf matches 8 run return run function rpg:pope_fight/boss/do_melee
execute if score #sk rpg_pf matches 9 run return run function rpg:pope_fight/boss/do_ring
execute if score #sk rpg_pf matches 10 run return run function rpg:pope_fight/boss/do_judge
execute if score #sk rpg_pf matches 11 run return run function rpg:pope_fight/boss/do_basic
execute if score #sk rpg_pf matches 12 run return run function rpg:pope_fight/boss/do_seals
execute if score #sk rpg_pf matches 13 run return run function rpg:pope_fight/boss/do_doom
