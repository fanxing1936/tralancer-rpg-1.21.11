# 树倒下：古龙（三阶段）还没做，暂时在这里结算。
function rpg:lucifer_boss/refill
tag @s add rpg.lub.end
scoreboard players set @s rpg_lub 9
scoreboard players set #stage rpg_lub 9
scoreboard players set @s rpg_lub_c 0
function rpg:lucifer_fight/cancel
function rpg:lucifer_fight/hold
effect give @s minecraft:resistance 10 4 true
function rpg:lucifer_p2/play/jungleabomination_death
bossbar set rpg:lucifer_boss value 0
tellraw @a[distance=..48] ["",{"text":"〖路西法〗","color":"#34975A","bold":true,"italic":false},{"text":" 𝔏𝔲𝔠𝔦𝔣𝔢𝔯","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"……树根断了。可蛇不会死在树上。","color":"#9C9A94","bold":false,"italic":false}]
