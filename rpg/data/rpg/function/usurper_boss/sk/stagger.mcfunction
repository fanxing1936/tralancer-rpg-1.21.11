scoreboard players operation #m rpg_ub = @s rpg_ub_t
scoreboard players set #k rpg_ub 8
scoreboard players operation #m rpg_ub %= #k rpg_ub
execute if score #m rpg_ub matches 0 run function rpg:usurper_boss/stagger_star
execute if score @s rpg_ub_t matches 40.. run function rpg:usurper_boss/sk/end
