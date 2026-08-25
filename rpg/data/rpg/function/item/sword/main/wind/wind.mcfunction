
advancement revoke @s only rpg:item/wind_charge
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{wind_tag:1b}] run scoreboard players reset @s wind
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{wind_tag:1b}] run return 0
scoreboard players add @s wind 1
execute if score @s wind matches 51.. run scoreboard players set @s wind 50
scoreboard players set @s rpg_hud 12
scoreboard players operation @s rpg_hud_p = @s wind
scoreboard players operation @s rpg_hud_p /= #rune5 rpg_hud_p
scoreboard players set @s rpg_hud_t 3
execute at @s anchored eyes run particle enchant ^ ^ ^0.4 0.25 0.25 0.25 0.2 4 force @s
