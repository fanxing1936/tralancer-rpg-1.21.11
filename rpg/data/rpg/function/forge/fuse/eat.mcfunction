# 吃掉一把祭品（宏：fu.c[0] 是格号）：经验的一半记进 #xa
$execute store result score #cx rpg_fg run data get entity @s Inventory[{Slot:$(c0)b}].components."minecraft:custom_data".rpg_eq.xp
scoreboard players operation #cx rpg_fg /= #2 rpg_fg
scoreboard players operation #xa rpg_fg += #cx rpg_fg
$item replace entity @s container.$(c0) with minecraft:air
