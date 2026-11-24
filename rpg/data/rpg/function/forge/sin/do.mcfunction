# 罪器锻造的按钮：50 打开，51..57 选柱，58 开炉
execute if score #do rpg_fg matches 50 run return run function rpg:forge/sin/open
execute if score #do rpg_fg matches 51..57 run scoreboard players operation @s rpg_fg_arg = #do rpg_fg
execute if score #do rpg_fg matches 51..57 run scoreboard players remove @s rpg_fg_arg 50
execute if score #do rpg_fg matches 51..57 run return run function rpg:forge/sin/pick
execute if score #do rpg_fg matches 58 run return run function rpg:forge/sin/start
