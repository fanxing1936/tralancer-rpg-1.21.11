scoreboard players add @s rpg_al_mt 1
execute if score @s rpg_al_sk matches 1 if score @s rpg_al_mt matches 7 run function rpg:jacques_ally/hit/front
execute if score @s rpg_al_sk matches 2 if score @s rpg_al_mt matches 9 run function rpg:jacques_ally/hit/front
execute if score @s rpg_al_sk matches 3 if score @s rpg_al_mt matches 3 run function rpg:jacques_ally/hit/sweep
execute if score @s rpg_al_sk matches 4 if score @s rpg_al_mt matches 4 run function rpg:jacques/weapon/harp2
execute if score @s rpg_al_sk matches 4 if score @s rpg_al_mt matches 8 run function rpg:jacques/weapon/harp3
execute if score @s rpg_al_sk matches 4 if score @s rpg_al_mt matches 12 run function rpg:jacques/weapon/harp4
execute if score @s rpg_al_sk matches 4 if score @s rpg_al_mt matches 14 if entity @e[tag=rpg.al.aim] facing entity @e[tag=rpg.al.aim,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_al_sk matches 4 if score @s rpg_al_mt matches 16 run function rpg:jacques/anim/enter/shoot
execute if score @s rpg_al_sk matches 4 if score @s rpg_al_mt matches 16 run function rpg:jacques_ally/hit/bolt
execute if score @s rpg_al_sk matches 4 if score @s rpg_al_mt matches 18 run function rpg:jacques/weapon/harp1
execute if score @s rpg_al_sk matches 1 if score @s rpg_al_mt matches 14.. run function rpg:jacques_ally/move_end
execute if score @s rpg_al_sk matches 2 if score @s rpg_al_mt matches 18.. run function rpg:jacques_ally/move_end
execute if score @s rpg_al_sk matches 3 if score @s rpg_al_mt matches 16.. run function rpg:jacques_ally/move_end
execute if score @s rpg_al_sk matches 4 if score @s rpg_al_mt matches 24.. run function rpg:jacques_ally/move_end
