scoreboard players set #ch1_choice_ok rpg_ch1_id 0
tag @s add rpg.ch1.choice.player
execute if entity @s[tag=rpg.ch1.member] if score @s rpg_ch1_session = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_session at @s as @e[type=minecraft:item_display,tag=rpg.ch1.rite,distance=..10,sort=nearest,limit=1,scores={rpg_ex_stage=4}] if score @s rpg_ch1_id = @a[tag=rpg.ch1.choice.player,limit=1] rpg_ch1_id run scoreboard players set #ch1_choice_ok rpg_ch1_id 1
tag @s remove rpg.ch1.choice.player
execute at @s if entity @e[type=minecraft:item_display,tag=rpg.ch1.rite,distance=..10,limit=1,scores={rpg_ex_stage=4}] if score #ch1_choice_ok rpg_ch1_id matches 0 run return run function rpg:campaign/beelzebub/verdict/reject
tag @s add rpg.rite.chooser
execute if score @s rpg_ex_choice matches 1 at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..10,sort=nearest,limit=1,scores={rpg_ex_stage=4}] run function rpg:inquest/outcome/eliminate
execute if score @s rpg_ex_choice matches 2 at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..10,sort=nearest,limit=1,scores={rpg_ex_stage=4}] run function rpg:inquest/outcome/banish
execute if score @s rpg_ex_choice matches 3 if items entity @s inventory.* minecraft:paper[minecraft:custom_data~{rpg_lantern:1b}] if entity @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..10,scores={rpg_ex_stage=4}] run tag @s add rpg.rite.choice.ok
execute if score @s rpg_ex_choice matches 3 if entity @s[tag=rpg.rite.choice.ok] run function rpg:inquest/choice/seal
execute if score @s rpg_ex_choice matches 3 unless entity @s[tag=rpg.rite.choice.ok] run tellraw @s ["",{"text":"[封印失败] 需要一盏封魔灯，并站在裁决法阵十格内。","color":"red","italic":false}]
execute if score @s rpg_ex_choice matches 4 at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..10,sort=nearest,limit=1,scores={rpg_ex_stage=4}] run function rpg:inquest/outcome/pact
tag @s remove rpg.rite.choice.ok
tag @s remove rpg.rite.chooser
