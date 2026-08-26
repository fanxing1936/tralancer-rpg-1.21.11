# 第 5 号编队：莫拉格斯 / 劳姆 / 毛莫 / 但他林 / 艾利欧格
tag @e[tag=rpg.demon.minion] add rpg.end.preexisting
execute if score #spawn rpg_end_tmp matches 1.. positioned ^-8 ^0 ^12 run function rpg:minion/summon/samael/marax
execute if score #spawn rpg_end_tmp matches 1.. positioned ^-8 ^0 ^12 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.enemy
execute if score #spawn rpg_end_tmp matches 1.. positioned ^-8 ^0 ^12 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.enemy.current
execute if score #spawn rpg_end_tmp matches 1.. positioned ^-8 ^0 ^12 run scoreboard players operation @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] rpg_end_id = @s rpg_end_id
execute if score #spawn rpg_end_tmp matches 1.. positioned ^-8 ^0 ^12 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.preexisting
execute if score #spawn rpg_end_tmp matches 2.. positioned ^8 ^0 ^12 run function rpg:endless/summon/raum
execute if score #spawn rpg_end_tmp matches 2.. positioned ^8 ^0 ^12 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.enemy
execute if score #spawn rpg_end_tmp matches 2.. positioned ^8 ^0 ^12 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.enemy.current
execute if score #spawn rpg_end_tmp matches 2.. positioned ^8 ^0 ^12 run scoreboard players operation @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] rpg_end_id = @s rpg_end_id
execute if score #spawn rpg_end_tmp matches 2.. positioned ^8 ^0 ^12 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.preexisting
execute if score #spawn rpg_end_tmp matches 3.. positioned ^0 ^0 ^16 run function rpg:endless/summon/murmur
execute if score #spawn rpg_end_tmp matches 3.. positioned ^0 ^0 ^16 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.enemy
execute if score #spawn rpg_end_tmp matches 3.. positioned ^0 ^0 ^16 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.enemy.current
execute if score #spawn rpg_end_tmp matches 3.. positioned ^0 ^0 ^16 run scoreboard players operation @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] rpg_end_id = @s rpg_end_id
execute if score #spawn rpg_end_tmp matches 3.. positioned ^0 ^0 ^16 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.preexisting
execute if score #spawn rpg_end_tmp matches 4.. positioned ^-12 ^0 ^18 run function rpg:endless/summon/dantalion
execute if score #spawn rpg_end_tmp matches 4.. positioned ^-12 ^0 ^18 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.enemy
execute if score #spawn rpg_end_tmp matches 4.. positioned ^-12 ^0 ^18 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.enemy.current
execute if score #spawn rpg_end_tmp matches 4.. positioned ^-12 ^0 ^18 run scoreboard players operation @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] rpg_end_id = @s rpg_end_id
execute if score #spawn rpg_end_tmp matches 4.. positioned ^-12 ^0 ^18 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.preexisting
execute if score #spawn rpg_end_tmp matches 5.. positioned ^12 ^0 ^18 run function rpg:minion/summon/abaddon/eligos
execute if score #spawn rpg_end_tmp matches 5.. positioned ^12 ^0 ^18 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.enemy
execute if score #spawn rpg_end_tmp matches 5.. positioned ^12 ^0 ^18 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.enemy.current
execute if score #spawn rpg_end_tmp matches 5.. positioned ^12 ^0 ^18 run scoreboard players operation @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] rpg_end_id = @s rpg_end_id
execute if score #spawn rpg_end_tmp matches 5.. positioned ^12 ^0 ^18 run tag @e[tag=rpg.demon.minion,tag=!rpg.end.preexisting,distance=..3,sort=nearest,limit=1] add rpg.end.preexisting
tag @e[tag=rpg.demon.minion] remove rpg.end.preexisting
execute as @e[tag=rpg.end.enemy.current] run function rpg:endless/enemy/scale
