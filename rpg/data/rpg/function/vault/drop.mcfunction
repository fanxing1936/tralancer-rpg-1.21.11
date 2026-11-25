execute at @e[type=minecraft:marker,tag=rpg.vt.me_c,distance=..6,limit=1] run summon minecraft:item ~ ~0.2 ~ {Tags:["rpg.vt.d"],PickupDelay:10s,Item:{id:"minecraft:stone",count:1}}
data modify entity @e[type=minecraft:item,tag=rpg.vt.d,distance=..4,limit=1] Item set from entity @s item
data modify entity @e[type=minecraft:item,tag=rpg.vt.d,distance=..4,limit=1] Owner set from entity @e[type=minecraft:marker,tag=rpg.vt.me_c,distance=..6,limit=1] data.owner
tag @e[type=minecraft:item,tag=rpg.vt.d,distance=..4] remove rpg.vt.d
