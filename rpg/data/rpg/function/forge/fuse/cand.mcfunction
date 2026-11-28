$execute store result score #cq rpg_fg run data get entity @s Inventory[{Slot:$(n)b}].components."minecraft:custom_data".rpg_eq.q
scoreboard players set #cg rpg_fg 0
execute if score #cq rpg_fg matches -5.. run scoreboard players set #cg rpg_fg 1
execute if score #cq rpg_fg matches 6.. run scoreboard players set #cg rpg_fg 2
execute if score #cq rpg_fg matches 11.. run scoreboard players set #cg rpg_fg 3
scoreboard players operation #lo rpg_fg = #g rpg_fg
scoreboard players remove #lo rpg_fg 1
execute if score #cg rpg_fg < #lo rpg_fg run return 0
$data modify storage rpg:forge fu.c append value $(n)
