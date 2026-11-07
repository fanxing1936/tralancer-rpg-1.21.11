execute if score #st rpg_pf matches 1 run function rpg:pope_fight/boss/hide
execute if score #st rpg_pf matches 2 at @e[type=minecraft:marker,tag=rpg.pf.center,limit=1] run tp @s ~ ~ ~
execute if score #st rpg_pf matches 2 run function rpg:pope_fight/boss/doom_mark
execute if score #st rpg_pf matches 5 run function rpg:pope_fight/boss/show
execute if score #st rpg_pf matches 40 run function rpg:pope_fight/clip/cast
execute if score #st rpg_pf matches 70 run function rpg:pope_fight/boss/doom_toll
execute if score #st rpg_pf matches 90 run function rpg:pope_fight/boss/doom_toll
execute if score #st rpg_pf matches 110 run function rpg:pope_fight/boss/doom_strike
execute if score #st rpg_pf matches 180.. run function rpg:pope_fight/boss/doom_end
