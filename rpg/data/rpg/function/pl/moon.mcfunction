execute if score #moon rpg_pl matches 1.. run return run function rpg:pl/moon_on
# 血雨里不来血月，等雨停
execute if score #rain rpg_pl matches 1.. run return 0
scoreboard players add #mw rpg_pl 1
execute if score #mw rpg_pl matches 1200.. run function rpg:pl/moon_start
