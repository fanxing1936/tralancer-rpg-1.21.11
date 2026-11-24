scoreboard players add @s rpg_bk_lucifer 1
function rpg:force/x/l/drop_lucifer
execute if score @s rpg_bk_lucifer matches 1 run return run function rpg:sephira/boss/first_lucifer
function rpg:world/boss/again_lucifer
execute if score @s rpg_bkd_lucifer matches 3.. run return 0
scoreboard players add @s rpg_bkd_lucifer 1
scoreboard players add @s rpg_ex_xp 15
tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"击败路西法 · 阅历 +15","color":"#E6DFCF","bold":false,"italic":false}]
