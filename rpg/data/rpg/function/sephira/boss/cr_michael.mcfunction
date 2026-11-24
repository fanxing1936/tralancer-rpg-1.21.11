scoreboard players add @s rpg_bk_michael 1
function rpg:force/x/l/drop_michael
execute if score @s rpg_bk_michael matches 1 run return run function rpg:sephira/boss/first_michael
function rpg:world/boss/again_michael
execute if score @s rpg_bkd_michael matches 3.. run return 0
scoreboard players add @s rpg_bkd_michael 1
scoreboard players add @s rpg_ex_xp 15
tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"击败米迦勒 · 阅历 +15","color":"#E6DFCF","bold":false,"italic":false}]
