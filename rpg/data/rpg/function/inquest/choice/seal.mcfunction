execute at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..10,sort=nearest,limit=1,scores={rpg_ex_stage=4}] run function rpg:inquest/tool/place/lantern
clear @s minecraft:paper[minecraft:custom_data~{rpg_lantern:1b}] 1
execute at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..10,sort=nearest,limit=1,scores={rpg_ex_stage=4}] run function rpg:inquest/outcome/seal
