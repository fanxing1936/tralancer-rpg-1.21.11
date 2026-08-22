##附魔
execute if entity @e[type=minecraft:item,tag=rpg.i.gold_tag1] run function rpg:command/com/g0


execute if entity @e[type=minecraft:item,tag=rpg.i.enchant_tag1] run function rpg:command/com/g1

##洗练
execute as @e[type=minecraft:item,tag=rpg.i.sword_tag1] at @s store result score @s weapon_xilian run data get entity @s Item.components.minecraft:custom_data.xilian
execute as @e[type=minecraft:item,tag=rpg.i.diamond_tag1] at @s if entity @e[scores={weapon_xilian=..9},distance=..1,type=minecraft:item,tag=rpg.i.sword_tag1] at @s run particle minecraft:glow ~0.25 ~0.5 ~0.25 -0.5 -1 -0.5 1 100
execute as @e[scores={weapon_xilian=..9},type=minecraft:item,tag=rpg.i.sword_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.diamond_tag1] run item modify entity @s contents rpg:command/xilian_sword
execute as @e[scores={weapon_xilian=..9},type=minecraft:item,tag=rpg.i.sword_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.diamond_tag1] store result score @s random run random value 1..5
execute as @e[scores={random=1},type=minecraft:item,tag=rpg.i.sword_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.diamond_tag1] store result entity @s Item.components.minecraft:attribute_modifiers.modifiers[0].amount double 0.9 run data get entity @s Item.components.minecraft:attribute_modifiers.modifiers[0].amount 1.05
execute as @e[scores={random=2},type=minecraft:item,tag=rpg.i.sword_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.diamond_tag1] store result entity @s Item.components.minecraft:attribute_modifiers.modifiers[0].amount double 1 run data get entity @s Item.components.minecraft:attribute_modifiers.modifiers[0].amount 1.05
execute as @e[scores={random=3},type=minecraft:item,tag=rpg.i.sword_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.diamond_tag1] store result entity @s Item.components.minecraft:attribute_modifiers.modifiers[0].amount double 1.05 run data get entity @s Item.components.minecraft:attribute_modifiers.modifiers[0].amount 1.05
execute as @e[scores={random=4},type=minecraft:item,tag=rpg.i.sword_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.diamond_tag1] store result entity @s Item.components.minecraft:attribute_modifiers.modifiers[0].amount double 1.1 run data get entity @s Item.components.minecraft:attribute_modifiers.modifiers[0].amount 1.05
execute as @e[scores={random=5},type=minecraft:item,tag=rpg.i.sword_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.diamond_tag1] store result entity @s Item.components.minecraft:attribute_modifiers.modifiers[0].amount double 1.15 run data get entity @s Item.components.minecraft:attribute_modifiers.modifiers[0].amount 1.05
scoreboard players reset * random
execute as @e[scores={weapon_xilian=..9},type=minecraft:item,tag=rpg.i.sword_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.diamond_tag1] store result score @s random run random value 1..5
execute as @e[scores={random=1},type=minecraft:item,tag=rpg.i.sword_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.diamond_tag1] store result entity @s Item.components.minecraft:attribute_modifiers.modifiers[1].amount double 0.0085 run data get entity @s Item.components.minecraft:attribute_modifiers.modifiers[1].amount 90
execute as @e[scores={random=2},type=minecraft:item,tag=rpg.i.sword_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.diamond_tag1] store result entity @s Item.components.minecraft:attribute_modifiers.modifiers[1].amount double 0.009 run data get entity @s Item.components.minecraft:attribute_modifiers.modifiers[1].amount 90
execute as @e[scores={random=3},type=minecraft:item,tag=rpg.i.sword_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.diamond_tag1] store result entity @s Item.components.minecraft:attribute_modifiers.modifiers[1].amount double 0.0095 run data get entity @s Item.components.minecraft:attribute_modifiers.modifiers[1].amount 90
execute as @e[scores={random=4},type=minecraft:item,tag=rpg.i.sword_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.diamond_tag1] store result entity @s Item.components.minecraft:attribute_modifiers.modifiers[1].amount double 0.01 run data get entity @s Item.components.minecraft:attribute_modifiers.modifiers[1].amount 90
execute as @e[scores={random=5},type=minecraft:item,tag=rpg.i.sword_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.diamond_tag1] store result entity @s Item.components.minecraft:attribute_modifiers.modifiers[1].amount double 0.0105 run data get entity @s Item.components.minecraft:attribute_modifiers.modifiers[1].amount 90
execute as @e[type=minecraft:item,tag=rpg.i.diamond_tag1] at @s if entity @e[scores={weapon_xilian=..9},distance=..1,type=minecraft:item,tag=rpg.i.sword_tag1] at @s run playsound minecraft:item.totem.use player @a[distance=..5]
execute as @e[scores={weapon_xilian=..9},type=minecraft:item,tag=rpg.i.sword_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.diamond_tag1] run scoreboard players add @s weapon_xilian 1
execute as @e[scores={weapon_xilian=..10},type=minecraft:item,tag=rpg.i.sword_tag1] at @s store result entity @s Item.components.minecraft:custom_data.xilian int 1 run scoreboard players get @s weapon_xilian
execute as @e[type=minecraft:item,tag=rpg.i.diamond_tag1] at @s if entity @e[scores={weapon_xilian=..10},distance=..1,type=minecraft:item,tag=rpg.i.sword_tag1] at @s run kill @s
scoreboard players reset * random








execute as @e[type=minecraft:item,tag=rpg.i.chestplate_tag1] at @s store result score @s weapon_xilian run data get entity @s Item.components.minecraft:custom_data.xilian
execute as @e[type=minecraft:item,tag=rpg.i.diamond_tag1] at @s if entity @e[scores={weapon_xilian=..9},distance=..1,type=minecraft:item,tag=rpg.i.chestplate_tag1] at @s run particle minecraft:glow ~0.25 ~0.5 ~0.25 -0.5 -1 -0.5 1 100
execute as @e[scores={weapon_xilian=..9},type=minecraft:item,tag=rpg.i.chestplate_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.diamond_tag1] run item modify entity @s contents rpg:command/xilian_chestplate
execute as @e[scores={weapon_xilian=..9},type=minecraft:item,tag=rpg.i.chestplate_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.diamond_tag1] store result score @s random run random value 1..5
execute as @e[scores={random=1},type=minecraft:item,tag=rpg.i.chestplate_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.diamond_tag1] store result entity @s Item.components.minecraft:attribute_modifiers.modifiers[0].amount double 0.9 run data get entity @s Item.components.minecraft:attribute_modifiers.modifiers[0].amount 1.05
execute as @e[scores={random=2},type=minecraft:item,tag=rpg.i.chestplate_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.diamond_tag1] store result entity @s Item.components.minecraft:attribute_modifiers.modifiers[0].amount double 1 run data get entity @s Item.components.minecraft:attribute_modifiers.modifiers[0].amount 1.05
execute as @e[scores={random=3},type=minecraft:item,tag=rpg.i.chestplate_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.diamond_tag1] store result entity @s Item.components.minecraft:attribute_modifiers.modifiers[0].amount double 1.05 run data get entity @s Item.components.minecraft:attribute_modifiers.modifiers[0].amount 1.05
execute as @e[scores={random=4},type=minecraft:item,tag=rpg.i.chestplate_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.diamond_tag1] store result entity @s Item.components.minecraft:attribute_modifiers.modifiers[0].amount double 1.1 run data get entity @s Item.components.minecraft:attribute_modifiers.modifiers[0].amount 1.05
execute as @e[scores={random=5},type=minecraft:item,tag=rpg.i.chestplate_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.diamond_tag1] store result entity @s Item.components.minecraft:attribute_modifiers.modifiers[0].amount double 1.15 run data get entity @s Item.components.minecraft:attribute_modifiers.modifiers[0].amount 1.05
scoreboard players reset * random
execute as @e[scores={weapon_xilian=..9},type=minecraft:item,tag=rpg.i.chestplate_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.diamond_tag1] store result score @s random run random value 1..5
execute as @e[scores={random=1},type=minecraft:item,tag=rpg.i.chestplate_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.diamond_tag1] store result entity @s Item.components.minecraft:attribute_modifiers.modifiers[1].amount double 0.0085 run data get entity @s Item.components.minecraft:attribute_modifiers.modifiers[1].amount 90
execute as @e[scores={random=2},type=minecraft:item,tag=rpg.i.chestplate_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.diamond_tag1] store result entity @s Item.components.minecraft:attribute_modifiers.modifiers[1].amount double 0.009 run data get entity @s Item.components.minecraft:attribute_modifiers.modifiers[1].amount 90
execute as @e[scores={random=3},type=minecraft:item,tag=rpg.i.chestplate_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.diamond_tag1] store result entity @s Item.components.minecraft:attribute_modifiers.modifiers[1].amount double 0.0095 run data get entity @s Item.components.minecraft:attribute_modifiers.modifiers[1].amount 90
execute as @e[scores={random=4},type=minecraft:item,tag=rpg.i.chestplate_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.diamond_tag1] store result entity @s Item.components.minecraft:attribute_modifiers.modifiers[1].amount double 0.01 run data get entity @s Item.components.minecraft:attribute_modifiers.modifiers[1].amount 90
execute as @e[scores={random=5},type=minecraft:item,tag=rpg.i.chestplate_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.diamond_tag1] store result entity @s Item.components.minecraft:attribute_modifiers.modifiers[1].amount double 0.0105 run data get entity @s Item.components.minecraft:attribute_modifiers.modifiers[1].amount 90
execute as @e[type=minecraft:item,tag=rpg.i.diamond_tag1] at @s if entity @e[scores={weapon_xilian=..9},distance=..1,type=minecraft:item,tag=rpg.i.chestplate_tag1] at @s run playsound minecraft:item.totem.use player @a[distance=..5]
execute as @e[scores={weapon_xilian=..9},type=minecraft:item,tag=rpg.i.chestplate_tag1] if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.diamond_tag1] at @s run scoreboard players add @s weapon_xilian 1
execute as @e[scores={weapon_xilian=..10},type=minecraft:item,tag=rpg.i.chestplate_tag1] at @s store result entity @s Item.components.minecraft:custom_data.xilian int 1 run scoreboard players get @s weapon_xilian
execute as @e[type=minecraft:item,tag=rpg.i.diamond_tag1] at @s if entity @e[scores={weapon_xilian=..10},distance=..1,type=minecraft:item,tag=rpg.i.chestplate_tag1] at @s run kill @s
scoreboard players reset * random


##锻造
execute if entity @e[type=minecraft:item,tag=rpg.i.echo_tag1] run function rpg:command/com/g2

execute if entity @e[type=minecraft:item,tag=rpg.i.echo_tag2] run function rpg:command/com/g3

##武器设置
##武器注册
execute as @a[tag=rpg.h.sword_tag1] at @s if entity @s[tag=!rpg.h.weapon_tag1] run item modify entity @s weapon.mainhand rpg:command/weapon
execute as @a[tag=rpg.h.chestplate_tag1] at @s if entity @s[tag=!rpg.h.weapon_tag1] run item modify entity @s weapon.mainhand rpg:command/chest_weapon
execute as @a[tag=rpg.h.bow_tag1] at @s if entity @s[tag=!rpg.h.weapon_tag1] run item modify entity @s weapon.mainhand rpg:command/weapon
execute as @a[tag=rpg.e.head_chestplate_tag1] at @s if entity @s[tag=!rpg.e.head_weapon_tag1] run item modify entity @s armor.head rpg:command/chest_weapon
execute as @a[tag=rpg.e.chest_chestplate_tag1] at @s if entity @s[tag=!rpg.e.chest_weapon_tag1] run item modify entity @s armor.chest rpg:command/chest_weapon
execute as @a[tag=rpg.e.legs_chestplate_tag1] at @s if entity @s[tag=!rpg.e.legs_weapon_tag1] run item modify entity @s armor.legs rpg:command/chest_weapon
execute as @a[tag=rpg.e.feet_chestplate_tag1] at @s if entity @s[tag=!rpg.e.feet_weapon_tag1] run item modify entity @s armor.feet rpg:command/chest_weapon

##武器数据读取
execute as @a at @s store result score @s player_attack_damage run attribute @s minecraft:attack_damage get 100
execute as @a at @s store result score @s player_attack_speed run attribute @s minecraft:attack_speed get 100
execute as @a at @s store result score @s player_armor run attribute @s minecraft:armor get 100
execute as @a at @s store result score @s player_armor_toughness run attribute @s minecraft:armor_toughness get 100
execute as @a at @s store result score @s player_attack_damage_ run attribute @s minecraft:attack_damage get
execute as @a at @s store result score @s player_attack_speed_ run attribute @s minecraft:attack_speed get
execute as @a at @s store result score @s player_armor_ run attribute @s minecraft:armor get
execute as @a at @s store result score @s player_armor_toughness_ run attribute @s minecraft:armor_toughness get
execute as @a at @s run scoreboard players operation @s player_attack_speed %= 100 player_attack_speed
execute as @a at @s run scoreboard players operation @s player_attack_damage %= 100 player_attack_damage
execute as @a at @s run scoreboard players operation @s player_armor %= 100 player_armor
execute as @a at @s run scoreboard players operation @s player_armor_toughness %= 100 player_armor_toughness
execute as @a[tag=rpg.h.sword_tag1] at @s run item modify entity @s weapon.mainhand rpg:command/sword_value
execute as @a[tag=rpg.e.head_chestplate_tag1] at @s run item modify entity @s armor.head rpg:command/chestplate_value
execute as @a[tag=rpg.e.chest_chestplate_tag1] at @s run item modify entity @s armor.chest rpg:command/chestplate_value
execute as @a[tag=rpg.e.legs_chestplate_tag1] at @s run item modify entity @s armor.legs rpg:command/chestplate_value
execute as @a[tag=rpg.e.feet_chestplate_tag1] at @s run item modify entity @s armor.feet rpg:command/chestplate_value

##武器等级输入输出
execute if entity @e[type=minecraft:item,tag=rpg.i.weapon_tag1] run function rpg:command/com/g4
execute as @e[type=minecraft:item,tag=rpg.i.level_item1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tag1] run kill
#计算
execute if entity @e[type=minecraft:item,tag=rpg.i.weapon_tag1] run function rpg:command/com/g5

#反馈
execute as @e at @s on attacker if entity @s[scores={weapon_attack=0..},tag=rpg.h.weapon_tag1] run playsound minecraft:entity.warden.attack_impact player @s
execute as @e at @s on attacker if entity @s[scores={weapon_attack=0..},tag=rpg.h.weapon_tag1] run particle crit ~0.25 ~1.5 ~0.25 -0.5 -0.5 -0.5 1 10
scoreboard players reset * weapon_attack

##武器分支
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tree1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run particle minecraft:totem_of_undying ~0.25 ~0.5 ~0.25 -0.5 -1 -0.5 5 100
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tree1] run item modify entity @s contents rpg:command/holy
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tree1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run playsound minecraft:item.totem.use player @a[distance=..5]
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tree1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run kill @s

execute as @e[type=minecraft:item,tag=rpg.i.weapon_tree2] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run particle minecraft:totem_of_undying ~0.25 ~0.5 ~0.25 -0.5 -1 -0.5 5 100
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tree2] run item modify entity @s contents rpg:command/holy2
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tree2] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run playsound minecraft:item.totem.use player @a[distance=..5]
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tree2] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run kill @s

execute as @e[type=minecraft:item,tag=rpg.i.weapon_tree3] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run particle minecraft:totem_of_undying ~0.25 ~0.5 ~0.25 -0.5 -1 -0.5 5 100
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tree3] run item modify entity @s contents rpg:command/holy3
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tree3] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run playsound minecraft:item.totem.use player @a[distance=..5]
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tree3] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run kill @s

execute as @e[type=minecraft:item,tag=rpg.i.weapon_tree4] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run particle minecraft:totem_of_undying ~0.25 ~0.5 ~0.25 -0.5 -1 -0.5 5 100
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tree4] run item modify entity @s contents rpg:command/devil
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tree4] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run playsound minecraft:item.totem.use player @a[distance=..5]
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tree4] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run kill @s

execute as @e[type=minecraft:item,tag=rpg.i.weapon_tree5] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run particle minecraft:totem_of_undying ~0.25 ~0.5 ~0.25 -0.5 -1 -0.5 5 100
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tree5] run item modify entity @s contents rpg:command/devil2
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tree5] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run playsound minecraft:item.totem.use player @a[distance=..5]
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tree5] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run kill @s

execute as @e[type=minecraft:item,tag=rpg.i.weapon_tree6] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run particle minecraft:totem_of_undying ~0.25 ~0.5 ~0.25 -0.5 -1 -0.5 5 100
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tree6] run item modify entity @s contents rpg:command/devil3
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tree6] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run playsound minecraft:item.totem.use player @a[distance=..5]
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tree6] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run kill @s
##显示名称
execute as @e[type=minecraft:item,name=1] at @s run data modify entity @s CustomNameVisible set value 1b
execute as @e[type=minecraft:item,name=1] at @s run data modify entity @s CustomName set from entity @s Item.components.minecraft:custom_name


##玩家面板
execute as @a[tag=rpg.h.skull_tag1] at @s if entity @s[tag=!rpg.h.player_tag1] run item modify entity @s weapon.mainhand rpg:command/player
execute as @a[tag=rpg.h.player_tag1] at @s run item modify entity @s weapon.mainhand rpg:command/player_value

##符石附着
execute if entity @e[type=minecraft:item,tag=rpg.i.weapon_tag1] run function rpg:command/com/g6
execute as @e[type=minecraft:item,nbt={Item:{components:{"minecraft:custom_data":{add_weapon_tag:1b,weapon_tag:1b}}}}] at @s run data remove entity @s Item.components.minecraft:custom_data.add_weapon_tag
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.add_weapon_tag1] run playsound minecraft:block.anvil.use player @a[distance=..5]
execute as @e[type=minecraft:item,tag=rpg.i.add_weapon_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tag1] run particle minecraft:firework ~0.25 ~0.5 ~0.25 -0.5 0 -0.5 0.3 100
execute as @e[type=minecraft:item,tag=rpg.i.add_weapon_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tag1] run kill @s



##铁斧不同攻击效果
