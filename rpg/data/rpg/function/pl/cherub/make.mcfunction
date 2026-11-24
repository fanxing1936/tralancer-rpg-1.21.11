tag @s add rpg.pl.b.cherub
tag @s add rpg.pl.g
attribute @s minecraft:max_health base set 320
attribute @s minecraft:attack_damage base set 12
data modify entity @s Health set value 320f
data modify entity @s CustomNameVisible set value 1b
data modify entity @s CustomName set value ["",{"text":"ℭ𝔥𝔢𝔯𝔲𝔟","color":"#FFFFFF","bold":false,"italic":false}]
particle minecraft:flame ~ ~1 ~ 1 2 1 0.1 120
playsound minecraft:item.trident.thunder master @a[distance=..48] ~ ~ ~ 1 0.8
