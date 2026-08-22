# 10 行原本各自扫一遍全实体表找 @e[type=minecraft:item,tag=rpg.i.weapon_tag1]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
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
