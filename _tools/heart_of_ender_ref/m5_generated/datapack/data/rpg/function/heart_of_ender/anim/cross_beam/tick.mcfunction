scoreboard players add @s rpg_he_t 1
function rpg:heart_of_ender/anim/cross_beam/at
execute if score @s rpg_he_t matches 80.. run scoreboard players set @s rpg_he_run 2
