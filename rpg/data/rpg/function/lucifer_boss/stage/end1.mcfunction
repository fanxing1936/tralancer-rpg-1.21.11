# 蛇 → 树：钳在底线，大招标记与时钟归零，交给已做好的变身演出。
function rpg:lucifer_boss/refill
scoreboard players set @s rpg_lub 2
scoreboard players set #stage rpg_lub 2
tag @s remove rpg.lub.u1
tag @s remove rpg.lub.u2
scoreboard players set @s rpg_lub_c 0
tag @s add rpg.lub
function rpg:lucifer_fight/morph/start
bossbar set rpg:lucifer_boss name {"text":"\ue234\ue1f5\ue1f1\ue1f9","font":"rpg:lucifer_boss"}
bossbar set rpg:lucifer_boss max 1000
bossbar set rpg:lucifer_boss value 1000
function rpg:lucifer_boss/music/2
tellraw @a[distance=..48] ["",{"text":"〖路西法〗","color":"#34975A","bold":true,"italic":false},{"text":" 𝔏𝔲𝔠𝔦𝔣𝔢𝔯","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"第二阶段 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"晨星落了下来，落回那棵树上。","color":"#9C9A94","bold":false,"italic":false}]
