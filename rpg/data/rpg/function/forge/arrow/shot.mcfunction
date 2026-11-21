# 刚松手：给附近还没登记的箭打上标记，按品质与等级放大伤害。
scoreboard players set @s rpg_fg_shot 60
scoreboard players set @s rpg_fg_crit 0
execute unless entity @s[tag=rpg.fg.k.ranged] run return 0
function rpg:forge/wb/new
function rpg:forge/wb/load_main
execute store result score #fac rpg_fg run data get entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.fac
function rpg:forge/wb/close
execute if score #fac rpg_fg matches ..0 run scoreboard players set #fac rpg_fg 100
scoreboard players operation #me rpg_fg = @s rpg_fg_id
scoreboard players set #met rpg_fg 0
execute if entity @s[tag=rpg.fg.r.meteor,x_rotation=-90..-45] run scoreboard players set #met rpg_fg 1
execute as @e[type=#minecraft:arrows,distance=..6,tag=!rpg.fg.a] run function rpg:forge/arrow/tag
