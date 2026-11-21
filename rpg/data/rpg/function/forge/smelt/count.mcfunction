execute store result score #ni rpg_fg run clear @s minecraft:iron_ingot[!minecraft:custom_data] 0
execute store result score #nd rpg_fg run clear @s minecraft:diamond[!minecraft:custom_data] 0
execute store result score #nn rpg_fg run clear @s minecraft:netherite_ingot[!minecraft:custom_data] 0
execute store result score #ns rpg_fg run clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"soul"}] 0
execute store result storage rpg:forge d.ni int 1 run scoreboard players get #ni rpg_fg
execute store result storage rpg:forge d.nd int 1 run scoreboard players get #nd rpg_fg
execute store result storage rpg:forge d.nn int 1 run scoreboard players get #nn rpg_fg
execute store result storage rpg:forge d.ns int 1 run scoreboard players get #ns rpg_fg
