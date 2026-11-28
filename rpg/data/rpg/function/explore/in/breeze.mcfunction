tag @s add rpg.in.breeze
scoreboard players add @s rpg_x_pt 5
scoreboard players add @s rpg_ex_xp 5
function rpg:explore/milestone
tellraw @s ["",{"text":"〖怪物情报〗","color":"#FF6B5E","bold":true,"italic":false},{"text":"  旋风人","color":"#E6DFCF","bold":true,"italic":false},{"text":"　弱点：会弹开弹射物，近身打　掉落：旋风棒","color":"#9C9A94","bold":false,"italic":false},{"text":"　此后打它 +5%","color":"#C9A646","bold":false,"italic":false}]
