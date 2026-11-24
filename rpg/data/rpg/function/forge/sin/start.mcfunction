# 开炉：靠近灵魂火、再核对一遍
scoreboard players operation #me rpg_fg = @s rpg_fg_id
scoreboard players set #fire rpg_fg 0
execute as @e[type=minecraft:marker,tag=rpg.fg.fire,distance=..8] if score @s rpg_fg_eo = #me rpg_fg at @s if block ~ ~ ~ #rpg:forge/soul_fire run scoreboard players set #fire rpg_fg 1
execute if score #fire rpg_fg matches 0 run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　离灵魂火太远了，靠近些再开炉","color":"#C04A3C","bold":false,"italic":false}]
execute if score @s rpg_fg_arg matches 1 run function rpg:forge/sin/check_1
execute if score @s rpg_fg_arg matches 1 if score #ok rpg_fg matches 1 run return run function rpg:forge/sin/forge_1
execute if score @s rpg_fg_arg matches 2 run function rpg:forge/sin/check_2
execute if score @s rpg_fg_arg matches 2 if score #ok rpg_fg matches 1 run return run function rpg:forge/sin/forge_2
execute if score @s rpg_fg_arg matches 3 run function rpg:forge/sin/check_3
execute if score @s rpg_fg_arg matches 3 if score #ok rpg_fg matches 1 run return run function rpg:forge/sin/forge_3
execute if score @s rpg_fg_arg matches 4 run function rpg:forge/sin/check_4
execute if score @s rpg_fg_arg matches 4 if score #ok rpg_fg matches 1 run return run function rpg:forge/sin/forge_4
execute if score @s rpg_fg_arg matches 5 run function rpg:forge/sin/check_5
execute if score @s rpg_fg_arg matches 5 if score #ok rpg_fg matches 1 run return run function rpg:forge/sin/forge_5
execute if score @s rpg_fg_arg matches 6 run function rpg:forge/sin/check_6
execute if score @s rpg_fg_arg matches 6 if score #ok rpg_fg matches 1 run return run function rpg:forge/sin/forge_6
execute if score @s rpg_fg_arg matches 7 run function rpg:forge/sin/check_7
execute if score @s rpg_fg_arg matches 7 if score #ok rpg_fg matches 1 run return run function rpg:forge/sin/forge_7
