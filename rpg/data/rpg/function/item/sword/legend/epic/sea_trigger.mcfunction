
advancement revoke @s only rpg:item/sea
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{sea_tag:1b}] run scoreboard players reset @s sea_step
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{sea_tag:1b}] run return 0
scoreboard players add @s sea_step 1
execute if score @s sea_step matches 11.. run scoreboard players set @s sea_step 10
scoreboard players set @s rpg_hud 14
scoreboard players operation @s rpg_hud_p = @s sea_step
scoreboard players set @s rpg_hud_t 3
execute at @s anchored eyes run particle enchant ^ ^ ^0.4 0.25 0.25 0.25 0.2 3 force @s
