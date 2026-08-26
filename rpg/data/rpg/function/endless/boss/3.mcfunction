tag @e[type=minecraft:vindicator,tag=rpg.advent] add rpg.end.preexisting
function rpg:taint/lord3
tag @e[type=minecraft:vindicator,tag=rpg.advent,tag=!rpg.end.preexisting,distance=..4,sort=nearest,limit=1] add rpg.end.enemy
tag @e[type=minecraft:vindicator,tag=rpg.advent,tag=!rpg.end.preexisting,distance=..4,sort=nearest,limit=1] add rpg.end.enemy.current
tag @e[type=minecraft:vindicator,tag=rpg.advent,tag=!rpg.end.preexisting,distance=..4,sort=nearest,limit=1] add rpg.end.boss
scoreboard players operation @e[type=minecraft:vindicator,tag=rpg.advent,tag=!rpg.end.preexisting,distance=..4,sort=nearest,limit=1] rpg_end_id = @s rpg_end_id
tag @e[type=minecraft:vindicator,tag=rpg.advent] remove rpg.end.preexisting
execute as @e[tag=rpg.end.enemy.current,tag=rpg.end.boss] run function rpg:endless/enemy/scale
tellraw @a[tag=rpg.end.member.current,distance=..96] ["",{"text":"[领主降临] ","color":"#5B5B62","bold":true,"italic":false},{"text":"亚巴顿 ","color":"#6A6A70","bold":false,"italic":false},{"text":"封锁本层出口。","color":"#AAB4C3","bold":false,"italic":false}]
