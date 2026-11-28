tag @s add rpg.in.creeper
scoreboard players add @s rpg_x_pt 5
scoreboard players add @s rpg_ex_xp 5
function rpg:explore/milestone
tellraw @s ["",{"text":"〖怪物情报〗","color":"#FF6B5E","bold":true,"italic":false},{"text":"  苦力怕","color":"#E6DFCF","bold":true,"italic":false},{"text":"　弱点：听到嘶声就后撤；被雷劈会变强　掉落：火药","color":"#9C9A94","bold":false,"italic":false},{"text":"　此后打它 +5%","color":"#C9A646","bold":false,"italic":false}]
