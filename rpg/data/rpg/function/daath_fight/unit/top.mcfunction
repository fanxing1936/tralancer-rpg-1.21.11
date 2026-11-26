attribute @s minecraft:max_health base set 1024
data modify entity @s Health set value 1024f
execute unless items entity @s weapon.offhand *[minecraft:death_protection] run item replace entity @s weapon.offhand with minecraft:paper[minecraft:death_protection={},minecraft:item_model="rpg:empty"]
