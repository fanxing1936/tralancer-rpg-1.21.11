# 引燃：先点上引信，等目标的受击无敌过去再炸开，伤害才落得满
scoreboard players reset @s rpg_mi_flame
tag @s remove rpg.mi.marked
tag @s add rpg.mi.fuse
scoreboard players set @s rpg_mi_fuse 11
execute if entity @a[tag=rpg.mi.owner,tag=rpg.mi.pair] run tag @s add rpg.mi.pairfuse
playsound minecraft:item.firecharge.use player @a[distance=..16] ~ ~ ~ 0.8 0.7
