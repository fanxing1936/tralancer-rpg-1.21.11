scoreboard players add @s rpg_al_mt 1
execute if score @s rpg_al_mt matches 24 run function rpg:jacques/anim/enter/down
execute if score @s rpg_al_mt matches 30.. run return run function rpg:jacques_ally/leave
