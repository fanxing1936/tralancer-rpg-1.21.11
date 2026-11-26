advancement revoke @s only rpg:panel/head_use
execute unless score @s rpg_panel_u matches 1.. run function rpg:panel/open
scoreboard players set @s rpg_panel_u 6
