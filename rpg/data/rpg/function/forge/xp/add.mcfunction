# 工作台里的装备加 #xa 点经验；升了几级记在 #up。
scoreboard players set #up rpg_fg 0
execute store result score #lv rpg_fg run data get entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.lv
execute if score #lv rpg_fg matches 10.. run return 0
execute store result score #xp rpg_fg run data get entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.xp
scoreboard players operation #xp rpg_fg += #xa rpg_fg
function rpg:forge/xp/loop
execute store result entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.lv int 1 run scoreboard players get #lv rpg_fg
execute store result entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.xp int 1 run scoreboard players get #xp rpg_fg
function rpg:forge/render
