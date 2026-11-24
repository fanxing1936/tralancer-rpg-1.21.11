summon minecraft:item ~ ~0.3 ~ {Item:{id:"minecraft:stone",count:1},PickupDelay:0,Tags:["rpg.ob.drop"]}
item replace entity @e[type=minecraft:item,tag=rpg.ob.drop,distance=..2,limit=1] contents from entity @s armor.legs
tag @e[type=minecraft:item,tag=rpg.ob.drop] remove rpg.ob.drop
item replace entity @s armor.legs with minecraft:air
