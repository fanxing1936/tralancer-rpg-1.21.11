execute if score #rain rpg_pl matches 1.. run return run function rpg:pl/rain/on
execute as @e[tag=rpg.pl.r] run function rpg:pl/rain/unbuff
execute if score #moon rpg_pl matches 1.. run return 0
execute unless score #rt rpg_pl matches 1.. store result score #rt rpg_pl run random value 900..1500
scoreboard players remove #rt rpg_pl 1
execute if score #rt rpg_pl matches 0 run function rpg:pl/rain/start
