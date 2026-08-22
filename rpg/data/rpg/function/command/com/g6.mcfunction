# 4 行原本各自扫一遍全实体表找 @e[type=minecraft:item,tag=rpg.i.weapon_tag1]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run data modify entity @s Item.components.minecraft:lore append from entity @e[limit=1,distance=..1,type=minecraft:item,tag=rpg.i.add_weapon_tag1] Item.components.minecraft:lore[-3]
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run data modify entity @s Item.components.minecraft:lore append from entity @e[limit=1,distance=..1,type=minecraft:item,tag=rpg.i.add_weapon_tag1] Item.components.minecraft:lore[-2]
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run data modify entity @s Item.components.minecraft:lore append from entity @e[limit=1,distance=..1,type=minecraft:item,tag=rpg.i.add_weapon_tag1] Item.components.minecraft:lore[-1]
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run data modify entity @s Item.components.minecraft:custom_data merge from entity @e[limit=1,distance=..1,type=minecraft:item,tag=rpg.i.add_weapon_tag1] Item.components.minecraft:custom_data
