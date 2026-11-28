# 开局走完（as 玩家，还在黑屏里）：排进序章的队
scoreboard players set @s rpg_ob 1
tag @s add rpg.ob.pro
dialog clear @s
title @s times 10 70 20
title @s subtitle {"text":"一千年前 · A Thousand Years Ago","color":"#797979","bold":false,"italic":true}
title @s title {"text":"序章","color":"#FFD85A","bold":true,"italic":false}
function rpg:prologue/enqueue
