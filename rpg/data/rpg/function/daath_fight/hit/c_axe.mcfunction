execute store result score #r rpg_dt run random value 0..6
execute if score #r rpg_dt matches 0 run return run function rpg:daath_fight/hit/ax1
execute if score #r rpg_dt matches 1 run return run function rpg:daath_fight/hit/ax2
execute if score #r rpg_dt matches 2 run return run function rpg:daath_fight/hit/ax3
execute if score #r rpg_dt matches 3 run return run function rpg:daath_fight/hit/da1
execute if score #r rpg_dt matches 4 run return run function rpg:daath_fight/hit/da2
execute if score #r rpg_dt matches 5 run return run function rpg:daath_fight/hit/bc1
execute if score #r rpg_dt matches 6 run return run function rpg:daath_fight/hit/bc2
