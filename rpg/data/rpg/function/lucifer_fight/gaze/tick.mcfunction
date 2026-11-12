execute if score @s rpg_l2_t matches ..29 run particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:1.2} ~ ~4.6 ~ 0.6 0.25 0.6 0 3
execute if score @s rpg_l2_t matches 15 run playsound minecraft:block.sculk_shrieker.shriek hostile @a[distance=..32] ~ ~ ~ 1 0.75
execute if score @s rpg_l2_t matches 30 run function rpg:lucifer_fight/gaze/judge
execute if score @s rpg_l2_t matches 30 run function rpg:lucifer_p2/play/jungleabomination_vineattacksucessful
execute if score @s rpg_l2_t matches 67 run function rpg:lucifer_fight/free
