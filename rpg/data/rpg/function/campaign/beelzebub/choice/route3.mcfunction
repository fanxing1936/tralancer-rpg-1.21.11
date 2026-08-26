tag @s add rpg.ch1.choice.player
execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..72,limit=1] if score @s rpg_ch1_id = @a[tag=rpg.ch1.choice.player,limit=1] rpg_ch1_id at @s run function rpg:campaign/beelzebub/route/resolve_route3
tag @s remove rpg.ch1.choice.player
