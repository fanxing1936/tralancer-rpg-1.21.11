particle minecraft:totem_of_undying ~-0.5 ~ ~-0.5 1 1 1 0.5 100
title @s title ["",{"text":"†","bold":true,"color":"white"},{"text":"LEVEL","bold":true,"color":"yellow"}," ",{"text":"UP","color":"gold","bold":true},{"text":"†","color":"white","bold":true}]
title @s subtitle ["♣当前",{"text":"等级","color":"gold","bold":true},"：",{"score":{"objective":"level","name":"@s"}}]
effect give @s minecraft:instant_health 1 10 true
scoreboard players operation @s player_level = @s level
