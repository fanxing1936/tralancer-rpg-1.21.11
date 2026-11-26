execute if score @s rpg_dt_t matches 1..24 run particle minecraft:squid_ink ~ ~0.6 ~ 0.6 0.8 0.6 0.05 8
execute if score @s rpg_dt_t matches 24 run function rpg:daath_fight/ten/spread
execute if score @s rpg_dt_t matches 26 run execute store result score @s rpg_dt_i run random value 0..9
execute if score @s rpg_dt_t matches 27 run function rpg:daath_fight/ten/mine
execute if score @s rpg_dt_t matches 28..66 if entity @s[tag=rpg.dt.found] run return run function rpg:daath_fight/ten/broken
execute if score @s rpg_dt_t matches 67 run function rpg:daath_fight/ten/rush
execute if score @s rpg_dt_t matches 84 run function rpg:daath_fight/ten/end
