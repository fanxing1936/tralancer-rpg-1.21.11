scoreboard players add @s rpg_av_t 1
function rpg:arch_visage/anim/spawn_attack/at
execute if score @s rpg_av_t matches 98.. run scoreboard players set @s rpg_av_run 2
