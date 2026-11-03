# as 穿戴者，at 其脚下。
execute unless score @s rpg_fm_id matches 1.. store result score @s rpg_fm_id run scoreboard players add #next rpg_fm_id 1
scoreboard players operation #id rpg_fm_id = @s rpg_fm_id
execute as @e[type=minecraft:item_display,tag=rpg.fm.part,distance=..6] if score @s rpg_fm_id = #id rpg_fm_id run tag @s add rpg.fm.mine
execute unless entity @e[type=minecraft:item_display,tag=rpg.fm.part,tag=rpg.fm.mine,limit=1] run function rpg:full_metal/summon
execute if predicate rpg:full_metal/sneaking rotated ~ 0 positioned ~ ~-0.2 ~ as @e[type=minecraft:item_display,tag=rpg.fm.part,tag=rpg.fm.mine] run tp @s ~ ~ ~ ~ ~
execute unless predicate rpg:full_metal/sneaking rotated ~ 0 as @e[type=minecraft:item_display,tag=rpg.fm.part,tag=rpg.fm.mine] run tp @s ~ ~ ~ ~ ~
tag @e[type=minecraft:item_display,tag=rpg.fm.part,tag=rpg.fm.mine] add rpg.fm.seen
tag @e[type=minecraft:item_display,tag=rpg.fm.part,tag=rpg.fm.mine] remove rpg.fm.mine
