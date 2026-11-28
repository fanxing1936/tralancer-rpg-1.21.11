# 重锤、弓弩：看附魔（宏 slot：SelectedItem 或 Inventory[{Slot:Nb}]）
scoreboard players set #e1 rpg_fg 0
scoreboard players set #e2 rpg_fg 0
$execute store result score #e1 rpg_fg run data get entity @s $(slot).components."minecraft:enchantments"."minecraft:unbreaking"
$execute store result score #e2 rpg_fg run data get entity @s $(slot).components."minecraft:enchantments"."minecraft:power"
$execute if score #e2 rpg_fg matches 0 store result score #e2 rpg_fg run data get entity @s $(slot).components."minecraft:enchantments"."minecraft:quick_charge"
execute if items entity @s weapon.mainhand minecraft:mace run scoreboard players operation #e2 rpg_fg = #e1 rpg_fg
execute if items entity @s weapon.mainhand minecraft:mace run scoreboard players add #e2 rpg_fg 1
execute if items entity @s weapon.mainhand minecraft:mace run scoreboard players add #e1 rpg_fg 1
scoreboard players operation #e1 rpg_fg < #e2 rpg_fg
scoreboard players remove #e1 rpg_fg 1
execute if score #e1 rpg_fg matches 1.. run scoreboard players operation #tier rpg_fg = #e1 rpg_fg
execute if score #tier rpg_fg matches 3.. run scoreboard players set #tier rpg_fg 2
