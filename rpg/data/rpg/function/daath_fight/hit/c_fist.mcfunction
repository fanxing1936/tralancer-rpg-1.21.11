execute store result score #r rpg_dt run random value 0..5
execute if score #r rpg_dt matches 0 run return run function rpg:daath_fight/hit/fi1
execute if score #r rpg_dt matches 1 run return run function rpg:daath_fight/hit/fi2
execute if score #r rpg_dt matches 2 run return run function rpg:daath_fight/hit/fi3
execute if score #r rpg_dt matches 3 run return run function rpg:daath_fight/hit/fi4
execute if score #r rpg_dt matches 4 run return run function rpg:daath_fight/hit/fi5
execute if score #r rpg_dt matches 5 run return run function rpg:daath_fight/hit/fi6
