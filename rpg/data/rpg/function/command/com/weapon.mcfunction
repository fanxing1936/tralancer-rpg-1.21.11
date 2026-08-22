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
execute as @e[type=minecraft:item,tag=rpg.i.level_item1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tag1] run kill
#计算
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s if score @s weapon_exp >= @s weapon_exp_max run function rpg:command/weapon_level
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s if score @s weapon_exp >= @s weapon_exp_max run scoreboard players operation @s weapon_exp_ -= @s weapon_exp_max
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s if score @s weapon_exp >= @s weapon_exp_max run scoreboard players operation @s weapon_exp_max_ *= 4 weapon_exp_max_
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s if score @s weapon_exp >= @s weapon_exp_max run scoreboard players operation @s weapon_exp_max_ /= 3 weapon_exp_max_
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s if score @s weapon_exp >= @s weapon_exp_max run playsound minecraft:block.trial_spawner.eject_item player @a[distance=..5]
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s if score @s weapon_exp >= @s weapon_exp_max run particle minecraft:totem_of_undying ~-0.5 ~ ~-0.5 1 1 1 0.5 100
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run scoreboard players operation @s weapon_exp = @s weapon_exp_
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s run scoreboard players operation @s weapon_exp_max = @s weapon_exp_max_
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s store result entity @s Item.components.minecraft:custom_data.exp int 1 run scoreboard players get @s weapon_exp
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s store result entity @s Item.components.minecraft:custom_data.exp_max int 1 run scoreboard players get @s weapon_exp_max

#反馈
execute as @e at @s on attacker if entity @s[scores={weapon_attack=0..},tag=rpg.h.weapon_tag1] run playsound minecraft:entity.warden.attack_impact player @s
execute as @e at @s on attacker if entity @s[scores={weapon_attack=0..},tag=rpg.h.weapon_tag1] run particle crit ~0.25 ~1.5 ~0.25 -0.5 -0.5 -0.5 1 30
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