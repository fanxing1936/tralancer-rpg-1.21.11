execute unless entity @e[type=minecraft:marker,tag=rpg.end.controller,distance=..16,sort=nearest,limit=1] run return run tellraw @s ["",{"text":"[无法加入] ","color":"#FF665E","bold":true,"italic":false},{"text":"附近 16 格没有活动回廊控制器。","color":"#AAB4C3","bold":false,"italic":false}]
tag @e[type=minecraft:marker,tag=rpg.end.controller] remove rpg.end.controller.current
tag @e[type=minecraft:marker,tag=rpg.end.controller,distance=..16,sort=nearest,limit=1] add rpg.end.controller.current
execute if entity @s[tag=rpg.end.member] run function rpg:endless/member/stale_cleanup
tag @s add rpg.end.member
tag @s add rpg.end.member.current
scoreboard players operation @s rpg_end_id = @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] rpg_end_id
scoreboard players set @s rpg_end_power 0
scoreboard players set @s rpg_end_vital 0
scoreboard players set @s rpg_end_claim 1
scoreboard players set @s rpg_end_pick 0
tellraw @s ["",{"text":"[已加入] ","color":"#62D9E8","bold":true,"italic":false},{"text":"从下一层奖励开始参与选择。","color":"#AAB4C3","bold":false,"italic":false}]
