# 主手的档与星（as 玩家）
execute store result score #q rpg_fg run data get entity @s SelectedItem.components."minecraft:custom_data".rpg_eq.q
execute store result score #st rpg_fg run data get entity @s SelectedItem.components."minecraft:custom_data".rpg_eq.star
scoreboard players set #g rpg_fg 0
execute if score #q rpg_fg matches -5.. run scoreboard players set #g rpg_fg 1
execute if score #q rpg_fg matches 6.. run scoreboard players set #g rpg_fg 2
execute if score #q rpg_fg matches 11.. run scoreboard players set #g rpg_fg 3
function rpg:forge/fuse/cls
execute unless data storage rpg:forge fu{cls:""} run function rpg:forge/fuse/scan with storage rpg:forge fu
execute store result score #nc rpg_fg run data get storage rpg:forge fu.c
execute store result score #ns rpg_fg run clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"soul"}] 0
scoreboard players set #need rpg_fg 0
execute if score #g rpg_fg matches 0 run scoreboard players set #need rpg_fg 1
execute if score #g rpg_fg matches 1 run scoreboard players set #need rpg_fg 2
execute if score #g rpg_fg matches 2 run scoreboard players set #need rpg_fg 4
execute if score #g rpg_fg matches 3 run scoreboard players set #need rpg_fg 6
