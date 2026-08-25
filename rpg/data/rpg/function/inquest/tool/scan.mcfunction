execute as @e[type=minecraft:item,distance=..3] if items entity @s contents *[minecraft:custom_data~{rpg_nail:1b}] run tag @s add rpg.rite.tool.nail
execute unless entity @s[tag=rpg.rite.nailed] as @e[type=minecraft:item,tag=rpg.rite.tool.nail,distance=..3,sort=nearest,limit=1] run return run function rpg:inquest/tool/nail_item
tag @e[type=minecraft:item,tag=rpg.rite.tool.nail,distance=..3] remove rpg.rite.tool.nail
execute as @e[type=minecraft:item,distance=..3] if items entity @s contents *[minecraft:custom_data~{rpg_chalk:1b}] run tag @s add rpg.rite.tool.chalk1
execute if score @s rpg_ex_slots matches 1.. unless entity @s[tag=rpg.layout.guard] as @e[type=minecraft:item,tag=rpg.rite.tool.chalk1,distance=..3,sort=nearest,limit=1] run return run function rpg:inquest/tool/chalk1_item
tag @e[type=minecraft:item,tag=rpg.rite.tool.chalk1,distance=..3] remove rpg.rite.tool.chalk1
execute as @e[type=minecraft:item,distance=..3] if items entity @s contents *[minecraft:custom_data~{rpg_chalk:2b}] run tag @s add rpg.rite.tool.chalk2
execute if score @s rpg_ex_slots matches 1.. unless entity @s[tag=rpg.layout.suppress] as @e[type=minecraft:item,tag=rpg.rite.tool.chalk2,distance=..3,sort=nearest,limit=1] run return run function rpg:inquest/tool/chalk2_item
tag @e[type=minecraft:item,tag=rpg.rite.tool.chalk2,distance=..3] remove rpg.rite.tool.chalk2
execute as @e[type=minecraft:item,distance=..3] if items entity @s contents *[minecraft:custom_data~{rpg_chalk:3b}] run tag @s add rpg.rite.tool.chalk3
execute if score @s rpg_ex_slots matches 1.. unless entity @s[tag=rpg.layout.haste] as @e[type=minecraft:item,tag=rpg.rite.tool.chalk3,distance=..3,sort=nearest,limit=1] run return run function rpg:inquest/tool/chalk3_item
tag @e[type=minecraft:item,tag=rpg.rite.tool.chalk3,distance=..3] remove rpg.rite.tool.chalk3
execute as @e[type=minecraft:item,distance=..3] if items entity @s contents *[minecraft:custom_data~{rpg_incense:1b}] run tag @s add rpg.rite.tool.incense
execute unless score @s rpg_ex_toolcd matches 1.. as @e[type=minecraft:item,tag=rpg.rite.tool.incense,distance=..3,sort=nearest,limit=1] run return run function rpg:inquest/tool/incense_item
tag @e[type=minecraft:item,tag=rpg.rite.tool.incense,distance=..3] remove rpg.rite.tool.incense
