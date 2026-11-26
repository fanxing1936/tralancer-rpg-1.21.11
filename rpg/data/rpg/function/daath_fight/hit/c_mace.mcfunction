execute store result score #r rpg_dt run random value 0..3
execute if score #r rpg_dt matches 0 run return run function rpg:daath_fight/hit/ma1
execute if score #r rpg_dt matches 1 run return run function rpg:daath_fight/hit/ma2
execute if score #r rpg_dt matches 2 run return run function rpg:daath_fight/hit/ma3
execute if score #r rpg_dt matches 3 run return run function rpg:daath_fight/hit/ha1
