tag @s add rpg.xt.9
scoreboard players add @s rpg_xt_n 1
scoreboard players add @s rpg_x_pt 15
scoreboard players add @s rpg_ex_xp 15
function rpg:explore/milestone
function rpg:events/bt/explore
loot give @s loot rpg:world/currency
loot give @s loot rpg:world/currency
tellraw @s ["",{"text":"〖见闻录〗","color":"#C9A646","bold":true,"italic":false},{"text":"  第一次来到拉末　阅历 +15　探索点 +15","color":"#9C9A94","bold":false,"italic":false}]
