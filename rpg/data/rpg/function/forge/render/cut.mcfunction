execute if score #ln rpg_fg matches ..0 run return 0
data remove entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:lore"[-1]
scoreboard players remove #ln rpg_fg 1
function rpg:forge/render/cut
