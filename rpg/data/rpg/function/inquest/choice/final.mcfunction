tag @s add rpg.rite.chooser
execute if score @s rpg_ex_choice matches 1 at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..10,sort=nearest,limit=1,scores={rpg_ex_stage=4}] run function rpg:inquest/outcome/eliminate
execute if score @s rpg_ex_choice matches 2 at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..10,sort=nearest,limit=1,scores={rpg_ex_stage=4}] run function rpg:inquest/outcome/banish
execute if score @s rpg_ex_choice matches 3 if items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_lantern:1b}] if entity @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..10,scores={rpg_ex_stage=4}] run tag @s add rpg.rite.choice.ok
execute if score @s rpg_ex_choice matches 3 if entity @s[tag=rpg.rite.choice.ok] run function rpg:inquest/choice/seal
execute if score @s rpg_ex_choice matches 3 unless entity @s[tag=rpg.rite.choice.ok] run tellraw @s ["",{"text":"[封印失败] 需要一盏封魔灯，并站在裁决法阵十格内。","color":"red","italic":false}]
execute if score @s rpg_ex_choice matches 4 at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..10,sort=nearest,limit=1,scores={rpg_ex_stage=4}] run function rpg:inquest/outcome/pact
tag @s remove rpg.rite.choice.ok
tag @s remove rpg.rite.chooser
