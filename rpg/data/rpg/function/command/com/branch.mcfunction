# 由 opt_misc.guard_com_sections 从 rpg:command/com 提出。
# 整段只在 rpg.i.weapon_tag1 落在地上时才有意义，所以上层用一次
# type=minecraft:item 的带类型查找把它挡住 —— 行内容原样保留。
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
