function rpg:forge/wb/new
function rpg:forge/wb/load_off
data modify storage rpg:forge e set from entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq
execute unless data storage rpg:forge e{gild:1b} run function rpg:forge/op/gild/do
function rpg:forge/wb/save_off
function rpg:forge/wb/close
scoreboard players set @s rpg_ob 11
function rpg:onboard/show
