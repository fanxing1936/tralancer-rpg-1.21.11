execute store result score #r rpg_dt run random value 0..6
execute if score #r rpg_dt matches 0 run return run function rpg:daath_fight/hit/sp1
execute if score #r rpg_dt matches 1 run return run function rpg:daath_fight/hit/sp2
execute if score #r rpg_dt matches 2 run return run function rpg:daath_fight/hit/sp3
execute if score #r rpg_dt matches 3 run return run function rpg:daath_fight/hit/bo1
execute if score #r rpg_dt matches 4 run return run function rpg:daath_fight/hit/bo2
execute if score #r rpg_dt matches 5 run return run function rpg:daath_fight/hit/bo3
execute if score #r rpg_dt matches 6 run return run function rpg:daath_fight/hit/bo4
