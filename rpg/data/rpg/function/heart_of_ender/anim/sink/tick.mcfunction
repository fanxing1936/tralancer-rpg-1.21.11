scoreboard players add @s rpg_he_t 1
function rpg:heart_of_ender/anim/sink/at
execute if score @s rpg_he_t matches 40.. run scoreboard players set @s rpg_he_run 2
