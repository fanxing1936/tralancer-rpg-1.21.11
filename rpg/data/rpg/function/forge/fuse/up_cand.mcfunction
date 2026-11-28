$execute store result score #cq rpg_fg run data get entity @s Inventory[{Slot:$(n)b}].components."minecraft:custom_data".rpg_eq.q
execute if score #cq rpg_fg matches ..10 run return 0
scoreboard players set #ct rpg_fg 0
$execute if items entity @s container.$(n) #rpg:fuse/t_brave run scoreboard players set #ct rpg_fg 1
$execute if items entity @s container.$(n) #rpg:fuse/t_epic run scoreboard players set #ct rpg_fg 2
scoreboard players operation #keep rpg_fg = #tier rpg_fg
$execute if score #ct rpg_fg matches 0 run function rpg:forge/fuse/tier_ench_slot {n:$(n)}
execute unless score #ct rpg_fg = #keep rpg_fg run return 0
$data modify storage rpg:forge fu.c append value $(n)
