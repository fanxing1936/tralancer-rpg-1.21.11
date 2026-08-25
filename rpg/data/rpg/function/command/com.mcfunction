##附魔
execute if entity @e[type=minecraft:item,tag=rpg.i.gold_tag1] run function rpg:command/com/g0


execute if entity @e[type=minecraft:item,tag=rpg.i.enchant_tag1] run function rpg:command/com/g1

##洗练
execute if entity @e[type=minecraft:item,tag=rpg.i.diamond_tag1] run function rpg:command/com/xilian

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

##武器数据读取（5 刻一次；注册与锻造事件仍逐刻响应）
scoreboard players add @a rpg_com_clock 1
execute as @a[scores={rpg_com_clock=5..}] at @s run function rpg:command/com/player_values
scoreboard players set @a[scores={rpg_com_clock=5..}] rpg_com_clock 0

##武器等级输入输出
execute if entity @e[type=minecraft:item,tag=rpg.i.weapon_tag1] run function rpg:command/com/g4
execute as @e[type=minecraft:item,tag=rpg.i.level_item1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tag1] run kill
#计算
execute if entity @e[type=minecraft:item,tag=rpg.i.weapon_tag1] run function rpg:command/com/g5

#反馈
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={weapon_attack=0..},tag=rpg.h.weapon_tag1] run function rpg:command/com/weapon_feedback
scoreboard players reset * weapon_attack

##武器分支
execute if entity @e[type=minecraft:item,tag=rpg.i.weapon_tag1] run function rpg:command/com/branch

##显示名称
execute as @e[type=minecraft:item,name=1] at @s run data modify entity @s CustomNameVisible set value 1b
execute as @e[type=minecraft:item,name=1] at @s run data modify entity @s CustomName set from entity @s Item.components.minecraft:custom_name


##玩家面板
execute as @a[tag=rpg.h.skull_tag1] at @s if entity @s[tag=!rpg.h.player_tag1] run item modify entity @s weapon.mainhand rpg:command/player
# 玩家面板数值并入 5 刻一次的 player_values。

##符石附着
execute if entity @e[type=minecraft:item,tag=rpg.i.weapon_tag1] run function rpg:command/com/g6
execute as @e[type=minecraft:item,nbt={Item:{components:{"minecraft:custom_data":{add_weapon_tag:1b,weapon_tag:1b}}}}] at @s run data remove entity @s Item.components.minecraft:custom_data.add_weapon_tag
execute as @e[type=minecraft:item,tag=rpg.i.weapon_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.add_weapon_tag1] run playsound minecraft:block.anvil.use player @a[distance=..5]
execute as @e[type=minecraft:item,tag=rpg.i.add_weapon_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tag1] run particle minecraft:firework ~0.25 ~0.5 ~0.25 -0.5 0 -0.5 0.3 100
execute as @e[type=minecraft:item,tag=rpg.i.add_weapon_tag1] at @s if entity @e[distance=..1,type=minecraft:item,tag=rpg.i.weapon_tag1] run kill @s



##铁斧不同攻击效果
