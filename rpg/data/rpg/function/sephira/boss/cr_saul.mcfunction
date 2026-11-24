scoreboard players add @s rpg_bk_saul 1
function rpg:force/x/l/drop_saul
execute if score @s rpg_bk_saul matches 1 run return run function rpg:sephira/boss/first_saul
function rpg:world/boss/again_saul
execute if score @s rpg_bkd_saul matches 3.. run return 0
scoreboard players add @s rpg_bkd_saul 1
scoreboard players add @s rpg_ex_xp 15
tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"击败扫罗 · 阅历 +15","color":"#E6DFCF","bold":false,"italic":false}]
