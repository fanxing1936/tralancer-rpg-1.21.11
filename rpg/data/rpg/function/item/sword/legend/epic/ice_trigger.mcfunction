
advancement revoke @s only rpg:item/ice
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{ice_tag:1b}] run scoreboard players reset @s ice_step
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{ice_tag:1b}] run return 0
scoreboard players add @s ice_step 1
execute if score @s ice_step matches 46.. run scoreboard players set @s ice_step 45
scoreboard players set @s rpg_hud 13
scoreboard players operation @s rpg_hud_p = @s ice_step
scoreboard players operation @s rpg_hud_p /= #rune5 rpg_hud_p
scoreboard players set @s rpg_hud_t 3
execute at @s anchored eyes run particle enchant ^ ^ ^0.4 0.25 0.25 0.25 0.2 4 force @s
