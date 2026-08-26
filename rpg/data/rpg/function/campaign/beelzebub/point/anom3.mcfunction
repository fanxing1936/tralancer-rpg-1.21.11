execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] if score @s rpg_ch1_id = @e[tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run scoreboard players add @s rpg_ch1_obj 1
playsound minecraft:block.enchantment_table.use player @a[tag=rpg.ch1.current,distance=..24] ~ ~ ~ 0.55 1.35
tellraw @a[tag=rpg.ch1.current,distance=..24] ["",{"text":"[调查] ","color":"#B8A98B","bold":true,"italic":false},{"text":"观察：钟灰混有透明虫翅，落向慈济所后门。","color":"gray","bold":false,"italic":false}]
tellraw @a[tag=rpg.ch1.current,distance=..24] ["",{"text":"陌生女声：","color":"#FFF2A8","bold":true,"italic":false},{"text":"别顺着翅膀找巢。先问它们替谁带路。","color":"gray","bold":false,"italic":false}]
kill @e[type=minecraft:text_display,tag=rpg.ch1.anom3.label,distance=..2]
execute as @e[type=minecraft:item_display,tag=rpg.ch1.anom3.prop,distance=..3] if score @s rpg_ch1_id = @e[tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run kill @s
kill @e[type=minecraft:marker,tag=rpg.ch1.point.active,distance=..0.1]
