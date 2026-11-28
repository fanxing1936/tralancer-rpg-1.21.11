scoreboard players set #tier rpg_fg 0
scoreboard players set #tier rpg_fg 0
execute if items entity @s weapon.mainhand #rpg:fuse/t_brave run scoreboard players set #tier rpg_fg 1
execute if items entity @s weapon.mainhand #rpg:fuse/t_epic run scoreboard players set #tier rpg_fg 2
execute if score #tier rpg_fg matches 0 run function rpg:forge/fuse/tier_ench {slot:"SelectedItem"}
