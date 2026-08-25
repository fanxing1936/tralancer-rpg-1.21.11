execute facing entity @a[tag=rpg.throne.source,limit=1] eyes run tp @s ^ ^ ^0.8
effect give @s minecraft:glowing 4 0 true
damage @s 8 minecraft:player_attack by @a[tag=rpg.throne.source,limit=1]
tag @s remove rpg.throne.mark
