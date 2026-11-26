execute store result score #r rpg_dt run random value 0..4
execute if score #r rpg_dt matches 0 run return run function rpg:daath_fight/hit/gl1
execute if score #r rpg_dt matches 1 run return run function rpg:daath_fight/hit/gl2
execute if score #r rpg_dt matches 2 run return run function rpg:daath_fight/hit/gl3
execute if score #r rpg_dt matches 3 run return run function rpg:daath_fight/hit/gu1
execute if score #r rpg_dt matches 4 run return run function rpg:daath_fight/hit/gu2
