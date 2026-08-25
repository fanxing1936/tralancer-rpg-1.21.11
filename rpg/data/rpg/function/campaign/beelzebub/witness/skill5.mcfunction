tag @s add rpg.ch1.witness.player
execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..72,limit=1] if score @s rpg_ch1_id = @a[tag=rpg.ch1.witness.player,limit=1] rpg_ch1_id unless entity @s[tag=rpg.ch1.witness.skill.5] run function rpg:campaign/beelzebub/witness/record5
tag @s remove rpg.ch1.witness.player
