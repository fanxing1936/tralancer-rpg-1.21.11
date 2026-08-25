execute as @e[type=minecraft:item,distance=..4] if items entity @s contents minecraft:snowball run tag @s add rpg.rite.offer
execute as @e[type=minecraft:item,distance=..4] if items entity @s contents minecraft:paper[minecraft:custom_data~{rpg_medium:5b}] run tag @s add rpg.rite.offer
execute if entity @e[type=minecraft:item,tag=rpg.rite.offer,distance=..4,limit=1] run return run function rpg:inquest/offer/5
tag @s remove rpg.rite.anchor.active
