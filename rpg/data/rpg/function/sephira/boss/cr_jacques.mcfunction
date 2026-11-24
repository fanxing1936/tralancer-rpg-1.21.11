scoreboard players add @s rpg_bk_jacques 1
function rpg:force/x/l/drop_jacques
execute if score @s rpg_bk_jacques matches 1 run return run function rpg:sephira/boss/first_jacques
function rpg:world/boss/again_jacques
execute if score @s rpg_bkd_jacques matches 3.. run return 0
scoreboard players add @s rpg_bkd_jacques 1
scoreboard players add @s rpg_ex_xp 15
tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"击败雅克 · 阅历 +15","color":"#E6DFCF","bold":false,"italic":false}]
