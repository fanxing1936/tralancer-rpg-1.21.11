$data remove entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".$(key)
$data modify storage rpg:forge mig.src set value "$(src)"
scoreboard players set #mname rpg_fg 1
