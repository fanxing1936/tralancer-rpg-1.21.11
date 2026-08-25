execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] if score @s rpg_ch1_id = @e[tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run scoreboard players add @s rpg_ch1_obj 1
playsound minecraft:block.enchantment_table.use player @a[tag=rpg.ch1.current,distance=..24] ~ ~ ~ 0.55 1.35
tellraw @a[tag=rpg.ch1.current,distance=..24] ["",{"text":"[调查] ","color":"#B8A98B","bold":true,"italic":false},{"text":"封存器具已按参与档案分发。","color":"gray","bold":false,"italic":false}]
execute as @a[tag=rpg.ch1.current] run function rpg:campaign/beelzebub/give/pending_page
execute as @a[tag=rpg.ch1.current] run function rpg:inquest/give/medium4
kill @e[type=minecraft:text_display,tag=rpg.ch1.cache1.label,distance=..2]
execute as @e[type=minecraft:item_display,tag=rpg.ch1.cache1.prop,distance=..3] if score @s rpg_ch1_id = @e[tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run kill @s
kill @e[type=minecraft:marker,tag=rpg.ch1.point.active,distance=..0.1]
