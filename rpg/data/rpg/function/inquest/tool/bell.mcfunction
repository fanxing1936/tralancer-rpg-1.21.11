execute if entity @s[scores={rpg_ex_toolcd=1..}] run return 0
tag @s add rpg.rite.chooser
execute at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..16,sort=nearest,limit=1,scores={rpg_ex_stage=2..4}] run function rpg:inquest/tool/bell_anchor
tag @s remove rpg.rite.chooser
scoreboard players set @s rpg_ex_toolcd 300
effect give @s minecraft:glowing 8 0 true
effect give @s minecraft:weakness 8 0 true
