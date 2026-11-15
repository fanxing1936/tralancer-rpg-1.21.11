# 所有已加载维度的本模型；不影响其它模型，未加载区块内实例不在命令范围。
execute as @e[type=minecraft:armor_stand,tag=rpg.he] at @s run function rpg:heart_of_ender/internal/clear
kill @e[type=minecraft:item_display,tag=rpg.he.part]
