# 落到门内（as 玩家）
tag @s remove rpg.pl.wait
tag @s add rpg.pl.in
scoreboard players add @s rpg_pl_best 0
scoreboard players set @s rpg_pl_dc 0
execute in rpg:paradise_lost run tp @s 0.5 88 17.5 180 0
effect give @s minecraft:slow_falling 5 0 true
playsound minecraft:block.end_portal.spawn player @s ~ ~ ~ 0.5 0.6
title @s times 10 50 20
title @s title ["",{"text":"失乐园","color":"#E0483C","bold":true,"italic":false}]
title @s subtitle ["",{"text":"𝔓𝔞𝔯𝔞𝔡𝔦𝔰𝔢 𝔏𝔬𝔰𝔱","color":"#8F7430","bold":false,"italic":false}]
function rpg:quest/start_7
execute if items entity @s container.* minecraft:paper[minecraft:custom_data~{rpg_eden_pass:1b}] run function rpg:pl/pass
