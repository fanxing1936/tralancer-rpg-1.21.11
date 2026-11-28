$scoreboard players set #cur rpg_say $(sid)
$scoreboard players set #f rpg_say $(f)
$execute in minecraft:overworld positioned $(x) $(y) $(z) run function rpg:town/say/dispatch
