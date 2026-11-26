execute if score @s rpg_dt_t matches 1..20 run particle minecraft:squid_ink ~ ~0.3 ~ 2.2 0.1 2.2 0.02 4
execute if score @s rpg_dt_t matches 22 run function rpg:daath_fight/blast/go
execute if score @s rpg_dt_t matches 46.. run function rpg:daath_fight/sk/end
