# 甩鞭：浮标即挥鞭。命中判定与收鞭都在同一刻完成，所以不会重复触发。
execute as @e[type=minecraft:fishing_bobber] on origin if entity @s[tag=rpg.h.vine_tag1,level=1..] at @s run function rpg:item/extra/vine_cast
execute as @e[type=minecraft:fishing_bobber] on origin if entity @s[tag=rpg.h.vine_tag1,level=..0] run playsound minecraft:entity.villager.no player @s
execute as @e[type=minecraft:fishing_bobber] on origin if entity @s[tag=rpg.h.vine_tag1] run tag @s add rpg.vine.reel
execute as @e[type=minecraft:fishing_bobber] at @s if entity @a[tag=rpg.vine.reel,distance=..48] run kill @s
tag @a[tag=rpg.vine.reel] remove rpg.vine.reel
