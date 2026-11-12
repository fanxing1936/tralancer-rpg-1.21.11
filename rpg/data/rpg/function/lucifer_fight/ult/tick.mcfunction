scoreboard players operation #id rpg_l2_id = @s rpg_l2_id
execute if score @s rpg_l2_t matches 23 run function rpg:lucifer_p2/play/jungleabomination_projectileattack_loop
execute if score @s rpg_l2_t matches ..29 run particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:2.4} ~ ~3 ~ 1.5 1.5 1.5 0.03 4
execute if score @s rpg_l2_t matches 30 run function rpg:lucifer_fight/ult/resolve
execute if score @s rpg_l2_t matches 31..53 run function rpg:lucifer_fight/ult/warn_rings
execute if score @s rpg_l2_t matches 42 run function rpg:lucifer_fight/ult/ring1
execute if score @s rpg_l2_t matches 48 run function rpg:lucifer_fight/ult/ring2
execute if score @s rpg_l2_t matches 54 run function rpg:lucifer_fight/ult/ring3
execute if score @s rpg_l2_t matches 68 run function rpg:lucifer_p2/play/jungleabomination_vineattackidle
execute if score @s rpg_l2_t matches 80 run function rpg:lucifer_p2/play/jungleabomination_vineattacksucessful
execute if score @s rpg_l2_t matches 117 run function rpg:lucifer_fight/free
