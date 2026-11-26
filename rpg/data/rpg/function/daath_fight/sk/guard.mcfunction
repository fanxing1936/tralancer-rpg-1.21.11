execute if entity @s[tag=rpg.dt.rip] run return run function rpg:daath_fight/guard/go
scoreboard players operation #m rpg_dt = @s rpg_dt_t
scoreboard players set #k rpg_dt 4
scoreboard players operation #m rpg_dt %= #k rpg_dt
execute if score #m rpg_dt matches 0 run particle minecraft:end_rod ^ ^1.4 ^0.6 0.25 0.35 0.1 0.01 2
execute if score @s rpg_dt_t matches 30.. run function rpg:daath_fight/sk/end
