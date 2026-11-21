$execute store result score #gl rpg_fg run data get entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:enchantments"."$(id)"
scoreboard players add #gl rpg_fg 1
$execute store result entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:enchantments"."$(id)" int 1 run scoreboard players get #gl rpg_fg
