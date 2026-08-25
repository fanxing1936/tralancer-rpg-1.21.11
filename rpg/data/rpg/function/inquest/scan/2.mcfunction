execute as @e[type=minecraft:item,distance=..4] if items entity @s contents minecraft:prismarine_crystals run tag @s add rpg.rite.offer
execute as @e[type=minecraft:item,distance=..4] if items entity @s contents minecraft:paper[minecraft:custom_data~{rpg_medium:2b}] run tag @s add rpg.rite.offer
execute if entity @e[type=minecraft:item,tag=rpg.rite.offer,distance=..4,limit=1] run return run function rpg:inquest/offer/2
tag @s remove rpg.rite.anchor.active
