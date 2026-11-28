tag @s add rpg.in.skeleton
scoreboard players add @s rpg_x_pt 5
scoreboard players add @s rpg_ex_xp 5
function rpg:explore/milestone
tellraw @s ["",{"text":"〖怪物情报〗","color":"#FF6B5E","bold":true,"italic":false},{"text":"  骷髅","color":"#E6DFCF","bold":true,"italic":false},{"text":"　弱点：近身打，它拉不开弓；亡灵　掉落：骨头、箭","color":"#9C9A94","bold":false,"italic":false},{"text":"　此后打它 +5%","color":"#C9A646","bold":false,"italic":false}]
