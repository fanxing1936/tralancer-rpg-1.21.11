scoreboard players set @s rpg_dt_ph 2
scoreboard players set @s rpg_dt_pt 0
execute store result storage rpg:daath t.n int 1 run scoreboard players get @s rpg_dt
function rpg:daath_fight/pl/down_m with storage rpg:daath t
tag @s add rpg.dt.in
effect give @s minecraft:slow_falling 3 0 true
title @s times 10 50 20
title @s subtitle ["",{"text":"דעת","color":"#8F7430","bold":false,"italic":false}]
title @s title ["",{"text":"Daath","color":"#AAB4C3","bold":true,"italic":false}]
playsound minecraft:block.end_portal.spawn player @s ~ ~ ~ 0.5 0.5
