tag @s add rpg.ch1.rite.active
execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] if score @s rpg_ch1_id = @e[type=minecraft:item_display,tag=rpg.ch1.rite.active,limit=1] rpg_ch1_id run scoreboard players set @s rpg_ch1_choice 4
function rpg:campaign/beelzebub/ui/verdict/pact
execute as @e[type=minecraft:vindicator,tag=rpg.ch1.boss,tag=rpg.exorcism.bound,distance=..14] if score @s rpg_ch1_id = @e[type=minecraft:item_display,tag=rpg.ch1.rite.active,limit=1] rpg_ch1_id if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.ch1.rite.active,limit=1] rpg_rite_id at @s run function rpg:campaign/beelzebub/escape_boss
execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] if score @s rpg_ch1_id = @e[type=minecraft:item_display,tag=rpg.ch1.rite.active,limit=1] rpg_ch1_id run scoreboard players set @s rpg_ch1_stage 8
execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] if score @s rpg_ch1_id = @e[type=minecraft:item_display,tag=rpg.ch1.rite.active,limit=1] rpg_ch1_id run scoreboard players set @s rpg_ch1_time 0
execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] if score @s rpg_ch1_id = @e[type=minecraft:item_display,tag=rpg.ch1.rite.active,limit=1] rpg_ch1_id at @s run function rpg:campaign/beelzebub/stage/8_enter
function rpg:inquest/tool/cleanup
