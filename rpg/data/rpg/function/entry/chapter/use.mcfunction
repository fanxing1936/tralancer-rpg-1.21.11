schedule function rpg:entry/chapter/rearm 20t replace
execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] run return run tellraw @s ["",{"text":"[名册未展开] ","color":"#FF3300","bold":true,"italic":false},{"text":"已有章节或回廊实例正在运行；请先完成或结束它。","color":"gray","bold":false,"italic":false}]
execute if entity @e[type=minecraft:marker,tag=rpg.end.controller,limit=1] run return run tellraw @s ["",{"text":"[名册未展开] ","color":"#FF3300","bold":true,"italic":false},{"text":"已有章节或回廊实例正在运行；请先完成或结束它。","color":"gray","bold":false,"italic":false}]
execute if entity @s[gamemode=spectator] run return run tellraw @s ["",{"text":"[名册未展开] ","color":"#FF3300","bold":true,"italic":false},{"text":"请回到主世界、退出旁观模式，再到旷野打开名册。","color":"gray","bold":false,"italic":false}]
execute unless dimension minecraft:overworld run return run tellraw @s ["",{"text":"[名册未展开] ","color":"#FF3300","bold":true,"italic":false},{"text":"请回到主世界、退出旁观模式，再到旷野打开名册。","color":"gray","bold":false,"italic":false}]
execute if entity @e[type=minecraft:villager,distance=..72,limit=1] run return run tellraw @s ["",{"text":"[名册未展开] ","color":"#FF3300","bold":true,"italic":false},{"text":"这里离聚落太近。带着名册走到旷野（72 格内无村民与铁傀儡）再打开。","color":"gray","bold":false,"italic":false}]
execute if entity @e[type=minecraft:iron_golem,distance=..72,limit=1] run return run tellraw @s ["",{"text":"[名册未展开] ","color":"#FF3300","bold":true,"italic":false},{"text":"这里离聚落太近。带着名册走到旷野（72 格内无村民与铁傀儡）再打开。","color":"gray","bold":false,"italic":false}]
execute if entity @e[tag=rpg.advent,distance=..72,limit=1] run return run tellraw @s ["",{"text":"[名册未展开] ","color":"#FF3300","bold":true,"italic":false},{"text":"附近还有恶魔战斗或活动法阵；先收尾，再到旷野打开名册。","color":"gray","bold":false,"italic":false}]
execute if entity @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..72,limit=1] run return run tellraw @s ["",{"text":"[名册未展开] ","color":"#FF3300","bold":true,"italic":false},{"text":"附近还有恶魔战斗或活动法阵；先收尾，再到旷野打开名册。","color":"gray","bold":false,"italic":false}]
tag @s add rpg.ch1.roster.open
function rpg:campaign/beelzebub/start
tag @s remove rpg.ch1.roster.open
