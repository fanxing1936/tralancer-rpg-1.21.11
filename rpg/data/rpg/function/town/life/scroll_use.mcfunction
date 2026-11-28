advancement revoke @s only rpg:town/scroll
execute if entity @s[tag=rpg.tl.ch] run return 0
execute unless score @s rpg_tw_home matches 1.. run return run tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  你还没有故乡。","color":"#FF6B5E","bold":false,"italic":false}]
tag @s add rpg.tl.ch
scoreboard players set @s rpg_tl_cht 5
scoreboard players set @s rpg_tl_dmg 0
execute store result score @s rpg_tl_px run data get entity @s Pos[0] 4
execute store result score @s rpg_tl_pz run data get entity @s Pos[2] 4
playsound minecraft:block.campfire.crackle player @s ~ ~ ~ 1 0.8
title @s actionbar ["",{"text":"余烬归途：站着别动…… 5","color":"#C9A646","bold":false,"italic":false}]
