gamemode adventure @s
function rpg:prologue_i2/player/to_west
effect give @s minecraft:instant_health 1 9 true
item replace entity @s weapon.offhand with minecraft:paper[minecraft:death_protection={},minecraft:item_model="rpg:empty",minecraft:custom_data={rpg_pr_guard:1b}]
