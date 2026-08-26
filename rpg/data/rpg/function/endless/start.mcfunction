execute if entity @e[type=minecraft:marker,tag=rpg.end.controller,limit=1] run return run tellraw @s ["",{"text":"[回廊占用] ","color":"#FF665E","bold":true,"italic":false},{"text":"已有无尽副本正在运行；请加入或等待其结束。","color":"#AAB4C3","bold":false,"italic":false}]
execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] run return run tellraw @s ["",{"text":"[章节占用] ","color":"#FF665E","bold":true,"italic":false},{"text":"第一章实例运行期间不能开启无尽副本。","color":"#AAB4C3","bold":false,"italic":false}]
scoreboard players add #next rpg_end_id 1
execute if score #next rpg_end_id matches ..0 run scoreboard players set #next rpg_end_id 1
execute as @a[tag=rpg.end.member] run function rpg:endless/member/stale_cleanup
summon minecraft:marker ~ ~ ~ {Tags:["rpg.end.controller","rpg.end.controller.new"]}
data modify entity @e[type=minecraft:marker,tag=rpg.end.controller.new,distance=..2,sort=nearest,limit=1] Rotation set from entity @s Rotation
scoreboard players operation @e[type=minecraft:marker,tag=rpg.end.controller.new,distance=..2,sort=nearest,limit=1] rpg_end_id = #next rpg_end_id
execute as @e[type=minecraft:marker,tag=rpg.end.controller.new,distance=..2,sort=nearest,limit=1] at @s run function rpg:endless/setup
