# 9 行原本各自扫一遍全实体表找 @e[type=minecraft:item,tag=rpg.i.weapon_tag1]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run item modify entity @s contents rpg:command/weapon_level

execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s store result score @s weapon_level_ run data get entity @s Item.components.minecraft:custom_data.level
#读取
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s store result score @s weapon_exp_max run data get entity @s Item.components.minecraft:custom_data.exp_max
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s store result score @s weapon_exp_max_ run data get entity @s Item.components.minecraft:custom_data.exp_max
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s store result score @s weapon_exp run data get entity @s Item.components.minecraft:custom_data.exp
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s store result score @s weapon_exp_ run data get entity @s Item.components.minecraft:custom_data.exp
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.level_item1] run scoreboard players add @s weapon_exp_ 100
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.level_item1] run particle minecraft:enchant ~-0.5 ~ ~-0.5 1 1 1 0.5 10
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.level_item1] run playsound minecraft:entity.experience_orb.pickup player @a[distance=..5] 
