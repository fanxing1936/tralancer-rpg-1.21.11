execute unless entity @e[type=minecraft:marker,tag=rpg.end.controller,distance=..96,sort=nearest,limit=1] run return run tellraw @s ["",{"text":"[需要副本] ","color":"#FF665E","bold":true,"italic":false},{"text":"先在附近开启七柱回廊。","color":"#AAB4C3","bold":false,"italic":false}]
tag @e[type=minecraft:marker,tag=rpg.end.controller] remove rpg.end.controller.current
tag @e[type=minecraft:marker,tag=rpg.end.controller,distance=..96,sort=nearest,limit=1] add rpg.end.controller.current
tp @e[tag=rpg.end.enemy] ~ -200 ~
execute as @e[type=minecraft:vex] at @s run function rpg:minion/role/vex_tick
kill @e[tag=rpg.end.enemy]
execute as @e[type=minecraft:vex,tag=rpg.demon.minion.ritual_vex] at @s run function rpg:minion/role/vex_tick
scoreboard players set @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] rpg_end_floor 72
scoreboard players set @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] rpg_end_state 0
scoreboard players set @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] rpg_end_time 79
tellraw @s ["",{"text":"[调试跳层] ","color":"#C28BE0","bold":true,"italic":false},{"text":"下一刻进入第 72 层；不会发放被跳过层数的奖励。","color":"#AAB4C3","bold":false,"italic":false}]
