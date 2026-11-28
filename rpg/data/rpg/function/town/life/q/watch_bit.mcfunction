$scoreboard players set #b rpg_tl $(b)
scoreboard players operation #x rpg_tl = @s rpg_tl_wt
scoreboard players operation #x rpg_tl /= #b rpg_tl
scoreboard players operation #x rpg_tl %= #2 rpg_tw
execute if score #x rpg_tl matches 1 run return 0
scoreboard players operation @s rpg_tl_wt += #b rpg_tl
title @s actionbar ["",{"text":"守夜：这一处看过了","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_tl_wt matches 1 run function rpg:town/life/q/watch_grave
execute if score @s rpg_tl_wt matches 15 run scoreboard players set @s rpg_tl_q3 16
execute if score @s rpg_tl_wt matches 15 run tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  四处都走过了，回去找守夜人。","color":"#C9A646","bold":false,"italic":false}]
