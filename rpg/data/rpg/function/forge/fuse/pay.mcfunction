execute if score #k rpg_fg matches 1.. run clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"soul"}] 1
scoreboard players remove #k rpg_fg 1
execute if score #k rpg_fg matches 1.. run function rpg:forge/fuse/pay
