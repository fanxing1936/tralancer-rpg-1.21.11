function rpg:forge/wb/new
function rpg:forge/wb/load_off
data modify storage rpg:forge e set from entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq
scoreboard players set #do rpg_fg 1
function rpg:forge/op/stone/do_rift
function rpg:forge/wb/save_off
function rpg:forge/wb/close
scoreboard players set #ok rpg_ob 1
