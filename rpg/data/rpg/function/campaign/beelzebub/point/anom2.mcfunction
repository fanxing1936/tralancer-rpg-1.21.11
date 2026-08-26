execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] if score @s rpg_ch1_id = @e[tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run scoreboard players add @s rpg_ch1_obj 1
playsound minecraft:block.enchantment_table.use player @a[tag=rpg.ch1.current,distance=..24] ~ ~ ~ 0.55 1.35
tellraw @a[tag=rpg.ch1.current,distance=..24] ["",{"text":"[调查] ","color":"#B8A98B","bold":true,"italic":false},{"text":"观察：死亡日期是明天，死因统一写作‘疫病净化’。","color":"gray","bold":false,"italic":false}]
function rpg:campaign/beelzebub/give/totem
tellraw @a[tag=rpg.ch1.current,distance=..24] ["",{"text":"伊莱亚：","color":"#D4AF37","bold":true,"italic":false},{"text":"墨水和封印都是真的。这更像命令，不像预言。","color":"gray","bold":false,"italic":false}]
kill @e[type=minecraft:text_display,tag=rpg.ch1.anom2.label,distance=..2]
execute as @e[type=minecraft:item_display,tag=rpg.ch1.anom2.prop,distance=..3] if score @s rpg_ch1_id = @e[tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run kill @s
kill @e[type=minecraft:marker,tag=rpg.ch1.point.active,distance=..0.1]
