execute as @e[type=minecraft:marker,tag=rpg.ch1.ui.escape,limit=1] at @s if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run particle minecraft:ash ~ ~ ~ 0.9 0.4 0.9 0.03 12 normal
schedule function rpg:campaign/beelzebub/ui/escape/pulse2 2t replace
