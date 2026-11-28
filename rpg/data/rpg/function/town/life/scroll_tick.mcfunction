# 每秒（as/at 念着余烬归途的人）
execute store result score #x rpg_tl run data get entity @s Pos[0] 4
execute store result score #z rpg_tl run data get entity @s Pos[2] 4
execute unless score #x rpg_tl = @s rpg_tl_px run return run function rpg:town/life/scroll_stop
execute unless score #z rpg_tl = @s rpg_tl_pz run return run function rpg:town/life/scroll_stop
execute if score @s rpg_tl_dmg matches 1.. run return run function rpg:town/life/scroll_stop
scoreboard players remove @s rpg_tl_cht 1
particle minecraft:small_flame ~ ~1 ~ 0.4 0.6 0.4 0.01 14
particle minecraft:ash ~ ~1 ~ 0.4 0.6 0.4 0 10
title @s actionbar ["",{"text":"余烬归途：站着别动…… ","color":"#C9A646","bold":false,"italic":false},{"score":{"name":"@s","objective":"rpg_tl_cht"},"color":"#C9A646"}]
execute if score @s rpg_tl_cht matches ..0 run function rpg:town/life/scroll_go
