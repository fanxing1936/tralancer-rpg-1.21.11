data remove entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".blow_tag
scoreboard players add #mstrip rpg_fg 3
data modify storage rpg:forge mig.refund append value {k:"rune_execute"}
