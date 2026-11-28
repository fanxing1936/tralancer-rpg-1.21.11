tag @s add rpg.xt.24
scoreboard players add @s rpg_x_pt 25
scoreboard players add @s rpg_ex_xp 25
function rpg:explore/milestone
function rpg:events/bt/explore
loot give @s loot rpg:world/currency
loot give @s loot rpg:world/currency
loot give @s loot rpg:world/currency
loot give @s loot rpg:world/bp_fragment
loot give @s loot rpg:world/bp_fragment
tellraw @s ["",{"text":"〖见闻录〗","color":"#C9A646","bold":true,"italic":false},{"text":"  发现地标：湖畔庄园　阅历 +25　探索点 +25","color":"#9C9A94","bold":false,"italic":false}]
