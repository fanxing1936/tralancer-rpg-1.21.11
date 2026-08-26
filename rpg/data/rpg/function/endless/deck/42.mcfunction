# 第 42 号编队：安洛先 / 安杜马里 / 比利士 / 华尔 / 安德拉斯
tag @e[tag=rpg.demon.minion] add rpg.end.preexisting
execute if score #spawn rpg_end_tmp matches 1.. positioned ^-8 ^0 ^12 run function rpg:endless/summon/alloces
execute if score #spawn rpg_end_tmp matches 1.. positioned ^-8 ^0 ^12 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.enemy
execute if score #spawn rpg_end_tmp matches 1.. positioned ^-8 ^0 ^12 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.enemy.current
execute if score #spawn rpg_end_tmp matches 1.. positioned ^-8 ^0 ^12 run scoreboard players operation @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] rpg_end_id = @s rpg_end_id
execute if score #spawn rpg_end_tmp matches 1.. positioned ^-8 ^0 ^12 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.preexisting
execute if score #spawn rpg_end_tmp matches 2.. positioned ^8 ^0 ^12 run function rpg:endless/summon/andromalius
execute if score #spawn rpg_end_tmp matches 2.. positioned ^8 ^0 ^12 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.enemy
execute if score #spawn rpg_end_tmp matches 2.. positioned ^8 ^0 ^12 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.enemy.current
execute if score #spawn rpg_end_tmp matches 2.. positioned ^8 ^0 ^12 run scoreboard players operation @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] rpg_end_id = @s rpg_end_id
execute if score #spawn rpg_end_tmp matches 2.. positioned ^8 ^0 ^12 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.preexisting
execute if score #spawn rpg_end_tmp matches 3.. positioned ^0 ^0 ^16 run function rpg:minion/summon/belial/berith
execute if score #spawn rpg_end_tmp matches 3.. positioned ^0 ^0 ^16 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.enemy
execute if score #spawn rpg_end_tmp matches 3.. positioned ^0 ^0 ^16 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.enemy.current
execute if score #spawn rpg_end_tmp matches 3.. positioned ^0 ^0 ^16 run scoreboard players operation @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] rpg_end_id = @s rpg_end_id
execute if score #spawn rpg_end_tmp matches 3.. positioned ^0 ^0 ^16 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.preexisting
execute if score #spawn rpg_end_tmp matches 4.. positioned ^-12 ^0 ^18 run function rpg:endless/summon/uvall
execute if score #spawn rpg_end_tmp matches 4.. positioned ^-12 ^0 ^18 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.enemy
execute if score #spawn rpg_end_tmp matches 4.. positioned ^-12 ^0 ^18 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.enemy.current
execute if score #spawn rpg_end_tmp matches 4.. positioned ^-12 ^0 ^18 run scoreboard players operation @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] rpg_end_id = @s rpg_end_id
execute if score #spawn rpg_end_tmp matches 4.. positioned ^-12 ^0 ^18 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.preexisting
execute if score #spawn rpg_end_tmp matches 5.. positioned ^12 ^0 ^18 run function rpg:endless/summon/andras
execute if score #spawn rpg_end_tmp matches 5.. positioned ^12 ^0 ^18 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.enemy
execute if score #spawn rpg_end_tmp matches 5.. positioned ^12 ^0 ^18 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.enemy.current
execute if score #spawn rpg_end_tmp matches 5.. positioned ^12 ^0 ^18 run scoreboard players operation @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] rpg_end_id = @s rpg_end_id
execute if score #spawn rpg_end_tmp matches 5.. positioned ^12 ^0 ^18 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.preexisting
tag @e[tag=rpg.demon.minion] remove rpg.end.preexisting
execute as @e[tag=rpg.end.enemy.current] run function rpg:endless/enemy/scale
