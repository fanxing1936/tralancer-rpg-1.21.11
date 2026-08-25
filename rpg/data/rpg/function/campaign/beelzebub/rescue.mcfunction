execute unless entity @s[tag=rpg.ch1.member] run return run tellraw @s ["",{"text":"[第一章] 你不在本次固定见证名单中。","color":"#8B2500","bold":false,"italic":false}]
execute unless entity @e[type=minecraft:marker,tag=rpg.ch1.controller,scores={rpg_ch1_stage=9},limit=1] run return run tellraw @s ["",{"text":"[第一章] 现在没有需要救下的见证人。","color":"gray","bold":false,"italic":false}]
execute unless score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run return run tellraw @s ["",{"text":"[第一章] 你的章节编号与当前实例不符。","color":"#8B2500","bold":false,"italic":false}]
execute unless score @s rpg_ch1_session = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_session run return run tellraw @s ["",{"text":"[第一章] 你的会话凭证已失效，请重新登记。","color":"#8B2500","bold":false,"italic":false}]
execute unless score @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_time matches 220.. run return run tellraw @s ["",{"text":"[第一章] 先听完米拉的四项人格见证。","color":"gray","bold":false,"italic":false}]
tag @s add rpg.ch1.rescue.player
tag @e[type=minecraft:villager,tag=rpg.ch1.witness] remove rpg.ch1.witness.current
execute as @e[type=minecraft:villager,tag=rpg.ch1.witness,tag=rpg.ch1.scene] if score @s rpg_ch1_id = @a[tag=rpg.ch1.rescue.player,limit=1] rpg_ch1_id run tag @s add rpg.ch1.witness.current
tag @s remove rpg.ch1.rescue.player
execute unless entity @e[type=minecraft:villager,tag=rpg.ch1.witness.current,distance=..12,limit=1] run return run tellraw @s ["",{"text":"[第一章] 你必须靠近本章节的米拉（12 格内）。","color":"#8B2500","bold":false,"italic":false}]
effect give @e[type=minecraft:villager,tag=rpg.ch1.witness.current,limit=1] minecraft:regeneration 8 2 true
effect give @e[type=minecraft:villager,tag=rpg.ch1.witness.current,limit=1] minecraft:absorption 60 3 true
particle minecraft:totem_of_undying ~ ~1 ~ 1.1 0.8 1.1 0.08 60 force
scoreboard players set @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_obj 1
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[第一次释放] ","color":"#8B2500","bold":true,"italic":false},{"text":"圣力与魔化在同一道伤口中回应。","color":"gray","bold":false,"italic":false}]

execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] if score @s rpg_ch1_id = @a[tag=rpg.ch1.member,tag=rpg.ch1.current,sort=nearest,limit=1] rpg_ch1_id at @s run function rpg:campaign/beelzebub/ui/title/rescue
