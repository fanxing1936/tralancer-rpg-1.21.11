tag @s add rpg.ch1.debug.controller
tag @e[tag=rpg.ch1.debug.current,distance=..72] remove rpg.ch1.debug.current
execute as @e[tag=rpg.ch1.scene,tag=!rpg.ch1.controller,distance=..72] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.debug.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.debug.current
execute as @e[tag=rpg.ch1.minion,distance=..72] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.debug.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.debug.current
execute as @e[tag=rpg.ch1.boss,distance=..72] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.debug.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.debug.current
execute as @e[type=minecraft:item_display,tag=rpg.ch1.rite,distance=..72] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.debug.controller,limit=1] rpg_ch1_id at @s run function rpg:inquest/tool/cleanup
kill @e[tag=rpg.ch1.debug.current,distance=..72]
tag @s remove rpg.ch1.recap.anomaly
tag @s remove rpg.ch1.recap.minions
tag @s remove rpg.ch1.recap.area
tag @s remove rpg.ch1.recap.hypothesis
tag @s remove rpg.ch1.recap.prep
tag @s remove rpg.ch1.witness.ready
tag @s remove rpg.ch1.debug.no_commit
scoreboard players set @s rpg_ch1_time 0
scoreboard players set @s rpg_ch1_obj 0
scoreboard players set @s rpg_ch1_sub 0
scoreboard players set @s rpg_ch1_guard 0
scoreboard players set @s rpg_ch1_rescue 0
tag @s remove rpg.ch1.debug.controller
