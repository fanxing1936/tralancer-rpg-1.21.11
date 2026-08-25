tag @e[type=minecraft:item_display,tag=rpg.ch1.ui.prop,distance=..72] remove rpg.ch1.ui.current
execute as @e[type=minecraft:item_display,tag=rpg.ch1.ui.prop,distance=..72] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.ui.current
execute as @e[type=minecraft:item_display,tag=rpg.ch1.ui.current,distance=..72] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run kill @s
tag @e[type=minecraft:block_display,tag=rpg.ch1.ui.prop,distance=..72] remove rpg.ch1.ui.current
execute as @e[type=minecraft:block_display,tag=rpg.ch1.ui.prop,distance=..72] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.ui.current
execute as @e[type=minecraft:block_display,tag=rpg.ch1.ui.current,distance=..72] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run kill @s
