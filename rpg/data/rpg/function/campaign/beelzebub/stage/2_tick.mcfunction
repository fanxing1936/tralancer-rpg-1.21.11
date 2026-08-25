tag @e[type=minecraft:villager,tag=rpg.ch1.vacant] remove rpg.ch1.vacant.current
execute as @e[type=minecraft:villager,tag=rpg.ch1.vacant] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.vacant.current
execute as @e[type=minecraft:villager,tag=rpg.ch1.vacant.current,limit=1] at @s if entity @a[tag=rpg.ch1.current,tag=rpg.holy,distance=..8,limit=1] run function rpg:vacant/reveal
execute as @e[type=minecraft:villager,tag=rpg.ch1.vacant.current,scores={rpg_vac_x=-80..},limit=1] at @s run function rpg:campaign/beelzebub/vacant_reveal
execute if score @s rpg_ch1_obj matches 1.. run function rpg:campaign/beelzebub/advance
