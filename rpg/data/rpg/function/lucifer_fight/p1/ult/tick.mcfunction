execute if score @s rpg_l2_t matches ..29 run particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:1.2} ~ ~1 ~ 0.55 0.75 0.55 0.02 3
execute if score @s rpg_l2_t matches 10 run function rpg:lucifer_fight/p1/ult/warn_rings
execute if score @s rpg_l2_t matches 20 run function rpg:lucifer_fight/p1/ult/warn_rings
execute if score @s rpg_l2_t matches 30 run function rpg:lucifer_lord/play/strong
execute if score @s rpg_l2_t matches 30 run function rpg:lucifer_fight/p1/ult/fire
execute if score @s rpg_l2_t matches 52 run function rpg:lucifer_fight/free
