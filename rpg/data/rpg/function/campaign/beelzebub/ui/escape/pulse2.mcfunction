execute as @e[type=minecraft:marker,tag=rpg.ch1.ui.escape,limit=1] at @s if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run particle minecraft:spore_blossom_air ~ ~ ~ 1.2 0.5 1.2 0.04 16 normal
schedule function rpg:campaign/beelzebub/ui/escape/pulse3 2t replace
