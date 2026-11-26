execute if score @s rpg_dt_t matches 1..58 run particle minecraft:squid_ink ~ ~0.4 ~ 9 0.1 9 0.02 8
execute if score @s rpg_dt_t matches 60 run function rpg:daath_fight/seal/go
execute if score @s rpg_dt_t matches 84.. run function rpg:daath_fight/sk/end
