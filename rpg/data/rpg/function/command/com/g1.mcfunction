# 4 行原本各自扫一遍全实体表找 @e[type=minecraft:item,tag=rpg.i.enchant_tag1]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[type=minecraft:item,tag=rpg.i.enchant_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run particle minecraft:wax_on ~0.25 ~0.5 ~0.25 -0.5 -1 -0.5 5 100 
execute as @e[type=minecraft:item,tag=rpg.i.enchant_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run data modify entity @e[limit=1,type=item,distance=0.1..1] Item.components.minecraft:enchantments.levels merge from entity @s Item.components.minecraft:enchantments.levels
execute as @e[type=minecraft:item,tag=rpg.i.enchant_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run playsound minecraft:item.totem.use player @a[distance=..5]
execute as @e[type=minecraft:item,tag=rpg.i.enchant_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run kill @s
