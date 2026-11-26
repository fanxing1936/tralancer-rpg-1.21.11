execute store result score #r rpg_dt run random value 0..1
execute if score #r rpg_dt matches 0 run return run function rpg:daath_fight/hit/sc1
execute if score #r rpg_dt matches 1 run return run function rpg:daath_fight/hit/sc2
