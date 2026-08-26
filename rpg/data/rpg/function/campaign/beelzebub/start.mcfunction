execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] run return run tellraw @s ["",{"text":"[第一章] 已有调查实例；请从档案选择加入。","color":"#8B2500","bold":false,"italic":false}]
execute if entity @s[gamemode=spectator] run return run tellraw @s ["",{"text":"[场地校验] 旁观者不能发起章节。","color":"#8B2500","bold":false,"italic":false}]
execute unless dimension minecraft:overworld run return run tellraw @s ["",{"text":"[场地校验] 第一章只能在配置维度展开。","color":"#8B2500","bold":false,"italic":false}]
execute if entity @e[type=minecraft:villager,distance=..72,limit=1] run return run tellraw @s ["",{"text":"[场地校验] 72 格内已有村民；请远离聚落。","color":"#8B2500","bold":false,"italic":false}]
execute if entity @e[type=minecraft:iron_golem,distance=..72,limit=1] run return run tellraw @s ["",{"text":"[场地校验] 72 格内已有聚落守卫。","color":"#8B2500","bold":false,"italic":false}]
execute if entity @e[tag=rpg.advent,distance=..72,limit=1] run return run tellraw @s ["",{"text":"[场地校验] 附近已有恶魔战斗。","color":"#8B2500","bold":false,"italic":false}]
execute if entity @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..72,limit=1] run return run tellraw @s ["",{"text":"[场地校验] 附近已有活动仪式。","color":"#8B2500","bold":false,"italic":false}]
execute if entity @s[y_rotation=-45..45] run scoreboard players set @s rpg_ch1_yaw 0
execute if entity @s[y_rotation=-45..45] rotated 0 0 run return run function rpg:campaign/beelzebub/scene/preflight
execute if entity @s[y_rotation=45.01..135] run scoreboard players set @s rpg_ch1_yaw 1
execute if entity @s[y_rotation=45.01..135] rotated 90 0 run return run function rpg:campaign/beelzebub/scene/preflight
execute if entity @s[y_rotation=-135..-45.01] run scoreboard players set @s rpg_ch1_yaw 2
execute if entity @s[y_rotation=-135..-45.01] rotated -90 0 run return run function rpg:campaign/beelzebub/scene/preflight
scoreboard players set @s rpg_ch1_yaw 3
execute rotated 180 0 run function rpg:campaign/beelzebub/scene/preflight
