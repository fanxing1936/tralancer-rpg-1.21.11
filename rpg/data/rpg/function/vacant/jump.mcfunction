# 换了一具躯体，仅此而已。
execute as @e[type=minecraft:villager,tag=!rpg.vacant,distance=..16,limit=1,sort=nearest] at @s run function rpg:vacant/take
title @s times 10 50 20
title @s title ["",{"text":"它没有死","italic":false,"color":"dark_purple","bold":true}]
title @s subtitle ["",{"text":"空壳换了一个人","italic":false,"color":"gray"}]
