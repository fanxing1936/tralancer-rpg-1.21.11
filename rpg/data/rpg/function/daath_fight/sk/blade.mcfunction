execute if score @s rpg_dt_t matches 1..18 run particle minecraft:smoke ^-0.4 ^1.2 ^0.4 0.2 0.4 0.2 0.02 4
execute if score @s rpg_dt_t matches 20.. run function rpg:daath_fight/sk/end
