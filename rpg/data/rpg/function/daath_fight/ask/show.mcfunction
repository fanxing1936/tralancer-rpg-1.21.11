title @a[tag=rpg.dt.me,limit=1] times 5 60 10
$title @a[tag=rpg.dt.me,limit=1] subtitle {"text":"$(q)","color":"#FFFFFF","italic":false}
title @a[tag=rpg.dt.me,limit=1] title {"text":""}
$tellraw @a[tag=rpg.dt.me,limit=1] ["",{"text":"〖","color":"#7C8593","bold":true},{"selector":"@a[tag=rpg.dt.me,limit=1]","color":"#FFFFFF","bold":true},{"text":"〗　","color":"#7C8593","bold":true},{"text":"$(q)","color":"#E6DFCF","bold":false}]
$execute if score @s rpg_dt_q matches 0 at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] positioned ~0.00 ~ ~-11.00 run function rpg:daath_fight/ask/card {x:"$(a0)",k:0}
$execute if score @s rpg_dt_q matches 0 at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] positioned ~9.53 ~ ~5.50 run function rpg:daath_fight/ask/card {x:"$(a1)",k:1}
$execute if score @s rpg_dt_q matches 0 at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] positioned ~-9.53 ~ ~5.50 run function rpg:daath_fight/ask/card {x:"$(a2)",k:2}
$execute if score @s rpg_dt_q matches 1 at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] positioned ~0.00 ~ ~-11.00 run function rpg:daath_fight/ask/card {x:"$(a2)",k:0}
$execute if score @s rpg_dt_q matches 1 at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] positioned ~9.53 ~ ~5.50 run function rpg:daath_fight/ask/card {x:"$(a0)",k:1}
$execute if score @s rpg_dt_q matches 1 at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] positioned ~-9.53 ~ ~5.50 run function rpg:daath_fight/ask/card {x:"$(a1)",k:2}
$execute if score @s rpg_dt_q matches 2 at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] positioned ~0.00 ~ ~-11.00 run function rpg:daath_fight/ask/card {x:"$(a1)",k:0}
$execute if score @s rpg_dt_q matches 2 at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] positioned ~9.53 ~ ~5.50 run function rpg:daath_fight/ask/card {x:"$(a2)",k:1}
$execute if score @s rpg_dt_q matches 2 at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] positioned ~-9.53 ~ ~5.50 run function rpg:daath_fight/ask/card {x:"$(a0)",k:2}
