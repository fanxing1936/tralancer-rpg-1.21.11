function rpg:forge/wb/new
function rpg:forge/wb/load_off
execute unless data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.pq store result entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.pq int 1 run random value -10..15
function rpg:forge/wb/save_off
function rpg:forge/wb/close
playsound minecraft:block.amethyst_block.resonate master @s ~ ~ ~ 1 1.2
scoreboard players set @s rpg_ob 9
function rpg:onboard/show
