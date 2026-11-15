execute facing entity @e[tag=rpg.al.aim,limit=1] feet run tp @s ~ ~ ~ ~ 0
scoreboard players set @s rpg_al_mt 0
execute if score @s rpg_al_cb matches 0 run scoreboard players set @s rpg_al_sk 1
execute if score @s rpg_al_cb matches 1 run scoreboard players set @s rpg_al_sk 2
execute if score @s rpg_al_cb matches 2 run scoreboard players set @s rpg_al_sk 3
execute if score @s rpg_al_cb matches 0 run function rpg:jacques/anim/enter/slash1
execute if score @s rpg_al_cb matches 1 run function rpg:jacques/anim/enter/slash2
execute if score @s rpg_al_cb matches 2 run function rpg:jacques/anim/enter/sweep
scoreboard players add @s rpg_al_cb 1
execute if score @s rpg_al_cb matches 3.. run scoreboard players set @s rpg_al_cb 0
