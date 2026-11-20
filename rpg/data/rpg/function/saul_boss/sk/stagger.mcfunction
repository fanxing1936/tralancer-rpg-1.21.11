scoreboard players operation #m rpg_sl = @s rpg_sl_t
scoreboard players set #k rpg_sl 8
scoreboard players operation #m rpg_sl %= #k rpg_sl
execute if score #m rpg_sl matches 0 run function rpg:saul_boss/stagger_star
execute if score @s rpg_sl_t matches 40.. run function rpg:saul_boss/stagger/end
