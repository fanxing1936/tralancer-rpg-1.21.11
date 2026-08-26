execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] if score @s rpg_ch1_id = @e[tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run scoreboard players add @s rpg_ch1_obj 1
playsound minecraft:block.enchantment_table.use player @a[tag=rpg.ch1.current,distance=..24] ~ ~ ~ 0.55 1.35
tellraw @a[tag=rpg.ch1.current,distance=..24] ["",{"text":"[调查] ","color":"#B8A98B","bold":true,"italic":false},{"text":"带血车辙由慈济所出发，与军粮车使用同一规格车轮。","color":"gray","bold":false,"italic":false}]
tellraw @a[tag=rpg.ch1.current,distance=..24] ["",{"text":"伊莱亚：","color":"#D4AF37","bold":true,"italic":false},{"text":"运的不是粮，是被登记为尸体的人。","color":"gray","bold":false,"italic":false}]
execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] at @s run function rpg:campaign/beelzebub/spawn/trail3
kill @e[type=minecraft:text_display,tag=rpg.ch1.trail2.label,distance=..2]
execute as @e[type=minecraft:item_display,tag=rpg.ch1.trail2.prop,distance=..3] if score @s rpg_ch1_id = @e[tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run kill @s
kill @e[type=minecraft:marker,tag=rpg.ch1.point.active,distance=..0.1]
