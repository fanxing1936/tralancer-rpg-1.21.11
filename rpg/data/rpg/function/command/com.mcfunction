# 已退役：装备养成重置（docs/EQUIP-REWORK.md）由 rpg:forge/* 接管。
##显示名称
execute as @e[type=minecraft:item,name=1] at @s run data modify entity @s CustomNameVisible set value 1b
execute as @e[type=minecraft:item,name=1] at @s run data modify entity @s CustomName set from entity @s Item.components.minecraft:custom_name


##玩家面板
execute as @a[tag=rpg.h.skull_tag1] at @s if entity @s[tag=!rpg.h.player_tag1] run item modify entity @s weapon.mainhand rpg:command/player
# 玩家面板数值并入 5 刻一次的 player_values。

execute as @a[scores={rpg_com_clock=5..}] at @s run function rpg:command/com/player_values
scoreboard players add @a rpg_com_clock 1
scoreboard players set @a[scores={rpg_com_clock=5..}] rpg_com_clock 0
