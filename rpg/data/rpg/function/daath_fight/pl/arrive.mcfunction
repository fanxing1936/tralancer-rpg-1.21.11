execute if score @s rpg_dt_pt matches 40 store result score @s rpg_pa_wn run clear @s #rpg:daath/weapon 0
effect clear @s minecraft:blindness
execute if score @s rpg_dt_pt matches 40 run function rpg:daath_fight/unit/summon
execute if score @s rpg_dt_pt matches 110.. run scoreboard players set @s rpg_dt_ph 3
