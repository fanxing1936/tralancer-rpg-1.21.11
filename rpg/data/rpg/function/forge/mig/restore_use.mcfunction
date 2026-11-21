# 旧符石把自己的右键组件盖在武器上：按物品身份还原，查不到就去掉。
scoreboard players set #ru rpg_fg 0
execute if score #ru rpg_fg matches 0 if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".night_tag run function rpg:forge/mig/use_night_tag
execute if score #ru rpg_fg matches 0 if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".typhoon_tag run function rpg:forge/mig/use_typhoon_tag
execute if score #ru rpg_fg matches 0 if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".ashes_tag run function rpg:forge/mig/use_ashes_tag
execute if score #ru rpg_fg matches 0 if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".blil_tag run function rpg:forge/mig/use_blil_tag
execute if score #ru rpg_fg matches 0 if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".jachin_tag run function rpg:forge/mig/use_jachin_tag
execute if score #ru rpg_fg matches 0 if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".leviathan_tag run function rpg:forge/mig/use_leviathan_tag
execute if score #ru rpg_fg matches 0 if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".forge_tag run function rpg:forge/mig/use_forge_tag
execute if score #ru rpg_fg matches 0 if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".dawn_tag run function rpg:forge/mig/use_dawn_tag
execute if score #ru rpg_fg matches 0 run data remove entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:consumable"
execute if score #ru rpg_fg matches 0 run data remove entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:food"
