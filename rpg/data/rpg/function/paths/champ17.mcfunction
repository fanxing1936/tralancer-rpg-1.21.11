# 近战记 1、弓弩记 2（rpg_pb_17 是位）
scoreboard players set #r rpg_pa 0
execute if items entity @s weapon.mainhand minecraft:bow run scoreboard players set #r rpg_pa 1
execute if items entity @s weapon.mainhand minecraft:crossbow run scoreboard players set #r rpg_pa 1
execute if score #r rpg_pa matches 1 unless score @s rpg_pb_17 matches 2.. run scoreboard players add @s rpg_pb_17 2
execute if score #r rpg_pa matches 0 if items entity @s weapon.mainhand #rpg:daath/weapon run function rpg:paths/champ17m
scoreboard players set @s rpg_pa_17 0
execute if score @s rpg_pb_17 matches 1 run scoreboard players set @s rpg_pa_17 1
execute if score @s rpg_pb_17 matches 2 run scoreboard players set @s rpg_pa_17 1
execute if score @s rpg_pb_17 matches 3 run scoreboard players set @s rpg_pa_17 2
